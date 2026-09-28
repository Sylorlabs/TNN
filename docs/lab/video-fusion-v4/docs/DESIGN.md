# Video Fusion v4 — Design

## Objective

Attack Step 3's untested territory with the same instruction ("merge the pig
and the bunny together") and the same sources, achieving:

- Pure Zag, zero RNG.
- Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Identity-preserving nonlinear photometric transfer beyond Step 3's 3× clamp.
- Head-only pig segmentation surviving camera shake, or mechanical no-valid-split proof.
- Pose normalization from measured landmarks in the plan language.
- Live corresponding donor frame on every output frame; never frozen frame 12.
- Exactly 24 frames, 320×240, 8 fps, 3.0 seconds.
- TNN-owned measured propose→evaluate→select reasoning.
- MERGE/SIDE/THEN instruction- and content-sensitive.
- Two byte-identical reruns comparing every frame and trace.
- No indexed `as []i32`; use `[]u8` little-endian arenas.

## Architecture: Fusion Organ v4

The v4 pipeline has five stages, each with TNN-owned measured reasoning:

### 1. STABILIZE (v4a.zag: v4_stable_frame, v4_stable_E, v4_measure_residual)

TNN deliberates its own stabilization:
- Measures per-frame translational drift via block matching on downsampled grayscale.
- Computes cumulative drift path (cum buffer).
- Measures residual (whole-frame difference before/after stabilization).
- Selects stabilization if residual improves.

Measured on pig source: shake_max_px=44, residual_before=24, residual_after=20,
use_stab=1. The stabilization is real (not a no-op).

### 2. ANATOMY (v4a.zag: v4_dw_one, v4_moments, v4_eigenvec, v4_snout, v4_neckcut, v4_head_region)

Per-frame snout-anchored head segmentation:

1. **v4_dw_one**: Extracts largest dark component (pig body) and largest bright
   component (white body reference) via connected components on stabilized frames.
   Uses union-find with path compression. Rejects border-touching components.

2. **v4_moments**: Computes raw moments (n, cx, cy, mxx, mxy, myy) of the dark mask.

3. **v4_eigenvec**: Principal axis via closed-form 2×2 eigendecomposition.
   Returns unit vector scaled to 1024.

4. **v4_snout**: Finds snout as max projection of dark mask onto facing direction.
   Tests both axis directions; picks the one with better neck score.

5. **v4_neckcut**: Samples width profile perpendicular to axis from snout backward.
   Finds neck constriction (local width minimum with prominence). Falls back to
   fixed distance if no constriction found.

6. **v4_head_region**: Defines head as dark pixels on snout side of neck cut plane.
   Splits legs via motion energy (Es buffer): high-motion components are legs,
   removed from head. Validates head area (500 < area < dark_area).

The anatomy is **identity-preserving**: it segments the actual pig head from the
actual frame, not a template. The snout, neck, and head are measured, not assumed.

### 3. POSE (v4c.zag: v4_slot, v4_ainv, v4_warp)

- **v4_slot**: Finds recipient slot (bunny head region) via largest subject component.
- **v4_ainv**: Computes affine inverse for pose normalization.
- Proposes similarity vs anisotropic transforms; selects via IoU.
- Vetoes extreme stretch.

### 4. PHOTOMETRIC (v4b.zag: T1-T4 candidates)

Four transfer candidates, TNN selects via measured metrics:
- **T1**: 3× gain clamp (Step 3 baseline).
- **T2**: Illumination gain (bright-reference ratio).
- **T3**: 2× illumination gain.
- **T4**: Quantile remap (nonlinear).

Metrics: texture preservation, chroma shift, seam visibility, clipping, monotonicity.
TNN picks the candidate with best measured tradeoff. This goes beyond Step 3's
fixed 3× clamp by *measuring* which transfer preserves identity.

### 5. RENDER (v4d.zag, v4e.zag: do_fuse4)

- Per-frame donor warping (live corresponding donor frame, never frozen).
- Feathered blending, light tilt, contact shadow.
- Writes 24 PPM frames + trace.

## Instruction Sensitivity

- **MERGE** → FUSE_HEAD plan (score 110).
- **SIDE** → SIDE_BY_SIDE plan (score 20).
- **THEN** → SEQUENCE plan (score 20).

The verb_fit dominates; content refines. Tested via plan selection scores.

## Determinism

- Pure Zag, zero RNG.
- Pinned compiler.
- Two reruns must be byte-identical (frames + trace).

## Status

**BLOCKED**: The anatomy mechanism (v4_anatomy_frame) is implemented and
functional in isolation (returns valid head segmentations without crashing).
However, the full pipeline integration crashes with "slice index out of bounds"
when valid heads are found and stored. The crash is in the caller (v4_merge),
not in the anatomy function itself. See VERDICT.md for the blocker list.
