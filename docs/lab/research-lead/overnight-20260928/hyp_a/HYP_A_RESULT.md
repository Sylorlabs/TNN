# RESULT: Hypothesis A Implementation (Residual-Driven Construction)

Date: 2026-09-30.
Status: COMPLETE. Builder verdict: BUILD-FAIL.
Prereg: 58c2cc66b (strict ancestor, verified).
Battery: 425f7276d. VM frozen as in 8d5f58b89.

## Summary

Hypothesis A implemented as preregistered. Tested on T0-T5.
Result: FAIL on all six tasks. A-F1 fires: A fails T0 (2x+1) and T2 (mod3).
The residual complexity driver is inadequate. Hypothesis A is falsified.

## Implementation

File: `hyp_a.zag` (pure Zag, compiles with znc 2026.07.0-dev).
Binary: `hyp_a_bin` (native, 44968 bytes).

Mechanism (per prereg section 1):
- Single program P, residual R where r_i = t_i - o_i.
- Loop: if R all zeros, SUCCESS. If R constant c, forced PUSH c, ADD.
  Else try all 31 ops in deterministic order, pick minimal complexity.
  Complexity = distinct_count * 1000000 + range.
- No population, no score ranking. Single trajectory.

## Results (3/3 byte-identical, md5 bc0c12e4518aea6a77b679cb05ff94f9)

| Task | Predicted | Observed | Exact | Evals | Program |
|------|-----------|----------|-------|-------|---------|
| T0 2x+1 | SOLVE | FAIL | 0/9 | 62 | [IN0] |
| T1 abs | FAIL | FAIL | 1/17 | 31 | [] |
| T2 mod3 | SOLVE | FAIL | 6/17 | 31 | [] |
| T3 parity | SOLVE | FAIL | 12/25 | 31 | [] |
| T4 nested | FAIL | FAIL | 2/13 | 31 | [] |
| T5 fragcomp | FAIL | FAIL | 0/13 | 31 | [] |

All runs: exit 0, zero stderr, 3/3 byte-identical.

## Trace analysis (T0)

STEP 0: P=[], R=[1,3,5,7,9,11,13,15,17], complexity=9000016.
  Best op: IN0 (new complexity 9000008). All other ops worse or tie.
STEP 1: P=[IN0], R=[1,2,3,4,5,6,7,8,9], complexity=9000008.
  No op reduces complexity. FAIL.

The algorithm gets stuck after [IN0]. To reach the predicted
[IN0, PUSH 2, MUL], it would need to append PUSH 2, but:
  P=[IN0, PUSH 2] gives output=2, R=[-1,1,3,5,7,9,11,13,15],
  complexity=9000016, which is WORSE than 9000008.

The greedy single-op selection cannot traverse the 2-step dependency
where the intermediate (PUSH 2) increases residual complexity before
MUL makes it constant. The "constant residual" signal is unreachable
via monotonic complexity reduction.

## Trace analysis (T2)

STEP 0: P=[], R=[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1], complexity=3000002.
  No op reduces complexity. FAIL immediately.

The empty program already achieves the minimal complexity (3 distinct
values, range 2). No single op can improve it. The predicted
[IN0, PUSH 3, MOD] requires IN0 first, but IN0 makes R worse
(complexity 6000015). The algorithm cannot start.

## Falsification

A-F1 FIRES: A fails T0 and T2. Both have clean constant-seeking
residual decompositions per the review, but the greedy mechanism
cannot find them. The residual complexity driver is inadequate.

A-F2 does NOT fire: the trace shows single-op evaluation, not a
ranked population of programs. The mechanism is genuinely different
from beam search; it is simply ineffective.

A-F3 does NOT fire: A does not solve T1.

## Honest assessment

Hypothesis A is falsified as a discovery mechanism for the battery.
The core flaw: residual complexity is not monotonically reducible by
single-op appends. Multi-step transformations (like PUSH 2 then MUL)
require traversing intermediate states with worse residuals, which
greedy selection forbids.

This does not falsify the review's assessment that discovery (not VM)
is the defect. Hypotheses B, C, D remain to be tested.

## Kill bars

- K1: PASS. A implemented per prereg (residual-driven, no population).
- K2: PASS. T0-T5 tested per battery protocol.
- K3: FAIL. Predictions not confirmed; A-F1 falsifies A.
- K4: PASS. Pure Zag, zero Python, zero em dashes, 3/3 deterministic.

Builder verdict: BUILD-FAIL (K3 fails; A-F1 fires).

## Files

- `PREREG_HYPA.md` (prereg, 58c2cc66b)
- `hyp_a.zag` (implementation)
- `HYP_A_RESULT.md` (this file)
- `HYP_A_RAW_1.txt`, `HYP_A_RAW_2.txt`, `HYP_A_RAW_3.txt` (raw logs)
- `HYP_A_RAW_1.err`, `HYP_A_RAW_2.err`, `HYP_A_RAW_3.err` (empty)
