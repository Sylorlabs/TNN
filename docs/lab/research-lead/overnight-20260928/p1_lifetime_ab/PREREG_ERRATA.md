# PREREG ERRATA: LIFETIME-AB-1

Recorded before any run. The prereg was committed alone at `7f66e5de7`.

## E1. PREREG section 3.1: three declared answer LENGTHS were mis-annotated

The frozen value SEQUENCES were correct and are unchanged. Only the
parenthesised lengths were wrong:

| goal | prereg said | correct length |
|---|---|---|
| GA | n=18 | n=17 |
| GC | n=19 | n=20 |
| GD | n=18 | n=17 |

Recount: GA = [8,10..17] (9) + [5,10..14] (6) + [1,2] (2) = 17.
GC = 9 + 9 + 2 = 20. GD = 9 + 6 + 2 = 17.

The evaluator never compared lengths: `lt_ans_eq` compares the count cell
and then element-wise, and the oracle is asserted against the declared
SEQUENCE. No bar moved.

## E2. PREREG section 6, P3: the per-query trial count at F is 0, not 3

Preregistered P3 predicted "MAIN at F: 3 of 4 need shapes are HITS, so the
per-query trial increment at F is exactly 3."

Re-derived from the frozen source before running: `learn_bindings` guards the
whole 3-family trial loop with `if(bind_fam(L,bi)<0)`, and
`try_family` decides the family from the need's field SHAPE alone -- it never
consults the arena. The family is therefore a total function of the need
shape, so a shape whose canonical tag is already bound consumes zero trials.
At F all four need shapes (nf=2, nf=7, nf=4, nf=3) were already bound from
stages A, B and C, so the increment is 0. FRESH remains 12 (4 unbound needs
x 3 families).

This strengthens the prediction; it does not move a bar. The kill bar K4
asks only whether the lifetime learner beats fresh on trials or cost, and 0
< 12 satisfies it either way.

## E3. PREREG section 4, phase 8: the TTC target for stage H

The stage-H goal (HG) has DECLINE as its correct behaviour, so "first
correct probe" is not a meaningful examples-to-criterion measure for it.
The TTC probe at stage H targets the stage-F composition goal instead, and
this substitution is recorded in the emitted TTC line by its `goal=` field.

## E4. PREREG section 2: the lane-local chain writer

PREREG section 2 listed the additive lane code. It did not list
`lt_chain_add` / `lt_chain_clear`, which became necessary because the frozen
`chain_add` miscompiles in this translation unit (see `DEFECT.md` B16).
They are layout- and semantics-identical to the frozen pair, are documented
at their definition, and are used only on the harness side to build episode
chains. They do not touch learner state.

## E5. Preregistered predictions that were NOT tested, and why

P13 (memory occupancy non-decreasing across stages) is reported but not
adjudicated as a prediction, because `lt_cells` counts nonzero cells through
the same indexed reads that B16 corrupts. No number derived from it is
asserted.

P10 (exactly one functional-arity violation at stage G) is reported as
NOT REPRODUCED in this run. The detector and the contradicting fact are both
present in source; the observed count was 0. Because B16 corrupts the
same class of read that the coverage dump uses to diagnose it, this is
recorded as unresolved rather than as a refuted prediction.