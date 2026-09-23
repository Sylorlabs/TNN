# tier1_batch1 findings — 52 files read (global indices 52–103)

Note: the batch manifest was repaired in place during the sweep; "local" names below
are the corrected 0052_*–0103_* filenames, all verified by size against the manifest.

## NEW findings (20)

### [1] 0053_DESIGN.md — N12 strict numeric-view engineering design (R33_NATIVE_N12_NUMERIC_VIEWS, PREREVIEW_V1)
- `TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/PREREVIEW_V1/DESIGN.md` · 13,097 B · 2026-09-18
- Verdict: NEW (minor). Fills gap on the recovery-lane numeric interpretation: native Zag
  interpretation of a declared NumPy `frombuffer` REDUCE-descriptor subset (i1–i8/u1–u8/f4/f8/b1,
  explicit endianness), with 100 bit fixtures + refusal codes −9001..−9008. Design rationale: trusted
  read-only inventory over the frozen N10 parent map; empty-view canonical-stride conventions are
  "an explicit bounded N12 convention, not a claim to reconstruct NumPy's" behavior.
  Quote: "Only a REDUCE descriptor for `numpy._core.numeric._frombuffer` ... with exactly four
  positional arguments and no subsequent mutation, is accepted."
- Baseline extension: recovery-lane machinery (N10/N11/N12), beyond the baseline's "FRAGMENTS ONLY" note.

### [2] 0054_R32_E51AJ_REPLAY_ORDER_DOSE_PREREG.md — E51AJ prereg (2026-09-05)
- `TNN/TNN/.scratch/e51aj/.../Research/R32_E51AJ_REPLAY_ORDER_DOSE_PREREG.md` · 12,783 B · 2026-09-05
- Verdict: NEW (minor). Historical design rationale for the replay studies: E51AI completed all 32
  continuing blocks — "Replay lost fewer first-encounter successes than real history without replay,
  including on a supplemental common success set, but did not preserve every prior success." E51AJ
  design: shared-start five-arm (sequential / replay+180 / balanced mix / A-only / frozen) × three
  fresh populations, exact record-multiset matching across 1,101,600 probe-episode rows.
  Quote: "This is a controlled extension, NOT an exact rerun/replication of E51AI: common
  pretraining, anchors and balanced replay scheduling are prospectively different."
- Baseline extension: replay/retention-line history feeding the delayed-credit work.

### [3] 0055_R33_NATIVE_N01B_DESIGN.md — N01B V3 process-supervisor design (compiler-bug diagnoses)
- `TNN/TNN/Research/R33_NATIVE_N01B_BUILD_01/R33_NATIVE_N01B_DESIGN.md` · 12,563 B · 2026-09-18
- Verdict: NEW (strong). Extends baseline's three-bug list with a FOURTH characterized znc defect,
  with source evidence: **imported top-level const lowering defect** — top-level Zag `const` decls are
  "represented as annotated nullary functions... the pinned `7cacbfc0` ARM64 backend lacks that
  handling," so imported refs materialize as function/fat-function values and imported i64 expected
  values arrived as address-like `610473...`. Plus precise detail on the arm64 syscall bug: pinned
  compiler `znc_macos_arm64_7cacbfc0` (source commit `7cacbfc04f6cffec02ea9b1d5ff6702fe2e93f3c`)
  lowered `_zag_clock_monotonic_ms()` to raw Darwin syscall **169** while installed SDK identifies
  `gettimeofday` as syscall **116**. N01B's fix avoids the helper entirely: EVFILT_TIMER deadline
  enforcement + direct syscall 116 for optional measurement.
  Quote: "The two N01A failure modes are distinct and are not treated as one inferred defect."
- Baseline extension: baseline lists hot-path miscompile / wasm breakage / syscall-lowering; this adds
  the imported-const defect as a fourth and pins the syscall-number details (169 vs 116).

### [4] 0056_R32_E51AG_RESULT.md — E51AG result (2026-09-01/04)
- `TNN/TNN/.scratch/e51ah/.../extracted/Research/R32_E51AG_RESULT.md` · 12,503 B · 2026-09-05
- Verdict: NEW (minor). Test result never seen: outcome `CURRENT_RESIDUAL_REPLICATION_STABLE_NEGATIVE`;
  frozen slot+direct union control 5261/5266→5261, 5276, 5271 /5400 on replicas A/B/C vs every learned
  residual arm only 5116, 5143, 5148 /5400. Known gains (+72/+80/+94) consistently outweighed by
  no-unique losses (−217/−213/−217). Closed "the current low-capacity trajectory-critical additive
  residual line as a stable negative." Also a 2026-09-04 diagnostic caveat: the historical oracle
  branch "assigned `success=1` instead of evaluating the selected action," qualifying all oracle-based
  expressivity inferences in E51AE/AG reports.
  Quote: "the current evaluator-blind additive residual representation does not reliably distinguish
  when candidate correction is beneficial from when the mature union should be left unchanged."
- Baseline extension: abandoned direction (trajectory-critical additive residual) + why.

### [5] 0057_DESIGN.md — R33-N17 native R27 continuity qualifier design (2026-09-09 closure)
- `TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/DESIGN.md` · 12,253 B · 2026-09-18
- Verdict: NEW (minor). Success ladder for native R27 continuity: `R27_NATIVE_IDENTITY_RECONFIRMED` →
  `R26_SEMANTIC_DIGEST_REPRODUCED_NATIVE` → `R27_SEMANTIC_DIGEST_REPRODUCED_NATIVE` →
  `R27_REQUIRED_VERIFIER_INVARIANTS_REPRODUCED_NATIVE` → `FULL_NATIVE_R27_CONTINUITY_QUALIFIED`.
  Senses-origins detail: the historical R27 parent inventory contains a **video encoder** (base/basis/mean
  float32), a **speech segmenter** state dict, a **speech_motif_decoder**, an **affordance_model**, and
  **semantic-specialist** identifiers — what the accepted parent's perceptual fields actually were.
  Quote: "A guessed preimage or a literal historical witness would be invalid continuity evidence."
- Baseline extension: what the recovered R27 parent contained on the perceptual side.

### [8] 0060_R32_E51AH_RESULT.md — E51AH result (2026-09-04/05)
- `TNN/TNN/Research/R32_E51AH_RESULT.md` · 10,934 B · 2026-09-18
- Verdict: NEW (minor). Test result never seen: outcome `PRESERVATION_REPLAY_DEVELOPMENT_FAILURE`;
  global replay arm preserved 12,386/12,622 frozen-union successes; local-384 preserved 12,501 and
  rescued 159 but lost 121 prior successes → net +38 development successes, failing the preregistered
  zero-preservation-loss gate. "This is a valid negative for the specified treatment, not an
  infrastructure failure."
- Baseline extension: grounded-preservation-replay abandoned as rescue for the residual line.

### [13] 0065_RESULT.md — R33-N16 support-routing result
- `TNN/TNN/Research/R33_NATIVE_N16_SUPPORT_ROUTING/RESULT.md` · 9,548 B · 2026-09-18
- Verdict: NEW (minor). Test result never seen: full preregistered synthetic N16 qualification,
  independently confirmed; native development selected arm19
  `additive_training_mean_projection_gate_75pct_dual512_preservation_tolerance1`
  (training-input mean-shift projection gate at 75% boundary + dual old-support preservation over
  512 support examples, tolerance1); 210 dev + 144 validation + 144 confirmation = 498
  arm-population exposures. "the strongest synthetic stability/plasticity mechanism result in this
  continuation" — explicitly NOT R27 continuity or a successor claim.
- Baseline extension: N16 specifics (selection + numbers) behind the wave-11 "Arm C" lineage.

### [16] 0068_R33_R27_ORIGINAL_RELEASE_RECOVERY_20260908.md — original R27 release recovered
- `TNN/TNN/Research/R33_R27_ORIGINAL_RELEASE_RECOVERY_20260908.md` · 9,212 B · 2026-09-18
- Verdict: NEW (minor). History anchoring: the original `tnn-pre-v1-r27-general-learning.zip`
  (56,777,645 bytes, SHA256 `7042ff849743c9509586840df865f34423a92f9afc09ef2c7cf937b35b68b65e`)
  was recovered 2026-09-08 from a timestamp-scoped ChatGPT Library metadata listing (Library creation
  2026-08-20T21:43:59Z), superseding the earlier "archive unavailable" conclusion. Contained the full
  r15–r27 source chain, the verification closure, and "a standalone `r27-accepted-state.pkl`, R27
  status/results/handoff documents and the historical category-holdout video."
  Quote: "This supersedes the earlier conclusion that the original `tnn-pre-v1-r27-general-learning`
  archive was unavailable."
- Baseline qualification: "proven unrecoverable" applied to perceptual origins and trace-op semantics,
  not to the archive itself — the archive WAS recovered; semantics stayed unrecoverable.

### [17] 0069_R33_B000_PREREGISTRATION.md — R33-B000 boundary audit (2026-09-05)
- `TNN/TNN/Research/R33_B000_PREREGISTRATION.md` · 9,088 B · 2026-09-18
- Verdict: NEW (minor). Five boundary failures deduced from static audit of prototype sensory helpers,
  preregistered as native diagnostic witnesses: W1 ordering loss in a channel-permutation transform
  ("Ordering loss in this transform, not failure of every vision route"); W2 selected-window
  subsampling loss in an audio-impulse window ("Distances 0, 0, 100"); W3 prototype saturation at
  8,192 emissions; W4 protected-entry selection ("Selecting a protected entry, not demonstrated
  deletion"); W5 bounded chunk truncation with no codebook change. Explicitly "not learner training
  or a sensory/authority certificate."
  Quote: "Do eight exactly copied prototype helpers exhibit the five boundary failures deduced during
  [static audit](R33_SUBSTRATE_AUDIT.md)?"
- Baseline extension: B000 is the earlier boundary-audit layer beneath baseline's B001 (11 component
  bugs) note.

### [25] 0077_DETAILED_REVIEW_WITNESS.txt — independent adversarial review (R33 final integration)
- `TNN/TNN/Research/R33_REMEDIATION_20260915T2152Z/DETAILED_REVIEW_WITNESS.txt` · 8,364 B · 2026-09-18
- Verdict: NEW (minor). Confirms [3]: "Stable compiler's general bare imported constant defect is
  still open." Also records N17 full verifier equivalence blocked on 26 rows "including... video/
  decode/name-resolution behavior" (evidence point behind the unrecoverability call), and the V91
  generation gap: "Fresh oracle runner matches 16 custodied strings but generates 0. ... Oracle lookup
  or historical receipts cannot substitute."
  Quote: "Overall R33 completion: REQUEST_CHANGES. The integrator's explicit incomplete status is
  supported; only the bounded engineering scopes above receive PASS."
- Baseline extension: late (2026-09-15) independent confirmation of the compiler defect + the
  video/decode row blockers.

### [27] 0079_R33_B001_C02_PREREGISTRATION.md — B001-C02 byte-originated record transport
- `TNN/TNN/Research/R33_B001_C02_PREREGISTRATION.md` · 8,289 B · 2026-09-18
- Verdict: NEW (minor). The C02 transport design behind baseline's sensor.zag lineage: `TNNRAW01`
  64-byte header (encoding, channels, rate, width, height, items, payload bytes, clock, ordinal, tick,
  timebase, source — 12 unsigned LE32 words); encoding1 = interleaved PCM16LE, encoding2 = packed
  RGB8; `TNNSNP01` snapshot format; 48-process schedule (capture/reload/continuation/snapshot-overlap
  controls). Design rationale quotes: "This is a file transport component, not a physical
  microphone/camera, integrated learner input, full S0/S1/S2 gate..." and "No outcome-driven fixture
  tuning is permitted after the primary run." BUILD_01/02 failed; BUILD_03/04 compiled; main-agent
  semantic review found a metadata read-after-overlapping-copy and fixed it pre-registration; the
  independent review dispatched to Galileo returned a terminal rate-limit error with no verdict.
- Baseline extension: the transport layer that preceded sensor.zag's byte-originated ingress.

### [28] 0080_R33_BIRTH_SUBSTRATE_HARDCODING_PLAN.md — birth-substrate hardcoding audit (PAM fragments)
- `TNN/TNN/Research/R33_BIRTH_SUBSTRATE_HARDCODING_PLAN.md` · 8,165 B · 2026-09-18
- Verdict: NEW (strong). The audit inventory of `tnn_r32_epistemic_chunking.zag` capability families
  is the most concrete PAM/vision/audio-origin record in this batch — actual design fragments:
  **Acoustic templates** (350–386): "32 motifs, width12, duration penalty×3, monotone decoding/collapse —
  Architecture prior; anonymous IDs require demonstrated learned origin; no claim of raw waveform
  equivalence"; **Segment/local temporal PAM** (1413–1543): "Reset accumulator, max/mean pooling,
  fixed-point rectified kernels, score-based shadow decision"; **Visual identity** (256–322): "Eight
  channels, invariant transform, fixed distance/continuity weights and merge/split thresholds —
  Representation/behavioral prior, not neutral raw I/O; optional audited arm only."
  Also: five-arm tournament plan (A minimal safe substrate … E learning from consequences) — "the
  objective is not minimal hardcoding at any cost."
  Quote: "Function names such as 'learned' are not evidence."
- Baseline extension: baseline says R32 acoustic PAMs were DROPPED (GRU/segmental .pt machinery) and
  the senses archaeology found FRAGMENTS ONLY — these ARE the fragments, with the audit rationale
  for why they were treated as priors, not learned perception.

### [31] 0083_TNN_R28_AEIF_RESULTS.md — R28 AEIF no-graph rebuild results (2026-08-23)
- `TNN/TNN/Research/TNN_R28_AEIF_RESULTS.md` · 8,014 B · 2026-08-23
- Verdict: NEW (strong). Test results never seen + abandoned-direction rationale:
  (a) AEIF (Associative Episodic Identity Fabric) retires graph state as identity authority:
  no-graph `AE_ACTIVE` 93.57% vs graph-authority `G_ACTIVE/G_ALL` 80.71% (30% floor, "classified as
  plateauing"); meta-search selected graph authority only 16.67% of the time.
  (b) Dose sweep peak at **256 examples/entity**; 512/1,024 caused "interference/overconsolidation
  rather than further learning."
  (c) Memory policy: user-selected default heuristic with TNN override (72.30% exact-detail queries,
  utility 0.6670) — the direct ancestor of the force-pin/override law; "LRU is eviction mechanics only."
  (d) **Connected speech — unresolved boundary** (the main capability blocker): earlier CTC 0% was an
  invalid split (discarded); after fixing acoustic identity across splits CTC "collapsed to blank
  outputs despite falling loss"; negative blank bias → only 2.9% token accuracy; isolated acoustic
  pretraining 91.81% yet CTC fine-tuning 5.14% → "CTC remains rejected in its current formulation";
  hard connected speech 22.08%. R28 NOT promoted: "the new Zag source has not been natively
  compiled/executed in this environment and hard connected speech remains unsolved."
  Quote: "The peak is **256 examples/entity**. Increasing to 512/1,024 caused
  interference/overconsolidation rather than further learning. This is evidence against treating low
  scores as automatically undertraining."
- Baseline extension: none of the AEIF results, dose-sweep knee, CTC-collapse diagnostics, or the
  memory-default rationale is in the baseline.

### [36] 0088_R32_E51AD_RESULT.md — E51AD router result (2026-08-31)
- `TNN/TNN/Research/R32_E51AD_RESULT.md` · 7,725 B · 2026-09-18
- Verdict: NEW (minor). Test result never seen: native result VALID NEGATIVE —
  `TRAJECTORY_ROUTER_NO_GAIN`; later deterministic reproduction byte- and ledger-identical.
  Quote (from frozen decision rules): every learned arm preserved all 12,334 development PRESERVE
  trajectories, yet no learned router beat the frozen union control on validation.
- Baseline extension: E51AD line closed as negative (router can't beat score-max union).

### [37] 0089_R33_PARENT_SOURCE_RECOVERY_ARCHIVE_INSPECTION_20260906.md — nested archive inspection
- `TNN/TNN/Research/R33_PARENT_SOURCE_RECOVERY_ARCHIVE_INSPECTION_20260906.md` · 7,645 B · 2026-09-18
- Verdict: NEW (minor). History anchoring: full backup `TNN_COMPLETE_R1_R32_FULL_BACKUP.tar.gz`
  (SHA256 `f966c0c7f1649feb1e83436b21d7c51a41442e8a9f3f4f41c33f08affbb3d748`) contains nested
  shadow bundles whose names reveal release lines baseline never mentions: `tnn-r30-big-boom-shadow`
  (R30 "big-boom") and `tnn-r31-endogenous-chunking-shadow` (R31 "endogenous chunking"). Also R28
  shadow policy metadata: active promotion `STRONGER_MASTER_GENERAL_SPECIFIC_BRIDGE`, retained
  R26/R25/R23 mechanisms, rolled-back proposals, shadow partials, locked gates.
  Quote: "The policy records the active promotion `STRONGER_MASTER_GENERAL_SPECIFIC_BRIDGE`,
  retained R26/R25/R23 mechanisms, rolled-back proposals, shadow partials, and locked gates."
- Baseline extension: R30/R31 release names; R28 promotion-policy record. (Source-availability status
  superseded by [16].)

### [41] 0093_ARCHITECTURE_ASSESSMENT.md — continuing-learner architecture assessment (2026-09-12)
- `TNN/TNN/Research/R33_CONTINUING_LIFE_V1/ARCHITECTURE_ASSESSMENT.md` · 7,523 B · 2026-09-18
- Verdict: NEW (minor). Honest structural verdict from late in the R33 campaign: "the repository
  contains several qualified or partially qualified mechanisms, but no native, behaviorally continuous
  R27 learner wired through the full observation, memory, hypothesis, action, consequence, and update
  loop." The missing path is named "the decisive limitation":
  "experience -> learner-owned memory/hypothesis change -> selected action -> attributed consequence
  -> native learner update -> preserved reload."
  Also an evidence-map row for "Encoded sensory transport: N14 is a consumed bounded PCM16LE/RGB8
  information-preservation pass — Physical microphone/camera transport, timing qualification, semantic
  perception, and changed-condition learning remain open."
- Baseline extension: explicit contemporary evidence-map / ownership-of-decisions framing.

### [42] 0094_R32_E51AE_RESULT.md — E51AE result (corrected authoritative, 2026-09-04)
- `TNN/TNN/Research/R32_E51AE_RESULT.md` · 7,475 B · 2026-09-18
- Verdict: NEW (minor). Test result never seen: outcome `TRAJECTORY_CANDIDATE_RESIDUAL_NO_RESCUE`;
  frozen union control 5260/5400 vs each learned residual arm 5132/5400; all learned arms failed the
  development preservation gate (12,135/12,644 preserved, gate 0) before validation. Correction note:
  supersedes a stale result text "assembled from stale handoff numbers and did not match the preserved
  Actions artifact," plus the oracle scoring caveat.
  Quote: "E51AE is a valid negative learned-treatment result."
- Baseline extension: E51AE numbers + the stale-handoff correction discipline.

### [44] 0096_R32_E51AB_DIRECT_CANDIDATE_COMMIT_PREREG.md — E51AB prereg (2026-08-30/31)
- `TNN/TNN/Research/R32_E51AB_DIRECT_CANDIDATE_COMMIT_PREREG.md` · 7,307 B · 2026-09-18
- Verdict: NEW (minor). Design rationale for the COMMIT(candidate) interface: E51AA "decomposed the
  resource-feasible terminal veto and proved that the existing shared commit-vs-UNKNOWN scalar cannot
  be a complete repair. On fresh stage 88, 48 known trajectories had **no grounded-correct
  KEEP/CURRENT/RESTORE action anywhere in the resource-feasible prefix**, and one additional
  trajectory had a correct feasible action that was never the frozen top commit."
  Quote: "This failure follows from coupling terminal reporting to already-materialized
  `initial/current/prior` belief-state slots."
- Baseline extension: why the direct-candidate interface replaced belief-slot terminal reporting.

### [46] 0098_R33_PRESERVATION_LEARNING_PLAN.md — preservation-learning plan (post-E51AJ reconciliation)
- `TNN/TNN/Research/R33_PRESERVATION_LEARNING_PLAN.md` · 7,259 B · 2026-09-18
- Verdict: NEW (minor). Carries the **E51AJ result numbers** (never seen in baseline): completed
  three-population diagnostic — "Replay reduced ever-lost and worst simultaneous losses in all three
  populations, but final old-success losses were sequential 1/9/17 versus replay 14/11/6. A-only
  continuation lost 19/19/11 prior successes, including losses in its own A cohort. The frozen fork
  lost none. `no_final_behavioral_tradeoff` was false." Also: E51AD's best router was "29 validation
  trajectories below score-max." New experimental question framed as "longitudinal update
  preservation at fixed support."
  Quote: "This is mixed evidence, not a replay cure and not a proof that switching alone caused
  forgetting."
- Baseline extension: E51AJ/E51AD quantitative outcomes.

### [48] 0100_TNN_NEXT_RUN_ARCHITECTURE_PLAN.md — R31 endogenous-chunking handoff plan (2026-08-23)
- `TNN/TNN/Research/TNN_NEXT_RUN_ARCHITECTURE_PLAN.md` · 7,203 B · 2026-08-23
- Verdict: NEW (strong). The R31 program plan — design rationale and abandoned-direction gold:
  "R31 should begin by correcting R30's speech abstraction. The main question is no longer how
  accurately TNN predicts an externally fixed motif/token sequence. The question is whether TNN can
  discover useful temporal chunks directly from raw sensory streams and use those chunks for
  grounding, prediction, memory, communication, and action."
  Binding constraints: no transformers/LLM wrappers/BPE/fixed tokenizer/next-token objective;
  "Human word/phoneme/boundary annotations are evaluator-only microscopes"; no supplied VAD or
  speech boundaries; no graph cognition; promotable mechanisms execute in native Zag; zero newborn
  restart; "Any exact 0%/100% result triggers the extreme-score diagnostic battery."
  Adaptive Motif lineage to port: motif confidence, motif-gated temporal workspace, Grounded
  Contrastive Schema Memory, support-gap recruitment, reversible longest-match cells,
  context-indexed exact spans, shadow replay, rollback; evidence: "chunks frequently cross human
  boundaries; held-out raw-stream compression without information loss."
  13-variant acoustic self-chunking tournament from raw waveform (fixed anonymous CTC inventory as
  control only); Phase 4 chunk ops (extend/shorten/split/merge/overlap/specialize/hierarchical/
  decay/archive/restore); Phase 8 cross-modal chunk emergence (acoustic/visual/action/multimodal);
  Phase 9: "Let TNN create new non-core chunking PAMs from generic primitives"; Phase 10 promotion
  bar: "no hidden tokenizer/VAD/boundary leakage."
- Baseline extension: the R31 endogenous-chunking direction (matches the `tnn-r31-endogenous-chunking`
  shadow bundle from [37]); explicit rejection rationale for R30's fixed-motif/token abstraction and
  for externally supplied linguistic units — the anti-LLM/anti-BPE architecture stance in writing.

## CONFIRMS (2)

- [30] 0082_README.md (`.../V92_STATE_IMAGE_QUAL/README.md` · 8,026 B · 2026-09-18): V92 qualification
  (339 selftest checks pass, 245472/245536-byte contracts) — one line: restates the reviewer-witness
  blocker state (N17 26 source-row deficits; V91 native generation 0/16; R33 incomplete).
- [32] 0084_R32_E48_ONLINE_BATCH_REPRESENTATION_PREREGISTRATION.md
  (`TNN/TNN/Research/R32_E48_ONLINE_BATCH_REPRESENTATION_PREREGISTRATION.md` · 7,890 B · 2026-08-28):
  one line: E48 executed as a valid native negative (`NO_TESTED_BATCH_SAFETY_RESCUE`, batch baseline
  346/1020 and batch joint 318/1020 no-unique cells) — one of baseline's "four valid negatives."

## SUPERSEDED (1)

- [9] 0061_PREREGISTRATION.md (`TNN/TNN/Research/R33_NATIVE_N07_AUTHORITY/PREREGISTRATION.md` · 10,378 B ·
  2026-09-18): R33-N07 authenticated-control-ledger design (HMAC, 128-byte policy, 224-byte requests,
  strictly increasing 31-bit nonce, operations replace/restrict) — one line: precursor design,
  superseded by the shipped authority (OS-level channel binding, overseer 117/117).

## NOISE (29)

- [0] 0052_CLOSEOUT_VERIFIED.txt · 13,190 B · 2026-09-18: SHA-verify checklist for the N17 lane-B audit
  (all entries OK) — procedural, no content.
- [6] 0058_R32_E51_EXECUTION_JOURNAL.md · 12,132 B · 2026-09-05: E51 execution journal — procedural;
  duplicates the E51AG result; only date/repo anchors (2026-08-31 activation, `/Users/Shared/micah/
  Documents/TNN/TNN`, branch `r32-agent-sequential-frontier`).
- [7] 0059_README.txt · 11,653 B · 2026-09-17: CPython idlelib README (bundled runtime) — irrelevant.
- [10] 0062_PREREGISTRATION.md · 9,937 B · 2026-09-18: R33-N10 inert parent-map prereg — recovery lane.
- [11] 0063_PREREGISTRATION.md · 9,772 B · 2026-09-18: R33-N13 torch-views prereg — recovery lane.
- [12] 0064_R32_E51AI_LONGITUDINAL_CONTEXT_PREREG.md · 9,647 B · 2026-09-05: E51AI prereg — procedural.
- [14] 0066_R32_E51AE_TRAJECTORY_CRITICAL_CANDIDATE_RESIDUAL_PREREG.md · 9,454 B · 2026-09-18: E51AE
  prereg — superseded by its result [42].
- [15] 0067_PREREGISTRATION.md · 9,241 B · 2026-09-18: R33-N09 anchored-checkpoint prereg — authority lane.
- [18] 0070_DESIGN.md · 8,900 B · 2026-09-18: R33-N13A fingerprint-scratch design — recovery lane.
- [19] 0071_PREREGISTRATION.md · 8,815 B · 2026-09-18: R33-N13A prereg — recovery lane.
- [20] 0072_PREREGISTRATION.md · 8,806 B · 2026-09-18: R33-N11 parent-custody prereg — recovery lane.
- [21] 0073_R32_E51AD_TRAJECTORY_CRITICAL_ROUTER_PREREG.md · 8,419 B · 2026-09-18: E51AD prereg —
  superseded by its result [36].
- [22] 0074_PREREGISTRATION.md · 8,397 B · 2026-09-18: R33-N05A durable-telemetry prereg — infrastructure.
- [23] 0075_R33_NATIVE_N01A_DESIGN.md · 8,395 B · 2026-09-18: R33-N01A supervisor V2 design — infrastructure.
- [24] 0076_R32_E51Z_STOPPING_STATE_ORACLE_AUDIT_PREREG.md · 8,379 B · 2026-09-18: E51Z prereg — procedural.
- [26] 0078_REVIEWER_REQUEST_CHANGES.md · 8,364 B · 2026-09-18: byte-identical duplicate of [25].
- [29] 0081_R32_E51AH_GROUNDED_PRESERVATION_REPLAY_PREREG.md · 8,065 B · 2026-09-05: E51AH prereg —
  superseded by its result [8].
- [33] 0085_N19_LANE_REVIEW.witness.md · 7,728 B · 2026-09-18: N19 lane-C review — runtime boundary;
  md5-identical to [34]/[35].
- [34] 0086_c_review.md · 7,728 B · 2026-09-18: duplicate of [33] (md5 match).
- [35] 0087_INDEPENDENT_REVIEW.md · 7,728 B · 2026-09-18: duplicate of [33] (md5 match).
- [38] 0090_INDEPENDENT_REVIEW.md · 7,594 B · 2026-09-18: lane-C independent N19 review — runtime boundary.
- [39] 0091_N19_INDEPENDENT_REVIEW_V3.md · 7,565 B · 2026-09-18: N19 review V3 — md5-identical to [40].
- [40] 0092_INDEPENDENT_REVIEW_V3.md · 7,565 B · 2026-09-18: duplicate of [39].
- [43] 0095_R32_E51AG_CURRENT_RESIDUAL_REPLICATION_PREREG.md · 7,411 B · 2026-09-18: E51AG prereg —
  superseded by its result [4].
- [45] 0097_PREREGISTRATION.md · 7,283 B · 2026-09-18: R33-N16 prereg — superseded by its result [13].
- [47] 0099_R32_E51N_CALIBRATION_FRONTIER_REPLICATION_PREREG.md · 7,230 B · 2026-09-18: E51N prereg —
  procedural.
- [49] 0101_R32_E51O_LOCAL_CALIBRATION_MEMORY_PREREG.md · 7,197 B · 2026-09-18: E51O prereg — procedural
  (notes E51D/E/F/G-L evidence basis only).
- [50] 0102_REVIEWER_DETAILED_REQUESTS.log.txt · 7,182 B · 2026-09-18: duplicate content of [25] plus
  trailing shell junk (`EOF`, `ruby <<'RUBY'`).
- [51] 0103_R32_E51Y_FIVE_WAY_SEQUENTIAL_POLICY_PREREG.md · 7,167 B · 2026-09-18: E51Y prereg — procedural.

## Cross-cutting observations

1. **No koryphaios/ghost mentions** in any of the 52 files (case-insensitive grep over the full set).
2. **No loud contradictions** with the baseline. One extension worth flagging: the baseline's znc
   bug list ("hot-path miscompile ZNC-2026-09-19-001, wasm codegen breakage, arm64 syscall-lowering
   dropping the syscall number") gains a FOURTH characterized defect — the ARM64 imported-top-level-
   const lowering bug (N01B design [3], confirmed still open by the 2026-09-15 adversarial review [25]).
3. Date anchors: R28 AEIF + R31 handoff both 2026-08-23; E51AD/AE/AG/AH/O/Y preregs 2026-08-30/31;
   E51AD executed 2026-08-31; E51AH executed 2026-09-04/05; E51AJ prereg 2026-09-05; R27 source recovery
   2026-09-06 (nested archives) → 2026-09-08 (original ZIP from ChatGPT Library); architecture
   assessment 2026-09-12; adversarial reviews 2026-09-15; Drive copies modified 2026-09-18.
4. The oracle-scoring caveat recurs across E51AE [42], E51AG [4], and E51AH [29] reports: the historical
   evaluator-only oracle assigned `success=1` instead of scoring its selected action — qualified as
   caveat on expressivity inferences only, not on the learned-arm comparisons or the negative outcomes.
5. Release-line names surfaced: R27 (canonical) → R28 AEIF (no-graph rebuild, not promoted) →
   R30 "big-boom" → R31 "endogenous chunking" → R32 → R33. Only names + the R31 plan are recovered for
   R30/R31; no code or results.
