# SEM-L3 Minimal v3: Red-Team Results

**Date:** 2026-09-29 ~03:15 PDT
**Target:** mini_learn.zag (v3 world)

## RT-1: Template Break — PASS

**Attack:** Rename all relations and objects to arbitrary tokens (r1, o1, r2, o2...).
Preserve the STRUCTURE (which surfaces share which pairs), destroy name meaning.

**Result:** Learner still unifies 4/4 true pairs, rejects 2/2 near-misses, scores 8/8.
**Verdict:** PASS. Learner uses structural equivalence, not template matching.

## RT-8: Memorization — PASS

**Attack:** Near-miss entities (norpaline, vellux) share surface prefixes and relations
with true entities. If learner memorizes surface similarity, it will falsely unify.

**Result:** 0/2 false unifications. P-NEAR 5/5 (correct withholds + distinct recall).
**Verdict:** PASS. Distinguishing check (same R, different O) blocks false unification.

## RT-7: Source Inspection — PASS (by construction)

**Attack:** Check if probe answers leak into teaching (entity IDs, answer keys).

**Result:** World generator emits only surface forms. No entity IDs in output.
Probes use untaught (S,R) combinations. Teaching and probe generation are separate.
**Verdict:** PASS.

## Summary

- RT-1 (Template): PASS
- RT-7 (Source): PASS  
- RT-8 (Memorization): PASS

**Remaining:** RT-2 (spurious correlation), RT-3 (uncertainty), RT-4 (ambiguity),
RT-5 (polysemy/split), RT-6 (scale). These require the full SEM-L3 implementation
with splitter and larger world.
