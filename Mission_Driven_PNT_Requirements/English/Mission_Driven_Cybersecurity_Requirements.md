# Mission-Driven Cybersecurity Requirements for GNSS-Dependent LEO Spacecraft

**A framework for deriving minimum onboard cyber requirements from PNT threat chains**

---

## Abstract

Low Earth Orbit (LEO) spacecraft have become structurally dependent on Global Navigation Satellite Systems (GNSS) for orbit determination, time synchronisation, attitude support, payload geolocation and autonomous manoeuvring. The security literature treats this dependency almost exclusively as a *signal* problem — how to detect spoofing, how to reject jamming — while the space cybersecurity literature treats it almost exclusively as a *principle* problem — defence in depth, secure-by-design, threat-informed defence. The two bodies of work rarely meet, and the practical consequence is that mission teams are told that "GNSS can be spoofed" without ever being told what their spacecraft must therefore be able to do.

This paper proposes **GNSS-CRF**, a cyber-resilience framework that narrows that gap by treating Position, Navigation and Timing (PNT) not as a sensor input but as a *trust-bearing service* with a mission-derived service contract. It builds directly on recent work by Falco and colleagues on deriving minimum space cyber requirements from mission priorities, and is best understood as a deep, quantified specialisation of that approach to a single dependency (Section 2.5). GNSS-CRF defines a seven-stage derivation chain — **Mission Objective → GNSS Dependency → Threat → Effect → Detection → Mitigation → Cyber Requirement** — and a set of rules that make each transition traceable, so that a PNT attack scenario is transformed deterministically into a verifiable spacecraft requirement rather than into a recommendation.

Three arguments distinguish the framework from a checklist. First, we argue that in spacecraft the dominant hazard is not the loss of a fix but **estimator poisoning**: false PNT is absorbed by the navigation filter and by propagated ephemeris, so its effect *persists after the attack has ended* and detection must therefore be state-aware, not merely signal-aware. Second, we show that LEO orbital dynamics constitute an **exploitable defender asymmetry** — a spacecraft's trajectory is constrained by physics that a ground-based spoofer must reproduce with high fidelity through a short, geometrically unfavourable window — and we convert this asymmetry into concrete detection primitives that require no cryptographic support. Third, we argue that the correct unit of mitigation is not a filter but an **authority gate**: PNT trust state must govern which autonomous actions the spacecraft is permitted to take, and no irreversible actuation should be executable under untrusted PNT.

Applying the chain to eight representative LEO mission objectives, and then in full depth to a hypothetical maritime-surveillance smallsat constellation, yields a **tiered Minimum Control Baseline (MCB)** of sixteen controls, mapped to SPARTA tactics, NIST SP 800-53 Rev. 5 control families and NIST IR 8323. We also propose an evaluation methodology and five resilience metrics (time-to-detect, spoof-induced state error at detection, holdover error growth, authority-gate correctness, and mission availability under attack), together with a hardware-in-the-loop validation plan. The case study produces a result the framework did not assume: under orbital-feasibility gating, a single ground-based spoofer is bounded to roughly one kilometre of induced position error by the spacecraft's own thrust capability and by pass geometry, and that bound scales with propulsion class across three orders of magnitude — making propulsion sizing a determinant of PNT attack surface. The framework is analytical and has not been flight-validated; Section 10 states this limitation explicitly and Section 11 defines the experimental programme required to close it.

**Keywords:** LEO satellites, GNSS spoofing, jamming, PNT resilience, secure-by-design, space cybersecurity, SPARTA, requirements engineering, threat modelling.

---

## 1. Introduction

### 1.1 Motivation

A modern LEO spacecraft is, in a very literal sense, a GNSS receiver with a payload attached. Onboard GPS/Galileo receivers provide real-time orbit determination at metre-level accuracy, discipline the onboard clock to UTC, timestamp payload data, drive antenna and instrument pointing, schedule ground contacts, and — increasingly — close the loop on autonomous collision avoidance and formation flying. Removing GNSS does not merely degrade a mission; for many smallsat architectures it removes the spacecraft's ability to know where and when it is at all.

This dependency has grown at the same time that the PNT threat environment has deteriorated. Jamming and spoofing of GNSS have moved from laboratory demonstrations to routine features of contested regions, and the 2022 Viasat KA-SAT incident demonstrated that adversaries willing to target space-enabled infrastructure will do so with capability and intent. Meanwhile, the economics of the smallsat industry have pushed operators toward commercial off-the-shelf receivers, unauthenticated civil signals, and software stacks that were never designed under an assumption of adversarial inputs.

The security response has been bifurcated. On one side, the navigation community — most prominently Humphreys and colleagues — has produced a mature body of work on the mechanics of spoofing, its detectability, and the design of authentication schemes. On the other, the space cybersecurity community — Falco, the Aerospace Corporation's SPARTA project, SPD-5, NIST IR 8270/8323 and the IEEE P3349 effort — has produced principles, threat matrices and control catalogues for space systems as a whole. What is missing between them is a *method*: a repeatable procedure that takes a specific mission, a specific PNT dependency and a specific attack, and produces a specific, testable requirement that an engineer can put into a spacecraft specification and a reviewer can verify.

### 1.2 Central research question

> **What is the minimum set of onboard cybersecurity controls that a GNSS-dependent LEO satellite must possess in order to continue operating — safely and within mission tolerance — during GNSS spoofing and jamming?**

Two words in that question carry the analytical weight. *Minimum* means the framework must produce a defensible floor rather than an aspirational maximum: spacecraft are constrained in mass, power, processing and schedule, and a baseline that ignores this will be ignored in turn. *Continue operating* means the objective is resilience, not prevention: the framework assumes the attack succeeds at the signal layer and asks what must be true of the spacecraft for the mission to survive it.

### 1.3 Contributions

The general idea of deriving minimum space cyber requirements from mission priorities is **not** claimed as novel here: it is due to Falco and colleagues (Section 2.5), and this paper is best read as a deep specialisation of that idea to one dependency.

1. **A formal derivation chain (GNSS-CRF)** specialised to PNT, converting GNSS attacks into spacecraft cybersecurity requirements through seven traceable stages with explicit transition rules and quantitative adequacy conditions at each stage (Section 4).
2. **The PNT Service Contract**, a per-objective specification of accuracy, integrity, holdover and authenticity bounds that makes "GNSS dependency" a measurable quantity rather than a qualitative statement (Section 4.2).
3. **The estimator-poisoning argument**: a characterisation of why deception attacks on spacecraft differ fundamentally from deception attacks on terrestrial receivers, and the recovery requirements this implies (Sections 3.4 and 4.3).
4. **LEO dynamics as a detection primitive**: four detection tests derived from orbital mechanics and LEO signal geometry that are unavailable to terrestrial users and require no cryptographic support (Section 4.3, stage 5).
5. **The PNT Trust State Machine and authority gating**, a mechanism that binds autonomous spacecraft authority to PNT trust level, with the rule that no irreversible actuation is permitted under untrusted PNT (Section 4.5).
6. **A tiered Minimum Control Baseline** of sixteen controls answering the central question, mapped to SPARTA, NIST SP 800-53 Rev. 5 and NIST IR 8323 (Section 7).
7. **A hypothetical case study** carried through to numbers, which yields a quantitative bound on achievable spoof-induced error, identifies a previously unstated coupling between propulsion architecture and PNT attack surface, and demonstrates the framework's ability to *eliminate* requirements as well as generate them (Section 6).
8. **An evaluation methodology** with five metrics, three falsifiable predictions and a hardware-in-the-loop validation plan (Section 8).

### 1.4 Scope and structure

The framework addresses the **space segment** of a LEO mission: the spacecraft, its GNSS receiver, its navigation filter, its clock and its autonomy. Ground-segment and link-layer security (command authentication, TT&C encryption, ground station hardening) are treated as assumed-present preconditions, not because they are unimportant — the Viasat incident shows the opposite — but because they are well covered elsewhere and because the contribution here is specifically about PNT dependency. Section 2 reviews the two source literatures and states the gap. Section 3 gives the threat model. Section 4 defines the framework. Section 5 applies it across eight mission objectives, and Section 6 applies it in depth to a hypothetical mission. Section 7 presents the baseline. Sections 8–11 cover evaluation, discussion, limitations and conclusions.

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

The published figures make that trade concrete rather than abstract. Galileo's OSNMA entered its public observation phase on 15 November 2021 and was declared operationally available on 24 July 2025. AFRL's Chimera signal enhancement for GPS L1C, flown as an experiment on the NTS-3 satellite launched on 12 August 2025, authenticates a standalone receiver — one with access to the GNSS signal alone — approximately **once every three minutes**, with faster intervals (of order seconds) available only to users who can receive the key over an out-of-band channel. A three-minute authentication interval is comfortably inside a six-hour orbit-determination holdover budget and comfortably outside the reaction time available to an autonomous collision-avoidance decision. Whether cryptographic authentication is a usable control for a given objective is therefore not a general question about the scheme; it is a question about that objective's `η`, which is exactly what the framework's adequacy condition (i) forces an analyst to compute.

**Interference is observable from orbit.** Humphreys' group has also published multi-year results from GNSS interference monitoring conducted *from* low Earth orbit, geolocating terrestrial jamming sources from a LEO platform. This matters to the present paper in two ways: it is direct empirical evidence that the LEO vantage point carries exploitable information about terrestrial RF interference, and it supports the attributability argument made for detection layer D4 in Section 4.3.

**LEO PNT is an emerging alternative.** Recent work, including Humphreys' investigations into opportunistic PNT from broadband LEO downlinks, points toward diversification of PNT sources. This framework treats such sources as candidate alternative navigation inputs (Section 4.3, stage 6) while noting that they are not yet mature enough to be assumed present in a minimum baseline.

### 2.3 Space system cybersecurity principles (the Falco line of work)

The second source literature approaches spacecraft as cyber-physical systems rather than as radios. Falco's work — including the argument that space systems have been treated as a security vacuum, the articulation of cybersecurity principles for space systems, and the leadership of standardisation efforts such as IEEE P3349 — established several positions that this framework builds on.

**Security must be designed in, not appended.** A spacecraft cannot be patched the way a server can. Uplink windows are short, bandwidth is scarce, a failed update is potentially mission-ending, and the platform will fly for years with whatever architecture it launched with. Security properties that are not present at design freeze are, in practice, permanently absent. This is the strongest available argument for deriving cyber requirements *before* the design is fixed — which is precisely what GNSS-CRF is for.

**Mission priorities must drive security decisions.** Not all functions of a spacecraft deserve equal protection, and a control catalogue applied uniformly wastes the scarce resources that space systems have least of. Security investment should follow from what the mission must not lose. GNSS-CRF operationalises this by starting every derivation chain at a mission objective and by scaling the resulting requirement's priority to the objective's criticality.

**Minimum viable requirements are the useful output.** For the smallsat and commercial sector, a maximal control set is aspirational; a defensible floor is actionable. The Minimum Control Baseline of Section 7 is written in that spirit.

**Threat-informed defence needs a space-specific model.** Generic IT threat models do not capture RF-layer attacks, orbital dynamics, ground-segment coupling or the irreversibility of on-orbit actions.

### 2.4 SPARTA as the threat-modelling substrate

SPARTA (Space Attack Research and Tactic Analysis), developed and published by **The Aerospace Corporation**, provides an ATT&CK-style matrix tailored to space systems, spanning the space, link, ground and user segments. Its nine tactics are Reconnaissance (ST0001), Resource Development (ST0002), Initial Access (ST0003), Execution, Persistence, Defense Evasion, Lateral Movement, Exfiltration and Impact, each populated with space-specific techniques, sub-techniques and countermeasures.

GNSS-CRF uses SPARTA at two points in the chain. At stage 3 (Threat), SPARTA supplies the vocabulary and the completeness check: a threat enumeration is only defensible if it has been walked against a published matrix rather than assembled from the analyst's imagination. At stage 7 (Cyber Requirement), SPARTA technique identifiers become the traceability anchor that ties a mission-specific requirement back to a documented adversary behaviour, which is what makes the requirement auditable by a third party.

*Note on citation hygiene:* SPARTA technique identifiers are versioned and change between releases. Throughout this paper we name SPARTA **tactics**, which are stable, and mark technique identifiers as fields to be populated against the live matrix at the time of use. Analysts applying the framework should pin the matrix version in their traceability record.

### 2.5 The closest prior work

One publication sits considerably closer to this paper than the rest of either literature, and honesty about the novelty claim requires stating so plainly. Falco, Boschetti, Vecellio Segate, Maple and colleagues, in *Minimum Requirements for Space System Cybersecurity — Ensuring Cyber Access to Space* (IEEE SMC-IT, 2024), propose a scalable, extensible method for deriving minimum cyber design principles, and subsequent requirements, for a space system **from a stated mission priority**. They test it on the mission priority of preserving access to space by preventing permanent loss of control of a satellite, and they express the output as minimum-requirement 'shall' statements.

That is the same fundamental move this paper makes — mission priority first, requirements as the output artefact, 'shall' statements as the format — and the general claim to have invented mission-driven derivation of minimum space cyber requirements therefore belongs to that work, not to this one. What this paper adds is depth in one dimension that a general method necessarily leaves open:

- **A specific, quantified dependency.** Their method takes a mission priority; GNSS-CRF takes a mission objective *and a PNT Service Contract* with numerical accuracy, integrity, holdover and authenticity bounds (Section 4.2), which is what permits the adequacy conditions of Section 4.3 and the arithmetic of Section 6 to exist at all.
- **A specific threat physics.** GNSS-CRF is built around the PNT attack surface — spoofing, meaconing, jamming, receiver exploitation and time-drag — rather than around loss of control generally.
- **Effect persistence in estimators.** The estimator-poisoning analysis of Section 3.4 has no counterpart in a principle-level method.
- **Detection as a first-class stage.** Their chain runs from priority to principle to requirement; GNSS-CRF inserts detection and mitigation as separate stages with their own selection rules, because for PNT the requirement is largely determined by what can be detected and how fast.
- **Authority gating.** Binding autonomous authority to a PNT trust state (Section 4.5) is, to our reading, not present in the prior method.

*Caveat, stated for the reader's protection:* the full text of the SMC-IT paper could not be retrieved during preparation of this draft, and the characterisation above is based on its abstract and published metadata. **It must be read in full and this subsection revised accordingly before submission.** If its method turns out to already encompass any of the five points above, the corresponding contribution claim in Section 1.3 must be withdrawn or narrowed.

### 2.6 The gap

Table 1 states the gap directly.

| | Navigation security literature | Space cybersecurity literature | Falco et al. 2024 (closest prior work) | GNSS-CRF |
|---|---|---|---|---|
| Primary object | The signal and the receiver | The spacecraft and the enterprise | The mission priority | The mission objective and its PNT contract |
| Threat treatment | Deep, quantitative, RF-specific | Broad, tactic-level, matrix-driven | Loss of control, generally | PNT-specific (T1–T9), via SPARTA vocabulary |
| Output | Detection algorithms, authentication schemes | Principles, control catalogues, threat matrices | Minimum-requirement 'shall' statements | 'Shall' statements with bounds and V&V methods |
| Quantified dependency | N/A | No | Not to our reading | Yes — `⟨D, α, ι, η, A⟩` (Section 4.2) |
| Handles estimator persistence | Rarely (terrestrial receivers are usually memoryless) | No | No | Explicitly (Section 3.4) |
| Detection as a derivation stage | Is the whole subject | No | No | Yes, with adequacy conditions (Section 4.3) |
| Handles autonomy authority | No | Partially (via general access control) | Not to our reading | Explicitly (Section 4.5) |
| Traceability to mission | Absent | Asserted as a principle | Mechanised | Mechanised, with numerical bounds |

**Table 1.** Positioning of GNSS-CRF relative to the two source literatures and to the closest prior work. Entries in the Falco et al. column are marked "to our reading" because they rest on that paper's abstract and metadata rather than its full text — see the caveat in Section 2.5.

The gap is not that either literature is wrong, nor that nobody has tried to bridge them — Section 2.5 shows that the bridge has been started. It is that the general bridge, by being general, cannot carry the quantities that PNT resilience turns on: an accuracy tolerance, a holdover budget, a detection latency, and the adequacy conditions that relate them. A method that stops at the 'shall' statement leaves the hardest question — *is this requirement sufficient?* — unanswerable. What a spacecraft programme needs at design freeze is a requirement with a bound, a verification method, and a demonstration that detection is fast enough to matter, traceable to both a mission objective and a documented threat.

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

## 6. Hypothetical Case Study: the TERRA-SENTINEL Constellation

Section 5 demonstrated the breadth of the framework across objectives. This section demonstrates its depth on a single hypothetical mission, carried through to numbers. The mission is fictional and the parameter values are illustrative — chosen to be representative of the smallsat class rather than drawn from any real programme — but the arithmetic is real, and it produces a result we did not anticipate when constructing the framework.

### 6.1 Mission definition

**TERRA-SENTINEL** is a hypothetical twelve-satellite maritime domain awareness constellation.

| Attribute | Value |
|---|---|
| Orbit | 550 km sun-synchronous, ~95.6 min period, three planes |
| Spacecraft | 180 kg class smallsat, ×12 |
| Payload | Optical imager (1.5 m GSD) + AIS receiver |
| GNSS | COTS dual-frequency receiver, GPS L1/L2 + Galileo E1/E5a, OSNMA-capable |
| Attitude | Two star trackers, coarse sun sensors, magnetometer, reaction wheels |
| Propulsion | Monopropellant, 1 N thrust — station keeping and collision avoidance |
| Crosslink | S-band inter-satellite link within plane |
| Clock | OCXO baseline; chip-scale atomic clock under trade |
| Autonomy | Autonomous conjunction avoidance enabled |
| Operating context | Routine passes over regions with documented GNSS interference |

**Table 7.** TERRA-SENTINEL reference mission (hypothetical).

The mission is deliberately chosen to sit at the point of maximum tension: it is cost-constrained enough that Tier 2 controls are unaffordable, autonomous enough that Rule 2 has real consequences, and operationally exposed enough that the threat is not hypothetical even though the mission is.

### 6.2 PNT Service Contracts

Applying stages 1 and 2 of the chain yields the following contracts. Values are illustrative; a real programme derives them from its own hazard and performance analyses.

| Objective | `κ` | `D` | `α` | `ι` | `η` | `A` |
|---|---|---|---|---|---|---|
| **O1** Orbit determination for conjunction screening | Catastrophic | P, V | 100 m (3σ) | 10⁻⁵ per screening | 6 h | source |
| **O2** Onboard time reference | Critical | T | 10 µs | 10⁻⁶ | 24 h | source |
| **O3** Autonomous collision avoidance | Catastrophic | P, V | as O1 | as O1 | warning-to-burn interval | source |
| **O4** Payload geolocation | Major | P, T | 15 m | 10⁻³ | one imaging pass (~10 min) | data |
| **O5** Ground contact scheduling | Minor | P, T | 1 s | 10⁻² | 72 h | none |

**Table 8.** PNT Service Contracts for TERRA-SENTINEL (illustrative values).

Two observations arise before any threat is considered, which is itself an argument for the framework: stage 2 pays for itself even if stage 3 is never reached.

First, **O2's contract is already in tension with the baseline hardware.** An OCXO with an effective post-calibration fractional frequency offset of 10⁻¹⁰ drifts 8.64 µs over the 24-hour holdover budget, consuming 86% of the 10 µs tolerance with no allowance for ageing or thermal excursion. The contract, written down honestly, converts the clock selection from a cost decision into a resilience decision: a CSAC at 10⁻¹¹ yields 0.86 µs over the same period, a tenfold margin. This is exactly the kind of design consequence that "GNSS can be spoofed" never produces.

Second, **O5 requires no authenticity at all** (`A = none`, `α` = 1 s, `η` = 72 h). Its contract is so loose that no PNT attack within the threat model can violate it. The framework therefore eliminates O5 from further analysis and records why. A method that generates requirements for everything is not a method; the ability to justify *not* levying a requirement is what makes the output defensible to a programme manager holding a mass and cost budget.

### 6.3 Scenario A — smooth-takeover spoofing during a pass

**Setup.** An adversary operating a ground-based spoofer within the constellation's coverage region executes a T4 overlay attack against a single spacecraft. The adversary knows the orbit from the public catalogue and can predict the pass. The attack is skilfully executed: signals are power-matched at acquisition and raised gradually, so that C/N0 rises by less than the D1 alarm threshold, and the spoofed constellation is fully self-consistent, so that D2 residual testing sees nothing. Layers D1 and D2 are, by construction, defeated.

**The D4 test.** Layer D4 asks a different question: is the reported motion physically possible for *this vehicle*? Walking the reported position away from truth requires the spoofed solution to exhibit an apparent acceleration that the spacecraft is not capable of producing. TERRA-SENTINEL's maximum propulsive acceleration is

```
a_max = F / m = 1 N / 180 kg = 5.56 × 10⁻³ m/s²
```

If the navigation subsystem rejects any solution implying a sustained unmodelled acceleration above `a_max` (plus a margin for dynamics-model error and measurement noise), the adversary is forced to keep the walk-off within that bound. The maximum position offset achievable is then bounded by the attack window:

```
offset_max = ½ · a_max · T_vis²
```

where `T_vis` is the duration for which the ground spoofer can illuminate the target. For a 550 km orbit, a horizon-to-horizon pass over a single ground site is on the order of ten minutes, so `T_vis ≈ 600 s`:

```
offset_max = ½ × 5.56 × 10⁻³ × 600²  ≈  1.0 km
```

**The result.** A single ground-based spoofer cannot induce more than approximately one kilometre of position error against this spacecraft without becoming dynamically infeasible and therefore detectable — *regardless of how sophisticated the spoofer is at the signal layer*. The bound comes from the vehicle's own thrust and from orbital geometry, not from the quality of the attacker's radio.

**The corollary, which is the more interesting finding.** The bound scales with propulsive capability, and therefore so does the attack surface:

| Propulsion | `a_max` (m/s²) | Bounded offset over a 600 s pass |
|---|---|---|
| Monopropellant, 1 N / 180 kg | 5.56 × 10⁻³ | ≈ 1000 m |
| Electric, 1 mN / 180 kg | 5.56 × 10⁻⁶ | ≈ 1 m |
| Non-manoeuvring (residual drag/SRP only, ~10⁻⁶) | ~10⁻⁶ | ≈ 0.18 m |

**Table 9.** Spoof-offset bound under Keplerian feasibility gating, by propulsion class.

**Low-thrust spacecraft are structurally far harder to spoof, and non-manoeuvring spacecraft are very nearly immune** — under this gate, and assuming the gate is enforced. Propulsion sizing, a decision made for entirely unrelated reasons early in mission design, turns out to determine the spacecraft's PNT deception exposure by three orders of magnitude. To our knowledge this coupling between propulsion architecture and PNT attack surface has not been stated in either source literature, and it is a direct product of running the chain rather than reasoning about spoofing in general.

**Honest qualifications.** Three, and they matter:

1. The detection threshold cannot be exactly `a_max`. It must be `a_max + margin`, where the margin covers dynamics-model error, unmodelled drag and SRP variability, and measurement noise. A loose margin weakens the bound proportionally; the numbers above are therefore a *best-case* bound, and characterising the achievable margin is precisely prediction **P1** of Section 8.3.
2. The gate must not fire on legitimate manoeuvres. The navigation subsystem must know when the propulsion system is commanded, which makes manoeuvre-state awareness a *security* requirement and not merely a navigation one — a coupling recorded as REQ-CS-03 below.
3. The bound applies to a *single* ground site. Multi-site or airborne adversaries extend `T_vis` and relax the bound quadratically, which is the adversary's cheapest counter-move.

**The adversary's adaptation, and why Rule 2 survives it.** A natural attacker response is to *ratchet*: stay within the feasibility gate on each pass and accumulate offset across many passes. This fails against TERRA-SENTINEL for a structural reason — the spacecraft returns to authentic signals for roughly 85 minutes of every 95.6-minute orbit, and authentic measurements pull the filter back. Ratcheting requires preventing re-anchoring between passes, which a single ground site cannot do.

So the attacker's rational move is not to corrupt the *state* but to corrupt a *decision*: time the spoof to coincide with a planned conjunction-avoidance burn, and use the bounded one-kilometre error to turn a correct manoeuvre into a wrong one. One kilometre is small compared to a spoofer's ambitions but not small compared to a conjunction screening volume. This is the scenario in which the entire defence reduces to a single control — **MCB-02, no irreversible actuation under untrusted PNT** — and it is why we place authority gating above detection in the baseline. Detection bounds the error; only the authority gate bounds the *consequence*.

### 6.4 Scenario B — regional jamming, and an eliminated requirement

**Setup.** A T1 broadband jammer denies GNSS for the full duration of each pass over a contested region: one pass per orbit, roughly 600 s of denial in every 95.6 minutes.

**Contract evaluation.** For O1, `η` = 6 h. A 600 s outage is an order of magnitude inside the holdover budget, and propagated ephemeris covers it comfortably. For O2, `η` = 24 h; the clock free-runs for 600 s, accruing well under a microsecond even on the OCXO. For O4, `η` is one imaging pass, and denial during the pass means the imagery from that pass is degraded — but the effect is E2, bounded, non-persistent, and visible.

`violates()` returns **false** for O1 and O2, and **true only for O4**, whose consequence is loss of geolocation accuracy on affected images rather than loss of the mission.

**What this demonstrates.** Jamming, the threat that receives the most attention operationally because it is the one people notice, produces the *weakest* requirement set for this mission: label the affected products (MCB-10) and accept the degradation. The framework says so explicitly, with arithmetic, rather than levying a control because jamming sounds serious. Meanwhile the threat that produces the catastrophic requirement — Scenario A's silent spoof — would produce no operator complaint at all while it was happening. This inversion between operational salience and actual risk is, we think, one of the more valuable things the framework surfaces.

### 6.5 Scenario C — time-drag against the clock

**Setup.** A T9 attack manipulates the timing solution slowly enough to stay below any jump-detection threshold, aiming to shift spacecraft time far enough to invalidate cryptographic validity windows and corrupt log ordering.

**The rate gate.** MCB-07 requires that accepted clock corrections be bounded by a physically justified rate. Legitimate corrections cannot exceed the oscillator's own drift, so a gate set at three times the OCXO's 10⁻¹⁰ drift permits at most 0.3 µs per 1000 s. Within a 600 s pass, the adversary can therefore inject at most **0.18 µs**, and reaching the 10 µs tolerance of O2 would require roughly **56 passes** of uninterrupted, cumulative manipulation — with the same re-anchoring problem as Scenario A defeating the accumulation.

**The structural result.** Scenarios A and C produce the same shape of answer by the same mechanism: *a physically justified rate bound, multiplied by a geometrically bounded attack window, bounds the adversary's total authority over the state.* This is the case study's principal theoretical contribution back to the framework, and it generalises beyond these two scenarios — wherever a defender can bound the legitimate rate of change of a quantity and the adversary's access is windowed, the achievable corruption is bounded without any cryptography at all.

### 6.6 Derived requirement set

Running stage 7 across the scenarios yields the following requirements for TERRA-SENTINEL.

| ID | Requirement | Source | MCB | Verification |
|---|---|---|---|---|
| **REQ-CS-01** | The navigation subsystem SHALL reject GNSS-derived solutions implying sustained unmodelled acceleration exceeding `a_max` plus characterised model margin, and SHALL transition to UNTRUSTED within 60 s of onset. | A / O1 | MCB-03, MCB-01 | HIL against walk-off profiles |
| **REQ-CS-02** | The spacecraft SHALL NOT execute any propulsive command while PNT trust is below NOMINAL, absent authenticated ground authorisation. | A / O3 | MCB-02 | Command-path test; AGC metric = 1.0 |
| **REQ-CS-03** | The navigation subsystem SHALL receive authoritative manoeuvre state from the propulsion subsystem and SHALL suppress feasibility-gate alarms only for commanded manoeuvres. | A / O3 | MCB-03 | Integration test |
| **REQ-CS-04** | The onboard clock SHALL maintain time within 10 µs over 24 h with no valid GNSS timing update. | B, C / O2 | MCB-06 | Analysis + thermal-vacuum characterisation |
| **REQ-CS-05** | The receiver SHALL reject clock corrections exceeding three times the characterised oscillator drift rate. | C / O2 | MCB-07 | Injection test |
| **REQ-CS-06** | All payload products SHALL carry the PNT trust state and holdover elapsed time at acquisition. | B / O4 | MCB-10 | Product inspection |
| **REQ-CS-07** | The navigation subsystem SHALL checkpoint trusted state and SHALL support rollback and reinitialisation from an authenticated ground-supplied orbit or star-tracker-derived solution. | A / O1 | MCB-09, MCB-12 | HIL recovery test |
| **REQ-CS-08** | Security-relevant PNT events SHALL be logged with monotonic ordering independent of the GNSS time source. | A, C | MCB-11 | Log inspection under time attack |
| **REQ-CS-09** | Exit from UNTRUSTED SHALL require positive re-anchoring against a non-GNSS source; cessation of the anomaly SHALL NOT constitute re-anchoring. | A | MCB-01, MCB-12 | State-machine test |

**Table 10.** Requirements derived for TERRA-SENTINEL.

Nine requirements, all Tier 0, none requiring hardware the mission does not already carry — with the single exception of REQ-CS-04, which may drive the CSAC selection. That is the practical shape of the framework's output.

### 6.7 What the case study establishes

The case study is hypothetical, and it proves nothing empirically. What it does establish is that the framework is *generative*: run end to end on a concrete mission, it produced four results that were not inputs to it.

1. **A quantitative spoof bound.** Keplerian feasibility gating bounds a single-site ground spoofer to ≈1 km of induced error against this spacecraft, from vehicle physics rather than signal processing.
2. **Propulsion architecture as PNT attack surface.** The bound scales with thrust across three orders of magnitude, making a propulsion trade into a security trade.
3. **The rate-bound × window-bound principle.** Scenarios A and C converge on the same structural defence, which appears to generalise beyond PNT.
4. **The salience inversion.** The loudest threat (jamming) generated the weakest requirements; the silent one (spoofing) generated the catastrophic ones.

It also produced one negative result worth stating: the framework eliminated O5 entirely and reduced jamming to a labelling requirement. A framework that only ever adds controls cannot be trusted to have analysed anything.

---

## 7. The Minimum Control Baseline

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

**Table 11.** The Minimum Control Baseline. SPARTA technique identifiers are deliberately omitted and should be populated against the pinned matrix version at time of use, per Section 2.4.

### 7.1 Why this is a *minimum*

Three properties justify calling Tier 0 minimal rather than merely small.

**It is achievable within smallsat constraints.** MCB-01 through MCB-12 are software controls plus one clock-quality decision. None requires a controlled-reception-pattern antenna, an additional RF chain, or a cryptographic module. The most computationally demanding, MCB-03, needs a dynamics model the spacecraft already carries for propagation.

**Each control closes a distinct failure mode.** Removing any Tier 0 control leaves an unhandled path from Table 2 to Table 3: without MCB-03 a self-consistent spoof is undetectable; without MCB-02 detection does not prevent an irreversible action; without MCB-09 recovery is impossible after estimator poisoning; without MCB-11 the incident cannot be investigated, because the attacker has corrupted the time base of the logs.

**It is coverage-complete against the threat taxonomy.** Every threat T1–T9 is addressed by at least one Tier 0 control, and every effect class E1–E5 has at least one detection and one recovery control. Coverage completeness is a weaker claim than efficacy, and we do not overstate it: it means no threat is unaddressed, not that every threat is defeated.

### 7.2 Mapping to external frameworks

The baseline is deliberately expressed so that it can be consumed by existing compliance structures rather than competing with them. NIST IR 8323 (the foundational PNT profile applying the Cybersecurity Framework to responsible use of PNT services) provides the closest external anchor, and the mapping is direct: its *Identify* function corresponds to GNSS-CRF stages 1–2, *Protect* to the prevent mitigations, *Detect* to stage 5, and *Respond*/*Recover* to the trust state machine and re-anchoring controls. NIST IR 8270 and SPD-5 supply the space-sector framing, CCSDS security standards cover the link-layer preconditions assumed in Section 1.4, and IEEE P3349 is the standardisation venue in which requirements of this kind are most likely to find a normative home.

---

## 8. Evaluation Methodology

A framework that proposes requirements must also propose how to tell whether they are met. We define five metrics and a validation environment.

### 8.1 Metrics

| Metric | Definition | Target property |
|---|---|---|
| **TTD** — time to detect | Interval from attack onset to trust-state transition | `TTD + t_response < η` (adequacy condition i) |
| **SIE** — spoof-induced state error at detection | Magnitude of navigation state error accumulated at the moment of detection | `SIE ≤ α` |
| **HEG** — holdover error growth | Rate of position/time error accumulation with no valid GNSS | Determines achievable `η`; drives clock and ephemeris design |
| **AGC** — authority-gate correctness | Fraction of irreversible commands correctly inhibited under sub-NOMINAL trust | Must be 1.0; anything less falsifies Rule 2 |
| **MAA** — mission availability under attack | Fraction of mission objectives meeting their contracts during and after an attack episode | The headline resilience figure |

**Table 12.** Evaluation metrics. TTD and SIE together characterise detection; HEG characterises graceful degradation; AGC characterises the safety property; MAA characterises the mission outcome.

A note on false alarms: `P_fa` must be evaluated jointly with TTD, because a detector tuned for speed will transition to UNTRUSTED on benign geometry changes, and a spacecraft that inhibits its own collision-avoidance manoeuvres on false alarms has traded one catastrophic failure mode for another. The framework does not resolve this trade; it requires that it be stated, measured, and defended per objective.

### 8.2 Proposed validation environment

We propose a hardware-in-the-loop testbed with four elements:

1. **Orbital dynamics simulation** (for example GMAT or Basilisk) generating truth trajectories with realistic perturbations, providing ground truth for SIE and HEG.
2. **GNSS signal simulation with LEO dynamics**, driving either a commercial constellation simulator or an SDR-based generator, and critically including LEO-correct geometry: limb-crossing main lobes, side-lobe reception, reduced satellite visibility and full-magnitude Doppler. Terrestrial-profile signal simulation will overstate defensive performance, because layer D4 depends on precisely the geometry that a terrestrial profile omits.
3. **Attack profile library** covering T1–T9, parameterised by walk-off rate for smooth-takeover spoofing, by delay for meaconing, by duty cycle for pulsed jamming, and by sub-threshold rate for time-drag.
4. **Flight-representative software** running the actual navigation filter, trust state machine and command path, so that AGC measures the real command path rather than a model of it.

### 8.3 Falsifiable predictions

The framework makes claims that the testbed can refute, and we state them so that it is falsifiable rather than merely plausible:

- **P1.** Against a smooth-takeover spoof that defeats layers D1 and D2, layer D4 (Keplerian feasibility) detects the attack before SIE exceeds `α` for walk-off rates above some threshold rate `r*`. If no such `r*` exists at usable false-alarm rates, the D4 claim of Section 4.3 fails.
- **P2.** Estimator poisoning persists measurably after attack cessation, with recovery time increasing as filter covariance decreases during the attack — the confidence-inversion effect of Section 3.4. If post-attack recovery is fast and covariance-independent, the case for MCB-09 weakens.
- **P3.** Authority gating (MCB-02) reduces catastrophic outcomes to zero across the attack library at the cost of a measurable availability penalty from false alarms. The size of that penalty is the framework's real cost and is unknown until measured.

---

## 9. Discussion

**The defender's asymmetry is physical, and it is under-used.** The dominant theme running through Sections 4 to 6 is that a spacecraft is a hard target for a PNT attacker in ways a car or a phone is not. It moves at 7.5 km/s along a trajectory constrained by celestial mechanics; it observes GNSS from a geometry the attacker cannot easily replicate; it is visible to an attacker only in short, predictable windows; and it carries a dynamics model precise enough to test its own reported motion for feasibility. Terrestrial anti-spoofing research has necessarily concentrated on cryptography and on RF-layer discrimination, because a terrestrial user has no equivalent physical constraint to appeal to. Spacecraft do, and the framework's practical recommendation is to exploit it first, because it is free.

**Security constraints can come from subsystems that are not security subsystems.** The case study's propulsion finding (Section 6.3) is the clearest instance. Thrust level is selected for delta-v budget, station-keeping cadence and cost; nobody selects it for spoofing resistance. Yet under feasibility gating it sets the ceiling on how far an adversary can move the vehicle's believed position, and it does so across three orders of magnitude. The general lesson is that in cyber-physical systems the security envelope is often defined by physical design decisions taken elsewhere in the programme, and that a requirements method which starts at the mission — rather than at the receiver — is the kind of method that will find them.

**Resilience is cheaper than prevention, and better matched to the sector.** Tier 0 contains no new hardware. This matters because the population of GNSS-dependent LEO spacecraft is dominated by cost-constrained commercial and academic platforms for which controlled-reception-pattern antennas and cryptographic modules are out of reach. A baseline they can actually implement is worth more than a stronger one they will not.

**The framework's real output is a set of numbers, not a set of controls.** `α`, `ι`, `η` and `A` per objective are what convert the analysis from narrative to engineering. In our experience of applying the chain, computing `η` is the step that changes design decisions most often, because it is the moment a team discovers how long the mission can actually survive without GNSS — a figure that is frequently much shorter, or much longer, than assumed, and either discovery reallocates budget.

**Relationship to safe mode.** An objection worth addressing is that spacecraft already have safe mode, and that untrusted PNT could simply trigger it. We think this is wrong in both directions. Safe mode is too blunt: it abandons the mission, and an adversary who can force safe mode with a jammer has achieved denial cheaply and repeatably. It is also insufficient: some safe-mode implementations themselves depend on GNSS for attitude or timing, so the fallback shares a failure mode with the thing it is falling back from. Trust-gated authority is the finer-grained construct — the spacecraft keeps doing everything that does not depend on the compromised input, and stops only what does.

**Applicability beyond LEO.** Stages 1–2 and 6–7 are orbit-agnostic. Stage 5's layer D4 is where the LEO specificity lives, and it generalises with modification: any vehicle whose motion is strongly constrained by a known dynamic model can test its own reported state for feasibility. The construction should transfer to MEO and GEO platforms, to launch vehicles and to deep-space missions, with the constraint tightening as the dynamics become more predictable.

---

## 10. Limitations

We state these plainly, because the framework's credibility depends on not overclaiming.

1. **No experimental validation.** GNSS-CRF is an analytical construction. None of the metrics of Section 8 has been measured, and predictions P1–P3 are untested. Section 8.2 is a proposal, not a report of results.
2. **The case study is hypothetical and its arithmetic is bounding, not predictive.** TERRA-SENTINEL is fictional and its contract values are illustrative. The ≈1 km spoof bound of Section 6.3 is a best-case figure that assumes a detection threshold set tightly at `a_max`; a real threshold must absorb dynamics-model error, drag and solar-radiation-pressure variability and measurement noise, and a loose margin degrades the bound proportionally. The bound also assumes a single ground site — multi-site or airborne adversaries relax it quadratically in the extended window. The number is an existence proof that a computable bound exists, not a performance claim.
3. **No flight heritage.** The framework has not been applied to a flown mission, and the operational cost of trust-state false alarms in a real programme is unknown.
4. **Detection performance is asserted, not characterised.** The claim that layer D4 detects self-consistent spoofs rests on physical reasoning. The achievable `P_d`/`P_fa` operating points, and their dependence on attack walk-off rate, orbital regime, filter tuning and dynamics-model fidelity, are precisely what has not been quantified. This is the framework's most significant open item.
5. **Contract parameters are mission-specific.** The framework tells an analyst what to compute, not what the answer is. Two teams applying it to similar missions may derive different `η` values, and the framework provides no calibration procedure to reconcile them.
6. **The threat model excludes the insider and the compromised ground segment.** An adversary with command authority is out of scope by construction (Section 3.1), though MCB-12's reliance on authenticated ground uploads means that a compromised ground segment degrades the recovery path — a coupling the framework acknowledges but does not solve.
7. **The literature review is structural rather than exhaustive, and three citations remain incomplete.** The reference list has been checked against primary or authoritative secondary sources, and the entries that could not be completed are marked **[unverified]** in Section 12: the page range for Bhatti and Humphreys (2017), the page range for Falco (2019), and the exact author list for the SMC-IT 2024 minimum-requirements paper. Two substantive corrections were made during verification and are recorded here for transparency: SPARTA is a product of **The Aerospace Corporation**, not MITRE, as an earlier draft of this paper stated; and the closest prior work (Section 2.5) was absent from that draft entirely. The review remains structural — it characterises the two source literatures at the level of their positions and results rather than surveying them exhaustively — and a full systematic review is outstanding.
8. **The closest prior work has been characterised from its abstract, not its full text.** See the caveat in Section 2.5. This is the single most important verification task remaining, because the novelty claims in Section 1.3 depend on it.
9. **SPARTA mapping is at tactic granularity.** Technique-level mapping requires a pinned matrix version and has not been performed.

---

## 11. Conclusion and Future Work

We asked what minimum set of cybersecurity controls a GNSS-dependent LEO satellite needs in order to keep operating through spoofing and jamming. The answer we derive is the sixteen-control baseline of Table 11, of which twelve are mandatory, all twelve are implementable in software, and the most important of them is not a detector at all but an authority gate: **no irreversible action under untrusted PNT**.

The method that produces that answer is the contribution we consider more durable than the answer itself. The seven-stage chain — Mission Objective → GNSS Dependency → Threat → Effect → Detection → Mitigation → Cyber Requirement — with the PNT Service Contract at stage 2 and the adequacy conditions at stage 7, converts PNT attacks into verifiable spacecraft requirements through steps that a reviewer can audit and a second analyst can reproduce. That is a different kind of artefact from a list of good practices, and it is the artefact that a spacecraft programme needs before design freeze, when security properties can still be added.

The case study of Section 6 supplied the framework's most concrete result, and it was not an input to it: under orbital-feasibility gating a single ground-based spoofer is bounded to roughly one kilometre of induced error against a 180 kg, 1 N spacecraft, and that bound falls to about a metre for a low-thrust vehicle and to centimetres for a non-manoeuvring one. Propulsion architecture, selected for reasons that have nothing to do with security, therefore sets the PNT deception envelope across three orders of magnitude. The same case study showed why detection is nonetheless insufficient: an adversary confined to a kilometre of error will stop attacking the state and start attacking the decision, timing the spoof to coincide with a planned collision-avoidance burn — which leaves the authority gate as the only control standing between a bounded error and an unbounded consequence.

Three further findings surprised us in the course of the construction and are worth carrying forward. Timing is the deepest and least documented GNSS dependency in a spacecraft, and its corruption has the widest blast radius. Irreversibility dominates likelihood in space systems, which means conventional risk scoring systematically under-protects them. And LEO orbital dynamics give the defender a detection primitive that costs nothing and that terrestrial users do not have — the strongest practical result in the paper, and the one most in need of experimental confirmation.

**Future work**, in priority order:

1. **Build the testbed of Section 8.2 and test P1.** Characterising the `P_d`/`P_fa` operating curve of orbital-dynamics plausibility checking against walk-off rate is the single highest-value next experiment, because the framework's most distinctive claim rests on it.
2. **Quantify estimator poisoning (P2)** across filter architectures, and derive checkpointing and rollback policies from the measured recovery dynamics.
3. **Measure the availability cost of authority gating (P3)**, since Rule 2's operational acceptability depends entirely on its false-alarm burden.
4. **Complete the technique-level SPARTA mapping** against a pinned matrix version (v2.0 or later), and propose PNT-specific countermeasure entries where the matrix is thin.
5. **Reconcile with the closest prior work** by obtaining and analysing the SMC-IT 2024 minimum-requirements method in full, and either narrowing this paper's claims or, preferably, expressing GNSS-CRF as a PNT instantiation of that method — which would strengthen both.
6. **Develop a calibration procedure for contract parameters**, so that `α`, `ι`, `η` and `A` are derived consistently across missions rather than per analyst.
7. **Extend the framework to alternative PNT sources**, including LEO-PNT from broadband downlinks, and to constellation-scale cross-vehicle detection (MCB-16), where the economics of attack and defence appear most favourable to the defender.

---

## 12. References

> **Verification status.** The entries below were checked against primary or authoritative secondary sources during preparation of this draft. Items marked **[unverified]** could not be confirmed in that pass — in every case because the publisher's site was unreachable from the drafting environment, not because the work is in doubt — and must be completed before submission. Nothing in this list is cited from memory alone.

**PNT threats, spoofing and detection**

1. Humphreys, T. E., Ledvina, B. M., Psiaki, M. L., O'Hanlon, B. W., and Kintner, P. M., Jr. "Assessing the Spoofing Threat: Development of a Portable GPS Civilian Spoofer." *Proceedings of the ION GNSS Conference*, Savannah, GA, 16–19 September 2008.
2. Humphreys, T. E. "Detection Strategy for Cryptographic GNSS Anti-Spoofing." *IEEE Transactions on Aerospace and Electronic Systems*, Vol. 49, No. 2, 2013, pp. 1073–1090.
3. Psiaki, M. L., and Humphreys, T. E. "GNSS Spoofing and Detection." *Proceedings of the IEEE*, Vol. 104, No. 6, June 2016, pp. 1258–1270.
4. Humphreys, T. E. "Interference." In Teunissen, P. J. G., and Montenbruck, O. (eds.), *Springer Handbook of Global Navigation Satellite Systems*, Springer, Cham, 2017, pp. 469–503. DOI 10.1007/978-3-319-42928-1_16.
5. Kerns, A. J., Shepard, D. P., Bhatti, J. A., and Humphreys, T. E. "Unmanned Aircraft Capture and Control Via GPS Spoofing." *Journal of Field Robotics*, Vol. 31, No. 4, 2014, pp. 617–636. DOI 10.1002/rob.21513.
6. Bhatti, J., and Humphreys, T. E. "Hostile Control of Ships via False GPS Signals: Demonstration and Detection." *NAVIGATION*, Vol. 64, No. 1, 2017. DOI 10.1002/navi.183. *(Page range **[unverified]**.)* Field demonstration against a 65 m yacht in the Mediterranean.
7. Murrian, M. J., Narula, L., Iannucci, P. A., Budzien, S., O'Hanlon, B. W., Powell, S. P., and Humphreys, T. E. "First Results from Three Years of GNSS Interference Monitoring from Low Earth Orbit." *NAVIGATION*, Vol. 68, No. 4, 2021, pp. 673–685. Preprint: arXiv:2009.04093.
8. Humphreys, T. E., Iannucci, P. A., et al. "Signal Structure of the Starlink Ku-Band Downlink." UT Austin Radionavigation Laboratory. *(Journal venue, volume and year **[unverified]**.)* Related: "Timing Properties of the Starlink Ku-Band Downlink," arXiv:2501.05302.

**Space system cybersecurity**

9. Falco, G. "The Vacuum of Space Cyber Security." *2018 AIAA SPACE and Astronautics Forum and Exposition*, AIAA, 17–19 September 2018. DOI 10.2514/6.2018-5275.
10. Falco, G. "Cybersecurity Principles for Space Systems." *Journal of Aerospace Information Systems*, Vol. 16, No. 2, 2019 (published online December 2018). DOI 10.2514/1.I010693. *(Page range **[unverified]** — AIAA's site was unreachable.)* This paper is widely credited as an input to SPD-5, which carries the same title.
11. Falco, G. "Job One for Space Force: Space Asset Cybersecurity." Cyber Security Project, Belfer Center for Science and International Affairs, Harvard Kennedy School, July 2018.
12. Falco, G., Boschetti, N., Vecellio Segate, R., Maple, C., et al. "Minimum Requirements for Space System Cybersecurity — Ensuring Cyber Access to Space." *2024 IEEE 10th International Conference on Space Mission Challenges for Information Technology (SMC-IT)*, Mountain View, CA, 2024, pp. 78–88. DOI 10.1109/SMC-IT61443.2024.00016. *(Complete author list and order **[unverified]** — indexes disagree on which co-authors are named.)* **Closest prior work; see Section 2.5. Full text must be read before submission.**
13. IEEE P3349, Space System Cybersecurity Working Group, IEEE Standards Association. G. Falco, founding chair. International technical standard for space system cybersecurity, developed by a working group spanning 20+ countries.

**Frameworks, standards and policy**

14. The Aerospace Corporation. *SPARTA: Space Attack Research and Tactic Analysis.* https://sparta.aerospace.org/ — v2.0 published; **pin the matrix version in the traceability record at time of use.** Note: SPARTA is an Aerospace Corporation product, not a MITRE one.
15. Bartock, M., Brule, J., Li-Baboud, Y.-S., Lightman, S., McCarthy, J., Meldorf, K., Reczek, K., Northrip, D., Scholz, A., and Suloway, T. *NIST IR 8323r1: Foundational PNT Profile — Applying the Cybersecurity Framework for the Responsible Use of Positioning, Navigation, and Timing (PNT) Services.* NIST, January 2023.
16. *NIST IR 8270: Introduction to Cybersecurity for Commercial Satellite Operations.* NIST, July 2023.
17. *NIST SP 800-53 Rev. 5: Security and Privacy Controls for Information Systems and Organizations.* NIST, September 2020, with subsequent updates (patch release 5.2.0). Controls cited in Table 11 are from this revision.
18. *Space Policy Directive-5 (SPD-5): Cybersecurity Principles for Space Systems.* Signed 4 September 2020; published in the Federal Register 10 September 2020.
19. *Executive Order 13905: Strengthening National Resilience Through Responsible Use of Positioning, Navigation, and Timing Services.* Signed 12 February 2020; Federal Register 18 February 2020. NIST IR 8323 was produced in fulfilment of this order.
20. *CCSDS 355.0-B-2: Space Data Link Security Protocol.* Recommended Standard (Blue Book), Issue 2, July 2022. (Issue 1: September 2015.)
21. EUSPA / European GNSS Service Centre. *Galileo Open Service Navigation Message Authentication (OSNMA).* Public observation phase from 15 November 2021; service declared operational 24 July 2025, with publication of the OSNMA Service Definition Document.
22. Air Force Research Laboratory. *Chimera (Chips-Message Robust Authentication) signal enhancement for GPS L1C.* Flown as an experiment on the Navigation Technology Satellite-3 (NTS-3), launched 12 August 2025 aboard a ULA Vulcan from Cape Canaveral. Standalone-receiver authentication interval ≈ 3 minutes; ≈ 1.5–6 s with an out-of-band key channel. See also ION publication "Chips-Message Robust Authentication (Chimera) for GPS Civilian Signals."

**Incidents**

23. SentinelLabs. *AcidRain: A Modem Wiper Rains Down on Europe.* 31 March 2022. Analysis of the wiper deployed against Viasat KA-SAT modems on 24 February 2022 via compromise of the KA-SAT management network. Note for the present paper's scope (Section 1.4): this was a **ground-segment** compromise, not an attack on a spacecraft.

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

*Draft for discussion. See Section 10 for limitations and Section 12 for the citation verification notice.*
