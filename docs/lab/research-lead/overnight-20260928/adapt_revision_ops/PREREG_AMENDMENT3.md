# PREREG Amendment 3: S1 uses a cyclic world change

Status: pre-implementation (no implementation committed yet; the
trial run below used uncommitted scratch sources only). This
amendment changes only the S1 world-change fact and expected
answer. It does not change the operators, the revision predicate,
kind dispatch, the battery structure, or any other arm.

## Finding: rebind steals the S1 phase-4 answer

The trial run (after Amendment 2: T1/T2-PASS, S2/S3-PASS, S1-FAIL)
showed S1 phase 4 answering 98 via rebind, not via the revision
bracket. Cause: the world-change fact (12,3,98) creates the
2-hop path 11->12->98, and rebind's pc_try_one assembles it from
Xs's shape (plen 3) before the adapt bracket ever runs. No
REVISE2-STALE fires; no revision is created.

This is correct rebind behavior, but it bypasses the operator
under test. The prior work's R1 defeated rebind the same way:
its frontier fact (14,3,12) formed a cycle that t2_gather rejects,
so no value path existed for rebind to steal.

Fix (driver only): S1's world change now teaches (12,3,12)
instead of (12,3,98). The path 11->12->12 is cyclic and rejected
by t2_gather's cycle check, so rebind cannot assemble it. The
revision path is unaffected: ts_specialize_src uses t2_lu_first
directly (not t2_gather), creates Xs2=[1,3] via (12,3,12), and
compose walks it to 12.

## Revised kill bar (frozen)

- K-S1: phase-2 ans = 99; phase-4 query (11,73,12) ans = 12;
  revision emits REVISE2-STALE kind=3 for Xs; new MAP Xs2
  relseq [1,3] with type-16 Xs2->Xs; Xs retired; type-16 Xs->X
  persists; X live and intact; Tt live; no type-16 targets Tt;
  type-16 edge count = c0+1. (Expected answer 98 -> 12; world
  fact (12,3,98) -> (12,3,12).)
- K-T1, K-T2, K-S2, K-S3, K-D, K-H1, K-H2: unchanged from
  Amendments 1-2.

## Unchanged

- Operators (ts_patch.zag), revision predicate, kind dispatch.
- All other arms, queries, expected answers.
- The TRUNCATE theorem.
- Commit order: this amendment is committed alone before the
  implementation.
