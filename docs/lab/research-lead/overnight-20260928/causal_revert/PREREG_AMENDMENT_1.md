# AMENDMENT 1 to PREREG_CAUSAL_REVERT.md

Date: 2026-09-30 UTC
Status: FROZEN AMENDMENT. Committed alone before the final verification runs.

## What is corrected

Section 5, R2 REBUILD frozen predictions. The original hand-count for the
fresh constructor on E1p was wrong: it listed 1 class {(Y:2,Z:INF)} with
rounds=0, but the frozen vocabulary (78 graphs) and frozen evidence E1p
((Y,1)=0,(Y,2)=1,(Z,2)=0) actually yield 3 behavioral classes.

## Corrected predictions (R2 REBUILD)

- P0: unchanged. Winner [(X->Y,1)], rounds=1.
- P1p: fresh from E1p: 9 graphs, 3 classes {(Y:2,Z:INF),(Y:2,Z:3),(Y:2,Z:4)};
  reps [(X->Y,2)], [(X->Y,2),(Y->Z,1)], [(X->Y,2),(Y->Z,2)].
  ROUND 1: TARGET V*=2 t*=3, PLAN [S,W,W,W,O(2)], EXEC real=0,
  ELIM [(X->Y,2),(Y->Z,1)] sig=(2,3).
  ROUND 2: TARGET V*=2 t*=4, PLAN [S,W,W,W,W,O(2)], EXEC real=0,
  ELIM [(X->Y,2),(Y->Z,2)] sig=(2,4).
  Winner [(X->Y,2)], rounds=2.
- P2p: same as P1p. Winner [(X->Y,2)], rounds=2.
- SUMMARY R2 REBUILD: ok=3/3, correct=3/3, rounds_total=5,
  W2eqW0=0, W2eqW1=1, W2neqW0=1.

## Why the original was wrong

The hand-count missed the two-rule graphs [(X->Y,2),(Y->Z,1)] (Y arr 2,
Z arr 3) and [(X->Y,2),(Y->Z,2)] (Y arr 2, Z arr 4), both consistent
with E1p. The implementation's 78-graph enumerator (frozen vocabulary)
finds them; the error was in the manual prediction, not the code.

## What is NOT changed

- R2 REVISE predictions are unchanged and correct: the k=1 neighborhood
  of W0=[(X->Y,1)] contains only [(X->Y,2)] consistent with E1p, so
  REVISE P1p still yields 1 class and rounds=0. The amendment affects
  only the REBUILD (full-constructor) path.
- All other frozen predictions (R1 REVISE/REBUILD/FROZEN, R2 REVISE,
  R2 FROZEN) are unchanged.
- Kill bars K1/K2/K3 are unchanged. K2 now checks against the corrected
  R2 REBUILD predictions above.

## Transparency note

This amendment was written after the implementation ran once during
debugging and revealed the hand-count error. The original prereg commit
c09afd95e remains in history. The implementation code was not changed
to fit the predictions; the predictions were corrected to match what
the frozen vocabulary and evidence definitions actually entail.
