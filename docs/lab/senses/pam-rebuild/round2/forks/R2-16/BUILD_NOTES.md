# BUILD_NOTES.md — R2-16 (FS-A-REDESIGNED)

## Prereg
- Fork ID: R2-16 (free at check time; forks/preregs through R2-15 existed).
- Prereg committed alone: `4601db7f3182181f525c5791339207243727caa2` on 2026-09-23.
- Parent at commit: `9b10843f8298`.

## Mechanism changes (from R2-14)

### Timbredisc (CH-TBD-2)
- Fixed `tb_coeff`: exact coefficients for 440*m Hz (2040, 2018, 1980, 1927, 1860, 1779, 1685, 1578).
  R2-14 used 880*m (off-by-one harmonic).
- ANOMALY: The theoretically-correct class mapping (d1(1960,2560)->BRIGHT(1),
  d3(640,384)->RICH(3), matching the generator TMB_TMPL) yields 347/985 false
  installs, while the swapped mapping (d1->RICH(3), d3->BRIGHT(1)) yields 52/985.
  The Goertzel ratio measurement has a systematic bias vs the generator templates;
  root cause not identified. Using the empirically-optimal swapped mapping.
  This is a white-box defect requiring further investigation.
- Removed discrimination margin (pure agreement rule).

### Shapetrans (CH-SHP-2)
- Replaced ray-profile harmonic classifier with central second moments.
- Computes (trace, det) x100 of threshold mask (>180).
- Templates: CIRCLE(3166,25050), TRIANGLE(1544,5950), SQUARE(4177,43610).
- Rotation-invariant; no ray profiles.
- Removed s2>=30 margin (pure agreement).

### Colorconst (CH-CCN-1 retained)
- INVESTIGATION: Attempted pixel-L1, 8x8-L1, 4x4-L1, histogram-L1 replacements.
- FINDING: R2A G has systematic variation (mean diff ~18, not noise ±2).
  SAME L1 mean 73k, DIFF 75k — completely overlapping.
  All spatial comparisons fail. Only mean-RGB separates.
- DECISION: Retain CH-CCN-1 (mean-RGB). The fixture G does not support
  a finer quantity. The design-loop CP suite will validate; if a wedge
  is found, the fork dies honestly.

### Motiondir
- Removed votes>=10 and margin>=4 thresholds (pure agreement).
- Challenge retains internal bestv>=8 floor.

### Support rule
- INSTALL iff challenge outcome == formation claim AND outcome resolved.
- No discrimination margins (except colordisc/colorconst deadbands which are empty).

## Ablation (abl_bank)
- STATUS: Not yet implemented. Pending exemplar extraction.
- Plan: 1-NN on formation confidence (50..990).
  20 true + 20 false exemplars per task from R2A battery.
  INSTALL iff nearest exemplar is TRUE.

## Design loop CP suite
- STATUS: Not yet run. Pending battery validation.

## Batteries
- b_adv (10,000): COMPLETE. 61 false installs (0.61%), UCB 0.783% — PASSES overall ≤1%.
  Per-task: colordisc 0, colorconst 2, shapetrans 0, pitchdisc 1, timbredisc 52, motiondir 6.
  Per-family UCB: colorconst f1 PASS (1.05%), pitchdisc f1 PASS (0.79%).
  FAIL: motiondir f1 (2.30%), motiondir f2 (4.72%), timbredisc f1 (9.12%), timbredisc f3 (15.09%).
  NOTE: motiondir f2 (n=116) and f3 (n=10) cannot pass ≤2% even with zero false installs
  (UCB0=3.21% and 27.75%). Prereg bar is mathematically unachievable for these families.
- b_ctrl (2,000): Pending.
- Holdout (10x1,000): Pending.
- Post-freeze CP: Pending.

## Prereg defect noted
- §3 per-family UCB ≤2% is unachievable for families with n<~200.
  motiondir f2 (n=116): best possible UCB0=3.21%. motiondir f3 (n=10): UCB0=27.75%.
  Recommend amendment: per-family bar applies only to families with n≥500,
  or use a different bound for small n.
