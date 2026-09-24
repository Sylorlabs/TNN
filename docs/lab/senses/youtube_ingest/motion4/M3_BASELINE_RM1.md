# M3 baseline on RM1 — 2026-09-24 (measurement only)

Frozen motion3 binary (verdict binary, md5 `fefb7a46ef33b8a10f5232ad34af3f94`)
run once per RM1 clip. This is the M3-side record for MOTION4 K3 baseline
(prereg §7: "M3 baseline on this subset: measured once with the frozen
motion3 binary, expected ≈0%").

## 6px subset (96 kill clips)

- Correct-direction CANDIDATE: **1/96 = 0.010** (≈0% as expected)
- The single hit: `rm1_t11_W6.vid` (uKNQCPXDNdc_w093 texture), judged
  W CANDIDATE, reason=coherent — lucky alignment of the ±2px grid on
  that texture, not tracked motion.

## False judgments (204 kill clips)

- **0** (expected 0). No CANDIDATE judgment was wrong on any kill clip.

## Supplementary distributions (all 252 clips, kill + exploratory 8px)

| truth | correct-CANDIDATE | WITHHOLD |
|---|---|---|
| 3px/frame × 8 dirs | 58/96 | 38/96 |
| 6px/frame × 8 dirs | 1/96 | 95/96 |
| 8px/frame × 4 cardinal (exploratory) | counted in totals above | |
| STILL | 12/12 STILL CANDIDATE (exact_still) | 0 |

Full per-clip table: truth in each clip's `.vid.truth`; binary stdout
compared judgment/decision against truth dir.

## Binary-anomaly follow-up (BUILD_NOTES.md §"Binary anomaly")

The single divergent run (`windows/OQSNhk5ICTI_w153.vid`, S/e_total=146801
vs correct N/150360) was re-tested: 20/20 consecutive runs of the frozen
binary return (N, e_total=150360). The divergent result did not reproduce
— consistent with the original documentation (100+ clean runs, Python
cross-check bit-exact). Cause remains unknown; verdict numbers all come
from verified runs.

## Determinism

RM1 generator is zero-RNG; 3 runs → byte-identical manifest
(sha256 `68e264630718e90d50cac9e8d580b5aaa95aaa6c4f0090357253e9e7aee16c3e`).
