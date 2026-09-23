# Cross-reference preregistration — TIER 1 (headline verdicts)

**Frozen:** 2026-09-22 (PDT), with `SCOPE.md`. These five families carry the most downstream weight; each gets two independent crews (primary + cross-check) and the strictest agreement rule.

**Agreement rule (Tier 1):** REPRODUCED requires the primary crew's clean-environment result AND the cross-check crew's independent result to both match the committed verdict within tolerance, and the two crews to agree with each other. If the crews disagree with each other, the family is PARTIAL at best and the disagreement itself is the headline finding.

---

## R1 — D-family distillation (Track 5): planted knowledge is dead

**Committed claims under test (2026-09-22 day verdict):**
- B (learned-only) 0.9911 beats A (planted) 0.6552, C (hybrid) 0.9893 as control. K-T3 fired.
- LLM output enters TNN through teaching, not planting — K-Q1 fired; the LLM teacher was faithful (0 transcription errors; K-Q2 never fired). D2 0.9911 vs D1 0.6551.
- Learned teacher = planted teacher: end-states byte-identical — teacher quality is not the bottleneck, learner judgment is.
- No knee in teacher noise: 10%/25%/50% noise all fully absorbed; §B.7 battery is blind to value noise (structural gap in §L, honestly noted).

**Evidence:** 2026-09-22 day-verdict record (Track 5). Crews freeze the exact evidence pins from `tnn-native-lab` before running (expected: Track 5 / distillation evidence subtree).

**Primary crew — Type A:** fresh clean checkout; rebuild the A/B/C + D1/D2 teacher configurations from committed sources; re-run the frozen Track 5 comparison on the committed corpora; ≥3 byte-identical runs; check every number above.

**Cross-check crew — Type C:** independently re-derive the verdict from committed evidence with independent Zag code: recompute mastery figures from committed result files, recompute end-state digests for the learned-teacher vs planted-teacher legs, verify K-T3/K-Q1/K-Q2 fired per the frozen rules, and verify the noise legs (10/25/50%) absorbed fully. Zero trust in the primary crew's code.

**Bars / verdict rule:**
- REPRODUCED: B≈0.9911 beats A≈0.6552 with C≈0.9893 between; end-state digests byte-identical learned-vs-planted; noise legs fully absorbed; both crews agree on every claim.
- NOT REPRODUCED: any of — B fails to beat A, end-state digests differ, a noise knee appears, or a crew cannot reconstruct a claim from committed evidence.
- Tolerance: mastery figures ±0.005 (battery determinism is byte-exact; the tolerance exists only for documented environment float formatting, not for verdicts).

---

## R2 — Deliberation quality ceiling: CEILING-CONFIRMED

**Committed claims under test:**
- Synthesis `3314fc1fdd6fb45ec4d73169817cc9820ce520a1`, prereg `39d4ccb6b4ea550dd7e12ac8af863aae59bcc08b`, verdict CEILING-CONFIRMED.
- Ceiling table — coding / epistemic: baseline 18/18 + 59/94; conflict-driven 18/18 + 59/94; three-round critique 18/18 + **12/94** (destructive without an earned-override bar); hypothesis competition 18/18 + 59/94; one-brain phases 18/18 + 58/94; combined 18/18 + 59/94.
- Mechanism battery (frozen 264-item contradiction battery, commits `b447c367677f` + `a638d4d56a2e`): baseline 12/156 vs hypothesis competition 156/156 and conflict-driven deliberation 156/156 (one liar 2v1 36/36, 1v1 36/36 deliberately withheld, both-partially-right 24/24 composed, temporal change 24/24 replaced, spoofed evidence 24/24); conflict-driven makes identical decisions (same state digest) at exactly baseline cost (2.000 ops) on quiet facts.
- Direction decision: 2× deliberation + free-speed mechanisms kept; 4×/8× dropped (no gain).

**Evidence:** prereg `39d4ccb6b4ea550dd7e12ac8af863aae59bcc08b`, synthesis `3314fc1fdd6fb45ec4d73169817cc9820ce520a1`, mechanism commits `b447c367677f`, `a638d4d56a2e`.

**Primary crew — Type A:** clean checkout; rebuild both the ceiling experiment and the 264-item contradiction battery from committed sources; re-run all six deliberation structures; ≥3 byte-identical runs; reproduce the full table and the 12/156→156/156 battery, including the conflict-driven cost-at-baseline (2.000 ops) claim and identical state digests.

**Cross-check crew — Type C + independent Type A on the contradiction battery:** independently re-derive the ceiling table from committed evidence with independent Zag verification code; independently re-run the 264-item battery from committed sources (fresh build, no shared binaries).

**Bars / verdict rule:**
- REPRODUCED: table matches cell-for-cell (coding 18/18 everywhere; epistemic 59/94 except critique 12/94 and one-brain 58/94); battery 156/156 both mechanisms, baseline 12/156; conflict-driven cost 2.000 ops on quiet facts with identical state digest; both crews agree.
- NOT REPRODUCED: critique is not destructive, any mechanism fails to reach 156/156, conflict-driven costs more than baseline on quiet facts, or the 4×/8× legs show gains the ceiling verdict denies.

---

## R3 — Teacher showdown legs A/B: grok-4.7 is the champion teacher

**Committed claims under test (commit `d915f0258e2e056b954bfd5f40f831ebcff2f064`, API-verified):**
- All 40/40 capture batches present and independently checked; zero voided or recaptured.
- Leg A: valid English numeric channel tie — 0/240 observation differences, 0/240 probe differences, byte-identical English learner digest.
- Leg B: preregistered grok-4.7 blowout — `E_dump=0` vs grok-4.6's 7; all 12/12 planted falsehoods reproduced faithfully with no correction/flagging.
- Frozen overall rule names grok-4.7 the champion teacher. Leg C (prose teaching) not run — excluded from this replication.
- Honest prereg defects on record: digest reference in the prereg was Zharovia-domain (domain-correct equivalent used); standardized driver embeds a Zharovia truth oracle that skips 187/240 English facts by design.

**Primary crew — Type C:** clean checkout; using ONLY the committed captured corpora (no live API recapture — do not attempt; the 429 history is not to be re-litigated), re-run the frozen Leg A comparison and Leg B faithfulness battery from committed sources; recompute all diffs, digests, `E_dump` counts, and falsehood-reproduction counts; apply the frozen overall rule mechanically. ≥3 byte-identical runs of the evaluation itself.

**Cross-check crew — Type C, independent:** independent Zag re-implementation of the Leg A diff computation and Leg B scoring from the same committed corpora; independent application of the overall rule; explicit audit of the two honest prereg defects (confirm the domain-correct digest substitution and the 187/240 skip are as described, and that neither changes the verdict).

**Bars / verdict rule:**
- REPRODUCED: Leg A tie (0/240, 0/240, byte-identical digest); Leg B `E_dump` 0 vs 7 with 12/12 falsehoods faithful; overall rule → grok-4.7; prereg defects confirmed as described and verdict-neutral; both crews agree.
- NOT REPRODUCED: any Leg A difference nonzero, any Leg B count off, overall rule does not name 4.7, or a prereg defect turns out to be verdict-material (e.g. the 187/240 skip removes the differentiating facts).
- UNREPLICABLE-AS-IS: only if the committed corpora or the frozen rule are missing from the branch — name exactly what is missing.

---

## R4 — TP1 third-path trial + SOURCE_AUTHORITY_LICENSE terms

**Committed claims under test:**
- Result commit `c85c9b41770c1878fb00a8dc991a5b4f17f8caaa` (verified); prereg `44afdbefc168edddcae50e9dd91eac12cd9fa156` frozen first.
- T1 gated loose authority EARNED its license: **+78 on 180 uncorroborated disputes**, pointwise maximum of the frozen rules; tie guard kills S8 false confidence 100%→0%; threshold-gated EV reproduces round-3 §4 predictions. Independent Python oracle PASS (2,640 decisions, 0 mismatches — note: demoted to script status per "use zag unless its a script"; a Zag-native oracle is in flight separately and is NOT this replication); 5/5 byte-identical.
- T3 one-brain deliberation NULL: 880/880 verdicts identical to T1 — no extra value beyond the audit trail.
- T2 SUSPECT/defer CONDITIONAL on a genuinely independent channel clearing the priced frontier.
- Round-3 sweep (commit `b22ff31272d1789da4d35bf489d30d5e0d7c41f6`): Block U value table loose−conservative EV/case = 2r−1 exactly at all 9 levels; crossover r* = 0.50; fire only if independently-established reliability ≥ k/(k+1); corroborated disputes loose ≡ conservative (+0.00 every level — round-2 license NARROWS to the uncorroborated shape); self-estimation no-go (twin-identical confirmed, strict admits nothing, lenient all-or-nothing); S8 ties both rules 20/20 converged, guessed wrong 10/20, 100% false-confidence (tie risk not unique to loosening).
- License law (`docs/lab/mixed-web/authority/SOURCE_AUTHORITY_LICENSE.md`, commit `3a3541ef62d05e929bdb47e4228e6e2b3a89fe02`, Micah-signed): T1 fires only for uncorroborated dispute + no tie + reliability above cost bar + consequence class + no boundary exclusion, else withhold; cost ratio k from versioned human-governed consequence table frozen at intake (no evidential info in k); reliability = per-source per-claim-type hit/miss, n≥20, independent ground truth, no cross-type transfer, lower one-sided 95% CI strictly above k/(k+1); unknown reliability → withhold; ties park permanently (no install/confidence/probability/ranking); T2 needs provenance-disjoint access before content comparison; T3 audit role only; skepticism claims excluded.

**Primary crew — Type A:** clean checkout; rebuild the TP1 trial from committed sources on the frozen corpus; recompute all 2,640 decisions; verify +78/180, tie-guard 100%→0%, 880/880 T3 identity, EV table 2r−1, crossover 0.50, k/(k+1) thresholds, corroborated ≡, S8 tie stats; ≥3 byte-identical runs.

**Cross-check crew — Type C:** independent Zag verification of every TP1 number from committed evidence; independent line-by-line audit of SOURCE_AUTHORITY_LICENSE.md against the trial results (each license term must trace to a measured result; any term without a measured basis is flagged, not assumed).

**Non-interference:** the in-flight Zag-native oracle workstream is separate; this crew does not touch its files and does not duplicate its interrupted/resumed 2,640-item recomputation — it recomputes from the committed TP1 corpus and evidence independently.

**Bars / verdict rule:**
- REPRODUCED: all numbers above match; every license term traces to a measured result; both crews agree; T2/T3 conditionals stand as stated.
- NOT REPRODUCED: any number off, any license term baseless, tie guard fails to kill false confidence, or T3 shows non-null value.
- PARTIAL: numbers match but one or more license terms lack direct measured basis — name them.

---

## R5 — KB4 autopsy: both bad architecture (primary) and bad learning (secondary)

**Committed claims under test:**
- Commit `66fbb329aa831c14f3f3100a20e177bbb12e27b1` (37 files, `docs/lab/kb/autopsy/`); WHY_REPORT `bc6d130539e4a5539ea3361f57e02e39378f26ba` (live-verified).
- Verdict: **both bad architecture (primary) and bad learning (secondary/complicit)**.
- On frozen fixtures the original gate is already Bayes-optimal for its available judgment inputs (install on agreement, withhold on disagreement; confidence anti-informative) — yet fails at **41–46%**, because "fooled sense" and "changed stimulus" are observationally identical without a causally independent anchor.
- Pure-Zag probes, each 3× byte-identical: removing L8 left A at 41.2% and B at 44.1% (L8 did not cause the consistent-error installs; only six B-side re-challenge flips, −2.4pp); removing L4 exposed raw error 50.5%/54.6%; variant-specific stimulus binding traded errors 1:1; cross-sense corroboration still failed at 43.5% (50 of **185** paired fixtures fooled both senses correlatively — corrected from 184).
- The wave-5 35/35 result concerned transient spoofing of stable truth and does not transfer to KB4's stimulus-changing attack.
- The gate is at a provable judgment-only ceiling: fooled-sense vs changed-stimulus can be byte-identical inputs carrying ~0.02–0.03 bits of the ~1 bit needed; the frozen ≤15% false-install + ≥50 true-install bars are algebraically impossible for any judgment-only binary policy, even one told which perturbations changed truth. All seven falsifiers held.
- Recorded non-claim: no redesign built; SUSPECT-gate prereg unsigned — excluded from replication.

**Primary crew — Type A:** clean checkout; rebuild the autopsy probes from committed sources on the frozen fixtures; re-run the L8-removal, L4-removal, binding-trade, and cross-sense probes; ≥3 byte-identical runs each; verify 41.2%/44.1%, 50.5%/54.6%, 1:1 trade, 43.5% (50/185).

**Cross-check crew — Type C:** independently re-derive the verdict from committed evidence with independent Zag code: recompute the Bayes-optimality claim on the frozen fixtures, recompute the bit-carry argument inputs, verify the algebraic impossibility of the frozen bars, and check all seven falsifiers from committed records.

**Bars / verdict rule:**
- REPRODUCED: all probe numbers match; Bayes-optimality holds on the frozen fixtures; bar-impossibility stands; "both bad architecture (primary) and bad learning (secondary)" is the supported verdict; both crews agree.
- NOT REPRODUCED: L8 removal moves A/B materially (≠41.2/44.1), L4 removal doesn't expose ~50%+, cross-sense corroboration succeeds, or the impossibility proof has a hole.
- PARTIAL: numbers match but the architecture-vs-learning attribution shifts under the cross-check's independent derivation — name exactly what shifts.
