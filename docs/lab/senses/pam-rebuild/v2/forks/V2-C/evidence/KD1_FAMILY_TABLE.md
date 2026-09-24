# KD-1 family table — V2-C measured (dmask=4095, run 1 of 3; runs 2–3 identical)

Frozen R2-4 baseline: 1,075 adversarial wrong-high-confidence judgments
(from `round2/forks/R2-4/evidence/clean`, per PREREG_V2-C_AMEND1.md §3).

| Family | n | R2-4 baseline | V2-C measured | Reduction | Detector | Note |
|--------|---|---------------|---------------|-----------|----------|------|
| PTC-2 | 400 | 400 | 0 | 100% | D1 glide-gate | caps to 650; fired on 400/400 |
| CCN-1 | 340 | 335 | 335 | 0% | D3 | NEVER FIRES on R2A fixtures (see D3_DEVIATION.md) |
| COL-2 | 350 | 313 | 313 | 0% | D4 disabled | per frozen calibration |
| CCN-2 | 340 | 17 | 17 | 0% | D5 | no reduction on wrong-HC |
| TMB-1 | 250 | 6 | 6 | 0% | D9 disabled | per frozen calibration |
| harness adv | 185 | 4 | 4 | 0% | — | — |
| all others | — | 0 | 0 | — | — | — |
| **Total** | **5,815** | **1,075** | **675** | **37.2%** | | **FAIL vs ≤537** |

KD-1 measured = 675 (identical in all 3 runs).
