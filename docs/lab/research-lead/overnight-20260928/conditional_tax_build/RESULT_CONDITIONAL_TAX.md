# Conditional Tax v2: Result

Date: 2026-09-30. Builder prereg: CONDITIONAL-TAX-PREREG-FROZEN,
committed 85b4325e5 before any v2 implementation (K1 satisfied).

## Verdict

CONDITIONAL-TAX-FAIL

Failing bars: P1' (CONDHIT round=-1, not <=2), P2' (A2-PASS 0, not 1).
Partial passes are diagnostics, never a pass.

## Bar-by-bar

- K1 (prereg commit strictly precedes implementation): PASS.
  Prereg at 85b4325e5; v2 implementation in r3t.zag, r1t.zag,
  frct.zag written and committed after.
- K2 (all runs complete): PASS. Nine runs, three per battery.
- K3 (pure Zag, 3/3 byte-identical, zero stderr): PASS.
  R3 md5 596c2545eba99865c812da72c652745a (3/3).
  R1 md5 97828042cbda01054424fc479beed589 (3/3).
  FREC md5 4532625993cd76afebdc62adaa65e912 (3/3).
  All nine .err files zero bytes. Zero Python at every stage.
- P1' (CONDHIT round <= 2): FAIL. CONDHIT round=-1. The Tier-1
  min-slice-4 requirement blocks the genuine COND(D,Y4,Y5) license.
  Diagnostic: with min slice 1 (debug build, not committed), CONDHIT
  round=0 and A2-PASS=1, confirming the threshold (not the tier
  mechanism) is the blocker.
- P2' (A2-PASS == 1): FAIL. A2 REUSE_IV 24 true=51/64 HAS_D=1;
  A2 SCRATCH_IV 24 true=52/64. Reuse does not solve the conditional
  target because the COND is never proposed.
- P3' (DROUND < 4): PASS. DROUND=1 (frozen baseline 4). The Tier-1
  terminal X1 still licenses COND(X1,XOR,AND) for phase-1 D.
- P4'(a) (A1-PASS == 1): PASS.
- P4'(b) (R1 PASS_SEEDS >= 0/5): PASS. Observed 2/5 (frozen 0/5,
  v1 1/5). Improvement, not regression.
- P4'(c) (FREC bests >= frozen): PASS.
  I1 best 48/64 >= 46/64 PASS.
  I2 best 63/64 >= 63/64 PASS.
  I3 best 40/64 >= 40/64 PASS.
  The v1 I3 regression (32/64) is REPAIRED. T1+T2 fix the
  evidence-overfitting as designed.
- P5' (diagnostic): not measured (P1' failure makes crowding
  diagnostic moot for the primary; FREC I3 beam composition
  available in raw outputs).
- F-CASE (eight audits): none fire. PASS.
  String audit clean on added/modified lines of all three files
  (diff-scoped grep for Y4/Y5/y4/y5/710202/fam8/F-PARCOND/
  710101-710299: zero matches). Gate, enumeration, semantics,
  tax-rate, tier, and tax-base audits verified by code review:
  tier classification branches only on ndg(nodes, n, 0)==0 vs ==1
  (node kind, structural); COND base B=2 (Tier-1) / B=4 (Tier-2)
  with uniform 200/opc; combiner enumerates Tier-1 (kind 0) then
  Tier-2 (kind 1) in beam order with no identity filter.

## Diagnosis

The v2 design correctly diagnoses and repairs the FREC-I3
evidence-overfitting: P4'(c) passes with I3 at the frozen 40/64
(v1: 32/64). The stability-gated license (T2) plus license-cost tax
(T1) work as intended on the control.

However, the Tier-1 minimum slice size of 4 rows is miscalibrated
for the R3 phase-2 target. The genuine structural condition D has
fewer than 4 rows in at least one branch of the observed evidence,
so the Tier-1 license never fires, CONDHIT stays -1, and A2-PASS
fails. The design's worked example assumed 32 rows per slice; the
actual evidence distribution is sparser.

This is a threshold calibration failure, not a mechanism failure:
with min slice 1, the full v2 mechanism (T1+T2) achieves CONDHIT 0
and A2-PASS 1 while retaining the FREC-I3 repair (verified in
uncommitted debug build /tmp/r3t_debug_bin).

## What this means

- The stability-gating principle is validated: it repairs I3
  without breaking I1/I2/R1/A1.
- The license-cost tax (T1) is validated: it participates in the
  repair (v1 I3 32/64 -> v2 I3 40/64).
- The Tier-1 min-slice-4 threshold is too strict for sparse
  structural conditions. A future design should calibrate the
  minimum slice to the evidence regime (e.g., min(4, en/8) for
  Tier-1 as well, or a lower absolute floor).
- No L3 claim. No Criterion 0 claim. Bounded-L2 only.

## Files

- PREREG_CONDITIONAL_TAX.md (frozen, 85b4325e5)
- r3t.zag, r1t.zag, frct.zag (v2 implementation)
- r3t_bin, r1t_bin, frct_bin (znc-built, not committed)
- TAX_R3_1/2/3.txt, TAX_R1_1/2/3.txt, TAX_FRC_1/2/3.txt (raw outputs)
- RESULT_CONDITIONAL_TAX.md (this file)

CONDITIONAL-TAX-FAIL (P1', P2').
