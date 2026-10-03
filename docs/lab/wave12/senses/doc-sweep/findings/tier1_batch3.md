# Tier-1 batch 3 findings (files 0156–0207)

Read against BASELINE.md. 52 files read. Verdicts: NEW=34, CONFIRMS=17, SUPERSEDED=1, NOISE=0.
No koryphaios/ghost mentions anywhere in this batch (grep confirmed).
No direct contradictions with baseline found; two tension points flagged.

---

## NEW findings (34)

### 0000 — N13 authoring/review history (test-process evidence)
- Drive: `TNN/TNN/Research/R33_NATIVE_N13_TORCH_VIEWS/BUILD_AND_REVIEW_HISTORY.md` (5309 B, 2026-09-18)
- Verdict: NEW — extends R33 N13 (baseline knows R33 E45/E48 qualification but not N13 review mechanics).
- Finding: independent reviewer Euler's V1 review fired REQUEST_CHANGES with four concrete findings R1–R4 (dot-key oracle, length-fields crossing record cap, empty failed fixture construction credited as a rejection, unchecked evaluator allocations); corrected BUILD_05/06 built but "No executable or fixture has run" at authoring time.
- Quote: "Independent final review returned REQUEST_CHANGES... It independently confirmed R1 (dot-key oracle), identified R2 (one/four-byte length fields crossing the record cap losing capacity provenance), R3 (empty failed fixture construction credited as a malformed-input rejection) and R4 (unchecked evaluator allocations before indexed setup writes)."
- Fills: review rigor detail for R33 N13; anchors reviewer codename "Euler".

### 0002 — R27 native master results (vision + PAM Foundry + speech + memory policy)
- Drive: `TNN/TNN/Research/TNN_R27_NATIVE_MASTER_RESULTS.md` (5206 B, 2026-08-23)
- Verdict: NEW — major; baseline knows none of this result content.
- Findings:
  1. **Autonomous PAM Foundry**: two opcode-credit learners FAILED (global credit "worse than random", per-op ablation worse still); replaced by whole-graph evolutionary shadow search: evolved hidden mean 252.02 vs random 196.09 (+55.93 gain, 99.33% win rate). "The search mechanism, not a particular topology, is now the canonical Foundry design in the shadow Zag source." → senses/PAM origins; ARCHAEOLOGY LEAD: a PAM-creation mechanism ("canonical Foundry design") exists in R27-era shadow Zag source, not yet inventoried.
  2. Vision tournament: sorted_normalized 1.000 across view/hard permutations at dose 16, but occlusion stuck ~0.06–0.10: "does not solve occlusion. Occlusion must rely on temporal entity continuity/active observation rather than pretending missing pixels contain identity."
  3. Connected speech without VAD: 99.98%/99.10% nominal, but 71.24% on harder challenge — "near-perfect nominal result therefore fails robustness qualification."
  4. Memory policy: converged to EXACT_ALL under weak pressure — "TNN should not forget merely to mimic humans" (design rationale for retention posture).
- Quotes: "The search mechanism, not a particular topology, is now the canonical Foundry design in the shadow Zag source." / "Occlusion must rely on temporal entity continuity/active observation rather than pretending missing pixels contain identity." / "the learned policy converged to EXACT_ALL, which is rational and was retained as a finding: TNN should not forget merely to mimic humans."
- Fills: PAM origins; abandoned direction (opcode-credit learners, why); vision honest limits; memory-policy rationale.
- ⚠ Tension (not contradiction): baseline says senses archaeology found "no recoverable full PAM design on searched layers"; this doc asserts a "canonical Foundry design in the shadow Zag source" — the shadow source may be an unsearched layer worth re-checking.

### 0005 — R33 parameter scaling plan (scaling doctrine)
- Drive: `TNN/TNN/Research/R33_PARAMETER_SCALING_PLAN.md` (5070 B, 2026-09-18)
- Verdict: NEW — design rationale absent from baseline.
- Finding: first fixed-family scaling matrix P(H)=67H+2 (8→2048 cells), with stop rules: plateau declared only under preregistered improvement margins, no post-hoc peak selection, and "Never shrink memory or restart the continuing brain to make a larger arm appear stable." Also: E51M/E51N dose×capacity results are "not a monotonic scaling law. Do not repeat it as the R33 capacity study."
- Quote: "Never shrink memory or restart the continuing brain to make a larger arm appear stable."
- Fills: design rationale — why past dose/capacity work is not repeated, and the anti-gaming rule for scaling studies.

### 0006 — E51AA result (terminal mechanism diagnosis)
- Drive: `TNN/TNN/Research/R32_E51AA_RESULT.md` (4988 B, 2026-09-18)
- Verdict: NEW — test result never seen (baseline: E50 parent evidence only).
- Finding: `MIXED_RESOURCE_FEASIBLE_TERMINAL_LIMIT` — 341 frozen misses decompose as 292 scalar-only, 1 commit-ranking-limited, 48 action-support-limited; the 48 are concentrated in changing-state regimes (modes 4/5): "the correct latent hypothesis may be supported by evidence before the temporal state machine has placed it in a reportable slot." Smallest justified change: generic `COMMIT(candidate)` direct access to hypothesis candidates.
- Quote: "48 known episodes cannot express the grounded-correct answer at any feasible stop because KEEP / CURRENT / RESTORE only report already-materialized belief-state slots."
- Fills: why direct-candidate-commit was introduced (E51AB→E51AC chain); design rationale.

### 0007 — E51N result (calibration dose/capacity plateau)
- Drive: `TNN/TNN/Research/R32_E51N_RESULT.md` (4911 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: `VALID NATIVE NEGATIVE — CALIBRATION DOSE/CAPACITY PLATEAU WITH TRADEOFFS`; the grid is non-monotone (16 hinges improve UNKNOWN but sacrifice known; 4x never dominates 1x); rejects the inherited E51M "coarse printed flags" (`dose_signal=1`/`capacity_signal=1` on any adjacent local step) as non-conclusions. Also establishes domain-separated world-ID/RNG evaluator infrastructure replacing the exhausted global transient-PRNG allocator.
- Quote: "The actual grid is not monotone... Therefore the defensible classification is a dose/capacity plateau with operating-point tradeoffs, not a validated training-dose rescue or monotone capacity curve."
- Fills: abandoned direction (scalar calibration dose/capacity as rescue), stated reason; evaluator infra rationale.

### 0008 — N15 preservation/additive design (stability-plasticity discriminator)
- Drive: `TNN/TNN/Research/R33_NATIVE_N15_PRESERVATION_ADDITIVE/DESIGN.md` (4910 B, 2026-09-18)
- Verdict: NEW — design rationale absent from baseline.
- Finding: 12-mechanism bounded discriminator testing the hypothesis that ordinary shared rewriting damages prior behavior while preservation-gated or zero-initialized additive specialists improve the frontier; explicit sentinel terminal negative `DEVELOPMENT_NO_POSITIVE_GAIN_CANDIDATE`; old/new probes are evaluator-only and never used to fit/gate.
- Quote: "Additive specialists begin with all-zero weights and therefore have zero behavioral contribution at the fork. Their gate is a generic two-prototype Manhattan-distance comparison estimated from unlabeled old and new training inputs."
- Fills: memory/learning-scheme origins — the stability-plasticity design lineage that N16 continues (→0008's closeout at 0036).

### 0009 — E51AC result (direct-candidate hybrid partial)
- Drive: `TNN/TNN/Research/R32_E51AC_RESULT.md` (4899 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: `VALID PARTIAL — DIRECT_CANDIDATE_COMPLEMENT_PARTIAL`; best hybrid +57 episodes over frozen controller (79 known gained, 22 no-unique lost); direct learner reaches 98 known trajectories the mature controller misses, but 140 known trajectories are unreachable by either learner — "routing alone cannot make the current pair exact."
- Quote: "E51AC establishes two distinct limits... direct candidate commitment is useful as an additive mechanism... However... 140 known trajectories remain outside the support of both learners."
- Fills: next-step rationale (trajectory-critical admission objective; candidate-value residual objective).

### 0011 — E51AF result (prereg integrity invalidation)
- Drive: `TNN/TNN/Research/R32_E51AF_RESULT.md` (4886 B, 2026-09-18)
- Verdict: NEW — procedural/integrity finding not in baseline.
- Finding: E51AF invalidated before execution — current native E51AE reproduction (run 33452596868) disagreed with frozen historical prerequisites on source identities AND development ledger (critical records 605 vs 639; no-unique 1 vs 133; 5132/5400 vs 5395/5400); the historical Actions run itself failed during assembly (missing e51ae_assemble.py). Rule honored: "any source or ledger disagreement invalidates E51AF before interpretation." E51AG takes the "accept current lineage" route.
- Quote: "E51AF must not execute or be interpreted as a partition-sensitivity experiment. Its preregistration required an independent GitHub-native reproduction... The successfully executed current E51AE lineage disagrees with those frozen historical prerequisites."
- Fills: honest-failure culture evidence; anchors the historical-vs-current E51AE divergence.

### 0012 — N11 supervisor-bound parent custody result
- Drive: `TNN/TNN/Research/R33_N11_CLOSEOUT_SNAPSHOT_V1/Research/R33_NATIVE_N11_RESULT.md` (4780 B, 2026-09-18)
- Verdict: NEW — test result never seen (baseline: no N11 content).
- Finding: engineering PASS — 424 completed-child checks (405 top-level + 19 worker); 128-byte binding tamper-proof; custody-only API returns -8904 (explicit always-unavailable training admission); 23 diagnostic batches consumed, zero R33 training runs.
- Quote: "The custody-only API returned its specified unavailable-training code -8904. That is an engineering refusal, not evidence of a learned ability or complete milestone enforcement."
- Fills: custody-lane milestone evidence.

### 0013 — R46 result (factorized latent residual NO-GO)
- Drive: `TNN/TNN/Research/R46_FACTORIZED_PREDICTIVE_LATENT_20260917/R46_RESULT.md` (4769 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: `DEVELOPMENT NO-GO / FRESH UNOPENED` — "falsifies this specific factorized additive-residual hypothesis as a general solution"; rules out BOTH low-dimensional fixes (scalar arbitration R40–R42, and single continuous additive residual R46). Next hypothesis: bounded state-conditioned expert-selection/mixture-of-residuals with anti-interference and noise-abstention controls. Note: ran on CPython 3.13.12 + NumPy (not native Zag).
- Quote: "The accumulated evidence now rules out both of the obvious low-dimensional fixes: 1. progressively finer scalar arbitration (R40–R42), and 2. a single continuously learned additive residual driven by the same delayed learner-visible state (R46)."
- Fills: abandoned direction + stated reason; extends "already-known Drive facts" with R46 closure.

### 0015 — N13 result (consumed resource-gate failure + diagnosis)
- Drive: `TNN/TNN/Research/R33_N13_CLOSEOUT_SNAPSHOT_V1/Research/R33_NATIVE_N13_RESULT.md` (4704 B, 2026-09-18)
- Verdict: NEW — test result never seen; honest FAIL-with-evidence.
- Finding: `FAILED_RESOURCE_GATE` — inventory child exceeded 384MiB ceiling by 6.875MiB (7,208,960 bytes); all functional checks passed (matrix 102, refusals 123) but resource gate overrode; diagnosis: pinned compiler lowers _zag_free to no-op + non-reclaiming bump arenas, with ~140MB of header tables and ~131.7MB of evaluator-hash copies identified as source-level extents.
- Quote: "Its zero exit and child PASS do not override that resource failure." / "The pinned compiler's actual commit source lowers _zag_free to a no-op and uses non-reclaiming bump arenas."
- Fills: concrete instance of the znc compiler-allocation behavior (relates to the znc bugs already in memory); honest-failure evidence.

### 0016 — R33 architecture contract (roles, lifetime identity, graph death)
- Drive: `TNN/TNN/Research/R33_ARCHITECTURE_CONTRACT.md` (4697 B, 2026-09-18)
- Verdict: NEW — design rationale absent from baseline.
- Findings:
  1. Explicit death of graph machinery as a candidate: "The inherited explicit correction keeps active cognition and future Foundry graph-free. Historical graph controls remain history, not an implementation candidate or a justification for restarting that tournament."
  2. Lifetime identity rules: brain_id, immutable parent digest, migration must preserve episodes/parameters/memory policy/optimizer/replay state/RNG streams; "A smaller-capacity arm cannot silently discard parent knowledge."
  3. Role table: human trainer never fabricates learner competence; evaluator "cannot influence learner features, scheduling or update selection through hidden labels."
- Quote: "The inherited explicit correction keeps active cognition and future Foundry graph-free. Historical graph controls remain history, not an implementation candidate or a justification for restarting that tournament."
- Fills: design rationale — abandoned direction (graph cognition) with the explicit correction that killed it.

### 0017 — N04 telemetry V2 preregistration
- Drive: `TNN/TNN/Research/R33_NATIVE_N04_PREREGISTRATION.md` (4691 B, 2026-09-18)
- Verdict: NEW (minor) — semantic rationale + honest review-gap admission.
- Finding: V2's only semantic change removes the requirement that every refusal record claim a new request ("Producers remain responsible for honest occurrence attribution"); plus the admission that the independent reviewer spawn failed the agent limit and "Neither counts as an independent verdict."
- Quote: "Reuse of the prior telemetry agent returned not-found; a new independent reviewer spawn failed the agent limit. Neither counts as an independent verdict."
- Fills: review-gap honesty trail.

### 0019 — R33 sensor qualification plan (S0/S1/S2 doctrine)
- Drive: `TNN/TNN/Research/R33_SENSOR_QUALIFICATION_PLAN.md` (4671 B, 2026-09-18)
- Verdict: NEW — design rationale behind the S0/S1/S2 contract the baseline already knows.
- Finding: three-gate ladder definitions (S0 transport / S1 information / S2 usable perception) with the key asymmetries: "Passing S0 does not establish S2; failure at S2 is not automatically failure of transport or higher cognition." Four-route factorial (raw only / processed only / raw+abstraction / raw+abstraction+arbitration). "100% good to go" defined as zero violations in a published bounded contract — never unrestricted perfect perception. Boundary battery requires boundary−1/boundary/boundary+1, empty, malformed, saturated, corrupted inputs.
- Quote: "S1 information: task-relevant distinguishing detail survives to an available learner input... Similarity of a processed embedding is not a proof of raw fidelity."
- Fills: senses ORIGINS — the qualification doctrine rationale; answers why S1 sits between transport and perception.

### 0023 — E51O result (local calibration memory negative)
- Drive: `TNN/TNN/Research/R32_E51O_RESULT.md` (4563 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: `VALID NATIVE NEGATIVE — WEAK MONOTONE LOCAL-CAPACITY SIGNAL WITH MATERIAL KNOWN/UNKNOWN TRADEOFF`; 8→64 cells: known 4174→4175, no-unique 1163→1166 at 13.6x routing cost; "one scalar offset per local region is still too low-capacity"; next = per-region conditional weight correction (→E51P).
- Quote: "This is therefore not evidence that simply scaling scalar prototypes to hundreds or thousands is the right cognitive architecture."
- Fills: abandoned sub-direction (scalar prototype scaling) + stated reason.

### 0024 — R42 result (state-conditioned reliability NO-GO)
- Drive: `TNN/TNN/Research/R42_STATE_CONDITIONED_RELIABILITY_20260917/R42_RESULT.md` (4498 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: `DEVELOPMENT NO-GO / FRESH UNOPENED` — bounded state-conditioned scalar blend correction failed; the state signal updated 4,792+ times per row but moved the 70/30 blend only 0.0012–0.0028 (floor 0.01); "using state only to perturb one factor-vs-stable mixture coefficient is still too restrictive." (Same CPython/NumPy platform note as R46.)
- Quote: "R40 ruled out global channel-level scalar reliability, R41 ruled out strategy-specific scalar reliability, and R42 now rules out this bounded state-conditioned scalar blend correction as an adequate solution."
- Fills: closes the R40–R42 scalar-arbitration line (cross-ref 0013).

### 0025 — N10 inert accepted-parent mapping result
- Drive: `TNN/TNN/Research/R33_NATIVE_N10_RESULT.md` (4427 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: engineering PASS — native parser consumed all 15,871,908 accepted bytes (375,763 inert nodes, 244,250 relations, 640,946 opcode occurrences, 175,954 memo entries); historical semantic digest preserved but unrecomputed; "Legacy graph/BPE/VAD content remains inert, not erased or activated."
- Quote: "Legacy graph/BPE/VAD content remains inert, not erased or activated."
- Fills: parent-recovery archaeology milestone; how graph/BPE/VAD were handled (frozen inert, not deleted).

### 0026 — N01B main review (review-gap honesty + provenance deviation)
- Drive: `TNN/TNN/Research/R33_NATIVE_N01B_MAIN_REVIEW.md` (4384 B, 2026-09-18)
- Verdict: NEW (minor) — process evidence.
- Finding: both assigned independent reviewers returned terminal infra errors; "No failed review is counted as successful." Documents a build-provenance deviation: BUILD01 binary hash changed after oracle amendment ("Do not claim the older binary is retained or that BUILD01 was immutable") — kept documented rather than rewritten as compliance.
- Quote: "No failed review is counted as successful. The completed earlier N01 review and N01A/N01P negatives remain applicable criticism, not final-source certification."
- Fills: honesty/anti-cheat trail detail.

### 0028 — E51B native result (continuation causal leverage)
- Drive: `TNN/TNN/Research/R32_E51B_NATIVE_RESULT.md` (4338 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: `EXECUTED_VALID_NATIVE_NEGATIVE — NO VALIDATED SEQUENTIAL RESCUE`; learned CONTINUE has genuine causal leverage (+68/+72 no-unique UNKNOWN conversions under both frozen terminal representations) but the single linear head is unselective: net grounded utility −283,812 (M0) / −261,383 (M1), known success −76/−58, every-cell safety still FAIL. Rejects the linear continuation approximation, "not continuation-versus-termination value itself"; next = learner-owned continuation-head Foundry.
- Quote: "A learned sequential continuation action has causal leverage: under both frozen E50 terminal representations it converts dozens of otherwise wrong no-unique commitments into grounded UNKNOWN outcomes."
- Fills: continuation-line evidence; why Foundry was the prescribed next step.

### 0029 — R33 independent review dispositions
- Drive: `TNN/TNN/Research/R33_INDEPENDENT_REVIEWS.md` (4314 B, 2026-09-18)
- Verdict: NEW — reviewer/people anchoring + dispositions absent from baseline.
- Finding: three read-only reviews 2026-09-05 — architecture (Leibniz), training (Locke), safety (Ptolemy). Strongest architecture objection: "silent trace saturation and mutation-before-record wrappers." Explicit attribution boundary: "Do not attribute prototype trace/LRU/sensory deficiencies to AJ, where those named helpers were absent from the inspected executable path." Plus a 2026-09-15 remediation closeout (safe-custody/stale-receipt changes closed; 508-byte historical R25 receipt hash-bound; 26 N17 rows still fail-closed).
- Quote: "The strongest objection is the gap between inspectability requirements and actual prototype behavior: silent trace saturation and mutation-before-record wrappers."
- Fills: people anchoring (Leibniz/Locke/Ptolemy reviewer codenames); AJ attribution boundary.

### 0032 — N09 supervisor-anchored checkpoint result
- Drive: `TNN/TNN/Research/R33_NATIVE_N09_RESULT.md` (4300 B, 2026-09-18)
- Verdict: NEW (minor) — test result never seen.
- Finding: engineering PASS — checkpoint cache qualified against supervisor journal; nested kernel-confined worker denied write/unlink/fork/socket; honest boundary: "NOT protection against a host administrator or trusted controller replacing the entire journal, nor a hardware/remote monotonic anchor. N07's authentic-prefix limitation remains true in that broader threat model."
- Quote: "This qualifies a bounded checkpoint cache against the independently held current supervisor journal and pinned kernel-worker boundary."
- Fills: custody/checkpoint lane milestone; explicit threat-model limits.

### 0036 — N16 closeout summary (stability/plasticity qualification)
- Drive: `TNN/TNN/Research/R33_N16_CLOSEOUT_SUMMARY.md` (4150 B, 2026-09-18)
- Verdict: NEW — major test result never seen.
- Finding: CLOSED/CONSUMED with independent disposition `CONFIRM_FULL_PREREGISTERED_SYNTHETIC_N16_QUALIFICATION` — development selected arm19 (75%-threshold training-mean projection specialist + dual-512 old-support preservation tolerance 1), gate 1 at development, validation (16 populations) and confirmation (16 populations); old loss reduced to 12 (val) / 7 (conf) vs N15's substantial unseen loss; 498 total arm-population exposures, no stage rerun. Explicit: "Why R27 remains unbeaten canonically" — synthetic parent, not R27-continuous.
- Quote: "Arm19 then retained useful new learning while reducing selected-arm old loss to 12 in validation and 7 in confirmation, with maximum final-old deficits 4 and 2 respectively."
- Fills: the stability/plasticity line's positive result (N15→N16 arc); qualified mechanism not yet applied to R27-continuous learner.

### 0037 — N19 adversarial review (poisoned-handle defect caught + repaired)
- Drive: `TNN/TNN/Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_B/ADVERSARIAL_REVIEW.md` (4145 B, 2026-09-18)
- Verdict: NEW — defect evidence never seen.
- Finding: confirmed defect — `n19_append_existing_fixture` and its retained-root variant replayed into a new handle without checking the caller's poison flag ("This contradicts the recovery protocol's unusable-handle promise"); V5 repair validates poison before open/write; disposition `PASS_WITH_NARROW_SCOPE`. Also a supervisor gap kept as additive independent candidate (up to 64 EINTR retries after kill).
- Quote: "The fresh pre-repair adversary returned status 0, changed the journal from 32 to 64 bytes, and exited 1 because the refusal assertion failed... This contradicts the recovery protocol's unusable-handle promise."
- Fills: adversarial-catch evidence in the runtime-boundary lane.

### 0039 — E51AB result (direct replacement negative)
- Drive: `TNN/TNN/Research/R32_E51AB_RESULT.md` (4089 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: `VALID NEGATIVE — DIRECT_CANDIDATE_ACTION_SUPPORT_UNCONFIRMED_COMPARE_LEDGER`; replacing the mature controller with regressed candidate-return heads fails: best local-384 arm 3,324/4,200 known vs mature 3,949/4,200 on the same fresh partition (direct heads learned safe-abstention, 1,200/1,200 no-unique, but suppressed valid commitment); "not evidence against direct candidate actions themselves. It is evidence against making low-support direct candidate regressors replace mature slot-based terminal competence." → justifies additive hybrid (E51AC).
- Quote: "This is not evidence against direct candidate actions themselves. It is evidence against making low-support direct candidate regressors replace mature slot-based terminal competence."
- Fills: the replace-vs-augment design lesson; causal link E51AB→E51AC.

### 0040 — E51AJ pre-execution review (external AI reviewers)
- Drive: `TNN/TNN/Research/R32_E51AJ_ANALYSIS/PREEXECUTION_REVIEW.md` (4082 B, 2026-09-18)
- Verdict: NEW — people/tooling anchoring.
- Finding: design reviewed by an external "ChatGPT Web" reviewer (agent `01a07027-7ea7-7d71-b2c8bdcf211e`, "no material pre-execution flaw"); "No Sol substitution was made"; the earlier Noether E51AI reviewer terminated on a browser-turn limit and supplied no verdict. Evidence-preservation note: GitHub artifact ZIP expires 2026-12-04T06:14:32Z, so the local ZIP is "intentionally not a versioned binary in this commit."
- Quote: "The reviewer checked that one common learned state is copied into all arms... Required qualifications retained: endpoint multiset matching does not match every intermediate block."
- Fills: people anchoring (ChatGPT Web reviewer agent IDs, Noether, Sol as agent names); dated 2026-09-05 Pacific.

### 0041 — N05B durable-telemetry preregistration (compiler allocation root cause)
- Drive: `TNN/TNN/Research/R33_NATIVE_N05B_DURABLE_TELEMETRY/PREREGISTRATION.md` (4061 B, 2026-09-18)
- Verdict: NEW (minor) — compiler-behavior evidence.
- Finding: corrective regression for N05A's configuration corruption; root cause documented from pinned compiler source (commit 7cacbfc0, `acodegen.zag`): "zfree is arena-style, not an incremental release"; allowed fix: native zalloc_i + corrected eight-byte alias extents + signed wire-range validation.
- Quote: "The pinned compiler source at 7cacbfc04f6cffec02ea9b1d5ff6702fe2e93f3c... defines eight-byte numeric element strides and zalloc_i allocations. Its zfree is arena-style, not an incremental release."
- Fills: concrete znc allocator semantics evidence (cross-ref 0015's no-op _zag_free).

### 0042 — B000 result (five native boundary defects)
- Drive: `TNN/TNN/Research/R33_B000_RESULT.md` (4048 B, 2026-09-18)
- Verdict: NEW — defect evidence never seen (baseline knows B001's 11 bugs, not B000's five witnesses).
- Finding: `EXPECTED_WITNESSES_MATCHED` — five confirmed boundary defects in prototype helpers: W1 visual transform loses channel order; W2 acoustic duration24/width12 window misses unsampled detail; W3 trace saturation silently drops an event at 8,192; W5 output limits silently omit the tail; W4 protected-slot selection works. "The justified next implementation is a separate native component with exact raw transport, explicit capacity failures, protected-slot refusal" — the direct rationale for the B001/sensor path.
- Quote: "W1 visual: Ascending and reversed eight-channel raw arrays produced identical signatures... The tested transform loses channel order."
- Fills: senses origins — the boundary-defect evidence that motivated the exact-raw-transport sensor design.

### 0043 — E51AJ post-execution review (Pauli reviewer)
- Drive: `TNN/TNN/Research/R32_E51AJ_ANALYSIS/POSTEXECUTION_REVIEW.md` (4034 B, 2026-09-18)
- Verdict: NEW — interpretation result never seen.
- Finding: reviewer "Pauli" (chatgpt-web/pro, agent 01a0708d-8e6c-7d71-94a9-c3660b456b3a, 2026-09-05); aggregate label `MIXED_OR_UNREPLICATED_RETENTION_DIRECTION` (replay counts 1/14, 9/11 fail; 17/6 passes); three interpretation boundaries: final recovery ≠ uninterrupted preservation (replica-2 lost/regained 4 anchors); aggregate improvements hide pointwise swaps (replica-2 A-only introduces 194 initial wrong commitments); a bias-only counterfactual was proposed but NOT executed (needs a separate analysis contract).
- Quote: "Final recovery is not uninterrupted preservation. Replica-2 replay cohort B ends retaining every anchor but lost and regained four along the way."
- Fills: retention-line interpretation detail; people anchoring (Pauli).

### 0044 — E50 preregistration + executed result (provenance contention negative)
- Drive: `TNN/TNN/Research/R32_E50_PROVENANCE_TEMPORAL_CONTENTION_PREREGISTRATION.md` (4018 B, 2026-08-29)
- Verdict: NEW — executed outcome appended to the prereg: test result never seen.
- Finding: `EXECUTED_VALID_NATIVE_NEGATIVE — 2026-08-28`; M1's grounded contention features (provenance-adjusted co-viability, temporal transition contention) were structurally active but changed no-unique outcomes 12,488 UNKNOWN/7,912 wrong → 12,428/7,972 — "60 fewer abstentions and 60 additional wrong commitments" — failing the every-cell safety gate; outcome `NO_TESTED_GROUNDED_PROVENANCE_TEMPORAL_CONTENTION_RESCUE`.
- Quote: "M1 changed no-unique outcomes from 12,488 UNKNOWN / 7,912 wrong to 12,428 UNKNOWN / 7,972 wrong: 60 fewer abstentions and 60 additional wrong commitments. It therefore failed the every-cell safety gate (0)."
- Fills: the E50 negative that motivated E51's continuation question.

### 0045 — Native journal design V1 (C03 replacement)
- Drive: `TNN/TNN/Research/R33_NATIVE_JOURNAL_DESIGN_V1.md` (3978 B, 2026-09-18)
- Verdict: NEW (minor) — design rationale.
- Finding: native Zag replacement for "C03's historical external Python collector"; root carries exact initial byte snapshot; "The hash chain is not a signature, grant or trusted timestamp. No learner can call this privileged operator API directly in a qualified system; that boundary is not yet proven." Component tests "do not prove they contain a complete TNN brain."
- Quote: "The hash chain is not a signature, grant or trusted timestamp."
- Fills: journal-lane origins; explicit claim boundaries.

### 0046 — E51G result (value-capacity negative)
- Drive: `TNN/TNN/Research/R32_E51G_RESULT.md` (3927 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: `VALID NEGATIVE — NO_TESTED_VALUE_CAPACITY_RESCUE`; learner-selected pairwise and hinge residuals were nondegenerate (12 commit terms each) but hinge improved no-unique +15 while losing 1 known — same abstention-vs-resolution tradeoff; next = approximation/objective geometry (→E51H/E51I).
- Quote: "This is the same qualitative abstention-versus-resolution tradeoff seen earlier, now under learner-selected nonlinear structure."
- Fills: why capacity wasn't the answer; causal link to the objective-geometry experiments.

### 0049 — E51A native result (continuation-audit negative)
- Drive: `TNN/TNN/Research/R32_E51A_NATIVE_RESULT.md` (3896 B, 2026-09-18)
- Verdict: NEW — test result never seen.
- Finding: `EXECUTED_VALID_NATIVE_DIAGNOSTIC_NEGATIVE`; all four arms 0/1000 no-unique UNKNOWN and 1000/1000 wrong — neither ungating continuation training nor the direct learned advantage rescues the historical E45 sequential controller; H4 supported: "changing continuation learning alone cannot rescue a controller whose terminal learner never represents a safe no-commit decision in the no-unique cells." Also: removing the initiation gate harmed known-truth success (5,734→5,608 etc.). Prescribes the E50+CONTINUE+cost+matched-control design (→E51B).
- Quote: "The preregistered H4 is supported: changing continuation learning alone cannot rescue a controller whose terminal learner never represents a safe no-commit decision in the no-unique cells."
- Fills: mechanism-level negative anchoring the E51B design.

### 0050 — N11 pre-exposure review (graph-as-bookkeeping rationale)
- Drive: `TNN/TNN/Research/R33_NATIVE_N11_PARENT_CUSTODY/REVIEW.md` (3848 B, 2026-09-18)
- Verdict: NEW (minor) — design rationale.
- Finding: "Native node/relation data is serialization bookkeeping, not active graph cognition." Also: training-admission function is explicitly always-unavailable for the custody API; disposal-controller may sign intentionally invalid descriptors; "No independent spawn-agent capability was returned by the available tool inventory" (review-gap honesty).
- Quote: "Native node/relation data is serialization bookkeeping, not active graph cognition."
- Fills: rationale for keeping serialized graph content inert (cross-ref 0025).

### 0051 — E51Q preregistration (residual margin audit; E51P numbers)
- Drive: `TNN/TNN/Research/R32_E51Q_RESIDUAL_MARGIN_AUDIT_PREREG.md` (3811 B, 2026-09-18)
- Verdict: NEW (minor) — test result numbers never seen.
- Finding: cites E51P's valid native 32-cell conditional-weight expert: 4,200/4,200 known-state reachability, 1,170/1,200 no-unique, every expert arm hit its 12-sweep optimization ceiling — the basis for the fresh uniform-shift-feasibility audit.
- Quote: "E51P's valid native 32-cell conditional-weight expert reached 4,200 / 4,200 known-state reachability but only 1,170 / 1,200 no-unique UNKNOWN reachability. Every expert arm hit its 12-sweep optimization ceiling."
- Fills: E51P outcome numbers absent from baseline.

---

## CONFIRMS (one line each)

- 0001 `0157_R32_E51B_BATCH_TERMINAL_SEQUENTIAL_CONTINUATION_PREREG.md` (5263 B): prereg for the E51B continuation experiment; outcome covered by 0028. Consistent with baseline prereg discipline.
- 0003 `0159_R32_E51H_NEUTRAL_RELATIVE_PREFERENCE_PREREG.md` (5202 B): prereg for E51H neutral-relative objective (UNKNOWN target exactly 0); no contradictions.
- 0004 `0160_README.md` (5107 B): E51AI reproducible-analysis packaging (archive verifier, frozen inputs); consistent with baseline provenance practice.
- 0010 `0166_INDEPENDENT_REVIEW.md` (4891 B): N19 recovery V5 PASS_WITH_NARROW_SCOPE; additive supervisor EINTR-retry candidate kept separate; all binaries freshly znc-built native. No baseline claims affected.
- 0014 `0170_DESIGN.md` (4715 B): N14 S1 information-preservation design behind the already-known N14 PASS; review-V1 blockers (superseded BUILD_01 named, positive-child-count acceptance) corrected pre-execution.
- 0018 `0174_DESIGN.md` (4685 B): N16 support-routing design; outcome covered by 0036.
- 0020 `0176_R32_E51I_TERMINAL_MARGIN_RANKING_AUDIT_PREREG.md` (4632 B): E51I margin/ranking diagnostic prereg (uniform-shift feasibility); consistent with baseline experimental norms.
- 0021 `0177_PREREGISTRATION.md` (4619 B): N08 kernel-confined worker prereg (Apple sandbox-exec loader); notes sandbox-exec "deprecated" — forward-compat risk stated, not a baseline claim.
- 0022 `0178_PREREGISTRATION.md` (4608 B): R46 prereg; frozen gates match the NO-GO outcome in 0013.
- 0027 `0183_R33_NATIVE_N14_RESULT.md` (4342 B): N14 ENGINEERING PASS (182 checks, 8 packets, 14 refusals) — the source of the baseline's N14 S1 PASS; notes a launch-wrapper defect (zero-byte start.utc/end.utc from missing /usr/bin/date), binary not rerun.
- 0030 `0186_R32_E51T_PAIRED_OPTIMIZATION_STABILITY_AUDIT_PREREG.md` (4307 B): E51T paired-stability audit prereg; cites E51S aggregates (4,195→4,197 known across 48→96→192 sweeps) — consistent, no verdict recorded here.
- 0031 `0187_R33_NATIVE_N06_RESULT.md` (4304 B): N06 S0 PASS — the source of the baseline's N06 figures (377,264 values, 636 fields); adds the caveat that payload-repeat tracking is "not a global scientific freshness audit."
- 0034 `0190_R32_E51AA_RESOURCE_FEASIBLE_TERMINAL_DECOMPOSITION_PREREG.md` (4194 B): E51AA prereg; outcome covered by 0006.
- 0035 `0191_R33_NATIVE_N03_REVIEW_DISPOSITIONS.md` (4159 B): main-agent dispositions of the independent N03 review's R1–R6 findings; "Do not exaggerate the old result into a data leak." Consistent with baseline integrity posture.
- 0038 `0194_R32_E51A_SEQUENTIAL_VALUE_MECHANISM_AUDIT_PREREG.md` (4139 B): E51A prereg; outcome covered by 0049.
- 0047 `0203_R33_NATIVE_N03A_PREREGISTRATION.md` (3915 B): N03A corrective-regression prereg (descriptor normalization); "Do not patch the frozen oracle to convert failure to success." Consistent.
- 0048 `0204_R33_NATIVE_N01B_PREREGISTRATION.md` (3904 B): N01B kernel-timer corrective regression prereg; no outcome recorded in batch.

---

## SUPERSEDED

- 0033 `0189_N13_RESULT_PRE_CLOSEOUT.md` (4251 B, `TNN/TNN/Research/R33_N13_POSTRUN_MEMORY_DIAGNOSIS/N13_RESULT_PRE_CLOSEOUT.md`): earlier revision of the N13 failure record; superseded by 0015 (`0171_R33_NATIVE_N13_RESULT.md`), which adds Euler's terminal postrun review (FAIL_CONSUMED) and the artifact index.

---

## Notes for the coordinator

1. **Archaeology lead**: 0002's "canonical Foundry design in the shadow Zag source" (whole-graph evolutionary PAM search) suggests a PAM-creation mechanism may live in R27-era shadow sources — an unsearched layer worth revisiting given the baseline's "FRAGMENTS ONLY" verdict on PAM designs.
2. **People/codenames anchored**: Euler (N13 reviewer), Leibniz (R33 architecture), Locke (R33 training), Ptolemy (R33 safety), Pauli + Noether + "Sol" (E51AJ external AI reviewer agent names, with UUID agent IDs). ChatGPT Web reviewers used for design/interpretation review.
3. **Dates**: E51 series executed 2026-08-29 → 2026-08-31 (GitHub Actions runs 33277163602 … 33371199421); R33 N-series 2026-09-05 → 2026-09-07; N19 recovery review 2026-09-15; R46 closed 2026-09-17; all docs last modified 2026-09-18 (upload snapshot); E51AI artifact ZIP expires 2026-12-04.
4. **Platform note**: R42/R46 ran on CPython 3.13.12 + NumPy 2.3.5 (macOS arm64), not native Zag — worth keeping distinct from native results if the program later re-runs them.
5. No loud contradictions with BASELINE.md; the only tension is the shadow-source PAM Foundry vs the "no recoverable full PAM design" archaeology verdict (flagged in #1, likely resolvable by checking the shadow layer).
