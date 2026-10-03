# ABLATION: DDES step 8 (guidance component ablation)

Wave: wave-20261002-0521pdt. Lane: DDES.
Prereg: PREREG_DDES78.md, frozen alone at ac7cc6856.
Same binary and transcripts as SEALED_EVAL.md (one deterministic
matrix: 5 variants x 6 sealed OOD worlds x 2 configs, 3/3
byte-identical runs, sha256
f7a7ec52bd642604c9ffc3619a72836674de4bc8a4e0d11b5895306c56dda074).

## Binding constraints honored

- The three binding citation caveats (see SEALED_EVAL.md) still
  bind every citation; nothing here weakens them.
- The DDES-ALT H1(b) rule: every equivalence and difference
  below is judged on DECISION lines only (TARGET, PLAN, EXEC,
  PRED, ELIM/SURVIVE, CONVERGE, CELLSUM). FLAG lines and variant
  labels are excluded from all comparisons. The FLAG marker is
  emitted in all five variants and remains print-only; it is not
  re-ablated here (already settled as unconsumed by DDES-ALT).

## Variants (controlled, derivation code otherwise unchanged)

- V_full: clamp max(t*,1) + t*-derived waits + earliest-frontier.
- V_noclamp: C1 removed (identity waits), C2 + C3 kept.
- V_nowaitderiv: C2 removed (fixed w=2), C1 + C3 kept.
- V_nofrontier: C3 removed (anti-frontier), C1 + C2 kept.
- V_none: C1 + C2 + C3 all removed (fixed w=2, anti-frontier).

## Measured CELLSUM verdict table (all variants x worlds)

- V_full:       O1 CORRECT, O2 CORRECT, O3 CORRECT,
                O4 CORRECT, O5 CORRECT, O6 LOUD-FAIL.
- V_noclamp:    O1 CORRECT, O2 CORRECT, O3 SILENT-WRONG,
                O4 CORRECT, O5 CORRECT, O6 SILENT-WRONG.
- V_nowaitderiv: O1 LOUD-FAIL, O2 LOUD-FAIL, O3 CORRECT,
                O4 LOUD-FAIL, O5 LOUD-FAIL, O6 LOUD-FAIL.
- V_nofrontier: O1 CORRECT, O2 CORRECT, O3 CORRECT,
                O4 CORRECT, O5 CORRECT, O6 LOUD-FAIL.
- V_none:       O1 LOUD-FAIL, O2 LOUD-FAIL, O3 CORRECT,
                O4 LOUD-FAIL, O5 LOUD-FAIL, O6 LOUD-FAIL.

## Decision-line diffs vs V_full (mechanical, FLAG excluded)

- V_noclamp: IDENTICAL decision lines on O1, O2, O4, O5.
  DIFFER on O3 (plan [S,OY] vs [S,W,OY]; cfg0 EXEC real=0,
  PRED 1/0, ELIM h0 with h0 true, convergence claimed on h1)
  and on O6 (plan [S,OZ]; cfg0 EXEC real=0, PRED 1/0,
  ELIM h0 true). Both diffs carry verdict flips.
- V_nowaitderiv: DIFFER on all six worlds. O1/O2/O4/O5:
  fixed w=2 cannot reach t* (5, 12, 3, 4); PRED h0=0 h1=0,
  p0==p1, CONVERGE-FAIL, verdict flips CORRECT to LOUD-FAIL.
  O3: plan [S,W,W,OY], PRED 1/0, CORRECT both configs
  (longer plan, same verdict). O6: plan [S,W,W,OZ], PRED 1/1,
  LOUD-FAIL (same verdict as V_full).
- V_nofrontier: IDENTICAL decision lines on O1, O2, O4, O5, O6.
  DIFFER on O3 only: anti-frontier picks Z at t*=2 over Y at
  t*=0 (TARGET V*=1 t*=2), plan [S,W,W,OZ], PRED h0=0 h1=1,
  CORRECT both configs. A different experiment, same verdict.
- V_none: DIFFER on all six worlds. Verdict flips on O1, O2,
  O4, O5 (CORRECT to LOUD-FAIL); O3 CORRECT with the
  anti-frontier plan [S,W,W,OZ]; O6 LOUD-FAIL.

## Component verdicts (frozen mechanical rule)

- C1 (clamp): verdict flips on O3 (CORRECT to SILENT-WRONG)
  and O6 (LOUD-FAIL to SILENT-WRONG) when removed alone.
  Verdict: LOAD-BEARING. Re-confirmed on OOD chain-shaped
  worlds, not just the single-hop repair family.
- C2 (t*-derived wait counts): verdict flips on O1, O2, O4, O5
  (CORRECT to LOUD-FAIL) when removed alone; the fixed w=2
  horizon cannot reach derived t* values of 3, 4, 5, 12.
  Verdict: LOAD-BEARING.
- C3 (earliest-frontier V* selection): no verdict flips; the
  only decision-line change is O3, where the anti-frontier
  builds a different but still correct experiment ([S,W,W,OZ]
  vs [S,W,OY]). Verdict: PARTIALLY-LOAD-BEARING (changes which
  experiment is built on competing-frontier worlds; does not
  change any verdict on this set).
- Joint (V_none): 4 verdict flips, equal to the worst single
  removal (V_nowaitderiv, 4). No positive interaction; the
  joint removal performs no better than its worst component.

Every claimed verdict flip above is backed by a decision-line
diff, and every decision-line diff carrying a verdict flip is
recorded. No SILENT-WRONG anywhere except the two V_noclamp
cells (O3, O6), both counted against C1.

Kill-bar check (frozen): (8a) determinism holds for every
variant x world x 3 runs: HOLD. (8b) every component received
its verdict by the mechanical rule: HOLD. (8c) the table is
faithful (checked diff-by-diff): HOLD. (8d) V_none flip count
(4) <= max single-removal flip count (4): HOLD.

## Verdict: BUILD-PASS (step 8)

The ablation ran as preregistered on decision lines. Load-bearing
vs decorative, measured: the clamp (C1) and the t*-derived wait
counts (C2) are load-bearing; earliest-frontier selection (C3)
is partially load-bearing (it changes experiment choice, not
verdicts, on this set); nothing measured here is decorative.
All predictions in the prereg materialized; no misses to report.

## Architecture accounting (ONE-SYSTEM rule)

- New hardcoded semantic cases: 0.
- New modes: 0. New bridges: 0. New handlers: 0.
- The four variants are controlled single-policy ablations of
  the frozen derivation machinery, not new machinery.
- Cognition lines added: 0 (evaluator harness only).
