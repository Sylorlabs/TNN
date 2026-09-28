# RUNLOG — B-3034COMP battery

**Crew:** B-3034COMP (PAM round-2 swarm, build crew)
**Date:** 2026-09-24
**Frozen prereg:** `d9e72746` (committed ALONE before code)
**Build:** `ad0e1ddd` (sources committed before runs)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)

## Build record

- `drive3034.zag` (new): SHA-256
  `1b1eb68ab4d0b704546b75ee0a6a7207cb7dcd59b6b6c53b5850d4b991e410b4`
- `b303134_common.zag` (from frozen `6e74ce54`, SHA-verified):
  `79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218`
- `R33_NATIVE_IO_V1.zag` (from frozen `6e74ce54`, SHA-verified):
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- `extract/`: script-extracted class definitions from frozen evidence
  `ec8d5d13` / `9f8ff63b` / `36b1d5fc2` (record: `extract/README.md`).
- Compile: clean, no warnings beyond the zagd-unavailable notice.
  Binary rebuilt from committed sources immediately before the runs;
  binary NOT committed.

## Battery

`run_battery.sh ./drive3034_bin ./runs` — 16 modes × 3 runs.
Result: **BATTERY_OK — 16/16 modes byte-identical across 3 runs.**
All stderr files empty. Per-mode run-1 SHAs in `runs/SHA256SUMS`:

| mode | run-1 SHA-256 |
|---|---|
| honest | a613ebb886ccce854659ef48ee82bc3d8fd1cf5a45d0b31a120c11e8da780f5b |
| rf_full | 7e39c5bb6c3670c0e9b4aaced64b3369499a379ed582682a2eaaac77ab8855b7 |
| rc_full | 52ff7d757745ecaf73895a25c34e0ed5fcbbe70a506211970b8b9b7517be99e3 |
| xr_fresh | a9d9d6844f477369f6b6084472f37721173e1016eea1da1e162f2a4dc431d759 |
| xr_reuse | 7928304b13e2f0ce58cd1ad537a9a1c33267c0ed2fc035e91cf5621ce9608d8a |
| n_goal | b57ef72d97736c46e034337765609d642a996643b99fb0935360720ef8807fea |
| o_temporal | 32bee404c21e1d9f34f527f68b9f287a158296a41d56d0ab57cf5a49ef4fd2aa |
| o_numeric | c1363880922b164e6f1d21a90888fcb3a7eb5ea82ef300d8d193249643885463 |
| p_remint | 6837401146a185c3acbde746d953fc81a43a5a9c0633efcf82549ef87fd40fef |
| j_dump | f44e6fb83a5dcf1b4fefae69b0351a5b15fe0af27544fa6b656de6c531baa540 |
| j_agg | 961020df50824bd61feb89ed738ff75a766ca62a405926fc5ebaa810500ec3cf |
| j_tag | 22c432dcfc40194e11a2b2ee2467beada37aef5179f4764dc911fdb3f489a6e5 |
| k_blind | 045981ecdf4d07b6dd651d46abf7b512ca61daa0f4662fc31684243c8564f863 |
| l_distal | e9d677e24042d0660883114cfc062a03b507cefd824260184c161029eda888de |
| ge_gap | 2a8a910f116edd3e8f85547987628f82947070b34663c86b2e47addac194368b |

Pure Zag, zero RNG. Deterministic fixtures: every fixture a pure function of
(mode, trial index, frozen constants).
