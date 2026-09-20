# tier2_batch3 findings — 114 files skimmed

Scope note: the manifest's `local` filenames did not exist on disk; the numeric prefixes
0416–0529 matched exactly 114 actual files in `docs_local/`. Those files were reviewed.

## NEW findings

### 1. The program's standing laws come from a dated 40-preference file (design rationale, dated anchors)
**Doc:** `0422_TNN_USER_RESEARCH_PREFERENCES.md` — "TNN User Research Preferences", last updated 2026-08-20, numbered preferences 1–40 with dated update rows (2026-08-20 / 08-21 / 08-23 / 09-05).
Fills: rationale behind the standing laws; extends baseline's condensed rules with the operational consequences Micah actually set.
Verbatim: "Preference: When a result is weak, first determine whether the failure is caused by insufficient data, poor lesson quality, missing contrasts, bad curriculum ordering, inadequate rehearsal, or a weak teacher. Change architecture only when the learning curve or error structure shows that training is no longer the main bottleneck." (training-first diagnosis #3)
Verbatim (2026-09-05): "This supersedes earlier permissions for Python external glue. New cognition, learning, telemetry, recovery, supervision and evaluation code must be Zag."
Also NEW: #38 "Consciousness is a project goal/research lane, not a current capability claim" — the user wants TNN to pursue consciousness; #23 graph retirement — "Large context-switching architecture replacements are acceptable and desirable when evidence indicates the current substrate constrains capability"; #32 UNKNOWN as structured epistemic state; #19 `INNATE_SYSTEM_FLUENCY` arm; #37 equal-fighting-chance comparisons with scaling curves/Pareto fronts.

### 2. R31 quantitative results and the user's self-chunking correction (test results never seen)
**Doc:** `0447_TNN_USER_RESPONSE_LOG.md` — user guidance log, 2026-08-20 through 2026-08-23.
Fills: test results + rationale never in baseline (baseline only names r31-endogenous-chunking as a shadow).
Verbatim: "Causal ablation rejected chunk-only sensory cognition: chunk-only hard grounding ~0.753 while raw-active ~0.921; dual-active preserved ~0.921 hard grounding while retaining ~0.852 compression gain and slightly improving near-twin discrimination."
Verbatim: "Support-gap acoustic recruitment is strong in the reference battery (~0.89–0.92 hard after only 1–16 grounded exposures) but clean 1.0 scores are quarantined as suspicious."
Also: recovered Adaptive Motif evidence — "compressed a 33,450-unit held-out raw stream to 2,789 learned units with exact round-trip"; regime memory "reduced context-model thrashing from ~2,147 switches to ~13"; E45–E48 native discriminator results (E48 outcome `NO_TESTED_BATCH_SAFETY_RESCUE`, 346/1,020 safe cells baseline vs 318/1,020 joint); V44 frontier identified as "option completion after initiation" failure; and the user's instruction "Do not store TNN project details in universal memory; keep them in project-local cloud files" (explains the whole Drive/local-file organization).

### 3. Acoustic PAM head-to-head numbers on seeds 35000/35200 (PAM history)
**Docs:** `0465_R32_COMPACT_HANDOFF_CURRENT.md`, `0458_NEXT_AGENT_START_HERE.md`.
Fills: specific PAM benchmark results never in baseline (baseline mentions R32 V39 GRU PAM but no scores).
Verbatim: "- seed 35000 temporal convolution raw-temporal PAM: overall 0.8409, hard mean 0.8559; - same seed segmental recurrent / learned-boundary PAM: overall 0.7917, hard mean 0.7928. - seed 35200 temporal convolution: overall 0.9104, hard mean 0.9235."
Design rationale drawn at the time: "Interpretation: the current learned segmentation gate is probably throwing away useful temporal evidence. **Do not force boundary decisions into the core sensory route.**"
Also NEW: v2 decision-policy overcorrection — "On seed 35400 it achieved `ambiguous_unknown_rate=1.0`, which is automatically suspicious, while resolvable correctness fell to roughly 0.22–0.48 across hostile conditions" — with the corrective rule "Train the decision policy only from delayed utility/regret."

### 4. R31 dual-route decision (design rationale)
**Doc:** `0478_R31_FINAL_REPORT.md` — "R31 Endogenous Chunking — Final Shadow Research Report".
Fills: rationale for the dual-route sensory architecture; contradicts nothing (statuses match baseline's shadow-only framing).
Verbatim: "**Decision:** self-chunking is retained as a compression/indexing/grounded-construction/memory route, but it must not erase or replace raw episodic evidence. The dual route preserves essentially all raw hard capability while keeping ~85% compression gain and slightly improving near-twin discrimination."
Verbatim: "**Decision:** do not add more generic threshold/budget layers in R31. The open problem is a richer representation of epistemic instability/no-unique-answer over time, not another probe-count heuristic."
Status note: R31 is explicitly `SHADOW / REFERENCE_ONLY` because "this runtime could not materialize or execute a usable `znc` compiler."

### 5. R30 long-training rationale + extreme-score policy evidence (design rationale + test numbers)
**Doc:** `0485_R30_FINAL_REPORT.md` — "R30 Big Boom — Final Shadow Research Report".
Fills: rationale behind "long developmental training curves before blaming architecture" + numbers baseline lacks.
Verbatim: "The central R30 speech finding is causal: **long training transformed a total-looking failure into high-90s bounded performance without replacing the core CTC architecture.**" (no-VAD speech: exact 0% at 1,024 utterances → 96.56% hard exact-sequence accuracy at 100,000 utterances)
Verbatim: "names: 100% — quarantined as evaluator saturation"; "LRU-as-representation: **0%*** exact recall"; episodic "full episodic passive: 56.05%" vs "one-view + active: 75.60%".

### 6. TNN autonomy position — decision-ownership framing + A0–A5 ladder (design rationale)
**Doc:** `0525_TNN_AUTONOMY_POSITION.md`.
Fills: rationale not present in baseline (baseline's phases are 0→1 trainer gate; this is the autonomy doctrine).
Verbatim: "TNN should become more autonomous in deciding **how to learn**, not in silently deciding what it is allowed to do."
Autonomy ladder A0 (passive) → A5 (developmental learner); anti-facade tests ("the system cannot state what evidence would change its decision"). Explicit caveat: "This is a design position, not a claim that current TNN has achieved these levels."

### 7. R32→R27 promotion rule: Pareto-style capability dominance (design rationale)
**Doc:** `0480_R32_R27_DOMINANCE_PROGRAM.md`, dated 2026-08-29.
Fills: the actual promotion criterion Micah set, never stated in baseline.
Verbatim: "R32 does not replace R27 because it has more mechanisms or a better average score. Promotion requires **Pareto-style capability dominance**: preserve the accepted R27 substrate and regression battery, add general capabilities R27 lacks, and demonstrate that the improvements survive fresh native qualification without evaluator leakage, newborn restart, or researcher-written domain policy."
Also: Phase 8 "Autonomous non-core PAM Foundry" — matches the autonomous-PAM preference (#12 in item 1).

### 8. R36–R46 state-conditioned reliability campaign: all NO-GOs, interference conclusion (test results never seen)
**Doc:** `0507_SESSION_FINDING_SNAPSHOT.md` (duplicated in `0508_TNN_SESSION_FINDING_20260917_STATE_CONDITIONED_RELIABILITY.md`), dated 2026-09-17.
Fills: a whole campaign baseline never mentions (R36–R46, 120+120+60+60 preregistered development jobs).
Verbatim: "The remaining problem is not solved by progressively finer scalar reliability memories or by one continuously learned additive residual surface." R40, R41, R42, R46 all development NO-GO; `selected_for_fresh = null` for both R42 and R46. Central R46 result: "local-gain/global-interference pattern" — `latent_balanced` improved cost recurrence but "simultaneously worsened overall regret, post-change regret, unseen pairing, and cross-noise."

### 9. M0–M7 authority milestone ladder (spec origins)
**Doc:** `0519_R33_AUTHORITY_MILESTONE_LADDER.md`.
Fills: the milestone-gated autonomy spec — extends baseline's phase gates with the detailed ladder.
Verbatim: "| M5 | Learned architecture-proposal policy | Experiment-history provenance, held-out failure-family improvement versus random/evolution; search cost counted |" — note the "vs random/evolution" no-free-lunch clause baked into the milestone. M7: "Integrated high-autonomy development ... not a consciousness certificate."

### 10. TNN naming taxonomy (design framing)
**Doc:** `0520_TNN_CATEGORY_COMPARISON.md`.
Fills: naming/identity framing the baseline only implies.
Verbatim: 'Canonical name: **TNN = True Neural Network**. "Grounded, Active, Non-Token Cognition" describes the direction; it is not the acronym expansion.' Classification: "hybrid continual cognitive architecture or developmental neural architecture"; "Its proposed differentiator is the **integration and ownership model**, not the [benchmark accuracy]."

### 11. Explicit claim-boundary rule: TNN vs LLMs (design rationale)
**Doc:** `0479_TNN_FRONTIER_MASTER_HANDOFF_20260915.md` — frontier master handoff R33/R34, 2026-09-15.
Fills: the documented honest-claims boundary (operationalizes preference #9 in item 1).
Verbatim: "Current evidence does not support a claim that TNN beats LLMs, beats transformers generally, reaches AGI, or wins 90% of capability categories. No equal-comparison benchmark suite establishing those conclusions exists yet."
Also: authoritative closeout "remains fail-closed overall: `R33_FINAL_CLOSEOUT.json` reports `r33_complete=false`" and the pass list (V68/V71/V73/V92 PASS).

### 12. N16 arm-selection smoke-test history (design rationale for N16 arm 19)
**Doc:** `0518_AUTHORING_HISTORY.md` — R33-N16 authoring history.
Fills: why the N16 support-routing family ended at the 21-arm matrix with arm 19 selected (baseline only records the validated result).
Verbatim: "Most notably, arm19 (75-percent projection plus dual512 preservation tolerance1) retained old_lost2 while gaining262 new successes, with anchor_loss1. This is authoring evidence only; it is not development or validation."
Documents the smoke progression: four-cluster → eight-cluster routing, occupancy veto family, then input-only projection discriminant family; Smoke06/07 reproduced byte-for-byte; V1/V2 independent pre-run reviews returned `REQUEST_CHANGES` on declaration/attribution mismatches only (no learner-runtime failure), with all binaries byte-identical across rebuilds.

### 13. Trainer-interface explanation rule (design rationale)
**Doc:** `0511_R33_TRAINER_INTERFACE_AND_TELEMETRY.md`.
Fills: rationale for how TNN explanations must be built.
Verbatim: "Generated prose may paraphrase cited records, but cannot invent a rationale. When the causal chain is incomplete, display the missing link."

### 14. E51AF permanently invalid + E51AJ per-replica retention tables (test results, partial)
**Docs:** `0501_R32_E51AC_AH_ARC_REPORT.md`, `0512_TABLES.md`.
Extends baseline's E51AJ one-liners with: E51AF "Historical source/ledger prerequisites did not match. The instance is permanently invalid"; E51AJ primary retention table (e.g. replica 0: 2091 shared successes, sequential/replay losses 1/14, ever-lost 31/24, retention direction "no").
Minor NEW — baseline has E51AJ outcome summary; these are the detailed receipts.

### 15. N17 blocker inventory specifics (senses archaeology detail)
**Doc:** `0464_R33_N17_BLOCKER_INVENTORY_20260918.md` — 2026-09-18, "26 rows remain fail-closed: 5 R27 and 21 R26".
Extends baseline's "FRAGMENTS ONLY" with specifics: R27-08/-09 — serialized model/centroid/df/docs bytes exist but "complete inference semantics and SOCIAL_NEAR/SOCIAL_FAR examples, labels, evaluation and tie rules are not admitted"; R26-08/-09 — "Original video path, hash and artifact bytes not admitted; no listed local media candidate" (no decoder/frame semantics, so no decoded-frame-count equivalent); R26-16 — name-memory "true_to_node[0] answer mapping" missing; R26-38 — original R26 policy absent, "Seven individual gate results cannot be inferred from a different R27 policy."

### 16. Continuing-life worklog dates (history anchoring, minor)
**Docs:** `0477/0488/0497_WORKLOG.md`.
Fills: user-authorized continuing-life implementation ran 2026-09-11/12, native Zag only; `ENGINEERING_06` run passed all five children; V71/V92 passed, V68 still failing. Minor anchoring.

## CONTRADICTIONS with baseline: none found.
Notes checked and cleared: `0521_VERIFY_CONTRACT.md`'s "R26/R27 NATIVE SEMANTIC-DIGEST CONTINUITY PASS" concerns verifier-source decomposition (33-check matrix), not the behavioral recovery efforts the baseline marks unrecoverable — different artifacts, no conflict. The `ghost` hit in `0476_AUTHORS.txt` is a Python contributor username, not the ghost project. koryphaios appears only as a filesystem search scope in candidate lists — consistent with memory.

## CONFIRMS / NOISE (one line each)
- 0416, 0436 candidates lists — recovery search scopes incl. koryphaios paths; NOISE (path names only).
- 0417/0418/0419/0420/0426/0428/0430/0431/0432/0434/0445/0449/0450 R33_HANDOFF variants; 0439/0440/0441/0443/0452/0457/0458 NEXT_AGENT_START_HERE; 0442/0446 roadmap matrix — CONFIRMS baseline R33 narrative (N13/N13A/N14 closeouts, N16 arm19, parent-recovery fail-closed, E51AJ frontier).
- 0421 News3.txt, 0435 NEWS2x.txt, 0483 HISTORY.txt, 0496 TODO.txt — Python/IDLE docs; NOISE.
- 0423/0460/0466 LICENSE.txt, 0476 AUTHORS.txt, 0457 vendor.txt, 0474/0500 entry_points.txt — vendored package files; NOISE.
- 0424 exact_size_hashes, 0427 hash_verification, 0437/0438/0444/0451/0453/0454/0456/0459/0461/0462/0463/0467/0468/0469/0470/0471/0490/0491/0492/0513/0514/0515/0516 artifact-verified/pins — bookkeeping; NOISE.
- 0425 SOURCE_DIFFS — R25 release-identity gate diff; NOISE.
- 0429 INDEPENDENT_ORACLES — N13 oracle authorship, not executed; CONFIRMS honest-discipline baseline.
- 0473/0484/0487/0498/0500/0503/0504 commands.txt — znc compile/invocation logs; NOISE (paths confirm compiler location).
- 0474/0502 R32 hand/charter E51 — CONFIRMS baseline frontier framing; 0522 E45 wide-call audit — bookkeeping detail, NOISE.
- 0448/0455/0475/0495/0486/0524 parent recovery docs; 0494 lane_n17_final; 0529 final report; 0510 remediation; 0521 verify contract — CONFIRMS baseline R27-recovery-blocked story.
- 0499 V38 autocontinue status — process log; NOISE.
- 0506 R31 handoff — CONFIRMS no-transformer/tokenizer/graph constraints.
- 0508 — duplicate of 0507 (deduped).
- 0517 N18 sidecar contract, 0527 execution board, 0528 E51AI validation — CONFIRMS/blockers unchanged; 0493 E51 causal map — CONFIRMS E51AJ numbers.
- 0505 LANE A report — V68/V73 repair closed by narrow source fix; CONFIRMS 0479's pass list.
