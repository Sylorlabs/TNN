# R32 E51AD — Trajectory-Critical Hybrid Router

Date frozen: 2026-08-31
Branch: `r32-agent-sequential-frontier`
Canonical status: **R27 remains canonical.**

## Causal basis

E51AC established a real but incomplete complement between two frozen terminal mechanisms on untouched stage-92 worlds:

- mature slot controller: 5,156 / 5,400 resource-feasible reachable episodes;
- frozen local-384 direct-candidate controller: complementary support on 98 known and 6 no-unique trajectories missed by the mature controller;
- evaluator-only union: 5,260 / 5,400, including 4,060 / 4,200 known and 1,200 / 1,200 no-unique;
- 140 known trajectories remained unreachable by either mechanism.

The smallest isolated next question is whether a learner-owned router can realize the measured complement while preserving mature competence. E51AD does **not** change either terminal mechanism. It learns only which frozen mechanism to admit at each learner-visible state.

## Frozen mechanism lineage

E51AD reconstructs and freezes:

1. the confirmed E51Y/E51X mature `KEEP / CURRENT / RESTORE / UNKNOWN` terminal controller;
2. the E51AB local-384 direct-candidate controller, including its frozen global candidate heads, first-32-cell routing partition, and candidate-local residual weights.

Neither mechanism is updated from E51AD development, validation, or confirmation worlds. The mature terminal hash must remain identical before and after every partition.

## Fresh partitions

Use domain-separated E51N world transport:

- stage 94 development: 12,960 episodes / 220,320 sequential states;
- stage 95 untouched validation: 5,400 episodes / 91,800 states;
- stage 96 sealed confirmation: 10,800 episodes / 183,600 states.

Stages 94–96 must be disjoint from the complete prior namespace through E51AC stage 93. Confirmation executes only after an exact deployable validation pass.

## Router state and target

The router sees only the same 32 evaluator-blind terminal features already available to both frozen mechanisms. It does not receive evaluator truth, ambiguity membership, mode, resource regime, stage/world identity, reachability category, or validation membership.

At a development state, evaluator-only grounded success determines a delayed mechanism-admission target:

- `+1000` when the direct-candidate mechanism succeeds and the mature mechanism does not;
- `-1000` when the mature mechanism succeeds, including states where both mechanisms succeed so mature competence remains the default;
- `0` when neither frozen mechanism succeeds.

These targets supervise only the router. They are not inference features and do not alter UNKNOWN, candidate values, slot values, belief transitions, or topology.

The deployable decision rule is fixed: choose the direct-candidate mechanism only when router score is strictly positive; otherwise preserve the mature mechanism. A direct-mechanism decision may itself return neutral UNKNOWN. Ties therefore preserve the mature controller.

## Matched arms

### Arm 0 — frozen mature control

Use the mature slot controller unchanged.

### Arm 1 — global linear router

Fit one deterministic linear router from the 32 learner-visible features and the fixed mechanism-admission targets.

### Arm 2 — local state-loss router

Start from Arm 1. Reuse the frozen first-32-cell learner-grown routing partition and fit one independent local residual router per cell for at most 384 coordinate sweeps under state-level squared target loss.

### Arm 3 — local trajectory-critical router

Start from Arm 2. Iteratively select, for each development trajectory with at least one frozen-mechanism success before resource cutoff, the learner-visible state and successful mechanism with the smallest current signed-margin loss. Refit the same 32-cell local router from these selected records. Accept a round only when resource-feasible development reachability strictly increases, or when reachability is unchanged and total trajectory margin loss strictly decreases. Maximum: four accepted/refit rounds, 384 coordinate sweeps per refit.

### Arm 4 — evaluator-only frozen union ceiling

Report whether either frozen mechanism succeeds at any resource-feasible state. This is not a deployable arm and never enters learner inference.

## Required measurements

For every arm report:

- overall, known, and no-unique resource-feasible episode reachability;
- time-zero success / UNKNOWN / wrong;
- reachability by evaluator mode and resource regime.

Also report:

- admission-target positive / negative / zero support;
- global, state-local, and trajectory-local forward/reverse identity;
- trajectory selected-record count, accepted rounds, trace, margin loss, reachable and impossible episode counts;
- evaluator-only union ceiling and the gap between each learned router and that ceiling;
- mature terminal hash before and after development, validation, and confirmation.

## Integrity gates

1. E50 parent and E51Y/E51X terminal reconstruction gates pass.
2. E51AB local-384 direct reconstruction has positive and negative grounded support for both candidates and reproduces exactly forward/reverse.
3. stage-94/95/96 world and domain separation passes with zero assignment failures.
4. exact partition sizes are built.
5. router targets contain both positive and negative support.
6. all global, local state-loss, and local trajectory-critical fits reproduce exactly under forward/reverse traversal.
7. the local routers are nondegenerate.
8. UNKNOWN remains fixed at neutral value 0 with no learned UNKNOWN head or positive UNKNOWN target.
9. neither frozen terminal mechanism changes.
10. no evaluator-only quantity enters inference and no topology, graph, feature, or belief-transition change occurs.

## Validation and confirmation gates

A deployable router arm passes validation only at:

- overall = 5,400 / 5,400;
- known = 4,200 / 4,200;
- no-unique = 1,200 / 1,200;
- every integrity gate passes.

If several pass, choose the lowest-resource arm in order 1, 2, 3. Only that frozen arm executes stage-96 confirmation. Confirmation requires 10,800 / 10,800 overall, 8,400 / 8,400 known, and 2,400 / 2,400 no-unique.

## Frozen outcomes

- `TRAJECTORY_CRITICAL_HYBRID_ROUTER_CONFIRMED` — exact validation and confirmation pass.
- `TRAJECTORY_CRITICAL_HYBRID_ROUTER_VALIDATION_ONLY` — exact validation but confirmation fails.
- `FROZEN_UNION_EXACT_ROUTER_INCOMPLETE` — the evaluator-only union is exact but no learned router is exact.
- `TRAJECTORY_CRITICAL_ROUTER_PARTIAL` — a learned router improves the mature frontier but remains below exact.
- `FROZEN_COMPLEMENT_NOT_REALIZED` — the union improves the mature controller but learned routers do not.
- `NO_FROZEN_COMPLEMENT` — the fresh union does not improve the mature controller.
- `INVALID_E51AD_INTEGRITY_FAILURE`.

A positive routing result does not repair the 140-trajectory support deficit measured in E51AC. That orthogonal deficit requires a later direct-candidate residual/trajectory objective on the same state and action interface. No E51AD result alone promotes R32 or establishes AGI/consciousness.
