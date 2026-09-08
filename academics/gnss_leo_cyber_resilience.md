# A Cyber-Resilience Framework for GNSS-Dependent LEO Satellites

**Deriving minimum onboard cybersecurity requirements from PNT threat chains**

---

## Abstract

Low Earth Orbit (LEO) spacecraft have become structurally dependent on Global Navigation Satellite Systems (GNSS) for orbit determination, time synchronisation, attitude support, payload geolocation and autonomous manoeuvring. The security literature treats this dependency almost exclusively as a *signal* problem — how to detect spoofing, how to reject jamming — while the space cybersecurity literature treats it almost exclusively as a *principle* problem — defence in depth, secure-by-design, threat-informed defence. The two bodies of work rarely meet, and the practical consequence is that mission teams are told that "GNSS can be spoofed" without ever being told what their spacecraft must therefore be able to do.

This paper proposes **GNSS-CRF**, a cyber-resilience framework that closes that gap by treating Position, Navigation and Timing (PNT) not as a sensor input but as a *trust-bearing service* with a mission-derived service contract. GNSS-CRF defines a seven-stage derivation chain — **Mission Objective → GNSS Dependency → Threat → Effect → Detection → Mitigation → Cyber Requirement** — and a set of rules that make each transition traceable, so that a PNT attack scenario is transformed deterministically into a verifiable spacecraft requirement rather than into a recommendation.

Three arguments distinguish the framework from a checklist. First, we argue that in spacecraft the dominant hazard is not the loss of a fix but **estimator poisoning**: false PNT is absorbed by the navigation filter and by propagated ephemeris, so its effect *persists after the attack has ended* and detection must therefore be state-aware, not merely signal-aware. Second, we show that LEO orbital dynamics constitute an **exploitable defender asymmetry** — a spacecraft's trajectory is constrained by physics that a ground-based spoofer must reproduce with high fidelity through a short, geometrically unfavourable window — and we convert this asymmetry into concrete detection primitives that require no cryptographic support. Third, we argue that the correct unit of mitigation is not a filter but an **authority gate**: PNT trust state must govern which autonomous actions the spacecraft is permitted to take, and no irreversible actuation should be executable under untrusted PNT.

Applying the chain to eight representative LEO mission objectives yields a **tiered Minimum Control Baseline (MCB)** of sixteen controls, mapped to MITRE SPARTA tactics, NIST SP 800-53 Rev. 5 control families and NIST IR 8323. We also propose an evaluation methodology and five resilience metrics (time-to-detect, spoof-induced state error at detection, holdover error growth, authority-gate correctness, and mission availability under attack), together with a hardware-in-the-loop validation plan. The framework is analytical and has not been flight-validated; Section 9 states this limitation explicitly and Section 10 defines the experimental programme required to close it.

**Keywords:** LEO satellites, GNSS spoofing, jamming, PNT resilience, secure-by-design, space cybersecurity, SPARTA, requirements engineering, threat modelling.

---

## 1. Introduction

### 1.1 Motivation

A modern LEO spacecraft is, in a very literal sense, a GNSS receiver with a payload attached. Onboard GPS/Galileo receivers provide real-time orbit determination at metre-level accuracy, discipline the onboard clock to UTC, timestamp payload data, drive antenna and instrument pointing, schedule ground contacts, and — increasingly — close the loop on autonomous collision avoidance and formation flying. Removing GNSS does not merely degrade a mission; for many smallsat architectures it removes the spacecraft's ability to know where and when it is at all.

This dependency has grown at the same time that the PNT threat environment has deteriorated. Jamming and spoofing of GNSS have moved from laboratory demonstrations to routine features of contested regions, and the 2022 Viasat KA-SAT incident demonstrated that adversaries willing to target space-enabled infrastructure will do so with capability and intent. Meanwhile, the economics of the smallsat industry have pushed operators toward commercial off-the-shelf receivers, unauthenticated civil signals, and software stacks that were never designed under an assumption of adversarial inputs.

The security response has been bifurcated. On one side, the navigation community — most prominently Humphreys and colleagues — has produced a mature body of work on the mechanics of spoofing, its detectability, and the design of authentication schemes. On the other, the space cybersecurity community — Falco, MITRE's SPARTA project, SPD-5, NIST IR 8270/8323 and the IEEE P3349 effort — has produced principles, threat matrices and control catalogues for space systems as a whole. What is missing between them is a *method*: a repeatable procedure that takes a specific mission, a specific PNT dependency and a specific attack, and produces a specific, testable requirement that an engineer can put into a spacecraft specification and a reviewer can verify.

### 1.2 Central research question

> **What is the minimum set of onboard cybersecurity controls that a GNSS-dependent LEO satellite must possess in order to continue operating — safely and within mission tolerance — during GNSS spoofing and jamming?**

Two words in that question carry the analytical weight. *Minimum* means the framework must produce a defensible floor rather than an aspirational maximum: spacecraft are constrained in mass, power, processing and schedule, and a baseline that ignores this will be ignored in turn. *Continue operating* means the objective is resilience, not prevention: the framework assumes the attack succeeds at the signal layer and asks what must be true of the spacecraft for the mission to survive it.

### 1.3 Contributions

1. **A formal derivation chain (GNSS-CRF)** that converts PNT attacks into spacecraft cybersecurity requirements through seven traceable stages, with explicit transition rules at each stage (Section 4).
2. **The PNT Service Contract**, a per-objective specification of accuracy, integrity, holdover and authenticity bounds that makes "GNSS dependency" a measurable quantity rather than a qualitative statement (Section 4.2).
3. **The estimator-poisoning argument**: a characterisation of why deception attacks on spacecraft differ fundamentally from deception attacks on terrestrial receivers, and the recovery requirements this implies (Sections 3.4 and 4.3).
4. **LEO dynamics as a detection primitive**: four detection tests derived from orbital mechanics and LEO signal geometry that are unavailable to terrestrial users and require no cryptographic support (Section 4.3, stage 5).
5. **The PNT Trust State Machine and authority gating**, a mechanism that binds autonomous spacecraft authority to PNT trust level, with the rule that no irreversible actuation is permitted under untrusted PNT (Section 4.5).
6. **A tiered Minimum Control Baseline** of sixteen controls answering the central question, mapped to SPARTA, NIST SP 800-53 Rev. 5 and NIST IR 8323 (Section 6).
7. **An evaluation methodology** with five metrics and a hardware-in-the-loop validation plan (Section 7).

### 1.4 Scope and structure

The framework addresses the **space segment** of a LEO mission: the spacecraft, its GNSS receiver, its navigation filter, its clock and its autonomy. Ground-segment and link-layer security (command authentication, TT&C encryption, ground station hardening) are treated as assumed-present preconditions, not because they are unimportant — the Viasat incident shows the opposite — but because they are well covered elsewhere and because the contribution here is specifically about PNT dependency. Section 2 reviews the two source literatures and states the gap. Section 3 gives the threat model. Section 4 defines the framework. Section 5 applies it. Section 6 presents the baseline. Sections 7–10 cover evaluation, discussion, limitations and conclusions.

---

## 2. Background and Related Work

### 2.1 The nature of GNSS dependency in LEO

GNSS reception in LEO is geometrically different from reception on the ground, and the difference matters for both the attack and the defence.

GNSS constellations occupy Medium Earth Orbit at roughly 20,200 km altitude, with transmit antennas pointed at the Earth. A spacecraft at 400–800 km altitude sits *below* that constellation, so it cannot see the satellites directly overhead in the way a ground user does. Instead it acquires signals from GNSS satellites on the far side of the Earth whose main-lobe emissions pass over the Earth's limb, supplemented by side-lobe energy. The practical consequences are: fewer usable satellites, weaker received power than the ground-level specification, poorer and more rapidly changing geometry, and Doppler shifts an order of magnitude larger than a static ground user experiences — on the order of tens of kilohertz on L1, driven by the spacecraft's own ~7.5 km/s orbital velocity.

Onboard, the receiver rarely feeds raw fixes directly to mission functions. It feeds a navigation filter — typically an extended or unscented Kalman filter — that fuses GNSS measurements with a dynamic model of the orbit and, on more capable platforms, with inertial and attitude sensors. Real-time onboard orbit determination in the metre class is routine with this architecture; ground post-processing reaches centimetre level. The filter is what makes GNSS useful in LEO, and, as Section 3.4 argues, it is also what makes GNSS deception dangerous in LEO.

The dependency is not confined to position. The GNSS timing solution disciplines the onboard clock, and that clock underwrites cryptographic validity windows, replay protection, log ordering, payload timestamping, inter-satellite link scheduling and ground-contact windows. Timing is frequently the deepest and least documented dependency in a spacecraft, and it is the one whose corruption produces the most cross-domain damage.

### 2.2 PNT threats and spoofing detection (the Humphreys line of work)

The navigation security literature, developed substantially by Humphreys and the University of Texas Radionavigation Laboratory and colleagues in the ION and IEEE communities, establishes several results that this framework takes as given.

**Attacks are cheap and no longer exotic.** Portable civil GPS spoofers built from software-defined radio components were demonstrated more than fifteen years ago, and the subsequent public demonstrations against a UAV and against a surface vessel showed that a well-constructed spoofer can capture a receiver's tracking loops and walk the reported solution away from truth smoothly enough that the victim's own instrumentation reports nominal operation throughout.

**Deception is more dangerous than denial.** Jamming announces itself: the receiver loses lock, flags loss of fix, and downstream consumers can react to an explicit failure. A well-executed spoof produces a *plausible, internally consistent, but false* solution, and the system continues to operate confidently on wrong data. Detection difficulty is therefore inversely related to attack sophistication, and the failure mode is silent.

**Detection is layered, and no single layer suffices.** The literature organises countermeasures into families that this framework adopts and extends: signal-level monitoring (automatic gain control and C/N0 anomalies, correlation-function distortion, received-power ceilings), measurement-level consistency (receiver autonomous integrity monitoring and its advanced variants, residual and innovation testing, Doppler-versus-pseudorange-rate consistency), spatial discrimination (angle-of-arrival estimation using multiple antenna elements, on the principle that authentic signals arrive from many directions and a spoof typically arrives from one), clock-behaviour monitoring, and cross-checking against independent non-GNSS sensors.

**Cryptographic authentication helps but does not close the problem.** Navigation message authentication — Galileo's OSNMA, and the Chimera concept for GPS — allows a receiver to verify that the navigation data it decoded originated with the constellation operator. This defeats data-level forgery. It does not by itself defeat meaconing (authentic signals recorded and replayed with delay), because the replayed bits are genuine; defeating replay requires additional timing constraints. Furthermore, schemes based on delayed key disclosure impose an authentication latency that must be reconciled with a mission's holdover budget — a trade this framework makes explicit in Section 4.2.

**LEO PNT is an emerging alternative.** Recent work, including Humphreys' investigations into opportunistic PNT from broadband LEO downlinks, points toward diversification of PNT sources. This framework treats such sources as candidate alternative navigation inputs (Section 4.3, stage 6) while noting that they are not yet mature enough to be assumed present in a minimum baseline.

### 2.3 Space system cybersecurity principles (the Falco line of work)

The second source literature approaches spacecraft as cyber-physical systems rather than as radios. Falco's work — including the argument that space systems have been treated as a security vacuum, the articulation of cybersecurity principles for space systems, and the leadership of standardisation efforts such as IEEE P3349 — established several positions that this framework builds on.

**Security must be designed in, not appended.** A spacecraft cannot be patched the way a server can. Uplink windows are short, bandwidth is scarce, a failed update is potentially mission-ending, and the platform will fly for years with whatever architecture it launched with. Security properties that are not present at design freeze are, in practice, permanently absent. This is the strongest available argument for deriving cyber requirements *before* the design is fixed — which is precisely what GNSS-CRF is for.

**Mission priorities must drive security decisions.** Not all functions of a spacecraft deserve equal protection, and a control catalogue applied uniformly wastes the scarce resources that space systems have least of. Security investment should follow from what the mission must not lose. GNSS-CRF operationalises this by starting every derivation chain at a mission objective and by scaling the resulting requirement's priority to the objective's criticality.

**Minimum viable requirements are the useful output.** For the smallsat and commercial sector, a maximal control set is aspirational; a defensible floor is actionable. The Minimum Control Baseline of Section 6 is written in that spirit.

**Threat-informed defence needs a space-specific model.** Generic IT threat models do not capture RF-layer attacks, orbital dynamics, ground-segment coupling or the irreversibility of on-orbit actions.

### 2.4 SPARTA as the threat-modelling substrate

MITRE's SPARTA (Space Attack Research and Tactic Analysis) provides an ATT&CK-style matrix for space systems, organising adversary behaviour into tactics spanning reconnaissance, resource development, initial access, execution, persistence, defence evasion, lateral movement, exfiltration and impact, each populated with space-specific techniques and countermeasures.

GNSS-CRF uses SPARTA at two points in the chain. At stage 3 (Threat), SPARTA supplies the vocabulary and the completeness check: a threat enumeration is only defensible if it has been walked against a published matrix rather than assembled from the analyst's imagination. At stage 7 (Cyber Requirement), SPARTA technique identifiers become the traceability anchor that ties a mission-specific requirement back to a documented adversary behaviour, which is what makes the requirement auditable by a third party.

*Note on citation hygiene:* SPARTA technique identifiers are versioned and change between releases. Throughout this paper we name SPARTA **tactics**, which are stable, and mark technique identifiers as fields to be populated against the live matrix at the time of use. Analysts applying the framework should pin the matrix version in their traceability record.

### 2.5 The gap

Table 1 states the gap directly.

| | Navigation security literature | Space cybersecurity literature | GNSS-CRF |
|---|---|---|---|
| Primary object | The signal and the receiver | The spacecraft and the enterprise | The mission function |
| Threat treatment | Deep, quantitative, RF-specific | Broad, tactic-level, matrix-driven | RF threats consumed via SPARTA vocabulary |
| Output | Detection algorithms, authentication schemes | Principles, control catalogues, threat matrices | Verifiable spacecraft requirements |
| Handles estimator persistence | Rarely (terrestrial receivers are usually memoryless) | No (not modelled at this granularity) | Explicitly (Section 3.4) |
| Handles autonomy authority | No | Partially (via general access control) | Explicitly (Section 4.5) |
| Traceability to mission | Absent | Asserted as a principle | Mechanised as a derivation chain |

**Table 1.** Positioning of GNSS-CRF relative to the two source literatures.

The gap is not that either literature is wrong. It is that neither produces the artefact a spacecraft programme actually needs at design freeze: a requirement, with a bound, with a verification method, traceable to both a mission objective and a documented threat.

---

## 3. Threat Model

### 3.1 Adversary

We assume an adversary with the following capabilities:

- **RF capability.** Can transmit in GNSS bands from ground or airborne platforms with high effective radiated power, and can generate signals with software-defined radios using published civil signal specifications. Can record and replay authentic signals.
- **Knowledge.** Knows the target's approximate orbit — a reasonable assumption, since LEO orbits are publicly catalogued — and can predict pass geometry and timing.
- **Persistence.** Can attack repeatedly across passes over territory it controls, and can coordinate attacks across multiple ground sites.
- **Cyber capability.** Can craft malformed or semantically hostile navigation data intended to exploit receiver firmware, and may have attempted supply-chain influence over receiver firmware or aiding data.

We assume the adversary **cannot** break the cryptography of authenticated signals where such signals are used, cannot place transmitters in orbit above the target, and does not have valid command authority over the spacecraft. The last assumption matters: an adversary with command authority does not need to spoof GNSS, and defending against that case is the ground segment's problem, not this framework's.

### 3.2 Attack surface

The PNT attack surface of a LEO spacecraft comprises five entry points:

1. **The RF front end** — the antenna and receiver chain, exposed to jamming, meaconing and spoofing.
2. **The navigation data content** — ephemeris, almanac and clock corrections decoded from the signal, exposed to forgery where authentication is absent, and to malformed-input exploitation of the receiver's parsing logic.
3. **The navigation filter** — exposed to measurement injection that is individually plausible but collectively deceptive.
4. **Uplinked aiding data** — orbit updates, TLEs, differential corrections and time references supplied from the ground, exposed to ground-segment compromise or supply-chain corruption.
5. **The onboard clock discipline loop** — exposed to slow time-drag attacks that shift spacecraft time without ever producing an obviously anomalous jump.

### 3.3 Threat taxonomy

| ID | Threat | Mechanism | Primary effect class |
|---|---|---|---|
| **T1** | Broadband jamming | High-power noise across the band | Denial |
| **T2** | Narrowband / chirp / pulsed jamming | Targeted interference, possibly intermittent to evade monitoring | Denial, intermittent degradation |
| **T3** | Meaconing (replay) | Authentic signals recorded and rebroadcast with delay | Deception (position and time offset) |
| **T4** | Overlay spoofing (smooth takeover) | Spoofed signals aligned to authentic ones, power gradually raised, solution walked off truth | Deception (silent, worst case) |
| **T5** | Asynchronous spoofing | Spoofed constellation transmitted without alignment; forces reacquisition onto false signals | Deception, preceded by brief denial |
| **T6** | Navigation-data forgery | False ephemeris/clock parameters injected where the signal is unauthenticated | Deception with long persistence |
| **T7** | Receiver exploitation | Malformed navigation frames used to trigger memory-safety or logic faults in receiver firmware | Compromise of the receiver itself |
| **T8** | Aiding-data corruption | Malicious or corrupted uplinked orbit/time/correction data | Deception, bypassing all RF defences |
| **T9** | Time-drag attack | Slow, sub-threshold manipulation of the timing solution | Cross-domain cascade (crypto, logs, scheduling) |

**Table 2.** PNT threat taxonomy used throughout the framework. T1–T6 map to the navigation security literature; T7–T9 are the cyber-crossover threats that motivate treating PNT as a security problem rather than a signal-processing problem.

### 3.4 The central hazard: estimator poisoning

The most important claim of this section is that spacecraft respond to deception differently from terrestrial receivers, and that the difference is architectural rather than incidental.

A handheld receiver is close to memoryless. When a spoof ends, the next fix is computed from the next set of measurements and the deception ends with it. A spacecraft navigation filter is not memoryless. It maintains a state estimate and a covariance, and it fuses measurements according to how confident it is in that state. This produces three consequences that are specific to spacecraft:

**Persistence.** False measurements accepted into the filter alter the state estimate. When the attack stops, the estimate does not spring back — it must be driven back by subsequent authentic measurements, and the more confident the filter had become in the poisoned state, the more slowly this happens.

**Confidence inversion.** A skilfully executed spoof produces measurements that are *more* mutually consistent than authentic ones, because the attacker controls all of them and the real world contains noise. The filter's covariance therefore shrinks: the estimator becomes maximally confident precisely when it is maximally wrong. Any detection scheme that treats low residuals as evidence of health will be inverted by this.

**Propagation.** The poisoned state is not confined to the filter. It is written into propagated ephemeris, into stored orbit solutions, into payload metadata already downlinked, and into scheduling tables. An attack lasting one pass can corrupt products for days.

The design consequences are direct, and they are the reason the framework does not stop at detection:

- Detection must include **state-aware** tests (does the estimated trajectory remain physically feasible?) and not only signal-aware tests, because signal-aware tests can be defeated by an attacker with sufficient fidelity while physics cannot.
- The system must be able to **quarantine and roll back** filter state, which means it must checkpoint trusted state and retain the ability to reinitialise from a non-GNSS anchor.
- Products generated under degraded PNT trust must be **labelled** with that trust level, so that corruption is bounded and identifiable after the fact rather than silently mixed into the archive.

### 3.5 Effect classes

We classify effects into five classes, used at stage 4 of the chain:

| Class | Definition | Detectability | Persistence after attack ends |
|---|---|---|---|
| **E1 Denial** | Loss of PNT solution | High (explicit) | None |
| **E2 Degradation** | Solution available but outside accuracy tolerance | Medium | Low |
| **E3 Deception** | Plausible but false solution | Low | **High** (estimator poisoning) |
| **E4 Temporal** | Clock offset or drift induced | Low | **High** (propagates into crypto, logs, scheduling) |
| **E5 Compromise** | Receiver or software state altered by hostile input | Very low | **Permanent until remediated** |

**Table 3.** Effect classes. Note the inverse relationship between detectability and persistence: the effects that are hardest to see are the ones that last longest. This relationship is the core justification for the framework's emphasis on recovery and authority gating rather than detection alone.

---

## 4. The GNSS-CRF Framework

### 4.1 Overview

GNSS-CRF is a derivation chain of seven stages. Each stage consumes the output of the previous one and applies a stated transition rule, so that the final requirement can be traced backwards to the mission objective that justifies it and forwards to the verification method that confirms it.

```
   [1]              [2]               [3]          [4]         [5]           [6]            [7]
Mission    →    GNSS         →    Threat    →   Effect   →  Detection  →  Mitigation  →  Cyber
Objective       Dependency                                                                Requirement
   |                |                 |            |            |             |              |
 what the        which PNT         which        what it     how we       what we do    what the
 mission         services,         attack       does to      notice      about it      spacecraft
 must not        to what           reaches      the                                    SHALL do,
 lose            tolerance         it           objective                              with a bound
```

**Figure 1.** The GNSS-CRF derivation chain.

The chain is applied once per (objective, threat) pair. A mission with eight objectives and nine threats does not require seventy-two analyses, because most pairs are eliminated at stage 2: a threat that cannot reach a dependency the objective does not have is out of scope, and the elimination itself is recorded, which is what makes the analysis auditable for completeness.

### 4.2 Formal definitions

**Mission objectives.** Let `O = {o₁, …, oₙ}` be the set of mission objectives, each with a criticality `κ(oᵢ) ∈ {catastrophic, critical, major, minor}` assigned by the mission's own hazard analysis. Criticality is inherited from safety and mission-assurance practice rather than invented here, which keeps the framework compatible with existing programme documentation.

**PNT services.** Let `S = {P, V, T}` denote position, velocity and time services.

**The PNT Service Contract.** For each objective, the dependency is expressed not as a boolean but as a contract:

```
C(oᵢ) = ⟨ D, α, ι, η, A ⟩

  D  ⊆ S              which PNT services the objective consumes
  α                   accuracy bound: maximum error tolerable while the objective is met
  ι                   integrity bound: maximum probability of undetected out-of-bound error
  η                   holdover budget: how long the objective survives with no valid PNT update
  A  ∈ {none, data, source, full}   authenticity level required of the PNT input
```

The holdover budget `η` is the single most useful number the framework produces, and most missions have never computed it. It is the answer to "how long can this function run on memory?", and it determines directly whether an authentication scheme with delayed key disclosure is usable, whether a chip-scale atomic clock is required or a temperature-compensated oscillator suffices, and whether a detection latency of thirty seconds is tolerable or fatal.

**Threats and effects.** Let `T = {T1, …, T9}` be the threat set of Table 2 and `E = {E1, …, E5}` the effect classes of Table 3. The effect mapping is

```
ε : O × T → E × ℝ⁺ × ℝ⁺
```

producing an effect class, a magnitude (the induced error in the units of `α`) and a persistence time (how long the effect outlives the attack).

**Contract violation.** An (objective, threat) pair is **in scope** if and only if the effect violates the contract:

```
violates(oᵢ, tⱼ)  ⇔  magnitude(ε(oᵢ,tⱼ)) > α(oᵢ)
                  ∨  persistence(ε(oᵢ,tⱼ)) > η(oᵢ)
                  ∨  A(oᵢ) is not satisfied by the available signal
```

This predicate is the elimination rule that keeps the analysis tractable, and it is also the framework's most important honesty mechanism: an analyst who cannot state `α` and `η` cannot evaluate it, and therefore cannot claim to have analysed the dependency at all.

**Detection and mitigation.** Let `Δ` be the set of detection mechanisms with, for each `d ∈ Δ`, a detection latency `λ(d)`, a detection probability `P_d(d, tⱼ)` against threat `tⱼ`, and a false-alarm rate `P_fa(d)`. Let `M` be the set of mitigations, each with a residual-risk function and a resource cost in mass, power, processing and non-recurring engineering effort.

**The requirement derivation rule.** For each in-scope pair, the derived requirement must satisfy three conditions simultaneously:

```
R(oᵢ, tⱼ) is adequate  ⇔
      (i)   λ(d) + t_response  <  η(oᵢ)              [timeliness]
      (ii)  P_d(d, tⱼ) ≥ 1 − ι(oᵢ)                    [integrity]
      (iii) residual_error after mitigation ≤ α(oᵢ)   [tolerance]
```

Condition (i) is the one most often violated in practice: a detection scheme that works but reports after the holdover budget has expired provides forensics, not resilience. Stating it as a formal adequacy condition forces the trade between detection confidence and detection speed to be made explicitly and defended, rather than discovered during an anomaly review.

**Requirement priority.** The priority tier of the derived requirement is a function of objective criticality, effect persistence and recoverability:

```
priority(R) = f( κ(oᵢ), persistence(ε), recoverability )
```

with the rule that any requirement addressing an effect that is **irreversible on orbit** — a propulsive manoeuvre executed on false position, a deorbit command, an irrecoverable safe-mode entry — is promoted to the highest tier regardless of the probability assigned to the threat. Irreversibility, not likelihood, is the dominant term in space systems, because there is no on-orbit undo.

### 4.3 The stages

**Stage 1 — Mission Objective.** Enumerate what the mission must not lose, in mission language rather than engineering language: *maintain orbit knowledge sufficient for conjunction assessment*, *deliver geolocated imagery within specification*, *maintain timing traceability for the payload*, *execute autonomous collision avoidance*. Assign `κ`. The discipline here is to resist starting at the receiver; starting at the receiver produces receiver requirements, which is the failure this framework exists to correct.

**Stage 2 — GNSS Dependency.** For each objective, complete the contract `C(oᵢ)`. Three questions are usually revealing: which of P, V, T does this objective *actually* consume, as opposed to which does it happen to receive; what error would make the objective fail rather than merely degrade; and how long could this objective run if GNSS vanished right now. Hidden timing dependencies surface at this stage more often than anything else, because timing is consumed by functions whose designers never thought of themselves as GNSS users.

**Stage 3 — Threat.** Walk the threat taxonomy of Table 2 against the dependency, cross-checked against the SPARTA matrix for completeness. Record eliminations with justification. The output is the set of threats that can physically reach this dependency.

**Stage 4 — Effect.** For each surviving threat, determine the effect class, the magnitude in the units of `α`, and the persistence. This is where the estimator-poisoning analysis of Section 3.4 is applied: the question is not what the receiver reports during the attack, but what the *mission state* looks like after it. Evaluate `violates()`. Pairs that do not violate the contract are documented and closed.

**Stage 5 — Detection.** Select detection mechanisms subject to adequacy conditions (i) and (ii). We organise available mechanisms into five layers, of which the fourth is specific to spacecraft and, we argue, underexploited.

*Layer D1 — Signal level.* Automatic gain control and C/N0 monitoring; received-power ceiling tests; correlation-function distortion monitoring; spectral monitoring for jamming signatures. Fast, cheap, defeated by a careful attacker.

*Layer D2 — Measurement level.* RAIM and its advanced variants; pseudorange residual testing; consistency between Doppler-derived range rate and pseudorange differencing; carrier-phase continuity. Effective against inconsistent spoofs, defeated by a fully self-consistent one.

*Layer D3 — Cryptographic.* Navigation message authentication (OSNMA, Chimera) where available. Defeats data forgery (T6) outright. Does not defeat meaconing without additional timing constraints, and imposes an authentication latency that must be checked against `η` under adequacy condition (i).

*Layer D4 — Orbital dynamics and LEO geometry.* This is the layer we argue is distinctive, because a spacecraft's motion is constrained by physics that the attacker must reproduce exactly and that costs the defender nothing to check:

  - **Keplerian feasibility.** A reported trajectory must be consistent with two-body motion plus known perturbations (J2, drag, solar radiation pressure) and with the spacecraft's known propulsive capability. A position sequence that implies an unmodelled acceleration exceeding what the thrusters can produce is not a possible trajectory, and no amount of internal self-consistency in the spoofed measurements can hide it.
  - **Sky-view geometry.** From LEO, the expected set of visible GNSS satellites, their approximate elevations and their signal-strength distribution are predictable from almanac and orbit. A ground-based spoofer producing a constellation whose implied geometry corresponds to a ground user's sky view — or whose signals all arrive from a single narrow angular sector near the limb — is inconsistent with the physics of reception at altitude.
  - **Doppler-profile consistency.** The Doppler signature of a receiver moving at ~7.5 km/s is large and highly structured, evolving predictably over a pass. Reproducing it requires the attacker to model the target's dynamics precisely and continuously.
  - **Link-budget plausibility.** Overpowering authentic GNSS signals at LEO altitude from the ground requires very high effective radiated power directed at a fast-moving target through a limited-duration window. The attack is therefore geometrically constrained and, in principle, detectable as an anomalous power event correlated with a specific ground region — which also makes it *attributable* across repeated passes.

  Layer D4 requires no additional hardware, only computation and a model the spacecraft already carries. For resource-constrained smallsats this is the highest-value detection layer available, and it is the one least addressed in the existing literature.

*Layer D5 — Cross-domain.* Comparison against star tracker, sun sensor, magnetometer and inertial measurements; against ground-supplied orbit solutions received over an authenticated link; against inter-satellite ranging; and against independently propagated ephemeris. Slow but independent of the attacked channel, which is what makes it the anchor for recovery.

The framework's rule at this stage is that **at least two layers of differing physical basis must be present** for any objective whose contract specifies `A ≥ source`, since single-layer detection has a single defeat condition.

**Stage 6 — Mitigation.** Mitigations are selected across five functions:

  - *Prevent:* controlled-reception-pattern antennas or null-steering where mass and cost permit; front-end filtering; receiver firmware hardening and input validation against T7; enabling authenticated signals where available.
  - *Detect and isolate:* the PNT Trust State Machine of Section 4.5; innovation gating in the navigation filter, with the explicit caveat from Section 3.4 that gating must not treat low residuals as proof of health.
  - *Degrade gracefully:* holdover on propagated ephemeris and a disciplined oscillator; attitude from star tracker independent of GNSS; timing from a local clock with a characterised drift model, sized so that drift over `η` remains within `α`.
  - *Recover:* checkpointed trusted state; filter quarantine and rollback; reinitialisation from a non-GNSS anchor (authenticated ground upload, star-tracker-based orbit determination, or inter-satellite ranging).
  - *Respond:* trust-state-gated autonomy, telemetry alerting, and product labelling with PNT trust level.

**Stage 7 — Cyber Requirement.** Express the outcome in a fixed template so that it is testable rather than aspirational:

> **[Subsystem] SHALL [capability] such that [measurable bound] under [threat condition], verified by [V&V method].**

A requirement that cannot be written in this form has not been derived; it has been wished for. The template forces a bound and a verification method, which are the two things that separate a requirement from a recommendation.

### 4.4 Worked transition example

Applying the chain to a single pair, in full:

| Stage | Content |
|---|---|
| **1. Objective** | Maintain orbit knowledge sufficient for autonomous conjunction avoidance. `κ = catastrophic` (collision creates debris and is irreversible). |
| **2. Dependency** | `D = {P, V}`; `α` = position error small relative to the conjunction screening volume; `η` = the interval over which propagated ephemeris remains within `α`, on the order of hours to a day for a well-modelled LEO orbit; `ι` very low; `A = source`. |
| **3. Threat** | T4 (overlay spoofing) — reaches the dependency directly; the adversary knows the orbit and can predict the pass. |
| **4. Effect** | E3 Deception. Magnitude: arbitrary, attacker-chosen. Persistence: high — the false state enters the navigation filter and the propagated ephemeris, outliving the attack by days. `violates() = true` on all three clauses. |
| **5. Detection** | D4 Keplerian feasibility (the spoofed trajectory implies acceleration inconsistent with the vehicle's propulsive capability) + D5 cross-check against authenticated ground-supplied orbit and star-tracker-derived attitude/orbit. Two layers, differing physical basis, satisfying the stage-5 rule. Latency must be shown less than `η` minus response time. |
| **6. Mitigation** | Transition to DEGRADED/UNTRUSTED trust state; quarantine filter updates; hold on propagated ephemeris; **inhibit propulsive manoeuvres** until trust is restored from a non-GNSS anchor; alert the operator. |
| **7. Requirement** | *The navigation subsystem SHALL detect position solutions inconsistent with feasible orbital dynamics and transition to UNTRUSTED PNT state within a latency demonstrably shorter than the propagated-ephemeris holdover budget, and SHALL inhibit all propulsive commands while in that state, verified by hardware-in-the-loop testing against a smooth-takeover spoofing profile at defined walk-off rates.* |

**Table 4.** Full traversal of the chain for one (objective, threat) pair.

Note what the chain produced that a principle-level treatment would not: an inhibit condition on propulsion. That requirement does not follow from "GNSS can be spoofed". It follows from tracing the specific effect of a specific threat on a specific objective through to the specific authority that must be withdrawn.

### 4.5 The PNT Trust State Machine and authority gating

The framework's central mitigation construct is that PNT trust is a **first-class, explicit system state** that governs spacecraft authority. Most spacecraft treat PNT validity as a per-measurement flag consumed locally by the navigation filter. We argue it should instead be a vehicle-level state that other subsystems read and obey, for the same reason that safe mode is a vehicle-level state: the correct response to untrustworthy navigation is a change in what the vehicle is *allowed to do*, not merely a change in what the filter believes.

| State | Entry criteria | Autonomy permitted | Products |
|---|---|---|---|
| **NOMINAL** | All detection layers nominal; authentication valid where available; residuals and dynamics consistent | Full autonomy, including propulsive manoeuvres | Unlabelled (nominal) |
| **SUSPECT** | Single-layer anomaly, or authentication unavailable, or degraded geometry | Non-propulsive autonomy; manoeuvres require ground confirmation | Labelled `PNT=SUSPECT` |
| **DEGRADED** | Confirmed jamming (E1/E2); PNT unavailable but not deceptive | Holdover operations only; no autonomous manoeuvres | Labelled `PNT=HOLDOVER`, with elapsed holdover time |
| **UNTRUSTED** | Multi-layer inconsistency, dynamics infeasibility, or confirmed deception (E3/E4) | **No irreversible actions.** GNSS input quarantined; filter frozen or rolled back to checkpoint | Labelled `PNT=UNTRUSTED`; downstream consumers must treat as invalid |

**Table 5.** PNT Trust State Machine. Transitions upward in trust require a positive, independent re-anchoring event; they must never occur merely because the anomaly stopped being observed.

Three design rules follow, and we state them as the framework's normative core:

**Rule 1 — Authority follows trust.** Every autonomous capability is annotated with the minimum PNT trust state under which it may execute. The annotation is enforced by the flight software's command path, not by convention.

**Rule 2 — No irreversible actuation under untrusted PNT.** Propulsion, deployment, deorbit, and any command whose effect cannot be undone on orbit require NOMINAL trust or explicit ground authorisation. This is the single highest-value requirement the framework produces, because it converts an information-integrity failure into a bounded loss of function rather than a permanent loss of vehicle.

**Rule 3 — Trust restoration requires an independent anchor.** Exit from UNTRUSTED requires re-anchoring against a source that is not the attacked channel — an authenticated ground upload, star-tracker-based orbit determination, or inter-satellite ranging. The absence of the anomaly is not evidence of its absence, and an attacker who observes the trust state in telemetry can otherwise simply pause to reset it.

---

## 5. Application: Eight Mission Objectives

Table 6 applies the chain to eight objectives typical of a LEO mission. It is intentionally compressed; each row is the summary of a traversal of the kind shown in full in Table 4.

| # | Mission objective | Dependency `D` | Dominant threat | Effect | Detection | Mitigation | Derived cyber requirement |
|---|---|---|---|---|---|---|---|
| 1 | Orbit determination | P, V | T4 overlay spoofing | E3 deception, high persistence via filter and ephemeris | D4 Keplerian feasibility + D5 ground/star-tracker cross-check | Trust state → UNTRUSTED; filter quarantine; holdover on propagated ephemeris | Detect dynamically infeasible solutions within holdover budget; quarantine filter; re-anchor from independent source |
| 2 | Onboard time reference | T | T9 time-drag, T3 meaconing | E4 temporal, cascades into crypto validity, replay windows, log ordering | D1 clock-drift monitoring vs oscillator model; D3 authentication; D5 authenticated ground time | Local oscillator holdover with characterised drift; bounded rate-of-change gate on clock corrections | Reject time corrections exceeding a physically justified rate bound; maintain time within `α_T` over `η` without GNSS |
| 3 | Autonomous collision avoidance | P, V | T4, T8 | E3, **irreversible** if a manoeuvre executes on false state | D4 + D5, two independent bases | **Inhibit propulsion** below NOMINAL trust; require ground confirmation | No propulsive command executes under sub-NOMINAL PNT trust (Rule 2) |
| 4 | Payload data geolocation | P, T | T4, T5 | E3 — silently corrupts the science/imagery archive | D2 residual consistency + D4 | Label products with PNT trust state; retain raw measurements for reprocessing | All payload products carry a PNT trust label; degraded-trust products are recoverable by ground reprocessing |
| 5 | Attitude determination support | P, V, T | T1/T2 jamming | E1/E2 — degrades pointing where GNSS aids attitude | D1 signal monitoring | Star tracker as primary attitude source, architecturally independent of GNSS | Attitude determination SHALL meet pointing spec with GNSS unavailable for the full holdover budget |
| 6 | Ground contact scheduling | P, T | T9, T8 | E4 — missed passes, degraded command opportunity, compounding isolation | D5 cross-check of schedule against propagated orbit | Schedule margin sized to holdover drift; ground-side schedule authority | Contact scheduling SHALL tolerate onboard time and orbit uncertainty accumulated over `η` |
| 7 | Constellation / formation coordination | P, V, T | T4 targeting one or several members | E3 — relative-state error propagates across the formation | D5 inter-satellite ranging; cross-vehicle consistency (a spoof affecting one member is visible to its neighbours) | Fall back to relative navigation via ISL; isolate the affected member | Relative navigation SHALL be maintainable without absolute GNSS for the coordination holdover budget |
| 8 | End-of-life deorbit execution | P, V, T | T4, T8 | E3, **irreversible and catastrophic** | D4 + D5 + ground authorisation | Ground-authorised execution only; multi-source state confirmation | Deorbit SHALL require authenticated ground authorisation and multi-source state confirmation; it SHALL NOT be autonomously executable on GNSS alone |

**Table 6.** Application of the GNSS-CRF chain to eight LEO mission objectives.

Three observations emerge from the application that were not evident before it.

**Timing is the most under-analysed dependency.** Objectives 2, 4, 6 and 8 all consume time, and in most spacecraft documentation none of them is recorded as a GNSS dependency. Time corruption is also the effect class with the widest cross-domain blast radius, because it silently invalidates cryptographic validity windows, replay protection and the ordering of the very logs an operator would use to investigate the incident.

**Irreversibility, not probability, drives the requirement set.** Objectives 3 and 8 produce the strongest requirements in the table, and they do so regardless of how likely one judges a spoofing attack to be, because the cost of being wrong is unbounded. This is a general property of space systems and it is why conventional risk-scoring, which multiplies likelihood by impact, systematically under-protects them.

**Formation flight inverts the attack economics.** Objective 7 shows that a constellation is not simply a larger attack surface. Neighbours are independent observers: a spoof that captures one member produces a relative-state inconsistency visible to the others, so multi-satellite architectures possess a detection capability that a single spacecraft does not. Inter-satellite ranging is therefore a security control as well as a navigation aid.

---

## 6. The Minimum Control Baseline

This section answers the central research question. The baseline is tiered so that it scales from a university cubesat to critical infrastructure, and every control is stated as a capability rather than as a product.

**Tier 0 — Mandatory for any GNSS-dependent LEO satellite.** These are the controls without which the spacecraft has no defence that survives a competent attacker, and all of them are achievable in software on hardware the spacecraft already carries.

| ID | Control | Function | SPARTA tactic | NIST SP 800-53 Rev. 5 |
|---|---|---|---|---|
| **MCB-01** | Explicit PNT Trust State Machine with the four states of Table 5 | Detect / respond | Impact, Defense Evasion | SI-4, SI-13 |
| **MCB-02** | Authority gating: no irreversible actuation under sub-NOMINAL trust (Rule 2) | Respond | Impact | AC-3, CM-5, SI-13 |
| **MCB-03** | Orbital-dynamics plausibility checking (D4 Keplerian feasibility) | Detect | Impact | SI-4, SI-10 |
| **MCB-04** | Signal-level anomaly monitoring (AGC, C/N0, power ceiling) | Detect | Initial Access, Impact | SI-4 |
| **MCB-05** | Navigation filter innovation gating with covariance-inversion awareness | Detect / isolate | Impact | SI-10, SI-13 |
| **MCB-06** | Timing holdover with a characterised drift model sized to `η` | Degrade | Impact | SC-45, AU-8 |
| **MCB-07** | Bounded rate-of-change gate on accepted clock corrections | Detect / prevent | Impact | SI-10, SC-45 |
| **MCB-08** | Receiver input validation and firmware hardening against malformed navigation data (T7) | Prevent | Execution, Initial Access | SI-7, SI-10, SA-8 |
| **MCB-09** | Trusted-state checkpointing with filter quarantine and rollback | Recover | Impact, Persistence | CP-10, CP-12 |
| **MCB-10** | PNT trust labelling of all products and telemetry | Respond / forensics | Exfiltration, Impact | AU-3, SC-16 |
| **MCB-11** | Security-relevant PNT event logging with integrity protection and monotonic ordering independent of GNSS time | Detect / forensics | Defense Evasion | AU-2, AU-8, AU-9 |
| **MCB-12** | Independent non-GNSS re-anchoring path for trust restoration (Rule 3) | Recover | Impact | CP-10, IR-4 |

**Tier 1 — Additional controls for manoeuvring, constellation and commercial-service missions.**

| ID | Control | Function | NIST SP 800-53 Rev. 5 |
|---|---|---|---|
| **MCB-13** | Navigation message authentication enabled where the signal supports it (OSNMA / Chimera), with authentication latency verified against `η` | Prevent | SC-8, SC-16, SI-7 |
| **MCB-14** | Independent secondary navigation source (star-tracker-based orbit determination, inter-satellite ranging, or LEO-PNT) | Degrade / recover | CP-10, SC-5 |

**Tier 2 — Additional controls for critical-infrastructure and high-assurance missions.**

| ID | Control | Function | NIST SP 800-53 Rev. 5 |
|---|---|---|---|
| **MCB-15** | Spatial discrimination: controlled-reception-pattern antenna or multi-element angle-of-arrival detection | Prevent / detect | SC-5, SI-4 |
| **MCB-16** | Cross-vehicle PNT consistency checking across the constellation | Detect | SI-4, SC-5 |

**Table 7.** The Minimum Control Baseline. SPARTA technique identifiers are deliberately omitted and should be populated against the pinned matrix version at time of use, per Section 2.4.

### 6.1 Why this is a *minimum*

Three properties justify calling Tier 0 minimal rather than merely small.

**It is achievable within smallsat constraints.** MCB-01 through MCB-12 are software controls plus one clock-quality decision. None requires a controlled-reception-pattern antenna, an additional RF chain, or a cryptographic module. The most computationally demanding, MCB-03, needs a dynamics model the spacecraft already carries for propagation.

**Each control closes a distinct failure mode.** Removing any Tier 0 control leaves an unhandled path from Table 2 to Table 3: without MCB-03 a self-consistent spoof is undetectable; without MCB-02 detection does not prevent an irreversible action; without MCB-09 recovery is impossible after estimator poisoning; without MCB-11 the incident cannot be investigated, because the attacker has corrupted the time base of the logs.

**It is coverage-complete against the threat taxonomy.** Every threat T1–T9 is addressed by at least one Tier 0 control, and every effect class E1–E5 has at least one detection and one recovery control. Coverage completeness is a weaker claim than efficacy, and we do not overstate it: it means no threat is unaddressed, not that every threat is defeated.

### 6.2 Mapping to external frameworks

The baseline is deliberately expressed so that it can be consumed by existing compliance structures rather than competing with them. NIST IR 8323 (the foundational PNT profile applying the Cybersecurity Framework to responsible use of PNT services) provides the closest external anchor, and the mapping is direct: its *Identify* function corresponds to GNSS-CRF stages 1–2, *Protect* to the prevent mitigations, *Detect* to stage 5, and *Respond*/*Recover* to the trust state machine and re-anchoring controls. NIST IR 8270 and SPD-5 supply the space-sector framing, CCSDS security standards cover the link-layer preconditions assumed in Section 1.4, and IEEE P3349 is the standardisation venue in which requirements of this kind are most likely to find a normative home.

---

## 7. Evaluation Methodology

A framework that proposes requirements must also propose how to tell whether they are met. We define five metrics and a validation environment.

### 7.1 Metrics

| Metric | Definition | Target property |
|---|---|---|
| **TTD** — time to detect | Interval from attack onset to trust-state transition | `TTD + t_response < η` (adequacy condition i) |
| **SIE** — spoof-induced state error at detection | Magnitude of navigation state error accumulated at the moment of detection | `SIE ≤ α` |
| **HEG** — holdover error growth | Rate of position/time error accumulation with no valid GNSS | Determines achievable `η`; drives clock and ephemeris design |
| **AGC** — authority-gate correctness | Fraction of irreversible commands correctly inhibited under sub-NOMINAL trust | Must be 1.0; anything less falsifies Rule 2 |
| **MAA** — mission availability under attack | Fraction of mission objectives meeting their contracts during and after an attack episode | The headline resilience figure |

**Table 8.** Evaluation metrics. TTD and SIE together characterise detection; HEG characterises graceful degradation; AGC characterises the safety property; MAA characterises the mission outcome.

A note on false alarms: `P_fa` must be evaluated jointly with TTD, because a detector tuned for speed will transition to UNTRUSTED on benign geometry changes, and a spacecraft that inhibits its own collision-avoidance manoeuvres on false alarms has traded one catastrophic failure mode for another. The framework does not resolve this trade; it requires that it be stated, measured, and defended per objective.

### 7.2 Proposed validation environment

We propose a hardware-in-the-loop testbed with four elements:

1. **Orbital dynamics simulation** (for example GMAT or Basilisk) generating truth trajectories with realistic perturbations, providing ground truth for SIE and HEG.
2. **GNSS signal simulation with LEO dynamics**, driving either a commercial constellation simulator or an SDR-based generator, and critically including LEO-correct geometry: limb-crossing main lobes, side-lobe reception, reduced satellite visibility and full-magnitude Doppler. Terrestrial-profile signal simulation will overstate defensive performance, because layer D4 depends on precisely the geometry that a terrestrial profile omits.
3. **Attack profile library** covering T1–T9, parameterised by walk-off rate for smooth-takeover spoofing, by delay for meaconing, by duty cycle for pulsed jamming, and by sub-threshold rate for time-drag.
4. **Flight-representative software** running the actual navigation filter, trust state machine and command path, so that AGC measures the real command path rather than a model of it.

### 7.3 Falsifiable predictions

The framework makes claims that the testbed can refute, and we state them so that it is falsifiable rather than merely plausible:

- **P1.** Against a smooth-takeover spoof that defeats layers D1 and D2, layer D4 (Keplerian feasibility) detects the attack before SIE exceeds `α` for walk-off rates above some threshold rate `r*`. If no such `r*` exists at usable false-alarm rates, the D4 claim of Section 4.3 fails.
- **P2.** Estimator poisoning persists measurably after attack cessation, with recovery time increasing as filter covariance decreases during the attack — the confidence-inversion effect of Section 3.4. If post-attack recovery is fast and covariance-independent, the case for MCB-09 weakens.
- **P3.** Authority gating (MCB-02) reduces catastrophic outcomes to zero across the attack library at the cost of a measurable availability penalty from false alarms. The size of that penalty is the framework's real cost and is unknown until measured.

---

## 8. Discussion

**The defender's asymmetry is physical, and it is under-used.** The dominant theme running through Sections 4 and 5 is that a spacecraft is a hard target for a PNT attacker in ways a car or a phone is not. It moves at 7.5 km/s along a trajectory constrained by celestial mechanics; it observes GNSS from a geometry the attacker cannot easily replicate; it is visible to an attacker only in short, predictable windows; and it carries a dynamics model precise enough to test its own reported motion for feasibility. Terrestrial anti-spoofing research has necessarily concentrated on cryptography and on RF-layer discrimination, because a terrestrial user has no equivalent physical constraint to appeal to. Spacecraft do, and the framework's practical recommendation is to exploit it first, because it is free.

**Resilience is cheaper than prevention, and better matched to the sector.** Tier 0 contains no new hardware. This matters because the population of GNSS-dependent LEO spacecraft is dominated by cost-constrained commercial and academic platforms for which controlled-reception-pattern antennas and cryptographic modules are out of reach. A baseline they can actually implement is worth more than a stronger one they will not.

**The framework's real output is a set of numbers, not a set of controls.** `α`, `ι`, `η` and `A` per objective are what convert the analysis from narrative to engineering. In our experience of applying the chain, computing `η` is the step that changes design decisions most often, because it is the moment a team discovers how long the mission can actually survive without GNSS — a figure that is frequently much shorter, or much longer, than assumed, and either discovery reallocates budget.

**Relationship to safe mode.** An objection worth addressing is that spacecraft already have safe mode, and that untrusted PNT could simply trigger it. We think this is wrong in both directions. Safe mode is too blunt: it abandons the mission, and an adversary who can force safe mode with a jammer has achieved denial cheaply and repeatably. It is also insufficient: some safe-mode implementations themselves depend on GNSS for attitude or timing, so the fallback shares a failure mode with the thing it is falling back from. Trust-gated authority is the finer-grained construct — the spacecraft keeps doing everything that does not depend on the compromised input, and stops only what does.

**Applicability beyond LEO.** Stages 1–2 and 6–7 are orbit-agnostic. Stage 5's layer D4 is where the LEO specificity lives, and it generalises with modification: any vehicle whose motion is strongly constrained by a known dynamic model can test its own reported state for feasibility. The construction should transfer to MEO and GEO platforms, to launch vehicles and to deep-space missions, with the constraint tightening as the dynamics become more predictable.

---

## 9. Limitations

We state these plainly, because the framework's credibility depends on not overclaiming.

1. **No experimental validation.** GNSS-CRF is an analytical construction. None of the metrics of Section 7 has been measured, and predictions P1–P3 are untested. Section 7.2 is a proposal, not a report of results.
2. **No flight heritage.** The framework has not been applied to a flown mission, and the operational cost of trust-state false alarms in a real programme is unknown.
3. **Detection performance is asserted, not characterised.** The claim that layer D4 detects self-consistent spoofs rests on physical reasoning. The achievable `P_d`/`P_fa` operating points, and their dependence on attack walk-off rate, orbital regime, filter tuning and dynamics-model fidelity, are precisely what has not been quantified. This is the framework's most significant open item.
4. **Contract parameters are mission-specific.** The framework tells an analyst what to compute, not what the answer is. Two teams applying it to similar missions may derive different `η` values, and the framework provides no calibration procedure to reconcile them.
5. **The threat model excludes the insider and the compromised ground segment.** An adversary with command authority is out of scope by construction (Section 3.1), though MCB-12's reliance on authenticated ground uploads means that a compromised ground segment degrades the recovery path — a coupling the framework acknowledges but does not solve.
6. **The literature review is structural rather than exhaustive.** We characterise the Humphreys and Falco lines of work at the level of their positions and results. **Every citation in Section 11 should be verified against the original source before this paper is submitted anywhere**, and specific technical figures quoted from those works should be checked against the published values rather than taken from this summary.
7. **SPARTA mapping is at tactic granularity.** Technique-level mapping requires a pinned matrix version and has not been performed.

---

## 10. Conclusion and Future Work

We asked what minimum set of cybersecurity controls a GNSS-dependent LEO satellite needs in order to keep operating through spoofing and jamming. The answer we derive is the sixteen-control baseline of Table 7, of which twelve are mandatory, all twelve are implementable in software, and the most important of them is not a detector at all but an authority gate: **no irreversible action under untrusted PNT**.

The method that produces that answer is the contribution we consider more durable than the answer itself. The seven-stage chain — Mission Objective → GNSS Dependency → Threat → Effect → Detection → Mitigation → Cyber Requirement — with the PNT Service Contract at stage 2 and the adequacy conditions at stage 7, converts PNT attacks into verifiable spacecraft requirements through steps that a reviewer can audit and a second analyst can reproduce. That is a different kind of artefact from a list of good practices, and it is the artefact that a spacecraft programme needs before design freeze, when security properties can still be added.

Three findings surprised us in the course of the construction and are worth carrying forward. Timing is the deepest and least documented GNSS dependency in a spacecraft, and its corruption has the widest blast radius. Irreversibility dominates likelihood in space systems, which means conventional risk scoring systematically under-protects them. And LEO orbital dynamics give the defender a detection primitive that costs nothing and that terrestrial users do not have — the strongest practical result in the paper, and the one most in need of experimental confirmation.

**Future work**, in priority order:

1. **Build the testbed of Section 7.2 and test P1.** Characterising the `P_d`/`P_fa` operating curve of orbital-dynamics plausibility checking against walk-off rate is the single highest-value next experiment, because the framework's most distinctive claim rests on it.
2. **Quantify estimator poisoning (P2)** across filter architectures, and derive checkpointing and rollback policies from the measured recovery dynamics.
3. **Measure the availability cost of authority gating (P3)**, since Rule 2's operational acceptability depends entirely on its false-alarm burden.
4. **Complete the technique-level SPARTA mapping** against a pinned matrix version, and propose PNT-specific countermeasure entries where the matrix is thin.
5. **Develop a calibration procedure for contract parameters**, so that `α`, `ι`, `η` and `A` are derived consistently across missions rather than per analyst.
6. **Extend the framework to alternative PNT sources**, including LEO-PNT from broadband downlinks, and to constellation-scale cross-vehicle detection (MCB-16), where the economics of attack and defence appear most favourable to the defender.

---

## 11. References

> **Verification notice.** The following list identifies the bodies of work on which this paper builds. Bibliographic details — years, venues, volume and page numbers — **must be verified against the original sources before submission**, and quantitative figures attributed to these works should be checked against their published values. See Limitation 6.

**PNT threats, spoofing and detection**

1. Humphreys, T. E., et al. "Assessing the Spoofing Threat: Development of a Portable GPS Civilian Spoofer." *Proceedings of the ION GNSS Conference*.
2. Humphreys, T. E. "Detection Strategy for Cryptographic GNSS Anti-Spoofing." *IEEE Transactions on Aerospace and Electronic Systems*.
3. Humphreys, T. E. "Interference." Chapter in *Springer Handbook of Global Navigation Satellite Systems*.
4. Psiaki, M. L., and Humphreys, T. E. "GNSS Spoofing and Detection." *Proceedings of the IEEE*.
5. Humphreys, T. E., et al. Work on opportunistic PNT from broadband LEO downlink signals (Starlink-based PNT).
6. Publications on the University of Texas UAV and surface-vessel spoofing demonstrations.

**Space system cybersecurity**

7. Falco, G. "The Vacuum of Space Cyber Security." *AIAA SPACE Conference*.
8. Falco, G. "Cybersecurity Principles for Space Systems." *Journal of Aerospace Information Systems*.
9. Falco, G. "Job One for Space Force: Space Asset Cybersecurity." Belfer Center, Harvard Kennedy School.
10. IEEE P3349 — Space System Cybersecurity standardisation working group.

**Frameworks, standards and policy**

11. MITRE. *SPARTA: Space Attack Research and Tactic Analysis* (matrix version to be pinned at time of use).
12. NIST IR 8323. *Foundational PNT Profile: Applying the Cybersecurity Framework for the Responsible Use of Positioning, Navigation, and Timing Services*.
13. NIST IR 8270. *Introduction to Cybersecurity for Commercial Satellite Operations*.
14. NIST SP 800-53 Rev. 5. *Security and Privacy Controls for Information Systems and Organizations*.
15. Space Policy Directive-5 (SPD-5). *Cybersecurity Principles for Space Systems*.
16. Executive Order 13905. *Strengthening National Resilience Through Responsible Use of Positioning, Navigation, and Timing Services*.
17. CCSDS 355.0-B. *Space Data Link Security Protocol*.
18. European Union Agency for the Space Programme. Galileo Open Service Navigation Message Authentication (OSNMA) documentation.
19. Chimera (CHIPS-Message Robust Authentication) signal authentication specification and NTS-3 experiment documentation.

**Incidents**

20. Analyses of the February 2022 Viasat KA-SAT modem disruption (AcidRain wiper).

---

## Appendix A — Requirement Template

```
REQ-[ID]
  Objective:        [mission objective, from stage 1]
  Criticality:      [κ]
  Contract:         D=[...]  α=[...]  ι=[...]  η=[...]  A=[...]
  Threat:           [Tn]  (SPARTA tactic: [...]; technique: [pin matrix version])
  Effect:           [En], magnitude [...], persistence [...]
  Statement:        The [subsystem] SHALL [capability] such that [bound]
                    under [threat condition].
  Detection:        [layers, with λ and P_d]
  Adequacy:         (i) λ + t_response = [...] < η = [...]   ☐
                    (ii) P_d = [...] ≥ 1 − ι = [...]          ☐
                    (iii) residual error = [...] ≤ α = [...]  ☐
  Trust gating:     Minimum PNT trust state for affected capability: [...]
  Verification:     [analysis | HIL test | simulation | inspection]
  MCB mapping:      [MCB-nn]
  Priority tier:    [from priority(R); irreversible ⇒ highest]
```

## Appendix B — Analyst Worksheet

For each mission objective:

1. State the objective in mission language, not engineering language. Assign `κ`.
2. Complete the contract. If you cannot state `η`, stop — the dependency is not yet understood.
3. Walk Table 2 against the dependency. Record and justify every elimination.
4. For each surviving threat, determine effect class, magnitude and persistence. Apply Section 3.4: ask what the *mission state* looks like after the attack, not what the receiver reported during it. Evaluate `violates()`.
5. Select detection across at least two layers of differing physical basis. Check adequacy conditions (i) and (ii).
6. Select mitigations across prevent / detect / degrade / recover / respond. Assign the minimum trust state for each affected autonomous capability.
7. Write the requirement using the Appendix A template. If it cannot be written with a bound and a verification method, return to step 2.

---

*Draft for discussion. See Section 9 for limitations and Section 11 for the citation verification notice.*
