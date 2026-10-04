# RUNLOG — JOB 1 red-team (2026-09-25)

## Pipeline check (§4): PASS
- Variant 20 re-run reproduces adopted m20 legs byte-identically
  (s1 `84ffaf89…`, s10 `20ff1d10…`, s100 `f6a38269…`).
- Re-scored bars match §1 adopted numbers. Toolchain `498abcb5…`.
- Note: `nec_v2d` uses `O_NOFOLLOW`; symlinked inputs fail rc=102.
  Use real paths.

## Battery freeze
- `ADDENDUM_V3B_JOB1_PRERUN_2026-09-25.md` + `gen_attacks.py` + 17
  batteries committed `5475c9fd` BEFORE any attack run.

## Attack runs (all A/B/C byte-identical, SHA-logged)
- RT-A `rta_s1` (300 rows), RT-B `rtb_s1` (100 rows, var 20 + var 11),
  RT-C `rtc_{base,v1..v6}` (7×120 rows), RT-D `rtd_s1/s10/s100`
  (200/3200/44000 rows), RT-E `rte_learn/fatigue/solo_*` (4 batteries),
  RT-F `rtf_collide` (100 rows).
- SHA log: `runs/sha_attacks.txt`.

## Analysis
- `bars_full.py` on analyzer legs; sim-vs-binary exact-rule checks
  (E1: 0/300 mismatches); solo-vs-in-battery independence (E2:
  byte-identical); G-curve white-box per battery.
- RT-F confirmed on binary (long ids 950×25). Root cause in
  `src/nec_v2d.zag` `nec_cmp_id` (63-byte cap).

## NEEDS-WORK fix round (FIX1)
- Pre-run addendum `ADDENDUM_V3B_JOB1_FIX1_PRERUN_2026-09-25.md`
  committed BEFORE fix validation.
- Fix: full-id compare via (ibuf offset, length) in slots.
- Validation: frozen matrix byte-identical s1/s10/s100; RT-F fixed;
  A/B/C deterministic. Evidence in `fix1/`, SHA-logged.
