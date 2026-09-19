#!/usr/bin/env python3
"""Run one experiment scenario end to end.

Boots the flight software under QEMU, opens the simulated radio link, uplinks
the scenario's telecommands, and reports what happened on board.

  python3 eval/run_scenario.py S0
  python3 eval/run_scenario.py ATK-1 --trace out/atk1.trace
"""
from __future__ import annotations

import argparse
import os
import pathlib
import socket
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ground_station"))
sys.path.insert(0, str(ROOT / "attacks"))

import attacks as atk                      # noqa: E402
from gs import GroundStation, Symbols, frame, APID_ADCS_MODE, APID_TM_BEACON, \
    APID_EPS_REPORT, APID_PLD_CAPT        # noqa: E402

ELF = ROOT / "firmware" / "build" / "flight.elf"

# Evidence that a critical function actually executed on board.
COMPROMISE_MARKERS = [
    "EPS KILL SWITCH ENGAGED",
    "PAYLOAD MEMORY WIPED",
    "ROGUE TASK SCHEDULED",
    "PRIVILEGED RAW WRITE EXECUTED",
]


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def nominal_traffic() -> list[bytes]:
    """Well-formed telecommands - the legitimate control-flow paths."""
    return [
        frame(APID_ADCS_MODE, bytes([2])),
        frame(APID_TM_BEACON, b""),
        frame(APID_EPS_REPORT, b""),
        frame(APID_PLD_CAPT, b""),
        frame(APID_ADCS_MODE, bytes([1])),
    ]


def malformed_traffic() -> list[bytes]:
    """Rejected by the parser without any control-flow deviation."""
    return [
        b"\x00\x00\x00\x00",                    # bad sync
        b"\xeb\x90\x99\x02\xAA\xBB",            # unknown APID
        b"\xeb\x90\x10\x00",                    # zero-length payload
    ]


def build_scenario(name: str, sym: Symbols) -> list[bytes]:
    if name == "S0":
        return nominal_traffic()
    if name == "S1":
        return malformed_traffic()
    if name == "S4":
        return nominal_traffic() * 20           # sustained load
    if name == "ATK-1":
        return nominal_traffic() + [frame(APID_ADCS_MODE, atk.atk1_buffer_overflow(sym))]
    if name == "ATK-2":
        return nominal_traffic() + [frame(APID_ADCS_MODE, atk.atk2_function_pointer(sym))]
    if name == "ATK-3":
        gadget = atk.find_pop_r7_pc_gadget(str(ELF))
        return nominal_traffic() + [frame(APID_ADCS_MODE, atk.atk3_rop_chain(sym, gadget))]
    if name == "ATK-4":
        return nominal_traffic() + [frame(APID_ADCS_MODE, atk.atk4_task_scheduling(sym))]
    if name == "ATK-5":
        return nominal_traffic() + [frame(APID_ADCS_MODE, atk.atk5_privileged_call(sym))]
    if name == "ATK-6":
        return nominal_traffic() + [frame(apid, p)
                                    for apid, p in atk.atk6_frames(sym)]
    if name == "S5":
        return nominal_traffic() + [frame(apid, p) for apid, p in atk.s5_data_only()]
    raise SystemExit(f"unknown scenario: {name}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario")
    ap.add_argument("--trace", help="write a QEMU execution trace to this file")
    ap.add_argument("--settle", type=float, default=3.0,
                    help="seconds of telemetry to collect after the uplink")
    args = ap.parse_args()

    if not ELF.exists():
        raise SystemExit(f"build the firmware first: make -C {ELF.parents[1]}")

    sym = Symbols(str(ELF))
    frames = build_scenario(args.scenario, sym)
    port = free_port()

    qemu = [
        "qemu-system-arm", "-M", "mps2-an385", "-cpu", "cortex-m3", "-m", "16m",
        "-nographic", "-monitor", "none", "-kernel", str(ELF),
        "-serial", f"tcp:127.0.0.1:{port},server=on,wait=on",
    ]
    if args.trace:
        pathlib.Path(args.trace).parent.mkdir(parents=True, exist_ok=True)
        qemu += ["-d", "exec,nochain", "-D", args.trace]

    proc = subprocess.Popen(qemu, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    gs = GroundStation(port=port)
    try:
        gs.connect()
        gs.pump(1.5)                       # let the flight software boot
        for f in frames:
            gs.send(f)
            time.sleep(0.15)
        out = gs.pump(args.settle)
    finally:
        gs.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    hits = [m for m in COMPROMISE_MARKERS if m in out]
    print("=" * 68)
    print(f"scenario : {args.scenario}")
    print(f"frames   : {len(frames)}")
    print(f"outcome  : {'COMPROMISED - ' + hits[0] if hits else 'no critical function executed'}")
    if args.trace:
        print(f"trace    : {args.trace}")
    print("=" * 68)
    print(out.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
