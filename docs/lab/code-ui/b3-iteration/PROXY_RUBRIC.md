# B3 BLIND HUMAN-PROXY RUBRIC — preregistered BEFORE any judging

**Frozen:** 2026-09-24 ~13:20 PDT (before v1 rendering/judging of the B3 iteration crew).
**Role:** prereg B3(b) evidence — a pixel-measurable, human-readable proxy for the
human comparison the protocol defers to Micah's eyes. Implements frozen
JUDGMENT_PROTOCOL.md §5 step 6: "the blind human-proxy rubric
(spacing/typography/alignment sub-scores recomputed from v2's pixels) improves
on a majority of the named defects."

**Independence:** implemented in `proxy_rubric.py` (plain deterministic Python,
PIL only) with *different* thresholds and algorithms than the frozen judge, so
it is not the judge re-running itself. It measures the same four human-visible
dimensions a person would see: spacing regularity, typography consistency,
alignment, hierarchy (+ color restraint as context).

**Blind procedure:** v1 and v2 images are copied to unlabeled filenames
`BLIND_A.img` / `BLIND_B.img` via a deterministic mapping recorded separately
in `blinding.txt` (SHA-256 of site name → A/B). Scoring runs on the blind
files; the mapping is unsealed only after measurements are recorded.

## Measurements (all deterministic, from RGB24 pixels)

Ink detection: pixel luminance L = 0.299R+0.587G+0.114B; bg estimate = median
of all L. Ink pixels: L < bg − 60.

1. **Spacing regularity** — rows with ink-count > 2% of width are "active";
   contiguous active runs (merged across gaps ≤ 8px) are bands. Inter-band
   gaps in px → `gap_cv` = stdev/mean (0 if <2 gaps). `margin_ink` = share of
   ink pixels in the top or bottom 10% of rows. `ink_total` = share of all
   pixels that are ink. GOOD direction: lower gap_cv, lower margin_ink,
   ink_total inside a sane range (0.5%..15% → deviation penalized both ways).
2. **Typography consistency** — `type_modes` = distinct band-height classes
   (heights clustered within 3px). `contrast` = (bg_lum+10)/(mean_ink_lum+10).
   GOOD: fewer type_modes (≥3 sizes for a real page is fine; penalty above 6),
   higher contrast.
3. **Alignment** — per band, left ink edge = first column where ≥10% of the
   band's rows have ink. `align_modes` = distinct left-edge x positions
   (clustered within 4px). GOOD: fewer align_modes.
4. **Hierarchy** — `hero_ratio` = max band ink-mass / total ink mass;
   `size_ratio` = max band height / median band height. GOOD: higher
   hero_ratio, higher size_ratio (a hero dominates).
5. **Color restraint (context)** — `satcov` = share of pixels with
   HSV saturation > 48; `hues` = distinct hue bins among saturated pixels.
   GOOD: lower satcov, fewer hues.

## Per-defect improvement rule

For each named defect in the site's JUDGMENT.md (from the 8 rubric-valid
names), the defect maps to a dimension above:

- SPACING_IRREGULAR → gap_cv strictly lower (ties = no improvement)
- MARGIN_CROWDED → margin_ink strictly lower
- DENSITY_CLUTTER → ink_total deviation from [0.005, 0.15] strictly lower
- TYPOGRAPHY_INCONSISTENT → type_modes strictly lower
- CONTRAST_POOR → contrast strictly higher
- ALIGNMENT_WEAK → align_modes strictly lower
- HIERARCHY_FLAT → hero_ratio strictly higher OR size_ratio strictly higher
- COLOR_UNRESTRAINED → satcov strictly lower OR hues strictly lower

**Pass criterion:** a strict majority of the named defects improve v1 → v2.
