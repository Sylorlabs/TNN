# K5 Result: Hierarchy Test

**Date:** 2026-09-29 00:15 PDT
**Test:** K5 Hierarchical Abstraction

## Setup

Sparrow-like (S1/s1, S2/s2): flies->yes, size->small, eats->seeds
Eagle-like (E1/e1, E2/e2): flies->yes, size->large, eats->meat

## Results

**Unifications:**
- Sparrow cluster: S1~s1~S2~s2 (all 6 pairs, Jaccard 3/3=1.0)
- Eagle cluster: E1~e1~E2~e2 (all 6 pairs, Jaccard 3/3=1.0)
- Cross-cluster: NONE (S1~E1 Jaccard 1/5=0.2 < 0.5)

**Hierarchy:** NONE. No "flying creature" node spanning both clusters.

## Verdict

**H-KILL SURVIVES.** The mechanism forms flat equivalence classes but cannot
invent hierarchical abstractions. The shared (flies, yes) pair does not generate
a higher-level concept. This is a fundamental limitation of pairwise Jaccard
clustering.

**Implication:** SEM-L3 is L2+ (clustering), not L3 (invention of novel representational
primitives). The "concepts" are equivalence classes, not hierarchical abstractions.
