# PREREG AMENDMENT 1: F2 OOD passive semantics and W2/W4 schedules

Date: 2026-09-30. Worker: F2 OOD Worker.
Status: FROZEN. Committed before rebuilding W2/W4.
Amends: PREREG_F2OOD.md (commit 8e795c2b9). Original predictions stand
except as noted below. Nothing is hidden; the error and fix are both recorded.

## What was wrong

During implementation I discovered that my hand-derived passive traces
assumed PERSISTENT levels (e.g. "X=1 at t=2,3,4"), but the engine
semantics give SINGLE-STEP pulses: w_passive's SET writes only the
current t slot, and the "X=0" entries I wrote are no-ops (the slot is
already 0). This matches world_a2.zag's own passive (X pulsed at t=2
and t=8 only), which I misread.

Consequences:
- W1 and W3 as built still test their structural axes (their window /
  delay dynamics respond to pulses), and their prereg predictions
  CONFIRMED on the first run. The d4-exclusion reasoning for W1 is
  corrected below; the prediction itself is unchanged.
- W2 as built gave each variable a SINGLE pulse (cnt=1 < 2), so Y got
  zero candidates for the boring reason "insufficient data", not the
  structural reason "negation unrepresentable". The design intent
  requires revision.
- W4 as built likewise gave cnt=1 per cause, so no candidates formed
  at all, and w_verify panicked indexing hysel with ne=0 (exit 1,
  slice index out of bounds in harness adjudication; the learner itself
  was unaffected).

## Corrections

### Passive semantics (applies to all four worlds)

A w_passive entry "X=1 at t=k" produces X=1 ONLY at trace step k.
Entries of the form "X=0 at t=k" are no-ops and are removed from the
schedules below.

### W1 (hysteresis): prediction stands, reasoning corrected

Effective trace: X=1 at t=1 and t=7 only. Y(t)=1 iff X in {t-1,t-2,t-3}
gives Y=1 at t=2,3,4,8,9,10. Candidates: (X->Y,d1),(X->Y,d2),(X->Y,d3);
d4 excluded because the t=1 pulse gives Y(5)=0. NHYP=3, survivor d1,
GOAL_REAL=1, post-hoc pulse falsifies survivor. All as originally
predicted. No rebuild needed.

### W2 (inhibition): revised schedule

New passive: X and Z pulsed TOGETHER at t=2 and t=6
(w_passive sets both at those steps; nothing else).
Effective trace: X=1 at t=2,6; Z=1 at t=2,6; Y always 0
(Y(3)=X(2)&!Z(2)=0; Y(7)=0).
Revised hand derivation:
- Y candidates: ZERO. X->Y d1 has cnt=2 but ok=0 (Y(3)=Y(7)=0):
  genuinely refuted by the overlap, not by cnt<2.
- X->Z: zero (d4 has cnt=2 but Z(10)=0 refutes).
- ne=0, NHYP=1, zero experiments, PLAN none found.
- Oracle witness [SX,W]: Y(1)=X(0)&!Z(0)=1. Achievable.
Revised P-W2: ne=0 (the originally predicted spurious X->Z candidate
does NOT materialize under pulse semantics; dropped), PLAN none found,
witness_goal=1. Core claim unchanged: F2 declares impossible what is
achievable, because negation is outside its vocabulary.

### W4 (disjunction): revised schedule

New passive: X pulsed at t=2 and t=5; Z pulsed at t=6 and t=9.
Effective trace: X=1 at t=2,5; Z=1 at t=6,9;
Y(t)=X(t-1)|Z(t-2) gives Y=1 at t=3,6,8,11.
Revised hand derivation:
- Y candidates: (X->Y,d1) [X events t=2,5 -> Y(3),Y(6)=1, cnt=2],
  (Z->Y,d2) [Z events t=6,9 -> Y(8),Y(11)=1, cnt=2]. Both TRUE.
- Spurious (X->Z,d4) [X events t=2,5 -> Z(6),Z(9)=1, cnt=2].
- evars=[Z,Y] (v=1 before v=2), ne=2, NHYP=2.
- First disagreement experiment [SX,W,OY] kills the hyp with
  (Z->Y,d2), a TRUE rule. Survivor's Y-rule is (X->Y,d1).
- Plan [SX,W]; GOAL_REAL=1.
Revised P-W4: survivor Y-rule=(X->Y,d1), (Z->Y,d2) killed,
GOAL_REAL=1, nhyp=2. w_verify rewritten to locate Y's position in
evars and to return REFUTED (not panic) if ne=0.

### W3 (long delay): unchanged

Effective trace was already pulses (X=1 at t=1,7); prediction
CONFIRMED on first run. No rebuild needed.

## Re-freeze

W2 and W4 will be rebuilt and run 3x AFTER this amendment commit.
W1 and W3 keep their existing binaries and first-run logs; two
additional runs each will be collected for the 3/3 determinism check.
