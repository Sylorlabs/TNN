# SEM-L3 Kill Battery Preregistration

**Date:** 2026-09-28 23:45 PDT
**Status:** FROZEN (before implementation)
**Target:** mini_learn.zag / mini_stream.zag (SEM-L3 minimal v3 mechanism)

## Hypothesis Under Test

H-KILL: SEM-L3's Jaccard-based concept unifier is limited to flat equivalence
classes and cannot handle hierarchical, overlapping, or dynamically revisable
abstractions. If true, the mechanism is L2+ (clustering), not L3 (invention).

## Kill Battery (preregistered)

### K1: Signature Collision (Mandate A)

**Setup:** Two entities with IDENTICAL immediate consequence signatures but
different deeper structure (e.g., same (R,O) pairs, but one has an additional
distinguishing context not in the signature).

**Prediction if H-KILL true:** Unifier merges them (false positive).
**Kill bar:** If merged, H-KILL survives (mechanism too shallow).

### K2: Delayed Divergence (Mandate B)

**Setup:** Entities E1a/E1b appear equivalent (high Jaccard). Later, distinguishing
evidence arrives (same R, different O).

**Prediction if H-KILL true:** Unifier cannot split; the false merge persists and
corrupts subsequent inferences.
**Kill bar:** If split fails or corruption occurs, H-KILL survives.

### K3: Delayed Convergence (Mandate C)

**Setup:** Entities start with disjoint signatures. Later evidence reveals
shared structure.

**Prediction if H-KILL true:** Unifier CAN merge (this is what it does). Not a kill.
**Kill bar:** N/A (tests basic functionality, not a kill).

### K4: Partial Overlap (Mandate D)

**Setup:** Entities share SOME consequences but not others. Jaccard ~0.4 (below threshold).

**Prediction if H-KILL true:** Unifier creates NO concept (all-or-nothing). Misses
useful partial abstraction.
**Kill bar:** If no partial concept formed, H-KILL survives (mechanism too coarse).

### K5: Hierarchical Abstraction (Mandate E)

**Setup:** 
- Sparrow-like: small, flies, eats seeds
- Eagle-like: large, flies, eats meat
- Both fly.

**Prediction if H-KILL true:** Unifier creates flat clusters (sparrow~sparrow, eagle~eagle)
but NO "flying-creature" abstraction spanning both. Cannot represent hierarchy.
**Kill bar:** If no hierarchical node emerges, H-KILL survives.

### K6: Cross-Surface Transfer (Mandate F)

**Setup:** Same as RT-1 but with changed vocabulary SIZE and ARITY (not just renaming).
Add distractor relations.

**Prediction if H-KILL true:** May still work (Jaccard is structural). Not a strong kill.
**Kill bar:** If fails, H-KILL survives; if passes, weak evidence against H-KILL.

### K7: Reversed Correlation (Mandate G)

**Setup:** Training: surface prefix "nor*" correlates with concept E1. Test: "norpaline"
(prefix "nor*") is actually near-miss (different concept).

**Prediction if H-KILL true:** Unifier uses (R,O) pairs, not prefixes, so should NOT
be fooled. Not a kill (already tested in RT-8).
**Kill bar:** N/A (redundant with RT-8).

### K8: Novel Composition (Mandate H)

**Setup:** Learn concept A (objects that emit when compressed). Learn concept B
(objects that cool when heated). Test: novel object that does both; infer compositional
consequence.

**Prediction if H-KILL true:** Unifier has no composition mechanism. Cannot combine
concepts.
**Kill bar:** If composition fails, H-KILL survives.

### K9: Interference (Mandate I)

**Setup:** After learning 4 concepts, teach 200 unrelated facts (random surfaces).
Retest original probes.

**Prediction if H-KILL true:** Unrelated facts create spurious signatures; may cause
false merges or degrade Jaccard scores.
**Kill bar:** If P-PARA drops >20 points, H-KILL survives (not robust).

### K10: Fresh-Process Recovery (Mandate J)

**Setup:** Serialize parent[] and signatures to file. Terminate. Reload in new process.
Retest.

**Prediction if H-KILL true:** Should work (state is serializable). Not a kill.
**Kill bar:** N/A (tests engineering, not mechanism).

### K11: Adversarial Near-Neighbors (Mandate K)

**Setup:** Create entity with Jaccard 0.49 (just below threshold) to true concept.
Slightly increase overlap to 0.51.

**Prediction if H-KILL true:** Threshold is brittle; small changes flip merge decision.
**Kill bar:** If 0.49→0.51 causes qualitatively wrong merge, H-KILL survives (threshold hack).

### K12: Many-Concept Scaling (Mandate L)

**Setup:** 50 entities, 10 true concepts (5 pairs each), 10 near-misses.

**Prediction if H-KILL true:** O(n²) pairwise Jaccard becomes slow; false merges increase
with density.
**Kill bar:** If runtime >10x or false merge rate >10%, H-KILL survives (not scalable).

## Implementation Priority (by information gain)

1. K5 (Hierarchy) — directly tests L3 vs L2+
2. K2 (Delayed divergence) — tests revisability
3. K4 (Partial overlap) — tests representational richness
4. K8 (Composition) — tests usefulness for thinking
5. K1 (Collision) — tests shallowness
6. K9 (Interference) — tests robustness
7. K12 (Scaling) — tests practicality
8. K11 (Threshold brittleness) — tests principledness

K3, K6, K7, K10 are low-information (expected to pass or redundant).

## Success Criteria

H-KILL is KILLED (mechanism is more than flat clustering) if:
- K5 PASSES (hierarchy emerges), OR
- K2 PASSES (splits correctly), OR
- K4 PASSES (partial concepts formed), OR
- K8 PASSES (composition works)

H-KILL SURVIVES (mechanism is L2+ clustering) if:
- K5, K2, K4, K8 all FAIL, AND
- K1, K9, K11, K12 show brittleness

## Frozen

This prereg is frozen before implementation. No thresholds will be adjusted post-hoc.
All tests use pure Zag. Determinism required where applicable.
