# R32 E51AA — Resource-Feasible Terminal Decomposition Audit

Date frozen: 2026-08-30/31
Branch: `r32-agent-sequential-frontier`
Canonical status: **R27 remains canonical.**

## Question

E51Z proved that the confirmed E51X terminal learner has exact full-tape reachability but loses grounded-successful terminal reachability on 326 / 5,400 fresh trajectories after E51Y's resource-feasible observation path is imposed. Before changing the terminal learner, E51AA asks what part of the terminal mechanism causes those resource-constrained misses.

## Frozen learner and population

- Reproduce the exact E51X 384-sweep terminal learner through the validated E51Y assembly.
- No continuation learner is modified or interpreted by this audit.
- Fresh stage **88**: 5,400 episodes / 91,800 states.
- Domain-separated evaluator RNG/world identities; stage 88 is disjoint from all prior stages.
- No stage-88 state trains, selects, tunes, or updates a learner parameter.

## Decomposition

For each known episode, restrict attention to states reachable before resource infeasibility and distinguish:

1. **Frozen success** — the actual frozen terminal choice is grounded-correct at some feasible state.
2. **Scalar-capable** — the frozen KEEP/CURRENT/RESTORE ranking head has a grounded-correct top commit at some feasible state, but the final shared commit-vs-UNKNOWN scalar calibration may suppress it.
3. **Ranking-limited** — no grounded-correct top commit is available in the feasible prefix, but at least one of KEEP/CURRENT/RESTORE would be grounded-correct at a feasible state if commit ordering changed.
4. **Action-support-limited** — no KEEP/CURRENT/RESTORE action is grounded-correct at any feasible state.

For no-unique episodes, UNKNOWN is already in the terminal action set at every state. A frozen no-unique miss is therefore classified as scalar calibration unless resource feasibility somehow removes state 0, which would be an integrity failure.

## Scalar theoretical ceiling

Report how many episodes could be solved by changing only the existing state-dependent scalar commit-vs-UNKNOWN surface while keeping KEEP/CURRENT/RESTORE ordering frozen.

For scalar-capable known trajectories choose, for audit only, the feasible grounded-correct top-commit state with the largest current scalar score. For no-unique trajectories choose the feasible state with the smallest current scalar score. Hash the effective learner-visible terminal features and verify full equality before counting an alias. Report any exact feature vector that is required to be both commit-side and UNKNOWN-side by these critical states.

Critical-state selection and labels are evaluator-only audit quantities and never enter learner inference.

## Integrity gates

1. E50/E51Y parent reconstruction integrity passes.
2. Stage-88 world/domain separation passes; assignment failures = 0.
3. Exactly 5,400 episodes / 91,800 states are built.
4. Terminal parameter hash is identical before and after stage 88.
5. UNKNOWN target/parameter geometry remains unchanged.
6. No evaluator mode/truth/resource label, stage/world identity, critical-state label, or audit category enters learner inference.
7. No topology, graph, routing tree, feature set, or action set changes.

## Frozen outcomes

- `RESOURCE_FEASIBLE_SCALAR_RESCUE_POSSIBLE` — every episode has a scalar-capable feasible success and no contradictory exact critical-state alias is found.
- `RESOURCE_FEASIBLE_COMMIT_RANKING_REQUIRED` — at least one known episode has a correct feasible commit action but never as the frozen top commit.
- `RESOURCE_FEASIBLE_ACTION_SUPPORT_VETO` — at least one known episode has no correct KEEP/CURRENT/RESTORE action anywhere in its feasible prefix.
- `RESOURCE_FEASIBLE_CRITICAL_ALIAS` — scalar-critical states contain an exact learner-visible commit-vs-UNKNOWN label conflict.
- `MIXED_RESOURCE_FEASIBLE_TERMINAL_LIMIT` — more than one non-scalar limitation is present.
- `INVALID_E51AA_INTEGRITY_FAILURE`.

The audit does not promote R32. It exists to choose the smallest justified resource-constrained terminal repair before continuation is retrained. No graph/connectivity change is tested.