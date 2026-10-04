# Round 7 report — alien planet landscape (D-BLIND repair round)

Date: 2026-09-22. Source: `r7_alien.zag` (pure Zag, zero RNG).
Artifact: `r7_alien_1024.bmp` (24-bit, 1024×1024), PNG preview `r7_alien_1024.png`.

## Why round 7 exists

On 2026-09-22 at ~16:53 UTC, five fresh blind judges unanimously read round 6 as
AI/procedurally generated (0/5 passing). Converged tells:

1. Tiled/topographic procedural texture across different materials.
2. Vertical banding and repeating geometry inside the mountain massif.
3. Perfect-circle or pasted-looking celestial bodies.
4. Uniform stamped pebble dashes/speckle.
5. Sticker-like rocks with haloed edges.
6. Inconsistent lighting.
7. Soft, detail-poor foreground despite its proximity.
8. Flat or smeared clouds.

Round 6 passed every mechanical bar (D-RES/D-SHARP/D-COMP/D-DET) but failed
D-BLIND. Round 7 fixes the eight tells **by eye**; round 5 established that
metric-chasing makes images measure cleaner but look worse.

## Preserved from round 6

Composition, palette, crisp silhouettes, inter-plane haze, one unified sun
toward (-880, -260, +390). All scene-builder call conventions and the render
loop layout are unchanged.

## What changed (per-judge-tell, diagnosed not metric-chased)

**Tell 2 — vertical banding (root-caused this round).**
Round 6 blamed a too-narrow lighting baseline and widened it; the stripes
survived. In round 7 I traced the real chain:
- 1D ridge noise sampled at constant y has V-shaped creases; any
  finite-difference lighting gradient straddling a crease prints a light/dark
  vertical stripe pair. Fix: the far range is now lit from a NEW smooth profile
  (`r7_hf_far_s`, fbm-only, peak + broad swells, no ridge terms); the creased
  `r7_hf_far` draws the silhouette only. The mid-hill lighting profile
  (`r7_hf_mid_s`) had the same 1D-ridge defect and was converted to fbm.
- Smoothing exposed a second defect: raw gradients of the smooth profile are
  <1px/px, and plain integer division posterized the lighting into 3–4 hard
  vertical levels (the stripes that survived the profile fix). Fix: gradients
  are now fixed-point ×64 (`gxf`, `gxfw`, `gxm`), and the `l`/`asp` formulas
  divide by 64. This also explains round 6's "flat shading with no real
  light falloff": its raw gradients were so large the old `×300` factor
  clamped almost everything to 90/1024.
- The gully lateral-lean terms were quantized on per-74px / per-68px hash
  cells (`r7_h01(x/74,…)`, `r7_h01(x/68,…)`), printing vertical seams every
  74/68px. Both now use smooth fbm.

**Tell 1 — tiled contour texture.**
- Rock albedo: single-scale fbm mottle → two-scale (fine grain dominates,
  broad blob term weakened); the broad contour-line blobs are gone.
- Strata spacing: hash-quantized steps → smoothly varying fbm spacing;
  strata lines are x-segmented so they never span the whole range; segmented
  ledges replace continuous ledge lines.
- Foreground plain: added mid-scale fbm clumping + stronger fine grit, so
  the plain reads at three scales (drifts / clumps / grit) instead of one
  soft wash.
- New second ground layer `r7_stones`: sparse half-buried stones (crown only,
  drift-gated, dust-settled), drawn under the boulder shadows.

**Tell 3 — pasted celestial bodies.**
- Planet limb wanders (fbm wobble on the radius, anti-aliased over the
  wobbled edge); terminator widened (hard day/night edge gone); night side
  keeps faint fbm flow structure instead of a flat fill; the bright storm
  core dimmed into the zonal palette.
- Moon: softer phase transition, stronger albedo contrast (was a flat gray
  fill); zonal warping strengthened.

**Tell 4 — stamped pebbles.**
Drift-gated density mask (patchy, never a uniform grid); size range 2–11px;
some stones half-buried (small, dark, dust-covered, no shadow).

**Tell 5 — sticker rocks.**
Contact darkening is now shadow-side-only and broken by noise; the old full
dark ring (cutout halo) is gone.

**Tell 6 — inconsistent lighting.**
Far range gains massif-scale aspect shading (±60px baseline on the smooth
profile) and the haze blend eased so directional lighting survives; clouds
carry sunlit fibers; rocks/planet/moon/pebbles all key off the same sun.

**Tell 7 — soft foreground.**
Three-scale texture (above); the closest ground is now the sharpest plane.

**Tell 8 — flat clouds.**
Fibrous interior (combed ridged noise), ragged eroded edges, sunlit fiber
crests; cirrus keeps its stretched form.

## Bar results

| Bar | Result |
|---|---|
| D-RES | PASS — 1024×1024, 24-bit |
| D-SHARP | PASS — ratio 2.657 (≥1.20); grad(O)=4.599, grad(B)=1.731 |
| D-COMP | PASS — zero axis-aligned filled-primitive placement tokens (grep audit) |
| D-DET | PASS — 3/3 clean renders byte-identical |
| BMP SHA-256 | `0a9183fd9098413070dc7d915e3d205b2734bf2df29605cd1340afe35d068cef` |

Pure Zag, zero RNG, all indexed slices below 2²⁵. Built with
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(`--no-zagd --no-analyze`).

## Blind judging

Round 7 is built, tested, and committed. D-BLIND judging (5 fresh judges,
question "would you have guessed AI?") is dispatched separately by the
coordinator — not run from this report.
