# JUDGMENT — selene v1 (B3 step 3)

**Judge:** frozen `judge` v1, protocol `JUDGMENT_PROTOCOL.md`.
**Rendered:** headless WeasyPrint, 1280×800, local files only (initial state).
**Trace:** `ui-judgment/traces/b3iter/selene_v1_a.txt` (rep a primary), `_b.txt` (rep b).

## Frozen mechanism verdict (verbatim)

- judgment=GOOD, score=704, confidence=260, best_ref=apple2
- defects (mechanism-named): **TYPOGRAPHY_INCONSISTENT**, **HIERARCHY_FLAT**
- Key metrics: m_type_modes=5 (envelope hi=4), m_hero_ratio=575 (envelope
  lo=952), m_contrast=5617, m_gap_cv=1048, m_margin_ink=0
- Rep b: identical (score=704, both defects)

## Named defects vs the T3 examples (≥3, rubric-valid)

1. **TYPOGRAPHY_INCONSISTENT** (mechanism-named). Five band-height classes
   vs the reference envelope max of 4 (vercel1=4). Concretely: 52px hero h1,
   26px section heads, 18px card titles, 18px moon text, 14px filter buttons,
   12px kicker — the 18px card titles and 18px moon paragraph are the same
   size doing different jobs, and 26/18/14 crowd the mid-range the way no
   reference does.
2. **HIERARCHY_FLAT** (mechanism-named). Hero share 575‰ vs envelope floor
   952‰. The 52px "Know the sky above you." sits in a 100/70 padded hero
   while the constellation section (26px head + filter pills + 4 cards)
   carries more visual mass — the page's weight is in section two, not the
   hero. apple2's hero is unambiguously the heaviest element.
3. **SPACING_IRREGULAR** (crew-observed vs linear1). Section rhythm: hero
   100/70, comp sections 48/48, footer 28+40 margin — the hero's asymmetric
   100/70 vs the uniform 48s vs the footer's 28+40 reads as three different
   spacing authors. Within the constellation section: h2→muted 8px,
   muted→fbtns 20px, fbtns→cgrid 24px, card gap 20px — four spacings where
   linear1 would use two.

## Iteration request for v2

- Enlarge the hero (h1 52→68px, padding 120/90) so it owns the page.
- Collapse type modes: card titles 18→20px semibold (distinct from 18px body
  copy → move card copy to 15px), moon paragraph 18→16px, section heads
  26→28px. Target ≤4 modes.
- Regularize section rhythm: all comp sections 64px, internal gaps from a
  2-step scale (16/32).
