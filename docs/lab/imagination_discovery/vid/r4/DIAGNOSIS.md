# D-VID-1 round 4 — DIAGNOSIS: why the frames read "Minecraft"

Date: 2026-09-22. Baseline: round-3 `frames/dvid1_f23.bmp` + debug channels
(foam=ch6, normal=ch7) rendered from unmodified `ocean.zag`.
Crops: 256×256 regions (foreground glitter, mid-frame foam line, spire
waterline), 2× nearest-neighbor enlargements for inspection.

## The Minecraft read, decomposed

The blocky read is not one artifact but three, ranked by measured strength:

### Culprit 1 — March-segment terracing (dominant, mid-frame)
Shading is evaluated **once per winning march step**; the winning segment's
pixels are filled with a Gouraud gradient between the current step's color
and the previous step's color. Within a segment this is smooth — but **every
segment boundary is a hard color discontinuity** (segment k's bottom color is
step k−1's color; segment k+1's top color is step k+1's color — they don't
match), and the boundary height differs per column because each column
marches independently. Result: a full grid of rectangular tiles with hard
edges on all four sides.

Evidence:
- foam debug channel, mid region: vertical edge energy **47.9**/px
  (horizontal band edges), vs 9.2 horizontal — banding dominates 5:1.
- base image, mid region: vertical edge energy 22.5/px.
- The tiles are ~10–25 px tall × ~10–40 px wide — exactly the march-step
  segment scale in the mid-field.

This is a discretization artifact, not a scene property: the true water
surface is continuous, but the renderer shades it as a stack of flat bands.

### Culprit 2 — Chunky foam breakup cells (foreground + mid)
Foam breakup is `o_vn2(wx*400, wz*400, 51)` — world-space value noise with
0.64-world-unit cells. Under perspective that's **11–33 px per cell** near
the camera (measured autocorrelation 0.5-lag: 33/16/11 px on three
foreground rows). Foam reads as discrete Minecraft blocks, and the
Gouraud fill smears each block vertically inside its segment.

Evidence: foam debug channel, foreground — visible ~15–30 px white/black
chunks with sharp vertical edges (per-column `steepf` jitter from the
`dhdx` finite difference adds the vertical striping: horizontal edge
energy 3.0 fg / 9.2 mid).

### Culprit 3 — Oversized normal facets, impotent micro-normals
The "fine shading detail" perturbation (`bn`, world-scale 90, amplitude
±35/1000) has **~187 px cells** near the camera — it is effectively a
second set of giant facets, and its amplitude (±2°) is invisible next to
the swell normals. The normal debug channel is nearly flat gray in the
foreground: specular and diffuse vary in huge smooth patches with no fine
glitter structure. Real sun glitter needs cm-scale facets.

Secondary contributors (noted, lower priority):
- Spire silhouettes: hard 1-px stepped edges + one flat fill color per
  column (no vertical shading variation, no sub-pixel coverage).
- Per-column `dhdx` finite-difference jitter → faint vertical striping.
- ±2-LSB dither is fine (not a contributor).

## What the fix must do (derived from the diagnosis)

1. Shade **per pixel from per-pixel surface parameters**, not per march
   segment — the surface is continuous; each pixel images one surface
   point. (Kills culprit 1 at the root.)
2. Give foam a physically fine cell size in world units (foam lace, not
   0.64-world-unit blocks), evaluated per pixel. (Kills culprit 2.)
3. Put real multi-scale structure in the normals: short-wave elevation
   (true height derivative) + capillary-scale facets for the specular
   lobe, distance-faded against aliasing. (Kills culprit 3.)
4. Shade spires per row with cone normals + sub-pixel silhouette
   coverage. (Kills the secondary spire stepping.)

## Candidate mechanisms (each tested alone as a crop vs baseline)

| ID | Mechanism | Class (Micah's law) |
|----|-----------|---------------------|
| Ma | Micro-chop octaves: short-wave elevation finite-differenced into the normal (does not touch marching → no occlusion instability) | LOGIC-DERIVED — short gravity waves are real elevation; their shading effect is surface tilt |
| Mb | Finer foam breakup: world-scale 400→1600 (0.16-world-unit cells), same advection speed | LOGIC-DERIVED — foam forms fine lace, not 0.64-world-unit blocks |
| Mc | Spray/mist at spire bases and waterline: deterministic droplet cells + soft mist band | LOGIC-DERIVED — surf against rock aerosolizes water |
| Md | Tighter specular glints: capillary-scale normal jitter applied to the specular lobe only | LOGIC-DERIVED — sun glitter comes from cm-scale facets |
| Me | Layered fine normal octave (2nd octave at 4× frequency in the shared normal) | LOGIC-DERIVED — wave normals are multi-scale |
| Mf | Atmospheric micro-variation: per-pixel fog grain | COSMETIC — no scene truth; fog is smooth; this is grain |
| Mg | Per-pixel shading across march segments: interpolate surface params between bracketing winning steps, shade every row | LOGIC-DERIVED — the surface is continuous; each pixel images one surface point |
| Mh | Spire per-row shading with cone normals + sub-pixel silhouette coverage | LOGIC-DERIVED — rock is a 3D solid; silhouette pixels are partially covered |

Per Micah's law (2026-09-22): the flagship advances ONLY on logic-derived
mechanisms. Mf is the negative control — included to test whether a pure
cosmetic tweak can fake the effect (expected: it adds grain, verdict KILL).
