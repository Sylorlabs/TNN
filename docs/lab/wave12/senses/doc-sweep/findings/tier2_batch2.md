# Tier2 Batch 2 findings — doc sweep skim

Batch: `batches/tier2_batch2.json` (114 entries). Drive `TNN/TNN/Research/...`.
**Important:** the batch manifest's `local` field is STALE (indexes into a different
download order). All local files below were resolved via `manifest.json` by matching
`drive_path` — true locals are the `06xx/07xx_` names shown. `/tmp/tier2b_map.json` has the full batch→local mapping.

Read the baseline at `../BASELINE.md` first. Coverage: 114 files skimmed
(head content + keyword pass), 16 read fully.

## NEW findings (14)

### NEW-1 — Pre-v1 R5: the PAM/vision/audio-era sensory architecture choice
- Doc: `0712_tnn-pre-v1-r5-STATUS.md` | Drive `TNN/TNN/Research/tnn-pre-v1-r5-STATUS.md` | 1142 bytes | 2026-08-23
- The old program ran a **broad variation tournament** and the R5 winner was documented:
- Quote:
  ```
  CONTROLLED_TRAINING_WINNER           NOISY_THEN_CLEAN_MULTIMODAL
  LARGE_BUDGET_NEAR_TIE                MIXED_ALL_FROM_BIRTH
  SELECTED_SENSORY_ARCHITECTURE        RECURRENT_PAM_HYBRID_AUDIO
  ```
- Also `SELECTED_DISCOURSE_MECHANISM = MOTIF_GATED_TEMPORAL_WORKSPACE`, explicit
  `FIXED_TOKENIZER 0`, `LLM_OR_TRANSFORMER_WRAPPER 0`, heldout scores 0.9700 /
  0.9617 / 0.9708, one-shot cross-frame 0.3125, and TEENAGER/ADULT_ENGLISH +
  NATURAL_VIDEO_AUDIO all `NOT_MET`.
- Extends baseline: first recovered record of how the old PAM-based sensory
  architecture was *chosen* (tournament, not default) and that no-fixed-tokenizer /
  no-LLM-wrapper was already a documented constraint at pre-v1 R5.

### NEW-2 — Pre-v1 R6: bounded self-architecture revision (RSI) detailed results
- Doc: `0654_tnn-pre-v1-r6-rsi-STATUS.md` | Drive `TNN/TNN/Research/tnn-pre-v1-r6-rsi-STATUS.md` | 1746 bytes | 2026-08-23
- Fills baseline's "pre-v1 RSI self-architecture revision note" with the actual numbers:
- Quote:
  ```
  FIRST_SCHEMA_REVISION                    REJECTED_BY_REGRESSION_GATE
  PROTECTED_SUPPORT_GAP_REVISION           PROMOTED_RESEARCH_CANDIDATE
  SELECTED_CANDIDATE                       GROUNDED_SCHEMA_BALANCED
  ```
  "R6 establishes a bounded self-revision result: a finite generic mutation
  library, shadow evaluation, rollback, and hidden promotion selected a protected
  one-shot binding mechanism."
- Hidden scores: one-shot 0.828125, natural one-exposure 0.885417, two-exposure 0.916667,
  `SAVE_RELOAD_PREDICTION_PARITY PASS`; `OPEN_ENDED_RECURSIVE_SELF_IMPROVEMENT NOT_MET`.
- Extends baseline item; no contradiction.

### NEW-3 — Motif Microscope: the learned sensory hierarchy
- Doc: `0681_tnn-pre-v1-r6-rsi-MOTIF_MICROSCOPE.md` | Drive `TNN/TNN/Research/tnn-pre-v1-r6-rsi-MOTIF_MICROSCOPE.md` | 1498 bytes | 2026-08-23
- NEW design rationale for the old sensory stack. Only ~14–30% of the lower
  Adaptive Motif layer's top-160 motifs aligned with known surface values; the higher
  contrastive-memory layer isolated clean cores (1.0000 / 0.9683):
- Quote: "The lower Adaptive Motif layer is not a hidden fixed tokenizer...
  This suggests a useful hierarchy: `messy overlapping compression motifs ->
  grounded discriminative alternatives -> construction schemas ->
  one-shot support-gap binding`."
- Fills baseline gap: how the pre-v1 PAM-adjacent sensory representation was
  actually structured and what it learned.

### NEW-4 — Hardcoded-English prosthesis: the scaffold-and-release origin
- Doc: `0682_tnn-pre-v1-r6-rsi-HARDCODED_ENGLISH_CONTROL.md` | Drive `.../tnn-pre-v1-r6-rsi-HARDCODED_ENGLISH_CONTROL.md` | 1493 bytes | 2026-08-23
- "The user requested a deliberate hardcoded-English experiment." Co-trained
  raw-text substrate retained bounded language after scaffold withdrawal: 0.9375 exact;
  prosthesis alone: covered-grammar 1.000, outside-grammar 0.000.
- Quote: "Co-training is more informative. A generic raw-text substrate trained
  while the prosthesis supplies meanings retains much of the bounded language
  after the prosthesis is removed. That suggests a temporary scaffold may
  accelerate acquisition."
- NEW: the historical precedent for the current program's scaffold-and-release
  (learner-initiated SIGNAL_DISCONNECT) paradigm — baseline has the mechanism as
  law but no recorded origin. Also explicitly "cannot contribute to any TNN
  production gate" — early honest-evaluation boundary.

### NEW-5 — R28 handoff: the acoustic-speech design rationale + Foundry history
- Doc: `0660_TNN_R28_AEIF_NEXT_STAGE_HANDOFF.md` | Drive `TNN/TNN/Research/TNN_R28_AEIF_NEXT_STAGE_HANDOFF.md` | 1713 bytes | 2026-08-23
- Two NEW rationale entries:
- Quote (priority 6): "Attack connected speech as **context-conditioned acoustic
  sequence learning, not as isolated motifs plus guessed hard cuts**. Preserve
  all failed CTC/DTW/EM/transition branches."
- Quote (priority 9): "Improve substrate Foundry from **six-profile meta-search**
  to many procedurally distinct landscapes and require clear
  learned-over-random replication."
- Plus: memory default stays privileged heuristic with explicit training of TNN
  override to surpass it; `LRU stays eviction-only`; graphs "retired as the
  default... optional derived relation indexes remain" (CONFIRMS graph-authority
  retirement in baseline, but with the retirement rationale).
- Extends baseline's "R32 acoustic PAMs DROPPED" — gives the stated intended
  replacement direction and names the failed branches (CTC/DTW/EM/transition).

### NEW-6 — R28 failures: numbers the program never saw
- Doc: `0674_TNN_R28_AEIF_FAILURES_AND_BOUNDARIES.md` | Drive `TNN/TNN/Research/TNN_R28_AEIF_FAILURES_AND_BOUNDARIES.md` | 1549 bytes | 2026-08-23
- Quote: "Hard connected speech is the dominant blocker: integrated hard speech
  **22.08%**; current CTC path **failed even after acoustic pretraining**."
- Also NEW: "More training is not monotonically beneficial: continuous-life
  performance **peaks at dose 256 and regresses at 512/1,024**" (overtraining
  regression); "Learned memory-only alternatives v3/v4/v5 did not beat the
  privileged heuristic"; "nominal sibling 100% fell to 93.54% interactive and
  78.96% high-noise"; hard identity 97.92%, hard switching 90.00%.
- Extends baseline: gives concrete failure numbers for the acoustic direction
  and a memory-policy competition history not previously recorded.

### NEW-7 — R27 native master status: PAM Foundry + no-VAD speech + visual signature
- Doc: `0680_TNN_R27_NATIVE_MASTER_STATUS.md` | Drive `TNN/TNN/Research/TNN_R27_NATIVE_MASTER_STATUS.md` | 1500 bytes | 2026-08-23
- CONFIRMS baseline (R27 canonical, verifier 33/33 rerun passed, step 60,423)
  and adds native-source components never inventoried:
- Quote: "autonomous **non-core PAM Foundry with whole-graph evolutionary
  shadow search**; generic protected-core **relational visual signature**
  candidate; ... **connected acoustic motif decoding without supplied VAD
  boundaries**; provenance-aware sibling testimony."
- Extends baseline senses inventory: PAM Foundry + visual-signature candidate +
  no-VAD acoustic decoding are pre-12-wave artifacts the baseline lacks.

### NEW-8 — R27 failures: PAM Foundry replacement rationale + hybrid rollback
- Doc: `0700_TNN_R27_NATIVE_FAILURES_AND_BOUNDARIES.md` | Drive `TNN/TNN/Research/TNN_R27_NATIVE_FAILURES_AND_BOUNDARIES.md` | 1280 bytes | 2026-08-23
- Quote: "**Two local-credit PAM Foundry learners underperformed random
  generation; whole-graph evolution replaced them.**"
- Also: "Multi-view set and contextual hybrid attempts traded off occlusion
  versus switching; **hybrid was rolled back**"; "No-VAD speech is near-perfect
  on nominal synthetic motifs but falls to **~71% under harder
  duration/noise/blending**"; "Learned memory policy rationally becomes
  EXACT_ALL when storage is cheap; selectivity only emerges under real
  resource pressure"; prior R27 0% changed-view identity test was structurally
  invalid (targets were unseen identities) — an honest self-invalidation.
- Extends baseline: rationale for the Foundry's evolutionary turn; vision
  occlusion/switching tradeoff history.

### NEW-9 — R31 failures: rejected sensory/curiosity objectives
- Doc: `0707_R31_FAILURES_AND_BOUNDARIES.md` | Drive `TNN/TNN/Research/R31_FAILURES_AND_BOUNDARIES.md` | 1220 bytes | 2026-08-23
- NEW abandoned directions with reasons:
- Quote: "Chunk-only sensory representation is rejected: it compresses strongly
  but **loses hidden grounding capability**." / "Predictive-surprise/giant-span
  objectives are rejected as primary chunk criteria when **compression gains
  outpace grounding**."
- Also rejected: always-reinspect (context-sensitive cheaper/better), naive
  regime banks (switching thrash), global probe-budget learning (too
  conservative), state-dependent RF stopping (0.676/0.544); "Natural continuous
  human speech/video self-chunking remains unqualified."
- Extends baseline: none of these rejections were in the baseline.

### NEW-10 — R27 accepted policy: retained / rolled-back promotions
- Doc: `0756_r27-accepted-policy.json.txt` | Drive `.../R33_NATIVE_N17_R27_CONTINUITY/SOURCE_REFERENCES/r27-accepted-policy.json.txt` | 713 bytes | 2026-09-18
- Retained: `R26_VIDEO_IDENTITY`, `R25_GENERIC_VAD`, `R23_R25_SEMANTIC_GENERATOR`;
  rolled back: `CATEGORY_METRIC`, `AFFORDANCE_GENERALIZATION`,
  `VISUAL_DEBATE_EXTRA_VIEW`, `PROTECTED_GENERATOR_SPECIALISTS`,
  `VIDEO_NOISE_RETRAIN`; shadow-partial: `NO_VAD_HIERARCHICAL_MOTIF_SEGMENTER`,
  `CATEGORY_ABSTRACTION`; locked gates incl. `NATURAL_VIDEO_AUDIO`,
  `HUMAN_SUPERIORITY`, `PRODUCTION_TNN_V1`.
- NEW: the actual promotion/rollback ledger for R27 — vision/speech components
  named by codename, none in baseline.

### NEW-11 — R28 hardcoding ledger: pretrained vision models explicitly forbidden
- Doc: `0701_TNN_R28_AEIF_HARDCODING_LEDGER.md` | Drive `TNN/TNN/Research/TNN_R28_AEIF_HARDCODING_LEDGER.md` | 1278 bytes | 2026-08-23
- Quote (explicitly absent/forbidden from mutable cognition): "human object/
  category labels or evaluator entity IDs as semantic answers; ... **YOLO/CLIP/
  SAM/pretrained visual-semantic models**; fixed developmental-age memory
  schedules; graph identity authority; evaluator hidden-set keys/answers."
- Also: "the privileged generic memory heuristic as a **birth/default** policy;
  this is tracked as hardcoding and not credited as emergent memory competence."
- NEW: the "birth/default" hardcoding concept and the pretrained-model ban;
  the memory-heuristic-as-hardcoding framing (extends baseline strength/
  memory-policy discussion).

### NEW-12 — R34 v3 closure: learner test numbers (2026-09-17)
- Doc: `0691_CLOSURE_20260917.md` | Drive `TNN/TNN/Research/R34_NATIVE_CONTINUAL_LEARNER_V3/CLOSURE_20260917.md` | 1386 bytes | 2026-09-18 (content dated 2026-09-17)
- NEW test results never seen: "baseline A is 8/16, trained A is 16/16,
  trained B is 16/16, return A is 15/16; exactly 48 A+B learner updates are
  recorded; update-disabled B records zero updates and 12/24 positives;
  **reward-scrambled A is 0/16**; deterministic learner/world/stream checks
  pass; pending-credit checkpoint fresh-process continuation is byte-for-byte
  exact; inner-state corruption is refused with code 2005; torn outer
  checkpoint is refused with code 2001."
- Receipt: `failures=0, scientific_exposure=0, canonical_r27_mutated=false,
  learner_authority_granted=false, learn_opened=false,
  successor_promoted=false, foreign_ml_runtime_used=false`. Next critical path:
  V91 historical-generator reconstruction and parity.
- Fills baseline's "R34 memory files" line with actual closure numbers.

### NEW-13 — R39 implementation correction: honest prereg deviation record
- Doc: `0677_IMPLEMENTATION_CORRECTION.md` | Drive `TNN/TNN/Research/R39_ONLINE_FACTOR_EXPERTS_20260917/IMPLEMENTATION_CORRECTION.md` | 1533 bytes | 2026-09-18
- The first probe revealed factor creation could never fire (posterior max
  identically 1.0 with one expert vs required <0.78). Corrected pre-tournament
  because it "contradicted the preregistered architecture, which explicitly
  requires persistent learner-visible predictive surprise to be able to create
  a new factor"; the pre-correction probe was preserved under
  `invalid_pre_freeze_probe/` and not scored. Separate success/cost surprise
  thresholds frozen before tournament (success 1.00/0.75/0.55, cost 0.25/0.18/0.12).
- NEW: a documented prereg amendment with preserved invalid probe — no baseline
  equivalent for R39.

### NEW-14 — Compute-efficiency: the Resource Envelope / fibers concept
- Doc: `0748_tnn-v1-current-execution-COMPUTE-EFFICIENCY.md` | Drive `TNN/TNN/Research/tnn-v1-current-execution-COMPUTE-EFFICIENCY.md` | 808 bytes | 2026-08-23
- Quote: "The human defines the total **Resource Envelope**. TNN—not the
  trainer—must decide how many **fibers** exist and how much of the envelope
  each fiber consumes."
- Caveat: "This is a controlled evaluator, not yet the final endogenous
  allocation mechanism. Production TNN must learn its allocation behavior from
  consequences rather than receiving the evaluator's formula."
- NEW: the fibers/resource-envelope design concept — absent from baseline.

## Minor NEW / anchoring details (one-liners)

- `0667_CONTRACT_STATUS.md` (R33 native purity gate, QUALIFIED PASS 2026-09-14):
  gate pins the compiler at `/Users/Shared/micah/Documents/Zag/znc` (SHA
  `3093d12d...`), fail-closed on Python/PyTorch/NumPy/sklearn/jq references —
  anchors Micah's local toolchain path; consistent with baseline's native-purity direction.
- `0755_R33_PARENT_SOURCE_ARCHIVE_CANDIDATES_20260906.txt`: Drive upload source
  candidates included `/Users/Shared/micah/Downloads/TNN_COMPLETE_R1_R32_FULL_BACKUP.tar.gz`
  and Codex checkpoint dirs (`2026-08-23/referenced-chatgpt-conversation-this-is-an`) —
  anchors the Drive corpus provenance.
- `0749_R30_RESET_RECOVERY_BOUNDARY.md`: R30 completed a **100k speech run**,
  **100k/120k developmental-life runs**, and matched teacher/memory/Foundry
  experiments, then lost the raw artifacts in a container reset — recovery
  ledger built only from printed metrics, explicitly non-promotable; R30 stays
  shadow/reference. Scale history not in baseline.
- `0658_SCIENTIFIC_CAMPAIGN_GATE.md`: continuing-life campaign gate design —
  "A failure determines the next controlled investigation; more checkpoints or
  longer execution do not count as improved cognition." Design rationale for
  test discipline, not in baseline verbatim.
- `0655_tnn-pre-v1-r6-rsi-HUMAN_COMPARISON_PROTOCOL.md`: "R6 does **not** claim
  to beat humans. No matched human participants were tested" — complements NEW-2.
- `0745_R32_V39_SHA256.txt`: filenames reveal an R32 V39 candidate
  `r32_v39_candidate_recurrent_temporal_pam.py` — another recurrent-PAM
  generation in the lineage (extends NEW-1's PAM genealogy).
- `0693_R32_E45_NEGATIVE_886943CB_SHARED_INIT_CROSS_BACKEND_DIVERGENCE.txt`:
  arm64 gates `final:FAIL`, x86 gates `final:FAIL` on shared-init cross-backend
  negative; checkpoint marked `obsolete-negative` — consistent with baseline's
  "four valid negatives" framing, adds the cross-backend verdict detail.
- `0687_AUTHORING_UPDATE_20260911.md` (2026-09-11): "Name-memory docs/motif/count
  serialization and `df` representation (`df` is explicitly unsupported by the
  N12 NumPy-view subset and was not coerced into one)" — minor authoring boundary.

## CONFIRMS baseline (compact)

- `0661_R31_HARDCODING_LEDGER.md`: memory storage classes protected substrate; privileged default = birth/default, LRU eviction-only.
- `0678_R32_E51AE_HARDCODING_LEDGER.md` (frozen 2026-08-31): exact reconstruction numbers only decide parent reproduction, never fed to policy.
- `0649_unreachable_objects.txt`, `0683_unreachable_blob_search.txt`: git parent-recovery archaeology — fragments only; consistent with baseline "FRAGMENTS ONLY" and the cancelled pre-git hunt.
- `0659_R32_E51AG_HARDCODING_LEDGER.md`, `0708_SMOKE_01.md`, `0730_R32_V43_PRELIM_BUG_BOUNDARY.md`,
  `0747_R32_V32_PRELIM_BUG_BOUNDARY.md`: bug/reject-before-interpretation discipline — matches baseline honesty culture.
- `0711_HISTORICAL_WITNESSES.md`: R27 receipt 33/33 is a historical witness, "must never be counted as N17 native checks" — matches baseline R27-canonical.
- `0743_SOURCES.verified.txt`, `0741_AUTHORITY_SHA256SUMS.txt`, preflight/postrun pin files (`0646/0647/0657/0662/0663/0664/0668`): provenance pinning practice.
- `0652_R32_EPISTEMIC_R31_MATCHED_V21_INTERPRETATION.md` + ~14 other V-series interpretation/sha256 files (`0644,0645,0650,0651,0653,0656,0665,0666,0673,0675,0684,0685,0689,0699,0702,0703,0713,0721,0744`): R32 epistemic qualification development notes, all REFERENCE_ONLY / R27-canonical — no new verdicts.
- `0629`-class licenses (`0676,0715,0718,0719,0720`): pip/numpy vendored LICENSE files — noise.
- `0716_STATUS.md` (selector authoring 04), `0739_STATUS.md` (03): native authoring probes under pinned macOS-arm64 compiler.
- `0740_R32_V43_SHA256.txt`, `0690_R32_E47_*_BUILD_PROVENANCE.txt`, `0704_SHA256SUMS.txt`, `0706/0735/0742_FRESH_CONTRACT.md`, `0726/0731_SELECTION_FREEZE.md`: freeze/selection discipline.
- `0698_TELEMETRY_OBSERVATION_CONTRACT.md`, `0705_RECOVERY_PROTOCOL.md`, `0738_ABI_BLOCKER.md`: runtime boundary contracts; ABI blocker lists stable errno translation etc.
- `0692_CUSTODY_CORRECTION.md`, `0725_REMEDIATION_STATUS.md`: custody/remediation bookkeeping.
- `0714_TNN_R28_AEIF_TRACEABILITY.md`: parent-linked event trace design — matches baseline traceability.
- `0737_transport.commands.txt`, `0732/0733_PARENT_RECOVERY_VERIFIED`, `0728_fixture_bytes.txt`: operational noise.
- `0734_R32_V38_SHA256.txt`, `0736_R32_V40_SHA256.txt`: sha lists of candidate/recurrent-model artifacts — file-name evidence of temporal-PAM work, no verdicts.

## NOISE (compact)

- Pure SHA256SUMS / preflight-pin / postrun-pin / import-closure / fixture-size / command logs with no prose: `0644,0646,0647,0657,0662,0663,0664,0668,0684,0685,0695,0694,0704,0713,0721,0740,0744,0723,0727`.
- Vendored third-party licenses: `0676,0715,0718,0719,0720`.
- `0728_fixture_bytes.txt`, `0744...`: fixture/command noise (covered above).

## koryphaios / ghost / sylorlabs

- **Zero hits** for `koryphaios`, `ghost`, `sylor`, `Cooley`, or github URLs across all 114 files.

## Note on manifest hygiene

- The batch manifest's `local` column is stale/wrong for this tier (points at
  `0416–0529_` names from a different enumeration order). Reliable identifiers
  are `drive_path` (all 114 matched via `manifest.json`). Parent may want to
  rebuild `batches/tier2_batch2.json` from `manifest.json` before other
  skimmers run their batches.
