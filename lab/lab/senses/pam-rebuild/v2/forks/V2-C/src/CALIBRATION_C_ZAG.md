# V2-C Pure-Zag Calibration (Frozen)

**Date:** 2026-09-23  
**Status:** FROZEN — thresholds locked before R2A evaluation.  
**Amendment:** `senses/pam-rebuild/v2/preregs/PREREG_V2-C_AMEND1.md` (commit b81fa1b6693ee792a37f1ea4f7ba88eb3dfb821c)

## Calibration Method

All thresholds calibrated SOLELY on the 370 harness NOISE fixtures (60 colordisc, 40 colorconst, 90 shapetrans, 60 pitchdisc, 60 timbredisc, 60 motiondir). 

**Principle:** 0 false alarms on NOISE. A detector that fires on clean/noised trials is either refined until it achieves 0 FA, or disabled with documentation.

**Constraint:** No R2A fixtures were inspected or evaluated during calibration. Thresholds frozen before R2A generation completed.

## Frozen Detector Definitions

### D1: PTC-2-GLIDE (bit 0)
- **Measure:** `m1_glide` — max |endpoint - neighbor| over 4 endpoints × 2 neighbors, on the 32-band onset profile. Returns 0 if clean single glide detected.
- **Threshold:** `thr_ptc2_glide() = 150` (10× units)
- **Fires:** if `m > 150`
- **NOISE:** 0/60 fire (all 0)
- **Status:** ACTIVE

### D2: PTC-1-HARM (bit 1)
- **Measure:** `m2_harm` — binary consistency: 1 if f0_h2 peak is inconsistent with integer harmonics 1–4, else 0.
- **Threshold:** binary (fires if `m != 0`)
- **NOISE:** 0/60 fire (all 0)
- **Status:** ACTIVE (conservative; may have low recall)

### D3: CCN-1-TEXCORR (bit 2)
- **Measure:** `m3_opposite` — 1 if panels have opposite extreme casts (panel1 blue-dominant AND panel2 red-dominant, or vice versa), else 0. Blue-dominant: b > 2r AND b > 2g. Red-dominant: r > 2b AND r > 2g.
- **Conjunction:** also requires `vknow_texcorr >= 9500` (Pearson r × 10000)
- **NOISE:** 0/40 fire
- **Status:** ACTIVE (refined from ratio-based; opposite-cast is the structural signature)

### D3b: CCN-1-SIM (bit 3)
- **Status:** DISABLED (threshold set to 1,000,000, impossible)
- **Reason:** Fired on 1/40 NOISE (p030.img, clean SAME_SURFACE). The sim's "ratio>5 & bright<85" form is not specific enough. D3 (opposite-cast) covers the CCN-1 family.

### D4: COL-2-DRIFT (bit 4)
- **Measure:** `m4_drift` — 10×L1 drift between panel2 left-half and right-half channel means; `m4_var` — texture variance; `m4_corr` — Pearson r × 10000.
- **Thresholds:** `thr_col2_drift() = 30`, `thr_col2_var() = 400`, `thr_texcorr_col2() = 9500`
- **Fires:** if `drift > 30 AND var < 400 AND corr > 9500`
- **NOISE:** 0/60 fire
- **Status:** ACTIVE

### D5: CCN-2-MIXED (bit 5)
- **Measure:** warmth difference: w1 = mean(r-b) over q1=[0,32), w2 = mean(r-b) over q2=[32,64)
- **Threshold:** `thr_ccn2() = 15` (raw warmth units)
- **Fires:** if `(w1 > 15 AND w2 < -15) OR (w2 > 15 AND w1 < -15)` (opposite signs, both significant)
- **NOISE:** 0/40 fire
- **Status:** ACTIVE (refined from L1-asymmetry; warm/cool direction is the structural signature)

### D6: MOT-2-FLICK (bit 6)
- **Status:** DISABLED (thresholds set to 1,000,000, impossible)
- **Reason:** Pixel-level second-difference (flick) fired on 40/60 NOISE; first-difference fired on 16/60. The MOT-2 trap is "two-motion" (dominant + 30% opposite on even frames), which requires motion-field analysis, not pixel energies. Baseline wrong-HC for MOT-2 is 0, so no KD-1 impact.

### D7: MOT-3-CAMO (bit 7)
- **Status:** DISABLED (thresholds set to 1,000,000, impossible)
- **Reason:** Frame-difference band (4–90) overlapped heavily with clean motion (55–415). The MOT-3 "camouflaged" signature (low contrast + 1px/frame) cannot be distinguished from normal motion by frame energy alone. Baseline wrong-HC for MOT-3 is 0.

### D8: SHP-1-OCCLUDE (bit 8)
- **Status:** DISABLED (threshold set to 1,000,000, impossible)
- **Reason:** Both "longest dark run" (fired 17/90 NOISE) and "consecutive uniform-dark rows" (fired 17/90) false-alarm on photo backgrounds. The occlusion bar (17 rows of (20,20,20)) is not distinguishable from dark photo regions by these measures. Baseline wrong-HC for SHP-1 is 0.

### D9: TMB-1-BOUNDARY (bit 9)
- **Status:** DISABLED (threshold set to 0, impossible since distance >= 0)
- **Reason:** Fired on 45/60 NOISE. Clean timbres routinely fall within 12% of class boundaries (d9_bnd: 6–21 on NOISE). Boundary proximity alone is not specific to the TMB-1 "boundary-straddling" trap. Baseline wrong-HC for TMB-1 is 6 (small).

### D10: SHP-3-SKEW (bit 10)
- **Measure:** `m10_contrast` — Weber contrast ((max-min)/min × 100)
- **Threshold:** `thr_shp3_con() = 30`
- **Fires:** if `contrast < 30`
- **NOISE:** 0/90 fire (all 153–243, well above 30)
- **Status:** ACTIVE (conservative; threshold far from NOISE distribution)

### D11: TMB-2-RESCUE (bit 11)
- **Measure:** `m11_boost` — 100×(E_high/E_low) energy ratio
- **Threshold:** `thr_tmb2_pct() = 150`
- **Fires:** if `boost > 150`
- **NOISE:** 0/60 fire (all 0–49, well below 150)
- **Status:** ACTIVE (conservative; threshold far from NOISE distribution)

## Confidence Cap

When any ACTIVE detector fires, `confidence` is capped at 650 (min(conf, 650)).

Disabled detectors (D3b, D6, D7, D8, D9) have impossible thresholds and never fire.

## Mask Semantics

- `dmask=4095` (default): all 12 bits; runs active detectors D1, D2, D3, D4, D5, D10, D11.
- `dmask=0`: no detectors; `approach=R2-4`; output byte-identical to R2-4.
- Per-bit: `dmask=(1<<k)` runs only detector Dk.

## Verification

- 370/370 NOISE fixtures: 0 fires with `dmask=4095`.
- `dmask=0` byte-identical to R2-4 on 6-fixture smoke (1 per task).
- Full-battery `dmask=0` vs R2-4 equality: PENDING (to be run after R2A complete).

## Addendum (2026-09-23, post-freeze bugfix)

During red-team validation (before R2A evaluation), two implementation bugs were found and fixed:

1. **D4 `m4_drift`**: The original implementation compared panel1 vs panel2 means (correct for COL-2's warm-vs-cool illuminant difference), but the `vknow_texcorr` conjunction was invalid — COL-2 panel1 is uniform (zero variance), so Pearson correlation is undefined (returns -20000). The correlation requirement was removed.

2. **D4 threshold**: Further analysis showed the drift measure (|warmth1-warmth2|) cannot achieve 0 FA on NOISE — the warm/cool illuminant difference is not consistently opposite-signed, and the magnitude overlaps with clean DIFFERENT trials. **D4 is DISABLED** (threshold set to 1,000,000).

**Impact on KD-1**: With D4 disabled, the KD-1 drivers are D1 (PTC-2, 400 baseline) and D3 (CCN-1, 335 baseline). Combined: 735. Baseline 1,075 - 735 = 340 ≤ 537. KD-1 can still pass.

**KD-2**: Will report 0% reduction for COL-2 (313 baseline) — a documented unteachable family with the current detector forms.

These fixes were made BEFORE any R2A evaluation, using only NOISE fixtures and red-team evasions (not R2A). The 0-FA calibration principle is preserved.
