# R32 E51D — Frozen Terminal Reachability Audit (Preregistered)

Date: 2026-08-29
Status before execution: `PREREGISTERED — EVALUATOR-ONLY DIAGNOSTIC`
Canonical brain: R27 at step 60,423. This audit cannot promote R32.

## Question

E51A showed that continuation cannot help when the terminal controller never
produces UNKNOWN. E51B showed a learned sequential continuation head can change
behavior but loses utility and known success. E51C produced a potentially useful
nonlinear signal, but its fresh-seed allocator saturated and invalidated the
validation result.

Before another continuation learner is built, E51D asks a narrower causal
question:

> With E50's terminal action-value head frozen exactly as trained, is a correct
> terminal action reachable at any resource-feasible stopping time on each valid
> E51B validation episode?

If the answer is no, continuation-only research is structurally incapable of
passing the every-cell gate; the next learned mechanism must change terminal and
continuation action-value geometry jointly.

## Frozen inputs

- Exact E50 source and terminal batch fit.
- UNKNOWN target and UNKNOWN-head parameters remain exactly zero.
- Exact E51B fresh development, validation, and sealed-confirmation allocation.
- Exact raw evidence, provenance, consequence, hazard, option-state, and resource
  machinery.
- Confirmation seeds are allocated but not executed.

## Audit method

For each E51B validation episode and each frozen E50 terminal model:

1. Generate every state on the 0..16 evidence tape.
2. Exclude stop times requiring an infeasible observation.
3. Ask the frozen terminal policy for its action at each reachable time.
4. Only after the action exists, use evaluator truth to record whether that stop
   would have been correct.
5. Separately compute the retrospective stop time maximizing terminal utility
   minus accumulated opportunity loss.

Evaluator truth never enters a feature, terminal score, option update, or learner
state. This is an oracle ceiling audit, not TNN capability.

## Preregistered outputs

- baseline success at t=0;
- whether any reachable time succeeds;
- success under the retrospective utility-optimal stop;
- no-unique episodes with any reachable UNKNOWN;
- known episodes with any reachable correct commit;
- never-UNKNOWN and never-correct episode counts;
- baseline versus oracle net utility;
- stop-time histogram;
- every-cell reachability gates for known and no-unique conditions.

## Decision rule

- If every episode has a reachable successful terminal action, keep the frozen
  terminal head as a control and focus the next experiment on learning the
  continuation/termination policy more selectively.
- If any episode lacks a reachable successful terminal action, stop treating
  continuation-only changes as sufficient. The next candidate must be a generic,
  learner-owned joint action-value Foundry over terminal actions and CONTINUE,
  with UNKNOWN still fixed at neutral zero and no ambiguity labels.

No quantitative threshold will be changed after execution. Negative and mixed
results are retained.
