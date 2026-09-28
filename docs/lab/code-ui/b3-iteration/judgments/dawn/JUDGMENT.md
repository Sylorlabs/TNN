# JUDGMENT — dawn v1 (B3 step 3)

**Judge:** frozen `judge` v1, protocol `JUDGMENT_PROTOCOL.md`.
**Rendered:** headless WeasyPrint, 1280×800, local files only.
**Trace:** `ui-judgment/traces/b3iter/dawn_v1_a.txt` (rep a primary), `_b.txt` (rep b).

## Frozen mechanism verdict (verbatim)

- judgment=GOOD, score=830, confidence=575, best_ref=apple2
- defects (mechanism-named): **HIERARCHY_FLAT**
- Key metrics: m_hero_ratio=430 (ref envelope lo=952), m_gap_cv=865,
  m_type_modes=4 (envelope hi=4), m_contrast=3307, m_margin_ink=0
- Rep b: identical (score=830, HIERARCHY_FLAT)

## Named defects vs the T3 examples (≥3, rubric-valid)

1. **HIERARCHY_FLAT** (mechanism-named). Hero ink-mass share 430‰ vs the
   reference envelope floor of 952‰ (apple2=1000, linear1=1000). Visually:
   the 56px hero h1 against 32px section heads is only a 1.75:1 ratio, so the
   hero reads as just another band; in apple2 the hero owns the viewport.
2. **SPACING_IRREGULAR** (crew-observed vs linear1). Vertical rhythm has no
   consistent multiple: hero padding 120/100, sections 80/80, footer 28 —
   and within the hero, kicker→h1 20px, h1→sub 20px, sub→buttons 36px, button
   gap 12px: four different vertical spacings inside one hero. linear1 holds
   a strict cadence; dawn's reads as improvised.
3. **TYPOGRAPHY_INCONSISTENT** (crew-observed vs apple3). Four heading sizes
   (56/32/28/18) where the 28px quote and 32px section heads sit only 4px
   apart — two voices for one job — plus a 12px kicker and 15px nav links.
   apple3 runs the whole page on two heading sizes; dawn's near-duplicate
   28/32 pair blurs which text is a section voice.

## Iteration request for v2

- Enlarge the hero (h1 56→72px, hero padding up) so the hero dominates.
- Regularize section rhythm to one multiple (e.g. all sections 96px, hero
  internal gaps from a 2-step scale).
- Collapse the 28/32 pair: quote 28→24 italic pull-quote, section heads stay
  32. Kicker/nav sizes untouched.
