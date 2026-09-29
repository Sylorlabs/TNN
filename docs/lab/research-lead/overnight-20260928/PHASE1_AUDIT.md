# Phase 1 Audit: SEM-L3 L3 Criteria (Independent Reproduction)

**Date:** 2026-09-28 23:30 PDT
**Auditor:** Research lead (independent reproduction)
**Method:** Recompiled from source, reran, verified scores, audited each criterion.

## Reproduction Results

**Build:** Pure Zag, compiled with znc 2026.07.0-dev. No Python.

**Scores (reproduced):**
- With unification: 8/8 total (P-PARA 3/3, P-NEAR 5/5)
- Without unification (ablation): 5/8 total (P-PARA 0/3, P-NEAR 5/5)
- Determinism: 3/3 byte-identical (1 unique SHA-256)

**Unifications (reproduced):**
- norpal ~ squeezer (Jaccard 2/4 = 0.50)
- vellum ~ sheet (Jaccard 2/3 = 0.67)
- glim ~ glow (Jaccard 2/2 = 1.00)
- ferrum ~ ironbar (Jaccard 2/2 = 1.00)
- norpaline: NOT unified (distinguished)
- vellux: NOT unified (distinguished)

All match reported results. Reproduction CONFIRMED.

## Criterion Audit

### C1: Structure not enumerated beforehand — PASS

**Definition:** The final learned concept nodes must not appear as literals in source.
**Evidence:** mini_learn.zag contains no hardcoded surface pairs. UNIFY output shows
discovered pairs (norpal~squeezer, etc.) that emerge from data.
**Mechanism:** Jaccard similarity over consequence signatures.
**Limitation:** The ALGORITHM (Jaccard + threshold) is human-authored. Only the
SPECIFIC groupings are learner-discovered.

### C2: Created after experience — PASS

**Definition:** Nodes must emerge from teaching data, not initialization.
**Evidence:** parent[] initialized to identity (parent[i]=i). Unifications occur
only after T facts are processed. Empty input → no unifications.
**Mechanism:** Incremental signature building, pairwise Jaccard check.
**Limitation:** None identified.

### C3: Inspectable persistent state — PASS

**Definition:** The invented structure must exist in observable state.
**Evidence:** UNIFY lines print discovered nodes. parent[] array holds equivalence
classes. In mini_stream.zag, state persists across interleaved T/Q stream.
**Mechanism:** Union-find parent pointers.
**Limitation:** In batch mini_learn, state is per-run (not cross-process persistent).
mini_stream demonstrates in-process persistence.

### C4: Causal trace — PASS

**Definition:** Must be able to explain WHY a specific node was created.
**Evidence:** Output includes "jacc 2/4" showing the similarity score. Distinguishing
check is explicit in source (same R, different O blocks unification).
**Mechanism:** Jaccard >= 0.5 AND no distinguishing triple.
**Limitation:** Trace is at the algorithmic level, not a "reason" in cognitive terms.

### C5: Ablation reduces capability — PASS

**Definition:** Removing the invented structure must hurt performance on unseen cases.
**Evidence:** mini_learn_nounify.zag (unification disabled): P-PARA 3/3 → 0/3.
P-NEAR unchanged (5/5), showing the drop is specific to concept-dependent probes.
**Mechanism:** Without parent[] merges, probe lookup finds no (member,R) facts.
**Limitation:** Ablation is coarse (all-or-nothing). Per-concept ablation not tested.

### C6: Generalizes to unseen instances — PASS

**Definition:** Must answer probes using (S,R) combinations never taught.
**Evidence:** Probe (squeezer, sqz_heat, ?) → velx. Teaching contains (norpal, sqz_heat, velx)
but NOT (squeezer, sqz_heat, *). Correct answer requires norpal~squeezer concept.
**Mechanism:** Concept-mediated lookup: resolve S to concept, search member facts.
**Limitation:** "Unseen" is within the same fixture distribution. No out-of-distribution test.

### C7: Reused later — PASS

**Definition:** Invented structure must be applied to cases beyond its creation context.
**Evidence:** Transfer test: novel surface norpal2 (2 examples) unified with E1 concept.
Probe (norpal2, sqz_heat, ?) → velx correct via reused concept.
mini_stream: concept formed at fact 4, used at query 7.
**Mechanism:** New surfaces with overlapping signatures merge into existing concepts.
**Limitation:** Reuse is within the same relational vocabulary. No cross-domain reuse.

### C8: Transfers to surface-different problem — PASS (with caveat)

**Definition:** Must work when surface forms change but deeper structure preserved.
**Evidence:** RT-1: all relations/objects renamed to arbitrary tokens (r1, o1, r2, o2...).
Structure (which surfaces share which pairs) preserved. Result: still 8/8, same unifications.
**Mechanism:** Jaccard operates on pair equality, not name meaning. r1==r1 regardless of label.
**Caveat:** This is "surface-different" in the sense of arbitrary renaming, but the
ABSTRACT structure (bipartite incidence) is identical. A stronger test would change
the relational vocabulary size, arity, or introduce distractors. Previous session
marked this as pending; audit finds the RT-1 evidence satisfies the criterion as stated,
but notes the limitation.

### C9: Simpler explanations attacked — PARTIAL

**Definition:** Must meaningfully test alternatives: signature hashing, equivalence-class
formation, deterministic clustering, memorization, template matching, hand-designed
equivalence, accidental fixture structure.

**Attacked:**
- Template matching: RT-1 PASS (arbitrary names work → not string-template matching).
- Memorization: RT-8 PASS (near-misses not unified → not mere similarity).
- Ablation: PASS (0/3 without concepts → not direct lookup).

**NOT attacked (or IS the mechanism):**
- Deterministic clustering: The mechanism IS Jaccard-based clustering. This is not
  a refuted alternative; it is an accurate description. The question is whether
  "clustering" qualifies as "invention". The L3 definition requires "useful representation
  not enumerated in solution space". The clusters are useful and not enumerated. But
  they are also exactly what a clustering algorithm produces.
- Equivalence-class formation: Same as above. The unifier forms equivalence classes.
  This is not an alternative explanation; it IS the mechanism.
- Accidental fixture structure: v1→v2→v3 iterations show the fixture was engineered
  for clean separation (disjoint vocabularies in v3). v2 failed because the world was
  "too entangled". This suggests the mechanism requires carefully separated fixtures
  to work. A genuine invention mechanism should handle messier worlds.

**Verdict:** 8/9 PASS, 1/9 PARTIAL (C9).

## Reconciliation with Previous 7/9 Claim

Previous session claimed 7/9 (C1-C7 PASS, C8-C9 pending).
This audit finds C8 PASSES based on RT-1 evidence (arbitrary renaming).
C9 remains PARTIAL: template/memorization attacked, but "it's just clustering"
is not refuted because it is true. The mechanism IS clustering.

## The Core Question

> Is SEM-L3 genuinely representational invention, or sophisticated narrow pattern matching?

**Honest assessment:** It is deterministic Jaccard clustering over consequence signatures.
The clusters are:
- Not pre-enumerated (C1 PASS)
- Useful for generalization (C5, C6 PASS)
- Reused (C7 PASS)
- Robust to renaming (C8 PASS)

But they are also:
- Exactly what the algorithm is designed to compute (not surprising)
- Brittle to fixture entanglement (v2 failed)
- Limited to equivalence classes (no hierarchy, no overlap, no splitting)

**This is L2+ (learner constructs relationships from generic mechanisms), not clearly L3.**
The L3 bar requires "invents/recruits a useful representation or primitive not enumerated
in the solution space." The Jaccard-clustering ALGORITHM was enumerated. The SPECIFIC
clusters were not. This is a gray area.

**Recommendation:** Phase 2 kill battery must test whether the mechanism can go beyond
flat equivalence classes (hierarchy, overlap, splitting, delayed divergence/convergence).
If it cannot, downgrade to L2+ and focus on what WOULD constitute genuine invention.
