# Step 5 Debug: From Sticker to Anatomical Reasoning

## The Two-Direction Facing Bug

**Symptom**: The donor "head" was a 3116 px fragment (50px cap near a wrong "snout").

**Root cause**: `v4_anatomy_frame` claimed to "try both axis directions" but only
tried the canonical eigenvector sign. For the pig (head left, body right), the
canonical sign (vx>0) pointed RIGHT (toward the body), not LEFT (toward the snout).

Consequences:
- "Snout" = max projection toward the body = (132,79), in the middle of the head,
  not the nose.
- "Neck cut" measured from the wrong snout: d_neck=66, prominence 3.8x.
- "Head" = dark pixels within FIXED 50px behind the wrong snout = fragment.

**Fix**: Try both (ux,uy) and (-ux,-uy). For each: find snout, measure neckcut.
Pick the direction with higher neck prominence. If neither has a neck (rc=1),
the frame is invalid (a head without a neck cannot be defended).

Result (frame 12):
- Picked: snout=(63,220) [the actual nose], d_neck=154, prominence=5.7x.
- Head: 6529 px (whole black head, 2.1x bigger).
- Rejected: snout=(132,79), d_neck=66, prominence=3.8x.

## The Fixed-50px Cut Bug

**Symptom**: Even with the correct snout, the head would be fragmented.

**Root cause**: `v4_head_region` was called with `d_cut=50` (hardcoded), ignoring
the measured `d_neck` from `v4_neckcut`. The neck was measured but not used.

**Fix**: Pass `best_dneck` (the measured cut) to `v4_head_region`. The head is
now "dark pixels on the snout side of the MEASURED neck constriction".

## The Upside-Down Flip Bug

**Symptom**: The graft had the pig's nose pointing UP (flip=0).

**Root cause**: The flip test ("snout-inside-slot") failed because the pig's nose
(at the head's edge) maps just outside the slot in BOTH flips (in0=0, in1=0).
Defaulted to flip=0, which put the nose up.

**Fix**: New rule — "upright": the snout must be BELOW the head centroid
(nose down = grazing/neutral; nose up = upside down). 
- flip=0: snout→(160,-9), above center (59) → upside down. REJECT.
- flip=1: snout→(194,128), below center → upright. SELECT.

## The Pink Pig Bug (Photometric)

**Symptom**: The black pig's head rendered PINK.

**Root cause**: The transfer selection picked the lowest SEAM among gate-passers.
T4 (quantile) had seam=56 (best) but tex=722 (barely passing). The quantile
remapped the donor's dark values to the slot's bright values (black→pink),
destroying the material. The gates (tex≥717) were too lax to catch it.

**Fix**: Selection by TEXTURE (identity), not seam. T2 (gain=1.0x) has tex=1024
(perfect). The pig stays black. Rationale: "Identity outranks blend. A low seam
bought by remapping the material is a different animal."

## The Cover Mode (Swap vs Blend)

**Change**: Added md=2 ("cover"): 1.5x the similarity scale. Selected by
COVERAGE (fraction of slot mask covered), not IoU.

- similarity: cov=394/1024
- anisotropic: cov=466/1024  
- cover: cov=551/1024 → SELECTED

**Rationale**: For a HEAD SWAP (replace), the donor must COVER the recipient.
For a BLEND, IoU (shape match) matters. Micah's bar is a swap, so coverage.

**Limitation**: 54% coverage is still poor (shape mismatch). The 1.5x scale
makes it blobby. The canvas was expanded from +8 to +32 to avoid clipping.

## Landmark Record Extension

The lmf record (16 qwords) now carries:
- 80: d_neck (px, measured)
- 88,96: facing (x1024, picked direction)
- 104,112: dark snout (px, for neck point computation)

Neck point (donor frame) = (104,112) - 80*(88,96)/1024.
**Not yet used** by the warp (centroid-anchored). Future work: neck-anchored warp.
