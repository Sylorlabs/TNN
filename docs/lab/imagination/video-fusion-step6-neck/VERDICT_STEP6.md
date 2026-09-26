# Step 6 Verdict: Still a Sticker (but now attached at the neck)

## Plain verdict

**Still a sticker.** The pig's head does not read as one animal with the
bunny's body. It reads as a black blob grafted onto the bunny's head.

## What Step 6 fixed

1. **Neck anchoring works.** The donor's measured neck-cut point (119,76)
   maps exactly onto the recipient's measured neck line (185,105). The head
   no longer sits centroid-on-face (Step 5's forehead sticker). It attaches
   at the neck joint.

2. **Flip corrected.** Step 5's "upright" rule was backwards (it selected the
   dorsal-down, upside-down flip). The corrected head-side rule selects
   flip=0: the head sits in the head position (above the neck), dorsal-up
   (ears up). The upside-down flip=1 hangs the head below the neck as a
   "beard" with only 2% slot coverage; the corrected flip=0 achieves 61%.

3. **Attachment is stable.** All 24 frames show the black head coherently
   attached at the neck, moving with the recipient. No flicker or
   detachment.

## What still fails (Step 5 failures #3 and #4, not this workstream's scope)

3. **The head is an unreadable blob.** Snout, ears, eyes are not recognizable
   after the warp. It renders as a black mass, not as a pig's head. (Step 5
   failure #3: "renders as blob (ears/snout/eyes not recognizable after
   warp)".)

4. **The bunny's head is still there.** The recipient's own face — eyes,
   muzzle, mouth — remains visible underneath/around the grafted black mass.
   The pig head sits ON TOP rather than REPLACING. (Step 5 failure #4:
   "Bunny's own head/face still visible".)

## Why "sticker" and not "head swap"

The task's bar: "does the result read as ONE animal with the pig's head
attached at the neck — snout, ears, eyes recognizable as a head — or still
a sticker?"

The attachment point is now correct (neck, not forehead). The position is
now correct (head position, not beard). The orientation is now correct
(dorsal-up, not upside-down). But the head itself is not recognizable as a
head, and the recipient's head was not removed. So it reads as a sticker —
a better-placed, better-oriented sticker, but a sticker.

## What would be needed for "head swap"

- **#3 (readability):** The warp must preserve the donor head's internal
  anatomy (snout shape, ear position, eye placement) so it reads as a pig's
  head, not a blob. This is a warp-quality / feature-preservation problem.
- **#4 (replacement):** The recipient's head must be removed (or fully
  occluded) where the donor head attaches, so there's one head, not two.
  This is a recipient-head-removal / occlusion problem.

Both are separate workstreams. Step 6's neck anchoring is the correct
foundation for them: once the head is readable and the recipient's head is
gone, the neck anchor puts the new head in the right place.

## Preservation / regression table (Step 5 gains)

| Step 5 gain              | Step 6 status | Notes                                              |
|--------------------------|---------------|----------------------------------------------------|
| Two-direction facing     | KEPT          | Unchanged deliberation                              |
| Measured neck cut        | KEPT          | Now used as the warp anchor (the point of Step 6)  |
| Whole-part enforcement   | KEPT          | Unchanged; 10/10 valid donor anatomy frames        |
| Upright flip             | CORRECTED     | Step 5's rule was backwards (upside-down); fixed   |
| Identity-first transfer  | KEPT          | transfer_kind=0, donor overwrites                  |
| Cover mode               | KEPT          | Mode deliberation; anisotropic selected, 61% cover |

The "upright flip" is marked CORRECTED, not KEPT, because Step 5's flip
selection was wrong (dorsal-down). The corrected rule preserves the INTENT
(an upright head) while fixing the SELECTION. See FLIP_CORRECTION.md.
