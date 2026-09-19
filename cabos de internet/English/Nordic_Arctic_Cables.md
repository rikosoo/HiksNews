# Subsea Cables in the Nordic Arctic: Climate, Geopolitics, and the Resilience of Critical Digital Infrastructure

## Abstract

Submarine fibre-optic cables carry very nearly all intercontinental data traffic — the widely repeated 99% figure rests on weak documentary foundations and is examined critically in Section 1 — making this physical layer a critical infrastructure asset as essential as power or transport networks. In the Nordic and Arctic region, that infrastructure operates under a singular condition: the same regional warming that makes new trans-Arctic routes viable, by reducing sea-ice cover and lengthening laying windows, is what degrades the conditions for installing, anchoring, and repairing those systems, through permafrost loss, coastal erosion, and intensified maritime traffic.

This paper analyses that tension in four movements. It maps the Nordic and Arctic cable landscape, including the trans-Arctic projects under development. It examines the Arctic climate as a physical risk vector, decomposed into five mechanisms, of which the seasonal constraint on repair capacity is the most determining. It integrates those mechanisms into a single threat model that treats natural, accidental, and adversarial origins as bearing on the same failure points — a model whose central premise, the indistinguishability of accident from aggression at the physical level, was confirmed judicially in the *Eagle S* case, where the Helsinki Court of Appeal held in August 2026 that the distinction rests not on the mechanism but on an assessment of subsequent conduct. Finally, it discusses the applicable regulatory framework (NIS2, the CER Directive, UNCLOS) and proposes resilience priorities ranked by risk vector addressed and by cost.

The argument advanced is that climate risk and adversarial risk are not separate agendas in this region but manifestations of a single resilience problem, and that the slowness of deterrence by legal route shifts the weight of the response towards early detection and resilient design.

---

## Keywords

Submarine Cables, Arctic Infrastructure, Critical Infrastructure Protection, Climate Resilience, Nordic Region, Hybrid Threats, Permafrost, Law of the Sea, UNCLOS, Cybersecurity

---

## 1. Introduction

Public perception of the internet is dominated by immaterial metaphors — cloud, ether, wireless. The operational reality is the opposite: intercontinental connectivity depends on a finite set of fibre-optic cables laid on the seabed, each a few centimetres in diameter, whose physical destruction interrupts digital services at national scale.

The figure most often repeated in this debate warrants care. The claim that "99% of intercontinental traffic travels through submarine cables" circulates widely in the press and in policy documents, almost always without a source. TeleGeography, to whom the figure is frequently attributed, notes that it holds no direct measurement of global traffic and that the traceable data point is a different one: statistics from the United States Federal Communications Commission indicate that satellites account for roughly 0.37% of US international capacity [8, 9]. The qualitative conclusion remains robust — dependence on the submarine layer is very nearly total, and satellite links function as redundancy of limited capacity rather than as a substitute — but the numerical precision often attached to it does not hold. This paper adopts the qualitative formulation.

Three characteristics make this topic particularly pressing in the Nordic region. First, structural dependency is high: Iceland, the Faroe Islands, Greenland, and Svalbard are territories whose entire connectivity rests on a very small number of cables — in some cases, two. Second, the region hosts an unusual density of sensitive digital infrastructure, including large-scale data centres drawn by the cold climate and inexpensive renewable energy, alongside satellite ground stations of scientific and military significance. Third, the retreat of Arctic sea ice has turned the region into the object of trans-Arctic route projects — notably Far North Fiber and Polar Connect — which promise to cut latency between Asia and Europe substantially relative to routes via Suez.

In parallel, the sequence of incidents between 2022 and 2024 in the Norwegian Arctic and the Baltic Sea moved submarine cables out of the category of technical asset and into that of security policy object. This paper takes that convergence as its point of departure and poses three research questions:

1. In what ways does Arctic climate change alter the physical risk profile of Nordic cable infrastructure?
2. How do climate risks and adversarial risks interact, rather than merely accumulate independently?
3. Which resilience strategies apply to an environment where repair capacity is geographically and seasonally constrained?

### 1.1 Method and Scope

The study is structured as a documentary and analytical review. Primary sources are of four kinds: peer-reviewed academic literature on permafrost degradation and climate impacts on Arctic infrastructure; European Union regulatory instruments and international law; technical reports from submarine cable sector bodies; and public reporting and official statements concerning the 2022–2024 incidents. No proprietary operational data from cable operators was used.

The geographic scope covers the five Nordic countries and their associated territories — Iceland, the Faroe Islands, Greenland, and Svalbard — extending to the Baltic Sea where recent incidents and the interconnection mesh require it. The temporal scope of the incidents analysed runs from 2022 to the end of 2024; the judicial and institutional developments arising from them are followed to August 2026, since the case law produced in the Eagle S proceedings bears directly on the analysis in Section 6.2. Limitations arising from these choices are set out in Section 9.

This paper is in dialogue with other work in this repository, in particular [*Security Challenges in Cloud-Based Critical Infrastructure Systems*](../../academics/Security_Challenges.md), which addresses the logical and cloud layer of the same asset class, and [*IT and OT as a Bridge of Friendship*](../../academics/ItAndOT.md), which examines the information/operational technology convergence referenced in Section 4.

---

## 2. The Nordic and Arctic Cable Landscape

### 2.1 Current Configuration

The region's cable infrastructure can be organised into four layers.

**North Atlantic links.** Iceland is served by a small set of systems: FARICE-1, operational since 2004, connecting the country to the Faroe Islands and Scotland; DANICE, since 2009, landing in Denmark; and IRIS, which entered service in 2023, establishing a direct route to Ireland. IRIS was added on an explicit national redundancy argument, which illustrates state-level recognition of the problem.

**Arctic and island links.** The Svalbard Undersea Cable System, comprising two fibre pairs between Longyearbyen and mainland Norway, supports not only the archipelago's civilian population but also data transmission from the SvalSat satellite station, which serves international scientific and commercial operators. Greenland depends on Greenland Connect, operational since 2009, in an equally concentrated configuration.

**Intra-Nordic and Baltic links.** The Baltic Sea is crossed by a dense mesh of telecommunications and power cables interconnecting Finland, Sweden, Estonia, Lithuania, Poland, and Germany. Among them, C-Lion1 (Helsinki–Rostock) and the BCS East-West Interlink (Lithuania–Sweden) became prominent through the damage sustained in 2024. The determining geographic characteristic here is depth: the Baltic is a shallow sea, which places cables within reach of commercial vessel anchors along much of their route.

**Trans-Arctic routes under development.** The Far North Fiber project, a joint venture between Finland's Cinia, the US-based Far North Digital, and Japan's Arteria Networks, proposes to connect Japan and Europe across the Northwest Passage over roughly 14,000 kilometres, with landings planned in Alaska, the Canadian Arctic, Greenland, Iceland, Norway, Finland, and Ireland. Polar Connect, pursued within NORDUnet and the Nordic academic networks, is studying a route from Norway via Svalbard across the Arctic Ocean [10]. Both derive their viability from ice conditions altered by regional warming.

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
| Far North Fiber | Japan – Europe, via the Northwest Passage (~14,000 km) | In implementation | Cinia / Far North Digital / Arteria consortium; viability arising from ice retreat |
| Polar Connect | Norway – Svalbard – Arctic – Asia / North America | Under study | Led by Nordic academic networks, with European co-financing |

### 2.2 Concentration and Chokepoints

From a critical infrastructure protection standpoint, the most relevant feature of this landscape is not the number of cables but the distribution of dependency. A territory served by two cables has, in practice, single-fault tolerance. Where both share a geographic corridor, a landing station, or terrestrial backhaul, even that tolerance is nominal: a single event can compromise both paths.

Landing stations warrant specific attention. They are terrestrial, fixed, publicly locatable facilities, frequently situated in remote coastal areas with limited surveillance. They concentrate, at a single point, the optical terminal equipment, the power feed for the submarine repeaters, and the interconnection to the terrestrial network. In the Arctic context they carry an additional vulnerability, addressed in the following section: many sit on ground whose geotechnical stability is changing.

---

## 3. The Arctic Climate as a Physical Risk Vector

The Arctic is warming at several times the global average rate, a phenomenon documented in the climatological literature as Arctic amplification. Rantanen et al. (2022) estimate that over the period 1979 to 2021 the region warmed approximately 3.8 times faster than the planetary average, with a higher ratio still in the Barents Sea [2]. The consequences for cable infrastructure distribute across five distinct mechanisms.

### 3.1 Sea-Ice Retreat: Enablement and Exposure

The annual minimum extent of Arctic sea ice, measured in September, shows a consistent declining trend over the past four decades, per the National Snow and Ice Data Center series [4] and the syntheses of the Arctic Monitoring and Assessment Programme [5]. For the cable industry, the primary effect is enabling: longer navigation windows permit laying operations on previously inaccessible routes, which is a precondition for projects such as Far North Fiber.

The secondary effect, however, is exposure. Navigable waters attract commercial, fishing, and tourist maritime traffic — and the dominant cause of submarine cable faults globally is neither sabotage nor natural disaster, but precisely that routine human activity. Sector data compiled by the International Cable Protection Committee place dragged anchors and bottom-trawling gear at between 70% and 80% of all faults, within a universe on the order of two hundred faults per year across global systems [6, 7]. It follows that a navigable Arctic is, by construction, an Arctic in which that dominant cause begins to operate.

It bears noting that reduced ice does not eliminate ice-related risk. Drifting icebergs and ice keel scouring of the seabed remain threats in shallow coastal waters, and increased ice mobility may make such events less predictable.

### 3.2 Permafrost Degradation Beneath Terrestrial Facilities

This is the mechanism of greatest relevance to landing stations and terrestrial backhaul. Permafrost thaw reduces the bearing capacity of the ground, produces differential settlement, and compromises foundations designed on the premise of permanently frozen terrain. Hjort et al. (2018), in a study published in *Nature Communications*, estimated that some 70% of built infrastructure in the permafrost domain lies in areas with high potential for near-surface permafrost thaw, and that roughly one-third of pan-Arctic infrastructure sits in regions where thaw-related ground instability can cause severe damage to the built environment by mid-century — proportions which, the authors note, are not substantially reduced even under a scenario in which the Paris Agreement targets are met [1].

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

**Svalbard, January 2022.** On 7 January 2022 one of the two cables in the Svalbard system — a link of roughly 1,300 km operated by Space Norway — lost communication after damage in a deep-water segment. The remaining link maintained the archipelago's connectivity, which demonstrated the value of the existing redundancy and, at the same time, exposed the fact that the system operated throughout the repair period without any further margin. Marks on the recovered cable were consistent with scraping by an object towed along the seabed, typically a trawl door. Norwegian police considered human activity the probable origin, did not establish intent, and closed the investigation for want of evidence, with no one charged [14]. The episode is examined in detail by Schia, Gjesvik and Rødningen [3], who trace the chain of consequences and the management of the crisis. The absence of conclusive attribution is itself an analytically relevant finding, taken up in Section 5.

**Balticconnector and associated cables, October 2023.** The Balticconnector gas pipeline between Finland and Estonia and nearby telecommunications cables were damaged simultaneously. The Finnish investigation focused on anchor dragging by a commercial vessel.

**Baltic Sea, November 2024.** The BCS East-West Interlink (Lithuania–Sweden) and C-Lion1 (Finland–Germany) cables were damaged within roughly 24 hours of each other, in a pattern consistent with anchor dragging along a single shipping route. The operator Cinia recorded the C-Lion1 fault at 04:04 Eastern European Time on 18 November 2024, attributed it to external physical force, and filed a request for investigation with the Finnish National Bureau of Investigation the following day [16]; service was restored on 28 November, after ten days of unavailability and the transit of a repair vessel from Calais [17]. The interval illustrates the argument of Section 3.5, even in a sea of comparatively easy access.

**Estlink 2 and adjacent cables, December 2024.** On 25 December 2024 the Estlink 2 power cable between Finland and Estonia and four telecommunications cables were damaged. Finnish authorities brought the tanker *Eagle S*, registered in the Cook Islands, into Finnish territorial waters and opened an investigation; according to the National Bureau of Investigation, the vessel dragged its anchor along the seabed for a distance on the order of ninety to one hundred kilometres [15]. The episode marked an inflection in the region's law enforcement posture and produced the judicial development addressed in Section 6.2, whose significance exceeds that of the isolated incident.

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
| Adversarial — cyber | Compromise of network management and landing station systems | No consolidated public data | Variable | Difficult |

Three observations follow from this structure.

First, **ambiguity is a property of the domain, not a failure of investigation.** When the same physical act may be either accident or aggression, the institutional response is structurally slow, and a rational adversary obtains effect at reduced attribution risk.

Second, **climate shifts the baseline against which anomaly is measured.** A more navigable sea produces more genuinely accidental incidents. This raises the background noise, making the deliberate event harder to distinguish — which constitutes an interaction between the climate vector and the adversarial vector, not merely a temporal coincidence.

Third, **the cyber dimension should not be omitted.** Public discussion concentrates on physical damage, but network element management systems, power feed equipment, and landing station access controls constitute a logical attack surface. The same principles of defence in depth, segmentation, and identity management discussed for cloud-based critical infrastructure and for IT/OT convergence apply here.

---

## 6. Governance and Regulatory Framework

### 6.1 European Level

The NIS2 Directive (Directive (EU) 2022/2555) [11] broadens the scope of entities subject to cyber risk management and incident notification requirements, explicitly including digital infrastructure. The CER Directive (Directive (EU) 2022/2557) [12], on the resilience of critical entities, addresses the physical dimension and requires Member States to identify critical entities and conduct risk assessments that account for, among other factors, natural risks and climate change. Read together, the two directives are the most direct instrument for addressing the convergence analysed in this paper.

Applicability across the region is not uniform. Denmark, Sweden, and Finland are European Union Member States. Norway and Iceland are part of the European Economic Area, with incorporation through a distinct mechanism and timetable. Greenland and the Faroe Islands hold specific statuses. The result is a regulatory mosaic over an infrastructure that is, by nature, transboundary.

### 6.2 International Law of the Sea

The United Nations Convention on the Law of the Sea (UNCLOS) [13] addresses the protection of submarine cables in Articles 113 to 115, obliging states to make it a punishable offence for a vessel flying their flag to damage a submarine cable wilfully or through culpable negligence. The regime has three operational weaknesses recognised in the literature: it depends on flag state jurisdiction, whose cooperation is uncertain; it was conceived for accidents rather than deliberate state action; and it offers limited interdiction instruments on the high seas.

The *Eagle S* case turned that doctrinal discussion into case law. In October 2025 the Helsinki District Court dismissed the criminal proceedings against the vessel's master and two officers on the ground that Finland lacked jurisdiction: the acts charged had occurred in the Finnish exclusive economic zone, outside the territorial sea, and Finnish criminal law therefore did not reach them. The ruling resonated as a concrete demonstration of the gap the literature had identified — vessels under flags of convenience could damage subsea infrastructure in non-territorial waters without effective criminal consequence.

On 27 August 2026 the Helsinki Court of Appeal unanimously overturned that decision, affirming Finnish jurisdiction and ordering the case reopened at first instance [18, 19]. Its reasoning is analytically relevant here: while the court accepted that the initial dropping of the anchor might be treated as accidental, it held that what followed — the prolonged drag along the seabed — does not fall within the category of maritime accident for UNCLOS purposes. The decision is not final and may be appealed to the Supreme Court, with the deadline falling in October 2026.

The episode confirms the central claim of Section 5 by judicial route: the line separating accident from aggression is not given by the physical mechanism, which is identical in both cases, but by an assessment of subsequent conduct. So long as that assessment depends on protracted litigation of uncertain outcome, deterrence through legal consequence remains weak — which raises the relative weight of the detection and resilient-design measures discussed in Section 7.

### 6.3 Defence and Regional Cooperation

The recent institutional response includes maritime surveillance initiatives dedicated to protecting subsea infrastructure, among them operation Nordic Warden, conducted within the Joint Expeditionary Force, and the Baltic Sentry activity launched by NATO on 14 January 2025 following the series of incidents, led by Allied Joint Force Command Brunssum in coordination with Allied Maritime Command [20]. Finland's and Sweden's accession to NATO substantively altered the regional security architecture over the period analysed.

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

A third observation concerns the asymmetry between the cost of attack and the cost of defence. Damaging a cable requires modest and widely available means. Protecting one requires continuous maritime surveillance over extensive areas, naval repair capacity, and expensive redundancy. That asymmetry is not eliminable by technical means; it shifts the weight of the response towards resilient design, early detection, and deterrence through attribution and credible legal consequence — which gives the regulatory discussion in Section 6 operational rather than merely formal weight. The judicial trajectory of the *Eagle S* case, which consumed nearly two years merely to settle which forum had competence, measures the distance between the deterrence intended and the deterrence actually available.

---

## 9. Limitations

This work is a documentary and analytical review, based on academic literature, public regulatory documents, and publicly available incident reporting. It does not incorporate proprietary operational data from cable operators, whose disclosure is restricted for commercial and security reasons. The investigations into the 2022–2024 incidents are, in part, without definitive public conclusion, so the characterisations presented in Section 4 should be read as a description of what is publicly known, not as attribution. The quantitative estimates cited — the share of intercontinental traffic carried by cables, the proportion of Arctic infrastructure at thaw risk — derive from the sources indicated and carry the methodological uncertainties proper to them. Finally, the regulatory and regional security situation described reflects the state of affairs as of September 2026 and is subject to rapid change; in particular, the outcome of the *Eagle S* case remains pending a possible appeal to the Finnish Supreme Court, so the conclusions of Section 6.2 should be read as analysis of a precedent that is not yet settled.

---

## 10. Conclusion

The submarine cable infrastructure of the Nordic Arctic occupies an unusual position in critical infrastructure analysis: it is the point at which climate risk, accidental risk, and geopolitical threat bear on the same physical asset, with the same failure modes and the same restricted set of repair options. The appropriate response is not to conduct three parallel risk analyses, but a single resilience analysis that recognises the interaction among these vectors.

Returning to the questions posed in Section 1:

**On the physical risk profile (question 1),** regional warming does not shift that profile in a single direction. It reconfigures it: enabling routes as the ice retreats, while simultaneously degrading the foundations of landing stations through permafrost thaw, exposing coastal segments to erosion, raising the probability of seabed instability events, and widening exposure to anchors and fishing gear as the sea becomes navigable. The mechanism of greatest practical consequence, however, is not the damage itself but the seasonal constraint on repair capacity, which structurally lengthens the outage window.

**On the interaction between vectors (question 2),** no causal relationship between climate change and adversarial action holds. Something more specific does: by raising the volume of legitimate maritime traffic, the thaw increases the rate of genuinely accidental incidents and, with it, the background noise against which a deliberate event would have to be distinguished. In a domain where the physical mechanism of accident and of aggression are identical, raising that noise amounts to degrading attribution capability. The *Eagle S* case gave this proposition judicial confirmation and measured its cost: nearly two years of litigation merely to settle which forum had competence.

**On the applicable strategies (question 3),** four priorities emerge, ranked in Table 3. Structural diversity assessed by common failure mode rather than by cable count. Early detection through sensing in the fibre itself, integrated with maritime traffic data — the measure with the best ratio of cost to vector coverage. Regional ice-class repair capacity, the most expensive and the only one that directly reduces outage time. And infrastructure design that adopts climate projections as an input parameter, given the mismatch between a 25-year service life and a non-stationary environment.

The physical layer of the internet was, for a long time, treated as a solved engineering problem. In the Nordic Arctic, it has become an open question of public policy, international law, and security once again.

---

## References

Twenty references, in an author–date style with numbered in-text keys. All online sources were verified on **19 September 2026**, the access date given in each entry. Entries [14], [18] and [19] are journalistic or academic-blog sources, used under the conditions described in the note at the end.

### Academic literature

[1] Hjort, J., Karjalainen, O., Aalto, J., Westermann, S., Romanovsky, V. E., Nelson, F. E., Etzelmüller, B. and Luoto, M. (2018) 'Degrading permafrost puts Arctic infrastructure at risk by mid-century', *Nature Communications*, 9, art. 5147, 11 December. DOI: 10.1038/s41467-018-07557-4. Available at: https://www.nature.com/articles/s41467-018-07557-4 (Accessed: 19 September 2026).

[2] Rantanen, M., Karpechko, A. Yu., Lipponen, A., Nordling, K., Hyvärinen, O., Ruosteenoja, K., Vihma, T. and Laaksonen, A. (2022) 'The Arctic has warmed nearly four times faster than the globe since 1979', *Communications Earth & Environment*, 3, art. 168, 11 August. DOI: 10.1038/s43247-022-00498-3. Available at: https://www.nature.com/articles/s43247-022-00498-3 (Accessed: 19 September 2026).

### Climate and environmental data

[3] Schia, N. N., Gjesvik, L. and Rødningen, I. (2023) *The subsea cable cut at Svalbard January 2022: What happened, what were the consequences, and how were they managed?* NUPI Policy Brief 1/2023. Oslo: Norwegian Institute of International Affairs. Available at: https://www.nupi.no/content/pdf_preview/26372/file/NUPI_Policy_Brief_1_23_Schia_Gjesvik_R%C3%B8dningen-FERDIG.pdf (Accessed: 19 September 2026).

### Climate and environmental data

[4] Fetterer, F., Knowles, K., Meier, W. N., Savoie, M., Windnagel, A. K. and Stafford, T. (2025) *Sea Ice Index*, Version 4 [dataset G02135]. Boulder, CO: National Snow and Ice Data Center. DOI: 10.7265/a98x-0f50. Available at: https://nsidc.org/data/g02135/versions/4 (Accessed: 19 September 2026).

[5] Arctic Monitoring and Assessment Programme (2021) *Arctic Climate Change Update 2021: Key Trends and Impacts*. Tromsø: AMAP, viii + 148 pp. Available at: https://www.amap.no/documents/doc/amap-arctic-climate-change-update-2021-key-trends-and-impacts/3594 (Accessed: 19 September 2026).

### Submarine cable infrastructure

[6] European Union Agency for Cybersecurity (2023) *Subsea Cables — What is at Stake?* Athens: ENISA, July. Available at: https://www.enisa.europa.eu/sites/default/files/publications/Undersea%20cables%20-%20What%20is%20a%20stake%20report.pdf (Accessed: 19 September 2026).

[7] International Cable Protection Committee (n.d.) *Government Best Practices for Protecting and Promoting Resilience of Submarine Telecommunications Cables*, version 1.2. ICPC. Available at: https://www.iscpc.org/documents/?id=3733 (Accessed: 19 September 2026).

[8] TeleGeography (2023) *Do Submarine Cables Account For Over 99% of Intercontinental Data Traffic?* Mythbusting series, part 3. Available at: https://resources.telegeography.com/2023-mythbusting-part-3 (Accessed: 19 September 2026).

[9] TeleGeography (n.d.) *Submarine Cable FAQs*. Available at: https://www2.telegeography.com/submarine-cable-faqs-frequently-asked-questions (Accessed: 19 September 2026).

[10] NORDUnet (n.d.) *Polar Connect*. Trans-Arctic link project description. Available at: https://nordu.net/polar-connect/ (Accessed: 19 September 2026).

### Legal instruments

[11] European Union (2022) *Directive (EU) 2022/2555 of the European Parliament and of the Council of 14 December 2022 on measures for a high common level of cybersecurity across the Union (NIS 2 Directive)*. Official Journal of the European Union, L 333, pp. 80–152, 27 December. CELEX 32022L2555. Available at: http://data.europa.eu/eli/dir/2022/2555/oj (Accessed: 19 September 2026).

[12] European Union (2022) *Directive (EU) 2022/2557 of the European Parliament and of the Council of 14 December 2022 on the resilience of critical entities and repealing Council Directive 2008/114/EC (CER Directive)*. Official Journal of the European Union, L 333, pp. 164–198, 27 December. CELEX 32022L2557. In force since 16 January 2023. Available at: http://data.europa.eu/eli/dir/2022/2557/oj (Accessed: 19 September 2026).

[13] United Nations (1982) *United Nations Convention on the Law of the Sea*. Montego Bay, 10 December. *United Nations Treaty Series*, vol. 1833, p. 3. In force since 16 November 1994. Articles 113–115. Available at: https://www.un.org/depts/los/convention_agreements/texts/unclos/unclos_e.pdf (Accessed: 19 September 2026).

### Primary sources on incidents

[14] The Barents Observer (2022) *'Human activity' behind Svalbard cable disruption*. Kirkenes, February. Available at: https://thebarentsobserver.com/en/security/2022/02/unknown-human-activity-behind-svalbard-cable-disruption (Accessed: 19 September 2026).

[15] Poliisi — Finnish Police (2024) *Police investigating incidents in the Gulf of Finland in cooperation with other authorities*. Official statement, 26 December. Available at: https://poliisi.fi/en/-/police-investigating-incidents-in-the-gulf-of-finland-in-cooperation-with-other-authorities (Accessed: 19 September 2026).

[16] Cinia Oy (2024) *A fault in the Cinia C-Lion1 submarine cable between Finland and Germany*. Official statement, 18 November. Available at: https://www.cinia.fi/en/news/a-fault-in-the-cinia-c-lion1-submarine-cable-between-finland-and-germany (Accessed: 19 September 2026).

[17] Cinia Oy (2024) *Cinia's C-Lion1 Submarine Cable Has Fully Restored*. Official statement, 28 November. Available at: https://www.cinia.fi/en/news/cinias-c-lion1-submarine-cable-has-fully-restored (Accessed: 19 September 2026).

[18] Yle News (2026) *Court u-turn: Finland does have jurisdiction in Eagle S cable damage case*. Helsinki, 27 August. Available at: https://yle.fi/a/74-20243196 (Accessed: 19 September 2026).

[19] *Anchoring Criminal Jurisdiction at Sea: The Helsinki District Court's Eagle S Judgement and its impact for the protection of submarine cables and pipelines* (2025). EJIL: Talk! — Blog of the European Journal of International Law. Available at: https://www.ejiltalk.org/anchoring-criminal-jurisdiction-at-sea-the-helsinki-district-courts-eagle-s-judgement-and-its-impact-for-the-protection-of-submarine-cables-and-pipelines/ (Accessed: 19 September 2026).

### Defence and regional cooperation

[20] NATO Allied Maritime Command (2025) *NATO's Baltic Sentry steps up patrols in the Baltic Sea to safeguard Critical Undersea Infrastructure*. Northwood. Available at: https://mc.nato.int/media-centre/news/2025/nato-baltic-sentry-steps-up-patrols-in-the-baltic-sea-to-safeguard-critical-undersea-infrastructure (Accessed: 19 September 2026).

### Note on sources

References [18] and [19] are, respectively, public-service journalism and doctrinal analysis on a specialist academic blog. They are used because, as of the access date, no full published text of the Helsinki District Court and Court of Appeal decisions was available in an open-access repository. For formal academic use, substitution with the original judgments is recommended once available. The authorship of entry [19] should be checked against the source before formal citation.

---

*An academic and analytical paper compiled from public sources. A Portuguese-language version is available at [`Portuguese/Cabos_Articos_Nordicos.md`](../Portuguese/Cabos_Articos_Nordicos.md). Contributions, corrections, and discussion are welcome via issues or pull requests.*
