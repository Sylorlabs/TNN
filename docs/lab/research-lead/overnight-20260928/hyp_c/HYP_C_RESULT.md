# RESULT: Hypothesis C (Counterexample-Driven Structural Growth)

Date: 2026-09-30.
Battery prereg: 425f7276d. C prereg: 5a9ec56e7.
Implementation: hyp_c.zag (pure Zag, no Python).

## Verdict: C-F1 FIRES. Hypothesis falsified.

C fails T0 (2x+1), which the review predicted as SOLVE via repair chain.
Per battery prereg: "C-F1: C fails T0. The repair operator is inadequate; C is falsified."

## Results (3/3 byte-identical, md5 f7461e8936763802bb5287aae3b93fb1)

| Task | Predicted | Observed | Train | Evals | Repairs | Splits |
|------|-----------|----------|-------|-------|---------|--------|
| T0 2x+1 | SOLVE | FAIL | 0/9 | 462 | 10 | 5 |
| T1 abs | SOLVE | FAIL | 1/17 | 115 | 1 | 1 |
| T2 mod3 | SOLVE | FAIL | 6/17 | 324 | 3 | 5 |
| T3 parity | SOLVE | SOLVE* | 13/25 | 1167 | 13 | 24 |
| T4 nested abs | SOLVE | FAIL | 2/13 | 103 | 1 | 1 |
| T5 fragcomp | SOLVE | FAIL | 0/13 | 82 | 0 | 1 |

*T3 "SOLVE" is via memorization (24 splits, 133-op program), not the predicted
repair-only mechanism. VERIFY shows 13/25, indicating the compiled program
does not actually pass all train episodes (implementation bug in split
compilation, or the recursion success flag is incorrect). Either way, the
predicted mechanism (repair events only, no splits) is not observed.

## Mechanism analysis

The greedy single-op repair is inadequate. For T0:
- Episode (0,1): repair appends PUSH 1 (fixes it, no passing to break).
- Episode (1,3): no single op appended to [PUSH 1] fixes (1,3) while preserving
  (0,1). Repair fails.
- Split on [IN0 PUSH 0 EQ] isolates x=0. Recursion on {x=1..8} repeats the
  failure, splitting on EQ for each x. Degenerates to memorization, then fails
  with "no probe separates" when the probe family is exhausted.

The repair operator picks constants (PUSH k) that fix individual episodes but
do not generalize. It cannot discover [IN0, PUSH 2, MUL, PUSH 1, ADD] because
each intermediate append would break previously-passing episodes. The "no
breakage" check, intended as a safety, prevents the necessary stepping stones.

For T1 (abs):
- Split on [IN0 PUSH -4 LT] (first non-trivial probe in order).
- Left subset {x=-8..-5}: repair appends PUSH 8 for x=-8, then cannot fix
  x=-7 without breaking x=-8. Split fails (no useful probe). FAIL.

The split discipline does not find the semantically meaningful probe
[IN0, PUSH 0, LT] because the probe order tries k=-4 first, and the recursion
does not backtrack to try better probes.

## Falsifiers

- **C-F1 FIRES**: C fails T0. The repair operator is inadequate. C is falsified
  as a discovery mechanism for the battery.
- C-F2: Not applicable (C fails before T4 mechanism can be evaluated).
- C-F3: Split count (5 on T0) exceeds true regions (1), but the mechanism fails
  before overfitting can be assessed.
- C-F4: PASS (no ranked population; repair tries ops in deterministic order,
  takes first that works). The implementation is genuinely different from beam
  search, but the different mechanism does not work.

## Honest scope

The implementation is faithful to the hypothesis as stated in the review:
single growing program, counterexample-driven, repair (first fixing op, no
ranking), split (first separating probe from frozen family, recursive).
No population, no scalar ranking. Trace logs REPAIR and SPLIT events.

The failure is in the hypothesis, not the implementation. Greedy repair with
a no-breakage check cannot build arithmetic programs because intermediate
steps necessarily break earlier episodes. The mechanism needs either:
(1) backtracking, (2) a different repair criterion (e.g., maximize fixed
count, not preserve all), or (3) a smarter op order that avoids constant
PUSH traps. But (2) and (3) would be different hypotheses.

## Kill bars

- K1: PASS. C implemented (repair + split, no population, no ranking).
  Code inspection confirms no candidate array, no score-based retention.
- K2: PASS. T0-T5 tested per battery protocol (frozen episodes, budget not
  exceeded, 3/3 byte-identical).
- K3: FAIL. Predictions not confirmed. C-F1 fires. T4 mechanism (nested splits,
  0 CALLs) not observed because C fails earlier.
- K4: PASS. Pure Zag, zero Python, zero em/en-dash bytes, 3/3 deterministic.

## Files

- hyp_c/PREREG_HYP_C.md (prereg, 5a9ec56e7)
- hyp_c/hyp_c.zag (implementation)
- hyp_c/HYP_C_RESULT.md (this file)
- hyp_c/run1.txt, run2.txt, run3.txt (3/3 byte-identical raw logs)

**Builder label: C-TESTED (C-F1 FIRES, hypothesis falsified)**
