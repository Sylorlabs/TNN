# Conditional Threshold Calibration: Result

Date: 2026-09-30. Builder prereg: CONDITIONAL-THRESHOLD-PREREG-FROZEN,
committed 7ae3a88fa before any threshold implementation (K1 satisfied).

## Verdict

THRESHOLD-PASS

All frozen bars pass. Partial passes are reported as diagnostics;
none were needed.

## Bar-by-bar

- K1 (prereg commit strictly precedes implementation): PASS.
  Prereg at 7ae3a88fa; threshold implementation in r3h.zag, r1h.zag,
  frch.zag written and committed after.
- K2 (all runs complete): PASS. Nine runs, three per battery.
- K3 (pure Zag, 3/3 byte-identical, zero stderr): PASS.
  R3 md5 12f93b593d65bb986e5e23ad9df33d3d (3/3).
  R1 md5 cc0300294803ee8ee8d684ced90d6aad (3/3).
  FREC md5 bde90e4686883846724d56b4ebd9c81f (3/3).
  All nine .err files zero bytes. Zero Python at every stage.
- P1'' (CONDHIT round <= 2): PASS. CONDHIT round=0. At R3 phase-2
  round 0, en=8 gives minsl1=min(4,8/8)=1, reproducing the debug-build
  regime (min slice 1) that the v2 result reported as achieving
  CONDHIT 0 and A2-PASS 1. The preregistered mechanistic prediction
  is confirmed by the committed implementation.
- P2'' (A2-PASS == 1): PASS. A2 REUSE_IV 5 true=64/64 HAS_D=1;
  A2 SCRATCH_IV 24 true=52/64. Reuse solves the conditional target
  with the D library term present.
- P3'' (DROUND < 4): PASS. DROUND=1 (frozen baseline 4; v2 also 1).
- P4''(a) (A1-PASS == 1): PASS.
- P4''(b) (R1 PASS_SEEDS >= 0/5): PASS. Observed 1/5 (frozen 0/5;
  v2 achieved 2/5; seed 84044 hits 64/64). No regression.
- P4''(c) (FREC bests >= frozen): PASS.
  I1 best 48/64 >= 46/64 PASS.
  I2 best 63/64 >= 63/64 PASS.
  I3 best 40/64 >= 40/64 PASS (seed S33).
  The v2 I3 repair (32/64 to 40/64) is PRESERVED under the
  recalibrated Tier-1 threshold. The residual risk named in the
  prereg (lenient early-round Tier-1 reintroducing overfitting)
  did not materialize: I3 holds at the frozen bar.
- P5'' (diagnostic): FREC I3 beam composition available in raw
  outputs; not needed for the verdict.
- F-CASE (nine audits): none fire. PASS.
  Audit 1 (string): diff-scoped grep of added/modified lines in all
  three files for Y4/Y5/y4/y5/710202/fam8/F-PARCOND/710101-710299:
  zero matches.
  Audits 2-8 (gate, enumeration, semantics, tax-rate, tier, tax-base,
  generality): unchanged from v2; the diff touches only comments and
  the minsl1 computation. Verified by code review: no new branch on
  terminal index or node identity; enumeration order unchanged;
  COND multiplexer semantics unchanged; 200/opc rate unchanged;
  tier classification still only ndg(nodes, n, 0)==0 vs ==1;
  B=2/B=4 unchanged; P3'' supplies the second compositional target.
  Audit 9 (threshold): minsl1 is computed purely from en (evidence
  row count, structural) as min(4, en/8); no branch on node identity,
  terminal index, family, or target literals anywhere in the
  threshold computation.

## Diagnosis

The threshold calibration failure is repaired. The v2 mechanism's
two load-bearing components (T1 license-cost tax, T2 stability-gated
license) are confirmed as the actual FREC-I3 repair: with only the
Tier-1 threshold recalibrated and everything else byte-identical to
v2, I3 stays at 40/64 while the R3 Arm 2 compositional repair is
restored (CONDHIT 0, A2-PASS 1). The v2 diagnosis stands: the
threshold was miscalibrated, not the mechanism.

Calibration summary:
- Tier-1 min slice = min(4, en/8): en=8..15 gives 1, en=16..23
  gives 2, en=24..31 gives 3, en>=32 gives 4.
- Tier-2 unchanged: min slice max(4, en/8) plus persistence gate.
- At en>=32 both tiers use 4; below en=32 Tier-1 is strictly more
  lenient, matching the design rationale (Tier-1 conditions are
  terminals/library terms, stable by construction).

## What this means

- Conditional-first search (COND primitive + BAP combiner) now
  passes all frozen bars: it repairs the R3 Arm 2 compositional
  reuse failure (the beam lineage's binding constraint per
  BEAM-REVIEW-COMPLETE) without regressing any frozen control.
- Scope remains bounded-L2: COND is researcher-supplied; no L3
  claim, no Criterion 0 claim. The mechanism does not invent
  conditionals.
- This result does not by itself promote the mechanism through the
  eleven-stage pipeline; it is a builder-stage result
  (THRESHOLD-PASS, not SURVIVES).

## Files

- PREREG_CONDITIONAL_THRESHOLD.md (frozen, 7ae3a88fa)
- r3h.zag, r1h.zag, frch.zag (threshold implementation; single
  change from v2: Tier-1 min slice min(4, en/8))
- r3h_bin, r1h_bin, frch_bin (znc-built, not committed)
- THR_R3_1/2/3.txt, THR_R1_1/2/3.txt, THR_FRC_1/2/3.txt (raw outputs)
- RESULT_CONDITIONAL_THRESHOLD.md (this file)

THRESHOLD-PASS.
