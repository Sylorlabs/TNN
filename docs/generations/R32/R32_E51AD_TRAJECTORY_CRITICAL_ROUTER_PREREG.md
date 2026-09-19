# R32 E51AD — Trajectory-Critical Conservative Mechanism Router

Date frozen: 2026-08-31
Branch: `r32-agent-sequential-frontier`
Canonical status: **R27 remains canonical.**

## Causal basis

E51AC established that the frozen mature slot controller and the frozen E51AB local-384 direct-candidate learner contain complementary resource-feasible support, but the best value-comparison hybrid recovered only 5,213 / 5,400 validation episodes while the evaluator-only union reached 5,260 / 5,400. The remaining 47-episode gap is a routing/calibration problem. The additional 140 known trajectories missed by the union are not addressable by routing between these fixed learners and are reserved for a separate candidate-support experiment.

E51AD therefore changes neither learner. It asks whether a learner-owned gate, trained with a whole-trajectory success-preservation objective, can recover the support already present in their fixed union without sacrificing mature competence.

## Frozen mechanism lineage

E51AD must reconstruct and freeze:

1. the exact confirmed E51Y/E51X mature `KEEP / CURRENT / RESTORE / UNKNOWN` terminal controller;
2. the exact E51AB stage-89 global plus local-384 direct `COMMIT(candidate) / UNKNOWN` learner;
3. the same evaluator-blind 32 learner-visible terminal features;
4. the same E51X learner-grown first-32-cell routing partition.

Neither frozen action learner may receive a stage-94, stage-95, or stage-96 update. Candidate identity, mechanism identity, evaluator truth, ambiguity membership, mode, resource regime, stage/world identity, validation membership, and trajectory reachability category never enter gate inference.

## Fresh partitions

- stage 94 development: 12,960 episodes / 220,320 states;
- stage 95 untouched validation: 5,400 episodes / 91,800 states;
- stage 96 sealed confirmation: 10,800 episodes / 183,600 states;
- domain-separated evaluator worlds strictly beyond E51AC stage 93;
- development, validation, and confirmation are mutually disjoint.

Confirmation executes only after a fixed learned router exactly recovers its validation union ceiling.

## Development support classes

For each development trajectory, evaluator-only analysis of resource-feasible states assigns one of three training roles:

- **PRESERVE** — the frozen mature slot controller succeeds at at least one feasible state;
- **DIRECT-ONLY** — the mature controller never succeeds, but the frozen direct learner succeeds at at least one feasible state;
- **NEITHER** — neither frozen learner succeeds before resource cutoff.

These roles construct delayed training targets only. They are never learner features. `NEITHER` trajectories are excluded from router fitting because no gate between fixed mechanisms can rescue them.

## Trajectory-critical gate objective

The gate emits one scalar from the same 32 features. At inference:

- gate score `<= 0`: preserve the mature slot action;
- gate score `> 0`: use the frozen direct action, including its neutral UNKNOWN decision;
- ties remain on the mature mechanism.

For each fitting round, select exactly one critical state per trainable trajectory:

- PRESERVE: the mature-success state with the minimum current gate score; target `-1000`;
- DIRECT-ONLY: the direct-success state with the maximum current gate score; target `+1000`.

Direct-only critical examples are deterministically replicated by `ceil(PRESERVE / DIRECT_ONLY)` so the rare rescue class is not erased by class frequency. The replication factor is derived only from the frozen development support counts and is fixed before fitting.

A global deterministic linear gate is fit first. Local residual gates then reuse the frozen first-32-cell routing partition. After every fitted gate, one scalar shift is chosen from development only: the largest shift that preserves at least one mature-success state in every PRESERVE trajectory. This monotone calibration maximizes potential direct admission subject to exact development preservation. It is not an ambiguity threshold and does not use evaluator categories at inference.

## Fixed arms

| Arm | Description |
|---|---|
| 0 | Frozen mature slot controller |
| 1 | Frozen E51AC score-max hybrid control |
| 2 | Calibrated global linear trajectory router |
| 3 | Calibrated local trajectory router, maximum 96 coordinate sweeps per fitting round |
| 4 | Calibrated local trajectory router, maximum 384 coordinate sweeps per fitting round |
| 5 | Evaluator-only union ceiling of the two frozen action learners |

Local fitting has at most four trajectory-critical rounds. A round is accepted only if exact development PRESERVE reachability remains complete and DIRECT-ONLY reachability increases, or if both reachability counts are unchanged and threshold loss decreases strictly. No post-validation arm, shift, feature, target, or stopping decision is permitted.

## Required measurements

For development, validation, and any opened confirmation partition report:

- overall, known, and no-unique resource-feasible reachability;
- time-zero success / UNKNOWN / wrong;
- reachability by mode and resource regime;
- oracle-union ceiling and each learned arm's union regret;
- PRESERVE, DIRECT-ONLY, and NEITHER counts on development;
- derived positive replication factor;
- global and local gate shifts;
- local accepted rounds, accepted updates, accepted sweeps, stop traces, threshold loss, and forward/reverse identity.

## Integrity gates

Before interpretation require:

1. E50 parent and E51Y/E51X mature terminal reconstruction pass;
2. E51AB stage-89 direct learner reconstructs with positive/negative target support, exact forward/reverse identity, and nonzero local updates;
3. stage-94/95/96 world and RNG-domain separation passes with zero assignment failures;
4. exact partition sizes and state counts;
5. at least one PRESERVE and one DIRECT-ONLY development trajectory;
6. global critical selection, parameters, bias, shift, trace, and loss are forward/reverse identical;
7. each local dose's first/final parameters, shift, accepted rounds, updates, sweeps, selection trace, fit trace, loss, and stop behavior are forward/reverse identical;
8. all calibrated router arms preserve every development PRESERVE trajectory;
9. the mature terminal hash and frozen direct parameters remain unchanged through validation;
10. UNKNOWN remains score/value zero with no learned UNKNOWN head;
11. no evaluator-only value enters the 32-feature gate input;
12. confirmation execution is zero unless a fixed learned arm exactly matches the validation union ceiling.

## Validation and confirmation gates

A learned arm 2, 3, or 4 solves the fixed-mechanism routing problem only when, with all integrity gates passing, its validation known and no-unique reachability exactly equal arm 5's evaluator-only union counts. Because every deployable choice is one of the two frozen mechanisms, equality in both categories implies zero union regret.

If multiple learned arms solve validation, select the lowest-resource arm in order 2, 3, 4. Only that frozen arm executes stage-96 confirmation. Confirmation succeeds only when the selected arm again exactly equals the fresh confirmation union in both categories.

E51AD does **not** require 5,400 / 5,400 validation reachability, because E51AC already proved that the fixed union can remain below exact. It tests routing sufficiency, not candidate-support sufficiency.

## Frozen outcomes

- `TRAJECTORY_ROUTER_COMPLEMENT_CONFIRMED` — zero union regret on validation and sealed confirmation.
- `TRAJECTORY_ROUTER_COMPLEMENT_VALIDATION_ONLY` — zero validation regret but nonzero confirmation regret.
- `TRAJECTORY_ROUTER_PARTIAL` — a learned trajectory router improves the prior score-max control but leaves positive union regret.
- `TRAJECTORY_ROUTER_NO_GAIN` — no learned router improves the prior score-max control.
- `INVALID_E51AD_INTEGRITY_FAILURE`.

A confirmed routing result would justify freezing the conservative gate and moving to a separate trajectory-critical candidate-value residual experiment for the union's remaining `NEITHER` trajectories. A partial or negative result would show that the fixed 32-feature routing geometry does not reliably separate mature-preservation states from direct-only rescue states, even though the underlying mechanisms are complementary.

No E51AD result can promote R32 or establish AGI/consciousness.
