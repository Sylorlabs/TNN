# CRITIC 3 (anti-PAR) — RUNLOG

## 2026-09-24 ~20:20 PDT — setup
- Read TOURNAMENT_SYNTHESIS.md (§4 cross-path map), crew_paths MATRIX.md
  (batteries, fable challenger tests, cost-honesty defect), crew_a VERDICT.md.
- Chose cell: IMAGE RASTER. A's recorded numbers: PERM 0 diffs, COH 0/180 vs
  nat 72/180, CASCADE 168 px / 1 quadrant, COST 55.6 ms vs nat 17.2 ms
  (LATENCY-1 wall clock, disclosed but never folded into the cell verdict).
- Attack design: S-CONF — contender B's structural scaffolding (2×2 tiles,
  per-tile state wiped between tiles) with a confluent merge (z-buffer +
  winner-index max-reduction) instead of B's non-confluent LUT re-seed.
  Hypothesis: B/C lost on merge confluence, not on statefulness.
- Wrote PREREG_CRITIC.md (bars B1–B8, overthrow condition, no-regression
  rule, map-reasoning note on the §6-analog COST question).

## ~20:28 PDT — prereg committed BEFORE any experiment
- `gh-api PUT .../critics/anti_par/PREREG_CRITIC.md` → blob
  `ae7fd984a7dc776d0218d15c5d72b832226e6e2a`, commit `28856c51d5efa9a32484071de2f0f918d0acc88f`
  on tnn-native-lab.

## ~20:31 PDT — baseline
- Fixture SHA-256: `254fa6bb9371659354801d11d694b689378560eb46e6e412f3987ede27c2b9e8`.
- `src/imgraster.zag` SHA-256: `744ca9a8ad843c0c8ffa81fc7d9e44c600e8793defd8d862660da4c3718bbb0a`.
- Built with pinned `znc_linux_x86_64_abed8aa1` → `imgraster_base`
  (SHA-256 `9f4ffc6485abe48b21e4d0c478789a2de3803a1a56fb75b6d52b144f2789496d`).
  Build warnings pre-existing (A0107 dead-loop false positives in
  f_read_all/f_write_all, A0102) — no errors.
- mode a render SHA-256 `0820a18b9a71d673c23c29a0decb60b1010db166b8cbe3935d16587be868c1d6`
  — matches recorded pre-clobber prefix `0820a18b9a71`. nat render matches
  `19e0a7eb2189`. Baseline reproduces the tournament exactly.

## ~20:35 PDT — S-CONF built
- `s_conf.zag` (helpers copied verbatim from imgraster.zag; new main with
  per-tile zbuf/idxb arenas — []u8 + p32/g32s per the ZNC-007 arena rule,
  never `as []i32`). Source SHA-256
  `e6e598ee3fc53e39a48e8e49a60e621223ef07769c8eb3b2550db91e12a4122e`.
- First render: byte-identical to A's (`0820a18b9a71…`, `cmp` clean).

## ~20:40 PDT — bars B1–B4, B6 (`s_battery.py`, tournament methodology)
- B1 DET PASS (S×2 cmp-clean; S SHA == A SHA full 64 chars).
- B2 PERM-analog PASS (scr/pscr2/tscr all cmp-clean).
- B3 LEAK PASS (outside tile 0: 0 diffs; inside: 512 — poisoned tile 0
  renders all-bg; the 512 = tile 0's non-bg pixels in the clean render).
- B4 CASCADE PASS — all 8 corruptK byte-identical S vs A; K=7: 168 px,
  1 quadrant `[0,168,0,0]`, exactly A's recorded numbers. (corrupt4 spans
  4 quadrants/280 px for BOTH — byte-identity is the stronger claim.)
- B6 COH PASS — 0/180.

## ~20:45 PDT — bar B5 CASCADE+ (`s_cascade_plus.py`)
- 16 corrupted plan files generated from the frozen fixture (Python, no
  hand edits): corruptzK (prim K z→99), corruptgK (prim K width×2).
- ALL 16: S byte-identical to A. Footprints exactly A's: corruptz2 = 64 px
  (P2 newly wins the designed file-order/z-order overlap — 1 quadrant);
  corruptz0/1/4/5/6/7 = 0 px (already-max-z prims, correctly no change);
  corruptg range 48–736 px / 1–3 quadrants.

## ~20:50 PDT — bar B7 COST, first attempt
- `/usr/bin/time` missing on this VM → substituted bash `time` builtin
  (M1', wait4-based, independent of Python's os.times()).
- M1': a 8.0 ms / s 2.0 ms (s/a = 0.25).
- M2 first try (`os.times()` children): a 0.00/0.01/0.01, s 0.00/0.00/0.00 —
  10 ms quantization unresolvable, script reported FAIL. This is a method
  resolution failure, not an effect failure (M1' already resolved it).
- Re-ran M2 with `os.wait4` rusage (µs resolution; the matrix's other
  prescribed valid method): a 7.5 ms / s 1.6 ms (s/a = 0.21). B7 PASS.
- RSS (fresh-process RUSAGE_CHILDREN max): a 11596–11652 KB / s 11496 KB.
- Wall-clock corroboration (LATENCY-1 style perf_counter, min-of-5):
  a 73.4 ms / s 18.5 ms (0.25). Ratio stable across all three methods.
- Extra: nat child-CPU 0.9 ms → a = 7.9× nat, s = 1.6× nat.

## ~20:55 PDT — bar B8 reruns
- Full battery + cascade+ re-run from scratch (artifacts deleted first):
  both logs byte-identical to run 1; SHAs stable.

## Decisions / judgment calls
- M1 method substitution (/usr/bin/time → bash time) and M2 method fix
  (os.times → wait4) were measurement-harness repairs, not bar changes:
  the bar ("honest child CPU, two independent methods, s<a strictly")
  is unchanged from the prereg.
- The prereg's B2 PERM-analog (prim/tile order scrambles instead of the
  battery's pixel-order scramble, which is meaningless for a stamp
  renderer) was used as written — no post-hoc change.
- No second implementation attempt was needed (first attempt passed all
  bars).

## Artifacts (workdir `~/workspace/par_critics/anti_par/work/`, not committed)
- `s_conf.zag`, `s_conf` binary, `imgraster_base.zag`/`imgraster_base`
  (tournament source copy + rebuilt baseline binary)
- `s_battery.py`, `s_cascade_plus.py`, `s_cost.py`
- `run1_battery.log`, `run2_battery.log` (byte-identical),
  `run1_cascadeplus.log`, `run2_cascadeplus.log` (byte-identical),
  `run1_cost.log`, `run2_shas.txt`
- `plan_z0..7.txt`, `plan_g0..7.txt` (generated corrupted plans)
- Rendered `.raw` files (withheld from review per battery convention)
