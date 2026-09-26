# Round 11 — hemisphere sky ambient (FINAL)

Date: 2026-09-26. Branch: `tnn-native-lab`. Pure Zag, zero RNG.

## Lineage

r4 (standing champion, bright day scene) → r5/r6/r7 → r8a (one-sun repair)
→ r8b Fork B (unified trace, T1..T12) → T13/T13b (Micah's moon + edge oracle
fixes) → **r11** (this round).

r11 builds on r8b+T13/T13b and is tested head-to-head against the r4
champion base, as ordered.

## The defect (seen with eyes, not metrics)

The r8b dusk scene's shadowed foreground — the bottom ~35% of the frame —
read as void. Rock-cause: in `b_tshade`, the dusk fill sampled the sky
along the surface normal. For flat ground the normal points at the
zenith — the darkest part of the deliberated sky. A real surface sees
the whole sky dome, and this world's deliberated dust glow lives at the
horizon ring (T2), not the zenith.

## The change (T14, one mechanism)

`imagination_discovery/img/r11_alien.zag`: the dusk fill now samples a
hemisphere ambient — 0.65 × the horizon-ring sky at the sun-ward azimuth
+ 0.35 × the normal-direction sky. No sun moved, no shadow re-derived,
the sunlit look untouched, the moon and sky untouched. Documented in the
trace as T14 feedback: depiction judged deliberation, deliberation
answered within the world model.

## Rejected fork (recorded so it is not retried)

A gamma-2.0 display encode (`byte = sqrt(linear)`) was trialed first on
the theory that linear framebuffer values were never display-encoded.
The eye rejected it: the trace's palette had already been deliberated
against unencoded output, so the encode was a re-grade, not a repair —
the dusk mood washed flat and pastel, and the deliberated 19%-lit
crescent collapsed against the planetshine side and read as a full grey
ball (a direct contradiction of the T13 deliberation). Rejected by eyes,
not metrics.

## Evidence (completed 2026-09-26)

- [x] 1024² render + byte-identical rerun (SHA-256
  `72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b`,
  both runs)
- [x] Full-eyes judging, r4 vs r11, normal vision — VERDICT.md (R11 takes
  championship); r8b same-scene before/after confirms T14 confined to the
  dusk fill
- [x] Display-size (256) acceptance pair (r11_256_preview.png,
  r11_compare_256.png, r11_compare2_256.png)
- [x] Commit to tnn-native-lab (never main)
