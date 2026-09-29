# Phase 4 Prereg: Concept Usefulness for Downstream Reasoning

**Date:** 2026-09-29 01:45 PDT
**Status:** FROZEN (before implementation)
**Question:** Do SEM-L3's invented concepts (L2+ clusters) improve later cognition?

## Hypothesis

H-USE: Concept nodes (even if L2+) provide functional advantage for prediction,
retrieval, or transfer compared to literal memory.

## Experiment Design

**Task:** Predict the object given (subject, relation), where subject is a novel
surface with sparse evidence.

**Setup:**
- Teaching: E1 concept (norpal/squeezer) with 6 facts (as in v3).
- Novel surface: "zorp" taught with 2 facts: (zorp, sqz_emit, glimx), (zorp, sqz_glow, glowx).
- Test: (zorp, sqz_heat, ?) → should be velx (via E1 concept).

**Conditions:**
1. **Full:** mini_learn with unification (concepts available).
2. **Ablated:** mini_learn_nounify (no concepts, literal only).
3. **Nearest-match:** Simple baseline: find taught surface with most overlapping (R,O) pairs, copy its answer.

**Prediction:**
- Full: CORRECT (via concept)
- Ablated: WITHHOLD (no (zorp, sqz_heat) taught)
- Nearest-match: CORRECT (zorp shares 2 pairs with norpal/squeezer; nearest is norpal)

**Kill bar for H-USE:** If Nearest-match baseline matches Full performance, then
concepts add NO advantage over simple similarity. H-USE is KILLED (concepts are
just fancy nearest-neighbor).

**Survival bar:** If Full > Nearest-match on a harder test (e.g., with distractors
or where nearest-match picks wrong due to surface similarity), H-USE survives.

## Harder Test (if basic passes)

Add distractor: "zorpal" (similar name to "zorp", but different concept).
- (zorpal, sqz_emit, o_distract), (zorpal, sqz_glow, o_distract2)
- Nearest-match might pick zorpal (name similarity) over norpal (structural).
- Full (concept-based) should pick norpal (structural overlap).

If Full succeeds where Nearest-match fails, concepts provide genuine abstraction
beyond surface similarity.

## Frozen

No thresholds adjusted post-hoc. Pure Zag. Deterministic.
