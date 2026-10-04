# R32 E51AE — implementation contract

Date frozen: 2026-08-31  
Branch: `r32-agent-sequential-frontier`  
Scientific preregistration: `Research/R32_E51AE_TRAJECTORY_CRITICAL_CANDIDATE_RESIDUAL_PREREG.md`

This file resolves implementation details that were implicit in the preregistration without changing its treatment, targets, partitions, arms, validation gates, confirmation rule, or claim boundary. It is frozen before stage-98 validation is executed.

## Deployment interpretation

E51AE is not a new mechanism router. For deployable treatment arms, the mature E51Y/E51X slot controller remains the same competitor used by E51AC score-max. The only change is that each frozen E51AB local-384 direct candidate value is replaced by the preregistered residual-corrected value:

`Q_treatment(c,x) = Q_frozen(c,x) + R_global(c,x) + R_local(c,x)`.

The existing deterministic E51AC score-max comparison is otherwise unchanged. Direct candidates replace the frozen slot action only on a strict value win, so ties preserve the mature slot. UNKNOWN remains exactly zero and has no trainable parameter.

Arm 0 is the evaluator-only frozen slot/direct union control specified by the preregistration. Arm 4 is the evaluator-only direct-action support oracle. Neither diagnostic arm is learner-deployable or used as an inference feature.

## Critical-state margin

State selection uses candidate-side grounded success margin only:

- known state: grounded-correct candidate score minus `max(other candidate score, UNKNOWN=0)`;
- no-unique state: `0 - max(candidate 0 score, candidate 1 score, 0)`.

This preserves the preregistered candidate-value question and does not introduce a router target. DIRECT-REQUIRED selects the lowest-margin frozen-direct-success state. UNION-NEITHER-KNOWN selects the highest-margin feasible state with a grounded candidate. UNION-NEITHER-NO-UNIQUE selects the highest UNKNOWN margin, equivalent to the smallest current maximum candidate score.

## Round comparison loss

The preregistered tie-breaker “trajectory margin loss” is the sum, across UNION-NEITHER development trajectories not already separated by a positive unit margin, of squared `1 - best_candidate_success_margin`. It is used only after exact frozen-union development preservation and only when rescue count is unchanged. It never enters learner-visible state.

## Isolation

Evaluator-only support class, mode/no-unique membership, grounded candidate targets, reachability truth, stage/world identity, and validation membership are not copied into the 32 learner feature columns. Before every residual fit, evaluator target fields 34–37 are zeroed in selected training records. Residual targets are stored in separate target arrays.

No validation-dependent threshold, shift, action rule, feature, route, topology, sweep dose, replication factor, target, or stopping rule may be changed after this contract is committed.
