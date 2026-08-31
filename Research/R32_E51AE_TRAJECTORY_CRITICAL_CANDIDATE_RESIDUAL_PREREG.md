# R32 E51AE — Trajectory-Critical Direct-Candidate Residual Support

Date frozen: 2026-08-31
Branch: `r32-agent-sequential-frontier`
Canonical status: **R27 remains canonical.**

## Causal basis

E51AC proved that the frozen mature slot controller and the frozen E51AB local-384 direct-candidate learner have complementary resource-feasible support, but their evaluator-only union still missed 140 known validation trajectories. No router between those fixed mechanisms can rescue a trajectory missed by both. E51AE isolates the remaining candidate-value problem: can a learner-owned trajectory-critical residual objective extend the direct candidate learner's support while preserving every trajectory already covered by the frozen union?

E51AE is independent of the E51AD routing result. It does not learn a mechanism router and does not change the mature slot controller. Its treatment is confined to residual value corrections on the existing generic `COMMIT(candidate)` action interface.

## Frozen lineage and exclusions

Every arm reconstructs and freezes:

1. the confirmed E51Y/E51X mature `KEEP / CURRENT / RESTORE / UNKNOWN` terminal controller;
2. the E51AB stage-89 global plus local-384 direct candidate value heads;
3. the evaluator-blind 32 terminal features;
4. the E51X learner-grown first-32-cell routing partition;
5. UNKNOWN at exactly zero with no learned UNKNOWN parameter.

E51AE adds no sensory feature, confidence threshold, ambiguity detector, mode/resource identity, stage/world identity, validation membership, graph edge, recurrence, topology rewrite, candidate table, or evaluator-derived inference input. Evaluator truth and ambiguity membership are used only to construct delayed grounded value targets and trajectory-level development gates.

## Fresh partitions

- stage 97 development: 12,960 episodes / 220,320 states;
- stage 98 untouched validation: 5,400 episodes / 91,800 states;
- stage 99 sealed confirmation: 10,800 episodes / 183,600 states;
- all evaluator world and RNG domains are disjoint from stages 89 through 96 and from one another.

Confirmation executes only after a fixed treatment reaches exact validation.

## Development support classes

Resource-feasible development trajectories are assigned evaluator-only roles under the two frozen action learners:

- **SLOT-COVERED** — the mature slot controller succeeds at a feasible state;
- **DIRECT-REQUIRED** — the slot controller never succeeds, but the frozen direct learner succeeds;
- **UNION-NEITHER-KNOWN** — neither frozen learner succeeds and the grounded outcome is unique;
- **UNION-NEITHER-NO-UNIQUE** — neither frozen learner succeeds and neutral UNKNOWN is optimal.

The role is never an inference feature. The frozen-union reachability set is a preservation constraint; the two UNION-NEITHER classes define the only admissible rescue target set.

## Residual candidate values

For candidate `c`, the frozen E51AB local-384 score is `Q_frozen(c, x)`. Treatment arms add learner-owned residuals:

`Q_treatment(c, x) = Q_frozen(c, x) + R_global(c, x) + R_local(c, x)`.

UNKNOWN remains exactly zero. The action is the maximum of candidate 0, candidate 1, and UNKNOWN with the existing deterministic candidate-side tie convention.

Grounded candidate targets retain the existing consequence units:

- correct candidate on a known world: `+1000`;
- incorrect candidate on a known world: `-2000`;
- either candidate on a no-unique world: `-1200`.

At each selected state, the fitted target for residual head `c` is the grounded candidate value minus `Q_frozen(c, x)`. Thus the new learner corrects the frozen head rather than replacing its learned representation.

## Trajectory-critical state selection

Select one state per trainable trajectory in each fitting round:

- **DIRECT-REQUIRED:** among states where the frozen direct learner succeeds, choose the state with the smallest current treatment success margin. This is the hardest preservation state.
- **UNION-NEITHER-KNOWN:** choose the resource-feasible state with the largest current margin for the grounded-correct candidate over both the other candidate and UNKNOWN. This is the closest available rescue state.
- **UNION-NEITHER-NO-UNIQUE:** choose the state with the smallest current maximum candidate score. This is the closest available UNKNOWN rescue state.

SLOT-COVERED trajectories need no direct-head preservation example because their frozen slot action remains available and unchanged. Nevertheless, every accepted treatment must preserve the complete frozen-union development reachability set exactly.

UNION-NEITHER examples are deterministically replicated by `ceil(DIRECT_REQUIRED / UNION_NEITHER)` when the preservation class is larger. The factor is derived only from frozen development support counts and is fixed before fitting.

## Fixed arms

| Arm | Description |
|---|---|
| 0 | Frozen mature-slot plus frozen-direct evaluator union control |
| 1 | Two deterministic global linear residual candidate heads |
| 2 | Arm 1 plus learner-routed local residuals, maximum 96 coordinate sweeps per round |
| 3 | Arm 1 plus learner-routed local residuals, maximum 384 coordinate sweeps per round |
| 4 | Evaluator-only direct-action support oracle |

The direct-action oracle reports whether some candidate commit or UNKNOWN is grounded-optimal at a resource-feasible state. It is diagnostic only and never enters learning or arm selection.

Local fitting has at most four trajectory-critical rounds. A round is accepted only when:

1. every frozen-union development trajectory remains reachable; and
2. the number of rescued UNION-NEITHER development trajectories increases, or the rescue count is unchanged and trajectory margin loss decreases strictly.

No arm, residual target, replication factor, sweep dose, shift, state-selection rule, or stopping decision may change after validation is observed.

## Required measurements

For development, validation, and any opened confirmation partition report:

- overall, known, and no-unique resource-feasible reachability for each deployable arm;
- frozen slot, frozen direct, and frozen-union reachability;
- UNION-NEITHER rescue counts;
- time-zero success / UNKNOWN / wrong;
- per-mode and per-resource reachability;
- direct-action oracle reachability;
- class counts and replication factor;
- candidate-wise selected-state target support;
- residual parameter counts, updates, sweeps, rounds, stop reasons, selection traces, fit traces, margin loss, and forward/reverse identity;
- frozen terminal and direct-head hashes before training, after training, and after validation.

## Integrity gates

Before interpretation require:

1. E50 parent and E51Y/E51X mature terminal reconstruction pass;
2. E51AB local-384 direct reconstruction has exact forward/reverse identity, positive and negative grounded target support for both candidates, and nonzero local updates;
3. stage-97/98/99 world and RNG-domain separation passes with zero assignment failures;
4. exact partition sizes and sequential-state counts;
5. development contains at least one frozen-union trajectory and at least one UNION-NEITHER trajectory;
6. selected critical records contain no evaluator-only metadata fields;
7. global residual records, targets, parameters, biases, traces, loss, and support counts reproduce under forward/reverse traversal;
8. every local dose's first/final residual parameters, rounds, updates, sweeps, stop reason, selection trace, fit trace, loss, and support counts reproduce under forward/reverse traversal;
9. each accepted arm preserves every frozen-union development trajectory;
10. the mature terminal controller and frozen E51AB direct parameters remain byte-for-byte logically unchanged through validation;
11. UNKNOWN has no learned parameter and remains exactly zero;
12. confirmation execution is zero unless a fixed arm passes exact validation.

## Validation and confirmation gates

Exact validation rescue requires, with all integrity gates passing:

- overall resource-feasible reachability = **5,400 / 5,400**;
- known = **4,200 / 4,200**;
- no-unique = **1,200 / 1,200**.

If multiple treatment arms pass, select the lowest-resource arm in order 1, 2, 3. Only that frozen arm executes stage-99 confirmation.

Confirmation requires:

- overall = **10,800 / 10,800**;
- known = **8,400 / 8,400**;
- no-unique = **2,400 / 2,400**;
- unchanged integrity, UNKNOWN, and frozen-lineage constraints.

## Frozen outcomes

- `TRAJECTORY_CANDIDATE_RESIDUAL_CONFIRMED` — exact validation and sealed confirmation pass.
- `TRAJECTORY_CANDIDATE_RESIDUAL_VALIDATION_ONLY` — exact validation passes but confirmation fails.
- `TRAJECTORY_CANDIDATE_RESIDUAL_PARTIAL` — a treatment strictly improves the frozen-union control but remains below exact.
- `TRAJECTORY_CANDIDATE_RESIDUAL_NO_RESCUE` — no treatment improves frozen-union reachability.
- `INVALID_E51AE_INTEGRITY_FAILURE`.

A confirmed result would show that the structural direct action support is sufficient and that the remaining failure was trajectory-level candidate-value optimization. A partial result would quantify the residual support frontier and motivate learner-owned prototype/local memory on the same state and action interface. A negative result would reject this low-capacity residual geometry without implying that direct candidate support itself is invalid.

No E51AE result can promote R32 or establish AGI/consciousness.
