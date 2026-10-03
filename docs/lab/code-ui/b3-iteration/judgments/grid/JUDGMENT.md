# JUDGMENT — grid v1 (B3 step 3)

**Judge:** frozen `judge` v1, protocol `JUDGMENT_PROTOCOL.md`.
**Rendered:** headless WeasyPrint, 1280×800, local files only.
**Trace:** `ui-judgment/traces/b3iter/grid_v1_a.txt` (rep a primary), `_b.txt` (rep b).

## Frozen mechanism verdict (verbatim)

- judgment=GOOD, score=830, confidence=575, best_ref=apple2
- defects (mechanism-named): **HIERARCHY_FLAT**
- Key metrics: m_hero_ratio=335 (ref envelope lo=952; lowest of the four
  sites), m_gap_cv=848, m_type_modes=4, m_contrast=3146
- Rep b: identical (score=830, HIERARCHY_FLAT)

## Named defects vs the T3 examples (≥3, rubric-valid)

1. **HIERARCHY_FLAT** (mechanism-named). Hero share 335‰ vs envelope floor
   952‰ — the weakest of all four v1 sites. The 64px masthead, 40px lead
   headline, and 28px "More headlines" rule compete instead of staging:
   masthead → lead → cards reads as three separate front pages, where
   linear1 stages one clear entry point.
2. **SPACING_IRREGULAR** (crew-observed vs linear1). Vertical cadence has no
   repeated multiple: sections pad 48/48/40, internal gaps run 48 (featured
   grid) vs 32 (card grid), masthead 40/28. The sidebar (40px) sits
   off-rhythm from the 48px sections above it. linear1's sections share one
   spacing token; grid's were picked per-section.
3. **TYPOGRAPHY_INCONSISTENT** (crew-observed vs apple3). Nine distinct text
   sizes on one page (64/40/28/20/18/17/15/14/11): the 15px byline, 15px card
   descriptions, 15px sidebar items, and 14px footer collapse four different
   voices (byline, summary, list, fine print) into one size. apple3 holds
   two sizes for meta text; grid's blur together.

## Iteration request for v2

- Stage the hierarchy: masthead 64→72px, lead headline 40→44px, section
  heads 28→24px, card heads 20→18px — widen the gaps between levels.
- Regularize vertical rhythm: all sections 56px, internal gaps 32px.
- Split meta text into two voices: byline 15px stays, card descriptions and
  sidebar items 15→16px body-meta, footer fine print 13→12px.
