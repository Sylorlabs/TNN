# PATH B White-Box: Can a Pose-Normalized Part Model Be Earned?

## The question
Build a 3D-ish head model from real observations that the warp can ROTATE
into the recipient's (front) view before grafting. The model must be earned
from what TNN can observe — not a programmer's sculpture.

## What the observations actually contain (measured)

Donor: ingest_pig_A, 24 frames, 320x240, monocular, one continuous 3.0 s shot.

1. **One pose family.** The pig grazes head-down at the fence for the whole
   shot. Per-frame dark-head principal-axis angle swings 3° -> 61°, but this
   is IMAGE-PLANE rotation driven by the pig walking left (centroid moves
   (164,100) -> (108,106)), not head rotation in 3D. The head stays pitched
   down (~70-90° below horizontal) in every frame. No frame shows the head
   upright or the face frontally to the camera.
2. **No depth.** Single fixed camera, no stereo, no motion parallax on the
   head (the head barely moves relative to the camera; frame diffs are
   translation/chewing, mean 28/255).
3. **No second viewpoint.** Same camera, same pig, same 3 s. Nothing in the
   24 frames constrains what the head looks like from the front.

## Why rotation cannot be earned (mechanism-level)

Rotating a 2D head image to a novel 3D view requires, per pixel, a depth
value (or equivalently a 3D surface prior). The observations provide zero
depth constraints: for ANY depth assignment consistent with the silhouette,
there exists a different rotation result. Choosing one (ellipsoid head,
extruded snout, assumed ear planes) is a prior smuggled in by the
programmer — a sculpture, not an observation.

What CAN be earned honestly from these frames:
- in-plane rotation/translation/scale (already done: step-5 warp),
- the silhouette and texture of the head AS SEEN from above-front,
- part locations WITHIN that view (snout tip, ear blobs) — but their
  3D positions relative to each other are unobserved.

None of these bridge a ~90° out-of-plane view gap. In-plane machinery
cannot produce out-of-plane appearance; that is the cross-view wall,
restated at the part level.

## Verdict on PATH B: FAKE (honest negative)

A pose-normalized 3D-ish part model cannot be built honestly from the
available observations. The required knowledge (depth / novel-view
appearance) is not in the data, and manufacturing it is sculpture.
PATH B is therefore NOT pursued to a render. The white-box reason is
recorded here instead of a fake rotating-head demo.
