# IMAGINATION DISCOVERY — Image Pipeline Notes (D-IMG-1, D-IMG-2)

Date: 2026-09-22. Generator: `disc.zag` (pure Zag, compiled with the pinned
`znc_linux_x86_64_abed8aa1` toolchain). Verifier: `verify_bars.py` (Python,
verification + lossless PNG preview only — never in the generation path).

## Pipeline operation

One Zag executable, `disc`, selects the subject from `argv[1]`
(`alien` | `arch`), the output directory from `argv[2]`, and the resolution
from `argv[3]` (`1024` | `2048`). It allocates a single image-sized RGB
buffer, rasterizes the scene **directly at the target resolution, one pixel
at a time**, then emits a bottom-up 24-bit BMP with chunked (≤1 MiB) writes.
BMP is written with `O_TRUNC` (never `O_EXCL`, which fails silently on
existing files). PNGs are lossless re-encodings produced by the Python
verifier for preview only.

## Bypassing the old 512² / 32 MiB cap

The legacy pipeline rasterized onto a 512² working grid (u4f) and upscaled.
`disc.zag` never builds a low-res grid: every pixel's color is computed from
closed-form deterministic noise fields sampled at that pixel's coordinates,
so resolution is a free parameter. The only resolution-dependent cost is one
`w*h*3`-byte buffer, which stays under znc's 2^25-byte single-slice indexing
limit at both 1024² (~3.15 MB) and 2048² (~12.6 MB). No chunking of the
image buffer itself is needed at these sizes.

## Deterministic noise core (shared)

- 32-bit integer coordinate hash (no RNG anywhere; two clean-process reruns
  are byte-identical, SHA-256 verified).
- Fixed-point smooth value noise, multi-octave fBm, ridged fBm, domain
  warping (all integer/fixed-point; the architecture scene additionally uses
  Zag `f64` for its analytic beam geometry while all procedural texture
  remains integer-noise based).
- Monochromatic per-pixel hash dither (±3 LSB) so gradients never band; the
  dither is hash-based texture, not blur, and the sharpness bar still passes
  at 2.4–2.5×.
- Zero axis-aligned filled-primitive placement calls in either scene builder
  (D-COMP grep audit passes); all coverage is per-pixel analytic tests
  (point-in-convex-quad, segment distance, radial falloff).

## D-IMG-1 — Alien planet (`disc alien . 1024`)

Extrasolar surface vista: domain-warped ridged/fBm terrain with separate
broad (relief lighting) and fine (albedo) fields, procedural strata palette,
glowing contour-derived lava veins, aerial perspective, a warped-fBm cloud
deck plus cirrus sampled in sky-UV for isotropy, and a ringed planet with
procedural bands, storms, limb darkening, and terminator shading. A dedicated
broad-crested ridged skyline field keeps the mountain silhouette from going
needle-like.

Notable bug fixed 2026-09-22: the 5-stop/4-stop palette interpolators
indexed one band too many (`vv*5` for 5 stops), pushing interpolation factors
past 1024 and wrapping channels through `&255` into magenta (~1,058 magenta
pixels). Fixed to `vv*4` / `vv*3` with channel clamps before packing;
magenta pixel count after fix: 0.

## D-IMG-2 — Impossible architecture (`disc arch . 1024`)

A Penrose-triangle stone frame: three convex beam quads with cyclic overlap
(beam 0 wins at vertex 1, beam 1 wins at vertex 2, beam 2 wins at vertex 0),
so each beam passes over one neighbor and under the other — the impossible
cycle. Coverage is point-in-convex-quad per pixel; the winner's inner edge
is extended past each miter and its diagonal end-cap is darkened to draw the
occlusion cut. Bevel shading (top-light), stone grain/mottling/cracks from
integer noise, ambient occlusion at the miters, drop shadow, and vignette.

## Measurements (final, 2026-09-22)

| Subject | File | Size | grad(O) | grad(B) | Ratio | D-RES | D-SHARP | D-COMP |
|---|---|---|---|---|---|---|---|---|
| D-IMG-1 alien | `d-img-1_alien_1024.bmp` | 1024×1024 24-bit | 7.813 | 3.257 | 2.399 | PASS | PASS | PASS |
| D-IMG-2 arch  | `d-img-2_arch_1024.bmp`  | 1024×1024 24-bit | 1.850 | 0.750 | 2.468 | PASS | PASS | PASS |

Sharpness bar: `grad(output) ≥ 1.20 × grad(downscale-by-2 then box-upscale-by-2)`.
Both exceed it at ~2.4×.

Determinism (two separate clean processes, final binary):
- alien BMP: `d9b036e6…95c56f4` both runs — identical.
- arch BMP: `b6591516…04f2b9a7` both runs — identical.

Render time (1024², lab VM): alien ~7.8 s, arch ~1.9 s.

### Artifact SHA-256

| File | SHA-256 |
|---|---|
| `d-img-1_alien_1024.bmp` | `d9b036e6f7d34b5dd7f116926fb943b16d1584c66629049b46a23d5be95c56f4` |
| `d-img-1_alien_1024.png` | `9bdf0952d1f8741d3deb3030db601b53bf9cf7dd086349baa4d3f85108d649eb` |
| `d-img-2_arch_1024.bmp`  | `b6591516b3cdfee30f96b917369026319a5a700b129c3037cbef85d604f2b9a7` |
| `d-img-2_arch_1024.png`  | `5d55037658e117e0340f57afbb2cef98b1ff2e7ee84380a6002a64a39a268f33` |
| `disc.zag` | `f13170a220b5fcd0ac0d3197570c2345818ca0d4e9b4b741d1c2113038197f7a` |
| `verify_bars.py` | `a413f6b8537aa46335b5bb829d26326f6c4c91001c488ebd70840de49d11c18f` |

## Limitations (honest)

- No blind quality judgment was performed by this crew; a separate judging
  pass follows. Passing D-RES/D-SHARP/D-COMP is mechanical, not aesthetic.
- 2048² was not attempted: the 1024² scenes were only just finalized, and the
  prereg sets 1024² as the exact minimum with 2048² optional. The pipeline
  supports it (buffer ≈ 12.6 MB < 32 MiB limit); it is untested.
- The architecture scene uses `f64` for beam geometry (deterministic on
  x86-64, but not the integer-only discipline used elsewhere); all texture
  noise remains integer-hash based.
- The alien skyline, while broad-crested, still leans spiky in places; the
  lava veins are subtle at 1024².
- `disc` binary, `.zagd`/`.zag-cache` files, and debug renders are build
  artifacts and are excluded from the commit.

---

## Round 2 repairs (2026-09-22) — blind-gate tell fixes

The round-1 images passed all mechanical bars but failed the fresh blind
gate. A separate blind crew listed 7 tells; this round repairs each one
structurally in `disc.zag` (source SHA
`f3f61e1d9a19323fc4ceeb9200b18bb082541785000fe7be5c3496c5aa515b34`).
Aesthetics were NOT self-judged — a separate blind crew re-judges.

### D-IMG-1 (alien) repairs

1. **PASTED PLANET** — rewritten planet renderer (`d_sky2`): a thin limb
   haze rim plus a forward-scatter halo biased toward the shared sun side
   (upper-left) sits between planet and sky; the cloud deck renders BEHIND
   the planet; wispy cirrus filaments drift IN FRONT of the lower limb;
   the back ring carries the planet's shadow bite; the ring casts a shadow
   band onto the planet; the front ring crosses the planet's lower half
   with its own terminator darkening. Cloud and terrain lighting both key
   off the same upper-left sun.
2. **FRACTAL-MOUNTAIN TILING** — terrain is now three ordered depth planes
   (`d_edge_far/mid/near`), each with its own field scale: far = broad
   massifs (150px ridge cells, heavy warp), mid = crags (48px cells),
   near = scree/detail (14px cells). Per-plane aerial perspective
   (strong blue wash on far, warm and contrasty on near), strata banding
   on far/mid, erosion streaks on mid/near, lava flows on near.
3. **LOWER-THIRD MUSH** — the near plane keeps full fine-octave detail
   (no blur with distance; contrast is preserved, only color warms and
   aerial perspective tints).

### D-IMG-2 (architecture) repairs

4. **ARCH SEAMS** — the cyclic over/under relation is preserved (mitered
   quads, each beam over one neighbor and under the other), but the butt
   look is gone: the winner's lap gets a scarf bevel (darkening within
   10px of the cut), an end fade at the lap tip, a highlight lip along its
   inner edge, the loser gets a soft contact shadow beside the cut, and
   ambient occlusion grounds each inner corner.
5. **IDENTICAL BEAM MOTTLE** — per-beam material: separate hash seeds per
   beam, per-beam tint (warm / cool / neutral), directional weathering
   streaks and scratch lines along each beam's axis, per-beam grain,
   mottle, cracks, and edge wear.
6. **FLAT SHADOW** — a 12-sample shadow cone along the light direction:
   samples near the frame stay hard (contact), farther samples spread in a
   widening cone, giving a contact-hardened soft shadow with
   distance-dependent penumbra on the wall.
7. **VOID BACKGROUND** — a full environment: night sky with stars and a
   dim glow, rock wall with strata and vertical shading, stone floor with
   a light pool under the frame, distance fog and horizon ambient
   occlusion, plus vignette.

### Round-2 measurements (final, 2026-09-22)

| Subject | File | Size | grad(O) | grad(B) | Ratio | D-RES | D-SHARP | D-COMP |
|---|---|---|---|---|---|---|---|---|
| D-IMG-1 alien | `d-img-1_alien_1024.bmp` | 1024×1024 24-bit | 10.254 | 4.115 | 2.492 | PASS | PASS | PASS |
| D-IMG-2 arch  | `d-img-2_arch_1024.bmp`  | 1024×1024 24-bit | 1.996  | 0.838 | 2.383 | PASS | PASS | PASS |

Determinism (two separate clean processes, final binary, 2026-09-22):
- alien BMP: `55b69f70…7753e` both runs — identical.
- arch BMP: `45d8a9c9…cda2643` both runs — identical.

Render time (1024², lab VM): alien ~10–11 s, arch ~6 s.

### Round-2 artifact SHA-256

| File | SHA-256 |
|---|---|
| `d-img-1_alien_1024.bmp` | `55b69f7058eee945243e6f09f448e5409febed77c8fdce6cf5e6d3923677753e` |
| `d-img-1_alien_1024.png` | `595f0718adaf93839f582d1f5d42367f01e2e2854d44a1e9cd86debeca8a560a` |
| `d-img-2_arch_1024.bmp`  | `45d8a9c925fbca0b48bb037a93ef42cede577dcc61ca39663e86968e6cda2643` |
| `d-img-2_arch_1024.png`  | `bfe4b4e0093674918f2a35f5b3ced30a023cb9b91ca08d4c26acfb88dac20714` |
| `disc.zag` | `f3f61e1d9a19323fc4ceeb9200b18bb082541785000fe7be5c3496c5aa515b34` |
| `verify_bars.py` | `a413f6b8537aa46335b5bb829d26326f6c4c91001c488ebd70840de49d11c18f` |

### Round-2 honest limitations

- The blind re-judgment is a separate crew's gate; nothing here claims it
  passed — only that the 7 listed tells were addressed structurally.
- 2048² remains untested (prereg minimum is 1024²).
- The architecture scene still uses `f64` for beam geometry; all texture
  noise remains integer-hash based.
- During round 2 a first draft of the wisps-in-front fix used the planet
  bounding box directly and left a faint rectangular boundary in the sky;
  caught on inspection and fixed with a radial falloff — the final images
  carry no box edges.

---

## Round 3 rebuild (2026-09-22) — second blind-gate tell pass

The round-2 images passed all mechanical bars but failed the fresh blind
gate again. A separate blind crew listed 8 tells (4 alien, 4 architecture).
This round rebuilds both scene renderers in `disc.zag` (source SHA
`a5cabe01931cba8bd95dcb1672e5decc311294b760d5458610a0524cf26fb120`)
to close each tell structurally. Aesthetics were NOT self-judged — a
separate blind crew re-judges (D-BLIND remains their gate, unclaimed here).

### D-IMG-1 (alien) — tell-by-tell

1. **REPEATED FRACTAL-SWIRL / SAME GRAIN NEAR+FAR** — the single terrain
   generator is replaced by three structurally different materials, one
   per depth plane, each with its own seed, scale, palette, lighting, and
   detail character: FAR = domain-warped terraced massifs (quantized
   benches, strata risers, aerial wash, clouds drifting between peaks);
   MID = domain-warped faulted crags (discontinuous fault steps, contour
   strata, concavity shading, downhill scree); NEAR = cellular
   boulder/talus mounds plus a separate ridged detail field with lava
   accumulating in the lows. A valley-fog function joins mid/near into
   continuous depth instead of stacked bands.
2. **PASTED DISC + ELLIPSE-LAYER PLANET** — the planet renderer is
   rebuilt: analytic tilted annulus with soft coverage edges; front/back
   ring ordering from ring-plane depth; planet shadow on the ring solved
   in 3D (ray impact parameter); ring shadow on the disc via
   ray-plane intersection; planet texture follows latitude relative to
   the ring plane (bands parallel to the rings) with two explicit storm
   cells; terminator, limb darkening, and limb haze all keyed to the same
   scene sun; asymmetric forward-scatter halo; cirrus drifting in front
   of the lower limb. **Bug caught and fixed during this round:** the
   planet dispatch bound (`d_a_sky_px`) was `1.6*rp` while the rings
   extend to `2.3*rp`, clipping the annulus at the dispatch square and
   leaving a faint rectangular boundary in the sky (edge gradient ~106
   LSB at the square border). Fixed to `2.4*rp` before final renders;
   post-fix edge gradient at the old boundary is at the noise floor
   (~3.5 LSB).
3. **STACKED TEMPLATE BANDS** — replaced by the valley-fog depth
   function plus per-plane aerial perspective; far peaks pass through
   the cloud banks.
4. **PLANET LIGHTING vs SCENE SUN** — one sun vector
   (approximately (-450,-750,490)) drives terrain shading, the planet
   terminator/limb, the ring lighting, and the halo asymmetry.

### D-IMG-2 (architecture) — tell-by-tell

1. **APEX MITER OVERHANG/LIP** — true closed miter geometry at every
   vertex: the three beam quads meet edge-to-edge along each miter
   bisector (computed from the beam direction pair, `ml = hw/sin(θ/2)`).
   No inner-edge extension, no overhang lip. The cyclic impossible
   over/under (b2 over b0 at V0, b0 over b1 at V1, b1 over b2 at V2) is
   carried by seam shading alone: a highlight lip on the winner's side
   of the miter line, a dark seam plus soft contact shadow on the
   loser's side, plus pocket AO at each inner corner.
2. **BEAM TEXTURE NOT ALIGNED / NO GEOMETRY WEAR / INCONSISTENT
   LIGHTING** — all beam texture is now sampled in beam-local
   (along, across) coordinates: grain elongated along the beam axis,
   scratches and cracks running with the beam, edge-wear chips derived
   from the across-coordinate, joint wear derived from distance to the
   vertices. One common sun and light color across all three beams (warm
   lit side / cool shaded side); no per-beam warm/cool tints.
3. **STARFIELD HARD CUTOFF** — star density/brightness now fades
   continuously into the wall over a 130px band (smoothstep on
   distance-to-walltop); no horizontal branch boundary.
4. **BOTTOM GRAY STRIP** — replaced with a perspective ground plane:
   flagstone/rock slabs in two-point perspective with staggered courses,
   per-slab tone hash, a light pool under the frame, and a real horizon
   with distance haze. The frame casts its contact-hardened shadow onto
   it.

### Round-3 measurements (final, 2026-09-22)

| Subject | File | Size | grad(O) | grad(B) | Ratio | D-RES | D-SHARP | D-COMP | D-DET |
|---|---|---|---|---|---|---|---|---|---|
| D-IMG-1 alien | `d-img-1_alien_1024.bmp` | 1024×1024 24-bit | 8.323 | 3.744 | 2.223 | PASS | PASS | PASS | PASS |
| D-IMG-2 arch  | `d-img-2_arch_1024.bmp`  | 1024×1024 24-bit | 2.290 | 0.963 | 2.377 | PASS | PASS | PASS | PASS |

Sharpness bar: `grad(output) ≥ 1.20 × grad(downscale-by-2 then box-upscale-by-2)`.
Both exceed it at ~2.2–2.4×.

Determinism (two separate clean processes, final binary, 2026-09-22):
- alien BMP: `176dad31…a2bf0e7` both runs — byte-identical.
- arch BMP: `a48d9b40…0ebaea54` both runs — byte-identical.

Render time (1024², lab VM): alien ~6 s, arch ~4–5 s.

### Round-3 artifact SHA-256

| File | SHA-256 |
|---|---|
| `d-img-1_alien_1024.bmp` | `176dad3132560caeb4e1d9e5ce69ae51615fed7fe5d05c63cd689c300a2bf0e7` |
| `d-img-1_alien_1024.png` | `3ec97ff4031ebea4f6fb6bb4a1979ae1fe4aa3a3920d068aecbe647bbb6d341e` |
| `d-img-2_arch_1024.bmp`  | `a48d9b4048a1d42ef54a59b8bbe929f7ce5026d1e7c562264a1275950ebaea54` |
| `d-img-2_arch_1024.png`  | `76f119a052c8823b6efbf424bdd62f238efdb9af81e9ada052c94c35e729a7d3` |
| `disc.zag` | `a5cabe01931cba8bd95dcb1672e5decc311294b760d5458610a0524cf26fb120` |
| `verify_bars.py` | `a413f6b8537aa46335b5bb829d26326f6c4c91001c488ebd70840de49d11c18f` |

(`verify_bars.py` unchanged since round 2; SHA matches the round-2 record.)

### Round-3 honest limitations

- D-BLIND (fresh blind judging) is explicitly out of scope for this crew
  and is not claimed — only the 8 listed tells were addressed
  structurally, and only a separate blind crew can confirm they read as
  closed.
- The ring system is an analytic tilted annulus (2D ellipse
  approximation), not a full 3D ring-plane solve; it reads as a ring
  system but a judge may still see "ellipse layers."
- The planet's bands are concentric latitude rings; the lava field in
  the near plane is a cellular speckle rather than flowing channels.
- 2048² remains untested (prereg minimum is 1024²; buffer ≈ 12.6 MB
  < 32 MiB limit, pipeline supports it).
- The architecture scene uses `f64` for beam geometry (deterministic on
  x86-64); all texture noise remains integer-hash based.
- `disc` binary, `.zagd`/`.zag-cache` files, and debug renders are build
  artifacts and are excluded from the commit.
