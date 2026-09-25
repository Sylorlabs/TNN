# F21 GRAF — Build Log

## Frozen inputs (verified)
- Prereg: `fork_round/PREREG_FORKROUND.md` FROZEN v1 (coordinator sign-off 2026-09-25).
- Ideas: `fork_round/ideas/native1_forks.md` Fork 2 (authoritative on discrepancy).
- Training: `training/features/features.tsv`, SHA-256
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`.
  **NOTE — single-char transcription typo in PREREG_FORKROUND.md §2** (and in the
  fork brief): the frozen prereg records `…f04e65e897d`; the on-disk file is
  `…f04e65a897d`. The on-disk hash matches SIX earlier frozen records
  (v2/PREREG_TRAINING_V2.md, v2/VERDICT.md, backlog/t05/PREREG_T05.md,
  sr_round/PREREG_SR.md, sr_round build logs) — the file is the true frozen
  artifact; the fork-round prereg's hash has the typo. Data is trustworthy;
  typo recorded here and in VERDICT.
- Toolchain (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Harness modules copied byte-identical (SHA-verified) from `training/src/`:
  R33_NATIVE_SHA256_V2.zag, R33_NATIVE_IO_V1.zag, dlb_util.zag, dlb_json.zag,
  dlb_cfg.zag, dlb_ledger.zag, dlb_delib.zag, policy.zag, mt_gate.zag.

## Frozen hyperparameters (before first training run)
- params/FROZEN_HYPERPARAMS.md: **λ=1, μ=4**, init w1=1000, w2..w8=0, b=0.
- Objective (literal frozen formula, i64):
  L = Σ_r n_r·G(r)² + λ·Σ(c−y)² + μ·Σ max(0, c_d−c_prev),
  G(r)=trunc(1000·Σ(c−y)/n_r), y∈{0,1000}, rungs=(family×depth) over
  released training cells (heldout=0, rel4=1); μ-adjacency = consecutive
  released training cells of the same item in ascending depth order.
- Optimizer: deterministic integer coordinate descent, sweep order
  w1..w8,b; per param try +step then −step; first strict L decrease
  accepted; phases ±8 then ±1 to full-sweep convergence.

## Build & training
- `src/train21.zag` written per spec ([]u8 arenas, LE accessors, no zalloc,
  no slice >2^25, native trunc-division matching policy.zag pl_conf exactly).
- Trainer built A/B with pinned znc: byte-identical.
- Training run TWICE on frozen features.tsv: rc=0 both; params byte-identical
  (`34848abf…e2f6d6651e7`), moves logs byte-identical. §8 determinism gate: PASS.
- Fit: L 395352720889719 → 57589098954757 (6.9×), 1041 accepted moves
  (664×−8, 376×+8, 1×−1), full-sweep convergence both phases.
- Independent Python replica of L at final weights: EXACT match
  (57589098954757) — objective implementation verified.
- Final weights: w=(2296,−1504,0,−1968,176,−353,768,−792), b=72.
  §5 checkpoint: weights ≠ init. PASS (liveness signal: 1041 strict-improvement moves).
- Training-set non-degeneracy: meanConfCorrect=0.979, meanConfWrong=0.189,
  separation=0.790; clamp0=3.1%, clamp1000=58.5%.

## Objective-scale observation (recorded, NOT re-weighted)
G(d) as literally specified is 10⁶× the analyzer's G(d) (fixed-point
precision scaling: 1000·Σ(c−y)/n with (c−y) in thousandths). The rung term
therefore outweighs the λ term ~10⁶× and the μ term ~10⁹× in commensurate
units (final L: rung 5.7589e13, λ 7.18e7, μ 2.15e5). The fitter effectively
minimized ΣnG² almost alone. Per round rules this is NOT silently
re-weighted; falsification (b) adjudicates misweighting. The literal
formula is what the ideas file (authoritative) and the brief both state.

## Policy build
- `work/build_policy.sh`: polbuild_a/b trees, pinned znc, A/B byte-identical.
- policy_bin sha256: `3ef3fb40f5948e473bebdaa567c456c2d15943e969395776194699e37d44e100`.
- Gate arg: 0 (MT-CONF; F21 has no learned gate — head unchanged).
  (v2/work/run_eval.sh hardcodes gate01=0; policy.zag documents 0=conf-only.)

## Eval
- `run_eval.sh full <policy_bin> 21 0` → 37 legs × A/B (logs/eval_full.log).
- Analysis: frozen `training/analyze.py` on results_full, mechs 21 (+4 for B9).
