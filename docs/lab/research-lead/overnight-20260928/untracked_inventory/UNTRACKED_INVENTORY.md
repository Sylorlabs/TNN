# Untracked File Inventory

DRAFT. Inventory only. Nothing was deleted, moved, or modified.
Generated from `git status --porcelain=v1 -uall` (read-only) on branch
`tnn-native-lab`.

## Totals

- **3380 untracked entries**, 1,002,708,418 bytes (~956 MiB).
- Bundles capture committed history only, so none of this affects bundle v16
  contents. This inventory is for working-tree hygiene and for knowing which
  in-progress worker outputs still need committing.

## By top-level area

| Area | Files | Bytes | Class |
| --- | --- | --- | --- |
| `docs/lab/rsi/runs` | 338 | 935,221,340 (~892 MiB) | Unrelated scratch |
| `docs/lab/senses/rebuild` | 2029 | 36,133,305 (~34 MiB) | Unrelated scratch |
| `docs/lab/research-lead/overnight-20260928` | 1009 | 31,353,602 (~30 MiB) | Mixed (see below) |
| repo root (`err.txt`, `run1.err`, `run2.err`, `run3.err`) | 4 | 171 | Unrelated stray logs |

## Unrelated scratch (leave alone)

1. **`docs/lab/rsi/runs`** (338 files, ~892 MiB): old wave run outputs,
   dominated by `.bmp` frames under
   `runs/wave-20260924-0521pdt/dvid1v2/frames_base/` (each ~3.1 MB).
   Prior-cycle experiment artifacts, not TNN-2 work.
2. **`docs/lab/senses/rebuild`** (2029 files, ~34 MiB): senses rebuild
   scratch. File types: 925 `.truth`, 475 `.img`, 300 `.pcm`, 170 `.jpg`,
   150 `.vid`, 6 `.tmp`, plus driver/checker binaries. Not TNN-2 work.
3. **Repo root**: `err.txt` (0 bytes), `run1.err`, `run2.err`, `run3.err`
   (57 bytes each). Stray logs.
4. **Old experiment dirs** under `overnight-20260928` (prior cycles, not
   TNN-2): `hyp_c`, `form_invent`, `causal`, `wall_remove_impl`,
   `learner_substrate`, `hypd_v3`, `f2_ablation`, `threshold_boundary`,
   `q4_parcond`, `fint4_l1`, `rep_v2`, `inquiry_build`, `lifetime_exp`,
   `goal_revise`, `mul_rungb_build`, `core_freeze_tnn1_eval` (83 files,
   8.8 MB), `beam_g2`, `opscope_behav`, `policy_integration`, `c0integ`,
   `proc_amort`, `pilot_clean`, `f3_phase3`, `conditional_threshold`,
   `tnn1_build`, `learn_scale`, `revise_baseline`, `form_inventor`,
   `phaseb_pilot`, `valley_run`, `beam_impl`, `q4_baseline`, `hyp_pop`,
   `hyp_a`, `sem_l3`, `q4_adv2`, `pilot_impl`, `beam_g0`,
   `unified2_adversary`, `inquiry_refreeze`, `valley_satsuch`, `top_recruit`,
   `ddes_depth`, `causal_revert`, `threshold_redteam`, `proclang_baseline`,
   `hyp_c2_impl`, `lifetime_race`, `l3_bridge_impl`, `ddes_repair`,
   `greedy_impl`, `devang4`, `q4_r3`, `q4_reuse`, `ddes_adv`,
   `core_freeze`, `conditional_build`, `devang3`, `substrate_scale`, `ddes`,
   `continuing_learner`, `s10_impl`, `l3c_v2_adv2`, `c0integ_phaseb_impl`,
   `seg_redesign`, `verify_build`, `integration_step_d`, plus 7 files at
   the `overnight-20260928` top level. None of these are TNN-2 cycle
   deliverables; leave alone.

## TNN-2 related untracked (must be committed by owners before bundle v16)

Total: **~420 files, ~8.8 MB** across 4 worker directories.

### 1. `core_freeze_tnn2_eval/` (329 files, 4,348,880 bytes)

Owner: freeze evaluator worker (still running).
Contents: `FREEZE_REPORT.md` (the uncommitted draft with the wrong 5/9),
`NAMECHECK.md`, `grade_plan.zag`, `probe_score.zag`, compiled `_bin`
binaries, `run_fw_battery.sh`, `run_w_battery.sh`, `build_err.txt`, and
`runs/` with per-world outputs (`.out`, `.stderr`, `.rc`, `.hash`,
`.statehash`, `_state.bin`) for fw_run1 (fw1-fw5, fw6 variants) and more.
Status: no commit yet for this directory. Must land reconciled
(corrected 4/9, K-FZ2-4 determinism, W1-W9, post-run hashes) before bundling.

### 2. `tnn2_boundary/` (74 files, 3,985,470 bytes)

Owner: capability-boundary worker (still running).
Contents: `NAMECHECK.md` plus `probes/` with Zag sources (`base.zag`,
`p0.zag`, `pA.zag` through `pJ.zag`, `pX/pY/pZ.zag`, `*_main.zag`,
`mkprobe.sh`), compiled `_bin` binaries, and `p*_out*.txt` outputs.
Status: no commit yet. Must be committed before bundling.

### 3. `tnn2_transfer/` (8 files, 418,906 bytes)

Owner: transfer/reuse probe worker (still running).
Contents: `NAMECHECK.md`, `TRANSFER_ANALYSIS.md`, `build.log`,
`build2.log`, `probes_run1.txt`, `transfer_driver.zag`,
`tnn2_nomain.zag`, compiled `tnn2_transfer_bin`.
Status: no commit yet. Must be committed before bundling.

### 4. `h2_trapworlds/` (8 files, ~25 KB, actively changing)

Owner: H2 trap-world builder (just spawned, in progress).
Contents: `NAMECHECK.md`, `SEAL_H2.md`, `TRAPWORLD_DESIGN.md`,
`gen_h2.zag`, `substrate/R33_NATIVE_IO_V1.zag`, and
`worlds/h2a_world.txt`, `h2b_world.txt`, `h2c_world.txt`.
Status: no commit yet. Must be committed before bundling.

## Worker directories already committed (no action needed)

Since the bundle v16 prep inventory, these landed:

- `gw_eval/`: committed as `881fbb3d4`, message
  "GW1-GW8 adversarial battery evaluation: GW-EVAL-COMPLETE, 2/8 WORLD-PASS".
  NOTE FOR PARENT: the GW evaluator finished and committed while this
  inventory ran. Verdict headline only; report not inspected here.
- `tnn2_h2probes/`: committed as `4631c5918`.
- `tnn3_prereg_struct/`: committed as `206499c03`.
- `gap_bars/`: committed as `36e5a70e1`.
- `session_summary/`: committed as `2d213a972`.
- `bundle_v16_prep/`: committed as `801dc071d`.
- The documentation index (`INDEX_TNN2/`) was committed inside `881fbb3d4`.

## Missing

- `final_check/` does not exist yet; the final consistency checker worker
  had not created its directory at inventory time.

## Recommendation

Do not delete anything. The 4 TNN-2 worker directories above should be
committed by their owning workers when their work completes; bundle v16
creation remains gated on the freeze reconciliation and the GW evaluation
report, per the v16 verification checklist.
