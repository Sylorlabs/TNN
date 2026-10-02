# D-VID-1 V2 implementation addendum (frozen before coding)

Wave: wave-20260924-0521pdt. Worker: D-VID-1 V2 (video lane).
Frozen: 2026-09-24 06:10 PDT. Status: ADDENDUM ONLY. No V2 generator,
verifier, or frame artifact exists yet. This addendum is committed
before any `.zag` implementation file. It binds the items the frozen
prereg
(`docs/lab/rsi/runs/wave-20260924-0521pdt/preregs/PREREG_DVID1_V2_0521.md`,
commit 840d54e6c)
requires bound before coding. It does not change the mechanism, the
metric definitions, or any kill bar.

## 1. Exact algebraic inverse of the frozen sampling transform

Frozen forward transform (generator, per pixel at world position
`(wx, wz)`, frame `f`; `rot`, `vwx`, `vwz` from the frozen `o_scene`):

```
mrad = rot * 6283 / 4000,  with rot = 8 * f
(cph, sph) = o_cos_sin(mrad):
    cph = 1000 - mrad*mrad / 2000000
    sph = mrad - mrad*mrad*mrad / 6000000000
rdx = wx - vwx
rdz = wz - vwz
qx = (rdx * cph - rdz * sph) / 1000
qz = (rdz * cph + rdx * sph) / 1000
inw = 1000 - f * 2
cx = qx * inw / 1000 + vwx
cz = qz * inw / 1000 + vwz
```

`(qx, qz)` are the rotating-frame coordinates of the pixel. The noise
is sampled at `(cx * 400, cz * 400)` (bup, seed 51), `(cx * 70,
cz * 70)` (sbup, seed 54), `(cx * 70, cz * 70)` (abup, seed 52).

Frozen inverse (verifier, per rotating-frame cell center `(qx, qz)`,
frame `f`; `mrad`, `(cph, sph)`, `(vwx, vwz, rot)` recomputed from the
same frozen formulas, no independent constants):

```
rdx = (qx * cph + qz * sph) / 1000
rdz = (qz * cph - qx * sph) / 1000
wx = vwx + rdx
wz = vwz + rdz
```

Screen projection (same as the marcher): `x = 512 + wx * 920 / wz`
(from `wx = (x - 512) * wz / 920`), `h = o_height(wx, wz, f, vwx,
vwz, rot, ...)`, `y = o_sy_fp(h, wz) / 32`. Nearest pixel; the
cell's mask state is the foam mask at that pixel.

Identity proof (exact algebra, integer rounding aside). Substitute
the inverse into the forward:

```
qx' = (rdx*cph - rdz*sph)/1000
    = ((qx*cph + qz*sph)*cph - (qz*cph - qx*sph)*sph) / 1000000
    = (qx*(cph^2 + sph^2) + qz*sph*cph - qz*cph*sph) / 1000000
    = qx * (cph^2 + sph^2) / 1000000
qz' = (rdz*cph + rdx*sph)/1000
    = ((qz*cph - qx*sph)*cph + (qx*cph + qz*sph)*sph) / 1000000
    = (qz*(cph^2 + sph^2) + qx*cph*sph - qx*sph*cph) / 1000000
    = qz * (cph^2 + sph^2) / 1000000
```

So `(qx', qz') = (qx, qz)` exactly when `cph^2 + sph^2 = 1000000`.
With the frozen small-angle formulas, `cph^2 + sph^2 = 1000000 - e`
where `e ~= mrad^4 / 3e9 <= 40` at the maximum `mrad = 590`
(`f = 47`). The scale error is at most `160 * 40 / 1000000 = 0.0064`
world units at the disc rim, far below one integer-division rounding
unit. The residual integer round-trip error (a few world units at
most, from the `/1000` divisions) is not assumed away: it is measured
by the trust gate below, which is the point of the gate.

The verifier copies `o_cos_sin`, `o_scene`, `o_height`, `o_sy_fp`,
`o_vn2`, `o_vn3`, `o_atan2`, `o_spire`, `o_isqrt`, `o_ss`,
`o_clamp01k` verbatim from the baseline generator. No independent
constants appear anywhere in the frame transform path.

## 2. Co-rotating cell grid geometry (T1 metric)

- The cell grid is fixed in the rotating frame: cell centers at
  rotating-frame positions `(qx, qz)` with `qx = -158 + 4*i`,
  `qz = -158 + 4*j` for `i, j` in `0..79`, kept iff
  `qx*qx + qz*qz <= 160*160`. This is the frozen 160 world-unit
  influence disc about the vortex center, the same physical radius
  V1 used, fixed in the rotating frame. Cell pitch 4 world units;
  about 5027 cells fall in the disc (exact count printed by the
  verifier).
- Per frame `f`, each cell maps to its screen pixel through the
  inverse transform of section 1 (nearest pixel). Cells mapping
  off-screen (`x` or `y` outside `0..1023`) read mask state 0.
- `T1 = mean over the 47 consecutive pairs of (cells whose mask
  state flips between f and f+1) / (cells masked foam at f)`.
  Baseline and variant are measured by the same verifier code and
  the identical cell grid. Bar (frozen): `T1_variant <= 0.700 *
  T1_baseline`, evaluated in per-mille integer arithmetic as
  `T1v_pm * 1000 <= T1b_pm * 700`.
- Foam mask (frozen, unchanged): pixel counts as foam iff
  `L >= 200` and `(max(R,G,B) - min(R,G,B)) <= 40` with
  `L = (299R + 587G + 114B)/1000`.
- Screen-space T1 (the V1 metric) may be reported as a diagnostic
  with no verdict weight; it can neither pass nor kill.

## 3. Noise-floor cap and rigid-rotation control (metric trust gate)

- The cap is bound as a formula, not a chosen number:
  `cap_pm = T1_baseline_pm * 250 / 1000`, where `T1_baseline_pm`
  is the baseline rotating-frame T1 measured by the frozen
  verifier in the same run. This satisfies `cap <= 0.250 *
  T1_baseline` by construction.
- Rigid-rotation control (pure Zag): the control simulates foam
  that rigidly rotates with the water, i.e. a texture exactly
  stationary in the rotating frame, built only from baseline
  frame f0's foam mask and the frozen formulas. Per frame `f`
  and cell `(qx, qz)`:
  1. `W = C(f) + R(-mrad(f)) * (qx, qz)` (world point the cell
     looks at at frame f; the section 1 inverse).
  2. Round trip back through the forward transform:
     `Q' = R(+mrad(f)) * (W - C(f))` (integer arithmetic; this is
     where remap rounding enters).
  3. `W0 = C(0) + Q'`; `P0` = nearest screen pixel of `W0` at
     frame 0 via `o_height` + `o_sy_fp`.
  4. Control mask state = foam mask of baseline f0 at `P0`.
  `control_pm` = the T1 formula of section 2 evaluated on the
  control masks over the 47 pairs. For an ideal ruler this is 0;
  the measured value is the ruler's quantization noise floor
  under exact rigid rotation (two nearest-pixel remaps, the
  migrating center, and integer round-trip error all included).
- Gate (frozen): the trust gate passes iff `control_pm <=
  cap_pm`. Gate failure voids the T1 measurement: verdict
  UNVERIFIABLE on T1, and return requires a new frozen prereg in
  a later wave. The gate is evaluated before any variant
  comparison is trusted.

## 4. T2, T3, V-RES, V-COMP (unchanged operationalizations)

- T2 (V-TEMP): per-pair mean `|dL|/255` over all pixels,
  `L = (299R + 587G + 114B + 500)/1000`, in units of percent
  x100; bar: every one of the 47 variant pairs in `[50, 1500]`
  (0.5% to 15%).
- T3 (V-SHARP): gradient ratio x1000 exactly as in V1's verifier
  (sum of `|dx| + |dy|` over L divided by the same after 2x2 box
  downscale to 512x512 and box upscale back); validation gate:
  baseline f0/f47 ratios must reproduce the documented
  1.607/1.543 within rounding before any variant comparison is
  trusted; bar: variant within 5% of baseline on f0 and f47.
- V-RES: 48/48 frames readable, BMP magic, 1024x1024, 24-bit,
  3145782 bytes, checked in the verifier from headers.
- V-COMP: grep audit of the variant source for
  filled-primitive placement tokens
  (fill/rect/circle/sprite/blit/place); must be zero, same as
  baseline.

## 5. Compute budget

- Baseline: fresh full 48-frame render of unmodified
  `docs/lab/imagination_discovery/vid/ocean.zag` (pipeline
  reproducibility check against the committed
  `vid/frames/SHA256SUMS`; doubles as the per-frame baseline
  timing). Budget: 5 minutes (V1 measured 91.7 s).
- Variant: full 48-frame render of `ocean_dvid1_v2.zag`.
  Budget: 5 minutes. VKB4 bar: per-frame within 2x baseline.
- Verifier (`v2_verify.zag`): T1 rotating-frame (48 frames x
  ~5027 cells x one `o_height` each, plus the control's second
  pass), T2 (47 pairs x 2 dirs x 1M pixels), T3, V-RES, and the
  screen-space T1 diagnostic. Budget: 15 minutes.
- VKB1: full clean 48-frame variant rerun + pure-Zag sha256 per
  frame, compared against the frozen V2 manifest frame by frame.
  Budget: 10 minutes.
- Total implementation-wave compute budget: 30 minutes wall.
- Pinned compiler: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (sha256 recorded in the evidence). Zero RNG anywhere
  (grep-verified: no rand/random/srand/time/clock tokens). No
  slice over 2^25 bytes (frame buffer 3145782 bytes). Pure Zag
  only; no Python touches any new wave artifact.

## 6. Red-team confounds: how each is attacked this wave

1. Remap quantization floor: attacked by the trust gate
   (section 3). If the gate fails, T1 is UNVERIFIABLE, not
   passed.
2. Inverse-transform identity: attacked by the section 1
   derivation (exact algebraic inverse, no independent
   constants) plus pipeline check P4 (variant f0 byte-identical
   to baseline f0: at f=0, mrad=0, cph=1000, sph=0, inw=1000,
   so cx=wx and cz=wz exactly, and all three breakup terms
   sample at the baseline coordinates).
3. Metric gaming by freezing: attacked by T2's 0.5% lower
   bound, VKB3 tell 2 (no frozen-overlay read), and VKB6
   together. A frozen texture passes T1_rot but fails T2 and
   the eye.
4. Inward-drift mismatch: the bar compares variant to baseline
   under the same rotating frame, so frame misalignment hurts
   the variant, not the ruler. P1 bets the analytic inw law is
   close; VKB6 arbitrates the visual claim.
5. Spire-ring coupling: ringf multiplies bupm (now co-rotating);
   VKB3 tell 4 (rings stay attached, no detach, no pulse) is
   the judge, on the frame sequence.
6. Region asymmetry: the verifier uses the identical disc,
   cell grid, and code path for baseline, variant, and
   control; the grid is built once and reused.

## 7. What the addendum does not change

The mechanism (frozen co-rotating block, sign convention, scales
400/70, seeds 51/54/52, inw law, streak ridge and spire-ring terms
untouched), the metric definitions (T1 rotating-frame boil, trust
gate form, T2, T3), the kill bars VKB1-VKB7, and the verdict rule
are exactly as frozen in the prereg. The open questions listed in
the prereg are closed by sections 1-5 above.
