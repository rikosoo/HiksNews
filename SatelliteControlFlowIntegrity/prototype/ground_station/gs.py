"""Ground station simulator.

Speaks the telecommand protocol to the flight software over the emulated
UART / radio link (a TCP socket exposed by QEMU's serial port).
"""
from __future__ import annotations

import socket
import struct
import subprocess
import time

SYNC = b"\xeb\x90"

APID_ADCS_MODE = 0x10
APID_TM_BEACON = 0x20
APID_EPS_REPORT = 0x30
APID_PLD_CAPT = 0x40


def frame(apid: int, payload: bytes) -> bytes:
    """Build a telecommand frame. LEN is one byte, hence the 255 limit."""
    if len(payload) > 255:
        raise ValueError("payload exceeds the 1-byte LEN field")
    return SYNC + bytes([apid, len(payload)]) + payload


class Symbols:
    """Symbol table of the flight software image, read from the ELF."""

    def __init__(self, elf: str, cross: str = "arm-none-eabi-"):
        self.elf = elf
        out = subprocess.check_output([cross + "nm", elf], text=True)
        self._syms = {}
        for line in out.splitlines():
            parts = line.split()
            if len(parts) == 3:
                self._syms[parts[2]] = int(parts[0], 16)

    def addr(self, name: str) -> int:
        return self._syms[name]

    def thumb(self, name: str) -> int:
        """Address with the Thumb bit set, as required by BX/POP-into-PC."""
        return self._syms[name] | 1


class GroundStation:
    def __init__(self, host: str = "127.0.0.1", port: int = 5555):
        self.host, self.port = host, port
        self.sock: socket.socket | None = None
        self.rx = bytearray()

    def connect(self, timeout: float = 15.0) -> None:
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                self.sock = socket.create_connection((self.host, self.port), 2.0)
                self.sock.settimeout(0.2)
                return
            except OSError:
                time.sleep(0.2)
        raise TimeoutError(f"no uplink to {self.host}:{self.port}")

    def send(self, data: bytes) -> None:
        assert self.sock is not None
        self.sock.sendall(data)

    def pump(self, seconds: float) -> str:
        """Collect downlinked telemetry for a while."""
        assert self.sock is not None
        end = time.time() + seconds
        while time.time() < end:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                self.rx += chunk
            except socket.timeout:
                pass
        return self.rx.decode("utf-8", "replace")

    def close(self) -> None:
        if self.sock:
            self.sock.close()
