# V1 vs V2 difference map

V1 = winner of TNN's own aesthetic scorer (candidate 14 of 224, score 314).
V2 = human-taste theme from Sol's recommendations (frozen prereg values).

| dimension | V1 (machine taste) | V2 (predicted human taste) |
|-----------|--------------------|-----------------------------|
| background | (10,10,12) near-black | (15,16,18) near-black |
| surface | (26,26,30) | (30,31,35) |
| accent | (245,245,247) white | (255,82,112) coral |
| text | (245,245,247) white | (247,247,245) warm white |
| muted | (150,152,160) | (157,160,168) |
| corner radius | 0 px (sharp) | 16 px |
| spacing unit | 4 px | 4 px |
| shadow | off | on (soft, 8px feel) |
| border | off | off |
| search field | sharp black inset | rounded, shadowed |
| cards | flat, sharp | rounded, shadowed |
| play button | white disc | coral disc |
| playing row | white title + white EQ | coral title + coral EQ |
| active tab | white dot | coral dot |
| toggles on | white | coral |
| sliders | white fill | coral fill |
| album art rings | white/gray | coral/pink |

Structural layout (positions, spacing rhythm, component inventory) is
IDENTICAL between V1 and V2 — only theme words differ. The scorer's winning
set was {spacing 4, palette dark-mono or dark-blue, no shadow, no border,
any radius}; tie-break (first max) selected dark mono, radius 0.

## What the difference reveals

The machine scorer rewards: maximum contrast (capped), fewest colors,
grid-exact geometry, shared x-alignment, left/right area symmetry —
and penalizes shadow (directional asymmetry) and borders (color complexity).
It is indifferent to corner radius (no scoring term touches it).

Sol's predicted machine-vs-human gaps, confirmed in the renders:
- machine: rigid symmetry, fewer colors, flatter affect, utilitarian type
- human-taste: tonal variation (coral on near-black), atmospheric depth
  (shadows), softer geometry (16px radius)

## Honest note on the scorer

Contrast is capped at 400:1-equivalent before normalization, so dark-mono
and dark-blue palettes tie; radius has no term at all. The "opinion" is
coarse — it selects a family (flat dark minimal), not a point. The tie-break
(first maximum wins) is deterministic and documented, not principled.
This is a limitation of the mechanism, reported as-is.
