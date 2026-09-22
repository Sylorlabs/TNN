# Blind judgments — ROUND 3 (2026-09-22)

5 NEW fresh judges (never saw rounds 1–2), same protocol: normal viewing
criteria, zero pipeline knowledge, judged the round-3 rebuilt artifacts.

## Tally ("would not guess AI" or "unsure")

| Judge | IMG-1 alien | IMG-2 arch | VID f00 | VID f23 | VID f47 |
|---|---|---|---|---|---|
| R3-J1 | Yes | Yes | Yes | Yes | Yes |
| R3-J2 | Yes | Unsure (procedural) | Yes | Yes | Yes |
| R3-J3 | Yes | Unsure (CG render) | Unsure (procedural) | Unsure | Unsure |
| R3-J4 | Yes | Yes | Yes | Yes | Yes |
| R3-J5 | Yes | Yes | Yes | Yes | Yes |
| **"not AI"/unsure** | **0/5** | **2/5** | **1/5** | **1/5** | **1/5** |

## Verdicts

- **D-IMG-1: FAIL** (0/5).
- **D-IMG-2: FAIL** (2/5, tells named by all 5).
- **D-VID-1: FAIL** (1/5, tells named by all 5).

Three full rounds. The verdict has not moved.

## The stable diagnosis (consistent across 15 judges, 3 rounds)

1. **Geometry too perfect** — concentric target-rings, equilateral triangle,
   five evenly-spaced identical spires, rigid tile grids. Real scenes and
   human art are imperfect; the generators are not.
2. **Textures applied ON surfaces, not worn INTO them** — noise fills,
   speckle overlays, marble swirls with no weathering, no pores, no seams
   where blocks would join, no light interaction between elements.
3. **Programmatic signature** — all five read as procedural/CG generation:
   not diffusion-AI artifacts, not human artwork, not photographic. The
   failure mode is "reads as a procedural render," and it is stable.
4. **Video-specific:** the per-column marcher structure reads as giant
   square blocks / a low-res upscale; motion reads as tile-reshuffling, not
   fluid flow; sun, spires, clouds frozen across frames while only the
   water pattern shuffles — "a static render with a noise-shuffled water
   texture."

## Consolidated round-3 tells

**Alien:** concentric target-planet bands (not latitude bands), halo as flat
2D overlay with posterized ring-stepping, orange storm spot = flat sticker
with no shading integration, mountains = fractal ridges with zero erosion
structure, foreground = uniform noise-splatter fill with orange dots,
mountains don't respond to the planet, halo glows uniformly behind it.

**Arch:** a single logo-like geometric glyph, not a scene; flat vector-like
bevel shading; dark notch seam at apex; miter-fold joints at base corners;
bottom bar ends overshoot into sharp points; faint seam/light line across
apex; zero environment integration — no ground, no contact shadow, no
lighting interaction; background speckles read as noise layer, not stars;
faint horizontal smudge streaks in background.

**Video:** sea = coarse tiled texture of hard-edged square blocks (teal/
white/black) with visible stair-stepping — reads as nearest-neighbor
upscale of a low-res field; five horizon spires = identical dark triangles,
evenly spaced (2nd and 4th pixel-identical to one judge); sun = plain white
disc with cheap radial glow; clouds = flat hard-edged white streaks /
smear-strokes with no form; flat bright-white waterline band; vertical
stretching/smearing of near-field blocks; tile pattern reshuffles between
frames (mechanical redistribution, not fluid motion); sky/sun/spires
frozen while only water shuffles.

## Paradigm conclusion

Three rounds of tell-repair have converged: the defects are no longer
specific fixable bugs but the NATURE of the field-generation method.
Patching tells within this paradigm has diminishing returns approaching
zero. Round 4 must test a different hypothesis: composed scenes (built
like a digital painter — imperfect geometry, atmospheric unity, wear and
story in the details) rather than generated fields. Single-subject test
first (alien planet); expand only if the blind bar moves.
