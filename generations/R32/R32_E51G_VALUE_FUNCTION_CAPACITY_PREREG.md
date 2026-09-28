# R32 E51G — Matched Value-Function Capacity Discriminator

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Question

E51F established that the learner-visible sequential terminal states are exactly distinguishable on fresh validation data. E51G therefore asks whether the remaining E51E reachability failures are caused by insufficient value-function capacity/generalization rather than missing state information.

## Constraints

- Full native Zag v2 only on the promotable path.
- Same learner-visible terminal state for all arms.
- Same grounded terminal utilities for all arms.
- UNKNOWN target remains exactly zero; UNKNOWN is not trained as an ambiguity class.
- Evaluator truth, ambiguity membership, stage membership, seed identity, resource label, and hidden labels are never learner inputs.
- No connection-topology rewrite in this experiment.
- No graph-like representation is privileged.
- Development selects all nonlinear additions. Validation is untouched by structure selection.
- No sealed confirmation unless an arm passes every preregistered validation gate.
- R27 is immutable control and remains canonical regardless of result.

## Fresh partitions

Use the existing evaluator-only fresh-seed allocator with new experiment domains:

- stage 34: development, 3,240 episodes / 55,080 sequential terminal states;
- stage 35: validation, 5,400 episodes / 91,800 sequential terminal states;
- stage 36: sealed confirmation, 10,800 episodes allocated but not executed unless every validation gate passes.

Within E51G every arm sees exactly the same development states, validation states, and grounded action utilities. The within-run linear arm is the matched control. E51E's historical 75/1,200 no-unique reachability veto is context, not a substitute for the fresh matched control.

## Primary representation

Use the E51E primary terminal representation only: the existing evaluator-blind 32-feature E45/E47 terminal state, including the grounded co-viability and support/contradiction co-mass coordinates already present in E51E. Do not add a hand-authored ambiguity feature.

## Matched arms

### A — linear terminal value head

Reproduce the E51E sequential terminal refit with the existing order-invariant integer batch fitter. Four grounded terminal action-value heads compete: KEEP, CURRENT, RESTORE, UNKNOWN. UNKNOWN targets remain zero and therefore may win only when learned commitment values do not exceed it.

### B — learner-selected sparse pairwise residual Foundry

Start from arm A. For each action, permit at most four accepted generic pairwise residual terms. A candidate term is the bounded product of two existing learner-visible features. At each growth step the learner searches all unordered feature pairs, estimates the residual-improving coefficient from development sufficient statistics, and accepts a term only if it strictly reduces full development squared error. Pair identity, coefficient, and stopping point are selected by development evidence; the researcher selects none of them.

This is deliberately **not** a repeat of E49. E49 tested one researcher-specified grounded conjunction (`slot3 × slot5`) inserted into one fixed terminal coordinate under the older E48 batch geometry. E51G-B instead searches the complete generic pair set on E51E sequential states, may recruit different pairs for different actions, starts from the E51E linear refit, and has a bounded learner-owned residual growth process.

### C — learner-selected sparse piecewise residual Foundry

Start from arm A. For each feature, compute its development mean from learner-visible states only. Candidate residual bases are the two generic one-sided hinges around that data-derived mean: positive deviation and negative deviation. For each action, permit at most four accepted bases. Feature identity, direction, coefficient, and stopping point are selected only by development residual improvement. The mean is not a confidence or ambiguity threshold; it is an unlabeled statistic of the input coordinate used to define a generic piecewise basis.

## Determinism and integrity

Before interpreting validation require:

1. E50 parent integrity passes;
2. exactly 19,440 E51G seed entries are allocated with zero assignment failures and confirmation execution remains zero;
3. development record count is exactly 55,080 and every UNKNOWN target is zero;
4. arm A's batch sufficient statistics and final parameters are identical under forward/reverse traversal;
5. B and C independently reproduce identical selected structures, coefficients, accepted counts, final losses, and trace hashes under forward/reverse development traversal;
6. any reported nonlinear arm is nondegenerate: at least one nonzero development-selected addition for a commit action, while UNKNOWN receives no positive warrant;
7. evaluator truth or ambiguity labels are absent from learner inputs and selection helpers.

## Primary validation gates

For an eligible nonlinear arm:

1. known-episode terminal reachability must remain **4,200 / 4,200**;
2. no-unique episodes with reachable UNKNOWN must exceed the fresh matched arm-A result and beat the historical E51E baseline of **1,125 / 1,200**;
3. no-unique episodes with no reachable UNKNOWN must therefore be below both the fresh arm-A veto and the historical **75 / 1,200** veto;
4. exact promotion to the next sequential-policy experiment requires **1,200 / 1,200** no-unique reachability while preserving **4,200 / 4,200** known reachability;
5. sealed confirmation remains untouched unless gate 4 is met.

If more than one nonlinear arm reaches the exact gate, choose the lower-resource arm first; ties use fewer accepted terms, then arm order B before C. This tie rule is fixed before validation.

## Frozen outcomes

- `VALUE_CAPACITY_REACHABILITY_RESCUE`: at least one nonlinear arm reaches exact 4,200/4,200 known and 1,200/1,200 no-unique reachability with all integrity gates passing.
- `VALUE_CAPACITY_PARTIAL_RESCUE`: at least one nonlinear arm beats both the fresh linear control and historical no-unique veto but does not reach the exact gate.
- `NO_TESTED_VALUE_CAPACITY_RESCUE`: neither nonlinear arm beats the matched linear control on the preregistered reachability objective.
- any integrity failure: invalid experiment; no capability interpretation.

If exact reachability is rescued, the next experiment may evaluate the direct five-way KEEP/CURRENT/RESTORE/CONTINUE/UNKNOWN sequential policy using the frozen winning terminal head. If exact reachability is not rescued, the next experiment must diagnose the remaining approximation geometry before any topology rewrite.

## Interpretation boundary

A positive result would show that the needed information was present in the existing learner-visible state and the prior value mapping was too restrictive. It would not show that graphs are superior, that R32 beats R27, or that AGI/consciousness has been demonstrated.
