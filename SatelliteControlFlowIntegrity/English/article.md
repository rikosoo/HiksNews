# Control-Flow Violation Detection for Embedded Satellite Flight Software

> **Status:** draft / outline. Each section lists what must be written and where
> the evidence comes from.

---

## Abstract
*(to write — 200 words: problem, gap, approach, headline result)*

**Research question:** can SHERLOC-like techniques be adapted to detect attacks
against the firmware of embedded space systems?

---

## 1. Introduction
- Growing dependence on orbital infrastructure (comms, navigation, observation).
- CubeSats and LEO constellations: cheap hardware, complex firmware, wide attack surface.
- What makes the space domain different: irreversibility, contact windows, power budget, radiation.
- Contributions (3–4 bullets).

## 2. Background
### 2.1 Typical on-board computer architecture
*(diagram: ground station → comms module → Cortex-M → FreeRTOS → subsystems)*
### 2.2 Control-flow hijacking on embedded targets
### 2.3 Hardware trace on Cortex-M (ETM / MTB)

## 3. Related work
→ see `docs/02-related-work.md`. Close on the gap: trace-based CFI has not been
evaluated under flight constraints.

## 4. Threat model
→ see `docs/01-threat-model.md`. Capabilities A1–A4, assets, out of scope.

## 5. Target system: on-board computer prototype
- Five FreeRTOS tasks: `tc_rx`, `adcs`, `eps`, `tm_tx`, `payload`.
- Telecommand format and parsing path.
- The controlled vulnerability and why it is representative.

## 6. Attack chain
```
ground packet -> vulnerable parsing -> buffer overflow
 -> overwritten return address -> control-flow hijack -> critical function
```
- Exploit description and the targeted critical function (`eps_kill_switch`).
- Why the consequence is irreversible on a real satellite.

## 7. Defense: control-flow monitor
- Static CFG extraction at build time.
- Online verification over hardware trace.
- Tiered response policy L0–L3, and why the tier is a mission decision, not a detector decision.

## 8. Evaluation
→ see `docs/05-evaluation.md`. Scenarios S0–S5, metrics, results table.

## 9. Discussion
- What the technique covers and what it does not (data-only attacks).
- Attack vs. radiation-induced fault: same signature, different response.
- The operational cost of a false positive in a real mission.

## 10. Conclusion and future work
- Direct answer to the research question.
- Next steps: real hardware, remote attestation over telemetry, context-sensitive CFG.

## References
*(to be completed)*
