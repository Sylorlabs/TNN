# Head-Swap Architecture Consultation

## 1. WHY THIS KEEPS COLLAPSING TO STICKERS

The fundamental missing representation is **articulated part pose** — specifically, a model of what a head *is geometrically as a deformable 3D object that can rotate, and what the neck *is as a joint that constrains how that object attaches to a torso.*

Here is the structural reason, stated precisely:

A mask tells you **where** head-pixels are. A warp tells you how to **remap** source pixels into that region. But neither representation contains any information about:

- **The head's viewing angle** relative to the body (is the head facing the camera? turned 30° left? in profile?)
- **The neck as a 3D hinge** — a cylindrical attachment surface that the head pivots around, which has a specific orientation in space relative to the torso
- **How head-surface geometry deforms under rotation** — when a head turns, visible surface area changes, foreshortening occurs, features slide relative to each other non-linearly

The reason no refinement of masks, tracking, or photometry can close the gap: these are all **per-pixel operations operating on a 2D canvas**. They can move pixels, recolor pixels, and mask pixels. But a head swap is not a pixel operation — it is a **structural substitution of a 3D part onto a different 3D skeleton**, viewed through a camera. The pipeline has no representation of the skeleton, no representation of the part's 3D pose, and no representation of the joint between them.

Concretely: when the bunny faces forward and the pig is in profile, the system needs to *rotate the pig head 80° around a vertical axis* so it faces forward on the bunny's body. A 2D warp cannot do this because rotation around a non-image-plane axis **generates and destroys visible surface** — the far side of the pig's head becomes visible, the near side's cheek disappears, the ear changes position non-linearly. No 2D affine or homography can synthesize the pixels that would appear on the "newly visible" side of the rotated head, because those pixels *do not exist in the source image.* A mask+pipeline is trying to solve a 3D visibility problem with a 2D lookup table. That is why it collapses to a sticker every time: it has no choice but to take whatever pig-head pixels exist and stretch them onto the mask shape, which looks like a flat texture because **it is** a flat texture.

The missing representation, named: **a parametric 3D part model with explicit pose (rotation and translation) relative to an articulated skeleton, plus a visibility/rendering step that determines which surface of the part is visible at the solved pose and synthesizes (or fetches) the correct appearance for that viewing angle.**

---

## 2. WHAT A GENUINELY LOGICAL HEAD-SWAP ARCHITECTURE LOOKS LIKE

### 2a. How parts are represented

**The skeleton** is a minimal articulated structure. For the head-swap task, it has exactly two bones:

- **Torso bone**: defined by the bunny footage. Anchored at the neck landmark (bottom of head) and extends downward along the spine/body midline. In 2D, this is a line segment with an orientation (angle from vertical).
- **Head bone**: defined as the extension of the torso bone upward from the neck point, with the head's orientation determined by the vector from neck to snout (or neck to head centroid if snout is occluded).

This is a **2.5D skeleton** — it is defined in image coordinates but carries a crucial 3D quantity: **the viewing angle** (yaw, and optionally pitch) of the body. This angle is estimated from the 2D landmark configuration:

- **Yaw estimation** (is the body facing camera, turned, or in profile): computed from asymmetry of the head's 2D bounding shape. When a head is frontal, its left-right width is maximized and the snout appears centered between the ears. When turned, the width narrows (foreshortening), the snout shifts toward one side, and one ear occludes part of the far side of the head. A deterministic formula: measure the horizontal offset of the snout landmark from the midpoint of the two ear landmarks (or from the head bounding box center). The ratio `(snout_offset / half_width)` is a monotonic function of yaw. Calibrate this with geometry: for a roughly spherical head of radius r at yaw θ, the apparent snout offset is `r·sin(θ)` and the apparent half-width is `r·cos(θ)`, so `tan(θ) = snout_offset / half_width`. This gives a **closed-form yaw estimate** from visible landmarks. Same logic for pitch using vertical snout-to-ear-midpoint offset.

**Each part (head) is represented as:**

- A **reference image** of the pig's head: ideally a near-frontal reference frame extracted from the footage, stored as a pixel image.
- A **landmark set** on that reference image: snout tip, left/right eye, left/right ear tip, chin, left/right jaw edge, top of skull. These are manually or algorithmically placed once on the reference frame and are fixed.
- A **parametric 2D warping model** (not arbitrary warp — a *structured* warp). The reference image is modeled as a **planar or cylindrical surface patch** parameterized by landmark positions. The warp from reference to target is defined by moving each landmark to a target position; the pixel interpolation is a constrained piecewise-affine or thin-plate spline *that respects the landmark correspondences*. This is the same category as Active Shape Models / 2D morphable models, but without the statistical learning — the correspondences are explicit.
- A **yaw parameter** θ that controls the warp: as θ changes, the landmarks move according to the geometric projection of a 3D head surface. Concretely, each landmark has an estimated 3D position on a unit sphere (relative to head center). The reference image corresponds to θ=0 (frontal). For any target yaw θ, each landmark's 2D position is `x' = x·cos(θ) + z·sin(θ)`, `y' = y` (ignoring pitch for now). This is **exactly 10 lines of code** — it is a projection of known 3D offsets through a rotation matrix. The result: you can warp the pig's head to *any yaw angle* by rotating its landmark constellation, and the pixel warp follows. Crucially, this warping **creates and destroys visible surface** in a geometrically correct way: at θ=0, the full frontal face is visible; at θ=60°, the far cheek is partially visible, the near ear is foreshortened, the snout shifts. This is not a 2D stretch — it is a projection-driven landmark warp.

**The 3D landmark positions** on the reference head can be estimated analytically from a single frontal image: ears are on the sides (z ≈ ±r), eyes are above and lateral to snout (z ≈ 0), jaw is below and lateral. A half-ellipsoid approximation (`x²/a² + y²/b² + z²/c² = 1`) with parameters estimated from the frontal-view landmark positions gives the z-coordinates. This is deterministic and requires no learning.

### 2b. How parts attach — the neck joint

The neck is the **attachment interface**, defined as:

- On the **body side** (bunny): a line segment or short curve at the base of the head mask, where the head meets the body. Its orientation is determined by the neck landmarks and the body's torso direction. This is a **contour**: the visible neckline.
- On the **part side** (pig head): the bottom edge of the head model (chin line, jawline). At reference yaw, this is the bottom of the reference image.

**Attachment constraints:**

1. **Positional continuity**: The center of the part's jawline must coincide with the center of the body's neckline. (One positional constraint — fixes translation.)
2. **Orientation continuity**: The part's jawline must be tangent to the body's neckline — i.e., the angle of the jawline at the attachment point must match the angle of the neckline. (One rotational constraint — fixes rotation.)
3. **Scale continuity**: The width of the part's jawline at the attachment must match the width of the neckline. This constrains the scale factor of the head. (One scale constraint.)
4. **Smoothness of silhouette**: At the attachment seam, the silhouette gradient (the direction of the boundary curve) must be continuous — no sharp kink between head outline and body outline. This is a **C¹ continuity constraint** at the join.

These four constraints (position, orientation, scale, silhouette continuity) are **all computable from landmarks** and enforceable by explicit code. They are the geometric definition of "the head is attached to the body, not floating on top of it."

The seam region (a strip of pixels along the neckline) is handled by a **cross-fade with geometric warping**: both the head's jaw edge and the body's neck edge are warped to a common seam curve (defined by the midpoint and interpolated tangent), and a narrow blend zone (5-15 pixels) performs alpha cross-dissolve. But the key point is: the cross-fade is **subordinate to** the geometric attachment. Without the geometric attachment, the cross-fade just blurs a sticker's edge. With it, the cross-fade smooths an already-aligned seam.

### 2c. Pose transfer: side-view pig onto front-view bunny

This is the core technical challenge, and the architecture handles it as follows:

**Step 1: Estimate the target pose (bunny's viewing angle).**
Using the yaw-estimation formula from 2a, compute `θ_target` from the bunny's landmark configuration in the current frame.

**Step 2: Retrieve or synthesize the pig head at `θ_target`.**
This is where the "imagination" happens. The system has a reference pig head at (or near) θ=0. It needs the pig head at θ=`θ_target`.

Two paths, in order of preference:

- **(Preferred) Cross-reference retrieval**: If the pig footage contains *any* frame where the pig's head is at approximately `θ_target`, extract that frame's head. Landmark the pig head in that frame (already done by the tracking system). Use *that* frame as the reference for the current composited frame. This is not cheating — it is the logical equivalent of "finding the right photo of the pig's head from the right angle." The system is choosing *which* of many available pig-head images to use, based on geometric reasoning about viewing angle.

- **(Fallback) Projection-driven warp**: If no pig footage frame matches the target yaw closely enough (within a threshold, e.g., 15°), use the parametric warp from 2a. Rotate the pig-head landmarks by `θ_target`, warp the reference image accordingly. This will be less detailed at extreme angles (the "newly visible" side of the pig's head is synthesized by extrapolation, which will be blurry or imprecise), but it will be *geometrically correct in structure* even if texture detail degrades.

The key insight: **the system is not warping a 2D image to fit a 2D mask shape. It is solving for the correct 3D viewing angle of the pig head, and then generating (or selecting) the pixel content that corresponds to that viewing angle.** The mask is a *consequence* of this process (the silhouette of the head at the solved pose), not the *input* to it.

**Step 3: Orient the head to match the body's pose.**
Once the pig head is at the correct yaw, it must also match the body's **pitch** (tilt forward/back) and **roll** (tilt sideways). These are estimated from the bunny's neck-to-snout vector:

- Pitch: vertical component of the neck-to-snout vector (longer vertical extent when looking down, shorter when looking up).
- Roll: the tilt of the neck-to-snout vector away from vertical.

Apply these as additional rotation parameters in the landmark projection. The code is: apply rotation matrix R_yaw, then R_pitch, then R_roll to the 3D landmark positions, then project to 2D. Three 3×3 matrix multiplications and a perspective divide. Deterministic, closed-form.

### 2d. Lighting unification

Pixel-level photometric transfer (as done in Step 3) is necessary but not sufficient. The reason the sticker looks wrong isn't only geometry — it's that **the lighting model on the head is inconsistent with the scene**. Specifically:

1. **Directional illumination**: The scene has a primary light direction. The pig head, if taken from different footage, has a *different* primary light direction. Photometric transfer tries to globally shift colors, but it cannot re-lit a surface — it cannot change where highlights and shadows fall.

2. **What makes lighting look unified to a human**: (a) consistent shadow direction, (b) consistent highlight position (specular reflections should appear on the same side of curved surfaces), (c) consistent color temperature, (d) consistent contrast/ambient ratio.

**The implementable approach (no full relighting, but geometrically informed):**

- **Estimate scene light direction from the bunny footage**: The shading on the bunny's body provides a light direction cue. Specifically, measure the brightness gradient across the torso (or head, before removal): which side is brighter? This gives a 2D light direction in image space: `L = (Lx, Ly)`. Deterministic: compute average brightness in left half vs right half, top half vs bottom half, of the head/body region. The difference vector is the light direction.

- **Apply a spatially-varying gain map to the pig head**: Instead of global color transfer, apply a **gradient-matched brightness overlay**. Compute the pig head's own shading gradient (which side is bright, which is dark) from the reference. Compute the target shading gradient from the light direction estimate. Apply a **gain ramp** that rotates the pig head's shading to match the target direction. Concretely: for each pixel in the pig head, compute its angle φ relative to the head center. The target brightness should follow `B(φ) = B_base + B_amplitude * cos(φ - φ_light)`, where `φ_light` is the estimated scene light angle. The source pixel's brightness is similarly parameterized. The transform is: multiply each pixel by the ratio `B_target(φ) / B_source(φ)`. This shifts where the highlights and shadows fall *without* inventing texture detail.

- **Color temperature**: Measure average color of the bunny's fur (excluding the head region). Measure average color of the pig head. Apply a per-channel gain so the pig head's white-point matches the bunny's. (One 3×1 vector multiply.)

- **Seam-zone lighting continuity**: In the blend zone along the neckline, interpolate not just alpha but also the lighting gain map, so there is no abrupt brightness change at the seam.

This is not true relighting — it is **shading rotation via gain remapping**. Its ceiling: it works well for diffuse surfaces under a single dominant light, which cartoon characters essentially are. It will fail for complex specular reflections or multi-source lighting. But for Big Buck Bunny (soft cartoon shading, single dominant light), this is well within the necessary quality.

### 2e. Coherence criterion (automated, no human in the loop)

The system needs a self-check that says "this looks like one animal, not two pasted images." Define these measurable criteria:

1. **Silhouette continuity (C¹ check)**: Sample the outline of the composited animal (head + body) at 100 evenly-spaced points. At each point, compute the tangent angle of the outline. The standard deviation of the tangent-angle *derivative* (curvature) along the entire outline should be below a threshold. A sticker produces a curvature spike at the seam; a well-attached head produces smooth curvature. **Metric**: max absolute second-derivative of outline angle across the seam region. **Threshold**: determined empirically, but a sticker will produce values 10-100× higher than a good attachment.

2. **Lighting consistency**: Compute the light direction (as in 2d) independently on the head region and the body region. **Metric**: angular difference between the two light-direction vectors. **Threshold**: < 15° for "consistent."

3. **Color histogram match**: Compute the color histogram of the head region and the body region (excluding overlap). Compute the Earth Mover's Distance (or simpler: chi-squared distance) between the two histograms. **Metric**: histogram distance. **Threshold**: determined empirically, but a well-matched composite will have distance below a threshold that a sticker (with mismatched color temperature) will exceed.

4. **Texture-frequency continuity at seam**: Compute the local spatial frequency (via simple gradient magnitude) in a narrow band on both sides of the seam. The ratio of average frequency on head-side to body-side should be close to 1. A sticker pasted from different-resolution footage will show a frequency discontinuity. **Metric**: ratio of mean gradient magnitude in 5-pixel-wide bands on either side of seam. **Threshold**: ratio between 0.7 and 1.43 (i.e., within 30% of unity).

5. **Geometric attachment check**: Verify that the attachment constraints from 2b are satisfied. **Metric**: (a) distance between jawline center and neckline center (positional error), (b) angle difference between jawline and neckline tangents (angular error), (c) width ratio between jawline and neckline (scale error). **Thresholds**: positional < 3 pixels, angular < 5°, scale ratio between 0.85 and 1.15.

If all five checks pass, the composite is geometrically and photometrically coherent. If any fails, the system can identify *which* aspect is broken and report it. No human needed for the binary classification; the human judge's role is only the final aesthetic evaluation.

---

## 3. THE MINIMAL NEXT STEP THAT ISN'T ANOTHER STICKER

**The smallest architectural change**: implement **yaw-aware head placement** — specifically, add a single new subsystem that takes ~100-200 lines of code.

Here is the exact proposal:

### What to build

A function called `pose_pig_head_to_bunny(bunny_landmarks, pig_reference_landmarks, pig_reference_image)` that does:

1. **Compute target yaw** from bunny landmarks: `θ_target = atan2(snout_offset, half_width)` (from 2a). Deterministic, 3 lines of code.

2. **Find best-matching pig frame** by yaw: iterate through the pig footage's tracked frames. Each frame has a computed pig-head yaw (same formula applied to pig landmarks). Find the frame whose yaw is closest to `θ_target`. Extract that frame's head region using the pig's head mask from tracking. This is a **lookup**, not a warp — no pixel synthesis, no distortion. You are selecting the *correct image of the pig's head from the angle that matches the bunny's body pose.* Deterministic, O(N) scan where N is number of pig frames.

3. **Place the selected pig head using neck-anchored alignment**: Instead of centroid-to-centroid alignment, align the pig head's jawline center to the bunny's neckline center. Orient the pig head so its jawline tangent matches the bunny's neckline tangent. Scale the pig head so its jawline width matches the neckline width. This is three constraints solved by one translation, one rotation, and one scale factor — all computed from landmark positions. ~30 lines of code.

4. **Apply the lighting gain remap** from 2d: compute light direction from bunny body, compute source light direction from pig head, apply gain ramp. ~40 lines of code.

5. **Cross-fade the seam**: blend over a 10-pixel strip along the neckline. ~10 lines of code.

6. **Run the coherence checks** from 2e. Report pass/fail. ~50 lines of code.

**Total: ~150 lines of explicit, deterministic code. Implementable in days.**

### Why this is not another sticker

The critical difference is **step 2**: the system is no longer taking *one* pig head image and warping it to fit a mask shape. It is **selecting a different pig head image based on the geometric relationship between the two animals' poses.** If the bunny faces forward, the system grabs a forward-facing pig head. If the bunny is in 3/4 view, the system grabs a 3/4-view pig head. This is qualitatively different from warping — it is *choosing the right source material*, which is the foundational operation of imagination in this context (reasoning about which view of X is needed to match the context of Y).

If no sufficiently close yaw match exists in the pig footage (e.g., bunny is at 40° yaw but pig footage only has 0° and 70°), the system falls back to the parametric warp from 2a. This fallback *will* look worse, but it will be geometrically structured — not a flat paste.

### Falsifiable pass/fail criteria

**Passes (genuine head swap):**
- The silhouette curvature check (2e.1) shows no spike at the seam — curvature is smooth.
- The lighting consistency check (2e.2) passes — head and body light directions agree within 15°.
- The automated check confirms: the pig head image used was NOT the same yaw as the pig's original reference — it was a *different* pig frame, selected to match the bunny's yaw. This is the smoking gun: if the system is choosing a different source image based on geometric reasoning, it is not pasting.
- Human judge: the head appears to be *facing the same direction as the body* (not at a mismatched angle), the jawline follows the neckline naturally, and there is no visible "edge" where head meets body.

**Fails (still a sticker):**
- Silhouette curvature spike at seam exceeds threshold — the outline has a kink.
- The pig head is at its original reference yaw (0°) regardless of the bunny's yaw — proving the system did not actually re-pose the head.
- The human judge sees a head that is at a *different angle* than the body (e.g., pig looking left while body faces forward) — this proves yaw-aware selection was not applied.
- Color/tone mismatch at seam is visible — lighting remap failed.

**The single most diagnostic test**: render two frames side-by-side. Frame A: bunny at 0° yaw (facing camera). Frame B: bunny at 45° yaw (turned). If the system is working, these two frames should show *different pig head images* — one frontal, one 3/4 — both correctly aligned to the bunny's neckline. If both frames show the same pig head image, the system is still pasting. This is trivially checkable and impossible to fake with a sticker pipeline.

---

**Summary of where I am speculating vs. confident:**

- **Confident**: The diagnosis of why stickers fail (no 3D pose representation, no visibility reasoning) is sound and follows from first principles of geometry.
- **Confident**: The neck-anchored attachment constraints (2b) and the yaw-estimation formula are correct geometry.
- **Confident**: The coherence checks (2e) are implementable and will reliably distinguish stickers from good composites.
- **Confident**: The minimal next step (yaw-aware frame selection + neck-anchored placement) is the right architectural move because it introduces *geometric reasoning about part pose* into the pipeline for the first time.
- **Speculating (mildly)**: The lighting gain remap (2d) will be sufficient for the cartoon aesthetic of Big Buck Bunny. For photorealistic footage, you would need more (environment-map-based relighting, subsurface scattering approximations). But for this specific deliverable, I believe it will cross the quality threshold.
- **Speculating (more)**: The parametric warp fallback (when no yaw-matched pig frame exists) will produce acceptable results at moderate yaw mismatches (<30°). At larger mismatches, it will degrade visibly. The system should detect this and report low confidence rather than producing a poor composite silently.
- **Acknowledging**: This is still a 2.5D solution, not full 3D. Its ceiling is: it cannot handle extreme pose mismatches (e.g., one animal facing directly away from camera while the other faces forward), and it cannot handle significant pitch differences well (the yaw model is the strongest axis). For the Big Buck Bunny task (moderate pose variation, cartoon aesthetic), this ceiling is likely high enough. For a general-purpose head-swap system, full 3D morphable models would eventually be needed — but that is a much larger build, and this step gets you from "sticker" to "structural compositing" with minimal new code.
