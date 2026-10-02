# SOURCE AUDIT

## Scope

White-box audit of the fusion source for H1 (3D/depth/occlusion representation) and the compositor semantics. Conducted 2026-09-26 on the source copies in `src/` (`composer_base.zag`, `fusion4.zag`, `main_tail.zag`).

## H1: Depth / 3D / occlusion references

**Method:** `grep -rin` for `depth`, `3d`, `occlu`, `behind`, `tuck`, `zbuffer`, `z-buffer` across `composer_base.zag`, `fusion4.zag`.

**Results:**

| Pattern | Hits in `fusion4.zag` | Hits in `composer_base.zag` |
|---|---|---|
| `depth` | 0 | 0 (in code) |
| `3d` | 0 | 0 |
| `occlu` | 0 | 0 |
| `behind` | 0 | 2 (trace strings only: `" behind); decisive: "`) |
| `tuck` | 0 | 0 |
| `zbuffer` / `z-buffer` | 0 | 0 |

**The only "behind" references are in human-readable trace strings**, not in geometry or compositing logic. There is **zero** depth, 3D, occlusion, tuck, or z-buffer machinery in the fusion source.

## The lmf contract (anatomy representation)

The `lmf` (landmark) block is 128 bytes = 16×i64, populated in `fusion4.zag` (~line 4899-4924):

| Offset | Content | Dimensionality |
|---|---|---|
| 0 | `hs+72` (aux) | scalar |
| 8 | `hs+0` (head area) | scalar |
| 16, 24 | centroid (dcx, dcy) | 2D |
| 32, 40 | principal eigenvector (udx, udy) | 2D |
| 48, 56 | eigenvalues (lam1, lam2) | scalars |
| 64, 72 | snout (snx, sny) | 2D |
| 80 | d_neck (distance) | scalar |
| 88, 96 | facing vector (fx, fy) | 2D |
| 104, 112 | skull point (dsx, dsy) | 2D |

**Every spatial quantity is 2D.** There is no z-coordinate, no surface normal, no depth map, no occlusion mask. The "facing vector" is a 2D image-plane direction, not a 3D orientation.

## Compositor semantics (`v4_composite`, fusion4.zag:4976)

```zag
fn v4_composite(fr, W, graft, alpha, sx0, sy0, sw, sh, tiltk) void {
    // for each pixel in graft bbox:
    //   if alpha > 0:
    //     gv = graft_pixel * tilt_factor / 1024   (brightness tilt)
    //     fr_pixel = (gv * alpha + fr_pixel * (255 - alpha)) / 255
}
```

**Semantics:** Standard alpha-over compositing. Every graft pixel with `alpha>0` is blended **on top** of the frame. There is:

- **No** depth test (no z-buffer, no per-pixel depth).
- **No** recipient-foreground preservation (the bunny's own head is not kept in front where it should occlude).
- **No** "behind" mask (no region where the graft goes behind the recipient).
- **No** tuck behavior (no folding the neck under the body).
- Only a `v4_shadow` (soft contact shadow below the bbox) and a tilt-based brightness factor — both cosmetic, not structural.

**The compositor is a 2D sticker-paster.** It cannot represent "the head goes behind the body at the neck" because it has no depth ordering.

## Conclusion for H1

The source contains **no** 3D world model, **no** depth representation, **no** occlusion handling, and **no** anatomical tuck/behind logic. The lmf is a flat 2D descriptor. The compositor is alpha-over with no depth. This confirms H1's kill-bar conditions all fail: no consistent 3D tracking, no explicit depth/occlusion, no tuck/behind compositor.

## H2d: znc toolchain (summary)

Full audit in `BUILD_AND_DETERMINISM.md`. Zero `as []i32/u32/u16` casts, no `nio_free` on non-owned pointers, correct `_zag_strcmp` usage, all allocations well under the 2^25 limit. Independent Python recomputation matches Zag exactly. The toolchain is exonerated.
