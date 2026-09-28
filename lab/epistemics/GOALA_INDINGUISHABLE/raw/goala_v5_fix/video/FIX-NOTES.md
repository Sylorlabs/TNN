# Goal-A video fix crew — FIX-NOTES.md

Working copy: `~/workspace/tnn-lab/` (not a git checkout; do not run git there).
Source: `imagination/src/field.zag`. Toolchain: `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Nothing committed; coordinator commits. Generation is pure Zag; Python is
measurement-only (`video/vidtool.py`, `video/vidmetrics.py`). No RNG anywhere;
two clean renders are byte-identical (see `video/sha256sums.txt`).
Kept 480x480, 36 frames, 12 fps, 44.1 kHz and the existing `f3_video_audio`.
Legacy `f3_emit_avi` untouched; only the G-video path changed. Normal vision throughout.

## What was wrong (the three tells)

The shipped G-video had animated static: no persistent subject, no motion
profile, no shot structure. Fixed by adding a subject system to the G-video
path (`f3_vidsubject_g`, called in the frame loop where `f3_vidfield_g` was).

## The fix (all in `imagination/src/field.zag`)

New code, inserted just before `f3_emit_avi_g`:
- `f3_ease_v1` / `f3_ease_v2`: closed-form integer ease curves (deterministic).
- Bird (v1 glacier sunrise): `f3_bird_sx` / `f3_bird_sy` (position), `f3_draw_bird`
  (flapping wings ±345x145 down / ±355x-190 up on an 8-frame triangle, body/head/
  tail/beak, landing wing-fold), `f3_bird_scene` (foreground ice ridge the bird
  passes behind, dawn glow coupled to bird position, far landing ridge).
  Position-triggered events: swoop dip for s in 700..900, landing descent for
  s>900, tone darkening 90->30 as the bird crosses the brightening sky.
- Boat (v2 harbor night): `f3_boat_bx` (position), `f3_boat_scene` (hull, cabin,
  warm window, mast lamp + halo, deck-light strip, speed-coupled wake length and
  lamp brightness, following reflection, bow pitch with speed, bob/roll
  articulation, foreground pilings the boat passes behind). Position-triggered
  event: hesitation (speed dip) when |bx-535|<130.
- `f3_vidsubject_g`: draws background via `f3_vidfield_g`, then the subject.
- Frame loop grain: `f3_raster_g(..., 7, 12)` — temporal grain seed FROZEN to a
  constant (was `fr`), so frame-to-frame change is spatially coherent
  subject/scene motion, not whole-frame shimmer (V-T5). The static grain
  component is untouched; the video keeps its filmic texture.

## Design iterations (evidence-driven)

1. First bird was small/dark and vanished against the dawn in early frames
   (exact-background mask near zero). Enlarged wings/body ~40% and gave the bird
   a position-triggered tone ramp (light gray-blue early -> silhouette late).
2. First ice ridge read as a bright dominant band; redesigned as a dark dawn
   mass with a warm rim so the bird stays the subject.
3. Boat was small with an invisible dark hull; scaled up ~20% and added a
   deck-light strip. Silhouette 11-19%, reads clearly.
4. Template-attack methodology hardened twice: (a) a bg-morph "floor"
   comparison was tried and dropped — dawn morph drift dominates it, making it
   meaningless; (b) replaced by a self-shift sanity check (frame vs itself
   shifted scores exactly 0.00 at the expected offset), which validates that a
   rigid template would score ~0; (c) attack now uses per-frame analytic subject
   boxes (the position functions are deterministic and mirrored in the measurer)
   after finding a glow-dominated centroid init could miss the true translation.

## Verification (see `video/metrics.txt` for full numbers)

- Determinism: two full renders byte-identical (v1 `fe0d2fb3…`, v2 `d7aa5f22…`).
- Audio: bit-identical to shipped videos (V-T7 deferred, untouched).
- V-T4: subject present 36/36 frames both videos; bbox 17-48% of frame;
  template-attack mean interior MAD 29.0 (v1) / 40.8 (v2) vs 0.00 rigid floor.
- V-T5: hold 0-5 / accelerate / cruise / hesitate / decelerate / settle 32-35
  beats from position functions; active-phase (6-31) mean abs frame diff 6.60
  (v1) / 3.18 (v2), both >2; inside-vs-outside-bbox diff ratios up to 45x (v2),
  confirming spatially coherent subject-driven change.
- V-T6: establish->move->settle continuous; position-triggered events verified
  (v1 swoop/landing, v2 hesitation + piling occlusion).
- Visual inspection of extracted frames confirmed: bird reads as a bird in
  flight and as a perched bird; boat reads as a lit boat with reflection/wake;
  occlusion beats read correctly.

## Files

- `video/f3gvid1.avi`, `video/f3gvid2.avi` — final renders (also in sha256sums.txt).
- `video/metrics.txt` — consolidated metrics; `video/metrics_v1.txt`,
  `video/metrics_v2.txt` — full per-frame output.
- `video/vidtool.py`, `video/vidmetrics.py` — measurement tools.
- `video/bgonly/` — exact background-only renders (measurement support).
- `video/run1/`, `video/run2/` — the two byte-identical render runs.

## Cleanup done

Temporary measurement artifacts `imagination/src/field_bg.zag` and
`imagination/src/field_bg_bin` were removed after final measurement. The shipped
source change is confined to `imagination/src/field.zag` (G-video path only).
