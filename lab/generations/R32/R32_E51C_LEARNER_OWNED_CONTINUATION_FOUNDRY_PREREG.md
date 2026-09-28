# R32 E51C — Learner-Owned Sparse Continuation Foundry

Date: 2026-08-29
Status: `PREREGISTERED_NATIVE_DISCRIMINATOR — NOT YET EXECUTED`
Canonical: R27 step 60,423
Parent evidence: E50 valid native negative, E51A valid native diagnostic negative, E51B valid native sequential negative

## Why this experiment

E51B established that learned continuation value has causal leverage: in fresh native validation it reduced no-unique wrong commitments by 68 in the primary M0 model and 72 in M1. But the single linear continuation head spent excessive observation cost and reduced known-case success, so net utility and non-inferiority failed.

Do not respond by hand-writing a new ambiguity feature or tuning a threshold. E51C tests whether the remaining problem is **learner-owned approximation/selectivity**.

## Causal question

> Can TNN use delayed utility/regret on development experience to construct a sparse nonlinear continuation head from generic composition primitives, then improve fresh validation safety and utility without researcher selection of the resulting feature topology?

## Frozen parent

- E50 deterministic M0 batch terminal controller is the primary terminal policy.
- UNKNOWN remains neutral grounded no-commit value `0`.
- E51B continuation target remains the delayed grounded advantage of one more feasible observation plus optimal later stopping versus terminating now, including actual observation/opportunity loss.
- No evaluator mode, truth, ambiguity label, seed identity, answer key, remaining horizon or fixed observation count is a policy feature.

## Generic Foundry substrate

The protected substrate supplies only one new generic composition primitive in E51C:

`interaction(i,j) = clamp(feature_i * feature_j / scale)`

This is not a domain/ambiguity feature. Candidate indices are chosen from the existing evaluator-blind continuation state. Human code supplies arithmetic, deterministic search, a small resource ceiling and rollback. TNN/development utility selects:

- which feature pair to connect;
- the sign and magnitude of its coefficient;
- whether the candidate strictly reduces development squared continuation-value error;
- whether to accept another interaction or stop.

Maximum accepted interaction count is **4** as a protected resource ceiling, not a target. The learner may stop earlier when no strict development improvement remains.

## Search discipline

For each stage:

1. compute residual continuation-value error under the current head on the fresh development ledger;
2. enumerate all distinct feature pairs from the generic state vector, excluding already-selected duplicate topology;
3. fit a deterministic one-dimensional coefficient from development residual correlation/energy;
4. choose the candidate with the best deterministic estimated gain;
5. execute an exact development loss check;
6. accept only on strict loss reduction, otherwise stop Foundry growth.

Run the complete search in forward and reverse development-record traversal. Selected pair topology, coefficients, accepted count and final development loss must be identical.

The sealed validation set is never used to choose topology, coefficient, interaction count or stopping.

## Fresh seed discipline

E51C first deterministically reserves the exact E51B stage-24/25/26 effective streams so they cannot be reused, then allocates new collision-checked streams:

- stage 27: development — 3,240 episodes / 55,080 time records;
- stage 28: validation — 5,400 episodes;
- stage 29: sealed confirmation — 10,800 episodes allocated but not executed unless validation earns it.

All streams remain disjoint from E46–E51B through the existing raw/evidence/resource seed collision checker.

## Validation arms

On the same fresh E51C validation episodes compare:

1. frozen E50 M0 terminal-only control;
2. fresh E51C linear continuation head using the same target but no Foundry interactions;
3. the frozen learner-selected sparse Foundry continuation head.

Runtime CONTINUE occurs only when predicted grounded continuation advantage is positive and another observation is feasible. Zero remains the sign boundary of a learned utility difference; it is not a tuned confidence threshold.

## Required reporting

- seed reservation/allocation and collision gates;
- base linear forward/reverse fitting identity;
- Foundry forward/reverse topology/parameter identity;
- selected pair indices and coefficients;
- accepted Foundry interaction count;
- development base and final loss;
- positive/negative/zero target support;
- terminal / linear / Foundry aggregate success, UNKNOWN, wrong commits, known success/wrong, no-unique UNKNOWN/wrong;
- observation count and opportunity loss;
- grounded net utility;
- stop-time distribution;
- every-cell no-unique Foundry safety;
- confirmation earned/executed status.

## Validation success gate

E51C earns sealed confirmation only if all integrity/determinism gates pass and the Foundry arm:

1. is non-degenerate (not always stop or always continue);
2. has higher grounded net utility than both terminal-only and linear-continuation controls;
3. does not increase no-unique wrong commitments versus either control;
4. preserves or improves known success versus terminal-only control;
5. does not increase known wrong commits versus terminal-only control;
6. passes the preregistered every-cell no-unique safety gate.

A failure remains a valid architecture negative. A validation pass only earns sealed confirmation; it does not promote R32 or change canonical status.
