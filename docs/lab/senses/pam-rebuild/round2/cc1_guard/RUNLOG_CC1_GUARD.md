# RUNLOG — CC1 margin-guard experiment (PAMs Round 2)

## Prereg
- Frozen prereg committed ALONE: `a673da8aa9481194992a38963eb7b99074fe1f5e`
  (tnn-native-lab, 2026-09-24).
- Files: `PREREG_CC1_GUARD.md`, `gen_guard.py` (single source of truth —
  the md tables, EXPECT_GUARD.tsv, EXPECT_GUARD_CELL.tsv, and
  src/guard_records.zag are all generated from it), `EXPECT_GUARD.tsv`,
  `EXPECT_GUARD_CELL.tsv`.
- No execution artifacts existed at prereg commit time.

## Build
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Command: `znc_linux_x86_64_abed8aa1 src/guard_main.zag -o build/guard_bin`
  (run with cwd=`src/`, so the `@import("guard_records.zag")` and
  `@import("R33_NATIVE_IO_V1.zag")` resolve locally).
- Build output: `znc: wrote native binary .../build/guard_bin (176212 bytes
  main, 0 external tools)` — one warning only (`zagd unavailable`, benign).
- `src/R33_NATIVE_IO_V1.zag` is a byte-identical copy of the frozen
  contradiction-matrix file
  (sha256 `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`).
- Workdir `~/workspace/pam_round2/cc1_guard/` (never /tmp).
- Binary NOT committed (build/ is local only).

## Runs
- Three full runs: `./build/guard_bin > evidence/runN.txt` (N=1..3).
- sha256 (all three):
  `14fc017a4a0dddf9a8dc3cea1db647a8759c363b46095f79516bca0ae67ae12f`
  — byte-identical across runs. Zero RNG; all inputs literal.
- 553 output lines per run = 79 trials × 7 configs.

## Scoring
- `python3 score_guard.py evidence/run1.txt prereg/` → exit 0,
  **fidelity 154/154 (cell, config) PASS** (full table in
  `evidence/score.txt`).
- Kill bars computed INDEPENDENTLY from run output + `gen_guard.py` cell
  metadata (not from EXPECT): MG1=KILL, MG2=KILL, MG3=KILL, MG4=KILL,
  MG6=SURVIVE (details in `evidence/score.txt` tail + VERDICT).
- V9 ceiling probe (unscored): all 7 configs false-install, as preregistered.

## Notes / deviations
- None. The battery reproduced the frozen known-unsafe baseline exactly
  (G1/G2 `PROV,PERM,CHAL,REV` + false install on CC1/V1/V2/V4/V5/V6/V7/V8;
  no corroboration on V3) and every guarded disposition matched the
  hand-derived EXPECT tables on the first run.
- Implementation note (prereg §8-adjacent): MG2's asymmetry test against a
  non-permanent incumbent is vacuous by construction (perm mrgF reads 0 from
  zeroed state, so the factor test passes); no fixture exercises that path.
- Truth handling: the string "truth" appears in guard_main.zag only in
  comments; gate/guard functions take (prog, jcode, conf, pred, meas, mrgF,
  jG, confG, seq, span_a, span_b) — truth is structurally unreadable.
  Guards additionally never read jG/confG (judgment-channel ban).
