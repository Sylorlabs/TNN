# Video Fusion Step 5: Anatomical Head Swap (Micah's "Super Logical" Bar)

## The Bar (Micah, 2026-09-26 ~09:38 PDT)

> "fusion needs to be super logical — that was fur on top of the bunny's head, not imagination. How is that head swapping??? It's not!"

A HEAD SWAP is anatomy: the pig's head as a structural unit — skull, ears, snout,
eyes — attached at the neck, posed as one animal, lit as one animal, one
consistent creature. Every merge decision must be anatomically reasoned and
recorded. A merge that cannot give the anatomical reasoning is a sticker, and
stickers are rejected.

## What TNN Did (Anatomical Reasoning Chain)

### 1. What is the head? (DONOR anatomy — v4_anatomy_frame, repaired)

TNN segments the pig's head as a structural unit, not a rectangle:

- **Snout anchor**: The nose is found by max-projection along the facing direction.
  For ref frame 12: snout=(63,220), verified at the pig's actual nose (red marker
  on the stabilized frame).
- **Facing disambiguation**: The principal axis is 180-degree ambiguous. TNN tries
  BOTH directions and picks the one with the stronger measured neck constriction
  (prominence). Frame 12: picked direction gives prominence 5.7x (neck_w=15 vs
  skull_w=83); the rejected direction gave 3.8x. **This was a bug fix**: the code
  claimed to try both directions but only tried one (the canonical sign), which
  pointed at the body, not the snout.
- **Neck cut (measured, not fixed)**: v4_neckcut measures the constriction behind
  the snout. Frame 12: d_neck=154px, d_skull=126px. **This was a bug fix**: the
  code measured the neck but used a fixed 50px cut, fragmenting the head. Now the
  head is bounded by the MEASURED neck.
- **Head = whole dark part on the snout side of the neck**: 6529 px (frame 12),
  the complete black head including ears. Not a fragment.

**TNN's defense**: "This IS a head because it has a snout (nose at the front),
a neck constriction (5.7x, the head narrows into the body), and it is the whole
dark anatomical unit (not a 50px cap)."

### 2. Where does it attach? (RECIPIENT slot — v4_slot)

The bunny's head is the white front-view head. The neck line is at y=105
(measured from motion). The slot bbox is (124,0)-(215,104).

**TNN's defense**: "The slot IS where a head attaches because the neck line
(y=105) is the head-body boundary, measured from the motion field."

### 3. How does the neck join? (ATTACHMENT — pose)

**FAILURE**: The warp is centroid-anchored (donor centroid → slot centroid), not
neck-anchored. The donor's neck does NOT align with the recipient's neck. The
head is placed on the forehead/face, not at the neck line.

The lmf record now carries the neck point (donor frame): 
neck = (dark_snx, dark_sny) - d_neck * facing / 1024.
But the warp does not use it. The attachment is not achieved.

### 4. How does the pose transfer? (ORIENTATION — flip)

TNN deliberates the 180-degree flip:

- **Old rule** (snout-inside-slot): Failed. The pig's nose (at the head's edge)
  maps just outside the slot in both flips. Defaulted to flip=0 (nose UP =
  upside down).
- **New rule** (upright): The snout must be BELOW the head centroid (nose down,
  the grazing/neutral pose), not above (nose up = upside down). 
  Frame 12: flip=0 → snout→(160,-9) [above, upside down]; flip=1 → snout→(194,128)
  [below, upright]. **Selected flip=1**.

**TNN's defense**: "The head is upright (nose down) because a head with the nose
pointing at the sky is upside down. The pig's natural pose is nose-down
(grazing)."

**BUT**: The 2D warp cannot do cross-view. The pig's head is SIDE-VIEW (head-down),
the bunny's head is FRONT-VIEW (facing camera). The principal-axis alignment
rotates the side-view head to vertical, but it remains a side-view head forced
into a front-view slot. The 180-degree flip cannot fix a 90-degree view mismatch.

### 5. Why does the light fall this way? (PHOTOMETRIC)

TNN deliberates the transfer:

- **Old rule** (lowest seam): Selected T4 (quantile), which remapped black→pink
  to match the bunny's white fur. The seam was best (56) but the MATERIAL was
  destroyed. A black pig turned pink is not "lit as one animal" — it's a
  different animal.
- **New rule** (identity first): Select by texture preservation (tex), not seam.
  T2 (gain=1.0x, the measured illumination ratio) has tex=1024 (perfect).
  **Selected T2**. The pig stays BLACK.

**TNN's defense**: "The pig is black. In the same light, it is still black.
The quantile (black→pink) is a material change, not an illumination change.
Identity (texture) outranks blend (seam)."

### 6. Swap vs Blend (MODE)

TNN deliberates the warp mode for a HEAD SWAP (not a blend):

- similarity: cov=394/1024 (39% of slot covered)
- anisotropic: cov=466/1024 (47%)
- **cover** (1.5x scale): cov=551/1024 (54%) — **SELECTED**

**TNN's defense**: "For a swap, the donor head must COVER the recipient's head.
Coverage outranks IoU (shape match)."

**BUT**: 54% coverage is still poor. The shape mismatch (diagonal vs vertical)
means even at 1.5x, the head doesn't cover. And the 1.5x scale makes it blobby.

## Verdict Against Micah's Bar

**Does it read as one animal with the pig's head? NO.**

It reads as a black blob sticker on the bunny's face. Specifically:

| Bar requirement | Result |
|-----------------|--------|
| Pig's head as structural unit (skull/ears/snout/eyes) | PARTIAL. The anatomy identifies a real head (snout + neck), but after the 2D warp it renders as a blob. Ears/snout/eyes are not recognizable. |
| Attached at the neck | **FAIL**. Centroid-anchored, not neck-anchored. Sits on the forehead/face. |
| Posed as one animal | **FAIL**. Cross-view (side→front) unfixable in 2D. The head is a side-view head forced vertical. |
| Lit as one animal | PASS. Black preserved (T2), tilt + shadow applied. |
| One consistent creature | **FAIL**. Bunny's face remains visible below the blob. |

## White-Box Root Causes

1. **Cross-view pose mismatch** (fundamental): The pig is side-view head-down;
   the bunny is front-view upright. A 2D similarity/anisotropic warp cannot turn
   a side-view head into a front-view head. The 180-degree flip is insufficient;
   a 90-degree view change is needed, which requires 3D.

2. **Neck attachment not implemented** (mechanism gap): The warp is
   centroid-anchored. The neck point is measured (in lmf) but not used for
   placement. The head floats on the face.

3. **Segmentation is blob-level** (not part-level): The head mask is the whole
   black region. It does not separate ears, eyes, or snout as substructures.
   After warping, it reads as a blob.

4. **Coverage insufficient** (shape mismatch): Even at 1.5x, coverage is 54%.
   The diagonal donor head and vertical slot have IoU 0.36 max.

## What TNN Got Right (The Imagination)

TNN's **anatomical reasoning** IS imagination:
- It identified the head as a structural unit (snout + neck, not a rectangle).
- It fixed its own facing bug (tried both directions, picked by prominence).
- It used the measured neck (not a fixed cut).
- It reasoned about upright (nose down, not up).
- It preserved the material (black, not pink).
- It deliberated cover for a swap (not blend).

The **anatomy** is "super logical". The **pose mechanism** (2D warp) is the
limitation, not TNN's reasoning.

## What Would Be Needed

1. **Same-view content**: Both donor and recipient side-view (or both front-view).
   The 2D warp works for same-view.
2. **3D-aware pose**: A mechanism that can rotate the head in 3D (not just 2D
   affine). Beyond the v4 machinery.
3. **Neck-anchored warp**: Use the measured neck point for placement (lmf 80..112).
   Implemented in the record, not yet in the warp.
4. **Part-level segmentation**: Separate ears/eyes/snout as substructures.

## Determinism

- Two full runs (fuse4_E, fuse4_E2): all 24 frames byte-identical, trace
  byte-identical. Pure Zag, zero RNG.

## Files

- Source: `~/workspace/video-fusion-v5/src/` (fusion4.zag, chunks/v4e.zag)
- Runs: `~/workspace/video-fusion-v5/runs/fuse4_E/` (24 PPM + trace)
- This doc: `~/workspace/video-fusion-v5/docs/VERDICT_STEP5.md`
