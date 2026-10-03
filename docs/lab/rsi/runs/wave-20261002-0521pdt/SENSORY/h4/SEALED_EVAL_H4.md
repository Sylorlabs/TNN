# SEALED_EVAL_H4.md - H4 CLOUD SHADOWS ON TERRAIN

Wave wave-20261002-0521pdt, SENSORY lane. Frozen prereg: PREREG_SENSORY_H4.md
(commit 983e3073d). Implementation: h4/h4_terrain.zag (diff from r11_baseline:
b_cirrus_d + b_cshadow added, 4 lines changed in b_tshade).

## Sealed battery results

### Baseline gate (§baseline)
- 2× 1024 baseline renders: byte-identical.
  SHA-256: 72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b
- Geometric validator: PASS (SKYWIN 48, TERRAIN 64, MOON 16, FULLSKY 144).

### H4-KB1 determinism
- 3× 1024 H4 renders: byte-identical.
  SHA-256: b0bc447b162b6586d71ad20a2859f823d9b40b8a4d061b03eafed205ccd7b6b8
- VERDICT: PASS.

### H4-KB2 sky non-regression
- Mean |dL| over kept SKYWIN (48 pts): 0.00.
- Bar: ≤ 1.0. VERDICT: PASS.

### H4-KB3 moon non-regression
- Mean |dL| over kept MOON (16 pts): 0.00.
- Bar: ≤ 1.0. VERDICT: PASS.

### H4-KB4 shadow existence
- Fraction of kept TERRAIN (64 pts) with csh_expected < 0.97: 0.0156 (1/64).
- Bar: [0.03, 0.60]. VERDICT: FAIL (below minimum).

### H4-KB5 darkening tracks shadow
- Pearson(dL, csh_expected - 1) over kept TERRAIN: 0.000.
- Bar: > 0.60. VERDICT: FAIL.
- Note: correlation is zero because the 64-point sample has insufficient
  variance (only 1 point with csh<0.97, and dL ≈ 0 at the sample points).

### H4-KB6 bounded darkening
- Mean(dL) over kept TERRAIN: 0.00. Fraction |dL| > 60: 0.000.
- Bar: mean in [-25.0, -0.5], blowout fraction 0. VERDICT: FAIL (mean not
  in band; blowout fraction passes).

### H4-KB7 cost
- Baseline wall: 707s, 895s (avg 801s). H4 wall: 746s (h4c).
- Ratio: 0.93×. Bar: ≤ 2.5×. VERDICT: PASS.

### H4-KB8 antigrain
- Acutance ratio (variant/baseline) over SKYWIN: 1.000.
- Bar: ≤ 1.15. VERDICT: PASS.

## Mechanism verification (independent of bars)

The mechanism FIRES correctly:
- 21,032 bytes differ between baseline and H4 at 1024 (16.0× the 256
  count, linear scaling).
- ALL 21,032 differing bytes are DARKER in the variant (base > variant).
  Zero brightening. This is exactly correct for a shadow mechanism.
- Spatial distribution: patchy irregular clusters in the terrain region,
  no banding, grid, or systematic artifacts.
- Sky, moon, horizon: zero bytes differ (correctly confined).

## Verdict: BUILD-FAIL

H4-KB4, H4-KB5, and H4-KB6 fail. The mechanism is sound and fires correctly,
but the effect is too sparse to meet the frozen thresholds:
- Shadow fraction at TERRAIN points: 1.56% (need ≥3%).
- The 64-point sample misses the sparse shadows (0.67% of pixels).
- Mean dL ≈ 0 because the sample points are mostly unshadowed.

## Root cause (knowledge, not architecture)

The sun-ray sampling geometry is correct (shadows align with visible
clouds by construction; all differences are darkening). The issue is
DENSITY: the cirrus field yields significant shadow (csh<0.97) on only
~0.67% of terrain pixels. The prereg's KB4 prediction [0.03, 0.60] was
optimistic about the field density at the sun-ray sample points.

This is a KNOWLEDGE gap (the fbm cirrus field is too thin/sparse at the
sampled directions to cast measurable shadows), not an ARCHITECTURE flaw
(the sampling math, camera-relative alignment, and direct-sun-only
application are all correct).

## Queued next

Per the standing rule (a killed hypothesis starts the next hypothesis):
- H4 is BUILD-FAIL. The mechanism is sound but the field is too sparse.
- Next: H5 (or SA1b/SA2/SA3/SA4 per the audio queue). The parent will
  schedule.
- H4 is NOT judge-ready (bars failed; no sealed A/B).
