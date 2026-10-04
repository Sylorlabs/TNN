# K2 Result: Delayed Divergence Test

**Date:** 2026-09-29 00:30 PDT
**Test:** K2 Delayed Divergence

## Setup

Phase 1: E1a/E1b taught with identical signatures (r1->o1, r2->o2). They unify.
Phase 2: Distinguishing facts arrive: (E1a, r3, o3a) vs (E1b, r3, o3b).

## Results

**Phase 1:** E1a~E1b unified (Jaccard 1.0). Query (E1b, r1) → o1 OK.

**Phase 2:** After distinguishing facts:
- Query (E1b, r3) → WITHHOLD (expected o3b) MISS
- Query (E1a, r3) → WITHHOLD (expected o3a) MISS

**Mechanism:** The unifier does NOT split. parent[] still merges E1a/E1b.
Lookup finds both (E1a,r3,o3a) and (E1b,r3,o3b) → conflict → WITHHOLD (ambiguous).

## Verdict

**H-KILL SURVIVES.** The mechanism cannot revise abstractions when contradictory
evidence arrives. The false merge persists, causing ambiguity instead of split.

**Correct behavior** (per epistemic requirements) would be:
- Detect the contradiction
- Split the concept OR maintain competing hypotheses
- Preserve provenance of the earlier (now qualified) abstraction

**Current behavior:** Collapse into WITHHOLD. The learner loses the ability to
answer correctly for EITHER entity, even though each has a taught fact.

**Implication:** SEM-L3 lacks belief revision. It is a monotonic clustering
system, not a revisable knowledge representation. This is a fundamental
architectural limitation for continuing learners.
