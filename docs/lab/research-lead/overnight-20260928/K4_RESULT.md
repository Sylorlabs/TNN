# K4 Result: Partial Overlap Test

**Date:** 2026-09-29 01:00 PDT
**Test:** K4 Partial Overlap

## Setup

B1: (r1,o1), (r2,o2), (r3,o3), (r5,o5) - 4 pairs
B2: (r1,o1), (r2,o2), (r4,o4), (r6,o6) - 4 pairs
Shared: 2, Jaccard = 2/6 = 0.33 (< 0.5 threshold)

## Results

**Unifications:** NONE (Jaccard below threshold).
**Probe:** (B2, r3) → o3: MISS (0/1).

## Verdict

**H-KILL SURVIVES.** The mechanism is all-or-nothing. With 50% structural overlap
(2/4 shared pairs), NO concept is formed. The learner cannot represent partial
similarity, graded membership, or overlapping abstractions.

**A genuine invention mechanism** should be able to:
- Form a partial concept for the shared structure, OR
- Represent B1 and B2 as overlapping (not disjoint), OR
- Use the 2 shared pairs to bootstrap inference

**Current behavior:** Binary threshold. Below 0.5 = no abstraction at all.
