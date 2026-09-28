# R32 E51AF — Frozen Global Candidate-Residual Replication and Margin Audit

Date frozen: 2026-08-31
Branch: `r32-agent-sequential-frontier`
Canonical status: **R27 remains canonical.**

## Causal basis

E51AE's byte-reproducible local native execution preserved every stage-97 frozen-union development success and raised stage-98 resource-feasible validation reachability from `5,290 / 5,400` to `5,395 / 5,400`. The global residual arm reached `4,195 / 4,200` known trajectories and all `1,200 / 1,200` no-unique trajectories. The evaluator-only direct-action oracle was exact. The local-96 and local-384 residual arms were weaker than the global arm despite fitting more development rescues.

A five-trajectory residual on one validation partition is too small to justify a targeted mechanism change. E51AF therefore introduces no new learner. It reconstructs the exact E51AE stage-97 global candidate-residual learner, freezes it, and tests whether its near-exact behavior replicates on three independent fresh partitions. It also records an evaluator-only taxonomy of the remaining action-margin failures without exposing that taxonomy to cognition.

E51AF is preregistered from the completed local E51AE ledger while the independent GitHub-native reproduction is still running. Any source or ledger disagreement invalidates E51AF before interpretation.

## Frozen learner lineage

E51AF must reconstruct and freeze:

1. the E50 parent and E51Y/E51X mature terminal controller;
2. the E51AB stage-89 global plus local-384 direct-candidate controller;
3. the E51AE stage-97 critical set and its two deterministic global residual heads;
4. the exact E51AE global residual parameters, traces, target support, loss, and model hash.

The E51AE local residual arms are not used. No E51AF world may train, tune, select, stop, or alter any parameter.

Required E51AE reconstruction constants include:

- development episodes: `12,960`;
- critical records: `639`;
- DIRECT-REQUIRED trajectories: `272`;
- union-neither known trajectories: `234`;
- union-neither no-unique trajectories: `133`;
- critical-set hash: `1498336702`;
- global residual model hash: `133555290`;
- frozen mature terminal hash: `238967492`;
- frozen direct-controller hash: `1790306570`.

## Fresh world partitions

Use the domain-separated E51N world transport with no learner access to world or partition identity:

- replica A: stage 100, `5,400` episodes / `91,800` states;
- replica B: stage 101, `5,400` episodes / `91,800` states;
- replica C: stage 102, `5,400` episodes / `91,800` states;
- sealed confirmation: stage 103, `10,800` episodes / `183,600` states.

Each replica contains exactly `4,200` known and `1,200` no-unique episodes. World tuples and RNG domains must be disjoint from all stages through 99 and from one another. Confirmation executes only under the exact three-replica gate below.

## Fixed arms

### Arm 0 — frozen mature-plus-E51AB direct union

Evaluator union of the unchanged mature slot controller and unchanged E51AB local-384 direct controller. This is the matched baseline and is not itself a deployable router.

### Arm 1 — frozen mature-plus-E51AE global-residual union

Evaluator union of the mature slot controller and the direct candidate controller after adding the exact frozen E51AE global residual heads. This is the only treatment.

### Arm 2 — evaluator direct-action oracle

At each resource-feasible state, select the candidate action with maximum grounded utility or neutral UNKNOWN. This never enters learner inference. It verifies that action support is sufficient on the fresh partitions.

## Margin audit

For every Arm-1 trajectory miss, compute the maximum correct-action margin over all resource-feasible states using evaluator-only grounded values.

For known trajectories classify the best state into exactly one category:

1. `BELOW_UNKNOWN_ONLY` — the grounded-correct candidate is not below the competing candidate under the applicable tie rule, but it fails to clear neutral UNKNOWN;
2. `CANDIDATE_ORDER_ONLY` — the grounded-correct candidate clears UNKNOWN but loses the candidate ordering constraint;
3. `JOINT_THRESHOLD_AND_ORDER` — both constraints fail.

For no-unique trajectories classify any failure as candidate 0 positive only, candidate 1 positive only, or both positive.

For each category report count, minimum deficit, maximum deficit, and fixed deficit buckets `1`, `2–4`, `5–16`, `17–64`, and `65+`. These quantities are evaluator-only diagnostics. They cannot alter a parameter, arm, gate, or outcome.

## Integrity gates

Before interpretation require:

1. all E50 and E51Y/E51X parent gates pass;
2. E51AB direct global/local reconstruction is forward/reverse identical, nondegenerate, and has positive and negative support for both candidates;
3. the E51AE stage-97 critical set is forward/reverse identical with the exact frozen count, trace, support, and hash;
4. the E51AE global residual heads are forward/reverse identical and reproduce the exact frozen hash and loss;
5. mature and frozen-direct hashes remain unchanged after every replica and after any confirmation;
6. stages 100–103 pass world and RNG-domain separation with zero assignment failures;
7. each replica has exactly `4,200` known and `1,200` no-unique trajectories;
8. UNKNOWN remains score zero with no learned head or positive target;
9. evaluator truth, margin category, mode/resource identity, stage/world identity, and replica identity never enter learner inference;
10. topology, graph connectivity, belief-state transitions, terminal features, action support, and tie conventions remain unchanged.

## Frozen outcomes

- `GLOBAL_RESIDUAL_EXACT_REPLICATED` — Arm 1 reaches `5,400 / 5,400` in all three replicas and then reaches `10,800 / 10,800` on sealed stage 103.
- `GLOBAL_RESIDUAL_EXACT_VALIDATION_ONLY` — all three replicas are exact but sealed confirmation is not exact.
- `GLOBAL_RESIDUAL_NEAR_EXACT_STABLE` — every replica is exact on all `1,200` no-unique trajectories, every replica has at most 10 known misses, and pooled known misses across the three replicas are at most 15.
- `GLOBAL_RESIDUAL_PARTITION_SENSITIVE` — the near-exact stability rule fails despite valid integrity.
- `GLOBAL_RESIDUAL_ACTION_SUPPORT_FAILURE` — the evaluator direct-action oracle is not exact on any replica.
- `INVALID_E51AF_INTEGRITY_FAILURE`.

If near-exact behavior is stable and `BELOW_UNKNOWN_ONLY` dominates, the next experiment may fit a low-capacity global commit calibration on a new development partition. If candidate ordering dominates, the next experiment must use a trajectory-level pairwise ranking objective. If the result is partition-sensitive, no mechanism may be justified from the five stage-98 misses alone.

No E51AF result promotes R32 or establishes AGI or consciousness.
