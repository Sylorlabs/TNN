# REDTEAM_ARTIFACTS_H4.md - H4 CLOUD SHADOWS ON TERRAIN

Wave wave-20261002-0521pdt, SENSORY lane. Updated with 1024 sealed results.

## Method

Compared baseline vs H4 at 256 (smoke) and 1024 (sealed). Analyzed:
byte-level diff locations, magnitudes, direction (darker/lighter),
spatial distribution; checked for banding, grid, flicker, or artifacts.

## Findings

### F1: Mechanism fires correctly, but sparse

- 1024: 21,032 bytes differ (0.67% of pixels). 256: 1,316 bytes (0.67%).
  Linear scaling (16.0×), consistent.
- ALL differing bytes are DARKER in the variant. Zero brightening.
  This is exactly correct for a shadow mechanism.
- Max per-channel difference: 34 levels (1024). Mean abs diff: 2.56.
- Spatial: patchy irregular clusters in terrain region. No banding,
  grid, scanlines, or block artifacts.

### F2: No dropout, flicker, or weirdness

- Difference map consistent with irregular cloud shadows: soft-edged
  patches, varying density, no hard edges.
- No blowout (max 34 < 60). No color shifts beyond expected darkening.
- Sky (48 pts), moon (16 pts): zero difference. Correctly confined
  to terrain direct-sun term.

### F3: Sparsity kills the bars (not a bug)

- The 64-point TERRAIN sample hits only 1 shadowed point (1.56%).
- The shadows exist (21k bytes), but cover 0.67% of pixels.
- The prereg's KB4 [0.03, 0.60] assumed 3%+ shadow fraction; actual
  is 1.56% at sample points, 0.67% overall.
- KB5 correlation is zero because the sample lacks variance, not
  because the mechanism is wrong (the 21k shadowed bytes ARE darker).

## Knowledge vs architecture

- **Architecture (SOUND):** Sun-ray sampling, camera-relative alignment,
  direct-sun-only multiplication are all correct. Shadows are darkening-
  only, patchy, terrain-confined. No geometry bug.
- **Knowledge (GAP):** The fbm cirrus field is too sparse/thin at the
  sun-ray sample directions to produce a measurable effect. Only 0.67%
  of terrain pixels get significant shadow. The field density (or the
  0.45 attenuation) is insufficient for the frozen thresholds.
- **Prereg (OPTIMISTIC):** KB4/KB5/KB6 predictions assumed a denser
  shadow field. The mechanism works; the effect size was overestimated.

## Verdict

No artifacts. Mechanism correct. BUILD-FAIL on effect size (KB4/KB5/KB6).
The honest conclusion: cloud shadows are real but too subtle/sparse in
this implementation to clear the frozen bars. A denser field or stronger
attenuation might work, but that would be a NEW prereg (H5), not a patch.
