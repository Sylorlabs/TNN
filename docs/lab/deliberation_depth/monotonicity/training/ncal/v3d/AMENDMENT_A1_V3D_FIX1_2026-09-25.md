# AMENDMENT A1 — v3d head-to-head: Micah's FIX1 ruling (2026-09-25 ~11:50 UTC)

- **Date:** 2026-09-25 (PDT). **Status:** dated amendment to the frozen
  `PREREG_NCAL_V3D_H2H_FROZEN.md` (committed `695997f5`). No measurement
  already taken is invalidated by this amendment.
- **Trigger:** Micah's ruling 2026-09-25 ~11:50 UTC — "Design S adoption WAITS
  for the speed/cost/catches head-to-head. FIX1 (63-byte ID cap removal)
  APPLIES NOW. FIX-A (pure-Zag port) APPLIES NOW. Dispatched."

## What changes

**Nothing about the contenders or the legs.** The frozen contenders
(variant 20 = adopted m20, variant 26 = Design S, both WITHOUT FIX1) stand,
because FIX1 is orthogonal to the design difference under test:

1. FIX1 changes only `nec_cmp_id` (the shared id-lookup: 63-byte cap →
   full-id compare). It is in the SHARED code path, identical for variants
   20 and 26 — not in either variant's tp=0 branch.
2. The job-1 FIX1 verdict proved "zero behavior change on ids ≤63, proven
   byte-identical" — every battery in this round except RT-F uses ids ≤63,
   so all SPEED and COST numbers and all non-RT-F CATCHES numbers are
   invariant to FIX1.
3. On RT-F itself, FIX1 flips BOTH contenders from miss to catch (the break
   is the same implementation defect on both sides) — the RT-F row stays a
   tie either way.

## What is recorded

- FIX1 is dispatched as its own workstream and applies to the adopted NEC
  mechanism now, per Micah's ruling — independent of this round's outcome.
- Whichever contender this round recommends, the recommendation is read as
  "<contender> + FIX1" (and + FIX-A pure-Zag port, likewise dispatched).
- The decision table's RT-F row is scored as-measured (both miss, same
  known break) with the FIX1-applied projection noted (both catch, tie
  preserved).

## Checklist delta

- [x] This amendment committed BEFORE the verdict (no scored leg re-run needed)
- [ ] VERDICT_V3D.md states the recommendation as "<contender> + FIX1"
