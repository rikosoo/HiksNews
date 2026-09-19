#!/usr/bin/env python3
"""On-line control-flow violation detector.

Consumes an execution trace of the flight software - here QEMU's block trace,
standing in for the ARM CoreSight ETM/MTB stream on real silicon - and checks
every observed control transfer against the static model produced by
cfg_extract.py.

  python3 monitor/cfi_monitor.py out/cfg.json out/atk1.trace

The monitor never runs in the address space of the firmware it watches: it
only sees the trace. A compromised flight image therefore cannot silence it.
"""
from __future__ import annotations

import argparse
import json
import re
import sys

TRACE_RE = re.compile(r"^Trace \d+: 0x[0-9a-f]+ \[[0-9a-f]+/([0-9a-f]{16})/")

COND_BRANCH = {
    "beq", "bne", "bcs", "bhs", "bcc", "blo", "bmi", "bpl", "bvs", "bvc",
    "bhi", "bls", "bge", "blt", "bgt", "ble", "cbz", "cbnz",
}
UNCOND_BRANCH = {"b"}
CALLS = {"bl", "blx"}
INDIRECT = {"bx", "blx", "tbb", "tbh"}


def is_transfer(insn: dict) -> bool:
    m, ops = insn["mnem"], insn["ops"]
    if m in COND_BRANCH or m in UNCOND_BRANCH or m in CALLS or m in INDIRECT:
        return True
    if m == "pop" and "pc" in ops:
        return True
    if m in ("ldr", "mov", "add") and ops.startswith("pc"):
        return True
    return False


class Policy:
    def __init__(self, model: dict):
        self.insns = {int(k, 16): v for k, v in model["instructions"].items()}
        self.direct = {int(k, 16): set(v) for k, v in model["direct_edges"].items()}
        self.indirect_sites = {int(a, 16) for a in model["indirect_sites"]}
        self.indirect_allowed = {int(a, 16) for a in model["indirect_allowed"]}
        self.ret_allowed = {int(k, 16): {int(t, 16) for t in v}
                            for k, v in model["return_allowed"].items()}
        self.handlers = {int(a, 16) for a in model["exception_handlers"]}
        hmap = model.get("exception_handler_map", {})
        self.handler_addr = {n: int(a, 16) for n, a in hmap.items()}
        self.pendsv = self.handler_addr.get("xPortPendSVHandler")
        self.handler_funcs = {v["func"] for a, v in self.insns.items()
                              if int(a) in self.handlers} if False else set()

        self.exc: "ExceptionState | None" = None
        entry_to_func = {int(v, 16): k for k, v in model["func_entry"].items()}
        self.handler_funcs = {entry_to_func[h] for h in self.handlers
                              if h in entry_to_func}

        # A handler that contains no return instruction cannot perform an
        # exception return: Reset_Handler falls into main(), HardFault_Handler
        # and default_handler spin forever. Derived from the disassembly rather
        # than from a list of names.
        funcs_with_returns = {self.insns[a]["func"] for a in self.ret_allowed
                              if a in self.insns}
        self.returning_handlers = self.handler_funcs & funcs_with_returns

        # Coarse-grained fallback for returns out of functions that are only
        # ever called indirectly: any legitimate return site in the image.
        self.all_return_sites = {int(a, 16)
                                 for a in model.get("indirect_call_returns", [])}
        for targets in self.ret_allowed.values():
            self.all_return_sites |= targets
        for site, targets in self.direct.items():
            insn = self.insns.get(site)
            if insn and insn["mnem"] in CALLS:
                self.all_return_sites.add(site + insn["size"])

    def extent(self, block_start: int) -> tuple[int, int]:
        """Linear span of a block: [start, end) up to and including its
        terminating instruction. A task parked by a context switch resumes
        somewhere inside this span."""
        pc = block_start
        while True:
            insn = self.insns.get(pc)
            if insn is None:
                return block_start, pc
            pc += insn["size"]
            if is_transfer(insn):
                return block_start, pc

    def resume_set(self, block_start: int) -> tuple[int, int, set]:
        """Where control may legitimately resume after an interrupt that hit
        while `block_start` was running.

        Two cases, both bounded by the model:
          * the interrupt landed inside the block -> resume within its span;
          * the interrupt landed on the block boundary, before the successor
            ran -> resume at a CFG successor of the block's terminator.
        """
        lo, hi = self.extent(block_start)
        term = lo
        pc = lo
        while pc < hi:
            term = pc
            pc += self.insns[pc]["size"]

        succs: set = set()
        if term in self.direct:
            succs |= self.direct[term]
        elif term in self.ret_allowed:
            succs |= (self.ret_allowed[term] or self.all_return_sites)
        elif term in self.indirect_sites:
            succs |= self.indirect_allowed
        return lo, hi, succs

    def terminator(self, block_start: int, dest: int) -> tuple[int | None, int]:
        """Walk forward from a traced block start to its terminating transfer.

        Returns (terminator address or None if the block simply falls through
        into dest, number of instructions walked).
        """
        pc, steps = block_start, 0
        while True:
            insn = self.insns.get(pc)
            if insn is None:
                return None, steps
            steps += 1
            if is_transfer(insn):
                return pc, steps
            pc += insn["size"]
            if pc == dest:
                return None, steps          # fall-through / early block end

    def check(self, block_start: int, dest: int) -> tuple[bool, str, int]:
        # An emulated block re-entered at its own start address is a trace
        # artefact: QEMU abandons a block when an interrupt arrives and
        # replays it from the top. Real ETM emits an explicit exception
        # packet instead, so this case does not exist on hardware.
        if dest == block_start:
            return True, "block-restart", 0

        site, steps = self.terminator(block_start, dest)
        if site is None:
            return True, "fallthrough", steps

        insn = self.insns[site]
        func = insn["func"]

        # Exception entry: the branch is performed by hardware and starts from
        # no program instruction, so it is legal from anywhere. What it is NOT
        # is free: the interrupted address is recorded so the matching return
        # can be checked.
        if dest in self.handlers:
            if self.exc is not None:
                return True, self.exc.on_entry(block_start, dest), steps
            return True, "exception-entry", steps

        # Exception return. Only the handler's own return instruction performs
        # one - its internal branches and its calls are ordinary control flow
        # and stay subject to the normal checks below.
        if func in self.returning_handlers and site in self.ret_allowed:
            if self.exc is None:
                return True, "exception-return", steps      # legacy: exempt
            ok, kind = self.exc.on_return(dest)
            return ok, kind, steps

        if site in self.direct:
            ok = dest in self.direct[site]
            return ok, "direct" if ok else "ILLEGAL-DIRECT", steps

        if site in self.ret_allowed:
            allowed = self.ret_allowed[site] or self.all_return_sites
            ok = dest in allowed
            return ok, "return" if ok else "ILLEGAL-RETURN", steps

        if site in self.indirect_sites:
            ok = dest in self.indirect_allowed
            return ok, "indirect" if ok else "ILLEGAL-INDIRECT", steps

        return True, "unmodelled", steps


class ExceptionState:
    """Interrupt- and scheduling-aware exception checking.

    Adapted from the algorithm in SHERLOC (Tan & Zhao, CCS '23, Apache-2.0),
    reimplemented here for a block-granular trace.

    Without this, an exception return is accepted from anywhere, because the
    restored PC comes from hardware and appears in no CFG. With it, a return
    out of a handler must land on one of three things:

      1. the address that was interrupted   -> the shadow stack top;
      2. another handler entry              -> nested exception;
      3. the resume point of a task that a  -> the suspended set, populated
         context switch previously parked      when PendSV preempts a task.

    Anything else is a control-flow violation. QEMU restarts an abandoned
    translation block from its start, so the block address pushed on entry is
    exactly the address control returns to - which is what makes the shadow
    stack work at block granularity.
    """

    def __init__(self, policy: "Policy"):
        self.p = policy
        # Interrupted code spans, innermost last. A span rather than a single
        # address because the trace is block-granular: the interrupt lands
        # mid-block and control resumes at the next instruction, not at the
        # block start. Real ETM/MTB reports the exact interrupted address and
        # would allow the tighter equality test SHERLOC uses.
        self.shadow: list[tuple[int, int, set]] = []
        # Tasks parked by a context switch, as the [start, end) span of the
        # block each was executing. A task yields mid-block (the store to the
        # NVIC that raises PendSV) and resumes at the next instruction, so the
        # resume point is inside the span rather than at its start.
        self.parked: list[tuple[int, int, set]] = []
        self.stats = {"irq_in": 0, "irq_return": 0, "nested": 0,
                      "ctx_switch": 0, "task_resume": 0, "task_start": 0}

    def on_entry(self, src_block: int, dst: int) -> str:
        """An exception was taken: src_block was interrupted, dst is a handler."""
        if self.p.pendsv is not None and dst == self.p.pendsv:
            # Context switch: the running task is parked, not merely interrupted.
            # Cortex-M tail-chains exceptions: SysTick can hand straight over
            # to PendSV without returning to the task first. In that case the
            # source is inside a handler and the task's own address is already
            # on the shadow stack - parking a span inside the handler would
            # pollute the set and consume a later, legitimate return.
            src_fn = self.p.insns.get(src_block, {}).get("func")
            if src_fn not in self.p.handler_funcs:
                self.parked.append(self.p.resume_set(src_block))
            if self.shadow:
                self.parked.append(self.shadow.pop())
            self.stats["ctx_switch"] += 1
            return "context-switch-in"
        self.shadow.append(self.p.resume_set(src_block))
        self.stats["irq_in"] += 1
        return "exception-entry"

    def on_return(self, dst: int) -> tuple[bool, str]:
        """A handler is returning. Only three destinations are legitimate."""
        if self.shadow:
            lo, hi, succs = self.shadow[-1]
            if (lo <= dst < hi) or dst in succs:
                self.shadow.pop()
                self.stats["irq_return"] += 1
                return True, "exception-return"
        if dst in self.p.handlers:
            self.stats["nested"] += 1
            return True, "nested-exception"
        for i, (lo, hi, succs) in enumerate(self.parked):
            if (lo <= dst < hi) or dst in succs:
                self.parked.pop(i)
                self.stats["task_resume"] += 1
                return True, "task-resume"
        # A task running for the first time resumes at its own entry point,
        # which FreeRTOS placed in the stack frame it built at xTaskCreate.
        # Those entries are address-taken in the image, so the model already
        # knows them - no hard-coded task list.
        if dst in self.p.indirect_allowed:
            self.stats["task_start"] += 1
            return True, "task-start"
        return False, "ILLEGAL-EXCEPTION-RETURN"


def stream_blocks(path: str):
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            m = TRACE_RE.match(line)
            if m:
                yield int(m.group(1), 16)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("trace")
    ap.add_argument("--max-report", type=int, default=5)
    ap.add_argument("--cpu-hz", type=float, default=25e6)
    ap.add_argument("--since-func", default="tc_copy",
                    help="measure detection latency from the last block of "
                         "this function (the corrupting write)")
    ap.add_argument("--json", help="write machine-readable results here")
    ap.add_argument("--exceptions", choices=["checked", "exempt"], default="checked",
                    help="checked: verify exception returns against a shadow "
                         "stack (default); exempt: accept them unconditionally, "
                         "the weaker policy, kept for comparison")
    args = ap.parse_args()

    with open(args.model) as fh:
        policy = Policy(json.load(fh))
    if args.exceptions == "checked":
        policy.exc = ExceptionState(policy)

    func_of = {}
    for a, i in policy.insns.items():
        func_of[a] = i["func"]

    prev = None
    n_blocks = 0
    n_insns = 0
    violations = []
    last_since = None            # (block index, instruction count)

    for pc in stream_blocks(args.trace):
        n_blocks += 1
        if func_of.get(pc) == args.since_func:
            last_since = (n_blocks, n_insns)
        if prev is not None:
            ok, kind, steps = policy.check(prev, pc)
            n_insns += steps
            if not ok:
                violations.append({
                    "index": n_blocks,
                    "instr": n_insns,
                    "lat_blocks": (n_blocks - last_since[0]) if last_since else None,
                    "lat_instr": (n_insns - last_since[1]) if last_since else None,
                    "from": prev,
                    "to": pc,
                    "kind": kind,
                    "from_func": func_of.get(prev, "?"),
                    "to_func": func_of.get(pc, "?"),
                })
        prev = pc

    print("=" * 72)
    print(f"trace              : {args.trace}")
    print(f"blocks executed    : {n_blocks}")
    print(f"instructions seen  : {n_insns}")
    print(f"exception policy   : {args.exceptions}")
    if policy.exc is not None:
        st = policy.exc.stats
        print(f"exceptions seen    : {st['irq_in']} entries, "
              f"{st['irq_return']} returns, {st['nested']} nested, "
              f"{st['ctx_switch']} context switches, "
              f"{st['task_resume']} task resumes, "
              f"{st['task_start']} task starts")
    print(f"violations         : {len(violations)}")
    print("=" * 72)
    for v in violations[:args.max_report]:
        ms = v["instr"] / args.cpu_hz * 1000.0
        print(f"  [{v['kind']}] {v['from']:#010x} ({v['from_func']}) "
              f"-> {v['to']:#010x} ({v['to_func']})")
        print(f"      block #{v['index']}  ~instr {v['instr']}  "
              f"~t={ms:.3f} ms since boot")
    if len(violations) > args.max_report:
        print(f"  ... {len(violations) - args.max_report} more")

    if violations and violations[0]["lat_instr"] is not None:
        li = violations[0]["lat_instr"]
        print(f"detection latency  : {li} instructions "
              f"({li / args.cpu_hz * 1000.0:.4f} ms at {args.cpu_hz/1e6:.0f} MHz) "
              f"after the corrupting write in {args.since_func}()")

    if args.json:
        import pathlib
        pathlib.Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        with open(args.json, "w") as fh:
            json.dump({
                "trace": args.trace,
                "blocks": n_blocks,
                "instructions": n_insns,
                "violations": [
                    {k: (hex(val) if k in ("from", "to") else val)
                     for k, val in v.items()}
                    for v in violations[:50]
                ],
                "n_violations": len(violations),
            }, fh, indent=2)
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
