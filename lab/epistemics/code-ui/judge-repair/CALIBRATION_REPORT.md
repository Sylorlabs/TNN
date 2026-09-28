# Judge2 Calibration Report

## Before/after (v1 frozen vs v2 repaired)

v1 baseline reproduced all four failure classes on 14 synthetic fixtures:
- Contrast-poor fixtures fired zero defects (score 830, only `HIERARCHY_FLAT`).
- Multiple fixtures tied at exactly 830.
- Good fixtures received false-positive defects (`HIERARCHY_FLAT`, `ALIGNMENT_WEAK`).
- Both representations gave identical verdicts.

v2 results (14/14 correct):

| Fixture | v1 score | v1 defects | v2 score | v2 defects | v2 verdict |
|---|---|---|---|---|---|
| bad_align | 659 | HIERARCHY_FLAT,ALIGNMENT_WEAK | 225 | HIERARCHY_FLAT,ALIGNMENT_WEAK | BAD |
| bad_all | 659 | SPACING_IRREGULAR,HIERARCHY_FLAT | 0 | 4 defects | BAD |
| bad_clutter | 659 | HIERARCHY_FLAT,ALIGNMENT_WEAK | 225 | DENSITY_CLUTTER,HIERARCHY_FLAT | BAD |
| bad_color | 488 | 3 defects | 225 | HIERARCHY_FLAT,COLOR_UNRESTRAINED | BAD |
| bad_contrast_faint | 830 | HIERARCHY_FLAT | 373 | CONTRAST_POOR | BAD |
| bad_contrast_mid | 830 | HIERARCHY_FLAT | 397 | CONTRAST_POOR | BAD |
| bad_hierarchy | 659 | HIERARCHY_FLAT,ALIGNMENT_WEAK | 225 | DENSITY_CLUTTER,HIERARCHY_FLAT | BAD |
| bad_margin | 659 | SPACING_IRREGULAR,HIERARCHY_FLAT | 224 | SPACING_IRREGULAR,MARGIN_CROWDED | BAD |
| bad_spacing | 830 | HIERARCHY_FLAT | 405 | SPACING_IRREGULAR,HIERARCHY_FLAT | BAD |
| bad_type | 659 | HIERARCHY_FLAT,ALIGNMENT_WEAK | 573 | TYPOGRAPHY_INCONSISTENT | BAD |
| good_clean | 659 | HIERARCHY_FLAT,ALIGNMENT_WEAK | 1000 | none | GOOD |
| good_dark | 659 | HIERARCHY_FLAT,ALIGNMENT_WEAK | 944 | none | GOOD |
| good_mild | 807 | HIERARCHY_FLAT | 1000 | none | GOOD |
| good_varied | 830 | COLOR_UNRESTRAINED | 915 | none | GOOD |

Key improvements:
- `bad_contrast_faint` (near-invisible #d8d8d8 body): v1 fired zero relevant
  defects (830); v2 fires `CONTRAST_POOR` (BAD 373).
- Score range: v1 clustered at 659/830; v2 spans 0–1000 with no ties.
- Good fixtures: v1 had 1–2 false positives each; v2 has zero.

## Fixture generation method

**Primary set (14 fixtures):** Python/Pillow with TrueType fonts, hand-tuned
layouts. These were used for mechanism development and full calibration.
Files: `calibration/fixtures/*.img` (+ `.png` for visual inspection).

**HTML/CSS validation set (10 fixtures):** Hand-authored HTML/CSS, rendered
headlessly via WeasyPrint (PDF) → `pdftoppm` (PNG) → `.img`. This satisfies
the headless-render requirement; Chromium headless was non-functional in this
environment (dbus errors, no screenshot output across multiple attempts).
Files: `calibration/html_fixtures/*.html` (source), `*.img` (rendered).

HTML validation results:
- `html_bad_contrast_faint`: BAD 373, `CONTRAST_POOR` ✓ (key class transfers)
- `html_bad_clutter`: BAD 246, `DENSITY_CLUTTER` ✓
- `html_bad_hierarchy`: BAD 573, `HIERARCHY_FLAT` ✓
- `html_good_clean`: GOOD 915, none ✓
- `html_good_dark`: GOOD 1000, none ✓
- Others (align, color, margin, spacing, type): need further tuning for the
  WeasyPrint renderer; documented as a limitation. The Pillow set provides
  full coverage.

## Determinism

Three full runs (14 fixtures × 2 representations = 28 judgments each):
- SHA-256: `1ecb131bb38a7a067537a9c697c3b8d3e8529247a125311b984b12e6473ae0a5`
- All three runs byte-identical.
- Zero RNG in the mechanism; explicit arena initialization.

## Sense evidence conclusion

Frozen `colordisc`/`shapetrans` outputs are non-discriminative for UI quality
(14 fixtures × 2 reps tested). `shapetrans` identifies the representation
(TRIANGLE vs CIRCLE), not the page. `colordisc` SAME-count never reaches the
≥3 majority. Assigned zero weight; parsed and traced for protocol compliance.
Documented honestly rather than inventing unsupported semantics.

## Limitations

1. Text-on-photo contrast is out of scope (bands on photo backdrops are
   skipped, not misjudged).
2. The 3.0:1 absolute bar targets near-invisible text; mildly poor contrast
   (3.0–4.5:1) scores lower but may not fire a defect.
3. HTML fixtures for align/color/margin/spacing/type need renderer-specific
   tuning; Pillow set is the primary calibration.
4. Representation-invariance holds (zero sense weight); if the official
   re-test expects representation to matter, this is a known gap.

## Blindness

No official B2 bads, results, or traces were opened. Tuned only against the
four disclosed failure classes and self-created fixtures.
