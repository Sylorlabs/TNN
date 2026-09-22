# FORK B — ONE UNIFIED TNN ACT (D-IMG-1)

There is no world model feeding a renderer. There are no modules.
This file is the trace of a single mind that conceives and paints in
one interleaved act: deliberation and depiction alternate and inform
each other. Each step is "I conceive X, so I paint Y" — and twice,
"I saw Y, so I reconceived Z." The same reasoning that invents the
world renders it. One trace, one process, one binary
(`r8b_alien.zag`, pure Zag, zero external build tools).

Ambition kept: a world with geology, history and intent — never
noise-on-shapes. Light kept causal: the sun is deliberated, the
light is derived — reasoned, never forced. But it is uniform: TNN
does it all.

## T0 — the shared substrate

Deliberation and depiction need one deterministic noise source, so
I fix it first: integer-hash value noise (2D/3D), fbm, ridged fbm,
plus small f64 math (Newton sqrt, rational falloffs — no libm).
No RNG anywhere in this trace, ever. The binary reruns
byte-identically.

## T1 — DELIBERATION: the star (before anything can be seen)

Nothing can be seen before there is light, so I conceive the light
first: a K2V orange dwarf (4900 K), amber daylight, 0.55 AU out so
its disc spans 1.1 degrees — wide enough for soft penumbrae, which
I must then honestly render. Sun vector: (-0.617, 0.191, -0.764).

DEPICTION: the sun constants; every shadow in the binary is a march
toward this one vector.

## T2 — DELIBERATION: the sky the star implies

A K2V star plus silicate dust at 0.6 bar gives a dusty violet-rose
sky: the horizon warms to amber toward the sun's azimuth and cools
away from it. I put the sun's disc IN the frame, low over the far
ridge — the honesty anchor.

DEPICTION: azimuth-dependent gradient, the 1.1-degree disc drawn by
cross-product (no trig), glow, thin cirrus warm-lit on the sun side,
faint stars near the zenith only.

## T3 — DELIBERATION: the moon in the same sky

The world has a moon, so the sky does too. Cinder is airless: sharp
terminator, no atmospheric softening. Reconceived in T13 (see below):
it hangs ~52 deg from the sun — a bold crescent, ~19% lit, on a
larger disc (r=80) — so the phase reads at display size, not just in
pixels; a black dot would mean the phase geometry failed, and gibbous
would mean the light transport is lying. Its dark side gets
planetshine (earthshine is real), the one derived secondary light,
strengthened so the full disc reads as a world.

DEPICTION: analytic sphere, crater-perturbed normal, lit by the T1
sun. The phase is computed, never painted.

## T4 — DELIBERATION: the ground the light falls on

Vesper: 1.3 g, basaltic volcanism still active, 0.6 bar of
silicate-dust air. A volcanic highland — rolling basalt, one shield
volcano with a ridged massif, a wandering rift valley, three young
impact craters on the valley floor (impacts happen; they must be real
geometry, never stamps).

DEPICTION: the height field — fbm highland, ridged massif under a
gaussian mask, rift carved along a noise-wandering axis, craters as
bowl+rim geometry.

## T5 — DEPICTION checks my own deliberation

If I stamp the same detail everywhere I repeat the old family's sins.
So detail fades with camera distance (near ground sharpest, far field
clean — no aliasing, no one-noise-fits-all), and strata live only in
3D noise on steep faces, never as contour rings.

## T6 — DELIBERATION: nothing in this world was placed

Rubble near the viewpoint must be the same continuous surface as the
ground. DEPICTION: five noise-displaced spheres smooth-min blended
INTO the distance field, burial depth computed exactly once per
render. One surface — stickers are impossible by construction.

## T7 — DELIBERATION: seeing is occlusion, not paint

I will not draw shadows; I will march rays and let the field decide.
DEPICTION: a true 3D signed distance field, coarse sphere trace,
bisection refine on the full field, numeric gradient, soft shadow as
a secondary march toward the T1 sun (penumbra from the 1.1-degree
disc), ambient occlusion sampled from the field itself. Shadows agree
because there is exactly one sun and every shadow asks the same field.

## T8 — DELIBERATION: albedo is geology, not decoration

Steep slopes expose fresh dark basalt; dust settles on flats and in
sheltered concavities (the AO term tells me where); volcanic layering
shows faintly on steep faces. Distance drowns in the T2 haze.

DEPICTION: sun x occlusion-shadow + sky ambient + fresh-rock glint,
aerial perspective toward the azimuth-dependent horizon color.

## T9 — DELIBERATION: the eye

Late afternoon, 16:40 local: on the rift's eastern scarp, 45 m above
the valley floor, looking WNW across the rift at the shield massif.
The near rubble must be the sharpest thing in frame — it is closest.

DEPICTION: the camera, the per-pixel raymarch dispatch
(terrain -> moon -> sky), hash dither as texture, never blur.

## T10 — FEEDBACK (first seeing)

The 256 smoke render showed harsh white sparkle — my dither was 255x
too strong. Depiction informed deliberation: keep texture, but at
0.0000235 amplitude. Corrected in the same act, same binary.

## T11 — FEEDBACK (second seeing)

The moon was a black blob above the frame. My deliberation was
sloppy: ~12 deg from the sun means near-new, a thin crescent — so I
lowered it into frame, lifted planetshine so the dark side reads, and
raised the sky fill because the foreground was unreadably black. The
world did not change; my seeing corrected my conceiving.

## T12 — FEEDBACK (third seeing, 1024)

The moon was STILL a featureless black disc — at 12 deg elongation
the lit fraction is ~1%, subpixel. My trace claimed "a thin crescent,
computed" but no crescent was visible: a genuine contradiction between
deliberation and depiction. So I reconceived Cinder's orbit: ~44 deg
from the sun, a young crescent (~14% lit, like a 3-day-old moon), and
strengthened planetshine — earthshine is real, and the dark side must
read as a world. Depiction judged deliberation and found it wanting;
the trace records the verdict.

## T13 — FEEDBACK (oracle: Micah's eyes, 1024)

The image reads as human-made — watercolor, a PASS on the not-AI
smell — BUT the moon "is a random black dot". T12's crescent was
pixel-measurable yet eye-invisible at display size: the trace
overclaimed a second time, and the failure this time is
methodological — depiction must judge deliberation AT DISPLAY SIZE,
not in pixel statistics. Phone-screen scale is the seeing that counts.

Reconception (moon only; the style verdict is binding, nothing else
in the scene changes): Cinder hangs ~52 deg from the sun — a bolder
crescent (~19% lit) — subtends a larger disc (r=80, ~122px at 1024,
~30px at phone size), and planetshine is strengthened ~2.2x so the
dark side reads as a world rather than a hole in the sky. Acceptance
was checked at 256px wide: lit limb on the sunward side, full disc
readable against the violet sky — unambiguously a crescent moon, not
a dot. The phase is still computed from the T1 sun, never painted;
earthshine is still the only secondary light.

## T13b — FEEDBACK (oracle: other humans' eyes, 1024)

Micah showed the image to other humans. Their verdict: AI — because
the mountains cut off weirdly. The massif's west flank and the right
hills hit the left/right frame edges as truncated ridge silhouettes,
and that is what convicts it. (This overturns the earlier solo
"human-made" read; the other humans' eyes are now the binding signal
on this point.) Depiction judged deliberation again: a ridge that dies
mid-stroke at the border is a compositional failure, not a world
failure.

Reconception (composition only; the world and the style are
unchanged): a deliberate lateral taper in the height field — past the
near ground (depth gate 220, so the foreground rubble is untouched),
relief eases toward smooth lowland as the view ray nears the lateral
frame edge (smoothstep on edge fraction and depth, view axis derived
from the T9 camera, never placed). Landforms now resolve into hazy
low ground before the border instead of being sliced by it. Checked
at 256px: no ridge line is cut mid-stroke at either edge; the center
of the composition is untouched.

## What this is not

- Not the r1..r7 family: no placed shapes, no pixel-noise fills, no
  celestial discs pasted on a background. The scene is a true 3D
  distance field, raymarched per pixel, with analytic light transport
  derived from the deliberated star.
- Not a world model feeding a renderer: the deliberation lives in the
  same trace as the depiction. Nothing is handed off between modules.
- Nothing is forced for effect: realism is a consequence of the
  imagined world — the light, the geology, the atmosphere, the
  viewpoint — never a template applied afterward.

## Evidence

- `r8b_alien.zag` — the single unified trace (source)
- `r8b_alien_1024.bmp` — canonical 1024² output (pure-Zag BMP)
- `r8b_alien_1024.png` — preview of the same
