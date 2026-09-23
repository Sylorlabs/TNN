# TRACE INTEGRITY RESULT — Test 4 (PREREG_STALL_TESTS.md)

Date: 2026-09-22. Branch: `tnn-native-lab`. Pure Zag, zero RNG.
Canonical: `imagination_discovery/img/r8b_alien_1024.bmp`
(SHA-256 `3829e21610cd9f3d35defe77fad3fae8aaecdc132a42b8291a66550237ffaefc`).
Pre-T13: commit `222bb38e8` blob `55cc2205ffb775b0edc67d72ee7cfeb318cb92cf`.
Verifier: `~/workspace/stall_sweep/ti_final.py` (verification-only; generates no artifacts).

## Method

Every quantitative claim in `UNIFIED_TRACE.md` (T1–T13b) and
`MOONFIX_T13_REPORT.md` was recomputed against the actual pixels of the
canonical BMP (and the pre-T13 BMP for delta claims). "PASS" means the
claim holds within measurement tolerance; "FAIL" means the pixels
contradict it; "MIXED" means it holds in one reading and fails in
another — the distinction is stated, not smoothed over.

## Score table

| Claim | Pixel recomputation | Verdict |
|---|---|---|
| T1 sun vector (-0.617,0.191,-0.764); 1.1° disc; honest penumbrae | vector in code ✓; disc angular radius 0.0096 rad = 1.10° ✓; shadow march uses 10·h/t penumbra from the disc ✓ | PASS |
| T2 "sun's disc IN the frame, low over the far ridge — the honesty anchor" | camera projection of the sun vector: ndcx = −1.29 (\|ndcx\|>1). The disc is OUT of frame, 29% of a half-width past the left edge. Only the glow is in-frame. | **FAIL** |
| T2 azimuth-dependent sky, warm toward sun | warm amber sector on the left horizon = sun azimuth ✓ | PASS |
| T2 faint stars near zenith only | 3,630 bright pixels in the zenith band, but 6,845 star-like point sources elsewhere in the sky (y<342). The "only" is contradicted by pixels. | **FAIL** |
| T3/T13 elongation ~52° → ~19% lit | vectors give 52.1° → geometric lit fraction 19.3% ✓. Crescent present, thin amber arc, lit limb on the sunward (left) side ✓. BUT: the crescent is dimmer than the sky over most of its extent (crescent strip mean RGB 87,68,65 vs sky 113,78,105; only the brightest arc pixels exceed sky). Pixel-bright fraction is 0.1–4% depending on threshold — a viewer counting bright pixels does not find 19%. | MIXED — geometry PASS, brightness reading qualified |
| T13 disc radius 55→80 (~122px at 1024) | code r=80 ✓ (b_moonhit 6400, shade /80). Measured dark silhouette 129×137 px; report's 122px ≈ the apparent size. (On-axis prediction is 112px; the moon sits 32.7° off-axis and rectilinear stretch accounts for the rest.) | PASS with note |
| T13 planetshine 2.2× → (0.34,0.32,0.33) | code ✓; dark-side disc measured RGB (44,42,43) vs code-predicted alb·(0.34,0.32,0.33)·255 ≈ (37,35,36) ✓ | PASS |
| T13 mlen from accessors | code ✓ (no pixel test possible) | PASS (code) |
| T13b edge taper past depth gate 220, relief → −15 lowland at lateral edges | edge-band (x<120 or x>904, y 380–720) mean abs delta prefix→canon = 2.23/255 — nonzero, T13b affected pixels ✓; edge crops show ridges resolving to haze before the border ✓ | PASS |
| T9 "the near rubble must be the sharpest thing in frame" | mean abs gradient: foreground third 2.32, middle third 2.73, sky 2.20. The middle (massif) is sharpest, not the foreground. | **FAIL** (literal reading) |
| T5 detail fades with distance; near sharpest, far clean | rocks grad 2.41 > sky, but massif (mid) 2.73 is the frame maximum; far field shows no aliasing sparkle ✓ | MIXED |
| T10 dither corrected to 0.0000235 | code ✓ (`((dh−512)·0.0000235`) | PASS (code) |
| D-SHARP grad(O)=2.414 grad(B)=0.875 ratio=2.759 ≥ 1.20 | independently reproduced exactly | PASS |
| D-DET two 1024² renders byte-identical | SHA-256 `3829e2…ffaefc` verified on two clean renders | PASS |
| T13 affected pixels (moon-region delta) | 25.66/255 mean abs delta in the moon region | PASS |
| Center composition untouched | 0.00/255 center-region delta | PASS |

## Struck claims

Per the frozen prereg ("claims with no visible effect are removed from
architecture evidence"), two trace claims are STRUCK from the Fork B
evidence (the mechanisms stand; the claims about them were wrong):

1. **T2 "sun's disc IN the frame."** False. The disc is 37% of a
   half-frame past the left edge. Corrected claim: the sun's *glow* is
   in-frame; the disc itself is just out of frame. The "honesty anchor"
   as stated does not exist.
2. **T9 "near rubble sharpest in frame."** False as stated. The massif
   (middle third, 2.73) out-resolves the foreground (2.32). The D-SHARP
   bar (object vs its own background, 2.759) still holds — the claim
   that fails is the frame-global superlative.
3. **T2 "faint stars near zenith only."** The "only" is false. Star-like
   point sources (bright, isolated, <12px) number 390 in the zenith band
   but 6,845 elsewhere in the sky. Faint points exist; they are not
   confined to the zenith.

## Qualified claim

- **T3/T13 "~19% lit."** True as phase geometry (52.1° elongation →
  19.3% of the disc has dif>0), and the crescent is genuinely visible as
  a thin amber arc on the sunward limb. But it is NOT 19% bright pixels:
  the crescent is dimmer than the sky across most of its arc. This is
  the T12 overclaim pattern recurring one level down — pixel-measurable
  and eye-visible at 1024, but the number "19%" describes geometry, not
  brightness. The trace should say "19% geometrically lit; thin dim
  crescent" rather than "bold crescent."

## Blocked on Micah

- Post-repair eye verdict on the repaired moon at display size
  (the report's `moonfix_accept_256.png` evidence is mechanical; only
  his eyes bind). Nothing here substitutes for it.
