# JUDGMENT — gadget v1 (B3 step 3)

**Judge:** frozen `judge` v1, protocol `JUDGMENT_PROTOCOL.md`.
**Rendered:** headless WeasyPrint, 1280×800, local files only (initial state;
aesthetic judgment is about static visuals).
**Trace:** `ui-judgment/traces/b3iter/gadget_v1_a.txt` (rep a primary), `_b.txt` (rep b).

## Frozen mechanism verdict (verbatim)

- judgment=GOOD, score=830, confidence=575, best_ref=apple2
- defects (mechanism-named): **HIERARCHY_FLAT**
- Key metrics: m_hero_ratio=659 (ref envelope lo=952), m_gap_cv=1102,
  m_type_modes=3, m_contrast=2866, m_margin_ink=1
- Rep b: identical (score=830, HIERARCHY_FLAT)

## Named defects vs the T3 examples (≥3, rubric-valid)

1. **HIERARCHY_FLAT** (mechanism-named). Hero share 659‰ vs envelope floor
   952‰. The 40px h1 vs 24px component titles is a flat 1.67:1; nothing on
   the page claims the viewport the way apple2's hero does.
2. **SPACING_IRREGULAR** (crew-observed vs stripe1). Three components, three
   interior paddings for the same "component body" role: accordion answers
   18px bottom, tab panes 24px all-round, todo items 12px/16px. Control-row
   gaps differ too (counter 20px, todo 12px). stripe1 repeats one component
   padding everywhere; gadget's reads as three separate authors.
3. **ALIGNMENT_WEAK** (crew-observed vs linear1). Three horizontal alignment
   strategies across four components: counter row is centered cluster, tab
   buttons are full-width thirds, accordion/todo are full-width left. The
   page's left text edge is the only consistent guide; linear1's components
   all obey one column discipline.

## Iteration request for v2

- Enlarge the hero (h1 40→56px) and give it breathing room so it dominates.
- Unify component body padding to 24px and control-row gaps to 16px.
- Align all components to the same wrap edge; keep the counter centered
  within its row (it is a centered instrument, not a text block).
