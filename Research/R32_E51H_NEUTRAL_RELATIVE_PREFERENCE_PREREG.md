# R32 E51H — Neutral-Relative Terminal Preference Discriminator

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Why E51H exists

E51F found zero exact aliases in the learner-visible sequential terminal state. E51G then gave two learner-selected nonlinear value families more capacity on that same state, yet neither removed the terminal reachability veto. The data-mean hinge arm improved no-unique reachability while regressing known reachability, reproducing the abstention-versus-resolution tradeoff.

E51H tests whether the remaining bottleneck is therefore the **training objective/decision geometry** rather than missing information or modest function capacity.

## Constraints

- Native Zag v2 only.
- Same primary E51E/E51G 32-feature terminal state for every arm.
- Same grounded terminal consequences generate all development supervision.
- Evaluator truth, ambiguity membership, seed identity, stage identity, and hidden labels are never learner inputs.
- UNKNOWN remains a neutral action with score/target exactly zero. No positive UNKNOWN classifier is trained.
- No topology changes, graph privilege, task-specific confidence threshold, ambiguity detector, or hand-selected feature pair.
- Development chooses all nonlinear residual additions.
- Validation is untouched by training/structure selection.
- Confirmation is sealed unless an exact validation gate passes.

## Fresh partitions

Use evaluator-only seed domains:

- stage 37: development, 3,240 episodes / 55,080 sequential states;
- stage 38: validation, 5,400 episodes / 91,800 sequential states;
- stage 39: confirmation, 10,800 episodes allocated but not executed unless exact validation succeeds.

All arms use exactly the same states and validation worlds within E51H.

## Arms

### A — absolute-utility linear control

Fit the existing order-invariant linear terminal value heads to the original grounded utilities, matching the E51E/E51G regression objective.

### B — neutral-relative preference linear head

For KEEP, CURRENT, and RESTORE, convert the grounded development utility to its sign relative to neutral UNKNOWN:

- positive grounded utility -> +1000 preference target;
- negative grounded utility -> -1000 preference target;
- zero grounded utility -> 0.

UNKNOWN target remains exactly 0.

This is not an ambiguity label. It is the generic decision question already implied by the action-value geometry: is committing with this action better or worse than taking the neutral no-commit action? The zero boundary is grounded neutral utility, not a researcher-chosen confidence threshold.

Fit the same order-invariant linear machinery to these neutral-relative targets.

### C — neutral-relative preference + learner-selected hinge residual Foundry

Start from arm B and permit at most four accepted generic data-mean hinge residual bases per commit action, using the same learner-owned mechanism preregistered in E51G-C. Feature, direction, coefficient, and stopping point are selected only by strict development loss improvement. UNKNOWN receives no residual terms.

## Integrity gates

Before interpreting validation require:

1. E50 parent integrity passes;
2. exactly 19,440 fresh E51H seeds allocated with zero assignment failures; confirmation execution remains zero;
3. exactly 55,080 development states;
4. UNKNOWN target nonzero count is zero in both absolute and preference records;
5. preference targets contain both positive and negative support for commit actions;
6. A and B each reproduce identical sufficient statistics/final parameters under forward/reverse training traversal;
7. C reproduces identical data means, selected structure, coefficients, accepted counts, final loss, and trace under forward/reverse traversal;
8. UNKNOWN has zero learned parameters in A/B and zero residual terms in C;
9. C is nondegenerate for at least one commit action.

## Validation gates

Report known and no-unique episode reachability for all arms. Exact objective rescue requires:

- known reachability = 4,200 / 4,200;
- no-unique UNKNOWN reachability = 1,200 / 1,200;
- all integrity gates pass.

A partial objective rescue requires an experimental arm to dominate the matched absolute-utility control on no-unique reachability without reducing known reachability, and to beat the historical E51E no-unique result of 1,125/1,200.

Confirmation remains sealed unless the exact gate passes.

## Frozen outcomes

- `NEUTRAL_RELATIVE_OBJECTIVE_RESCUE`: B or C reaches the exact gate.
- `NEUTRAL_RELATIVE_OBJECTIVE_PARTIAL_RESCUE`: B or C strictly improves the matched reachability frontier without exact rescue.
- `NO_TESTED_OBJECTIVE_RESCUE`: neither B nor C improves the preregistered frontier.
- integrity failure: invalid experiment, no capability interpretation.

If exact rescue occurs, the next experiment may evaluate the direct five-way KEEP/CURRENT/RESTORE/CONTINUE/UNKNOWN sequential controller using the frozen winning terminal head. If exact rescue does not occur, E51I must characterize the remaining failure margins/local geometry before any topology rewrite.

No E51H result can by itself promote R32 or establish AGI.
