# Prereg Amendment 1: H-REVISE2 (P1 encoding expectation)

**Date:** 2026-09-29
**Amends:** PREREG_REVISE2.md (frozen 3f582bb46)
**Status:** FROZEN (committed before any implementation file exists)
**Reason:** corrected expectation derived from the frozen discovery order.

## Change

Phase D of the prereg states: "Expect P1 = [C0] (constant 0, broadcast-first)."

Corrected expectation: P1 = [N N SUB] (nnodes=3, bytes
[1,255,255],[1,255,255],[6,0,1]), which also computes constant 0.

## Derivation (from frozen code, no execution)

The canonical discovery (unified_learn.zag, pdiscover_direct) enumerates
1055 programs and applies the H-GENBIAS N-first filter: pass 1 considers
only N-using programs in enumeration order. For the counterexample subset
{("xab"->"xxx")}, seq=[0,0,0], n=3:

- pi=1 (N): P(k,3)=3, does not fit.
- ADD size-3 N-using programs: minimum value 3 (ADD(C0,N)), none fit.
- SUB size-3, in order: SUB(K,N) fails (k-3), SUB(N,K) fails (3-k),
  SUB(N,N) = 0 fits all k. This is the first N-using fitter.

[C0] (pi=2) is not N-using and is only reached in pass 2, which never runs
because pass 1 succeeds. Hence P1 = [N N SUB].

## Kill bar impact

None. K-RV1 tests behavior (correct outputs), K-RV2 tests that the version
store holds two distinct programs plus a condition record ([N N SUB] vs
[N C1 SUB] are distinct bytes), K-RV3/K-RV4/K-RV5 are unaffected. The
amendment corrects a design-section expectation only.

## What this confirms

The researcher's pre-implementation analysis of the frozen enumeration
order is auditable: anyone can re-derive P1 = [N N SUB] from
unified_learn.zag without running code.
