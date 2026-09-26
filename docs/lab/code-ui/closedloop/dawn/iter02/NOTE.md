# iter02 NOTE

## (a) What my eyes saw (view.png)
- Nav fixed: "Features", "How it works", "Start focusing" all single-line; the pill is now a proper pill. Genuinely looks clean.
- Hero unchanged otherwise and still looks good: eyebrow, serif H1, lede, actions, timer card all read well. The "See how it works" link without underline + wider gap looks calmer.
- Remaining nit I see: vertical rhythm feels slightly uneven (hero bottom padding vs. top), nothing structural.

## (b) Judge
judge2, reps a/b agree: BAD, score 55 (unchanged), same defects TYPOGRAPHY_INCONSISTENT, SPACING_IRREGULAR, ALIGNMENT_WEAK. My nav fix moved margin_ink 0.1912→0.209 but not the score.

## (c) Proxy
A(iter02): bands=10, gap_cv=1.039, margin_ink=0.209, ink_total=0.0314, type_modes=7, contrast=1.917, align_modes=2, hero_ratio=0.3091, size_ratio=2.519, satcov=0.0183, hues=3.
B(iter01): identical except margin_ink=0.1912, type_modes=6, hero_ratio=0.3159.

## (d) Defects I name myself
1. Key discovery: the frozen pipeline renders at exactly 1280×800 (pdftoppm -W 1280 -H 800, first page only) and png_to_img resizes to 1280×800 — so the judge and proxy see ONLY the nav+hero viewport. Below-fold sections are invisible to the score. (Full page still kept coherent for the actual deliverable.)
2. The judge's three defect codes therefore all describe the hero. My leading hypothesis: the Georgia-serif-body + Arial-sans-labels mix reads as typographic inconsistency; paddings/gaps are not on a common rhythm (spacing); left-edge/band rhythm is loose (alignment).

## (e) Changes for iter03 (aimed at the defect codes, keeping the dawn design)
- Typography: body and all UI text move to the system sans stack; serif kept ONLY for the H1 display line (clear display-vs-UI role split). Collapse sizes to ~5 modes: 12 / 52 / 18 / 15 / 13.
- Spacing: hero padding 96/96 symmetric; lede margin 32; actions margin-bottom 24; eyebrow margin-bottom 24 — all on an 8px rhythm.
- No content changes.

## Decision
CONTINUE to iter03. DONE criteria unchanged (stated in iter01): judge GOOD + zero defects both reps AND my eyes find nothing left.
