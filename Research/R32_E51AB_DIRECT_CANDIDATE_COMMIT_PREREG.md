# R32 E51AB — Direct Candidate Commit Action Support

Date frozen: 2026-08-30/31
Branch: `r32-agent-sequential-frontier`
Canonical status: **R27 remains canonical.**

## Causal basis

E51AA decomposed the resource-feasible terminal veto and proved that the existing shared commit-vs-UNKNOWN scalar cannot be a complete repair. On fresh stage 88, 48 known trajectories had **no grounded-correct KEEP/CURRENT/RESTORE action anywhere in the resource-feasible prefix**, and one additional trajectory had a correct feasible action that was never the frozen top commit. This failure follows from coupling terminal reporting to already-materialized `initial/current/prior` belief-state slots.

E51AB tests the smallest justified action-support change: keep persistent belief-state maintenance untouched, but allow the terminal value system to report any currently represented hypothesis candidate directly through a generic `COMMIT(candidate)` interface.

This is not an evaluator answer table. Candidate identity is an index into the learner's existing hypothesis set. In the current diagnostic world the set has two members, so the generic interface is instantiated by candidate indices 0 and 1.

## Fixed cognition and exclusions

Every arm keeps:

- native Zag v2 only;
- the same evaluator-blind 32-feature terminal state;
- the same E51X frozen auxiliary cognition and E51X learner-grown first-32-cell routing partition;
- the same grounded terminal utility scale;
- UNKNOWN fixed at score/value 0 with no positive UNKNOWN target or learned UNKNOWN head;
- the same resource process and resource-feasible stopping definition;
- no new sensory feature, ambiguity detector, confidence threshold, evaluator mode, truth label, stage/world identity, resource label, or validation-membership learner input;
- no graph topology, recurrence, cross-cell edge, or dynamic connectivity change.

Belief-state transition behavior is not accelerated or rewritten. Direct candidate commitment is a reporting/action interface only.

## Fresh worlds

Use domain-separated E51N world transport:

- stage 89 development: 12,960 episodes / 220,320 states;
- stage 90 untouched validation: 5,400 episodes / 91,800 states;
- stage 91 sealed confirmation: 10,800 episodes / 183,600 states.

World and RNG domains must be disjoint. Confirmation executes only after an exact validation pass.

## Direct candidate grounded values

For generic candidate index `c`, evaluator-only grounded consequence is:

- grounded outcome absent/no-unique -> `-1200` for committing any candidate;
- `c` equals grounded outcome -> `+1000`;
- otherwise -> `-2000`.

UNKNOWN remains `0`.

These are exactly the existing E45 terminal consequence units, applied directly to candidate actions instead of routing the answer through KEEP/CURRENT/RESTORE state slots. Grounded outcome is used only to construct delayed training/evaluation targets; it is never a learner feature.

## Matched arms

### A — frozen E51X state-slot terminal control

Reproduce the confirmed E51X 384-sweep terminal learner and measure its resource-feasible success reachability on the new validation worlds. No parameter changes.

### B — global direct candidate value heads

Fit two independent deterministic linear value heads, one for each available candidate index, from the same 32 learner-visible features and direct grounded value targets. UNKNOWN is exactly zero and untrained. At inference select the maximum among candidate-value heads and UNKNOWN; ties preserve the existing commit-side convention.

### C — local direct candidate values, 96-sweep dose

Start from B. Reuse the exact first-32-cell learner-grown routing partition from the reproduced E51X terminal learner. Each routed region learns independent residual feature weights for each candidate value head with a maximum 96 coordinate sweeps. The routing partition itself does not see candidate identity or evaluator labels.

### D — local direct candidate values, 384-sweep dose

Identical to C except maximum 384 coordinate sweeps. This isolates optimization dose within the same direct action support.

No arm changes the belief-state transition machinery.

## Determinism and integrity

Before validation interpretation require:

1. E50 parent integrity and E51X terminal reconstruction gates pass;
2. stage 89/90/91 world/domain separation passes with zero assignment failures;
3. exact allocation counts: 12,960 development, 5,400 validation, 10,800 sealed confirmation;
4. both candidate target streams contain positive and negative grounded support;
5. global candidate heads reproduce exactly under forward/reverse development traversal;
6. each local candidate head and dose reproduces exact parameters, update counts, sweep counts, stop reason, trace and loss under forward/reverse traversal;
7. local arms are nondegenerate;
8. UNKNOWN has no learned parameter and remains exactly zero;
9. frozen E51X control parameters remain unchanged;
10. no evaluator-only quantity becomes a learner input.

## Resource-feasible terminal success

For every episode enumerate only states reachable before resource infeasibility.

For direct-action arms, evaluator success at a state means the chosen terminal action achieves the maximum grounded utility among all available candidate commits and neutral UNKNOWN. This generic definition yields correct-candidate commitment on known worlds and UNKNOWN on no-unique worlds without introducing an ambiguity classifier.

Report for each arm:

- overall resource-feasible successful episode reachability;
- known reachability;
- no-unique reachability;
- t0 terminal successes/wrongs/UNKNOWN;
- per-mode and per-resource reachability;
- development and validation candidate-value sign/value error;
- parameter/resource counts.

## Validation and confirmation gates

Exact validation rescue requires:

- overall resource-feasible reachability = **5,400 / 5,400**;
- known = **4,200 / 4,200**;
- no-unique = **1,200 / 1,200**;
- all integrity gates pass.

If multiple treatment arms pass, select the lowest-resource arm in order B, C, D. Only that arm executes the sealed stage-91 confirmation.

Confirmation requires:

- overall = **10,800 / 10,800**;
- known = **8,400 / 8,400**;
- no-unique = **2,400 / 2,400**;
- identical integrity/UNKNOWN constraints.

## Frozen outcomes

- `DIRECT_CANDIDATE_ACTION_SUPPORT_CONFIRMED` — exact validation and confirmation pass.
- `DIRECT_CANDIDATE_ACTION_SUPPORT_VALIDATION_ONLY` — exact validation but confirmation fails.
- `DIRECT_CANDIDATE_ACTION_SUPPORT_PARTIAL` — direct actions strictly improve resource-feasible reachability but remain below exact.
- `DIRECT_CANDIDATE_ACTION_SUPPORT_NO_RESCUE` — no treatment improves the matched control.
- `INVALID_E51AB_INTEGRITY_FAILURE`.

If direct candidate support removes the structural action veto but per-state value fitting still leaves reachability misses, the next experiment may apply the already-validated trajectory-critical objective to the direct candidate heads on the same state/action interface. If an arm is confirmed exact, the next step returns to direct five-way sequential agency with a success-preservation continuation objective and observation cost treated secondarily.

No E51AB result alone promotes R32 or establishes AGI/consciousness.