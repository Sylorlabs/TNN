# tier1_batch5 findings (52 docs, global indices 260–311)

**Manifest note:** the batch's original `local` names pointed at batch 0's files (0000–0051). Resolved via the master `manifest.json` drive_path mapping to the true locals `0260_*`–`0311_*`; the in-place-fixed manifest now matches. All 52 files below were read from the correct local paths.

## NEW findings

### N1. R33 structural plasticity plan (M2–M7 roadmap)
- `TNN/TNN/Research/R33_STRUCTURAL_PLASTICITY_PLAN.md` · 2867 B · 2026-09-18 · **NEW**
- Design rationale for future self-modification of structure: hierarchical motif programs (region spec, repeat counts, connectivity, sparsity) materializing thousands/millions of effective interactions without a central executive choosing every edge; M5 learns a proposal policy from prior proposals/failures/ablations; M7 integrates qualified capabilities over a continuing life.
- Quote: "A researcher-selected controlled candidate remains a researcher-controlled arm, not proof of autonomous architecture invention."
- Fills gap: baseline has no structural-plasticity plan; this is the pre-designed falsifier set for it ("gains require manual task routing; no improvement over random at matched search cost").

### N2. Competence-gated assistance withdrawal (H0–H5)
- `TNN/TNN/Research/R33_HAND_HOLDING_WITHDRAWAL_PLAN.md` · 2854 B · 2026-09-18 · **NEW**
- The scaffold-and-release design behind the baseline's SIGNAL_DISCONNECT: six stages from full demonstrations (H0) to full withdrawal with safety supervisor remaining (H5), per-competency, with an advancement contract (fresh transfer slices, delayed retention, no regression) and causal withdrawal tests (matched forks: continued help vs graded vs abrupt vs request-only).
- Quote: "Performance collapse is evidence of scaffolding dependence, not a reason to silently restore help and count the episode as independent."
- Extends baseline's one-line "scaffold-and-release with learner-initiated SIGNAL_DISCONNECT".

### N3. Memory autonomy plan (M1)
- `TNN/TNN/Research/R33_MEMORY_AUTONOMY_PLAN.md` · 2423 B · 2026-09-18 · **NEW**
- Learner-owned memory-policy design: learner chooses representation/tier/retrieval/rehearsal/eviction; generic storage + protected constraints supplied by architecture.
- Quotes: "LRU is a subordinate control/mechanic, not the learner's representation policy." / "A mutable chunk dictionary must not retroactively change remembered experience."
- Design rationale we lacked; connects to baseline's deliberate memory ops but predates the post-toy framing (prospective M1).

### N4. Fair architecture-family benchmark (no-free-lunch formalization)
- `TNN/TNN/Research/R33_ARCHITECTURE_COMPARISON_BENCHMARK.md` · 2825 B · 2026-09-18 · **NEW**
- The benchmark design behind Micah's no-free-lunch law: families named (dense/MoE transformers, recurrent/state-space, memory-augmented, neuro-symbolic/tool, associative-memory...), matching ledger with MATCHED/BOUNDED/ESTIMATED/MISMATCHED/UNKNOWN axes, separate equal-experience/equal-compute/equal-memory frontiers, Pareto reporting, no composite score hiding violated floors.
- Quote: "A specific benchmark win is neither general intelligence nor consciousness."
- Extends baseline's standing law into the actual planned method.

### N5. R32 E51 causal series results (E51E, E51H, E51I, E51J)
- `TNN/TNN/Research/R32_E51E_RESULT.md` · 2858 B; `R32_E51H_RESULT.md` · 2251 B; `R32_E51I_RESULT.md` · 2802 B; `R32_E51J_RESULT.md` · 2645 B · all 2026-08-30 · **NEW**
- Never-seen test results, all `VALID NEGATIVE` (R27 unchanged):
  - E51E (terminal refit reachability): primary exact gate failed — known reachable 4,200/4,200 but no-unique UNKNOWN reachable only 1,125/1,200 (75 residual failures).
  - E51H (neutral-relative preference): rejected — "Changing supervision from absolute grounded utility to the sign of commit utility relative to neutral UNKNOWN did not rescue terminal reachability."
  - E51I (margin/ranking geometry audit): uniform commit-shift theorem — satisfying all known needs `s >= +57`, satisfying all no-unique needs `s <= -631`; intersection empty, so "one global bias or temperature cannot solve both sides."
  - E51J (state-dependent calibration): calibration eliminates 70 of 92 no-unique vetoes but suppresses valid commitment on 55 additional known episodes — diagnosed as "a calibration generalization/support problem, not a commit-ranking problem."
- Baseline's R32 section lists only E45/E48; the whole E51 terminal-reachability campaign (exact gates, fresh seeds 19,440/run) is new.

### N6. R36 context identification (REFERENCE PASS) + prereg
- `TNN/TNN/Research/R36_CONTEXT_IDENTIFICATION_20260917/R36_RESULT.md` · 2738 B; `.../PREREGISTRATION.md` · 2408 B · 2026-09-17 · **NEW**
- Learner-side identification of returning self-contexts from learner-visible evidence: candidate `eig_012` cut return regret 29.21% (dev) / 24.74% (fresh family) vs V2; all development and fresh-family aggregate gates passed.
- Key ablation: "The passive posterior archive explains most of the gain" — EIG diagnostic actions added only 2.62% incremental reduction at 0.001111 diagnostic-action fraction.
- Status is reference-only; Phase 6 closed, `learn_authority=0`, native Zag implementation pending. Prereg admission gates (return-regret ≥5% better than V2, overall ≤3% worse, etc.) document the bar.
- Baseline has no R35/R36 context-identification results.

### N7. R38 → R39 → R40 → R47 self-context/factor chain
- `R38_FACTORIZED_CONTEXT_20260917/PREREGISTRATION.md` · 2273 B (2026-09-17); `R39_ONLINE_FACTOR_EXPERTS_20260917/R39_RESULT.md` · 2594 B; `R40_RELIABILITY_ARBITRATION_20260917/PREREGISTRATION.md` · 2116 B; `R40_RESULT.md` · 1956 B; `R47_STATE_RESIDUAL_MIXTURE_20260918/PREREGISTRATION.md` · 2214 B · **NEW**
- Chain of abandoned/iterated directions, all new to baseline:
  - R38 prereg records the R37 finding: "a monolithic context posterior can improve average adaptation while still making severe return-routing errors when previously learned success and cost components recombine" → factorize success/cost as independent latent factors.
  - R39 result: **FRESH NO-GO** — `balanced_blend30` passed 7/8 fresh gates; cost-recurrence gate failed (only ~3.4% improvement vs required 10%). Conclusion: "a fixed blend between factor experts and the stable monolithic posterior is still too coarse."
  - R40 (channel-specific reliability arbitration, factor weights bounded [0.15, 0.90]): **DEVELOPMENT NO-GO / FRESH UNOPENED** — no candidate cleared all 8 development gates; "learned success/cost factor weights remained close to 0.5 ... global channel-level predictive-loss arbitration did not separate the substrates strongly enough." Next: strategy-specific/state-conditioned reliability.
  - R47 prereg: "R46 rejected one continuously learned residual surface despite strong exercise" → test multiple locally-valid residual corrections selected from learner-visible state.
- Design rationale + abandoned directions with stated reasons, exactly the category of interest.

### N8. R50 bounded multimodal P1/P2 prereg (senses origins)
- `TNN/TNN/Research/R50_P1_P2_BOUNDED_MULTIMODAL_TOOLS_20260918/PREREGISTRATION.md` · 2095 B · 2026-09-18 · **NEW**
- Six frozen synthetic sense tracks with exact-verifier gates, explicitly "deliberately does not relabel these as broad natural language, natural connected speech, or real-world vision":
  1. grounded compositional language (novel-composition ≥0.90); 2. generic tool sequencing (`READ`, `SEARCH+READ`, `WRITE+TEST`, `CALCULATE`, `INSPECT+TEST`, held-out templates ≥0.85); 3. synthetic vision — raw 8×8 arrays, translation/noise, occlusion ≥0.70, uncertainty-triggered reinspection; 4. object persistence (moving point, hidden frame, ≥0.95); 5. synthetic hearing — acoustic motifs from raw waveforms, held-out speakers/amplitude/phase/noise (≥0.85), phrase composition ≥0.80; 6. cross-modal grounding visual↔audio from co-occurrence only (≥0.90).
- All labels/tokens randomized by evaluator, absent from source before execution. `learn_authority=0`.
- Direct senses/PAM/vision/audio origins: the planned multimodal track that follows the R33 S0/S1 sensor qualification.

### N9. N06 sensor review — design rationale for byte-originated ingress
- `TNN/TNN/Research/R33_NATIVE_N06_SENSOR_TRACE/REVIEW.md` · 2382 B · 2026-09-18 · **NEW** (minor)
- The WHY behind sensor.zag's byte-first design: "The sensor path does not reduce raw evidence to an invariant summary. A packet's complete physical metadata and bytes are retained... without semantic units, normalization, subsampling, or an evaluator argument."
- Also: raw storage needs a separate persistent reservation "because process death may occur before the telemetry attempt exists."
- Extends baseline's sensor.zag/RawRecord knowledge with rationale.

### N10. N14 closeout — full S1 PASS record
- `TNN/TNN/Research/R33_N14_CLOSEOUT_SUMMARY.md` · 1968 B · 2026-09-18 · **CONFIRMS**
- Independent reviewer returned `CONFIRM_BOUNDED_ENGINEERING_PASS` (consumed). Matches baseline's N14 S1 PASS line; adds operational detail: 8 packets byte-exact after fresh-process replay, 14 malformed refused, 182 child + 48 parent checks, wrapper `/usr/bin/date` path invalid on host (zero-byte start.utc/end.utc preserved, no backfill).

### N11. Native journal design (replaces C03's Python collector)
- `TNN/TNN/Research/R33_NATIVE_N03_BUILD_01/R33_NATIVE_JOURNAL_DESIGN_V1.md` · 2768 B · **NEW**
- Native Zag journal candidate replacing "C03's historical external Python collector": exact initial byte snapshot, per-record sequence/tx identity/parent/mutation kind/before-after digests, no-replace hardlink publish, fsync discipline; rollback is a new kind2 snapshot record, never deletion.
- Quote: "The hash chain is not a signature, grant or trusted timestamp."
- Design rationale for the audit/journal substrate; explicitly does not prove the "no learner can call this privileged operator API directly" boundary.

### N12. C03 result — user ordered Python supervisor dropped
- `TNN/TNN/Research/R33_B001_C03_RESULT.md` · 2353 B · 2026-09-05 · **NEW**
- 21/21 engineering groups matched (80 native Zag replay executions + 173 subprocesses incl. Python supervisor). The decision: "The user's subsequent native-Zag-only correction excludes this Python supervisor from the forward runtime, supervision and evaluation path... Do not rewrite or rerun C03 to relabel it native-only."
- People/date anchor: Micah's direct directive (pure-Zag law origin), preserved as historical mixed-language component.

### N13. C01 result — native component checks matched
- `TNN/TNN/Research/R33_B001_C01_RESULT.md` · 2847 B · 2026-09-05 · **NEW**
- 77 scalar observations + 40 vectors (77,986 elements) matched independent expected values. Coverage: all 65,536 PCM16 codewords decoded to specified signed values; 64×64 RGB frame retained all 12,288 channel values; protected-LRU refusal, codebook mutation/reorder rejection.
- Note: "This is component engineering evidence, not complete B001" — and the baseline's "B001 11 component bugs" were in the unexecuted candidate; this is the executed C01.
- Also records the honest-limits culture: "No learning was involved"; "Hard RSS and filesystem read isolation remain unqualified, as disclosed before execution."

### N14. N15 closeout + independent review (additive preservation)
- `TNN/TNN/Research/R33_N15_CLOSEOUT_SUMMARY.md` · 2802 B; `R33_NATIVE_N15_PRESERVATION_ADDITIVE/INDEPENDENT_REVIEW_V1.md` · 2124 B · **NEW**
- Disposition `CONFIRM_CONSUMED_NEGATIVE_WITH_PROMISING_FRONTIER_SIGNAL`: 156 fresh exposures, arm10 retained positive new gain in every validation population but exceeded frozen preservation limits (max final-old deficit 21).
- Key clue: "arm10 validation `anchor_loss=0` alongside material unseen old-probe loss: the current preservation anchors are being protected while protection fails to generalize across the broader old-behavior distribution."
- Pre-run review was `REQUEST_CHANGES` with 3 blockers (undeclared new_gain tie-break, arm1/2 admissibility mismatch, no native validation→confirmation gate).

### N15. N16 review arc V1→V2→V3 (REQUEST_CHANGES → approve-for-prereg-only)
- `R33_NATIVE_N16_SUPPORT_ROUTING/INDEPENDENT_REVIEW_V1.md` (2643 B), `_V2.md` (2524 B), `_V3.md` (2221 B) · 2026-09-07 · **NEW**
- Three-review correction arc, all preserved with exact manifests and byte-identical build hashes: V1 REQUEST_CHANGES (holdout comparator arm-scope mismatch; old-support attribution mismatch) → V2 REQUEST_CHANGES (one blocker left: support target-truth attribution — `n16_anchor_set_loss()` uses labeled support loss for update acceptance despite CONFIG claiming it "never contributes ... target truth") → V3 `APPROVE_FOR_PREREGISTRATION_ONLY_NO_EXECUTION_AUTHORIZATION` (all three blockers closed).
- Evidence of the review discipline; no N16 scientific execution was authorized by any of the three.

### N16. N18 review V4 — four hard blockers
- `R33_NATIVE_N18_R27_FROZEN_CORE_SIDECAR/INDEPENDENT_REVIEW_V4.md` · 2505 B; `REVIEW_REQUEST.md` · 2501 B · **NEW**
- V4 disposition `REQUEST_CHANGES`; blockers: (1) actual parent-to-sidecar semantics unresolved (R27 feature source/dimension/ordering/scale/clipping deferred — "The synthetic N16 16-dimensional mechanism cannot substitute for this mapping"); (2) no qualified native parent runtime/evaluator; (3) no admissible route selected; (4) custody/forward-dependency evidence only templated.
- Decision: "Do not register, preregister, reserve, freeze, admit, execute, or make a scientific claim from N18." (Review request itself with its 11 review questions: process NOISE.)

### N17. N08 family arc (N08 FAILED → N08A FAILED → N08B PASSED)
- `R33_NATIVE_N08_RESULT.md` · 1981 B; `R33_NATIVE_N08A_RESULT.md` · 2011 B; `R33_NATIVE_N08B_RESULT.md` · 2561 B; `R33_NATIVE_N08A_ISOLATION/PREREGISTRATION.md` · 2820 B; `R33_NATIVE_N08B_ISOLATION/PREREGISTRATION.md` · 2277 B; `R33_NATIVE_N08_ISOLATION/REVIEW.md` · 2400 B · **NEW**
- Full honest failure-to-pass arc: N08 failed before worker entry (SIGABRT in dyld, abort "inside dyld ignition_halt/boot_boot/CacheFinder before main") → N08A prereg evidence-grounded on the actual macOS diagnostic report (worker PID 45937), byte-exact copy of Apple's dyld-support.sb hashed into the repo; N08A then failed 13/14 (socket syscall didn't return EPERM/EACCES) → N08B prereg explicitly denied syscall entry 97/135/450 → N08B PASSED (15 worker assertions, 67 parent checks, canary bytes unchanged).
- N09 review notes its OS adapter is "the bounded passing N08B design" — N08B became infrastructure.

### N18. N01A / N01P failures (supervisor + compiler fault isolation)
- `TNN/TNN/Research/R33_NATIVE_N01A_RESULT.md` · 2275 B; `R33_NATIVE_N01P_RESULT.md` · 2027 B · **NEW**
- N01A failed: monotonic-clock call failed in the pinned native binary (NRV2_CLOCK), 21 of 66 CHECK rows failed; "newer compiler source is not proof of that binary's support."
- N01P isolated an imported-constant fault ("pointer-like values instead of the authored integers") and explicitly rules out the workaround: "the proposed N01B cast-only oracle workaround is NOT validated. No N01B primary has run."
- Relevant to the baseline's znc compiler bugs — a fourth characterized compiler/lowering fault class (imported-constant visibility/resolution).

### N19. N03 journal failure → journalV2/N03A required
- `TNN/TNN/Research/R33_NATIVE_N03_RESULT.md` · 2413 B · **NEW**
- Sole primary exit1 after 36/58 children; boundary11 failed only on the closed-lock field (observed -2 vs expected -1): `nj_close` normalizes only nonnegative fds, so the -2 error value was retained instead of the closed sentinel. "This is not evidence of a descriptor leak... The preregistered assertion is nevertheless failed, not revised after the run."
- Corrective implementation "must use journalV2 and a new N03A identity"; boundaries 12–32 never executed.

### N20. R34 v2/v3 continual-learner preregs + v3 checklist
- `R34_NATIVE_CONTINUAL_LEARNER_V2/PREREGISTRATION.md` · 2656 B; `R34_NATIVE_CONTINUAL_LEARNER_V3/PREREGISTRATION.md` · 2115 B; `TNN_R34_V3_QUALIFICATION_CHECKLIST.md` · 1952 B · **NEW**
- Fixed claims both versions: untrained regime-A baseline 8/16 → 16/16 after 24 experiences → hidden switch, 24 B experiences → 16/16 and a second latent context "allocated from outcome surprise rather than a regime label"; return to A 15/16 with no score/count updates; exactly 48 updates; reward-scrambled control 0/16; inner-learner digest refuses corruption even after outer digest recompute.
- V3 adds a structural isolation gate: `r34_learner_core.zag` may import the observation contract only — "must not import `world.zag` or `checkpoint.zag`... no `cw_` calls or `CWOutcome` references."
- R34 native held-out behavioral V1 prereg (`.../.r34_native_extract_20260917/.../PREREGISTRATION.md`, 2203 B): six staged mechanisms with fixed gates — memory lifecycle (learned recall ≥ FIFO+0.15, ≥0.55), hypothesis state (≥0.85, +0.20 over zero-credit), association credit, provenance reliability, curiosity (informative arms ≥0.70, noise arm ≤0.25), self model (regret ≥20% lower, optimal-strategy ≥0.60).
- Extends baseline's "R34 memory files / delayed-credit formula dropped" with the concrete native qualification machinery.

### N21. V91 native historical-generator sidecar (R23 recovery PASS)
- `TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT/README.md` · 2178 B · **NEW**
- The historical R23 semantic generator reconstructed in pure Zag: dataset/order 16/16, naive generation 16/16 exact, semantic roundtrip n=128 16/16 exact, byte-identical deterministic repeat; frozen evidence `RECOVERY_EXACT_ROUNDTRIP_20260918T051756Z`; "Historical Python source is inert specification only."
- Claim boundary kept: "This does not open `learn`... Full N17 continuity remains fail-closed while R25/R26 source/member dependencies remain unresolved."
- Related recovery evidence (n17_lane_witness README, 2787 B): Lane B bounded local evidence audit — V91 had "exact 16-string oracle custody" but "generated zero strings" from the author reconstruction; "Exact missing input identities were not found within this documented scope"; recovery inventories cover hidden/ignored TNN and local Zag paths, 27 archives, every reachable/unreachable Git blob. Extends baseline's "historical recovery efforts" with the V91 win and the missing-inputs negative result.

### N22. N19 design — Zag host-ABI qualification boundary
- `TNN/TNN/Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/DESIGN.md` · 2452 B · **NEW**
- N19 is DESIGN_AND_COMPILE_ONLY: bounded native runtime/telemetry gate (32-byte records, 8 journal events, checked CPU/output limits).
- Explicit blocker recorded: "the current Zag host ABI does not provide a reviewed capability-safe, root-relative macOS/APFS adapter with a stable contract for openat-like traversal, symlink policy, crash durability, process-group containment, and portable errno translation."
- Design rationale / platform-limitation anchor.

### N23. Efficiency & sparse-compute plan (prospective)
- `TNN/TNN/Research/R33_EFFICIENCY_AND_SPARSE_COMPUTE_PLAN.md` · 2583 B · **NEW**
- Candidate mechanisms (routed PAMs, block-sparse, event-driven, lazy motif expansion, memory tiering...); reporting rules: "Plot capability against active inference operations... Show a Pareto set rather than one composite score that can hide a violated floor."
- Honest note: "The inherited compute-efficiency document contains an empty result table and describes an evaluator, not an endogenous allocator. R33 will not copy it as measured efficiency evidence."

### N24. N13 build/review history (Euler reviewer)
- `TNN/TNN/Research/R33_NATIVE_N13_TORCH_VIEWS/PREREVIEW_V1/BUILD_AND_REVIEW_HISTORY.md` · 2421 B · **NEW** (minor)
- People anchor: "Euler's initial review found F1 resource failures obscured by generic refusals and F2 repeated parsing/hashing without aggregate limits. It did not approve preregistration." BUILD_01 (compile-only, exit 2) and BUILD_02 compiled but never executed; final review/registration/freeze pending. No N13 fixture or primary has executed.

### N25. N02 prereg — native SHA256 replaces Python hashing
- `TNN/TNN/Research/R33_NATIVE_N02_PREREGISTRATION.md` · 2018 B · **NEW** (minor)
- 35-assertion native SHA256 KAT (incl. 1M-byte case, overlapping input/output); "Native SHA256 implementation and assertion driver replace Python hashing/verification on the forward path." No cryptographic certification claimed.

### N26. Pre-v1 RSI self-architecture revision note
- `TNN/TNN/Research/tnn-pre-v1-r6-rsi-SELF_ARCHITECTURE_REVISION.md` · 2060 B · 2026-08-23 · **CONFIRMS**
- Matches baseline's already-known pre-v1 RSI note: two-step R6 revision (unprotected one-shot-gain candidate rejected for established-language regression; protected support-gap candidate promoted on hidden seeds); `BOUNDED_SAR = PASS`, `OPEN_ENDED_RECURSIVE_SELF_IMPROVEMENT = NOT_MET`. Next target: infer a saturation variable from marginal information gain / cross-modal agreement / novelty.

## CONFIRMS / NOISE (one line each)

- `R33_NATIVE_N14_SENSOR_INFORMATION/PRE_REVIEW_V2_INPUTS_VERIFIED.txt` (2584 B) · **NOISE** — 40-line file-verification manifest for the N14 S1 run (all OK); no findings.
- `R33_NATIVE_N14_SENSOR_INFORMATION/PRE_REVIEW_INPUTS_VERIFIED.txt` (2512 B) · **NOISE** — same, V1/BUILD_03-04 variant.
- `R33_NATIVE_N18_R27_FROZEN_CORE_SIDECAR/REVIEW_REQUEST.md` (2501 B) · **NOISE** — the 11-question review-request brief for the N18 review; process doc, no results.
- `R33_NATIVE_N10_PARENT_MAP/REVIEW.md` (2584 B) · **CONFIRMS** — native pickle→typed-inert-record mapping review; consistent with baseline's "trace-op semantics proven unrecoverable / mapping only" stance.
- `R36_CONTEXT_IDENTIFICATION_20260917/PREREGISTRATION.md` (2408 B) · **CONFIRMS** — companion prereg to the R36 result (N6); admission gates detail only.
- `R33_NATIVE_N08_ISOLATION/REVIEW.md` (2400 B) · **CONFIRMS** — N08 pre-exposure engineering review; the news (N08B pass) is in N17.
- `R33_NATIVE_N09_ANCHORED_CHECKPOINT/REVIEW.md` (2197 B) · **CONFIRMS** — restore/export engineering review; notes N09's OS adapter is the passing N08B design.

## What was NOT found

- No contradictions with the baseline's standing laws or wave results. The honest-failure culture in these docs (E51 series VALID NEGATIVEs, R39/R40 NO-GOs, N08/N08A/N01A/N03 failures reported as-is with frozen evidence) is consistent with baseline.
- No mentions of "koryphaios" or "ghost" projects anywhere in this batch.
- No new people anchors beyond the independent reviewer codename "Euler" (N13 history) and Micah's machine paths (`/Users/Shared/micah/...`, `/Users/Shared/micah/Documents/zag/znc`).
- Date anchors: E51 series 2026-08-30; C01/C03 runs 2026-09-05; N16 reviews 2026-09-07; R36/R38/R40 preregs 2026-09-17; R47/R50 preregs 2026-09-18; V91 roundtrip evidence 20260918T051756Z; RSI note 2026-08-23.
