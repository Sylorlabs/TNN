# BEAUTY DIAGNOSIS — why r8b reads "2000s CG"

Date: 2026-09-22. Round: r10 (beauty push, Track A). Oracle verdict driving
this round (third party via Micah): the alien planet stills "look like
2000's computer graphics, not what you'd imagine an alien planet looks
like." Micah's bar: THE MOST BEAUTIFUL THING HE HAS EVER SEEN. New
standing requirement: TNN must have a PROPER RELATIONSHIP WITH DISTANCES
— near vs far must read correctly (scale cues, atmospheric perspective,
depth ordering, parallax-consistent detail falloff).

Micah's law (standing): imagination means LOGIC — every visible change
must trace to a deliberated scene truth. Classified LOGIC-DERIVED vs
COSMETIC in BEAUTY_MECHANISMS.md; flagship advances on logic-derived only.

Method: 256×256 crops cut from the frozen baseline `r8b_alien_1024.png`
(byte-frozen artifact, sha in ROUND8A lineage), viewed at 2×. Crop PNGs in
`r10/crops/beauty_*.png`. Every tell below was verified by eye against
these crops — the task brief's starter list was checked, not trusted.

## B1 — The horizon slab: a dead gray band with a razor edge (strongest tell)

Evidence: `beauty_horizon.png`, `beauty_glitter.png`, `beauty_ridge.png`.
At the left horizon sits a flat gray-pink BAND with perfectly straight
top and bottom edges, containing a floating orange ellipse "island."
It reads as a painted sea/river on a matte painting — the single most
2000s-CG element in the frame. Root cause: the T13b edge-taper flattens
far relief toward h=-15 past ~220 depth units near the lateral frame
edges; the aerial-perspective mix (`f=1-exp(-t*0.0011)`) grays it toward
the horizon color but the GROUND/SKY boundary stays a hard silhouette
edge — a flat plane at grazing incidence with a knife horizon line.
There is no water geometry; the "sea" the brief mentions is this slab
pretending to be hazed ground. The orange blob is a partially-tapered
sunlit slope (or crater rim) floating in the gray — an island in a dead
sea. Missing scene truth: at 1600 depth units in 0.6 bar of silicate-dust
air, the far field should DISSOLVE into the horizon sky — and the
compositional band should either be honest ground fading out or honest
water. NOTE: the brief's "(4) the sea is a flat band" is half-right —
there is no sea, only a band that reads as one. The r10 reconception
(T14): the graben floor floods — the band becomes a real rift lake.

## B2 — Foreground crushed to black; no sky-fill legibility

Evidence: `beauty_foreground.png` (340,700,256² at 2×).
The near foreground is a near-featureless black wash — albedo texture
vanishes where direct sun dies. Root cause in `b_tshade`: the ambient
term samples the deliberated sky dome ONCE, in the surface-normal
direction — straight up, where the dusk sky is darkest (zenith
0.13,0.12,0.26). But a ground point's hemisphere INCLUDES the bright
amber sunward horizon band (0.85,0.45,0.28); sampling only the normal
direction throws that light away. On a dusty world at dusk the sky IS
the light for shadowed ground, and the renderer is ignoring most of it.
Estimated fill on flat dust: ~0.03 → ~8/255. Missing: hemisphere
integration of the deliberated dome (two-lobe approximation), not a
brighter constant.

## B3 — Waxy/plastic specular streaks + aliased sparkle chains

Evidence: `beauty_massif.png` (ridge at left shows a dotted BRIGHT CHAIN
along the crest), `beauty_foreground.png` (isolated white speckles on
black ground), `beauty_ridge.png` (diagonal wet-plastic smears).
Root cause: the T8 "fresh-rock glint" — `sp32*sp16*sp8*sp4 * 0.12`,
a power-~60 lobe on a noisy normal field. Sub-pixel normal variation
makes the lobe fire on isolated pixels: sparkle chains and speckles
(the T10 dither fix addressed dither, not this). On broad slopes the
same lobe smears into waxy highlights — basalt reading as wet plastic.
Missing scene truth: a rough surface's specular integrates over the
pixel footprint (microfacet reasoning) — the lobe must widen and weaken
with distance, not sparkle; near-field volcanic glass may still glint.

## B4 — No atmospheric perspective worthy of the name

Evidence: full frame + `beauty_ridge.png`.
The far ridge behind the massif is nearly as dark and contrasty as the
mid-ground; the fog that exists (`t*0.0011`) only grays. At 0.6 bar of
silicate dust the far ranges should PALE toward the horizon sky —
lose contrast, not just shift hue. Root cause: the scattering
coefficient is too small for the deliberated atmosphere, and the fog
color target is dim on the anti-sun side. The depth ordering reads
collage-like (cf. the Fork A critic: "construction-paper strips").
Missing: honest exponential scatter at the deliberated dust density,
fog color from the azimuth-dependent horizon, full dissolve at the far
plane so no slab edge survives.

## B5 — Moon: a black balloon with a thin crescent

Evidence: `beauty_moon.png`.
Cinder reads as a flat black disc with a thin lit limb — the dark side
is ~85% of the disc and nearly featureless, so against the bright
violet sky it reads as a HOLE, not a world. Root cause: planetshine
(0.34/0.32/0.33 × albedo ≈ 0.12–0.18 → ~35/255) is below display-size
legibility for the disc interior; the terminator is razor (correct for
airless) but the lit crescent has no limb falloff. NOTE on the brief's
"limb glow from thin atmosphere": Cinder is deliberated AIRLESS (T3 —
"sharp terminator, no atmospheric softening"). A limb glow would
contradict the world; declined. The honest fix is stronger
phase-consistent planetshine (earthshine is real) so the full disc
reads, with crater shading kept consistent with the one sun.

## B6 — Clouds: blurry gray smears at uniform brightness

Evidence: `beauty_sky.png`.
The cirrus reads as flat brush-strokes: uniform mask brightness
regardless of azimuth or distance, no sun-side silver lining, no
filament structure, no fade into the horizon haze. Root cause in
`b_sky`: the cirrus mask `m` is azimuth-blind (only the COLOR mixes
toward warm on the sun side), and the elevation gate
`ss((dy-0.02)/0.15)` fades the deck but nothing ties brightness to the
forward-scatter geometry. Missing scene truth: ice streaks between
viewer and sun forward-scatter (Mie) — the sunward edges silver;
upper winds shear the streaks along the deliberated flow (r9 M-c);
a deck 50 km away merges into horizon haze.

## B7 — Zero scale cues; melted-taffy rocks (r9's line, folded in)

Evidence: r9 DIAGNOSIS.md D1/D2 (verified in `beauty_foreground.png` —
the five near rocks are invisible in the black crush; where visible in
r9's crops they are smooth-min welded taffy).
The r9 detail crew's diagnosis stands: noise-displaced spheres welded
with `b_smin(...,3.0)`, no discrete pebbles, no angular talus, albedo
grain too weak. Their rev2/rev3 mechanisms (M-F angularity, M-A/M-P
cobbles + per-cobble tint, M-D ejecta grain, M-b striation, M-e talus)
are folded into r10 as the near-field foundation. Judging status at
r10 build time: r9 blind judging was still in flight (`_judging_` in
MECHANISMS.md) — the revs are included on the crew's own iteration
evidence (originals logged MISS/FAIL by the crew), flagged as
pending-judgment in the mechanism table.

## B8 — Geology: smooth clay slopes, no strata

Evidence: `beauty_massif.png`, `beauty_ridge.png`.
Broad slopes shade as smooth clay; the "volcanic layering" the T8
comment claims is not in the code path (only noise tint on steep
faces). Missing: flood-basalt strata — thin flow-banding on steep
faces, world-space, subtle; plus the r9 M-b fall-line striation.

## What is NOT broken (kept)

- One-sun light transport: the sun vector, moon phase, and shadow
  marches all derive from the T1 accessors — byte-identical, enforced
  by the generator script's diff assertion.
- The composition: rift valley → massif → horizon band → moon; the
  r10 work keeps the camera, the massif, the rift, and Cinder's orbit.
- The sky gradient's azimuth logic (warm toward sun, cool away).
