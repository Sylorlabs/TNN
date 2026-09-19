# R32 E51AC — Additive Direct-Candidate Hybrid

Date frozen: 2026-08-31
Branch: `r32-agent-sequential-frontier`
Canonical status: **R27 remains canonical.**

## Causal basis

E51AA established that the mature `KEEP / CURRENT / RESTORE / UNKNOWN` report geometry has a resource-feasible action-support ceiling: some known trajectories contain no grounded-correct slot action before resource cutoff. E51AB then showed that replacing the mature terminal controller with direct candidate-return heads is destructive: the selected local-384 direct learner preserved no-unique UNKNOWN reachability but reached only 3,324 / 4,200 known trajectories on fresh validation.

The smallest remaining question is whether the direct candidate learner is **complementary** to the mature slot controller. E51AC therefore preserves the complete mature E51Y/E51X terminal policy and adds the previously selected E51AB local-384 candidate learner rather than replacing the mature policy.

## Frozen learner lineage

- Reconstruct the exact E51Y/E51X mature terminal learner and require its historical full-tape reproduction gate.
- Reconstruct the exact E51AB stage-89 global + local-384 direct candidate learner. The 384-sweep arm is frozen because it was the strongest direct arm in E51AB's completed stage-90 comparison.
- No stage-92 or stage-93 state may train, select, tune, or update any parameter.
- The mature terminal parameter hash must remain identical throughout E51AC.

## Fresh partitions

- stage 92: validation, 5,400 episodes / 91,800 sequential states;
- stage 93: sealed confirmation, 10,800 episodes / 183,600 states;
- domain-separated world RNG;
- stage 92 and 93 must be strictly beyond E51AB stage 91 and disjoint from every prior stage.

## Matched arms

### Arm 0 — frozen mature slot controller

Unchanged E51Y terminal policy over `KEEP / CURRENT / RESTORE / UNKNOWN`.

### Arm 1 — UNKNOWN-only direct fallback

Run the frozen mature slot policy first. If it chooses a slot action, preserve that action exactly. Only when it chooses UNKNOWN may the frozen E51AB local-384 direct candidate learner choose `COMMIT(candidate)` or preserve UNKNOWN.

This is the conservative additive arm. Direct candidate scores cannot override a mature slot commitment.

### Arm 2 — score-max additive hybrid

Expose four learner-owned alternatives in common grounded utility units:

- mature top slot commitment, scored by its frozen state-dependent scalar value;
- direct candidate 0 value;
- direct candidate 1 value;
- neutral UNKNOWN = 0.

The highest value wins. Mature slot tie behavior is preserved; direct candidates must strictly exceed the current best value to override it.

### Arm 3 — evaluator-only union ceiling

Report whether either the frozen slot action or the frozen local-384 direct action is grounded-successful at any resource-feasible state. This arm never enters learner inference and is not deployable. It measures whether the two learned mechanisms contain complementary success support.

## Required measurements

For all arms report:

- all episode reachability;
- known reachability;
- no-unique UNKNOWN reachability;
- time-zero success / UNKNOWN / wrong;
- reachability by evaluator mode and resource regime.

For the frozen slot and direct local-384 learners report, separately for known and no-unique trajectories:

- both reachable;
- slot-only reachable;
- direct-only reachable;
- neither reachable;
- union reachable.

## Integrity gates

1. E50 parent and E51Y/E51X terminal reconstruction gates pass.
2. stage-92/stage-93 world and domain partition gates pass; assignment failures = 0.
3. E51AB stage-89 reconstruction contains positive and negative grounded support for both candidate actions.
4. global and local-384 direct fits are forward/reverse identical and nondegenerate.
5. mature terminal parameter hash is identical before training reconstruction and after validation.
6. UNKNOWN remains neutral score 0 with no learned head or positive target.
7. evaluator truth, ambiguity membership, mode/resource labels, stage/world identity, and reachability categories never enter learner inference.
8. no topology, graph, feature, belief-state transition, or hardcoded ambiguity rule changes.

## Validation and confirmation gates

A deployable arm 1 or 2 reaches the exact validation gate only at:

- known reachability = 4,200 / 4,200;
- no-unique UNKNOWN reachability = 1,200 / 1,200;
- all integrity gates pass.

If both pass, arm 1 wins because it permits fewer overrides of mature competence. Only the frozen winning arm may execute stage-93 confirmation. Confirmation requires 8,400 / 8,400 known and 2,400 / 2,400 no-unique reachability.

## Frozen outcomes

- `ADDITIVE_DIRECT_CANDIDATE_HYBRID_CONFIRMED` — a deployable hybrid reaches exact validation and confirmation.
- `ADDITIVE_DIRECT_CANDIDATE_HYBRID_VALIDATION_ONLY` — exact validation, failed confirmation.
- `DIRECT_CANDIDATE_COMPLEMENT_EXACT_ROUTING_REQUIRED` — evaluator-only union is exact but neither learned hybrid is exact.
- `DIRECT_CANDIDATE_COMPLEMENT_PARTIAL` — direct candidate support improves the mature reachability frontier but remains incomplete.
- `NO_DIRECT_CANDIDATE_COMPLEMENT` — no material complementary support.
- `INVALID_E51AC_INTEGRITY_FAILURE`.

A positive union does not justify a graph rewrite. It localizes the next problem to learner-owned routing/calibration between mature and direct report mechanisms. A non-exact union means the direct candidate value learner itself still lacks sufficient support.

No E51AC result can promote R32 or establish AGI/consciousness.