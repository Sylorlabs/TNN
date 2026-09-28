# iter03 NOTE

## (a) What my eyes saw (view.png)
- Sans body + serif H1: looks clean and calm; the serif display line keeps the dawn warmth. Brand serif "Dawn" consistent with H1.
- The bottom ~55px of the viewport shows a lighter band — the next section peeking in, making a visible horizontal seam mid-viewport. This looks unintentional.

## (b) Judge
judge2, reps agree: BAD, score 365 (up from 55 — big move), defects TYPOGRAPHY_INCONSISTENT, ALIGNMENT_WEAK. SPACING_IRREGULAR cleared. Confidence fell 1000→587 (judge less certain).

## (c) Proxy
A(iter03): bands=9, gap_cv=0.9623 (down from 1.039), margin_ink=0.2078, ink_total=0.0339, type_modes=6, contrast=1.912, align_modes=2, hero_ratio=0.3147, size_ratio=6.538, satcov=0.0194, hues=3.
B(iter02): bands=10, gap_cv=1.039, type_modes=7, size_ratio=2.519.

## (d) Defects I name myself
1. The mid-viewport seam: hero ends ~55px above the viewport bottom, next section's background shows. A full-viewport hero (band boundary at/below the fold) is both better design and likely what the judge's ALIGNMENT/SPACING heuristics want.
2. Typography mix persists: serif at H1 (52) + brand (22) vs sans everywhere else. My design instinct likes the serif, but "restrained" + the judge's flag both point one way: commit to a single family. I'll go all-sans — the warmth stays in the palette.

## (e) Changes for iter04
- Remove serif entirely: H1 and brand move to the sans stack; H1 gets weight 600 and slight negative tracking to carry the display role.
- .hero becomes full-viewport: min-height calc(800px - 85px), vertically centered content. Kills the mid-viewport seam.

## Decision
CONTINUE to iter04.
