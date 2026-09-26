# Flip Correction: Step 5's "Upright" Rule Was Backwards

## The problem

Step 5's flip deliberation said: "A head is upright if the snout sits BELOW
the head centroid (nose down, the grazing/neutral pose), not above it (nose
up = upside down)." It selected flip=1.

This conflates **pitch** (nose-down vs nose-up) with **roll**
(dorsal-up vs dorsal-down, i.e. upright vs upside-down). A nose-down head can
be upside-down. A nose-up head can be upright.

## The 180° flip and dorsal-ventral

The two flip candidates differ by a 180° in-plane rotation of the donor's
head. A 180° rotation inverts BOTH the snout direction AND the
dorsal-ventral axis. Therefore, for the flip pair:

- "Snout above the neck" and "dorsal up" select the SAME flip.
- "Snout below the neck" and "dorsal down" select the SAME flip.

Step 5's "snout below = upright" selected the dorsal-down (upside-down)
flip. It was backwards.

## Dorsal verification (donor ear)

The donor is a pig, left side visible, grazing (head down). Its ear is a
dorsal landmark. In the stabilized donor frame (320x240):

- Head axis: neck (119,76) → snout (63,220)
- Ear (visible pointed protrusion at top of dark head): ≈ (97,83)
- Ear is on the up-left side of the head axis (cross-product confirmed).
- Donor dorsal direction: ≈ (-0.93, -0.36) [up-left].

Warp analysis (rotation from donor to slot, derived from the snout mapping):

- flip=0: dorsal maps to (0.94, -0.34) = right-UP. **Ears up. Upright.**
- flip=1: dorsal maps to (-0.94, 0.34) = left-DOWN. **Ears down. Upside-down.**

(The 180° difference is exact; the anisotropic scale (aspect ≤ 2.0) cannot
invert it.)

## The corrected criterion

**The warped snout must lie on the HEAD side of the recipient's neck line
(above it, where the swapped head goes).**

This is:
1. **Position:** A swapped head occupies the head position (above the neck).
   flip=1 hangs it below the neck as a "beard".
2. **Upright:** By the 180° argument, "snout above" = "dorsal up".
3. **Coverage:** flip=0 achieves 61% slot coverage; flip=1 only 2%.

## Empirical confirmation

| Flip | Snout maps to | Headside | Dorsal | Coverage | Visual |
|------|---------------|----------|--------|----------|--------|
| 0    | (144,-9)      | 1 (above neck) | up-right (upright) | 61% | Head on top, attached at neck |
| 1    | (225,219)     | 0 (below neck) | down-left (upside-down) | 2% | "Beard" under chin |

The corrected rule selects flip=0. This is a CORRECTION to Step 5, not a
regression: it preserves the intent (an upright head) while fixing the
selection (Step 5 picked the upside-down one).

## Why Step 5 got away with it

Under centroid anchoring, flip=1 (nose-down) kept the blob on the forehead —
it "looked" like a head-shaped sticker. The upside-downness was invisible
because the result was a blob (failure #3). Under neck anchoring, the
upside-down flip hangs the head below the neck, making the error obvious.
The neck anchor exposed the flip bug.
