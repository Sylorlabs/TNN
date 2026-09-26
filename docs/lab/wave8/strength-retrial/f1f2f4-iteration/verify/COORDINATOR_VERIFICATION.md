# Coordinator verification log — F1/F2/F4 iteration (2026-09-26)

All builds with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Fresh builds (from the exact applied sources, this turn)

- `trial_f1a`, `f1_attack_a` — from `~/workspace/strength-f1f2f4/f1/` (fork A applied)
- `trial_f2a`, `f2_attack_a` — from `~/workspace/strength-f1f2f4/f2/` (fork A applied)
- `trial_f4b`, `f4_attacks_b` — from `~/workspace/strength-f1f2f4/f4/f4b/`
- `f4_attacks_pristine` — `f4_attacks.zag` built against the PRISTINE,
  md5-verified-unmodified `f4/r4val/trial/` sources
  (strength_core.zag md5 `4c928c29b9a2d4fc79d153fecba1e381`)

## Honest-cell checks (B × VUP × var 0 × S1)

| binary | output | vs frozen evidence |
|---|---|---|
| trial_f1a | trial_f1a_BVUP0.log | byte-identical to `evidence_r4f/cell_B_VUP_0_r1.log` |
| trial_f2a | trial_f2a_BVUP0.log | byte-identical to `evidence_r4f/cell_B_VUP_0_r1.log` |
| trial_f4b | trial_f4b_BVUP0.log | byte-identical to `evidence_r4f/cell_B_VUP_0_r1.log` |

## Attack spot-checks (full batteries run; key lines)

- f1_attack_a.log: `F1_A1 wk_rc=0 j_rc=0 ow_rc=109 cf=0` (closed),
  `F1_A2 wk_rc=0 j_rc=0 ow_rc=109 cf=0` (closed).
- f2_attack_a.log: `F2_A1 origA3 wk_rc=0 ow_rc=0 before=10 after=50 checker_failures=1`
  (flagged; ck_ow_effort 1 vs 4).
- f4_attacks_b.log: `FA_A5 ... ow_rc=121` (closed),
  `FA_V4 ... recite_rcs=111,111,111,111 ... ow_rc=121` (closed),
  `FA_V1 ... kill_evidenced_rc=0` (legitimate pass, per report §5).
- f4_attacks_pristine.log: runs FA_A5, FA_V1, FA_V1B (ke2_rc=0 — the F4 hole,
  present in pristine), then **`panic: slice index out of bounds`** — the §1
  base defect reproduced on unmodified sources. Exit code 1.

## Source-structure checks (this turn)

- F1: both checker copies byte-identical; `st_epoch_highwater` present in both
  cores + both checkers; trial/learner sources unchanged.
- F2: both cores pristine vs `pristine_backup/` (diff empty); both checker copies
  byte-identical; `ck_birth_idx`/`ck_high_water` present in both checkers.
- F4b: both checker copies byte-identical; `st_cite_consumed` /
  `st_count_spent_cites` present in both cores; root↔trial core copies differ
  only by the test-only `st_overwrite_direct` hunk (verified by diff).
- F4a vs pristine core: 25-line diff (10 changed lines per report).
