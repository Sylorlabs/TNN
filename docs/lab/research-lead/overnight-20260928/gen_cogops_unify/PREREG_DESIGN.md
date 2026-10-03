# PREREG DESIGN: GEN-COGOPS-UNIFY Full Test (C418)

Status: DESIGN ONLY. No implementation. This document is a prereg-ready
specification for the full unification test. It must be committed alone
before any implementation file exists (per loop governance).

## Hypothesis

H1: One GEN composer subsumes COGOPS composition. Learner-owned
cognitive procedures, represented as GEN MAPs with learned
kind-contracts, compose with domain MAPs through GEN's value pool, with
no cognitive-specific composition machinery.

H0 (null): Cognitive procedures require a separate composition
mechanism (bindings, plans, version selection) that GEN's trial over a
value pool cannot reproduce.

## Scope

Composition ONLY. Per the audit: REPAIR, DIVERGE, and INLINE stay
distinct. Body invention stays distinct. This test covers whether
GEN's composer can execute cognitive+domain composites.

## Arms

**U1 (replication):** Re-run the PoC's F1 (cog RET + domain COUNT).
Must reproduce ANS=1 TRIES=3 byte-identically from the frozen PoC
source. (Regression guard.)

**U2 (cog-cog composite):** Cognitive RETRIEVE + cognitive VERIFY on a
positive case (both succeed). Expect ANS=1. Tests that two cognitive
MAPs compose through the pool.

**U3 (fan-out/fan-in):** Re-run PoC's U3. Must reproduce ANS=2 TRIES=7.

**U4 (three-way with pivot):** A goal requiring a relation pivoted from
a retrieved chain (cogops-3way pattern). The pivot must be computed by
a MAP, not researcher code. Expect ANS=correct, and the pivot MAP must
appear in the trial trace. (Addresses honest negative #4.)

**U5 (order dissociation):** Two goals from the same bindings that
require opposite execution orders ([RET,VFY] vs [VFY,RET]). GEN must
solve both. The trial sequences must differ in the predicted way.
(Addresses honest negative #3. If GEN cannot, H1 is weakened.)

**U6 (learned kinds):** Replace pkind's researcher-written ranges with
kinds learned from experience (teach/observe only, no value-range
literals). Re-run U1-U3. Must still pass. (Addresses honest negative
#5. This is the strongest test of "learned contracts".)

**U7 (rename/world-B):** After freeze, rename all relations/objs
(arbitrary permutation) and re-run U1-U5. Results must be equivalent.
(Domain-blindness: no dependence on human labels.)

**U8 (oracle agreement):** On a held-out set of 20 composite goals,
GEN's answers must agree with the frozen cogops_compose binary's
answers 20/20. (Cross-mechanism validation.)

**U9 (red team):** Adversary supplies malformed goal handles
(out-of-range, negative, colliding with pool values) and adversarial
seeds. Requirements: zero panics, zero fabrications (no ANS that is
not derived from a trial), decline (-2) on all malformed inputs.

**U10 (GEN regression battery):** The full gen_generality + gen_statefix
regression suite must pass unchanged on the unified base. (Ensures the
cognitive MAPs did not regress domain composition.)

## Kill bars

| Bar | Frozen prediction | Fail means |
|-----|-------------------|------------|
| K1 | U1,U3 byte-identical to PoC | Regression; halt |
| K2 | U2 ANS=1, cog-cog composes | Cognitive MAPs do not compose; H1 falsified |
| K3 | U4 pivot MAP in trace, ANS correct | Pivot requires separate machinery; H1 weakened |
| K4 | U5 both orders solve, sequences differ as predicted | GEN cannot do order dissociation; H1 weakened |
| K5 | U6 passes with learned kinds | Contracts are researcher-supplied; H1 falsified |
| K6 | U7 rename-equivalent | Label dependence; architectural failure |
| K7 | U8 20/20 oracle agreement | GEN diverges from cogops; investigate |
| K8 | U9 zero panics, all declines | Unsafe; halt |
| K9 | U10 regression suite green | Domain regression; halt |
| K10 | 3/3 byte-identical runs | Nondeterminism; halt |
| K11 | safebin, no python, pure Zag | Process fail |
| K12 | zero em/en dash bytes in docs | Doc hygiene |

## Falsification criteria

H1 is FALSIFIED if:
- K2 fails (cognitive MAPs do not compose through the pool), OR
- K5 fails (kind-contracts cannot be learned; researcher ontology is required).

H1 is WEAKENED (but not falsified) if:
- K3 fails (pivot needs a decision, but composition still works), OR
- K4 fails (order dissociation needs plan storage, but trial-order composition works).

H1 SURVIVES if K1,K2,K5,K6,K7,K8,K9,K10,K11,K12 pass, with K3/K4
documented as weakened or addressed.

## Verdict mapping

- ALL K PASS: UNIFICATION DEMONSTRATED. GEN subsumes COGOPS composition.
- K2 or K5 FAIL: UNIFICATION FALSIFIED. Document exactly which sub-capability failed.
- K3 or K4 FAIL (only): PARTIAL UNIFICATION. Composition works; plan/pivot need separate treatment.
- Any halt bar fails: BUILD-FAIL, fix and re-prereg.

## Implementation notes (for the builder)

1. Start from the PoC lane (gu_*.zag). The PoC is the baseline.
2. The tried-table relocation (GU-GEN-DELTA 2) must be preserved. Any
   change to MAP count requires re-verifying the tried layout.
3. U6 (learned kinds) is the hardest arm. Design the kind learner
   BEFORE implementing. It must use only teach/observe, no literals.
4. U4 (pivot) needs a MAP whose body computes a relation from a chain.
   Lift from cogops_3way's pivot logic, do not write new semantics.
5. U5 (order dissociation) may require GEN to support goal-dependent
   trial ordering. If it requires a plan store, that WEAKENS H1 (K4).
   Document the mechanism honestly.
6. All arms must be pure Zag, safebin, deterministic.

## Governance

- Prereg commit must precede implementation (commit-order self-check).
- Frozen kill bars; no weakening to force passes.
- 3/3 byte-identical runs required.
- Honest negatives reported as information.
- If H1 is falsified, the negative result is the outcome. Do not
  force a unification that does not work.
