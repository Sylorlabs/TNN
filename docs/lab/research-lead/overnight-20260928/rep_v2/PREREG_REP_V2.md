# Preregistration: Representation Invention v2 (FDCR)

**Date:** 2026-09-29 07:20 PDT
**Status:** FROZEN (before implementation)
**Researcher:** Representation Invention Researcher (v2)
**Target:** New Zag implementation `rep_v2/fdcr_learn.zag` (does not yet exist)

## Background

SEM-L3 (Jaccard + union-find) was falsified as L3. It is L2+ bounded structural
clustering. Three fatal limitations (KILL_BATTERY_PREREG.md, results K2/K4/K5):

1. **K5:** No hierarchical abstraction. Sparrow/eagle clusters form, but no
   "flying creature" parent emerges from the shared (flies, yes) feature.
2. **K2:** No revision. E1a/E1b merge, distinguishing facts arrive, mechanism
   collapses to WITHHOLD for both. Cannot split a false merge.
3. **K4:** No partial overlap. 2/4 shared features (Jaccard 0.33) yields NO
   concept at all. Binary threshold, no graded membership.

## Hypothesis

**H-REP:** A concept learner with (a) lattice-structured concepts (intent +
members + parent/child links), (b) failure-driven structure-growth operators,
and (c) graded membership overcomes all three limitations while remaining
generic (no hardcoded hierarchy, overlap, or domain semantics).

## Mechanism: Failure-Driven Concept Recruitment (FDCR)

### Representation

A **concept** is:
- **intent:** set of characteristic features, where a feature = (relation, object)
  pair observed in experience
- **members:** entities currently assigned
- **parent / children:** hierarchical links (a concept lattice, not flat partitions)
- **provenance:** which operator created it and from what evidence
- **active:** whether currently in force

**Membership is graded:** strength(E, C) = |features(E) intersect intent(C)|
/ |intent(C)|. Full membership = 1.0. Partial membership is representable
(overlap), unlike SEM's binary merge/no-merge.

### Operators (generic, domain-blind)

Operators trigger on specific structural signals, not on task content:

1. **FORM (shared-subset recruitment):** If two or more active concepts share a
   non-empty feature subset S that is not the intent of any existing concept,
   create a new concept with intent S. The sharing concepts become its children
   (or gain it as an ancestor). This is the hierarchy engine: shared structure
   recruits a parent. Nothing about "flying" or "birds" is in the operator.

2. **MERGE (identity collapse):** If two concepts have identical intents, unify
   them (union of members, one survives). Prevents duplicate concepts.

3. **SPLIT (contradiction-driven revision):** If members of one concept exhibit
   contradictory outcomes for the same relation (R maps to O1 for some members
   and O2 != O1 for others), split: create one child per distinct outcome with
   intent = parent intent + the distinguishing (R, Oi) feature, members =
   those exhibiting Oi. The parent is PRESERVED (shared abstraction survives;
   only the overgeneralization is repaired). This is the revision engine.

4. **GRADE (graded inference):** Queries are answered via the most specific
   concept containing the entity; confidence = membership strength. Partial
   matches yield partial-confidence answers instead of WITHHOLD-or-nothing.

5. **COMPOSE (exploratory v1):** Given two concepts, form a candidate with
   intent = union of intents. Tested on a simple case only.

6. **CONTEXTUALIZE (exploratory v1):** Facts may carry an optional context tag.
   If a would-be SPLIT correlates with context tags (distinguishing facts come
   from different contexts), create context-conditioned children instead of
   entity-specific ones. Minimal test only.

### Learning loop (batch v1)

1. Ingest facts. Build per-entity feature sets.
2. One concept per entity (intent = full feature set).
3. MERGE identical intents (fixpoint).
4. Detect contradictions within concepts -> SPLIT (fixpoint).
5. FORM parents for uncovered shared subsets (fixpoint).
6. Answer probes via most-specific-concept + GRADE.

Streaming/incremental update is future work; v1 re-runs the loop per batch.
Phase structure of K2 (teach, learn, teach more, learn again) is supported
because the loop is re-entrant on accumulated facts.

### Inspiration disclosure

The concept lattice (intent/extent, parent/child via subset relation) is
inspired by Formal Concept Analysis. FDCR differs in three load-bearing ways:
(1) concepts are recruited on demand by failure/success signals, the full
lattice is NOT computed; (2) SPLIT provides contradiction-driven revision,
which FCA does not have; (3) graded membership drives inference, not just
binary extent membership. FCA is inspiration, not the implementation.

### What this is NOT

- Not Jaccard + union-find (no pairwise similarity, no threshold, no DSU).
- Not a hardcoded hierarchy (no "bird" or "flying" in source; parents emerge
  from shared subsets).
- Not a neural network, transformer, or probabilistic graphical model.
- Not a fixed ontology (all concepts are learner-created).

## Predictions

If H-REP is true, then on the exact K5/K2/K4 setups that killed SEM:

### K5-v2 (Hierarchy) -- KILL BAR

Setup: identical to K5_RESULT.md (sparrows S1/s1/S2/s2, eagles E1/e1/E2/e2).

- FORM recruits a parent concept P with intent exactly {(flies, yes)}.
- All 8 entities are members of P (strength 1.0).
- Sparrow-concept and eagle-concept are children of P.
- **PASS iff:** P exists with intent {(flies,yes)} AND all 8 entities are
  members AND the two cluster concepts are descendants of P.
- SEM scored: no parent (FAIL).

### K2-v2 (Delayed split) -- KILL BAR

Setup: identical to K2_RESULT.md. Phase 1: E1a/E1b identical -> one concept.
Phase 2: (E1a,r3,o3a), (E1b,r3,o3b) arrive -> contradiction -> SPLIT.

- After phase 2, query (E1b, r3) -> o3b; query (E1a, r3) -> o3a.
- Parent concept {(r1,o1),(r2,o2)} preserved with both members.
- **PASS iff:** both probes correct.
- SEM scored: WITHHOLD / WITHHOLD (FAIL).

### K4-v2 (Partial overlap) -- KILL BAR

Setup: identical to K4_RESULT.md. B1: 4 features; B2: 4 features; 2 shared.

- FORM recruits shared concept S with intent {(r1,o1),(r2,o2)}.
- B1 and B2 are both members of S (strength 1.0 on S).
- B1 and B2 each retain specialized child concepts (their full 4-feature
  intents), so they are represented as OVERLAPPING, not disjoint and not
  merged.
- Graded cross-membership is computed: strength(B1, B2-concept) = 0.5,
  strength(B2, B1-concept) = 0.5 (reported, not a bar).
- **PASS iff:** S exists with exactly the 2 shared features AND B1,B2 are
  members AND distinct specialized children exist for B1 and B2.
- SEM scored: no concept at all (FAIL).
- The analogical probe (B2,r3)->o3 is EXPLORATORY (reported with confidence,
  not a kill bar), because inferring B2's r3 from B1 is a guess, not a
  deduction. The bar is representational (shared concept exists), matching
  the K4 verdict's "form a partial concept" criterion.

### K3-v2 (Delayed merge) -- non-kill sanity

Entities start disjoint; later facts reveal shared structure -> FORM creates
parent. PASS iff parent forms. (SEM could do this; confirms no regression.)

### K-CTX (Context) -- exploratory

Minimal: entity E shows (E,r,o1) in context c1, (E,r,o2) in context c2.
CONTEXTUALIZE creates context-conditioned children. Reported, not a bar.

### K-COMP (Composability) -- exploratory

Two concepts A (intent {a}), B (intent {b}); COMPOSE forms C intent {a,b};
probe via C works. Reported, not a bar.

## Controls

- **C-LIT (literal baseline):** Answer probes from taught facts only, no
  concepts. Expect 0/4 on inference probes (the K5/K2/K4 probes requiring
  generalization). Confirms the probes are not trivially answerable.
- **C-REG (no regression):** Original mini_world 8/8 (P-PARA 3/3, P-NEAR 5/5).
  FDCR must score 8/8. A new mechanism must not lose what the old one could do.

## Falsification conditions

H-REP is KILLED (not merely weakened) if:
- K5-v2, K2-v2, K4-v2 ALL fail, OR
- the implementation is found to reintroduce Jaccard-threshold + union-find
  under other names, OR
- the "hierarchy" is hardcoded (e.g., source contains the expected parent
  intents for the test fixtures).

H-REP SURVIVES (bounded) if at least one kill bar passes. Each bar is
reported independently; a 1/3 is not "basically L3."

## Scope and honesty constraints

1. Batch learning only in v1. No streaming, no persistence across processes.
2. Small fixtures (the exact K5/K2/K4 setups). Scaling is future work.
3. Context and composability are exploratory; weak results there do not kill
   H-REP but must be reported as limitations.
4. The operators are researcher-designed. Any L3 assessment must be against
   the nine criteria and must be conservative. This prereg claims
   representational ADEQUACY (the structure can express hierarchy/overlap/
   revision), not L3 invention, which requires transfer, ablation, red team,
   and the rest.
5. Pure Zag. No Python anywhere (implementation, fixtures, scoring).
6. Deterministic. All outputs byte-reproducible.

## Frozen

Prereg frozen before implementation. `fdcr_learn.zag` does not exist yet.
Kill bars will not be adjusted post-hoc. If the design changes during
implementation, an amendment will be filed BEFORE results are examined.
