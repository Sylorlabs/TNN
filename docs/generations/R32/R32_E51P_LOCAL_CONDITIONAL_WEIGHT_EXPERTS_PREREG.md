# R32 E51P — Learner-Owned Local Conditional Weight Experts

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Evidence basis

E51O established that learner-recruited local regions carry real but weak calibration signal. Increasing scalar local cells from 8 to 64 monotonically improved the local family from 4174/1163 to 4175/1166 (known/no-unique reachability), but the gain saturated rapidly and remained worse than the uncalibrated base on known reachability. Development sign error also remained large at 64 cells.

Therefore simply adding more scalar prototypes is not justified. The next causal question is whether **the same learner-visible state requires different feature weighting in different regions**.

E51P tests that question directly without changing the learner representation, terminal commit ordering, evaluator semantics, or global connection topology.

## Frozen invariants

E51P keeps:

- native Zag v2 only;
- the same primary 32 learner-visible features;
- frozen E50 auxiliary cognition;
- base KEEP/CURRENT/RESTORE absolute-utility ordering head fit only on the first 1x development prefix;
- UNKNOWN fixed at score 0 with no positive target or learned UNKNOWN parameters;
- top-commit sign target derived only from grounded consequence of the learner-selected top commit;
- one final scalar correction applied equally to KEEP/CURRENT/RESTORE, so local experts cannot alter commit identity/order;
- no evaluator mode, resource regime, truth, ambiguity membership, seed, stage, partition, or answer identity as a learner feature;
- no graph/topology rewrite.

## Fresh evaluator worlds

Use the validated E51N domain-separated evaluator transport with injective stages:

- stage 61: development = 12,960 episodes / 220,320 sequential states;
- stage 62: validation = 5,400 episodes / 91,800 sequential states;
- stage 63: sealed confirmation = 10,800 episodes / 183,600 states.

All stages are disjoint from E51N/O worlds and from each other.

## Matched controls

Using only stage-61 development:

A. uncalibrated base top-commit score;
B. full-4x global linear sign calibration;
C. learner-owned scalar local memory using the E51O mechanism, capped at 64 cells.

## Learner-owned routing

Recruit the cumulative prototype/parent routing tree using the frozen E51O algorithm on stage-61 development residuals. No validation state participates in recruitment.

The tree is an indexing/routing mechanism only. It is not assumed to be the final cognitive architecture and does not create general recurrent graph connectivity.

## Conditional local expert

For a chosen routing capacity N, each active cell receives a local linear residual expert:

`local_correction(cell, state) = bias_cell + Σ_i weight[cell,i] * feature_i`

The final sign score is:

`global_linear_score(state) + local_correction(routed_cell, state)`.

Each local expert is trained only from the development states routed to that cell. It starts at zero correction. Coordinate updates are accepted only when they strictly reduce squared sign-target residual on that cell. There is no semantic feature selection, ambiguity detector, confidence threshold, answer table, or task-specific rule.

All expert parameters are generic signed integer weights with bounded magnitude. Training stops after a fixed resource ceiling of 12 coordinate sweeps or earlier if an entire sweep accepts no update. The sweep count is a compute ceiling, not a cognitive rule.

## Capacity arms

Fit independent cumulative routing/expert arms at:

- 4 cells;
- 8 cells;
- 16 cells;
- 32 cells;
- 64 cells.

Each arm uses the first N cells of the single learner-recruited cumulative routing tree and refits its own local experts from zero on stage-61 development. This prevents higher-capacity weights from leaking into lower-capacity arms.

## Resource accounting

Per cell report/account:

- 32 prototype values;
- 1 parent index;
- 32 local feature weights;
- 1 local bias.

Total stored i32-equivalent parameters = 66 × active cells, excluding shared global controls.

Also report worst-case feature-distance routing operations and accepted coordinate updates/sweeps.

## Determinism and integrity

Before interpreting validation require:

1. E50 parent integrity PASS;
2. stage-61/62/63 world and domain ranges valid/disjoint;
3. zero world assignment failures;
4. exact development and validation counts;
5. UNKNOWN target/parameters exactly zero;
6. positive and negative development sign support;
7. base terminal forward/reverse identity PASS;
8. global linear forward/reverse identity PASS;
9. learner routing tree forward/reverse identity PASS;
10. for every capacity arm, local expert parameters, accepted update count, sweep count, loss, and trace hash are forward/reverse identical;
11. every accepted coordinate update strictly reduces development SSE;
12. sealed confirmation remains unexecuted until an exact validation pass.

## Validation

Evaluate every frozen arm once on the same untouched stage-62 partition.

Report:

- development positive/negative sign accuracy;
- validation positive/negative sign accuracy;
- known correct-commit reachability / 4,200;
- no-unique UNKNOWN reachability / 1,200;
- memory and routing cost.

Exact validation requires both:

- known reachability = 4,200 / 4,200;
- no-unique UNKNOWN reachability = 1,200 / 1,200.

The first exact arm in preregistered order 4 → 8 → 16 → 32 → 64 is the only arm eligible for sealed stage-63 confirmation.

## Frozen outcomes

- `LOCAL_WEIGHT_EXPERT_RESCUE_CONFIRMED`
- `LOCAL_WEIGHT_EXPERT_VALIDATION_RESCUE_CONFIRMATION_FAIL`
- `LOCAL_WEIGHT_EXPERT_CAPACITY_SIGNAL`
- `LOCAL_WEIGHT_EXPERT_TRADEOFF`
- `LOCAL_WEIGHT_EXPERT_PLATEAU`
- `INVALID_LOCAL_WEIGHT_EXPERT_INTEGRITY_FAILURE`

A useful capacity signal must improve capability meaningfully, not merely reduce training loss. A model that gains UNKNOWN reachability by materially destroying known reachability is a tradeoff, not a rescue.

If conditional experts substantially improve development fit but fail fresh validation, diagnose teaching/generalization before adding architecture. If both development and validation plateau despite local conditional weights, the next discriminator should test learner-created **recombinable feature interactions or temporary routed connections**, with graph-like topology only as one matched arm.

No E51P result promotes R32 or establishes consciousness/AGI.
