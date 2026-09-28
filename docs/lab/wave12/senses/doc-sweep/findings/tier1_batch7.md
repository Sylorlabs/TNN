# tier1_batch7 findings — 52 files read (global 0364–0415), 20 NEW, 9 CONFIRMS, 23 NOISE

Baseline: `../BASELINE.md`. Batch manifest: `../batches/tier1_batch7.json`.
Batch7 entry i → docs_local/0364+i. Dates: nearly all docs modified 2026-09-18; #18 modified 2026-08-23 (pre-September program).

## NEW

### [00] `0364_R33_NATIVE_D01_PREREGISTRATION.md` — TNN/TNN/Research/R33_NATIVE_D01_DURABLE_TELEMETRY/R33_NATIVE_D01_PREREGISTRATION.md, 1025B, 2026-09-18
- **Finding:** Prereg for a native append-only telemetry substrate — this is the design origin of the append-only audit evidence chain (baseline's wave-12 "sealed verdict record / audit instrumentation" has this ancestor; D01 itself is not in baseline).
- Quote: "A native append-only telemetry substrate can preserve an evidence chain across commit interruption, restart, and replay while explicitly rejecting incomplete or corrupted records."
- Extends: wave-12 audit-ledger instrumentation (rationale: interrupted commits detected, no silent state loss, fresh-process replay).

### [01] `0365_PREREGISTRATION_WAVE2.md` — TNN/TNN/Research/R38_FACTORIZED_CONTEXT_20260917/PREREGISTRATION_WAVE2.md, 993B, 2026-09-18
- **Finding:** R38 (factorized context) is an entire research round absent from baseline. Wave 1: factorization improved recombination but had a stability tradeoff; no wave-1 candidate passed every gate. Wave 2 tests a bounded mixture of stable whole-context + independently factorized posteriors (hybrid25/hybrid50/hybrid75/hybrid_adaptive), same delayed experience to both, no evaluator context, frozen fresh family still unopened.
- Quote: "Wave 1 factorization improved recombination but revealed a stability tradeoff. No wave-1 candidate passed every gate, and the already-frozen fresh family remains unopened."
- Fills: unknown research round — design rationale + gate structure for R38.

### [02] `0366_R49_RESULT.md` — TNN/TNN/Research/R49_META_AUTONOMY_20260918/R49_RESULT.md, 986B, 2026-09-18
- **Finding:** R49 meta-autonomy closeout **PASS** — baseline has no R48/R49. R48 exposed two failures (curiosity scoring, self-model exploration); R49 changed only those, generated fresh randomized test identities post-freeze, kept update-disabled controls; curiosity = transition predictability + outcome entropy + non-overlapping rolling learning progress + decaying novelty; `learn_authority=0`, R27 unchanged.
- Quote: "R49 was preregistered after R48 exposed two failures. It changed only curiosity scoring and self-model exploration, generated fresh randomized test identities after source freeze, and retained update-disabled controls."
- Fills: test result never seen (curiosity/self-model machinery PASS).

### [03] `0367_R33_NATIVE_N02A_RESULT.md` — TNN/TNN/Research/R33_NATIVE_N02A_RESULT.md, 975B, 2026-09-18
- **Finding:** N02A correction qualified: 45/45 native assertions passed, exit 0; corrected round-constant table + validation (KAT answers unchanged); original N02 negative frozen and consumed. Also: "Read-only artifact hashing may now use the exact frozen corrected binary's `file` mode; those verifications are not new scientific experiments."
- Quote: "The original N02 negative remains frozen and consumed."
- Fills: R33 N-series qualification detail not in baseline.

### [05] `0369_PREREGISTRATION.md` — TNN/TNN/Research/R56_CONVOLUTIONAL_VISUAL_20260918/PREREGISTRATION.md, 966B, 2026-09-18
- **Finding:** Vision lineage beyond baseline's R51–R54: R55 "learned dense representation nearly closes clean visual transfer but remains fragile to occlusion and noise"; R56 = learned local convolutional bank (16 learned 3×3 filters on 13×13 raw pixels, ReLU, global max+mean pooling) — translation structure without category-specific features. Frozen gates: clean ≥0.95, occluded ≥0.85, noise-heavy ≥0.85, active ≥0.93.
- Quote: "R55 demonstrated that a learned dense representation nearly closes clean visual transfer but remains fragile to occlusion and noise."
- Fills: senses/vision origins — R55/R56 generation + rationale.

### [06] `0370_PREREGISTRATION.md` — TNN/TNN/Research/R57_SCANNED_LEARNED_TEMPLATE_VISUAL_20260918/PREREGISTRATION.md, 965B, 2026-09-18
- **Finding:** R57 rationale: R56 strong on clean/active but below frozen single-view corruption floors; new mechanism = learn a local occupancy template per randomized category, then scan it over every spatial location at inference — marginalizes translation, isolates local evidence from global noise. No category-specific detector written.
- Quote: "R56 shows a learned convolutional representation is strong on clean and active-view panels but still below the frozen single-view corruption floors."
- Fills: vision lineage R57 design rationale.

### [07] `0371_PREREGISTRATION_V3.md` — TNN/TNN/Research/.r34_native_extract_20260917/Research/R34_BEHAVIORAL_HELDOUT_STAGE_20260916/PREREGISTRATION_V3.md, 958B, 2026-09-18
- **Finding:** R34 behavioral held-out V3 rationale: V2 passed 5/6 gates; its association arm failed because "a single undifferentiated association strength has no forgetting or latent-context mechanism: a forced mapping reversal causes old and new consequence credit to cancel." V3 changes only the association evaluator (5 learner-visible cue nodes, stationary hidden neighbor mapping); held-out seeds 34211/34213/34217 never executed pre-prereg.
- Quote: "V2 development passed five of six gates. Its association arm failed because a single undifferentiated association strength has no forgetting or latent-context mechanism: a forced mapping reversal causes old and new consequence credit to cancel."
- Fills: abandoned mechanism detail (undifferentiated association strength) + held-out discipline specifics.

### [08] `0372_README.md` — TNN/TNN/Research/R34_NATIVE_CONTINUAL_LEARNER_V1/README.md, 957B, 2026-09-18
- **Finding:** R34 native continual learner v1 origin: small pure-Zag online learner — learner owns four integer action values, deterministic native RNG state, update counter, pending causal credit; Task B initially failed → mastered via experience, Task A retained; full mutable state serialized w/ SHA-256, fresh-process reconstructable. Explicitly "not wired to the R33 `learn` admission gate, does not mutate canonical R27, and is not a scientific TNN result." Build path `/Users/Shared/micah/Documents/zag/znc` (anchors Micah's Mac compiler location).
- Quote: "The learner owns four integer action values, deterministic native RNG state, an update counter, and pending causal credit."
- Fills: continual-learner origins; note "deterministic native RNG state" in an early prototype (deterministic-given-state, so consistent with — but worth noting against — the zero-RNG law).

### [09] `0373_README.md` — TNN/TNN/Research/R34_NATIVE_CONTINUAL_LEARNER_V3/README.md, 946B, 2026-09-18
- **Finding:** R34 v3 structurally separates learner from evaluator/world (`r34_learner_core.zag` vs `r34_continuing_harness_v3.zag`; learner imports only R33 observation layer); adds latent-context switching, pending-credit fresh-process continuation, corruption fixtures; additive/quarantined, no R27 mutation, no `learn` admission.
- Quote: "R34 v3 structurally separates the learner from the evaluator/world used by R34 v2."
- Fills: R34 learner lane evolution v1→v3 design rationale.

### [11] `0375_PREREGISTRATION.md` — TNN/TNN/Research/R58_SUPPORT_CHANNEL_CONV_VISUAL_20260918/PREREGISTRATION.md, 879B, 2026-09-18
- **Finding:** R58 rationale: R55–R57 solved translation mostly; sparse pixel noise is now the dominant failure. Adds one generic observation channel (local occupied-neighbor density map, identical for every category, computed only from current observation); learner learns all category features through conv bank + hidden layer. Same frozen gates.
- Quote: "R55–R57 show that translation is mostly solved but sparse pixel noise remains the dominant failure."
- Fills: vision lineage R58 design rationale.

### [13] `0377_PREREGISTRATION.md` — TNN/TNN/Research/R53_OCCLUSION_MARGINAL_VISUAL_20260918/PREREGISTRATION.md, 868B, 2026-09-18
- **Finding:** R53 rationale: R52 passed clean/active floors but failed single-view occlusion floor; keeps local cluster/translation normalization, changes only category scoring — Bernoulli occupancy prototype per randomized category; missing expected evidence gets a generic occlusion likelihood, extra unexpected evidence gets ordinary noise likelihood; same likelihood rule for every category.
- Quote: "For each evaluator-randomized category, the learner estimates a Bernoulli occupancy prototype over the normalized local patch from training examples. At inference, missing expected evidence receives a generic occlusion likelihood while unexpected extra evidence receives the ordinary noise likelihood."
- Fills: vision lineage R52/R53 design rationale (occlusion handling mechanism).

### [14] `0378_PREREGISTRATION.md` — TNN/TNN/Research/R54_LEARNED_LOCAL_TEMPLATE_VISUAL_20260918/PREREGISTRATION.md, 859B, 2026-09-18
- **Finding:** R54 rationale: "hand-selected geometric summaries are the current visual bottleneck" → removes summary layer; learns 3×3 probabilistic occupancy template per randomized category directly from examples; translation via window search; margin-triggered active second view. Gates: clean ≥0.92, occluded ≥0.80, active ≥0.90.
- Quote: "R52 and R53 show that hand-selected geometric summaries are the current visual bottleneck. R54 removes that summary layer."
- Fills: vision lineage R54 design rationale (abandoned hand-selected summaries — why).

### [16] `0380_V4_PATCH_NOTES.md` — TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/V92_STATE_IMAGE_QUAL/V4_PATCH_NOTES.md, 843B, 2026-09-18
- **Finding:** Fourth znc compiler bug characterization (beyond baseline's ZNC-2026-09-19-001, wasm, arm64): range branches in `r27s4_count_valid` returning compound boolean expressions cast directly to `i32` did not produce the required `1` for valid scalars under the local Zag compiler — patch replaced casts with explicit `return 1` / `return 0` branches for PAM count, acoustic motif count, name count, trace count, development step, newborn restarts. No R27 values changed.
- Quote: "Under the local Zag compiler used by this lane, those return paths did not produce the required `1` for valid scalar values."
- Fills/extends: znc bug inventory — bool-cast codegen miscompile in `r27_native_state_sections_v4.zag`.

### [18] `0382_TNN_R28_AEIF_MEMORY_POLICY.md` — TNN/TNN/Research/TNN_R28_AEIF_MEMORY_POLICY.md, 808B, modified 2026-08-23 (pre-September program)
- **Finding:** R28 memory policy — the origin of the memory-policy stance. Birth/default `PRIVILEGED_HEURISTIC_DEFAULT` is researcher-authored bootstrap, "explicit hardcoding and is **not credited as learned cognition**." Authority: TNN owns storage decisions; learned experience may override/mutate/replace the default. LRU allowed only as eviction-order primitive after TNN chose representation/value policy (`LRU_REPRESENTATION_CONTROL` is a control, not canonical authority). Rationale: 12-seed R28 battery — pure LRU had higher raw recall but sacrificed exact-detail retention; heuristic-default + TNN-override had highest defined project utility and preserved substantially more exact evidence.
- Quote: "`PRIVILEGED_HEURISTIC_DEFAULT` is researcher-authored core bootstrap policy. It is explicit hardcoding and is **not credited as learned cognition**."
- Fills: design rationale for memory-policy/LRU stance + predates force-pin-as-law (no contradiction: override-right here concerns the default policy, not force-pinned memories). Dates the LRU-vs-judgment decision to 2026-08-23 with a 12-seed battery.

### [19] `0383_README.md` — TNN/TNN/Research/R34_NATIVE_CONTINUAL_LEARNER_V2/README.md, 777B, 2026-09-18
- **Finding:** R34 v2 moves learner into the persistent R33 world: observation packets, delayed touch consequences, hidden regime changes, latent context reuse, complete checkpointing, fresh-process continuation; reward policy + hidden regime state stay in `R33_CONTINUING_LIFE_V1/world.zag`; "The learner is never passed the regime bit."
- Quote: "The learner is never passed the regime bit."
- Fills: R34 v2 design (evaluator-blindness by construction).

### [27] `0391_README.md` — TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT/AGENT_FRONTIER_20260915/README.md, 607B, 2026-09-18
- **Finding:** V91 semantic-generator recovery lane mechanism: scanner searches repo/archive text for generator/dataset/RNG/sampling/model-forward/tokenizer-BPE semantics (historical Python treated as inert text, never executed); parity is fail-closed until exact generation semantics reproduce historical outputs without hardcoded oracle strings.
- Quote: "Actual V91 parity remains fail-closed until the exact generation semantics reproduce the historical outputs without hardcoded oracle strings."
- Extends: baseline's "historical recovery" entries — this is the V91 mechanism rationale (anti-oracle-string rule).

### [28] `0392_README.md` — TNN/TNN/Research/R33_REMEDIATION_20260915T2152Z/AGENT_ARCHIVE_SWEEP_20260915/README.md, 574B, 2026-09-18
- **Finding:** N17/R25/R26 exact archive recovery lane: sweep enumerates local tar/zip archives, streams candidate bytes to SHA-256 without executing/deserializing, records exact matches to the three known historical hashes. Admission rule: exact-hash only.
- Quote: "Admission is exact-hash only. Similar names, shadow states, witness receipts, and reconstructed artifacts do not close the historical verifier-equivalence rows by themselves."
- Extends: baseline's cancelled/unrecoverable historical-recovery efforts — the admission standard that governed them.

### [34] `0398_README.txt` — TNN/TNN/Research/R42_STATE_CONDITIONED_RELIABILITY_20260917/ATTEMPT0_RUNTIME_ABORTED/README.txt, 161B, 2026-09-18
- **Finding:** R42 (state-conditioned reliability, not in baseline) attempt 0: stopped for runtime throttling before aggregation; partial candidate rows not inspected and deleted before refreezing.
- Quote: "First orchestration attempt was stopped for runtime throttling before aggregation. Partial candidate rows were not inspected and were deleted before refreezing."
- Fills: first sighting of R42 + aborted-attempt handling rule.

### [35] `0399_restoration.results.txt` — TNN/TNN/Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_B_PROCESS_GAPS/restoration.results.txt, 152B, 2026-09-18
- **Finding:** Restoration anomaly worth a look: `c_restored expected=0 actual=127` and `full_reviewer_baseline expected=0 actual=127` in the first block (second block: expected=0 actual=0/1). 127 files restored against an expectation of zero — suggests unexpected restoration volume in recovery lane B; interpretation not self-evident from the file alone.
- Quote: "c_restored expected=0 actual=127 / full_reviewer_baseline expected=0 actual=127 / c_restored expected=0 actual=0 / full_reviewer_baseline expected=0 actual=1"
- Flag: flagged for parent — possible recovery-lane defect indicator, needs its context directory to interpret.

### [36] `0400_fs-inspect.txt` — TNN/TNN/.scratch/fs-inspect.txt, 130B, modified 2026-08-23
- **Finding:** Brain file copies on an external mount: `/mnt/data/tnn-v1-continue/tnn_v1.zag` and `/mnt/data/tnn-v1.0-research/src/zag/tnn_v1.zag`, both exactly 64,482 bytes (identical sizes). Dates provenance: 2026-08-23 scratch inspection.
- Quote: "/mnt/data/tnn-v1-continue/tnn_v1.zag 64482 / /mnt/data/tnn-v1.0-research/src/zag/tnn_v1.zag 64482"
- Fills: people/places anchor — tnn v1 brain existed on /mnt/data mounts.

## CONFIRMS (one line each)

- [10] `0374_README.md` (R33_N11_CLOSEOUT_SNAPSHOT_V1): N11 closeout snapshot discipline (SHA-256 verified, historical not rollback) — confirms R33 audit hygiene.
- [12] `0376_REVIEW_REQUEST.md` (R33_NATIVE_N19_RUNTIME_BOUNDARY): independent read-only review request enumerating no-learner/no-execution checks — confirms review-gate process.
- [15] `0379_INDEPENDENT_REVIEW_V2.md` (R33_NATIVE_N17_R27_CONTINUITY): N17 correction review REQUEST_CHANGES, N17 binary compile-only, not continuity evidence — confirms gate fired correctly.
- [17] `0381_INDEPENDENT_REVIEW_V1.md`: same lane V1 REQUEST_CHANGES for unfrozen parent inventory/verifier matrix — confirms review discipline.
- [22] `0386_INDEPENDENT_REVIEW_V2.md` (R33_NATIVE_N15_PRESERVATION_ADDITIVE): N15 V2 REQUEST_CHANGES over `N15_DEV_SELECTION,-1,0` sentinel handling — confirms independent review function.
- [23] `0387_AUTHORING_NOTES.md` (R33_NATIVE_N18_R27_FROZEN_CORE_SIDECAR): N18 is documentation-only, no binary/source/registry — confirms packet discipline.
- [24] `0388_INDEPENDENT_REVIEW_V3.md`: N18 V3 REQUEST_CHANGES (unresolved R27-to-sidecar mapping) — confirms review function.
- [25] `0389_INDEPENDENT_REVIEW_V2.md`: N18 V2 REQUEST_CHANGES (no registration path, mapping absent) — confirms review function.
- [31] `0395_README.md` (R32_E51G_NATIVE): E51G = preregistered matched value-function capacity discriminator in native Zag — confirms E51 frontier scope naming.

## NOISE (one line each)

- [04] `0368_umath-validation-set-README.txt`: numpy venv test-data README (ufunc validation instructions) — vendored dependency doc, unrelated to TNN.
- [20] `0384_R33_N12_CLOSEOUT_SNAPSHOT_VERIFIED.txt` / [21] `0385_R33_N12_CLOSEOUT_VERIFIED.txt`: identical SHA-256 checklists (all OK) — duplicate verification manifests.
- [26] `0390_R33_PROGRESS_CLOSEOUT_20260906_VERIFIED.txt`: all-OK checksum list for progress closeout — manifest only.
- [29] `0393_supplement.results.txt`, [32] `0396_supplement.results.txt`, [33] `0397_supplement.results.txt`: N19 recovery lane expected/actual row counts, all zeros (malformed_cli 2=2) — raw check rows, no interpretation.
- [30] `0394_R33_N11_CLOSEOUT_VERIFIED.txt`: all-OK checksum list — manifest only.
- [37] `0401_README.txt`: CPython venv site-packages README — vendored dependency doc.
- [38] `0402_README_EXECUTION.md`: placeholder ("recorded here only after native workflow evidence is available") — empty.
- [39]–[51] `0403_extra.summary.txt` … `0415_results.summary.txt`: single-line command-count summaries (`failures=0 commands=N`) from N19 recovery lanes — raw tallies, no interpretation. Note: [51] is truncated (`commands=` with no value).
- [40] `0404_summary.txt`: `verification_failures,0` — tally only.
- [41] `0405_current-source-analysis.txt`: `NO CANONICAL CANDIDATE` — single status line.

## Notes for the coordinator

- No contradictions with baseline found. Mild tensions noted but not loud: [08]'s "deterministic native RNG state" in an early R34 prototype vs the zero-RNG law (deterministic-given-state, so arguably compliant); [18]'s learned-override right vs force-pin-as-law (different objects: default policy vs pinned memories).
- No mentions of "koryphaios", "ghost", or other Micah projects. People/date anchors: build path `/Users/Shared/micah/Documents/zag/znc` (Micah's Mac znc compiler) in [08]; [18] and [36] dated 2026-08-23 (pre-September program).
- Batch-local manifest names (0000–0051) did not exist in docs_local; actual files are globally numbered 0364–0415 (batch7 entry i → 0364+i, verified by size match).
- Strongest NEW cluster: the R52→R58 vision lineage (5 preregs) — a full visual-generation sequence the baseline's R51–R54 note does not cover. Second: R28 memory policy origin (2026-08-23). Third: fourth znc compiler bug (bool-cast codegen).
