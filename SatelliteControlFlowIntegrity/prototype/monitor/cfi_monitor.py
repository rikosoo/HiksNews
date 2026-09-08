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
        self.handler_funcs = {v["func"] for a, v in self.insns.items()
                              if int(a) in self.handlers} if False else set()

        entry_to_func = {int(v, 16): k for k, v in model["func_entry"].items()}
        self.handler_funcs = {entry_to_func[h] for h in self.handlers
                              if h in entry_to_func}

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

        # Exception entry: performed by hardware, legal from anywhere.
        if dest in self.handlers:
            return True, "exception-entry", steps
        # Exception return: the restored PC is not visible in the model.
        if func in self.handler_funcs:
            return True, "exception-return", steps

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
    args = ap.parse_args()

    with open(args.model) as fh:
        policy = Policy(json.load(fh))

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
