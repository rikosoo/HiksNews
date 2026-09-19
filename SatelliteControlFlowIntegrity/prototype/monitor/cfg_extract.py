#!/usr/bin/env python3
"""Static control-flow model extraction (build time).

Disassembles the flight software ELF and emits the policy the on-line monitor
enforces: for every control-transfer instruction, the set of destinations the
program is allowed to reach.

  python3 monitor/cfg_extract.py firmware/build/flight.elf -o out/cfg.json

Design notes
------------
* Forward edges from direct branches and calls are exact: the target is
  encoded in the instruction.
* Forward edges from indirect calls (``blx rN``) are resolved to the set of
  address-taken functions - the coarse-grained approximation that any
  practical CFI implementation has to make.
* Backward edges (returns) are constrained to the return sites of the actual
  callers of the enclosing function.
* Exception entry and exception return are legal from anywhere: the hardware
  performs them and the trace cannot tell them from a jump. This is stated
  explicitly because it is a real gap in the threat coverage, not an
  implementation shortcut.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

FUNC_RE = re.compile(r"^([0-9a-f]{8}) <([^>]+)>:$")
INSN_RE = re.compile(r"^\s*([0-9a-f]+):\s+((?:[0-9a-f]{2,8} )+)\s*(\S+)(?:\s+(.*))?$")
TARGET_RE = re.compile(r"^([0-9a-f]+)\s*(?:<.*>)?$")

COND_BRANCH = {
    "beq", "bne", "bcs", "bhs", "bcc", "blo", "bmi", "bpl", "bvs", "bvc",
    "bhi", "bls", "bge", "blt", "bgt", "ble", "cbz", "cbnz",
}
UNCOND_BRANCH = {"b"}
CALLS = {"bl", "blx"}
INDIRECT = {"bx", "blx", "tbb", "tbh"}


def _base(mnemonic: str) -> str:
    """Strip Thumb width and IT suffixes: 'bls.n' -> 'bls', 'bl.w' -> 'bl'."""
    return mnemonic.split(".")[0]


class Program:
    def __init__(self, elf: str, cross: str = "arm-none-eabi-"):
        self.elf = elf
        self.insns: dict[int, dict] = {}
        self.order: list[int] = []
        self.func_of: dict[int, str] = {}
        self.func_entry: dict[str, int] = {}
        self._disassemble(cross)

    def _disassemble(self, cross: str) -> None:
        out = subprocess.check_output([cross + "objdump", "-d", self.elf], text=True)
        current = "?"
        for line in out.splitlines():
            m = FUNC_RE.match(line)
            if m:
                current = m.group(2)
                self.func_entry[current] = int(m.group(1), 16)
                continue
            m = INSN_RE.match(line)
            if not m:
                continue
            addr = int(m.group(1), 16)
            width = len(m.group(2).replace(" ", "")) // 2
            mnem = _base(m.group(3))
            ops = (m.group(4) or "").strip()
            self.insns[addr] = {
                "mnem": mnem, "raw": m.group(3), "ops": ops,
                "size": width, "func": current,
            }
            self.func_of[addr] = current
            self.order.append(addr)

    # -- classification ---------------------------------------------------
    @staticmethod
    def is_transfer(insn: dict) -> bool:
        m, ops = insn["mnem"], insn["ops"]
        if m in COND_BRANCH or m in UNCOND_BRANCH or m in CALLS or m in INDIRECT:
            return True
        if m == "pop" and "pc" in ops:
            return True
        if m in ("ldr", "mov", "add") and ops.startswith("pc"):
            return True
        return False

    @staticmethod
    def direct_target(insn: dict) -> int | None:
        """Immediate branch/call target, when the instruction encodes one."""
        ops = insn["ops"]
        last = ops.split(",")[-1].strip()
        m = TARGET_RE.match(last)
        if m:
            try:
                return int(m.group(1), 16)
            except ValueError:
                return None
        return None


def build_model(elf: str) -> dict:
    prog = Program(elf)

    call_targets: dict[int, set[int]] = {}   # callee entry -> return sites
    direct_edges: dict[int, set[int]] = {}   # transfer site -> targets
    indirect_sites: list[int] = []
    indirect_call_returns: set[int] = set()
    return_sites: list[int] = []

    for addr in prog.order:
        insn = prog.insns[addr]
        if not Program.is_transfer(insn):
            continue
        mnem, ops = insn["mnem"], insn["ops"]
        nxt = addr + insn["size"]
        tgt = Program.direct_target(insn)

        if mnem in CALLS and tgt is not None:
            direct_edges.setdefault(addr, set()).add(tgt)
            call_targets.setdefault(tgt, set()).add(nxt)
        elif mnem in COND_BRANCH and tgt is not None:
            direct_edges.setdefault(addr, set()).update({tgt, nxt})
        elif mnem in UNCOND_BRANCH and tgt is not None:
            direct_edges.setdefault(addr, set()).add(tgt)
        elif mnem == "pop" and "pc" in ops:
            return_sites.append(addr)
        elif mnem in INDIRECT or (mnem in CALLS and tgt is None):
            if mnem == "bx" and ops.strip() == "lr":
                return_sites.append(addr)
            else:
                indirect_sites.append(addr)
                if mnem == "blx":
                    # An indirect call also creates a legitimate return site.
                    indirect_call_returns.add(nxt)
        else:
            indirect_sites.append(addr)

    # Address-taken functions bound the indirect-call target set.
    address_taken = sorted({t for ts in call_targets.values() for t in ()} |
                           _address_taken(prog))

    # Backward edges: a return may only land on a return site of a caller of
    # the function it is returning from.
    ret_allowed: dict[int, list[int]] = {}
    for site in return_sites:
        fn = prog.func_of[site]
        entry = prog.func_entry.get(fn)
        allowed = call_targets.get(entry, set()) if entry is not None else set()
        ret_allowed[site] = sorted(allowed)

    handlers = _exception_handlers(prog)
    entry_to_name = {v: k for k, v in prog.func_entry.items()}

    return {
        "elf": elf,
        "instructions": {hex(a): {"mnem": i["mnem"], "ops": i["ops"],
                                  "size": i["size"], "func": i["func"]}
                         for a, i in prog.insns.items()},
        "direct_edges": {hex(a): sorted(t) for a, t in direct_edges.items()},
        "indirect_sites": [hex(a) for a in indirect_sites],
        "indirect_allowed": [hex(a) for a in address_taken],
        "indirect_call_returns": [hex(a) for a in sorted(indirect_call_returns)],
        "return_allowed": {hex(a): [hex(t) for t in ts]
                           for a, ts in ret_allowed.items()},
        "exception_handlers": [hex(a) for a in handlers],
        "exception_handler_map": {entry_to_name[h]: hex(h)
                                  for h in sorted(handlers) if h in entry_to_name},
        "func_entry": {k: hex(v) for k, v in prog.func_entry.items()},
    }


def _address_taken(prog: Program) -> set[int]:
    """Functions whose address is materialised into a register.

    In this firmware the only indirect call is the telecommand dispatch, whose
    pointers come from lookup_handler(); its literal pool holds exactly the
    legitimate handlers. We approximate the address-taken set with every
    function entry referenced by a literal load, which is conservative.
    """
    taken: set[int] = set()
    entries = {v for v in prog.func_entry.values()}
    out = subprocess.check_output(
        ["arm-none-eabi-objdump", "-s", "-j", ".text", prog.elf], text=True)
    words: set[int] = set()
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        for chunk in parts[1:5]:
            if len(chunk) == 8:
                try:
                    raw = int(chunk, 16)
                except ValueError:
                    continue
                # little-endian words in the dump
                le = int.from_bytes(raw.to_bytes(4, "big"), "little")
                words.add(le & ~1)
    for e in entries:
        if e in words:
            taken.add(e)
    return taken


def _exception_handlers(prog: Program, cross: str = "arm-none-eabi-") -> set[int]:
    """Entries reachable through the vector table, read from the table itself.

    The vector table is the ground truth for which addresses the hardware may
    branch to. Deriving this from a list of well-known handler names instead
    both misses handlers the application adds and, worse, makes their
    legitimate exception entries look like violations.

    Word 0 of the table is the initial stack pointer, not a handler.
    """
    out = subprocess.check_output(
        [cross + "objdump", "-s", "-j", ".isr_vector", prog.elf], text=True)
    words: list[int] = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) < 2 or len(parts[0]) < 4:
            continue
        try:
            int(parts[0], 16)
        except ValueError:
            continue
        for chunk in parts[1:5]:
            if len(chunk) == 8:
                try:
                    be = int(chunk, 16)
                except ValueError:
                    continue
                words.append(int.from_bytes(be.to_bytes(4, "big"), "little"))

    entries = set(prog.func_entry.values())
    handlers = set()
    for w in words[1:]:                      # skip the initial SP
        a = w & ~1
        if a in entries:
            handlers.add(a)
    return handlers


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("elf")
    ap.add_argument("-o", "--out", default="out/cfg.json")
    args = ap.parse_args()

    model = build_model(args.elf)
    import pathlib
    pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(model, fh)

    print(f"instructions      : {len(model['instructions'])}")
    print(f"direct edges      : {len(model['direct_edges'])}")
    print(f"indirect sites    : {len(model['indirect_sites'])}")
    print(f"allowed indirect  : {len(model['indirect_allowed'])}")
    print(f"return sites      : {len(model['return_allowed'])}")
    print(f"model written to  : {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
