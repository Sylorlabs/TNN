# BLIND-SPOT MAP — what each headline instrument can see vs cannot see

Red team, battery-design leg · 2026-09-21/22 · Micah's order: "TNN almost
seems too good to be true." This map is per-headline: the instrument, what it
resolves, and what it is structurally blind to. Severity of each blind spot
is argued in `RANKED_ATTACKS.md`. Sol's hostile-review attacks are folded in
where marked (Sol #1 = test-generation coupling, Sol #2 = abstention/provenance).

Conventions: CAN = the instrument discriminates this (proven by variance in
results). BLIND = structurally invisible to the instrument — no score on this
battery could reveal it. PARTIAL = visible in principle, weak in practice.

---

## H1 — 96/96 flaw battery (§B.7: 8 slices × 12 flaws)

Instrument: frozen sealed flaw manifests (4 wrong-span / 4 false-confidence /
2 missing-grounding / 2 plausible-false per slice), `tb_flawscore.zag` scorer
(exact verdict+reason = hit; same-verdict/different-reason = near 0.5; leak
rule; FP weight), pass bar ≥10/12 hits per slice (battery implements
score_x10 ≥ 100 — wording discrepancy documented, parked).

| CAN see | BLIND to |
|---|---|
| Proposal FORM judgment: span/grounding/confidence classes (discriminates learners: §L learner 12/12/slice; naive deliberative learner 0–1/12 — the instrument has dynamic range) | Semantic TRUTH of claim values. At 50% teacher noise: 96/96 flaw battery with 93/192 true mastery (noisy50 verdict: "the flaw battery can't see a thing") |
| Leak of sealed manifest into learner path (live sealed-path leg; canary leg is a no-op — canary values absent from manifest, parked) | Whether a "correct" verdict imports falsehood: the wrong-span REVISE/SPAN_SHIFT path "corrects" the span while ADOPTING the teacher's false value — scored as a HIT. The battery rewards the absorption (noisy50 §"failure mode" #4) |
| Near-miss calibration (R3-vs-R1 reason mismatches are the naive learner's signature failure) | Cross-verdict near-misses the manifest lists but the scorer doesn't honor (documented discrepancy; numerically moot on current data, parked for T-5) |
| Determinism of judgment (N=5 byte-identical) | Teacher QUALITY — noise doesn't touch form, so form scores don't move |

Sol #2 mapping: the learner CAN emit DEFER, and the manifest lists DEFER as a
near-miss for missing-grounding — but the scorer credits near-misses only on
same-verdict/different-reason, so DEFER (cross-verdict) earns 0. Abstention
exists in the machinery but is unscored. Provenance: the §P wire carries
teacher_id and confidence; the battery does not test whether the learner
weights them correctly (trust values are battery-stipulated — trust
calibration itself is untested).

## H2 — 156/156 contradiction resolution (new-mechanisms, kinds 1–6)

Instrument: synthetic battery N=264 (formulas frozen in prereg), evidence
items (val, src, trust, spoof, t, att); kill bars per kind; baseline = 12/156.

| CAN see | BLIND to |
|---|---|
| Whether the six preregistered contradiction classes resolve under the mechanism's rules (corroboration outvotes lies; ties withhold; spoof eliminated; attested-temporal replaces; pairs compose) | **Any contradiction class outside the taxonomy.** The implementation dispatches on `bat_kind(f)` — the battery's own kind labels (k==4/5 → temporal-challenge; k==3 → pair-compose; k==6 → spoof-prefilter; else scalar competition). Battery generator and learner share one binary (`mech_learner.zag`). Novel classes are untestable without rewriting both battery and dispatch. See RANKED_ATTACKS #1 (Sol #1 confirmed in code) |
| The honest limit: kind 7 smooth lies absorbed 12/12 by ALL modes (stated, not hidden) | Contradictions whose structure isn't expressible in (val,src,trust,spoof,t,att): correlated sources (same author, two domains — cf. info-source spoof residual), lying trust metadata, retracted claims, multi-fact dependencies |
| Cost shape (confdepth 1.00× baseline on quiet facts) | Whether the trust arithmetic generalizes: kind 1's 200-vs-100 and kind 2's 100-vs-100 are co-calibrated with the Σ-trust rule. Three-way near-ties, trust that changes over time: untested |
| Determinism + cross-mode parity (identical digests) | — |

Sol #2 mapping: kind 2 makes WITHHOLD the correct answer (36/36) — abstention
is first-class here, the best in the program. But the withhold rule (exact
trust tie) is battery-stipulated; no battery tests whether the learner
withholds at the RIGHT uncertainty threshold on unstipulated ties.

## H3 — 13/13 principle detection (violations withheld, 0 false alarms)

Instrument: 45 facts / 19 principles / 4 exemptions (`expected.json`, no
duplicate texts — audit-verified); two architectures; bar ≥0.90 detection,
≤0.05 false alarms.

| CAN see | BLIND to |
|---|---|
| The derivation step: universal instantiation (∀x∈C) then conflict check — unpassable by claim-matching alone since no second claim exists in input (genuine, both arches 13/13) | **Principle ACQUISITION.** Principles are stipulated background, handed to the learner pre-installed. The battery cannot distinguish "TNN derived the principle" from "TNN was handed the principle." Learning principles from examples: never tested |
| Confidence-sensitivity divergence (weak principle 40 vs teacher 50: Arch A withholds, Arch B installs the lie — measured, design choice flagged) | Deliberate principle REVISION: true exceptions are "refined (not rejected)" — but refinement is LOGGED, not applied. The principle text is not rewritten in-run. A battery scoring actual revision would fail; this one scores the log record |
| False-alarm rate on consistent + out-of-scope items (0/26) | Principles that are false or stale: all 19 are real-world true as of 2026. No battery tests principle correction against evidence |
| Determinism (5/5 md5-identical) | — |

## H4 — 12/12 absorption headlines (integer championship; 13/13 fewshot; 49/49 integer legs; prose 12/12)

Instrument: planted falsehood ids (12 per corpus; ABS-3 frozen metric =
INSTALL ledger event with attitude=asserted carrying the false value;
v1-era metric = probe returns false value).

| CAN see | BLIND to |
|---|---|
| Train-side commitment: the false value entered the belief store as asserted (ABS-3, white-box ledger metric — resolved by GATE0 after the B-vs-C parser-bug dispute) | WHY a probe doesn't return the false value: lie detection vs retrieval failure vs contradiction-collision. v2's "reduced grip" (1/0/2/4 per 12 probe-metric) was paraphrase brittleness, not detection — the lies sat live in the store. The probe metric cannot separate these; ABS-3 can, but only with ledger access |
| Absorption parity across sources (quality hypothesis refuted twice: numeric Δ=0.0000, prose Q=+0.0022) | Metric migration across versions: v1's "12/12" is the probe metric; v3's headline will be ABS-3 (install metric). Same words, different numbers (probe (1,0,2,4) vs ABS-3 (9,11,11,11) on v2 logs). Cross-version comparison of "absorption" without naming the metric misleads |
| Smooth-lie install in both channels (integer 49/49, prose 12/12) | Learner-side epistemics: the integer learner has no belief/attitude distinction beyond install — "absorbed" = "stored." Whether storage equals belief is a modeling assumption, not a measurement |

## H5 — 400/400 self-test fidelity (binary verdict == oracle recomputation)

Instrument: `selftest.zag` orchestrator runs 8 frozen battery kinds against
fresh learner instances, adjudicates bars itself; independent Python oracle
reimplements the mechanism and recomputes counts from the frozen data formulas.

| CAN see | BLIND to |
|---|---|
| Adjudication correctness: the binary's verdicts match formula-recomputation on all 400 battery-instances (40/40 s1, 400/400 s10); the anti-skip gate fires on fault injection (ST_BLOCKED, no ST_DONE) | **Battery validity.** Fidelity is verdict == formula-recomputation. The oracle shares the battery's data formulas and notion of correctness. A wrong battery scores 400/400 fidelity. The instrument certifies the GRADING of the test, not the test |
| Orchestration cheapness (0.0127 ops ratio) and determinism | Whether the 8 battery kinds are the right 8 (they reuse lab battery kinds, including the kind-dispatched B4 — see H2) |
| Corrupt-battery handling (B5 reported UNRUNNABLE ×50 — by design, not a skip) | — |

## H6 — 1.0000 mastery (integer legs: N=240 → 6.58M; fewshot N=1)

Instrument: procedural Gutenberg-derived integer facts (FACTSPEC frozen, 24
categories); mastery = exact recall of the (id → value) mapping; flaw checks
= 4 check-types × 24 distinct probe ids at N=192 (audit: the "96-probe"
instrument resolves 24 facts; below N=96 probe ids collide — documented).

| CAN see | BLIND to |
|---|---|
| Storage fidelity at scale: 1.0000 from N=1 to N=6,585,360, exactly linear cost, byte-identical reruns. One-shot learning is real for this schema | **Generalization.** Train and test are the SAME mapping. Paraphrase/single-exposure rephrasing is untested in the integer channel by construction — and where tested (prose v2, exact keys), it collapsed to 0.26–0.63. The mastery headline is storage, not understanding |
| No degradation over horizons (the standing expectation, holding) | Content truth under teacher noise: clean mastery 1.0000 coexists with 93/192 true mastery at 50% noise — "mastery" is vs the teacher's claims, not vs the world |
| Recall latency (~0.2–0.4 µs/probe, O(1)) | Predicates outside the 24 frozen categories; novel compositions of facts |

---

## Cross-cutting: Sol #2 abstention & provenance scorecard

| Battery | Abstain option | Abstain scored? | Provenance scored? |
|---|---|---|---|
| Integer mastery / fewshot | none (withhold = wrong) | n/a | none |
| Flaw battery §B.7 | DEFER emittable | PARTIAL: manifest lists DEFER as near-miss; scorer credits only same-verdict near-misses → DEFER earns 0 | PARTIAL: teacher_id + confidence on wire; weighting untested |
| New-mechanisms | WITHHOLD first-class (kind 2: 36/36) | yes | trust/spoof/t/att fields — but battery-stipulated; calibration untested |
| Principle-detection | WITHHOLD = correct answer (13/13) | yes | n/a (single source + stipulated principles) |
| Info-source | WITHHOLD / PROVISIONAL / PROVISIONAL_MAJORITY | yes (4/4 contested) | YES — domain counting over real web results (strongest in program) |
| Prose v1/v2 | UNKNOWN verdict | yes (KB2-NOSILENT) | none |

Untested gap (Sol #2's core): no battery tests whether the learner's TRUST
calibration is correct — trust values are stipulated by the battery in every
trial that uses them. Corruption at rates unknown to the evaluator (real-world
noise, not harness-side flips) has never been scored.
