# PREREG: Hypothesis A Implementation (Residual-Driven Construction)

Date: 2026-09-30.
Status: FROZEN PREREGISTRATION. No implementation is authorized by this document.
Authority: implements hypothesis A from `arch_review/ARCHITECTURE_REVIEW.md` (18be93c3e)
  against the frozen battery `discovery_battery/PREREG_BATTERY.md` (425f7276d).

## 0. Commit order

This prereg commit strictly precedes the implementation commit.
Verified by `git merge-base --is-ancestor` before results are accepted.
Battery prereg 425f7276d is a strict ancestor (inherited from repo state).

## 1. Mechanism specification (K1)

Hypothesis A: residual-driven construction. Single growing program P plus
explicit residual object R. No population, no score ranking, no beam.

Definitions:
- Program P is a linear (op, arg) sequence over the frozen GENEXEC2 VM
  (opcodes 0..12 for construction; 0=PUSH, 1=IN0, 2=IN1, 3=ADD, 4=SUB,
  5=MUL, 6=DIV, 7=MOD, 8=NEG, 9=DUP, 10=DROP, 11=SWAP, 12=OVER).
- For train episode i with inputs (x_i, y_i) and target t_i, run P to get
  output o_i (top of stack, or 0 if P empty). Residual r_i = t_i - o_i.
- Residual object R is the vector [r_0, ..., r_{n-1}] over all train episodes.

Construction loop:
1. Initialize P as empty. R is the target vector (o_i = 0 for all i).
2. If all r_i == 0: SUCCESS. Return P.
3. If R is constant (all r_i == c, c != 0): append PUSH c, then APPEND ADD.
   This is a forced move dictated by the residual, not a choice.
   (Justification: t_i = o_i + c for all i, so ADD of pushed c completes.)
   Continue to step 2.
4. Otherwise: consider each op in deterministic order (see section 2).
   For each op, tentatively append to P, compute R', compute complexity(R').
   Choose the op with minimal complexity. Ties broken by earliest in order.
   If the best op does not strictly reduce complexity vs current R: FAIL.
   Append the chosen op to P. Log the residual vector and chosen op.
   Continue to step 2.
5. Budget: 1M candidate evaluations or 300s per task (per battery prereg).
   One candidate evaluation = one tentative op append scored on full train set.

Complexity measure (generic, not task-specific):
- If R constant: complexity = 0 (handled by step 3, not reached here).
- Else: complexity = distinct_count * 1000000 + range.
  - distinct_count = number of distinct values in R.
  - range = max(R) - min(R).
  - Lexicographic: fewer distinct values dominates; range breaks ties.
- This is a generic simplicity bias, not a task-specific score.
  It does not rank programs by output match; it measures residual structure.

Deterministic op order (section 2):
- PUSH(c) for c in -9..9 in increasing order (19 ops).
- Then IN0, IN1, ADD, SUB, MUL, DIV, MOD, NEG, DUP, DROP, SWAP, OVER (12 ops).
- Total 31 candidate ops per step. Fixed order, no randomization.

What counts as a "candidate evaluation": each tentative single-op append
executed against the full train episode set to compute R'. The forced
PUSH c, ADD in step 3 counts as 0 evaluations (dictated, not searched).

Trace mandatory events (per battery section 5):
- Per construction step: log the residual vector (all r_i), the chosen op,
  and the resulting complexity.
- For T0: the step choosing PUSH 1 then ADD must show constant residual [1,...,1].
- No ranked population of candidate programs anywhere in the trace.
  (We evaluate ops, not programs; we keep one program, not K.)

## 2. Predictions (K3)

From the review discrimination matrix and section 5 confirmation rule:

- T0 2x+1: predicted SOLVE. Program should be [IN0, PUSH 2, MUL, PUSH 1, ADD].
  Mechanism: constant residual of 1 after [IN0, PUSH 2, MUL] dictates PUSH 1, ADD.
- T1 abs: predicted FAIL. Trace must show failure report with sign-partitioned
  residual (diagnosis). No straight-line op sequence makes R constant or zero.
- T2 mod3: predicted SOLVE. [IN0, PUSH 3, MOD] drives R to zero.
- T3 parity: predicted SOLVE. Residual over joint input (a,b);
  [IN0, IN1, ADD, PUSH 2, MOD] drives R to zero.
- T4 nested abs: predicted FAIL standalone.
- T5 fragment composition: predicted FAIL standalone.
- T6 adversary: conditional (evaluated after seal; not in this wave).

Confirmation requires outcome match AND mechanism trace (battery section 5).
Outcome without the mandatory trace events is UNCONFIRMED.

## 3. Falsifiers (frozen from review)

- A-F1: A fails T0 or T2. The residual complexity driver is inadequate.
- A-F2: trace shows multiple candidate programs ranked by residual score.
  A collapses into the banned beam class.
- A-F3: A solves T1 straight-line. Investigate: VM flaw or smuggled conditional.

## 4. Kill bars

- K1: A implemented per section 1 (residual-driven, single program, no population).
- K2: T0-T5 tested per frozen battery protocol (episodes, budget, determinism).
- K3: predictions evaluated per section 2 (CONFIRMED / UNCONFIRMED / falsified).
- K4: pure Zag, zero Python, zero em dashes, 3/3 byte-identical runs.

## 5. Governance

- Pure Zag for implementation, harness, and analysis. No Python anywhere.
- No threshold weakening after results.
- This document contains no em dashes (verified by byte grep before commit).
- Builder reports BUILD-PASS or BUILD-FAIL against K1-K4.
- Battery confirmation evaluated separately under battery section 5.
