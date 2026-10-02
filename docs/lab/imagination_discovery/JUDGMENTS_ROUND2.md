# Blind judgments — ROUND 2 (2026-09-22)

5 NEW fresh judges (never saw round 1), same protocol: normal viewing
criteria, zero pipeline knowledge, judged the repaired artifacts.

## Tally ("would not guess AI" or "unsure")

| Judge | IMG-1 alien | IMG-2 arch | VID f00 | VID f23 | VID f47 |
|---|---|---|---|---|---|
| R2-J1 | No (reads as procedural render) | Unsure | No ×3 (procedural) | — | — |
| R2-J2 | Yes | Yes | Yes | Yes | Yes |
| R2-J3 | Unsure | Unsure | Unsure | Unsure | Unsure |
| R2-J4 | Yes | Unsure (lean yes) | Yes | Yes | Yes |
| R2-J5 | Yes | Yes | Yes | Yes | Yes |
| **"not AI"/unsure** | **2/5** | **3/5** | **2/5 each frame** | | |

Bar: ≥3/5 "not AI"/unsure AND no template/blur tell named unprompted.

## Verdicts

- **D-IMG-1: FAIL** (2/5, and tells named by all 5).
- **D-IMG-2: FAIL** (3/5 on the count, but every judge named template tells
  unprompted — the strict condition fails).
- **D-VID-1: FAIL** (2/5, tells named by all 5).

## Pattern across judges (the honest finding)

4 of 5 judges independently classify the work as PROCEDURAL/DETERMINISTIC
renders rather than diffusion-model AI: "reads as a Terragen-era 3D render",
"a shader/simulation frame", "a procedural turbulence texture". The defects
are compositional and textural (tiled noise, flat primitives, hard seams,
banding) rather than classic AI giveaways (garbled text, malformed anatomy).
The bar's spirit — "you would've never guessed it was an AI", i.e. reads as
real or genuinely human-made — still fails: judges guess synthetic every
time, just a different kind of synthetic.

## Consolidated round-2 tells (feed round 3)

**Alien planet:**
1. Repeating fractal-swirl texture tiles across all ridges; identical grain
   near and far; no atmospheric or geometric variation between ridge rows
   (3+ judges).
2. Planet = pasted disc + ellipse layers: horizontal banding across lower
   half, ghost double-edge on rings behind disc, hard clipped wedge where a
   ring meets the limb (3 judges).
3. Scene reads as stacked template bands (sky gradient / ridge ×3 / planet
   + rings), different texture style per band (2 judges).
4. Planet lighting unrelated to scene; soft white halo doesn't interact with
   the sky behind it (2 judges).

**Architecture:**
1. Apex miter botched: right beam overhangs with a lip/overlap — two rotated
   rectangles composited, not real joinery (3 judges).
2. Beam texture = noise-fleck overlay that doesn't follow beam direction;
   no wear variation; warm-left vs cool-bottom lighting mismatch (3 judges).
3. Starfield = even dot pattern with a hard horizontal cut at the top third
   (3 judges).
4. Bottom gray bar: flat gradient strip with a hard ungraded edge, no
   compositional purpose — canvas artifact (2 judges).

**Video:**
1. Repeating cellular/crescent sparkle tiling at uniform scale — shader
   signature (5 judges).
2. Vortex = distortion-filter stamp on the noise field: smeared melting
   contours, smear trails crossing the ripple direction, a dark patch with a
   hard vignette-ish edge (4 judges).
3. Teal/green vs deep-blue split reads as RGB-shift/palette re-tint, not
   material color (2 judges).
4. Blocky pixel steps in highlight clusters — reads as an upscaled low-res
   source field (2 judges).
5. No scene content at all: no subject, horizon, focal plane, or depth —
   pure texture wash (3 judges).

## Note on diminishing returns

Two full rounds, 13+14 tells repaired, and verdicts have not moved to
"real": the remaining tells converge on "it is procedural", which is
inherent to the deterministic integer-hash field method — the textures
repeat, band, and tile no matter how well they are composed. Round 3 needs
a fundamentally better renderer (non-repeating multi-scale structure,
real occlusion/lighting integration, wear that follows geometry), not
more tell-patching. A-BLIND (audio) still pending — Micah's ears binding.
