# Judge2 Protocol Amendments

Amendments to the frozen `JUDGMENT_PROTOCOL.md` for the repaired judge (`judge2.zag`).
The frozen protocol's mechanism (reference-envelope deviations, defect list, verdict
threshold) is preserved; the amendments below repair the four disclosed failure
classes. Nothing here changes the 8 valid reason names or the GOOD≥600 verdict bar.

## 1. Contrast: absolute body-text readability bar (fixes CONTRAST_POOR misses)

**Problem.** The frozen contrast metric averaged only "solid ink" pixels
(`|ΔL|>48` from the page background). Near-invisible body text (`|ΔL|≤48`)
was excluded entirely, so a page with unreadable body copy but dark headings
scored normally and fired zero defects.

**Fix.** A new metric `m_body_contrast` measures the DOMINANT body-text band
against its own local backdrop:
- Bands are detected at a low threshold (`|ΔL|>12`) so faint text forms bands.
- The band backdrop is the band-row luminance MODE (first principles: text is
  judged against its local backdrop, not the page-global background).
- Only bands on the page background are judged (backdrop within 24 of global
  bg); text-on-photo bands are skipped rather than misjudged.
- Only bands in the middle 70% of the page (not header/footer chrome).
- The ink representative is the 25th percentile from the text end (robust to
  anti-aliasing fringes that pull the mean toward the background).
- Contrast is WCAG 2.x relative luminance via an sRGB linearization table
  (256-entry, exact to table precision), reported ×1000.
- Absolute bar: `CONTRAST_POOR` fires when the dominant body band is below
  3.0:1 (dev scales to severe below ~1.8:1).

The legacy solid-ink `m_contrast` is retained as an envelope metric for context.

## 2. Score decompression (fixes 830 ties)

**Problem.** Many pages tied at exactly 830 because the weighted mean deviation
saturated and a single mild defect (-80) produced identical scores.

**Fix.**
- The worst weighted metric counts double in the mean.
- A quadratic term (`mean²/2500`) spreads the multi-defect tail.
- Defect penalties are tiered: mild -100, severe -250 (was flat -80).
- Result: calibration scores span 0–1000 with no ties.

## 3. False-positive reduction (fixes good pages losing)

**Problem.** Good pages received mild false-positive defects (e.g.,
`HIERARCHY_FLAT`, `ALIGNMENT_WEAK`) from photo-poisoned envelope metrics.

**Fix.**
- Defect fire threshold raised from 450 to 600 (severe at 800).
- Photo-poisoned metrics replaced with absolute/text-aware ones:
  - `m_bands`: absolute bar (>13 text bands = clutter), not envelope.
  - `m_hero_ratio`: absolute bar (<35% = flat), not envelope.
  - `m_align_k`: absolute bar (≥4 distinct edge positions in every axis),
    replacing the fragile `m_align_conc`/`m_guides` envelope metrics.
  - `m_margin_share`: absolute bar (>70% of content in outer rows).
  - `m_hues`: counts hues in small (text/chrome) bands only, excluding photo
    hues; absolute bar (≥4 distinct chrome hues) since all refs score 0.
- Result: all 4 good calibration fixtures score GOOD with zero defects.

## 4. Sense evidence (not load-bearing)

**Finding.** The frozen sense tasks (`colordisc`, `shapetrans`) were tested
across 14 fixtures × 2 representations. Outputs are coarse and
non-discriminative for UI quality:
- `shapetrans`: always TRIANGLE (rep A) or CIRCLE (rep B) — identifies the
  representation, not the page quality.
- `colordisc`: typically 1–2 SAME out of 5; the ≥3 majority bonus never fires.
- Good and bad fixtures produce identical sense patterns.

**Decision.** Sense evidence is parsed and traced (protocol compliance), but
assigned zero scoring weight. Inventing a representation-dependent aesthetic
mapping would be unsupported. Documented as a limitation, not a repair.

## Metric inventory (17)

Envelope-scored: `m_bg_lum`, `m_ink_lum`, `m_contrast`, `m_ink_total`,
`m_gap_cv`, `m_margin_ink`, `m_guides`, `m_align_conc`, `m_type_modes`,
`m_rows`, `m_satcov`.

Absolute-bar: `m_bands` (density), `m_hues` (color), `m_hero_ratio`
(hierarchy), `m_body_contrast` (readability), `m_align_k` (alignment),
`m_margin_share` (margins).

## Defect mapping

- `TYPOGRAPHY_INCONSISTENT` ← `m_type_modes` (envelope, high)
- `CONTRAST_POOR` ← max(`m_contrast` envelope low, `m_body_contrast` abs low)
- `SPACING_IRREGULAR` ← `m_gap_cv` (envelope, high)
- `MARGIN_CROWDED` ← `m_margin_share` (absolute, high)
- `DENSITY_CLUTTER` ← `m_bands` (absolute, high)
- `HIERARCHY_FLAT` ← `m_hero_ratio` (absolute, low)
- `COLOR_UNRESTRAINED` ← max(`m_hues` abs high, `m_satcov` envelope high)
- `ALIGNMENT_WEAK` ← `m_align_k` (absolute, high)

## Blindness declaration

Tuned only against the four disclosed failure classes and self-created
fixtures. Never opened `b2-bads/`, `OFFICIAL_RESULTS.txt`, or
`traces/b2_official/`. The official 10/14 result was disclosed only as a
score, not as per-fixture data.
