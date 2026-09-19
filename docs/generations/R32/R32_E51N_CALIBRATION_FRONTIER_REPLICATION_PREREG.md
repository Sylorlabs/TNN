# R32 E51N — Calibration Frontier Replication

Date frozen: 2026-08-30 PDT
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51M produced a valid native development/validation curve with exact integrity but no exact terminal-calibration rescue. Three low-capacity contrasts moved the reachability frontier in the Pareto direction on its untouched validation partition:

1. dose at zero hinges: 1× linear `4193 / 1144` to 2× linear `4193 / 1149`;
2. capacity at 1×: 0 hinges `4193 / 1144` to 4 hinges `4194 / 1147`;
3. capacity at 2×: 0 hinges `4193 / 1149` to 4 hinges `4196 / 1156`.

The larger curve was non-monotonic and no calibrated arm dominated the uncalibrated base. E51N therefore does not add architecture. It asks whether these three named low-capacity contrasts replicate on independent fresh world tuples.

## Invariants

E51N must preserve E51M's cognition and learning contract:

- full native Zag v2 only on the promotable path;
- the same 32 learner-visible terminal features;
- the same grounded KEEP / CURRENT / RESTORE utilities;
- the same frozen base commit-ordering head, trained only on the first 1× development prefix of each replica;
- UNKNOWN fixed at score zero with no positive UNKNOWN target or classifier;
- the same consequence-derived top-commit sign target;
- the same deterministic integer scalar fitter;
- the same learner-selected data-mean one-sided hinge search;
- one scalar shift shared by all commit actions, preserving their ordering;
- no confidence threshold, ambiguity detector, fixed observation duration, graph, topology rewrite, hand-selected feature, or evaluator-derived margin;
- evaluator truth, ambiguity membership, seed identity, domain identity, replica identity, stage identity, and validation membership never enter learner-visible state.

## Expanded evaluator world namespace

The historical allocator is retired for E51N because its global component-state disjointness requirement is exhausted. E51N uses domain-separated evaluator world tuples.

Each executable world has evaluator-only identities for:

1. truth;
2. history evidence;
3. passive evidence;
4. active evidence;
5. resource state.

The five identities are deterministic functions of one globally unique E51N world ordinal and fixed substream-domain constants. They are passed separately to the existing generic E45 generators. The resulting world tuple—not each component ID independently—is the freshness unit.

Required namespace properties:

- every E51N executable world ordinal is unique across every replica and partition;
- complete E51N world tuples are injective by construction;
- E51N's nonzero history-domain displacement makes an exact tuple identical to the historical tied-seed E51M generator impossible;
- development and validation tuple overlap is zero;
- cross-replica tuple overlap is zero;
- component-state overlap with historical experiments is measured and reported but does not invalidate a tuple;
- no namespace value is available to cognition;
- sealed confirmation receives nominal IDs only and is never executed in E51N.

A native algebraic/integrity gate must verify the injectivity assumptions before any result is interpreted.

## Replicas and partitions

Run three independent replicas. Each replica receives:

- maximum development: 6,480 episodes / 110,160 sequential states;
- 1× prefix: first 3,240 episodes / 55,080 states;
- untouched validation: 5,400 episodes / 91,800 states;
- validation composition: 4,200 known / 1,200 no-unique;
- sealed confirmation: 10,800 nominal IDs / 0 executed.

Replica partitions are generated from disjoint world-ordinal ranges. No model, term, coefficient, or stopping decision is shared between replicas. Only the experiment contract is shared.

## Fixed arms

Each replica evaluates exactly five arms:

| Arm | Description |
|---|---|
| BASE | Frozen uncalibrated terminal head |
| D1C0 | 1× sign-calibration dose, linear scalar |
| D1C4 | 1× dose plus first four learner-selected hinges |
| D2C0 | 2× sign-calibration dose, linear scalar |
| D2C4 | 2× dose plus first four learner-selected hinges |

The four-hinge structure is selected independently from the corresponding replica and dose's development residuals. No E51M-selected feature identity, direction, mean, or coefficient is imported.

## Frozen contrasts

Three contrasts are tested; no other contrast can be promoted after validation is seen.

### A — dose contrast

`D1C0 → D2C0`

Passes in one replica only when known reachability does not decrease, no-unique UNKNOWN reachability does not decrease, and at least one increases strictly.

### B — 1× capacity contrast

`D1C0 → D1C4`

Uses the same Pareto rule.

### C — 2× capacity contrast

`D2C0 → D2C4`

Uses the same Pareto rule.

For each contrast also compute pooled reachability by summing the three replica validation partitions. A contrast replicates only when:

1. it passes independently in at least two of three replicas; and
2. it passes on the pooled counts.

## Exact gate

Report whether any fixed arm reaches `4200 / 4200` known and `1200 / 1200` no-unique in any replica. This is diagnostic only. E51N has no executable confirmation partition and cannot promote R32.

## Integrity gates

Before interpretation require:

1. parent E50 integrity passes;
2. native world-namespace injectivity gate passes;
3. exactly three disjoint executable replicas are built;
4. each replica has exactly 6,480 development and 5,400 validation episodes;
5. every validation partition contains exactly 4,200 known and 1,200 no-unique episodes;
6. UNKNOWN targets and parameters remain zero;
7. every replica's base terminal fit is forward/reverse identical;
8. every replica/dose scalar fit is forward/reverse identical;
9. every replica/dose first-four-hinge sequence, coefficients, means, loss, and trace are forward/reverse identical;
10. each dose contains both positive and negative sign targets;
11. validation and replica identities are absent from learner inputs;
12. confirmation execution is zero.

## Frozen outcomes

- `CALIBRATION_FRONTIER_REPLICATED`: dose contrast A and at least one capacity contrast B/C replicate.
- `CALIBRATION_DOSE_REPLICATED_ONLY`: A replicates but neither B nor C replicates.
- `CALIBRATION_CAPACITY_REPLICATED_ONLY`: B or C replicates but A does not.
- `CALIBRATION_SIGNAL_UNSTABLE`: none of A/B/C satisfies the replication rule.
- `INTEGRITY_FAILURE`: any required integrity gate fails; no scientific interpretation.

## Interpretation boundary

A positive E51N result would show that additional experience and/or a small amount of learner-selected boundary capacity has reproducible leverage on the same R32 state-to-action geometry. It would not show exact safety, R27 dominance, superiority of graphs, consciousness, or AGI.

If the frontier replicates, the next experiment should change the *learning geometry* rather than topology: trajectory-level ranking or learner-owned local/prototype calibration memory on the same state. If the signal is unstable, E51M is classified as partition-sensitive and the next mechanism must be justified without assuming more scalar dose will solve it.
