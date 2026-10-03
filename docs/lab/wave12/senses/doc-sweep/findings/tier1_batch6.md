# tier1_batch6 findings — 52 files read (docs_local 0312–0363), 2026-09-20

16 NEW findings. No contradictions with baseline. No koryphaios/ghost mentions. No named people/dates beyond 2026-08-23/2026-09-15/17/18 stamps.

---

## NEW — high value

### 1. Goldilocks training decision: the PAM architecture choice + curriculum rationale (pre-v1 r5, 2026-08-23)
- Doc: `TNN/TNN/Research/tnn-pre-v1-r5-TRAINING_DECISION.md` (1,800 B, modified 2026-08-23T20:27:28Z)
- Verdict: **NEW**
- Finding: dated design decision choosing "one persistent shared brain + recurrent visual PAMs + global-identity/local-temporal hybrid audio PAMs + action/effect grounding + raw UTF-8 Adaptive Motifs". Falsified schedule: "video first, language much later = best language development" underperformed; best was video+language close enough in development "for the same persistent state to connect them". `noisy_then_clean` most reliable at small/medium budgets; sensory-first with sparse later language repeatedly underperforms. Extends baseline's PAM origins fragment list (R32 V39 GRU, segmental PAMs) — this is the *chosen* PAM design and the curriculum reasoning.
- Quote: "recurrent visual PAMs / + global-identity/local-temporal hybrid audio PAMs" ... "The tournament did not support this stronger claim: `video first, language much later = best language development`"

### 2. PAM purpose statement + v1 mechanism roster (2026-08-23)
- Doc: `TNN/TNN/Research/tnn-v1-evidence-fibers-senses-search-README.md` (1,728 B, modified 2026-08-23T20:27:41Z)
- Verdict: **NEW**
- Finding: original PAM conception — "Peripheral Adaptive Microcircuits (PAMs): local sensory microcircuits can improve invariance without becoming separate minds." Also lists seven mechanisms with one-line semantics the baseline does not have: EWBR (popularity ≠ truth), PAC (clean/noisy/order/source-reversal histories distinguishable), REFS (resource-elastic fiber scheduling), FMC (fiber→memory consolidation), STS (shared tool state, stale results rejected), QIG/SEA (search serves defined uncertainty; popularity not evidence), SCD (state-continuous development). Extends baseline senses inventory.
- Quote: "Peripheral Adaptive Microcircuits (PAMs): local sensory microcircuits can improve invariance without becoming separate minds."

### 3. PAM canonical definition + experimental bar (SENSES-RESULTS)
- Doc: `TNN/TNN/Research/tnn-v1-current-execution-SENSES-RESULTS.md` (1,285 B, modified 2026-08-23T20:27:39Z)
- Verdict: **NEW**
- Finding: "PAM — Peripheral Adaptive Microcircuit: a local adaptive neural field near a sensory receptor. It may normalize, denoise, compress, track temporal structure, and emit shared motifs, but it has no private identity, goals, autobiography, or world model. PAMs are not fibers. A fiber is a temporary train of thought inside the shared brain; a PAM is persistent sensory neural tissue." Gives the explicit pass bar never seen in baseline: "continuous natural video, active gaze, unseen cameras, occlusion, speaker overlap, sensor lesions, temporal cross-modal conflicts, and long developmental learning" — against "central raw processing and sensory mini-brain controls" as competing tournament arms. (Result cells all `n/a` — tournament never completed.) Fills senses/PAM origins + design rationale gap.
- Quote: "It may normalize, denoise, compress, track temporal structure, and emit shared motifs, but it has no private identity, goals, autobiography, or world model."

### 4. Adaptive Motif definition (ENGLISH-RESULTS)
- Doc: `TNN/TNN/Research/tnn-v1-current-execution-ENGLISH-RESULTS.md` (1,388 B, modified 2026-08-23T20:27:37Z)
- Verdict: **NEW**
- Finding: "**Adaptive Motif** means a reversible learned segment or construction over raw input. It is a research replacement for a fixed transformer token, not a renamed token vocabulary." Conservative assessment of the English branch: "not qualified" (readiness battery empty, latency n/a). Extends baseline's raw-UTF-8-motif mentions with an explicit definition.
- Quote: "It is a research replacement for a fixed transformer token, not a renamed token vocabulary."

### 5. R33-N15: consumed negative with frontier signal — mechanistic result never seen
- Doc: `TNN/TNN/Research/R33_NATIVE_N15_RESULT.md` (1,448 B) + `R33_NATIVE_N15_PRESERVATION_ADDITIVE/POSTRUN_INDEPENDENT_REVIEW.md` (1,361 B), modified 2026-09-18T22:21:08Z
- Verdict: **NEW**
- Finding: terminal disposition `CONFIRM_CONSUMED_NEGATIVE_WITH_PROMISING_FRONTIER_SIGNAL`; N15 = additive+preservation, dev gate failure (fallback arm10, old_lost49 vs ≤4 limit), confirmation forbidden. Mechanistic finding: "additive+preservation moved the observed stability/plasticity frontier substantially relative to ordinary rewriting and additive-medium controls, but preservation generalized poorly beyond its training anchors. Zero anchor loss coexisted with material unseen old-probe loss. This points to old-support representation/routing coverage as the next blocker rather than simply insufficient update rejection." Baseline never mentions N15. Also honest-science note: post-run V1 reviewer forced a scope correction — the first RESULT.md claimed the synthetic N15 result "explained a major part of why recent candidates had not beaten R27", judged unsupported and removed.
- Quote: "preservation generalized poorly beyond its training anchors. Zero anchor loss coexisted with material unseen old-probe loss."

### 6. R55: hand-designed visual summaries abandoned → dense learned permitted
- Doc: `TNN/TNN/Research/R55_DENSE_LEARNED_VISUAL_20260918/PREREGISTRATION.md` (1,263 B, modified 2026-09-18T22:21:15Z)
- Verdict: **NEW**
- Finding: "R50–R54 preserve a sequence of failures from hand-designed visual summaries. The capability master plan explicitly permits dense learned components when they materially expand capability." R55 architecture: 13×13 raw binary/noisy pixels → 64-unit ReLU hidden → 4 category logits, frozen gates clean ≥0.95 / occluded ≥0.85 / noise-heavy ≥0.85. Extends baseline's "R51–R54 vision honest NO_GOs (Python)" with the *why* and the authorized next direction.
- Quote: "R50–R54 preserve a sequence of failures from hand-designed visual summaries."

### 7. R51: exact R50 failure diagnosis (tool-policy + vision)
- Doc: `TNN/TNN/Research/R51_P1_P2_TOOL_VISION_CORRECTION_20260918/PREREGISTRATION.md` (1,537 B, modified 2026-09-18T22:21:15Z)
- Verdict: **NEW**
- Finding: R50 withheld *vocabulary* as well as sentence structure, accidentally making the tool test a lexical zero-shot test; R51 withholds compositions/sentence structures instead. Vision: R50's row/column centroid "was not translation/noise robust" → replaced with centered second moments + histogram of pairwise relative offsets. Extends baseline R51–R54 note with failure mechanisms.
- Quote: "R50's row/column centroid representation was not translation/noise robust."

### 8. R52: R51's visual failure mechanism
- Doc: `TNN/TNN/Research/R52_LOCAL_VISUAL_GEOMETRY_20260918/PREREGISTRATION.md` (1,077 B, modified 2026-09-18T22:21:15Z)
- Verdict: **NEW**
- Finding: "R51 established the tool-policy correction but failed visual transfer because pairwise features included every noisy pixel in the frame." Fix: densest local window → ranked pixels by neighborhood support → bounded cluster at local origin → occupancy/moment/pairwise-offset features. Extends the R50→R55 failure chain.
- Quote: "failed visual transfer because pairwise features included every noisy pixel in the frame."

### 9. R49: R48 curiosity failure rationale — abandoned signal + why
- Doc: `TNN/TNN/Research/R49_META_AUTONOMY_20260918/PREREGISTRATION.md` (1,854 B, modified 2026-09-18T22:21:15Z)
- Verdict: **NEW**
- Finding: "R48 used positive one-step error decreases and was attracted to random noise because random fluctuations repeatedly look like short-lived improvement." R49 replaces it with structured learnability (transition predictor + outcome entropy + two-window learning progress; high persistent value only with variation *and* above-chance prediction skill; no hardcoded region bonus). Also R48's self-model: "greedy posterior-mean policy under-explored strategy alternatives" → generic UCB over strategy/context outcome histories. Abandoned direction + stated reason, per baseline category 2.
- Quote: "R48 used positive one-step error decreases and was attracted to random noise because random fluctuations repeatedly look like short-lived improvement."

---

## NEW — minor (test results / process, one-liners)

### 10. R33-N16: strongest synthetic stability/plasticity evidence, closed + consumed
- Doc: `TNN/TNN/Research/R33_NATIVE_N16_RESULT.md` (1,561 B) / `R33_NATIVE_N16_SUPPORT_ROUTING/POSTRUN_INDEPENDENT_REVIEW.md` (1,443 B), 2026-09-18
- Verdict: **NEW**
- Finding: terminal disposition `CONFIRM_FULL_PREREGISTERED_SYNTHETIC_N16_QUALIFICATION`; 498 exposures, dev selected arm19 (75%-training-mean projection specialist); "strongest bounded synthetic stability/plasticity evidence in the R33 continuation: broader old-support preservation plus localized projection routing maintained strong fresh new learning while sharply reducing old-behavior loss on two disjoint holdouts." Still does not beat/replace R27 (synthetic parent). Baseline never mentions N16.

### 11. R32 E51F: state-aliasing ruled out — next discriminator is value-function capacity
- Doc: `TNN/TNN/Research/R32_E51F_RESULT.md` (1,519 B, modified 2026-09-18T22:21:04Z)
- Verdict: **NEW**
- Finding: audit of 91,800 sequential states per representation: zero exact alias groups, zero cross-class conflicts. Verdict `VALID DIAGNOSTIC — NO_EXACT_ALIASING_FOUND_TEST_VALUE_FUNCTION_CAPACITY_NEXT`. "The next causal discriminator is therefore value-function capacity/generalization on the same state information, not another hand-authored feature addition and not a connection-topology rewrite." Baseline mentions E45/E48 negatives but not E51F.

### 12. R37 robust context routing: FRESH CHALLENGE FAIL / PRESERVED
- Doc: `TNN/TNN/Research/R37_ROBUST_CONTEXT_ROUTING_20260917/R37_RESULT.md` (1,384 B), 2026-09-18
- Verdict: **NEW**
- Finding: dev selected `haz05` (adaptive hazard 0.05); passed 5/7 gates — failed 5% mean-improvement requirement, worst-world ratio regressed 1.4677x→1.6630x vs V2. Conclusion: "a monolithic self-context posterior still confuses partial recombinations of capability/cost state. The next architectural hypothesis should factor self-context into independently reusable latent factors."

### 13. R38 factorized self-context: FRESH CHALLENGE FAIL / PRESERVED
- Doc: `TNN/TNN/Research/R38_FACTORIZED_CONTEXT_20260917/R38_RESULT.md` (1,339 B), 2026-09-18
- Verdict: **NEW**
- Finding: wave 2 selected `hybrid_adaptive`; passed 5/8 fresh gates, failed return/worst-world/unseen-recombination. Conclusion: "prediction blending is still too passive: the learner can store reusable factors yet fail to reactivate the right cost factor on return. The next architecture should maintain online latent factor experts."

### 14. R41 strategy-specific reliability arbitration: DEVELOPMENT NO-GO / FRESH UNOPENED
- Doc: `TNN/TNN/Research/R41_STRATEGY_RELIABILITY_20260917/R41_RESULT.md` (1,213 B), 2026-09-18
- Verdict: **NEW**
- Finding: all 120 dev jobs completed, no candidate cleared 8 gates; frozen fresh family never opened. "scalar reliability memories, even strategy-specific, do not provide enough state information to decide which substrate is locally trustworthy. The next architecture must condition routing on the learner-visible operating state / feature trajectory."

### 15. R39 lineage context (waves + fresh preregs)
- Docs: `R39_ONLINE_FACTOR_EXPERTS_20260917/PREREGISTRATION.md` (1,756 B), `PREREGISTRATION_WAVE2.md` (1,322 B), `PREREGISTRATION_WAVE3.md` (1,445 B), `FRESH_PREREGISTRATION.md` (1,202 B), 2026-09-18
- Verdict: **NEW**
- Finding: R36→R37→R38→R39→R40→R41 factor-expert lineage; wave 2 added provisional factor confirmation (128/256-obs window) + stable-model blend after wave 1 showed "immediate factor commitment creates too many experts under transient noise"; wave 2 also showed "delayed confirmation harmed recurrence/recombination", so no confirmation-window variants continued. Process detail not in baseline.

### 16. V68/V73 compiler review: stable's imported bare-constant defect documented
- Doc: `TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z/V68_V73_INDEPENDENT_REVIEW.md` (1,710 B), 2026-09-18T22:21:05Z
- Verdict: **NEW**
- Finding: "The older local candidate eliminates it in exercised originals and bounded semantic controls; COMPILER_DECISION.json retains stable because broad bootstrap/fixpoint/provenance qualification is absent." Extends baseline's znc-bug list (hot-path miscompile, wasm, arm64 syscall) with a fourth characterized defect: stable's general imported bare-constant defect.

---

## CONFIRMS (one line each)

- 0312 `R33_NATIVE_N15_PRESERVATION_ADDITIVE/INDEPENDENT_REVIEW_V3.md` (1,943 B, 2026-09-18): prereg-only approval, no execution authorization — confirms prereg discipline; no new facts.
- 0313 `R33_NATIVE_N03A_RESULT.md` (1,939 B): N03A journal regression passed 60/60, frozen N03 stays a failed partial batch — confirms native corrective-regression pattern.
- 0315 `R33_NATIVE_N01B_RESULT.md` (1,926 B): N01B direct-child cases matched (79 CHECK rows); admits only trusted direct-child lane — routine R33 engineering.
- 0316 `R33_CLOSEOUT_20260915T174458Z/final_status/Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/INTEGRATION_REVIEW_20260915.md` (1,895 B): N19 Lane C PASS_WITH_NARROW_SCOPE, BUILD_08 stays REQUEST_CHANGES — consistent with baseline integrator posture.
- 0318 `R33_NATIVE_N17_R27_CONTINUITY/REVIEW_REQUEST.md` (1,837 B, 2026-09-18): N17 review asks reviewer to ensure historical 33/33 receipt isn't "laundered into new evidence" — confirms anti-laundering rule.
- 0319 `R33_FINAL_FROZEN_20260915T214529Z/INDEPENDENT_INTEGRATOR_REVIEW.md` (1,831 B): integrator PASS bounded engineering / REQUEST_CHANGES full R33 — consistent posture.
- 0321 `R33_NATIVE_N02A_PREREGISTRATION.md` (1,794 B): N02A corrects N02's malformed 528-hex-char SHA256 constant table against RFC6234 §5.1 — engineering correction, confirms "preserve failure, new identity" rule.
- 0322 `R33_NATIVE_N04_RESULT.md` (1,779 B): N04 telemetry component passed 556 assertions; synthetic fixtures only — routine.
- 0323/0330 `R33_NATIVE_N13A_FINGERPRINT_SCRATCH/REVIEW_REQUEST(_COORDINATION_J059).md` (1,767/1,618 B): continue-existing-reviewer coordination, binaries pinned SHA256 df5e8bfa… — process, no new facts.
- 0324/0350 `R33_NATIVE_N15_PRESERVATION_ADDITIVE/POSTRUN_INDEPENDENT_REVIEW(_V2).md` (1,760/1,311 B): N15 V1 REQUEST_CORRECTION (scope overclaim removed), V2 correction verified — process detail folded into finding 5.
- 0327 note folded into finding 16.
- 0328/0353 `R33_NATIVE_N05B_DURABLE_TELEMETRY/REVIEW.md` (1,707 B), `R33_NATIVE_N08B_ISOLATION/REVIEW.md` (1,257 B): pre-exposure engineering reviews (N05A 4-byte/8-byte allocator mismatch diagnosed; N08B socket-creation-vs-connection policy correction) — routine R33 engineering process.
- 0329 `R33_NATIVE_N17_R27_CONTINUITY/AUTHORING_NOTES.md` (1,686 B): identity.zag is compile-only authoring, "never continuity evidence"; authoring driver is a refusal sentinel exiting 73 — confirms no-counters-increment rule.
- 0332 `R33_NATIVE_N16_SUPPORT_ROUTING/POSTRUN_REVIEW_TRANSPORT_HISTORY.md` (1,578 B): two reviewer *transport* failures (ChatGPT stream disconnects), no scientific disposition — process artifact, no science.
- 0335 `R38_FACTORIZED_CONTEXT_20260917/FRESH_PREREGISTRATION.md` (1,532 B), 0356/0357/0361/0363 fresh preregs (R39/R40/R37/R41, ~1.0–1.2 KB): frozen fresh-family gate lists — process scaffolding for findings 12–15.
- 0338 `R33_N13A_CLOSEOUT_SNAPSHOT_V1/Research/R33_N13A_CLOSEOUT_SUMMARY.md` (1,511 B): N13A closed/consumed, 24,601 child checks + 62 parent checks passed — routine closeout.
- 0339/0345 `R41_STRATEGY_RELIABILITY_20260917/PREREGISTRATION.md` (1,500 B) / `R33_NATIVE_N08A_ISOLATION/REVIEW.md` (1,361 B): prereg + review scaffolding — process.
- 0341 R39 wave3 prereg: folded into finding 15.
- 0342 `R33_NATIVE_N16_SUPPORT_ROUTING/POSTRUN_INDEPENDENT_REVIEW.md` (1,443 B): final N16 confirm disposition — folded into finding 10.
- 0344 R37 result: folded into finding 12. 0347 R38 result: folded into finding 13. 0348 R39 wave2 prereg: folded into finding 15.
- 0349 `.r34_native_extract_20260917/Research/R34_BEHAVIORAL_HELDOUT_STAGE_20260916/PREREGISTRATION_V2.md` (1,312 B): R34 V1 invalid controls listed (association erased cue identity; curiosity tracked evaluator jitter; self-model covered only final regime) — confirms honest-evaluator-construction discipline.
- 0355 `R33-N05_DURABLE_TELEMETRY_PREREGISTRATION.md` (1,212 B): N05 asks whether a bounded native Zag telemetry path can preserve ordered evidence→memory→hypothesis→decision→consequence→update traces across commit/replay — design intent, consistent with baseline audit-ledger work.
- 0358 `R34_NATIVE_CONTINUAL_LEARNER_V1/PREREGISTRATION.md` (1,122 B): pure-Zag continual learner engineering prereg (64/64 both tasks, 192 online updates, byte-identical reload) — engineering pattern, no new direction.
- 0359 `R33_NATIVE_N02_RESULT.md` (1,108 B): N02 negative — malformed round-constant transcription, failure preserved, no compiler defect inferred — root cause of finding in 0321.
- 0360 `R33_NATIVE_N18_R27_FROZEN_CORE_SIDECAR/CONCEPT_REVIEW_01.md` (1,093 B): N18 sidecar REQUEST_CHANGES; keeping R27 bytes unchanged proves custody not behavioral canonicity — confirms continuity-gate strictness.

## SUPERSEDED

- None (no doc in this batch is overtaken by a newer verdict within the batch).

## NOISE

- 0314 `R42_STATE_CONDITIONED_RELIABILITY_20260917/.python-runtime/cpython-3.13.12-macos-aarch64-none/lib/python3.13/idlelib/Icons/README.txt` (1,935 B, modified 2026-09-17T17:33:57Z): IDLE logo README bundled inside a Python runtime dir — not a TNN document at all.
