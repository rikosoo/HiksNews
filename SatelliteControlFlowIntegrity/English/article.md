# Control-Flow Violation Detection for Embedded Satellite Flight Software

**Keywords:** space security, embedded systems, control-flow integrity,
ARM Cortex-M, FreeRTOS, hardware trace, CubeSat

---

## Abstract

Small satellites run flight software on microcontrollers without an MMU, with
memory in the tens of kilobytes and a hard power budget — an environment where
conventional defenses against control-flow hijacking are too expensive to fly.
This work asks whether hardware-trace-based detection, in the line of SHERLOC,
transfers to the space domain.

We built a working on-board computer — an ARM Cortex-M3 running FreeRTOS and five
flight tasks (telecommand reception, attitude control, power, telemetry and
payload) — and injected a single controlled parsing vulnerability into it. On top
of that one flaw we implemented five distinct attacks: buffer overflow, function
pointer corruption, ROP chain, malicious task scheduling, and unauthorized
privileged execution. An external monitor extracts the control-flow graph from
the binary at build time and checks the execution trace against it.

The monitor detected **5 of 5 attacks**, with **zero false positives** across 1.4
million blocks of legitimate execution, and a detection latency between 0.001 and
0.052 ms — roughly two orders of magnitude below the attitude control loop
period. Because the firmware is never instrumented, the on-board cost is **0%
CPU, 0 KB flash and 0 KB RAM**; the cost migrates entirely to trace channel
bandwidth, which we identify as the dominant practical limitation.

We also deliberately implemented a sixth scenario outside the technique's reach:
a data-only attack that compromises the mission without diverting control flow.
The monitor does not detect it, and could not. That boundary is part of the
result.

---

## 1. Introduction

Orbital infrastructure is no longer an isolated domain. Low Earth Orbit
constellations underpin communications, navigation and Earth observation, and the
February 2022 attack on Viasat's KA-SAT network showed the sector to be a real
target with operational effect at scale — including spillover into civil
infrastructure, as 5,800 wind turbines in Germany lost remote monitoring [12].

Precision matters here: that attack bricked **ground modems**, through a
misconfigured VPN appliance in the management segment; it was not a compromise
of on-board firmware. It motivates this work by demonstrating capable and
interested adversaries in the space domain, not by being an instance of the
threat we attack here.

What makes the space domain distinct is not the nature of the vulnerabilities —
buffer overflows in protocol parsers are the same as in any embedded system — but
the **constraints the defense must operate under**:

| Constraint | Consequence for the defense |
|---|---|
| MCU without MMU | No strong isolation between RTOS tasks |
| Tens to hundreds of KB of RAM | Shadow stacks and heavy instrumentation are infeasible |
| Hard power budget | CPU overhead carries real thermal and electrical cost |
| Short contact window | Human incident response is slow or impossible |
| Expensive, risky firmware updates | Post-incident fixes take months |
| Irreversible actions | Cutting bus power ends the mission |

The last item reorders the priorities. On a server, detecting late still allows
remediation. On a satellite, a critical function executed once can end the
mission. **Detecting at the moment of the deviation is worth more than remediating
afterwards** — and that is the gap motivating this work.

### Research question

> Can SHERLOC-like techniques be adapted to detect attacks against the firmware
> of embedded space systems?

### Contributions

1. A working on-board computer, from bare-metal bring-up to FreeRTOS flight
   software, built specifically as a security measurement target.
2. Five reproducible control-flow attacks, all riding the same injected
   vulnerability, isolating the type of deviation as the only variable.
3. A trace-based detector with no firmware instrumentation: static CFG extraction
   and external verification.
4. Quantitative evaluation under flight-relevant metrics: detection, false
   positives, latency, and CPU, flash and memory overhead.
5. An explicit demonstration of the technique's boundary, via a data-only attack
   that compromises the mission undetected.

---

## 2. Background

### 2.1 Typical on-board computer architecture

```
Ground station
      |  telecommand (TC)
      v
Communications module
      v
ARM Cortex-M
      v
FreeRTOS
      v
Flight software
      v
+---------------------------------+
| ADCS | Telemetry | EPS | Payload |
+---------------------------------+
```

Telecommands arrive over RF, are unpacked by a communications module and handed
to the flight software, which interprets them and drives the subsystems. The
telecommand parser is therefore the boundary where attacker-controlled data meets
privileged code.

### 2.2 Control-flow hijacking on embedded targets

On ARM the return address lives in the `lr` register. A leaf function keeps it in
a register and is immune to the classic stack attack; a function that calls others
must preserve it on the stack (`push {r7, lr}`), and it is that copy an overflow
reaches. The Cortex-M executes only the Thumb instruction set, and bit 0 of an
address loaded into `PC` selects the instruction state — an address with that bit
clear faults instead of executing the target.

The absence of an MMU means there is no address-space separation between tasks:
isolation rests entirely on the MPU, which is optional and frequently unused.

### 2.3 Hardware trace on Cortex-M

Cortex-M cores expose, through CoreSight [6, 7], the **ETM** (Embedded Trace Macrocell),
which emits a compressed stream of taken branches, and the **MTB** (Micro Trace
Buffer), a circular buffer in RAM. Both operate **outside the firmware's execution
domain**: compromised firmware cannot forge its own trace. This property is what
grounds the approach — the detector trusts nothing running in the domain it
observes.

---

## 3. Threat model

**Assumed attacker capabilities:**

- **A1 — Hostile uplink.** Can inject malformed telecommands, whether through a
  compromised ground station, RF spoofing, or abuse of a legitimate operator.
- **A2 — Firmware knowledge.** Knows the binary, whether COTS, open source, or
  leaked through the supply chain.
- **A3 — No physical access.** Cannot reprogram over JTAG after launch.
- **A4 — No crypto break.** Telecommand authentication, where present, is the
  boundary; the attack happens **after** parsing.

**Out of scope:** jamming, physical attacks, compromise of the ground station
itself (a premise, not a target), and side channels.

**Attacker goal:** divert execution into a critical function unreachable from the
parser's legitimate path.

**Defender posture:** the monitor observes only the execution trace. It trusts no
state reported by the firmware.

---

## 4. Target system

We implemented CubeSat-like flight software on QEMU `mps2-an385` (Cortex-M3 at
25 MHz), FreeRTOS Kernel V11.1.0, a 23 KB text image.

| Task | Priority | Period | Role |
|---|---|---|---|
| `tc_rx` | 4 | 2 ms polling | telecommand reception and parsing |
| `adcs` | 3 | 10 ms | attitude control loop |
| `eps` | 2 | 5 s | power monitoring |
| `tm_tx` | 1 | 2 s | telemetry beacon |
| `payload` | 1 | 50 ms | payload |

Priority 5 stays free in nominal operation — a detail that becomes relevant in
Section 5.

**Telecommand format:**

```
+--------+--------+--------+-------------------+
| SYNC   | APID   | LEN    | PAYLOAD (LEN B)   |
| EB 90  | 1 B    | 1 B    | 0..255 B          |
+--------+--------+--------+-------------------+
```

**Critical functions**, unreachable from any legitimate path and present solely as
measurable targets: `eps_kill_switch()` (cuts bus power), `payload_wipe()` (erases
payload memory), `debug_spawn_rogue_task()` (a factory hook left in the image) and
`priv_raw_write_body()` (privileged write).

### 4.1 The controlled vulnerability

A single flaw, in `tc_handle_frame()`: the telecommand `LEN` field is used without
validation as the copy length into a 64-byte stack buffer. The stack frame, read
from the compiled binary:

```
offset  0..63   ctx.buf[64]
offset 64       ctx.handler        <- indirect call target
offset 76       saved r7
offset 80       saved LR           <- popped into PC on return
offset 84/88    gadget frame       <- second ROP stage
```

Concentrating every attack on one flaw is a methodological choice: it isolates the
**type of control-flow deviation** as the experimental variable, removing
input-bug differences as a confounder.

---

## 5. The five attacks

| ID | Attack | Mechanism | Mission effect |
|---|---|---|---|
| ATK-1 | Buffer overflow | overwrites the saved LR | bus power cut |
| ATK-2 | Function pointer corruption | overwrites the dispatch pointer | payload memory erased |
| ATK-3 | ROP chain | two stages via a `pop {r7, pc}` gadget | payload memory erased |
| ATK-4 | Malicious task scheduling | diverts into a residual debug hook | pointing lost |
| ATK-5 | Unauthorized privileged function | enters the body past the auth check | privileged write without auth |

Two deserve comment.

**ATK-3** injects no code: it reuses what is already in the image. The
`pop {r7, pc}` gadget (Thumb encoding `0xbd80`) is the standard epilogue of every
non-leaf function compiled without optimization — the binary offers 148 of them.
This is why preventing code injection is not sufficient.

**ATK-4** runs no shellcode and corrupts no mission data: it uses the **scheduler
as the weapon**. The task it creates at priority 5 sits above the ADCS at priority
3, and the attitude control loop simply stops being scheduled. The consequence is
not "code executed" but loss of pointing — followed by loss of link and of power
generation.

---

## 6. The detector

### 6.1 Static phase (build time)

`cfg_extract.py` disassembles the ELF and emits the allowed-edge policy:

- **Direct edges** (`b`, `bl`, conditionals): exact target encoded in the
  instruction.
- **Indirect calls** (`blx rN`): approximated by the set of functions whose
  address is materialized in the image — the conservative approximation every
  practical CFI implementation must make.
- **Returns**: restricted to the return sites of the function's actual callers.
- **Exception entry and return**: accepted unconditionally (see 6.3).

On the evaluated image: 9,716 instructions, 1,156 direct branch sites, 3 indirect
sites, 148 return sites. Extraction takes 0.3 s.

### 6.2 Dynamic phase (runtime)

`cfi_monitor.py` consumes the execution trace — here QEMU's block log, standing in
for the ETM stream — reconstructs each transition and checks it against the
policy. The monitor **does not run in the firmware's address space**: compromised
flight software cannot silence it.

### 6.3 What is accepted without checking

Two classes of transition are accepted unconditionally, and declaring them is part
of the result — not least because this is where SHERLOC [3] is ahead of this
prototype: it solves the problem with an interrupt- and scheduling-aware
detection algorithm, whereas our monitor simply exempts both cases. That is a gap
of ours relative to the state of the art, not a difference in scope.

- **Exception entry**: the branch is performed by hardware and originates from no
  program instruction; no CFG contains it.
- **Exception return**: the restored `PC` is not in the model. The sharpest case is
  `PendSV`, which switches the running task — without this exemption every context
  switch would be a false positive, at 1 kHz.

These are real coverage gaps, not implementation shortcuts.

### 6.4 Incident response

The response policy is a mission decision, not the detector's:

| Tier | Action |
|---|---|
| L0 | Log to security telemetry |
| L1 | Quarantine the affected subsystem |
| L2 | Enter safe mode (stable attitude, radio up, payload off) |
| L3 | Restart from a trusted image |

The separation matters: a false positive that triggers L3 carries a real
operational cost, measured in mission days.

---

## 7. Evaluation

### 7.1 Per-scenario results

| Scenario | Compromised | Violations | Detected | Latency (instr) | Latency (ms) |
|---|---|---|---|---|---|
| S0 — nominal telecommands | no | 0 | n/a | — | — |
| S1 — malformed, rejected | no | 0 | n/a | — | — |
| S4 — sustained load | no | 0 | n/a | — | — |
| ATK-1 — buffer overflow | yes | 1 | **YES** | 1230 | 0.0492 |
| ATK-2 — function pointer | yes | 1 | **YES** | 26 | 0.0010 |
| ATK-3 — ROP | yes | 2 | **YES** | 1303 | 0.0521 |
| ATK-4 — task scheduling | yes | 1 | **YES** | 1230 | 0.0492 |
| ATK-5 — privileged function | yes | 2 | **YES** | 1230 | 0.0492 |
| **S5 — data-only attack** | **yes** | **0** | **NO** | — | — |

ATK-3 and ATK-5 produce two violations because the deviation has two stages; these
are edges of the same attack, not independent alerts.

### 7.2 Summary metrics

| Metric | Value |
|---|---|
| Attack detection | **5/5 (100%)** |
| False positives | **0** across 1.4 M blocks (S0, S1, S4) |
| Detection latency | 26–1303 instructions (0.001–0.052 ms at 25 MHz) |
| On-board CPU overhead | **0%** |
| On-board flash overhead | **0 KB** |
| On-board memory overhead | **0 KB** |
| CFG model (monitor side) | 940 KB |
| Monitor throughput | ~31 MB of trace/s |

### 7.3 Reading the results

**Zero on-board overhead is the central result, and it is a structural property,
not an optimization.** The firmware is not instrumented; the detector consumes the
trace the hardware already produces. On a satellite, where flash and RAM are fixed
before launch and every CPU cycle carries thermal and electrical cost, a scheme
charging 0 KB and 0% on the board is qualitatively different from one charging
5–15%.

The cost does not vanish: it **migrates entirely to trace channel bandwidth.** One
second of emulated flight produced roughly 200 MB of raw QEMU trace. That is the
dominant practical limitation and the next experimental item.

**Latency fits the real-time budget.** The measured worst case, 0.052 ms, is about
190 times smaller than the ADCS loop period (10 ms). There is headroom to trigger
containment before the next control cycle — which is what separates "detecting"
from "containing".

**ATK-2 is detected 47 times faster** than the return-based attacks (26 versus
~1230 instructions). All corrupt the stack at the same instant; the difference is
*when the corrupted value is consumed*. The function pointer is used immediately
at the indirect call; the return address is only consumed at the epilogue, after
the legitimate handler has run in full. **Detection latency is a property of the
attack, not only of the detector.**

### 7.4 The boundary: scenario S5

S5 was built to fail. A second controlled vulnerability — an out-of-bounds write
into a mission parameter table — lets two **perfectly well-formed** telecommands
compromise the satellite:

1. `param_set(index=8)` writes past the end of the table and lands on the
   `authenticated` field of the adjacent configuration block.
2. A legitimate privileged telecommand then passes the authentication check it
   should have failed.

No illegal edge is executed, because **every edge is legal**. The monitor reports
zero violations. The satellite keeps transmitting telemetry normally — there is not
even a visible fault. The mission is compromised.

This is the limit of the approach, and it is structural: a control-flow detector
cannot see an attack that does not divert control flow. Reporting it as a result,
rather than omitting it, is what separates an evaluation from a demonstration.

---

## 8. Discussion

### 8.1 Attack or radiation?

A radiation-induced Single Event Upset can corrupt a return address with no
adversary involved. To the detector, both situations produce the **same
signature**: an edge the CFG does not allow.

This is not merely noise. It has a direct operational consequence: the correct
response to an attack (enter safe mode, isolate the uplink) differs from the
correct response to an SEU (correct and continue). Telling them apart requires
correlation with other sources — ECC counters, orbital position relative to the
South Atlantic Anomaly, historical event rate — and is out of scope for this
prototype. It is, in our assessment, the most interesting research question the
work opens.

### 8.2 The cost of a false positive

Zero false positives across 1.4 million blocks is encouraging, but the firmware is
small and the load is synthetic. Extrapolating to real flight software is not
valid without repeating the measurement.

The point deserves emphasis because the cost asymmetry is severe: on a satellite, a
false positive that triggers safe mode costs mission days and a contact window for
recovery. A detector with even a low but non-zero false positive rate needs a
tiered response policy — which is why Section 6.4 separates detection from
reaction.

### 8.3 Positioning

Two families of defense compete in this space, and what separates them is where
the cost is paid.

**Kage** [5] protects application and kernel control data on FreeRTOS through
compiler transformation and memory region separation — that is, it pays the cost
**on board**, in flash, RAM and cycles. **SHERLOC** [3] uses hardware trace and
neither instruments the protected software nor changes its memory layout, moving
the cost off the board. This work follows the second family, which is what
explains the zero overhead in Section 7.

Compared to SHERLOC specifically:

| Axis | SHERLOC [3] | This work |
|---|---|---|
| Target | Embedded firmware, ARMv8-M / Cortex-M33 | Flight software on FreeRTOS, Cortex-M3 |
| Evidence | Hardware trace | Hardware trace (QEMU standing in for ETM) |
| Interrupts and context switches | **Handled** by a dedicated algorithm | **Exempted** — declared gap (6.3) |
| Threat | Local or network attacker | Compromised ground station, hostile uplink |
| Response | Alert / halt | Safe mode, quarantine, security telemetry |
| Dominant constraint | Cost and memory | Power, radiation, contact window, irreversibility |
| Validation | Real hardware (V2M-MPS2+) | Emulation |

The contribution is not a new detection technique, and presenting it as one would
be incorrect — in detection capability this prototype sits **behind** SHERLOC,
not ahead of it. The contribution is the transfer to a threat model in which
**incident response cannot depend on immediate human intervention**, the
evaluation under the metrics that context imposes, and the empirical delimitation
of the technique's boundary (Section 7.4).

---

## 9. Limitations

- **Data-only attacks escape by construction** (Section 7.4).
- **Trace volume.** ~200 MB/s from QEMU is infeasible for downlink. Real ETM
  compresses aggressively and the MTB keeps only a circular window, but how much
  trace fits the bandwidth budget remains open.
- **Conservative CFG for indirect calls**, more permissive than the real target
  set.
- **Exception exemption** (Section 6.3) is a declared coverage gap.
- **Power was argued, not measured.** With no on-board instrumentation the added
  board consumption is zero by construction; the trace channel's consumption needs
  hardware measurement.
- **Emulation artifacts.** QEMU restarts blocks on interrupt and, with chaining
  enabled, omits executions — which required `-d exec,nochain`. Neither exists in
  real ETM, but both affect comparability.

### Threats to validity

Small firmware (23 KB) written by the authors: the CFG is simpler and more precise
than that of real flight software. Converting instructions to milliseconds assumes
1 instruction per cycle, which underestimates time on the Cortex-M3. One run per
scenario: latency figures should be read as orders of magnitude, not distribution
means.

---

## 10. Conclusion

**Yes, with a precise boundary.** Trace-based control-flow violation detection
transfers to satellite flight software, and the transfer is favorable: 100%
detection across five distinct attack classes, no false positive on the evaluated
load, latency two orders of magnitude below the attitude control loop, and **zero
CPU, flash and memory cost on board** — the property that makes the approach
plausible under a satellite's power budget and real-time deadlines.

The boundary is equally clear. The technique does not see attacks that do not
divert control flow, and we demonstrated this by compromising the satellite with
two well-formed telecommands without raising a single alert. It also cannot
distinguish an attack from a radiation event — which, in the space domain, is not
a detail.

### Future work

1. **Port to real hardware** with ETM/MTB, and measure the trace channel's energy
   cost — today argued, not measured.
2. **Trace bandwidth budget**: how much trace a satellite can actually process on
   board, and what the MTB's circular window leaves out.
3. **Discriminating attack from SEU**, by correlating ECC counters and orbital
   position.
4. **Data-flow integrity** to cover the S5 class.
5. **Remote attestation over telemetry**, turning the monitor's verdict into
   evidence verifiable at the ground station.
6. **Interrupt and context-switch handling** at SHERLOC's level [3], removing the
   exemption of Section 6.3.
7. **Mapping the covered techniques onto the SPARTA framework** [8], from The
   Aerospace Corporation.

---

## Availability

Firmware, attacks, monitor and measurement harness are in `prototype/`, with a
pinned toolchain and one script per scenario. The raw results table is generated
by `eval/run_matrix.py`.

## Ethical considerations

All work runs on firmware written by the authors, executed in an emulator. No
satellite in orbit, operator, or third-party ground station is involved. The
vulnerabilities are deliberately introduced as measurement targets; no third-party
product flaw is exploited or disclosed.

## References

[1] M. Abadi, M. Budiu, Ú. Erlingsson, J. Ligatti. *Control-Flow Integrity.*
In *Proceedings of the 12th ACM Conference on Computer and Communications
Security (CCS '05)*, Alexandria, VA, USA, Nov. 2005, pp. 340–353.
DOI: 10.1145/1102120.1102165

[2] M. Abadi, M. Budiu, Ú. Erlingsson, J. Ligatti. *Control-Flow Integrity
Principles, Implementations, and Applications.* ACM TISSEC, v. 13, n. 1,
Oct. 2009. DOI: 10.1145/1609956.1609960

[3] X. Tan, Z. Zhao. *SHERLOC: Secure and Holistic Control-Flow Violation
Detection on Embedded Systems.* In *CCS '23*, Copenhagen, Denmark,
26–30 Nov. 2023, pp. 1332–1346. DOI: 10.1145/3576915.3623077

[4] X. Tan, Z. Ma, S. Pinto, L. Guan, N. Zhang, J. Xu, Z. Lin, H. Hu, Z. Zhao.
*SoK: Where's the "up"?! A Comprehensive (bottom-up) Study on the Security of
Arm Cortex-M Systems.* In *18th USENIX WOOT*, 2024, pp. 149–169.

[5] Y. Du, Z. Shen, K. Dharsee, J. Zhou, R. J. Walls, J. Criswell. *Holistic
Control-Flow Protection on Real-Time Embedded Systems with Kage.* In *31st
USENIX Security Symposium*, Boston, MA, USA, Aug. 2022, pp. 2281–2298.

[6] Arm Ltd. *Embedded Trace Macrocell Architecture Specification, ETMv4.0 to
ETMv4.6.* ARM IHI 0064.

[7] Arm Ltd. *CoreSight Architecture Specification.* ARM IHI 0029.

[8] The Aerospace Corporation. *SPARTA — Space Attack Research & Tactic
Analysis.* https://sparta.aerospace.org/

[9] M. Scholl, T. Suloway. *Introduction to Cybersecurity for Commercial
Satellite Operations.* NIST IR 8270, July 2023.

[10] CCSDS. *Space Data Link Security Protocol.* Recommended Standard,
CCSDS 355.0-B-2 (Blue Book), July 2022.

[11] CCSDS. *TC Space Data Link Protocol.* Recommended Standard,
CCSDS 232.0-B-4 (Blue Book), Issue 4, Oct. 2021.

[12] J. A. Guerrero-Saade, M. Hegel. *AcidRain — A Modem Wiper Rains Down on
Europe.* SentinelLabs, 31 Mar. 2022.

[13] F. Bellard. *QEMU, a Fast and Portable Dynamic Translator.* In *USENIX
Annual Technical Conference, FREENIX Track*, 2005, pp. 41–46.

[14] FreeRTOS Kernel V11.1.0. https://github.com/FreeRTOS/FreeRTOS-Kernel
