# R2-7 Frozen Challenge Registry

**Status: FROZEN 2026-09-23.** This registry is preregistered per PREREG_R2-7 §1.
No entry may be added, removed, or modified after results. Each entry names:
(a) the strongest plausible alternative, (b) the predicted outcome under the
claim, (c) the predicted DIFFERENT outcome under the alternative, (d) the
disjoint evidence path.

## CH-COL-1 (colordisc)

- **Alternative:** "different surface" (the two patches are different colors).
- **Under claim "SAME":** spectral L1 ≤ 8,000 (u16 reflectance units).
- **Under alternative:** spectral L1 ≥ 25,000.
- **Evidence:** G-span spectra (12×u16 per patch) captured under the neutral
  D65 re-render; disjoint bytes from the F-span RGB patches.
- **Method:** different measurement path (spectrometer vs RGB camera).
- **Support rule:** claim SAME requires L1 ≤ 8,000; claim DIFFERENT requires
  L1 ≥ 25,000. Otherwise WITHHOLD.

## CH-CCN-1 (colorconst)

- **Alternative:** "different surface" (illuminant fooled the formation).
- **Under claim "SAME_SURFACE":** mean-RGB Euclidean ≤ 12 on neutral-illuminant G.
- **Under alternative:** mean-RGB Euclidean ≥ 30.
- **Evidence:** G-span = both views re-rendered under D65 (controlled
  intervention: neutral illuminant); disjoint bytes from F.
- **Method:** controlled intervention (illuminant normalization).
- **Support rule:** claim SAME_SURFACE requires d ≤ 12; claim DIFFERENT
  requires d ≥ 30. Otherwise WITHHOLD.

## CH-SHP-1 (shapetrans)

- **Alternative:** "occluder/distractor is the object" (formation latched onto
  the wrong contour).
- **Under claim (e.g. CIRCLE):** ray-profile harmonic analysis on the clean
  G quadrant yields CIRCLE with margin ≥ 30.
- **Under alternative:** yields a DIFFERENT class (or low margin).
- **Evidence:** G-span = 48×48 clean re-render of the target class, centered;
  disjoint bytes from the F-span 96×96 occluded frame.
- **Method:** different measurement path (polar ray-profile + Fourier
  harmonics vs Cartesian image moments). Rotation-invariant.
- **Support rule:** challenge outcome == claim AND harmonic margin ≥ 30.
  Otherwise WITHHOLD.

## CH-PTC-1 (pitchdisc)

- **Alternative:** "pitch difference is below/above threshold"
  (formation's coarse count was fooled by glide or distractor).
- **Under claim "SAME":** interpolated frequency ratio |r| ≤ 35 (0.01%).
- **Under claim "HIGHER":** r ≥ 65. Under "LOWER": r ≤ -65.
- **Evidence:** G-span = clean re-render at true endpoint frequencies;
  disjoint bytes from F (seconds 0–2 vs the G token).
- **Method:** different measurement path (interpolated zero-crossing span
  vs raw crossing count) + controlled intervention (clean token).
- **Support rule:** as above. Otherwise WITHHOLD.

## CH-TMB-1 (timbredisc)

- **Alternative:** "different timbre class" (formation's coarse centroid bins
  were fooled by harmonic boost).
- **Under claim (e.g. RICH):** Goertzel power-ratio template match yields
  RICH with margin ≥ 20,000.
- **Under alternative:** yields a DIFFERENT class.
- **Evidence:** G-span = clean re-render of the true harmonic profile;
  disjoint bytes from F.
- **Method:** different measurement path (3-harmonic power-ratio template
  vs 8-harmonic spectral centroid). Controlled intervention (clean token).
- **Support rule:** outcome == claim AND template margin ≥ 20,000.
  Otherwise WITHHOLD.

## CH-MOT-1 (motiondir)

- **Alternative:** "reverse/opposite direction" (formation was fooled by
  reversal, flicker, or camouflage).
- **Under claim (e.g. N):** block-match votes on clean high-contrast G
  yield N with ≥10 votes and margin ≥4.
- **Under alternative:** yield a DIFFERENT direction.
- **Evidence:** G-span = frames 51–100, clean high-contrast re-render of the
  same motion; disjoint bytes from F (frames 1–50).
- **Method:** controlled intervention (high-contrast clean presentation).
  Same block-match algorithm but on disjoint evidence (the intervention is
  the clean re-render, not the algorithm).
- **Support rule:** outcome == claim AND votes ≥10 AND margin ≥4.
  Otherwise WITHHOLD.

## Discrimination audit

Each entry's (b) and (c) predict DIFFERENT outcomes. The runner
(`chal_supports` in r27.zag) mechanically rejects non-discriminating
challenges: if the challenge outcome does not match the claim's prediction
with the required margin, the result is WITHHOLD, never INSTALL. No registry
entry accepts "looks independent but doesn't discriminate."
