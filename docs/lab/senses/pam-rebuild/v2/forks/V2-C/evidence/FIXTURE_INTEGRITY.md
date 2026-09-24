# Fixture integrity — V2-C battery

**Date:** 2026-09-24
**Generator:** `~/workspace/pamv2_gapA/r2a_gen.py`, MASTER seed 20260923,
  deterministic (no RNG in outputs). Started 2026-09-23 18:47 UTC, exited
  cleanly 2026-09-24 (exact target reached: resumable skip logic stopped at
  10,915 pairs).

## Counts (frozen spec §5: 21,830 files)

- `.r24` fixtures: 10,915
- `.r24.truth` files: 10,915
- Total: 21,830
- Zero-size files: 0
- Orphan `.r24` (no truth): 0
- Orphan truth (no `.r24`): 0

## Per-family counts

| Task | Family | n |
|------|--------|---|
| colordisc | normal (r2n) | 1,080 |
| colordisc | COL-1 | 400 |
| colordisc | COL-2 | 350 |
| colordisc | COL-3 | 400 |
| colorconst | normal (r2n) | 720 |
| colorconst | CCN-1 | 340 |
| colorconst | CCN-2 | 340 |
| motiondir | normal (r2n) | 564 |
| motiondir | MOT-1 | 350 |
| motiondir | MOT-2 | 350 |
| motiondir | MOT-3 | 295 |
| pitchdisc | normal (r2n) | 720 |
| pitchdisc | PTC-1 | 350 |
| pitchdisc | PTC-2 | 400 |
| pitchdisc | PTC-3 | 400 |
| shapetrans | normal (r2n) | 1,296 |
| shapetrans | SHP-1 | 400 |
| shapetrans | SHP-2 | 450 |
| shapetrans | SHP-3 | 300 |
| timbredisc | normal (r2n) | 720 |
| timbredisc | TMB-1 | 250 |
| timbredisc | TMB-2 | 250 |
| timbredisc | TMB-3 | 190 |
| **Total** | | **10,915** (5,100 normal / 5,815 adversarial) |

Harness fixtures (pre-existing, `senses/rebuild/harness/fixtures`): 925
(370 primary + 370 noise + 185 adversarial). Battery total: 11,840.

## Determinism spot-check

9 fixtures regenerated from `r2a_gen.py` in a clean directory
(r2n_colordisc_0000/1079, r2a_colorconst_CCN-1_000, r2a_pitchdisc_PTC-2_000/399,
r2a_motiondir_MOT-1_000, r2a_shapetrans_SHP-1_000, r2a_timbredisc_TMB-2_000/249):
all byte-identical to the generator's files (fixture + truth).
