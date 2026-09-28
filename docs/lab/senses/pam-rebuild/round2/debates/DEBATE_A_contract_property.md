# DEBATE A — What property should the memory contract check?

**PAM rebuild, round 2, crew A. Date: 2026-09-22.**
**Question:** six forks died on the KB4 problem (adversarial false installs). Every fork's *gate mechanism* was load-bearing; what died was the *property* each gate checked. What property should the round-2 contract check?

## Method note (read this first)

This crew ran as **structured proposition/opposition swarm rounds**, not as parallel subagent crews: a depth-2 subagent cannot spawn children, so each property was debated by two explicit teams — Team FOR (steelman the property) vs Team AGAINST (steelman the killing argument) — through opening statements, rebuttals, and a judging pass. No strawmen: each team's best case is presented before it is ruled on. Second opinions were solicited live from **gpt-5.6-sol** and **grok-4.6** via the UnoRouter connector (verbatim, §13). ExperientialLabs was checked live during this debate and is **empty** (balance $-0.02, `insufficient_credits`, 2026-09-22) — documented, not assumed.

**Frozen sources verified, not re-derived:** `../HYPOTHESES.md` (all six hypotheses verbatim) and per-fork verdicts under `../forks/{H1,H2,H3,G1,G2,G3}/`. Key numbers below are copied from those verdicts. Baseline Approach A fails the KB4 adversarial false-install test at 59% (round-1 summary).

## §1. The frozen evidence both teams accept

| Fork | Contract property checked | B1 viability | KB4 false-install (bar) | Fate |
|---|---|---|---|---|
| H1 Witnessed Event Lattice | witness-addressability / provenance (support ≥ threshold, contradiction = 0, corroboration) | 74.7% | 44.5% (118/265), bar 5% | DEAD |
| H2 Executable Percept Programs | executable testability (+ 1 prediction outside source span) | 84.3% | **0% (0/10,000)**, bar 3% — but kill-2: only 38.9% of wrong high-conf percepts self-flagged (bar 90%) | DEAD |
| H3 Counterfactual Predictive State | persistence-over-time (prediction confirmation across episodes) | 72.6% | 22.95% (70/305), bar 4% | DEAD |
| G1 Symmetry Group | generator match within 5-bit Hamming | 62.9% | 54.5% per-install (6/11), bar 5% | KILLED |
| G2 Predictive Residual | predictability (residual norm < 24 + hash match) | 75.4% | 23.9% (50/209), bar 8% | KILLED |
| G3 Relational Signature | relational distinctiveness (exact-match on hashed signature) | 98.6% | 4.36% (12/275), bar 1% | DEAD |

Two facts neither team disputes:

1. **Every gate was load-bearing.** Ablation (always-install) raised false installs in all six forks: H1 118 vs 224, H2 0 vs 186, H3 70 vs 174, G1 6 vs 41, G2 50 vs 132, G3 12 vs 102. The *mechanism* of gating installation works. What died was the *property* checked.
2. **H2 is the outlier that constrains every theory.** Its gate made ZERO false permanent installs in 10,000 trials. It died on kill-2 (percept self-calibration, 38.9% vs 90%), while the gate itself withheld all 108 wrong high-confidence percepts anyway. Any theory of "what property to check" must explain H2's clean safety record, not just the five deaths.

## §2. The opening proposition both teams accepted: the shared-measurement trap

Before debating individual properties, both teams agreed on the unifying pattern, because it is visible in all six verdicts:

> **Every dead gate checked evidence downstream of — or identical to — the evidence that formed the percept.** H1's witnesses were the same regions the lattice measured. H3's predictions re-ran T0's own measurements (verdict: "predictions check the same measurements the baseline uses — fooled together"). G2's residuals lived in the same invariant space as the fooled front-end. G3's signature was hashed from the same quantized features the attacks manipulated. G1's generators came from the same segmentation the attacks broke. When the front-end is fooled, a gate that re-reads the front-end's evidence certifies the mistake. H2 survived only where its gate demanded evidence the front-end had not seen: rule 4's successful prediction *outside the original source span*.

The teams split on what follows from this: Team FOR (for most properties) argues each property can be repaired by bolting on evidence-independence; Team AGAINST argues that concession proves the property itself was never the load-bearing part. The judging pass rules property by property below.

## §3. P1 — Predictability ("the world continues as it is")

**Team FOR (steelman):** Prediction is the only forward-looking check available at install time. G2's gate was load-bearing — it cut false installs from 132 to 50 (B4: 50.8% of attack dispositions changed). Residuals are nearly free on images (+12 ops/fixture). The failure was calibration and predictor choice, not the property: G2 used one generic stationarity prior ("world continues as it is") for every judgment task. Motiondir's 27 false installs came from a constant-velocity predictor that is *satisfied* by reversed videos — the wrong predictor for a direction judgment. Match the predictor to the judgment (predict the *consequences of the claimed class*), tune EPS per task instead of one global EPS=24, and predictability becomes a real check.

**Team AGAINST (steelman):** The kill is conceptual, not calibration. Predictability measures "does the observation match the model of how the world continues" — but adversarial falsehoods *are* predictable. The adversary crafts inputs the front-end misreads while the world continues normally: reversed video keeps constant velocity while the direction readout is wrong (adversarial motion judgment accuracy 37.1%, yet 53 installs). No EPS tuning fixes orthogonality. G2's own data proves the lies were not borderline: false installs had mean residual norm 4.6 against EPS=24 — confidently predictable, not near-threshold. And the hash-equality gate did all the real work while being uneven across tasks (colorconst: brutally strict, 5 installs with 0 false but 81.7% judgment accuracy starved of memories; motion: 53 installs, 27 false). Tuning trades recall for nothing.

**Rebuttals.** FOR: compute residuals against the *judgment's predicted consequences*, not a generic world-prior — a wrong direction judgment then predicts the wrong future and the residual spikes. AGAINST: that is no longer predictability as G2 specified it — it is H2's executable tests (predicted consequences of the *claim*). The property as specified dies; the rescue is a different property wearing its name.

**Judge's ruling: P1 DIES as an install-gate property.** "Predictable ≠ right" stands as the sharpest negative result of round 1. Predictability survives only as a *retrieval bias* (G2's confidence modulation ±100 on predicted-byte agreement harmed nothing), never as an install warrant.

## §4. P2 — Witness-addressability / provenance ("show me where you saw it")

**Team FOR (steelman):** Provenance is what makes a memory auditable, re-checkable, and revocable instead of a bare assertion. H1's ledger machinery is the program's best audit artifact: 1,165/1,165 fixtures byte-identical across three runs, 850/850 ledger entries independently re-verified with a from-scratch checker. And there is an existence proof the contract works *as designed*: on motiondir — where the flicker/two-motion traps genuinely produced contradiction > 0 — the contract saw it: 0/41 false installs, 91.1% recall. Provenance turns "trust me" into "check here," which is the only honest basis for a memory that must later be revised.

**Team AGAINST (steelman):** Auditability is not truth. H1's deciding failure is the cleanest in the program: the contract is a filter on *reported confidence*, not a check on truth. The adversarial traps produced high-support, zero-contradiction, mutually corroborating event lattices that were simply wrong — 44.5% false-install, shapetrans 19/19 false installed with recall 0%, timbredisc's contract changing literally nothing (0% disposition difference, 45.7% false-install). Provenance checks that the evidence *exists* and is *addressable* — the adversary's evidence exists too, neatly addressable. Corroboration across two fooled spans is two lies agreeing with each other.

**Rebuttals.** FOR: require the corroborating evidence to come from an *independent causal source* — different time *and* different modality — not just a second span of the same fooled measurement. AGAINST: that concedes the debate — the load-bearing part of the rescue is the *independence* (§11), not the provenance. Provenance alone, as frozen and tested, dies.

**Judge's ruling: P2 DIES as the install property; SURVIVES as the audit property.** Every installed memory must carry addressable evidence (source spans, witness refs) so it can be re-checked, contradicted, and revoked later — H1's ledger is worth inheriting. But addressability never *authorizes* installation. "I can point at where I saw it" is necessary for memory hygiene and insufficient for memory truth.

## §5. P3 — Executable testability ("every percept carries its own experiment")

**Team FOR (steelman):** This is the program's best safety datum: **zero false permanent installs in 10,000 trials** — the only fork with a clean KB4 record, against the strictest non-G3 bar (3%). Executability mechanizes falsification: each percept is a bounded program with explicit PASS/FAIL/UNRESOLVED outcomes, deterministic, ledger-bound, and UNRESOLVED is an honest third state instead of a forced label. The kill-2 death (38.9% self-flag vs 90%) tested *program self-calibration*, not the gate — and the gate withheld all 108 wrong high-confidence percepts anyway. The verdict itself says it: "If the bar had tested installed falsehoods, H2 would live." On the KB4 problem as stated — installed falsehoods — H2 is undefeated.

**Team AGAINST (steelman):** What saved H2 was rule 4 — the required successful prediction *outside the original source span* — not executability. The programs' own tests ran on the *same evidence* as the front-end, and kill-2 proves they confirmed the lies: only 38.9% of wrong high-confidence programs emitted FAIL/UNRESOLVED. Executability without evidence-independence is a fancy way to re-assert the front-end's mistake with extra steps and extra compute. The 0/10,000 record belongs to the out-of-span requirement (§11's property), not to the executable costume it wore.

**Rebuttals.** FOR: executability is what *makes* the out-of-span check expressible, bounded, and machine-checkable — the property is properly stated as "the percept carries executable falsification tests, **including at least one test on evidence disjoint from formation evidence**." The composite is the property; kill-2's fix is to require the out-of-span test in every program (drafted below as HC-4). AGAINST: accepted — but then judge the composite honestly: pure executability (tests on same evidence) dies by kill-2's lesson; what survives is executability *plus* evidence-independence.

**Judge's ruling: P3 SURVIVES-IN-COMPOSITE (P3 + P9).** The surviving formulation: *an executable warrant with at least one test on formation-independent evidence.* Pure executability — tests re-running the percept's own evidence — DIES; kill-2 is its epitaph.

## §6. P4 — Relational distinctiveness ("this is like a known truth, unlike known lies")

**Team FOR (steelman):** G3's *mechanism* passed every bar: B4 84% disposition change (12 vs 102 false installs without the gate), 97.0% retrieval correctness (745/768), B6 byte-identical determinism, and it beat baseline A head-to-head 98.6% vs 74.1% at lower cost (36 fixed bytes vs A's variable ~31; 8k–204k ops vs A's 8k–4.5M). The failure was localized and honest: the quantized features (4-bit harmonic bins, area/radius ratios, coarse displacement cells) were too coarse — attacks moved the class without moving the bins. That is a *front-end feature* failure, not a contract-property failure. Keep the contract, rebuild the features attack-aware, and distinctiveness stands.

**Team AGAINST (steelman):** "Exact-match on a lossy signature certifies collisions as memories" — and *every* signature is lossy; lossiness is what makes it a signature instead of the raw input. The adversary's optimal strategy is always to find collisions in the lossy space, and G3's own attack suite did exactly that: 2nd-harmonic boost ×1.15 changed timbre class without moving coarse bins (collision with enrolled PURE); an occlusion bar moved a CIRCLE's area/radius ratio into a TRIANGLE's signature (collision with the wrong exemplar); reversed videos block-matched to the wrong displacement. Distinctiveness against enrolled *true* exemplars only checks "is this like something known" — it never checks "is this a known lie." A property blind to the adversary's move is a wish, and 106/370 enrolled signatures already collided with each other before any attack.

**Rebuttals.** FOR: make the reference two-sided — install requires margin over the nearest true exemplar **and** margin over a frozen bank of known-false collision patterns; the false bank grows with every caught attack (deliberate learning from mistakes). The adversary must then beat two distances. AGAINST: margin-over-known-false is adversarial robustness (§10) bolted onto distinctiveness — judge it as the composite. And note the regress: who maintains the false bank, what stops the next uncovered collision, and the feature space itself needs rebuilding (a front-end project, not a contract property).

**Judge's ruling: P4 SURVIVES-IN-COMPOSITE (P4 + P8).** Reformulated: *two-sided distinctiveness — nearer to enrolled true exemplars than to a frozen bank of known-false patterns, by a margin, on attack-aware features.* As frozen (exact-match to knowns only), it DIES; G3's 4.36% is its epitaph.

## §7. P5 — Persistence-over-time ("a percept earns authority by surviving time")

**Team FOR (steelman):** Time is the one check the adversary cannot fake at a single instant. H3's mechanism defeated attacks aimed directly at it: 0/120 false installs on H3ADV, the suite designed specifically against H3's predictions. Broken-prediction quarantine is the only *active memory hygiene* in round 1 — memories that fail get downgraded, withdrawn, revoked, with negative evidence stored. No other fork retired bad memories; the rest only withheld. "A percept earns authority by surviving time" is principled, and the passage of sensory time is free evidence.

**Team AGAINST (steelman):** Two independent kills. First, H3's predictions checked the *same measurements* as the front-end — time added delay, not independence: the lie installed provisionally, confirmed itself against the same fooled measurements, and went durable (22.95% false-install vs 4%; the harness adversarial set fooled measurements at 37.8% while H3ADV scored 0). Second, the sticky quarantine confused "this counterfactual's predictions failed on an episode where it is false" — correct behavior — with "evidence against the claim": true claims were permanently banned (0% recall on colordisc and colorconst; shapetrans banned CIRCLE at episode 1), and KB4 regret ran +89% vs A on colorconst because withholding correct claims costs more than installing them. Persistence without independent measurements is slow self-confirmation; with sticky revocation it is amnesia.

**Rebuttals.** FOR: per-episode (non-sticky) quarantine plus predictions on *independent* measurements fixes both defects — the mechanism is sound, the frozen parameters were wrong. AGAINST: the other crew's post-freeze experiment is the counter-evidence: removing stickiness re-admitted the lies (their rerun traded the KB3 kill for KB1 35.2% and KB2 57.6% kills). The tension is structural — persistence gates trade false-installs against recall on the *same measurement axis*, and no quarantine schedule escapes it without independent evidence.

**Judge's ruling: P5 DIES as a standalone property.** Time is a dimension, not a witness. It survives only inside the P3+P9 composite: out-of-span tests *are* temporal, but what makes them work is evidence-independence, not the passage of time.

## §8. P6 — Cross-modal corroboration ("two senses agree")

**Team FOR (steelman):** The attacker must fool two independent sensors simultaneously — the hardest attack in any battery. Both H1 (rule 5) and H2 (rule 4) used cross-modal agreement as the gold-standard install condition. In nature it is the strongest everyday warrant: you hear *and* see the dog. As a strengthening condition it strictly raises the adversary's cost.

**Team AGAINST (steelman):** H1 *had* cross-modal corroboration in its contract and still died at 44.5% — the adversarial battery fooled both modalities together (the 30%-misleading set was audio-visual by design). Corroboration is not independence when the adversary controls both channels. Worse, many percepts are legitimately unimodal (a pure tone, a still photo) — a *required* property that cannot be checked half the time is not a contract, it is a sometimes-bonus. And when modalities disagree, which wins? The contract needs a tie-break rule — i.e., *another* property.

**Rebuttals.** FOR: corroboration was never anyone's sole property — it is a booster that raises the adversary's bar; keep it as a strengthening condition, never a gate. AGAINST: agreed, with the warning that "two fooled modalities agreeing" must be modeled as a correlated-failure case in the battery, not assumed away.

**Judge's ruling: P6 SURVIVES-IN-COMPOSITE as a booster only.** When two modalities independently support the claim, the provisional period shortens / install confidence rises; never required, never sufficient alone.

## §9. P7 — Deliberation-ratification ("TNN itself chooses to remember")

**Team FOR (steelman):** This is the program's core thesis — deliberate memory agency (MA1 58/58 checks; MA4 18/18 on the adversarial curriculum). A memory that bypasses deliberation is a reflex, not a memory. H1's rule 4 gave deliberation both sides of every conflict; H2's UNRESOLVED passed hypotheses to deliberation with unresolved predicates explicitly listed. The contract should check that TNN itself deliberately ratified the install, with alternatives visible and the choice audited. Ratification is also what makes the force-pin law and scaffold-and-release coherent: memories must be TNN's own commitments.

**Team AGAINST (steelman):** Deliberation is only as good as its evidence. H1 gave deliberation both sides of every conflict and deliberation still installed falsehoods at 44.5% — because the evidence it deliberated over was the fooled lattice. Ratification does not detect front-end error; it *launders* it through a fancier process. It adds a failure mode of its own: deliberation can be adversarially steered by which alternatives are framed and shown. As a KB4 property it is empty — a deliberate lie is still a lie.

**Rebuttals.** FOR: ratification's value is agency, commitment, and revocability — it keeps the "who decided" ledger clean. It is load-bearing for the architecture, just not for KB4. The honest statement: deliberation chooses *among verified candidates*; it does not verify. AGAINST: accepted — which is exactly why it cannot be *the* property the contract checks against adversarial install.

**Judge's ruling: P7 DIES as the KB4 property; SURVIVES as architectural mechanism.** The contract should *record* deliberation's ratification (audit trail, agency, force-pin coherence), but ratification must never be mistaken for verification.

## §10. P8 — Adversarial robustness as the property itself ("survives the attacker")

**Team FOR (steelman):** The KB4 problem *is* adversarial false-install; the only honest property is "survives the adversary." G3's 1% bar — the strictest in round 1 — produced the best mechanism. Micah's standing testing standard is "tests decide." A contract that checks "does this percept survive the frozen perturbation battery" directly measures what we care about, with no proxy and no pretense.

**Team AGAINST (steelman):** Circular and regressive. A perturbation battery is a *test suite*, not a percept property — it classifies the *check*, not the percept. The adversary adapts: round 1 needed fork-specific trap families to kill each fork; no single battery killed all six, so today's frozen battery is stale tomorrow. As a property it is "checks that it checks" — infinite regress: what adversarially validates the battery? Add cost (a full attack battery per install is prohibitive) and Goodhart (this program already learned that bars get gamed — the no-harmonics bar measured hiss, not quality, since real Mars wind scores 0% on it).

**Rebuttals.** FOR: freeze the battery per prereg, version it, grow it with every caught attack — the regress is managed the way science manages it: the test suite is the current best adversary, always provisional, never final. AGAINST: that is exactly the kill-bar *format* round 1 already used — it belongs at the evaluation layer, not inside the gate. Running the battery at install time also confuses the map (the frozen test) with the territory (the live adversary).

**Judge's ruling: P8 DIES as the checked property; SURVIVES as the measurement instrument.** Adversarial batteries are how we *falsify* candidate properties — the kill-bar format — not a property a gate checks at install time. P8 is the referee, not a player.

## §11. P9 — Evidence-independence ("the gate must see what the percept-maker didn't") — crew-added

**Team FOR (steelman):** It is the only candidate that explains all six deaths *and* both survivals. Deaths: H1 (witnesses = same regions), H3 (predictions = same measurements), G2 (residuals = same invariant space), G3 (signature = same quantized features), G1 (generators = same segmentation) — every gate re-read the percept's own evidence. Survivals: H2's rule 4 (prediction outside the source span — evidence the front-end had not seen) → 0/10,000; G3's mechanism wherever its features were adequate. It operationalizes concretely: the contract declares, per install, an evidence set E_gate disjoint from the percept's formation evidence E_percept (disjoint source spans, disjoint time windows, or disjoint modality), and the kill bar is *interventional* — paired fixtures where the front-end is fooled but E_gate is clean must withhold ≥90%. Disjointness of source spans is checkable in pure Zag today; H2's rule 4 already did it.

**Team AGAINST (steelman):** It is a design constraint on the *gate*, not a property of the *percept* — you cannot point at a percept and measure its "evidence-independence." It risks infinite regress: what gates the gate's evidence? Who watches the out-of-span evidence's own front-end? And "informational independence" needs a computable measure — conditional mutual information is not something a pure-Zag deterministic gate can evaluate per install. As stated it is a slogan, not a falsifiable hypothesis.

**Rebuttals.** FOR: the regress stops at the ledger — E_gate's formation is *audited* (P2's surviving role), not gated; audit is cheaper than gating and breaks the regress. The computable version is *declared disjointness plus interventional testing*: the prereg declares which evidence sets count as disjoint for each task, and the battery contains paired fooled-front-end/clean-gate fixtures. That is falsifiable with numbers. AGAINST: accepted as an admission criterion — but judge it as what it is: a *meta-property* (a law candidate gates must satisfy), not a competitor property.

**Judge's ruling: P9 SURVIVES as the design law (meta-property).** Every round-2 candidate must satisfy it; it is the admission criterion, not a contestant. Its concrete operationalization — declared disjoint evidence sets + interventional withhold-rate kill bar — is falsifiable.

## §12. Key clashes (what the debates actually turned on)

**Clash 1 — Is there any install-time property at all, or is all verification post-install?**
P5's team argued time itself is the check; the opposition showed H3's time-gate merely delayed self-confirmation (22.95% false-install) and then induced amnesia (0% recall). Resolution: install-time checks are possible — H2's gate proves it (0/10,000) — but only when the check's evidence is independent of formation evidence. Time without independence is delay, not verification.

**Clash 2 — Executability vs evidence-independence: who gets credit for H2's 0/10,000?**
The sharpest intra-crew fight. P3's team claims the executable program; the opposition claims rule 4 (out-of-span prediction). Both external judges split it the same way the crew did: SURVIVES-IN-COMPOSITE. The load-bearing element is the *conjunction* — a bounded executable test *run on disjoint evidence*. Neither half survives alone (kill-2 killed same-evidence executability at 38.9%).

**Clash 3 — Can distinctiveness survive lossiness?**
Every signature is lossy; the adversary lives in the lost bits (G3's harmonic-boost and occlusion collisions). P4's rescue — a two-sided reference with a frozen bank of known-false patterns — was accepted as a composite, but the opposition's regress stands unanswered: the false bank is always one attack behind. Both judges ruled P4 DIES as tested.

**Clash 4 — Is deliberation a check or a launderer?**
H1 gave deliberation both sides of every conflict; false installs stayed at 44.5%. Sol: "a system's decision to install is not evidence that the percept is true" (DIES). Grok-4.6 dissents: deliberation as an *untested meta-gate that can invoke independent checks* deserves composite status. The crew's synthesis: deliberation is the *dispatcher* of checks, never the check itself — it chooses among verified candidates.

**Clash 5 — The judges' joint correction: independence is not enough; the check must discriminate.**
Both external judges independently added what the crew's nine properties missed. Sol: independent evidence can still be wrong or share a confound — the check must make *competing interpretations predict different outcomes* (claim-discriminative grounding). Grok-4.6: the check must succeed on an *interventional* outcome, not a passive observational prediction (do-operator testability). The crew accepts the correction: P9 (evidence-independence) is necessary but not sufficient. The surviving standard is **independent + discriminative + interventional**.

## §13. Crew-added from external judges: P10 and P11

**P10 — Claim-discriminative grounding (Sol).** The contract's check must distinguish the installed claim from its strongest plausible alternative — competing interpretations must predict *different* outcomes under the check. Supporting evidence is cheap; discriminating evidence is the property. *Judge's ruling: SURVIVES — adopted as a required element of every round-2 candidate (see HC-5). It repairs P9's gap: disjoint evidence that doesn't discriminate is just independent irrelevance.*

**P11 — Interventionist testability (Grok-4.6).** The contract must succeed on an independent *interventional* outcome (do-operator), not merely a passive observational prediction. Observation can be confounded in ways intervention breaks. *Judge's ruling: SURVIVES-IN-COMPOSITE — adopted as the strongest form of the out-of-span check (see HC-6). Pure observation without intervention is the weaker, still-admissible form.*

## §14. Verbatim external opinions

### gpt-5.6-sol (UnoRouter, 2026-09-22)

The following is the complete verbatim response from gpt-5.6-sol:

> **(a) Verdicts**
>
> 1. **Predictability — DIES.** Small residuals and successful predictions can certify a consistently wrong interpretation.
> 2. **Witness-addressability/provenance — DIES.** Traceable, mutually corroborating evidence can still support a false claim.
> 3. **Executable testability — SURVIVES-IN-COMPOSITE.** It blocked all false permanent installs in 10,000 trials, but its tests rarely exposed wrong high-confidence percepts; it is a useful gate component, not a sufficient contract.
> 4. **Relational distinctiveness — DIES as tested.** Exact matching a lossy signature mistakes collisions for distinct memories.
> 5. **Persistence-over-time — DIES as tested.** Repeating the front end's measurements repeats its failure, while sticky quarantine can reject true claims.
> 6. **Cross-modal corroboration — SURVIVES-IN-COMPOSITE.** It can add independent evidence, but agreement across modalities is not decisive if their errors share a cause.
> 7. **Deliberation-ratification — DIES.** A system's decision to install is not evidence that the percept is true.
> 8. **Adversarial robustness as the property — SURVIVES-IN-COMPOSITE.** Robustness is the needed outcome, but as a contract property it is only meaningful against a specified, held-out attack distribution; no finite suite certifies general robustness.
> 9. **Evidence-independence — SURVIVES-IN-COMPOSITE.** Reusing the evidence that formed the percept makes confirmation circular. Independent evidence helps, but independent evidence can still be wrong.
>
> **(b) Missing property**
>
> **Claim-discriminative grounding:** evidence must distinguish the claim from plausible alternatives, not merely support it. Independent sources can share a confound; repeated observations can preserve the same ambiguity. The test needs to make competing interpretations predict different outcomes.
>
> **(c) Round 2 candidate**
>
> **Independent discriminative challenge contract:** Install a claim only if a preregistered challenge, selected to distinguish it from its strongest plausible alternative, succeeds using evidence not used to form or select the percept. The challenge must be generated through a different measurement path or a controlled intervention; a re-run of the front end does not count. Unresolved or non-discriminating challenges withhold installation.
>
> **Falsifiable kill bar:** On a frozen set of at least 10,000 adversarially misleading percepts and 2,000 true controls, require:
> - False permanent installs ≤1% overall and ≤2% in every attack family.
> - True-claim recall ≥80%.
> - At least 90% of wrong high-confidence percepts flagged or left unresolved by the challenge.
> - No attack family may pass by reusing, transforming, or selecting the original evidence.
>
> Fail any bar and kill the contract. The key test is whether the challenge actually separates wrong claims from nearby alternatives, not whether it looks independent or produces a clean confirmation.

### grok-4.6 (UnoRouter, 2026-09-22)

The following is the complete verbatim response from grok-4.6 (never "4.7"):

> (a) Verdicts:
> (1) predictability: DIES — G2 showed wrong-direction reversed videos still produced small residuals + hash matches; predictable ≠ correct.
> (2) witness-addressability/provenance: DIES — H1 adversarial fixtures generated high-support, zero-contradiction, mutually corroborating lattices that were simply false.
> (3) executable testability: SURVIVES-IN-COMPOSITE — H2 produced zero false permanent installs (withheld every one of 108 wrongs) via an outside-span prediction, but failed the 90% self-flag bar (only 38.9%).
> (4) relational distinctiveness: DIES — G3 exact-match on a lossy hashed signature certified collisions as installed memories.
> (5) persistence-over-time: DIES — H3 re-ran the identical front-end measurements, so attacks confirmed; sticky quarantine then produced 0% recall on true claims.
> (6) cross-modal corroboration: SURVIVES-IN-COMPOSITE — supplies a concrete source of evidence-independence that H1-style same-lattice corroboration lacked.
> (7) deliberation-ratification: SURVIVES-IN-COMPOSITE — untested meta-gate that can invoke independent checks before installation.
> (8) adversarial robustness as the property itself: DIES — that is the outcome metric (KB4), not a checkable property of any given percept.
> (9) evidence-independence: SURVIVES — every killed fork used evidence overlapping the percept-formation process (same measurements, same source span, lossy hash of the same bits); H2's outside-span requirement was the sole exception that achieved zero false-installs.
>
> (b) Missed property: interventionist (do-operator) testability — the contract must succeed on an independent interventional outcome, not merely an observational prediction.
>
> (c) Round-2 candidate (H4 Independent Interventional Program): INSTALL only if an executable program derived from the percept (i) produces a successful prediction on at least one held-out source whose raw measurements are informationally independent of percept formation (different sensor, later time, or different modality) and (ii) produces a clear FAIL (residual > 3σ or hash mismatch) on ≥3 adversarial perturbations of that same independent source. Kill bar (frozen, 10 k adversarial trials): false-install < 0.5 %, ≥95 % of high-confidence wrongs self-flag FAIL/UNRESOLVED, and true-install recall ≥70 % on two held-out tasks.

## §15. Final judged verdicts (crew + both external judges reconciled)

| # | Property | Crew | Sol | Grok-4.6 | Final |
|---|---|---|---|---|---|
| P1 | Predictability | DIES | DIES | DIES | **DIES** — unanimous. "Predictable ≠ right" is round 1's sharpest negative result. Retrieval bias only. |
| P2 | Witness-addressability / provenance | DIES as install property; SURVIVES as audit | DIES | DIES | **DIES as install property; SURVIVES as audit property.** Every memory carries addressable evidence for re-check/revocation; addressability never authorizes install. |
| P3 | Executable testability | SURVIVES-IN-COMPOSITE (P3+P9) | SURVIVES-IN-COMPOSITE | SURVIVES-IN-COMPOSITE | **SURVIVES-IN-COMPOSITE** — unanimous. Formulation: executable warrant with ≥1 test on formation-independent evidence. H2's 0/10,000 is the datum to beat. |
| P4 | Relational distinctiveness | SURVIVES-IN-COMPOSITE (P4+P8) | DIES as tested | DIES | **DIES as tested; SURVIVES-IN-COMPOSITE reformulated** (two-sided reference: true exemplars + frozen known-false bank, attack-aware features). The crew keeps the reformulation alive; both judges would re-kill it if the false-bank regress isn't answered. |
| P5 | Persistence-over-time | DIES standalone | DIES as tested | DIES | **DIES** — unanimous as standalone. Time is a dimension, not a witness. Lives only inside P3+P9 composites. |
| P6 | Cross-modal corroboration | SURVIVES-IN-COMPOSITE (booster) | SURVIVES-IN-COMPOSITE | SURVIVES-IN-COMPOSITE | **SURVIVES-IN-COMPOSITE** — unanimous. Booster only: never required, never sufficient. Correlated fooling must be in the battery. |
| P7 | Deliberation-ratification | DIES as KB4 property; SURVIVES as mechanism | DIES | SURVIVES-IN-COMPOSITE | **DIES as the KB4 property; SURVIVES as dispatcher/mechanism.** Sol's line stands ("a decision to install is not evidence of truth"); Grok's nuance is kept: deliberation may *invoke* independent checks, never *substitute* for them. |
| P8 | Adversarial robustness as property | DIES as property; SURVIVES as instrument | SURVIVES-IN-COMPOSITE | DIES | **DIES as the checked property; SURVIVES as the measurement instrument and named outcome.** Sol's qualifier is adopted: kill-bar batteries must be *held-out* from the fork's design — no finite suite certifies general robustness. |
| P9 | Evidence-independence | SURVIVES as design law | SURVIVES-IN-COMPOSITE | SURVIVES | **SURVIVES as the admission law.** Every round-2 candidate must declare disjoint gate evidence and pass an interventional withhold test. Corrected by both judges: necessary, not sufficient. |
| P10 | Claim-discriminative grounding (Sol) | — (adopted §13) | (proposed) | — | **SURVIVES.** The check must make competing interpretations predict different outcomes. Required element of HC-5. |
| P11 | Interventionist testability (Grok-4.6) | — (adopted §13) | — | (proposed) | **SURVIVES-IN-COMPOSITE.** Interventional outcome is the strongest form of the out-of-span check. Required element of HC-6. |

**Net survivors:** no standalone property survives except as a component. The round-2 contract is a composite: **executable warrant (P3) + formation-independent evidence (P9) + discriminative-vs-alternatives check (P10) + interventional form where available (P11)**, audited by addressable provenance (P2), boosted by cross-modal agreement (P6), dispatched by deliberation (P7), and falsified by held-out adversarial batteries (P8).

## §16. HYPOTHESIS CANDIDATES for round 2

Each is a concrete contract-property hypothesis with a sketched kill bar — falsifiable, measurable, prereg-ready. Bars are sketched; exact frozen numbers belong in the round-2 prereg.

**HC-1 — Executable out-of-span warrant (P3+P9).**
*Rule:* INSTALL only if a bounded deterministic test program derived from the percept PASSES every test, including ≥1 test executed on evidence disjoint from the percept's formation evidence (later time window, second occurrence, or different modality). FAIL or UNRESOLVED on the disjoint test → WITHHOLD. The program, its tests, and the disjoint evidence spans are ledger-bound.
*Sketched kill bar (frozen, ≥10,000 trials, ≥30% adversarial):* false permanent installs ≤2%; true-install recall ≥80%; ablate the disjoint-evidence requirement → false installs must rise by ≥5× (load-bearing proof); byte-identical reruns. Dies if the gate's safety comes from anything other than the disjoint test.

**HC-2 — Two-sided adversarially-distinctive signature (P4+P8).**
*Rule:* INSTALL only if the percept's relational signature is nearer to enrolled true exemplars than to a frozen bank of known-false collision patterns, by a preregistered margin, on attack-aware features. Nearer to (or within margin of) a known-false pattern → WITHHOLD. The false bank grows with every caught attack across rounds.
*Sketched kill bar:* false-install ≤1% under signature-targeted attacks (attacks designed to collide); retrieval accuracy ≥90%; every enrolled false pattern must withhold its own class (no self-collision installs). Dies if a novel collision class installs, or if answering the false-bank regress ("always one attack behind") fails measurably.

**HC-3 — Evidence-independence admission law (P9, interventional).**
*Rule (meta, applies to every round-2 gate):* the prereg must declare, per task, the evidence sets counting as disjoint from percept formation. The battery must contain paired fixtures: front-end fooled × gate-evidence clean. On those pairs the gate must WITHHOLD ≥90%.
*Sketched kill bar:* withhold rate on fooled-front-end/clean-gate pairs ≥90%; a gate that cannot name its disjoint evidence sets is rejected before evaluation. Dies if any candidate passes while its gate evidence overlaps formation evidence on the paired fixtures.

**HC-4 — Calibrated executable self-report (P3 rematch of H2's kill-2).**
*Rule:* rerun H2's kill-2 bar with programs required to contain ≥1 out-of-span test: ≥90% of wrong high-confidence percepts must reach FAIL or UNRESOLVED *by their own programs*.
*Sketched kill bar:* self-flag rate ≥90% on wrong high-confidence percepts (the exact bar that killed H2 at 38.9%); false permanent installs ≤3% on 10,000 trials; byte-identical reruns. Dies if executability still can't flag its own errors — which would kill P3 outright, composite included.

**HC-5 — Independent discriminative challenge contract (P9+P10; from Sol).**
*Rule:* INSTALL only if a preregistered challenge, selected to distinguish the claim from its strongest plausible alternative, succeeds using evidence not used to form or select the percept. The challenge must come from a different measurement path or a controlled intervention; re-running the front end does not count. UNRESOLVED or non-discriminating challenges → WITHHOLD.
*Sketched kill bar (frozen, ≥10,000 adversarial + ≥2,000 true controls):* false permanent installs ≤1% overall and ≤2% in every attack family; true-claim recall ≥80%; ≥90% of wrong high-confidence percepts flagged or left unresolved; no attack family may pass by reusing, transforming, or selecting the original evidence. Dies on any bar — and specifically dies if the challenge separates "looks independent" from "actually discriminates."

**HC-6 — Independent interventional program (P3+P9+P11; from Grok-4.6).**
*Rule:* INSTALL only if an executable program derived from the percept (i) predicts successfully on ≥1 held-out source whose raw measurements are informationally independent of percept formation (different sensor, later time, or different modality), AND (ii) produces a clear FAIL (residual > 3σ or hash mismatch) on ≥3 adversarial perturbations of that same independent source.
*Sketched kill bar (frozen, 10,000 adversarial trials):* false-install <0.5%; ≥95% of high-confidence wrongs self-flag FAIL/UNRESOLVED; true-install recall ≥70% on two held-out tasks. Dies if the interventional leg adds no measurable safety over HC-1's observational out-of-span check (ablation decides).

## Appendix — provenance and method notes

- **Debate format:** structured proposition/opposition rounds per property (§3–§11), rebuttals, judging pass, key-clash synthesis (§12), external judges (§14), reconciled verdicts (§15), candidates (§16). Run as explicit internal swarm teams: this crew is a depth-2 subagent and cannot spawn subagents, so parallel crews were replaced by recorded proposition/opposition rounds with a judging pass. No strawmen — each position's best case is stated before ruling.
- **Second opinions:** gpt-5.6-sol and grok-4.6 via UnoRouter (`custom.unorouter`), same prompt file (`.opinion_prompt.txt`), responses verbatim in §14. Prompt and raw responses are in `debates/` as dotfiles (`.opinion_prompt.txt`, `.opinion_sol_raw.txt`, `.opinion_grok_raw.txt`) for audit; the verbatim text in §14 is copied character-for-character.
- **ExperientialLabs:** checked live 2026-09-22 — gateway reachable, credits EMPTY (`insufficient_credits`, balance $-0.02). Not used; documented per task.
- **Laws observed:** no code was written in this debate (nothing to keep pure-Zag); zero RNG in any decision path (deterministic judging from frozen verdict numbers); max-risk posture N/A (no destructive actions taken); plain language throughout for Micah.
- **What this debate does not claim:** it does not re-derive round-1 results (frozen verdicts are taken as given); it does not preregister round 2 (kill bars above are sketches — freezing them needs the round-2 prereg process); human-oracle bars (B7s) remain pending Micah where noted in the frozen verdicts.
