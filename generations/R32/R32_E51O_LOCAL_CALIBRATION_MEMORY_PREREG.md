# R32 E51O — Learner-Owned Local Calibration Memory

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Evidence basis

The valid E51N replication established:

- exact learner-state aliasing is not the residual problem (E51F);
- a frozen terminal head was a major reachability bottleneck (E51D/E51E);
- global linear, sparse pairwise, hinge, preference, and sign-calibration surfaces move the operating point but do not reach the exact safety/known-state target (E51G-L);
- valid 1x/2x/4x dose × 0/4/8/16-hinge curves under the repaired evaluator do not show a monotone rescue direction (E51N);
- substantial development sign error remains at 4x dose.

The next causal question is therefore whether the commit-vs-neutral boundary is **locally heterogeneous** in learner-visible state space and can be represented by bounded learner-owned local memory without changing the 32-feature representation or connection topology.

## Frozen learner state and terminal ordering

E51O keeps:

- native Zag v2 only;
- the same primary 32-feature learner-visible state;
- frozen E50 auxiliary cognition;
- the absolute-utility KEEP/CURRENT/RESTORE ordering head fit only on the first 1x development prefix;
- UNKNOWN score exactly zero;
- no positive UNKNOWN target;
- top-commit sign target: +1000 for positive grounded utility, -1000 for negative grounded utility, 0 if neutral;
- one scalar correction applied equally to all three commit values, so local calibration cannot change KEEP/CURRENT/RESTORE ordering;
- no graph/topology change;
- no evaluator truth/mode/resource/seed/stage/partition membership as a learner feature.

## Fresh evaluator partitions

Use the E51N domain-separated evaluator infrastructure with new, injective world-identity stages:

- stage 58: development = 12,960 episodes / 220,320 sequential states;
- stage 59: validation = 5,400 episodes / 91,800 sequential states;
- stage 60: confirmation = 10,800 episodes / 183,600 states, sealed unless exact validation succeeds.

No stage-56 E51N validation state is reused for E51O model selection or validation.

## Global controls

On full 4x development fit and freeze:

A. uncalibrated frozen top-commit score;
B. global linear top-commit sign calibrator;
C. global linear + first 16 learner-selected data-mean hinges.

These are matched controls, not candidates selected using E51O validation.

## Local memory mechanism

E51O adds a generic bounded **local residual partition memory** on top of the frozen global linear sign calibrator.

A memory cell stores only:

- one 32-feature learner-state prototype;
- a parent cell index used for deterministic local routing;
- one scalar mean residual correction.

It stores no evaluator mode, ambiguity label, answer identity, truth state, seed, stage, or task-specific rule.

### Root

The root prototype is the feature-wise development mean. Every development state initially belongs to the root. The root scalar correction is the mean residual:

`sign_target - global_linear_prediction`.

### Learner-owned recruitment

Repeatedly, up to a 64-cell ceiling:

1. Compute each development state's current local prediction using its assigned cell correction.
2. Choose the state with the largest current squared residual, multiplied by its generic normalized feature distance from its current cell prototype. Ties use canonical development index only for deterministic audit; the index is not a learner feature.
3. Create a candidate child prototype at that learner-visible state and attach it to the state's current cell.
4. Split only that parent cell: a state moves to the child iff the child prototype is strictly closer than the parent prototype under the generic normalized L1 metric.
5. Refit only scalar residual means for the resulting cells from development consequences.
6. Accept the child only if development squared error strictly decreases and both resulting cells are nonempty. Otherwise reject that candidate and continue searching deterministically.

Because each accepted child only partitions one existing cell and each cell receives its own least-squares scalar residual mean, accepted growth must be empirically loss-improving. No researcher chooses a semantic region, feature, prototype, answer class, or ambiguity pattern.

Feature normalization uses only development feature ranges. Zero-range features contribute zero distance.

## Capacity arms

Freeze cumulative snapshots at:

- 8 cells;
- 16 cells;
- 32 cells;
- 64 cells.

If fewer cells are accepted, larger arms use the accepted maximum and are marked capacity-exhausted.

Validation sees all frozen arms once on one common stage-59 partition.

## Resource accounting

Report for each local-memory arm:

- accepted cell count;
- stored i32-equivalent memory units: 32 prototype values + parent + scalar correction per cell;
- worst-case routing feature-distance operations per state;
- development SSE;
- development sign accuracy;
- validation sign accuracy;
- known and no-unique reachability.

Resource accounting does not override capability gates in this diagnostic; it prevents a later claim that larger memory is free.

## Determinism / integrity

Require before scientific interpretation:

1. E50 parent integrity PASS;
2. domain-separated stage 58/59/60 identity ranges disjoint and valid;
3. zero world assignment failures;
4. exact development/validation counts;
5. UNKNOWN targets/parameters remain zero;
6. positive and negative sign support exists;
7. base terminal fit forward/reverse identity PASS;
8. global scalar fit forward/reverse identity PASS;
9. global hinge fit forward/reverse identity PASS;
10. local prototype locations, parent indices, corrections, accepted count, and loss trace are forward/reverse identical;
11. each accepted local split strictly reduces development loss;
12. confirmation remains unexecuted before an exact validation pass.

## Validation success

A local-memory arm passes the E51O reachability gate only if it reaches:

- known correct-commit reachability = 4,200 / 4,200;
- no-unique UNKNOWN reachability = 1,200 / 1,200.

The first passing arm in the preregistered order 8 → 16 → 32 → 64 is the only arm eligible for sealed confirmation.

Sealed confirmation must also reach exact known and no-unique reachability before local calibration can be accepted into the next five-way sequential action-value experiment.

## Frozen outcomes

- `LOCAL_CALIBRATION_RESCUE_CONFIRMED`
- `LOCAL_CALIBRATION_VALIDATION_RESCUE_CONFIRMATION_FAIL`
- `LOCAL_CALIBRATION_CAPACITY_SIGNAL`
- `LOCAL_CALIBRATION_TRADEOFF`
- `LOCAL_CALIBRATION_PLATEAU`
- `INVALID_LOCAL_CALIBRATION_INTEGRITY_FAILURE`

If local memory produces a strong monotone capacity improvement but misses exactness, extend memory/curriculum before topology changes. If it plateaus while development fit is still poor, the next discriminator may compare a learner-grown local conditional expert family against global weights. If development fit becomes near-exact but validation does not, investigate local-memory generalization/teaching before architecture changes.

No E51O result promotes R32 or establishes consciousness/AGI.
