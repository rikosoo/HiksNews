# Subsea Cables in the Nordic Arctic: Climate, Geopolitics, and the Resilience of Critical Digital Infrastructure

## Abstract

Roughly 99% of intercontinental data traffic travels through submarine fibre-optic cables, making this physical layer a critical infrastructure asset as essential as power or transport networks. In the Nordic and Arctic region, that infrastructure operates under a singular condition: the same regional warming that makes new trans-Arctic routes viable — reducing sea-ice cover and opening laying windows that were previously impractical — is what degrades the conditions for installing, anchoring, and repairing those systems, through permafrost loss, coastal erosion, and intensified maritime traffic. This paper analyses that tension. It first maps the Nordic and Arctic cable landscape, including the trans-Arctic projects under development. It then examines the Arctic climate as a physical risk vector and connects it to the hybrid threat model evidenced by the Svalbard (2022) and Baltic Sea (2023–2024) incidents. Finally, it discusses the applicable regulatory framework (NIS2, the CER Directive, UNCLOS) and proposes resilience priorities: route and landing-point diversity, distributed acoustic sensing, regional ice-class repair capacity, and infrastructure planning informed by climate projections. The argument advanced is that climate risk and adversarial risk are not separate agendas in this region, but manifestations of a single resilience problem.

---

## Keywords

Submarine Cables, Arctic Infrastructure, Critical Infrastructure Protection, Climate Resilience, Nordic Region, Hybrid Threats, Permafrost, Cybersecurity

---

## 1. Introduction

Public perception of the internet is dominated by immaterial metaphors — cloud, ether, wireless. The operational reality is the opposite: intercontinental connectivity depends on a finite set of fibre-optic cables laid on the seabed, each a few centimetres in diameter, whose physical destruction interrupts digital services at national scale. Estimates widely cited in the telecommunications literature indicate that roughly 99% of international data traffic traverses these systems, with satellite links serving as redundancy of limited capacity rather than as a substitute.

Three characteristics make this topic particularly pressing in the Nordic region. First, structural dependency is high: Iceland, the Faroe Islands, Greenland, and Svalbard are territories whose entire connectivity rests on a very small number of cables — in some cases, two. Second, the region hosts an unusual density of sensitive digital infrastructure, including large-scale data centres drawn by the cold climate and inexpensive renewable energy, alongside satellite ground stations of scientific and military significance. Third, the retreat of Arctic sea ice has turned the region into the object of trans-Arctic route projects — notably Far North Fiber and Polar Connect — which promise to cut latency between Asia and Europe substantially relative to routes via Suez.

In parallel, the sequence of incidents between 2022 and 2024 in the Norwegian Arctic and the Baltic Sea moved submarine cables out of the category of technical asset and into that of security policy object. This paper takes that convergence as its point of departure and poses three research questions:

1. In what ways does Arctic climate change alter the physical risk profile of Nordic cable infrastructure?
2. How do climate risks and adversarial risks interact, rather than merely accumulate independently?
3. Which resilience strategies apply to an environment where repair capacity is geographically and seasonally constrained?

### 1.1 Method and Scope

The study is structured as a documentary and analytical review. Primary sources are of four kinds: peer-reviewed academic literature on permafrost degradation and climate impacts on Arctic infrastructure; European Union regulatory instruments and international law; technical reports from submarine cable sector bodies; and public reporting and official statements concerning the 2022–2024 incidents. No proprietary operational data from cable operators was used.

The geographic scope covers the five Nordic countries and their associated territories — Iceland, the Faroe Islands, Greenland, and Svalbard — extending to the Baltic Sea where recent incidents and the interconnection mesh require it. The temporal scope of the incidents analysed runs from 2022 to the end of 2024. Limitations arising from these choices are set out in Section 9.

This paper is in dialogue with other work in this repository, in particular [*Security Challenges in Cloud-Based Critical Infrastructure Systems*](../../academics/Security_Challenges.md), which addresses the logical and cloud layer of the same asset class, and [*IT and OT as a Bridge of Friendship*](../../academics/ItAndOT.md), which examines the information/operational technology convergence referenced in Section 4.

---

## 2. The Nordic and Arctic Cable Landscape

### 2.1 Current Configuration

The region's cable infrastructure can be organised into four layers.

**North Atlantic links.** Iceland is served by a small set of systems: FARICE-1, operational since 2004, connecting the country to the Faroe Islands and Scotland; DANICE, since 2009, landing in Denmark; and IRIS, which entered service in 2023, establishing a direct route to Ireland. IRIS was added on an explicit national redundancy argument, which illustrates state-level recognition of the problem.

**Arctic and island links.** The Svalbard Undersea Cable System, comprising two fibre pairs between Longyearbyen and mainland Norway, supports not only the archipelago's civilian population but also data transmission from the SvalSat satellite station, which serves international scientific and commercial operators. Greenland depends on Greenland Connect, operational since 2009, in an equally concentrated configuration.

**Intra-Nordic and Baltic links.** The Baltic Sea is crossed by a dense mesh of telecommunications and power cables interconnecting Finland, Sweden, Estonia, Lithuania, Poland, and Germany. Among them, C-Lion1 (Helsinki–Rostock) and the BCS East-West Interlink (Lithuania–Sweden) became prominent through the damage sustained in 2024. The determining geographic characteristic here is depth: the Baltic is a shallow sea, which places cables within reach of commercial vessel anchors along much of their route.

**Trans-Arctic routes under development.** The Far North Fiber project proposes to connect Japan and Europe across the Northwest Passage, with landings planned in Alaska, the Canadian Arctic, Greenland, Iceland, Norway, Finland, and Ireland. Polar Connect, pursued within NORDUnet and the Nordic academic networks, is studying a route across the central Arctic Ocean. Both derive their viability from ice conditions altered by regional warming.

**Table 1 — Reference systems in the Nordic and Arctic region**

| System | Route | In service | Note |
|---|---|---|---|
| FARICE-1 | Iceland – Faroe Islands – Scotland | 2004 | Iceland's first modern link |
| DANICE | Iceland – Denmark | 2009 | Second Icelandic route |
| IRIS | Iceland – Ireland | 2023 | Added on an explicit national redundancy argument |
| Greenland Connect | Greenland – Iceland / Canada | 2009 | Concentrated dependency |
| Svalbard Undersea Cable System | Longyearbyen – mainland Norway | 2004 | Two fibre pairs; supports the SvalSat station |
| C-Lion1 | Helsinki – Rostock | 2016 | Damaged in November 2024 |
| BCS East-West Interlink | Lithuania – Sweden | 2009 | Damaged in November 2024 |
| Far North Fiber | Japan – Europe, via the Northwest Passage | Planned | Viability arising from ice retreat |
| Polar Connect | Europe – Asia, via the central Arctic | Under study | Led by Nordic academic networks |

### 2.2 Concentration and Chokepoints

From a critical infrastructure protection standpoint, the most relevant feature of this landscape is not the number of cables but the distribution of dependency. A territory served by two cables has, in practice, single-fault tolerance. Where both share a geographic corridor, a landing station, or terrestrial backhaul, even that tolerance is nominal: a single event can compromise both paths.

Landing stations warrant specific attention. They are terrestrial, fixed, publicly locatable facilities, frequently situated in remote coastal areas with limited surveillance. They concentrate, at a single point, the optical terminal equipment, the power feed for the submarine repeaters, and the interconnection to the terrestrial network. In the Arctic context they carry an additional vulnerability, addressed in the following section: many sit on ground whose geotechnical stability is changing.

---

## 3. The Arctic Climate as a Physical Risk Vector

The Arctic is warming at several times the global average rate, a phenomenon documented in the climatological literature as Arctic amplification. The consequences for cable infrastructure distribute across five distinct mechanisms.

### 3.1 Sea-Ice Retreat: Enablement and Exposure

The annual minimum extent of Arctic sea ice, measured in September, shows a consistent declining trend over the past four decades. For the cable industry, the primary effect is enabling: longer navigation windows permit laying operations on previously inaccessible routes, which is a precondition for projects such as Far North Fiber.

The secondary effect, however, is exposure. Navigable waters attract commercial, fishing, and tourist maritime traffic. The dominant cause of submarine cable faults globally is neither sabotage nor natural disaster, but routine human activity — dragged anchors and bottom-trawling gear. A navigable Arctic is, by construction, an Arctic in which that dominant cause begins to operate. Reduced ice does not eliminate ice risk: drifting icebergs and ice keel scouring of the seabed remain threats in shallow coastal waters, and increased ice mobility may make such events less predictable.

### 3.2 Permafrost Degradation Beneath Terrestrial Facilities

This is the mechanism of greatest relevance to landing stations and terrestrial backhaul. Permafrost thaw reduces the bearing capacity of the ground, produces differential settlement, and compromises foundations designed on the premise of permanently frozen terrain. Hjort et al. (2018), in a study published in *Nature Communications*, estimated that a majority share of built infrastructure in the Arctic permafrost domain — on the order of 70% — lies in areas at elevated risk of thaw-related damage by mid-century.

The implication for cables is direct and frequently underestimated: the resilience of a submarine system is generally assessed by its submerged segment, yet the point of failure may be on dry land, beneath a landing facility whose foundation is shifting.

### 3.3 Coastal Erosion and Seabed Instability

The combination of degraded coastal permafrost, reduced protection from sea ice, and greater wave energy accelerates the erosion of Arctic coastlines, with retreat rates reaching several metres per year in some stretches. Cables landing on such coasts may have their beach segment exposed, displaced, or subjected to mechanical stresses not anticipated in design. In the submarine environment, increased fluvial sediment supply and slope instability raise the probability of turbidity currents — mass sediment flows capable of severing multiple cables simultaneously along a single submarine canyon, with documented precedents in other regions of the world.

### 3.4 Thermal Effects on the Optical System

Temperature variation affects optical and electronic parameters in long-haul systems. In the deep submarine segment, temperature is stable and the effect is marginal. Sensitivity concentrates in shallow segments, in the terrestrial portion, and in landing station equipment, where changes in the thermal regime and in ground stability influence both performance and the maintenance cycle. This is a secondary factor compared with the geotechnical mechanisms, but relevant to design margins in systems with a projected 25-year service life — a horizon over which baseline environmental conditions can no longer be treated as stationary.

### 3.5 Seasonal Constraint on Repair Capacity

Repair time is the variable that converts a fault into a crisis. Globally, submarine cable repair depends on a specialised fleet of cable ships that is numerically small, of high average age, and unevenly distributed. In the Arctic, three factors compound the situation: the distance to bases of available vessels, the need for an ice-class hull to operate for part of the year, and restricted weather windows. A fault occurring in early winter may remain unrepaired for months.

This point deserves analytical emphasis: in temperate regions, resilience is discussed largely in terms of path redundancy. In the Arctic, path redundancy is necessary but insufficient, because the outage window for any given path is structurally longer.

---

## 4. Cables as Critical Infrastructure: Dependencies and Cascading Effects

The classification of submarine cables as critical infrastructure follows less from the service they provide directly than from the dependencies other sectors have built upon them.

**Energy.** Modern generation and transmission systems depend on telemetry, remote supervision, and coordination between operators. Where IT/OT (operational technology) convergence has been implemented with a dependency on external connectivity — for cloud monitoring, predictive maintenance, or remote vendor access — loss of international connectivity degrades the capacity for supervised operation. Power and telecommunications cables frequently share corridors in the Baltic, creating failure correlation between the two sectors.

**Financial and public services.** The advanced digitalisation of the Nordic states, with digital identity, electronic payments, and predominantly online public services, converts a connectivity interruption into an interruption of services essential to citizens.

**Health and remote operations.** In sparsely populated Arctic territories, telemedicine and remote support for search-and-rescue operations are not conveniences but components of the care system.

**Science and Earth observation.** The Svalbard case is illustrative: the SvalSat station downlinks data from polar observation satellites for international operators, and the onward flow of that data depends on the submarine cable. Damage to the link affects users well beyond Norway.

**Data centres.** The region's attractiveness for large-scale computing rests on cheap renewable power and free cooling, but the economic value of that workload is realised only through international connectivity. Concentrating compute in a location with few egress paths transfers the concentration risk from the cable to the services hosted on it.

### 4.1 Reference Incidents

**Svalbard, January 2022.** One of the two cables in the Svalbard system sustained damage in a deep-water segment. The remaining link maintained the archipelago's connectivity, which demonstrated the value of the existing redundancy — and, simultaneously, the fact that the system operated throughout the repair period without any further margin. The investigation conducted by Norwegian authorities pointed to human activity as the probable cause, without reaching a conclusive attribution. The absence of attribution is itself an analytically relevant finding.

**Balticconnector and associated cables, October 2023.** The Balticconnector gas pipeline between Finland and Estonia and nearby telecommunications cables were damaged simultaneously. The Finnish investigation focused on anchor dragging by a commercial vessel.

**Baltic Sea, November 2024.** The BCS East-West Interlink (Lithuania–Sweden) and C-Lion1 (Finland–Germany) cables were damaged within roughly 24 hours of each other, in a pattern consistent with anchor dragging along a single shipping route.

**Estlink 2 and adjacent cables, December 2024.** The Estlink 2 power cable between Finland and Estonia and several telecommunications cables were damaged. Finnish authorities detained and investigated a tanker suspected of anchor dragging, marking an inflection in the region's law enforcement posture.

The pattern common to these cases is significant for risk analysis: the physical mechanism of the damage — an anchor dragged along the seabed — is identical to that of an ordinary maritime accident. That equivalence is precisely what makes attribution difficult, and what the security literature characterises as action below the threshold of armed conflict.

---

## 5. Threat Model: Natural, Accidental, and Adversarial

Conventional practice separates natural risk analysis from security risk analysis. For Nordic Arctic cables, that separation produces incomplete assessments, because all three origin types converge on the same small set of failure points and, in part, on the same physical mechanism.

**Table 2 — Consolidated threat model**

| Origin | Typical mechanism | Relative frequency | Repair time | Attribution |
|---|---|---|---|---|
| Natural — geotechnical | Permafrost thaw, coastal erosion, submarine landslide | Low per event, rising trend | Long (civil works) | Not applicable |
| Natural — ice | Ice keel scouring, drifting iceberg | Low to moderate, seasonal | Long (access constraint) | Not applicable |
| Accidental — human | Anchor, bottom-trawling gear | High (dominant cause globally) | Medium, window-constrained | Generally possible |
| Adversarial — hybrid | Deliberate anchor dragging, subsea intervention | Low, geographically concentrated | Medium to long | Difficult and frequently inconclusive |
| Adversarial — cyber | Compromise of network management and landing station systems | Not public | Variable | Difficult |

Three observations follow from this structure.

First, **ambiguity is a property of the domain, not a failure of investigation.** When the same physical act may be either accident or aggression, the institutional response is structurally slow, and a rational adversary obtains effect at reduced attribution risk.

Second, **climate shifts the baseline against which anomaly is measured.** A more navigable sea produces more genuinely accidental incidents. This raises the background noise, making the deliberate event harder to distinguish — which constitutes an interaction between the climate vector and the adversarial vector, not merely a temporal coincidence.

Third, **the cyber dimension should not be omitted.** Public discussion concentrates on physical damage, but network element management systems, power feed equipment, and landing station access controls constitute a logical attack surface. The same principles of defence in depth, segmentation, and identity management discussed for cloud-based critical infrastructure and for IT/OT convergence apply here.

---

## 6. Governance and Regulatory Framework

### 6.1 European Level

The NIS2 Directive (Directive (EU) 2022/2555) broadens the scope of entities subject to cyber risk management and incident notification requirements, explicitly including digital infrastructure. The CER Directive (Directive (EU) 2022/2557), on the resilience of critical entities, addresses the physical dimension and requires Member States to identify critical entities and conduct risk assessments that account for, among other factors, natural risks and climate change. Read together, the two directives are the most direct instrument for addressing the convergence analysed in this paper.

Applicability across the region is not uniform. Denmark, Sweden, and Finland are European Union Member States. Norway and Iceland are part of the European Economic Area, with incorporation through a distinct mechanism and timetable. Greenland and the Faroe Islands hold specific statuses. The result is a regulatory mosaic over an infrastructure that is, by nature, transboundary.

### 6.2 International Law of the Sea

The United Nations Convention on the Law of the Sea (UNCLOS) addresses the protection of submarine cables in Articles 113 to 115, obliging states to make it a punishable offence for a vessel flying their flag to damage a submarine cable wilfully or through culpable negligence. The regime has three operational weaknesses recognised in the literature: it depends on flag state jurisdiction, whose cooperation is uncertain; it was conceived for accidents rather than deliberate state action; and it offers limited interdiction instruments on the high seas. The 2024 Baltic events, in which coastal authorities adopted more assertive measures towards suspect vessels, indicate a practical test of that regime's limits.

### 6.3 Defence and Regional Cooperation

The recent institutional response includes maritime surveillance initiatives dedicated to protecting subsea infrastructure, among them operation Nordic Warden, conducted within the Joint Expeditionary Force, and the Baltic Sentry activity launched by NATO in January 2025 following the series of incidents. Finland's and Sweden's accession to NATO substantively altered the regional security architecture over the period analysed.

---

## 7. Resilience Strategies

The measures below are organised by implementation horizon and address the risk origins identified in Section 5 jointly.

### 7.1 Structural Diversity

**Route and landing diversity.** Redundancy is effective only when alternative paths share no submarine corridor, landing station, terrestrial backhaul, or power supplier. The assessment should be conducted as a common failure mode analysis, not as a count of cables. The Icelandic case, with the addition of IRIS on a distinct route, exemplifies the application of this principle.

**Technological heterogeneity.** Low Earth orbit satellite constellations do not substitute for a cable's capacity, but they can sustain minimum essential services — emergency communication, critical telemetry, response coordination — during the repair period. Sizing should be explicit about that limitation, and the satellite layer itself carries a distinct set of vulnerabilities.

### 7.2 Detection and Monitoring

**Distributed acoustic sensing (DAS).** Techniques that use the optical fibre itself as a distributed sensor allow mechanical events along the cable to be detected — including anchor activity in the vicinity — before damage occurs or immediately afterwards, with precise localisation. The value is twofold: it reduces fault localisation time, a significant component of total repair time, and it provides technical evidence for investigation and attribution.

**Fusion with maritime traffic data.** Correlating events detected in the fibre with AIS data allows anomalous patterns to be identified, including transponder shutdown and speeds inconsistent with normal navigation over known cable routes.

**Geotechnical monitoring of landings.** Instrumentation for ground temperature and settlement at stations located in the permafrost domain, integrated into the preventive maintenance cycle.

### 7.3 Response Capacity

**Regional repair capacity.** The availability of an ice-class cable ship stationed in the region, whether through a readiness contract shared among Nordic operators or a public-private arrangement, directly addresses the repair-time variable identified in Section 3.5. Among the measures listed, this is the costliest and the one with the greatest effect on aggregate risk.

**Cross-sector contingency planning.** Exercises involving telecommunications and energy operators, maritime authorities, and civil protection bodies, with scenarios that include prolonged unavailability rather than brief interruption alone.

### 7.4 Climate-Informed Design

Systems with a 25-year service life installed today will operate under environmental conditions significantly different from present ones. Route selection, burial depth, landing site choice, and foundation design should use regional climate projections as an input parameter, rather than historical series treated as stationary. For new trans-Arctic routes this principle is especially pertinent, given that the project's very viability follows from an environmental change still under way.

### 7.5 Synthesis

Table 3 relates each measure to the risk vectors of Section 5, showing which ones act on more than one risk origin at once — a useful prioritisation criterion where budget is limited.

**Table 3 — Resilience measures and risk vectors addressed**

| Measure | Geotechnical | Ice | Accidental | Adversarial | Horizon | Relative cost |
|---|:---:|:---:|:---:|:---:|---|---|
| Route and landing diversity | ✔ | ✔ | ✔ | ✔ | Long | High |
| Technological heterogeneity (satellite) | ✔ | ✔ | ✔ | ✔ | Short | Medium |
| Distributed acoustic sensing (DAS) | — | ✔ | ✔ | ✔ | Short | Low to medium |
| Fusion with AIS data | — | — | ✔ | ✔ | Short | Low |
| Geotechnical monitoring of landings | ✔ | — | — | — | Medium | Low |
| Ice-class cable ship in region | ✔ | ✔ | ✔ | ✔ | Medium | Very high |
| Cross-sector contingency planning | ✔ | ✔ | ✔ | ✔ | Short | Low |
| Climate-informed design | ✔ | ✔ | — | — | Long | Low for new build |

Two readings stand out. Distributed sensing and AIS fusion offer the best ratio of cost to vector coverage, acting on fault localisation time and on attribution capability. Regional repair capacity is the most expensive measure and the only one that directly reduces outage duration, the determining variable identified in Section 3.5.

---

## 8. Discussion

The central tension identified in this paper can be stated directly: **Arctic thaw is simultaneously the condition of possibility for, and the principal source of physical risk to, the region's new cable routes.** The same conditions that make a trans-Arctic route economically attractive — less ice, longer navigation windows — produce unstable landing ground, eroding coastlines, and denser maritime traffic over cable routes. Treating opportunity and risk as separate agendas, handled by distinct teams, is the analytical error this paper seeks to make visible.

A second conclusion concerns the relationship between climate and hybrid threat. No causal relationship between climate change and adversarial action is asserted here. The argument is more specific and, from a defence standpoint, more consequential: the increase in legitimate maritime traffic raises the rate of genuinely accidental incidents, which widens the background noise against which a deliberate event would have to be distinguished. In a domain where the physical mechanism of accident and of aggression are indistinguishable, raising the background noise is, functionally, degrading attribution capability.

A third observation concerns the asymmetry between the cost of attack and the cost of defence. Damaging a cable requires modest and widely available means. Protecting one requires continuous maritime surveillance over extensive areas, naval repair capacity, and expensive redundancy. That asymmetry is not eliminable by technical means; it shifts the weight of the response towards resilient design, early detection, and deterrence through attribution and credible legal consequence — which gives the regulatory discussion in Section 6 operational rather than merely formal weight.

---

## 9. Limitations

This work is a documentary and analytical review, based on academic literature, public regulatory documents, and publicly available incident reporting. It does not incorporate proprietary operational data from cable operators, whose disclosure is restricted for commercial and security reasons. The investigations into the 2022–2024 incidents are, in part, without definitive public conclusion, so the characterisations presented in Section 4 should be read as a description of what is publicly known, not as attribution. The quantitative estimates cited — the share of intercontinental traffic carried by cables, the proportion of Arctic infrastructure at thaw risk — derive from the sources indicated and carry the methodological uncertainties proper to them. Finally, the regulatory and regional security situation described reflects the state of affairs as of the time of writing and is subject to rapid change.

---

## 10. Conclusion

The submarine cable infrastructure of the Nordic Arctic occupies an unusual position in critical infrastructure analysis: it is the point at which climate risk, accidental risk, and geopolitical threat bear on the same physical asset, with the same failure modes and the same restricted set of repair options. The appropriate response is not to conduct three parallel risk analyses, but a single resilience analysis that recognises the interaction among these vectors.

Four priorities emerge from the analysis: structural diversity assessed by common failure mode rather than by cable count; early detection through sensing in the fibre itself, integrated with maritime traffic data; regional ice-class repair capacity, since outage duration is the variable that converts a fault into a crisis; and infrastructure design that adopts climate projections as an input parameter, given the mismatch between a 25-year service life and a non-stationary environment.

The physical layer of the internet was, for a long time, treated as a solved engineering problem. In the Nordic Arctic, it has become an open question of public policy, international law, and security once again.

---

## References

The references below indicate the sources and categories of material underpinning the analysis. Consultation of the most recent versions is recommended, given the rapid evolution of the subject.

1. Hjort, J. et al. *Degrading permafrost puts Arctic infrastructure at risk by mid-century.* Nature Communications, vol. 9, 2018.
2. TeleGeography. *Submarine Cable Map* and associated reports on international traffic and the cable ship fleet.
3. International Cable Protection Committee (ICPC). Publications on submarine cable fault causes and protection best practice.
4. European Union. Directive (EU) 2022/2555 (NIS2), on measures for a high common level of cybersecurity across the Union.
5. European Union. Directive (EU) 2022/2557 (CER), on the resilience of critical entities.
6. United Nations. United Nations Convention on the Law of the Sea (UNCLOS), Articles 113 to 115.
7. National Snow and Ice Data Center (NSIDC). Arctic sea ice extent series.
8. Arctic Monitoring and Assessment Programme (AMAP). Reports on Arctic amplification and infrastructure impacts.
9. Public reporting and official statements concerning the Svalbard (2022), Balticconnector (2023), and Baltic Sea (2024) incidents.
10. Public documentation of the Far North Fiber and Polar Connect (NORDUnet) projects.

---

*An academic and analytical paper compiled from public sources. A Portuguese-language version is available at [`Portuguese/Cabos_Articos_Nordicos.md`](../Portuguese/Cabos_Articos_Nordicos.md). Contributions, corrections, and discussion are welcome via issues or pull requests.*
