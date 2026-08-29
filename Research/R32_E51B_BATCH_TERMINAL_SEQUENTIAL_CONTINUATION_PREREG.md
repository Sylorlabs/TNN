# R32 E51B — Batch Terminal + Sequential Continuation Advantage

Date: 2026-08-29
Status: `PREREGISTERED_NATIVE_DISCRIMINATOR — NOT YET EXECUTED`
Canonical: R27 step 60,423
Parent evidence: valid E50 native negative + E51 action-value geometry audit + valid E51A diagnostic negative

## Causal question

E51A showed that repairing continuation learning inside the historical E45 sequential controller cannot help while its terminal head still makes a wrong commitment in every no-unique validation cell. E50's deterministic batch terminal learner is materially safer: it creates a real UNKNOWN region and sharply reduces known wrong commitments, although it still fails every-cell no-unique safety.

E51B asks one bounded question:

> When the safer E50 terminal action values are frozen, can a separately learned continuation advantage use additional grounded evidence only when its delayed utility exceeds terminating now, without sacrificing no-unique safety or known-resolution performance?

## Architecture

The terminal controller is frozen from E50. UNKNOWN remains the fixed grounded no-commit value `0`; no positive UNKNOWN target is introduced.

A new CONTINUE head predicts:

`A_continue(t) = delayed return from one more observation and optimal later stopping - delayed utility of terminating now`

Training targets are generated from complete development trajectories using only evaluator-side delayed grounded utility/regret and actual observation/opportunity cost. Evaluator mode, truth, ambiguity labels, seed IDs, answer keys, remaining horizon, and fixed observation counts are not policy inputs.

The runtime rule is simply:

- if no further observation is feasible, terminate;
- otherwise CONTINUE iff the learned continuation advantage is positive;
- if not, execute the highest-valued frozen terminal action.

The zero boundary is not a tuned confidence threshold: it is the sign of a learned utility difference in the same grounded units used to construct the target.

## Models

Two paired terminal representations are retained from E50:

- M0: E50 matched batch joint control (co-viability + contradiction co-mass);
- M1: E50 provenance/temporal-contention treatment.

Each receives its own continuation advantage target because its frozen terminal choices define a different terminate-now return.

Primary comparison:

1. frozen E50 terminal-only behavior;
2. frozen E50 terminal behavior + learned sequential CONTINUE.

The E50 M0 control is the primary safety reference because E50 M1 had slightly worse no-unique wrong commitments.

## Fresh seed discipline

E51B allocates new effective development, validation, and sealed-confirmation streams only after all E46–E50 effective streams and E50 sealed confirmation streams are already reserved. Allocation uses the existing effective raw/evidence/resource collision checker.

- development: 3,240 episodes / 55,080 time records;
- validation: 5,400 episodes, 20 observations per base/mode/resource cell;
- confirmation: 10,800 episodes allocated and sealed, not executed unless validation earns it.

No E50 validation or confirmation item may be used to fit the continuation head.

## Fit discipline

The continuation head uses the same deterministic complete-dataset integer batch-fitting machinery as E50. Forward and reverse sufficient statistics and fitted parameters must be identical. This avoids making presentation order another hidden causal variable.

## Required validation reporting

For each model report at minimum:

- episodes;
- correct terminal outcomes;
- UNKNOWN terminal outcomes;
- wrong commitments;
- mean observations;
- observation/opportunity cost;
- aggregate grounded utility;
- no-unique UNKNOWN and wrong-commit rates;
- every-cell no-unique safety;
- known-resolution correctness/wrong-commit metrics;
- fraction of episodes that continue at least once;
- stop-time distribution;
- continuation target interior variation;
- continuation parameter nonzero count;
- deterministic forward/reverse fitting gates.

## Success gate

E51B does not earn confirmation merely by increasing average utility. A candidate must simultaneously:

1. pass source/integrity/seed-disjointness/determinism gates;
2. not worsen the E50 terminal-only no-unique wrong-commit count;
3. improve no-unique UNKNOWN or every-cell safety materially;
4. preserve known-resolution success and wrong-commit performance within preregistered non-inferiority margins;
5. show nontrivial learned continuation behavior rather than always-stop or always-continue collapse;
6. reduce delayed regret or improve grounded utility net of observation cost.

Even a validation PASS is not promotion. It only earns execution of the already allocated sealed confirmation stream and then a fresh R27-vs-R32 qualification battery.

## Disallowed rescue tactics

- positive UNKNOWN reward without independently observed delayed utility;
- evaluator ambiguity labels in learner state or targets as a class label;
- mode/truth/seed/resource identifiers in policy inputs;
- fixed `N` observations;
- confidence cutoffs tuned after validation;
- hard-coded mode-specific routing;
- changing the world generator or scoring rules after seeing results;
- treating a validation win as canonical promotion.
