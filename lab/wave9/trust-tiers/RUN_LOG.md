# RUN_LOG — Wave 9 trust-tiers campaign matrix (RUN worker)

**Date:** 2026-09-20 (PDT) · **Worker role:** RUN only (execute matrix, no result interpretation)

## Commands executed (exact)

```bash
cd ~/workspace/tnn-lab/wave9/trust-tiers/substrate
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 trust_tiers.zag \
  --no-zagd --no-analyze --no-foreground-cache -o trust_tiers.bin
./run_matrix.sh purity
./run_matrix.sh smoke
~/workspace/tnn-lab/wave9/trust-tiers/run_matrix_s1.sh   # background
~/workspace/tnn-lab/wave9/trust-tiers/run_matrix_s10.sh  # background, after S1 clean
```

## Source shas (pre-build, proves what was compiled)

- `trust_tiers.zag`        `91063bf7e55d8533d5e1c3bcfb97d72f2977128513e93fce7770cf838d64614f`
- `st_memory_core.zag`     `474ac0bb2417f26e531450a4fa406662aa733138eeaf622f454222509834da8d`
- `cl/common.zag`          `8aec83cb4feb83a20bc91c8179d7055d691c155414a359f7014386271aa6168b`
- `R33_NATIVE_IO_V1.zag`   `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- `R33_NATIVE_SHA256_V2.zag` `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`
- `run_matrix.sh`          `201a1367ebaae6f39016a8d6eba5c9d58a95c0f41e098eb1d066dce7b139f323`

Build command identical to BUILD_NOTES.md; compiled clean, binary `trust_tiers.bin` (276440 bytes) produced fresh from source. Binary was NOT committed (per instruction).

## Static gates (before matrix)

- `run_matrix.sh purity`: invalid-selector rejections (64/65) OK; Arm-B tier-purity OK.
- `run_matrix.sh smoke`: T/N/B paired A1 runs byte-identical (required smoke).

## A0 arm-T-only handling

Checked `run_matrix.sh full`: it skips arms N/B for A0 (`if [ "$camp" = "A0" ] && [ "$arm" != "T" ]; then continue; fi`) — no deviation needed. My S1 runner (`run_matrix_s1.sh`) applies the same rule. Executed cell count is therefore **792 cells / 1584 runs** (not 1728): 8 campaigns × 3 variants × 12 instances × 2 runs × 3 arms = 1728 minus the 144 non-T A0 executions excluded by the amended prereg §3.

## S1 matrix (SCALE=1, 500 episodes)

- Cells completed: **792** (1584 executions)
- Paired-run divergences: **0** (all RUN=0/RUN=1 stdout pairs byte-identical)
- RC failures / non-zero exits: **0**; non-empty stderr captures: **0**
- `evidence/s1/`: 792 × `.run0.log` + 792 × `.run1.log`, plus `cells.sha256` manifest (1584 entries, `sha256sum -c` → ALL OK). No `DIVERGENCES.txt` produced.
- Log naming: CELL = `{ARM}_{CAMP}_{VARIANT}_{INSTANCE}_{SCALE}` (e.g. `T_A1_0_00_1`); files `{CELL}.run0.log` / `{CELL}.run1.log`. Sample log head confirms selector fields: `ST_CELL,T,A1,0,0,S1,500`.
- Wall-clock: ~26 min (S1 runner: ~1.5–2.0 s per execution).

## S10 stretch (conditional, prereg V2 §11)

- Authorization: S1 completed with **zero INVALID findings** (0 divergences, 0 failures) → stretch ran.
- Matrix: arms {T, N} × campaigns {A1..A6} × variant {0} × instance {00} × runs {0,1} × SCALE=10 — **12 cells / 24 executions**. A0, A1-MS, N0 excluded per §11.
- Divergences: **0**; RC failures: **0**.
- `evidence/s10/`: 12 × `.run0.log` + 12 × `.run1.log`, `cells.sha256` (24 entries, `sha256sum -c` → ALL OK). Sample log head: `ST_CELL,T,A1,0,0,S10,5000` — confirms 5000-episode horizon.
- Wall-clock: ~82 s.

## Anomalies

**None.** No divergence, no crash, no unexpected exit code, no skipped cell, no stderr output anywhere, no manifest mismatch. Matrix was not stopped at any point. No re-runs of any cell.

## RUN_SUMMARY

| arm | campaign | S1 cells | S1 divergences | S10 cells | S10 divergences |
|-----|----------|----------|----------------|-----------|-----------------|
| T | A0 | 36 | 0 | — | — |
| T | A1 | 36 | 0 | 1 | 0 |
| T | A2 | 36 | 0 | 1 | 0 |
| T | A3 | 36 | 0 | 1 | 0 |
| T | A4 | 36 | 0 | 1 | 0 |
| T | A5 | 36 | 0 | 1 | 0 |
| T | A6 | 36 | 0 | 1 | 0 |
| T | N0 | 36 | 0 | — | — |
| N (T-NC) | A1 | 36 | 0 | 1 | 0 |
| N (T-NC) | A2 | 36 | 0 | 1 | 0 |
| N (T-NC) | A3 | 36 | 0 | 1 | 0 |
| N (T-NC) | A4 | 36 | 0 | 1 | 0 |
| N (T-NC) | A5 | 36 | 0 | 1 | 0 |
| N (T-NC) | A6 | 36 | 0 | 1 | 0 |
| N (T-NC) | N0 | 36 | 0 | — | — |
| B | A1 | 36 | 0 | — | — |
| B | A2 | 36 | 0 | — | — |
| B | A3 | 36 | 0 | — | — |
| B | A4 | 36 | 0 | — | — |
| B | A5 | 36 | 0 | — | — |
| B | A6 | 36 | 0 | — | — |
| B | N0 | 36 | 0 | — | — |
| **total** | | **792** | **0** | **12** | **0** |

Each (arm, campaign) S1 count = 3 variants × 12 instances = 36 cells. Divergences = 0 everywhere. Ready for CHECK worker.
