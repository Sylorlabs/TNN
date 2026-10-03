# PATH_MECHANICS — video generation, native

**Scope:** the two native video paths — `imagination_discovery/vid/ocean.zag`
(D-VID-1, plus the round-4 variants in `r4/src/ocean_*.zag`) and the field
imagination AVI emitters in `imagination/src/field.zag`. Zero RNG in all of
them (deterministic integer-hash noise: `o_hash2`/`o_hash3`, `f3_hash2`).

## The short version

**Video is PAR at frame granularity and stateful-sequential within a frame.**
Every frame is a pure function `frame = F(plan, f)` with zero carried state
between frames. The emitted pixel bytes are never read back as generation
input. The "plan" is scene constants + the frame index. Temporal coherence is
plan-sourced (advected coordinates, keyframe interpolation), never
state-sourced.

## Path 1: ocean (D-VID-1) — `imagination_discovery/vid/ocean.zag`

Core loop, `main()` (`ocean.zag:871`):

```
let f:i64 = 0;
while (f < 48) {
    rc = o_emit_frame(f, dir, bmp, 0);   // ocean.zag:885
    ...
    f = f + 1;
}
```

`o_emit_frame(f, dir, bmp, dbg)` (`ocean.zag:650`):

1. **Scene parameters from the frame index only** — `o_scene(f, &vwx, &vwz, &rot)`
   (`ocean.zag:672`; fn at `ocean.zag:234-238`): the vortex center and
   rotation are deterministic hash functions of `f` (`o_vn3(f * 64, …)`),
   rotation is `f * 8`. No other input.
2. **Per-column far→near z-march** (1536 steps, `ocean.zag:675-774`): for each
   of 1024 columns, march inverse-depth steps, evaluate
   `o_height(wx, wz, f, …)` (`ocean.zag:242`). Time enters the heightfield as
   **advected coordinates**: `sx1 = wx - f*12/10`, `sz1 = wz - f*5/10`
   (`ocean.zag:248-249`) — the plan moves the water under a fixed camera.
3. **Per-pixel shading** (`o_shade_water`, `o_shade_rock`, `o_sky`) — pure
   functions of (x, y, world coords, f, material law). Dither is
   `o_hash2(x*3+sy, f+700, 78) % 5 - 2`: deterministic, per-pixel, stateless.
4. **Writes are overwrite-only.** Pixel bytes are written to `bmp` via
   `bmp[at] = …` and never read back. The same `bmp` buffer is reused across
   frames in `main`, but every frame fully overwrites it (sky fills
   `[0, ytop)`, the marcher covers `[ytop, 1024)` contiguously after the
   round-3 gap fixes — see VID-README bugs #2/#3; V-RES bar: 48/48 files at
   3,145,782 bytes).
5. **Emit**: BMP header filled (`ocean.zag:830-856`), frame written by path
   `dvid1_f<nn>.bmp`, per-frame scratch arenas freed.

### What state is carried, and where it stops

| State | Scope | Reset | Output feedback? |
|---|---|---|---|
| `ybuf` (1-D occlusion buffer, x32 subpixel) | one column | per column | No — occlusion test, not readback |
| `hsc`/`hsp`, `msc`/`msp` (6144-byte arenas, current/previous column heights+materials) | two adjacent columns | per frame (`nio_free` at `ocean.zag:826-830`) | No — finite-difference `dhdx` for normals, like filter memory |
| `lr/lg/lb` (previous marcher step's color) | one column's winning steps | per column | No — Gouraud vertical gradient, plan-derived colors |
| `y0/y1` segment fill | one column | per column | No |
| Spire ray pass `ybuf` reuse | one column | per column | No — occlusion against the same plan-derived buffer |
| `r4` `mg_prev` (`r4/src/ocean_r4.zag:791`) | one column's marcher steps | per column | No — cross-step surface params, within-frame |

**Nothing crosses a frame boundary.** No phase, no momentum, no error
accumulator, no "previous frame" anything. The round-4 mechanism variants
(`ocean_Ma.zag` … `ocean_Mh.zag`) change within-frame shading/geometry; all
keep the `while (f < 48)` driver (`r4/src/ocean_r4.zag:1073`) and the same
no-cross-frame-state property.

### What the "plan" is

Fixed scene constants in the source (sun vector, six spire profiles from
`o_spire(i)`, the material law depth→color / sun-diffuse / fresnel / foam /
fog in `o_shade_water`, vortex rules in `o_scene`/`o_height`) **plus the frame
index `f`**. That is the complete input to a frame. There is no separate
plan file, no event list — the plan is authored constants and one integer.

## Path 2: field AVI — `imagination/src/field.zag`

Two emitters: `f3_emit_avi` (`field.zag:1481`, 240×240 × 24 frames @ 8 fps)
and `f3_emit_avi_g` (`field.zag:1848`, 480×480 × 36 frames @ 12 fps, the
"g-series" with organic per-cell transition timing).

Per frame `fr` (`f3_emit_avi`, `field.zag:1654-1700`):

```
f3_vidfield(v, fr, far);        // field.zag:1411 — interpolate 4 keyframes at position fr
f3_raster_visual(far, px, W, H); // field.zag:1233 — bilinear upscale 24x24 field -> pixels
// copy px rows into the AVI movi chunk (container assembly, not generation)
```

- `f3_vidfield(v, fr, far)` (`field.zag:1411-1437`): keyframes
  `a = fr/8`, `b = a+1` from `f3_video_key(v, k, …)` (`field.zag:2167` —
  **the plan**: four authored keyframes built from `f3_vgrad`/`f3_blotch`/
  `f3_rect`/`f3_dither` primitives, e.g. v=1 "glacier sunrise", v=2 "city of
  bells at night"); per-cell interpolation
  `va + (vb - va) * t8 / 8`. G-series (`f3_vidfield_g`, `field.zag:1447`)
  adds per-cell lead/lag `f3_hash2(x, y, 4242) % 5 - 2` — still a pure
  function of `(v, fr, NF)`.
- `f3_raster_visual` (`field.zag:1233-1262`): reads only the `far` field,
  writes `px` overwrite-only. **No pixel readback.**
- Audio is interleaved plan-pure: `f3_video_audio` imagines a soundtrack,
  `apf = total / NF` samples per frame — a plan-derived interleave, not a
  measurement.
- Subjects (`f3_vidsubject_g`, `field.zag:1841`): `f3_bird_scene(far, fr, NF)`
  / `f3_boat_scene(far, fr, NF)` — again pure functions of `(v, fr, NF)`.

### What the "plan" is

The four authored keyframes plus the frame index. Temporal coherence is
**keyframe interpolation** — plan-sourced by construction: endpoints land
exactly on key 0 and key 3, midpoints are deterministic blends.

## Where output bytes could in principle be read back

They can't, and don't — in generation. The complete inventory of byte reads
in both paths:

1. **Occlusion/normal scratch reads** (`hsp`, `ybuf`, `mg_prev`): read
   *scratch state*, never emitted pixel bytes. Analogous to audio's phase
   accumulators / filter memory — carried state, not feedback.
2. **Container assembly copies** (BMP header fill; AVI `px` → `movi` chunk
   copy): read emitted bytes to place them in a file container. This is
   bookkeeping (the survey's "additive accumulation does not count" clause);
   removing it changes nothing about any later computation.
3. **Verifier reads** (`verify_vid.py`, V-RES/V-SHARP/V-TEMP): post-hoc
   judging, outside the generator.

There is **no read of rendered output feeding any synthesis decision** in
either native video path. Video is the path that comes closest to the
constructed PAR extreme: the frame is `F(plan, f)` with less carried state
than even PAR-audio's block rendering needed.

## Video's temporal model, stated once

Audio's stateful-sequential renderers carry phase/filter state *across time*,
so temporal continuity is state-sourced. Video carries **nothing** across
time: continuity is authored into the plan (advected coordinates in ocean,
keyframe interpolation in field-AVI). Consequences:

- Recurrence is 1.0 by construction: re-rendering frame `f` yields
  byte-identical bytes (V-DET: clean rerun → 48/48 frames byte-identical,
  manifest `400ae5c6…938b26ac9` — VID-README).
- There is no "settling", no warm-up, no long-range memory to protect or to
  exploit. A frame has no past and no future inside the renderer.
