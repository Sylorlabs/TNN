# Fable's Design Opinion — Fork B Integration Analysis (2026-09-26)

## Status
OPINION, not evidence. Used as design input for TNN-native discovery, not as verdict.
Source: `~/workspace/fusion_fable/summary.md` (Fable consultation, 2026-09-26).

## Fable's Core Claim
The missing representation is **ARTICULATED PART POSE**. The line has been
"solving a 3D visibility problem with a 2D lookup table."

## Fable's Sketch (Summary)
1. **Parts**: 2.5D articulated skeleton (torso bone + head bone); yaw/pitch from
   closed-form landmark geometry, e.g. `tan(yaw) = snout_offset / half_width`.
2. **Head**: Reference image + fixed landmark set + landmark-parameterized warp +
   3D offsets on half-ellipsoid from frontal frame.
3. **Attachment**: Neck as 4-constraint interface (position, orientation, scale,
   C1 silhouette continuity). Cross-fade subordinate to geometric attachment.
4. **Pose transfer**: SELECT yaw-matched pig frame from tracked footage
   ("choosing the right source material is the foundational operation of
   imagination"); fallback to projection-driven warp only within ~15°.
5. **Lighting**: Gain ramp from estimated scene light direction
   (`B_target(φ)/B_source(φ)`), plus per-channel white-point.
6. **Coherence**: Five automated checks (silhouette C1, light-direction <15°,
   color-histogram distance, texture-frequency continuity, attachment residuals).

## Where It Applies to Fork B

| Fable Element | Fork B Applicability | Notes |
|---------------|---------------------|-------|
| Neck as 4-constraint interface | **APPLIES** | My K3 is a point. Fable's position/orientation/scale/silhouette constraints are implementable and would improve attachment. Not yet implemented. |
| Yaw from landmark geometry | **APPLIES** | Donor has measurable facing vector (-388,946). Could compute yaw via `atan2`. Not yet implemented. |
| Coherence checks (5) | **PARTIALLY APPLIES** | I have seam_crisp (≈check #1). Lack light-direction, histogram, texture-frequency, attachment residuals. Implementable. |
| Lighting gain ramp | **APPLIES** | My harmonize is crude global gain. Fable's spatially-varying ramp is more principled. Not yet implemented. |
| 2.5D skeleton | **DEGRADED** | Without multi-view donor, the 3D offsets cannot be built. Collapses to 2D. |

## Where It Does NOT Apply (Critical)

### Frame Selection: UNAVAILABLE
Fable's "foundational operation of imagination" — **SELECTING a yaw-matched
frame** — is **UNAVAILABLE** to Fork B.

**Reason**: The donor (pig) is head-down in ALL 24 frames. There is ZERO yaw
variation in the source material. Fable's preferred method (lookup, not warp)
cannot be performed. Fable's fallback (warp within ~15° of available footage)
also fails: there is no donor frame within 15° of the target (front-view bunny).

**This is not an implementation failure. It is a limitation of the INPUT PAIR.**

### The Smoking Gun Test Fails
Fable: "The system must use a DIFFERENT pig frame for a 0°-yaw bunny vs a
45°-yaw bunny. If both composites use the same pig image, it's still pasting."

Fork B uses the SAME pig head (frame 12) for all renders because there is no
alternative. **By Fable's own criterion, Fork B is still pasting.**

### 3D Landmark Warp: UNAVAILABLE
The half-ellipsoid 3D offsets require a frontal reference frame to estimate
landmark depths. The donor has no frontal frame. The 2.5D skeleton cannot be
constructed.

## The Finding

**Fable's architecture requires source material with pose variation. The
(head-down pig, front-view bunny) pair does not contain the source material
for a head swap.**

This unavailability is itself a finding about what the pair can yield:
- A head swap is **impossible** by Fable's own criteria (needs yaw-matched frame; none exists).
- The warp fallback is **insufficient** by Fable's diagnosis (2D warp cannot synthesize newly-visible surfaces).
- The honest outputs are: (a) decline the head swap, or (b) scene composition (two animals, honestly labeled).

**TNN cannot imagine what it has never seen — or rather, it can only warp,
not select. When selection is the "foundational operation," the absence of
selectable material is a hard ceiling, not a bug to fix.**

## Design Input Taken
1. **Neck constraints**: Will implement Fable's 4-constraint interface (position,
   orientation, scale, silhouette) as an upgrade to K3 point-anchor.
2. **Coherence checks**: Will implement the 5 automated checks as TNN-native
   perception (no human in loop).
3. **Yaw estimation**: Will add `atan2`-based yaw from landmark geometry for
   both donor and recipient, to quantify the pose mismatch explicitly.

## Design Input Rejected (With Reason)
1. **Frame selection**: Cannot implement; no yaw variation in donor. Not a
   choice — a constraint.
2. **3D half-ellipsoid warp**: Cannot implement; no frontal reference. Would be
   fabrication, not estimation.
3. **"Minimal next step" (`pose_pig_head_to_bunny`)**: Step 2 (scan for matching
   yaw frame) is impossible. The function cannot be built as specified.

## Conclusion
Fable's diagnosis (3D visibility problem, 2D lookup table) is correct and
applies to Fork B. Fable's architecture is sound but **requires inputs that
Fork B does not have**. The gap between the sketch and the constraints is not
bridgeable by implementation effort — it is a property of the data.

The TNN-native discovery must therefore be: **given that the foundational
operation is unavailable, what is the honest architecture?** The answer (from
H1d): decline the fabrication, or compose honestly.
