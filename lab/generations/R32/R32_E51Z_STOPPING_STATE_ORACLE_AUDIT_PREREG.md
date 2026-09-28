# R32 E51Z — Resource-Constrained Stopping-State Oracle Audit

Date frozen: 2026-08-30/31
Branch: `r32-agent-sequential-frontier`
Canonical status: **R27 remains canonical.**

## Causal basis

E51X established exact *unconstrained terminal-state reachability* for the frozen 384-sweep trajectory-critical terminal learner: every untouched validation and sealed-confirmation trajectory contained at least one state where the frozen terminal policy selected the grounded-successful terminal action.

E51Y then trained direct five-way `KEEP / CURRENT / RESTORE / CONTINUE / UNKNOWN` stopping policies. All continuation arms were nondegenerate but failed no-unique safety and lost net utility after observation cost. The local arms changed behavior substantially, so the next question is not whether CONTINUE can affect the policy; it is why the selected stopping states are wrong.

A key unresolved structural issue is that E51X terminal reachability enumerated terminal states independently of the resource-feasibility path used by E51Y. A successful terminal state may exist later in the trajectory but be unreachable after the observation budget is exhausted. In addition, E51Y trains CONTINUE from unconstrained grounded utility while validation applies a strict zero-no-unique-wrong safety gate. Those two objectives may disagree when reaching UNKNOWN costs more than the finite penalty for an unsafe no-unique commit.

E51Z is therefore an **evaluator-only audit**. It changes no learner parameter and adds no cognition.

## Frozen learners

Reproduce exactly the E51Y learner stack from development-only worlds:

- E51X confirmed 384-sweep terminal learner from stage 81;
- E51Y global linear CONTINUE learner from stage 84;
- E51Y local CONTINUE-96 learner from stage 84;
- E51Y local CONTINUE-384 learner from stage 84.

All terminal and continuation parameters must remain unchanged through this audit.

## Fresh audit population

Use stage **87** only:

- 5,400 fresh episodes / 91,800 sequential states;
- 20 episodes per base/mode/resource cell under the existing six-base evaluation layout;
- domain-separated world identity and evaluator RNG transport;
- no stage-87 state may train, tune, select, or gate any learner parameter.

No confirmation population is required because this is diagnostic, not a promotion experiment.

## Audit 1 — resource-constrained success reachability

For every episode, enumerate states reachable from state 0 under the exact E51Y observation feasibility/budget process.

A terminal state is **grounded-successful** when:

- known episode: the frozen terminal choice is a non-UNKNOWN commit with grounded utility `+1000`;
- no-unique episode: the frozen terminal choice is `UNKNOWN`.

Report:

- episodes with at least one grounded-successful terminal state anywhere in the full trajectory;
- episodes with at least one grounded-successful terminal state **reachable before resource infeasibility**;
- missing cost-feasible success by mode and resource;
- first successful stopping time and last resource-feasible stopping time.

If cost-feasible success is absent for any no-unique validation analogue, the strict E51Y zero-wrong gate is structurally impossible for a pure stopping policy over the frozen terminal learner on those episodes.

## Audit 2 — two evaluator-only stopping oracles

### Utility oracle

For every resource-feasible stopping time `t`, compute

`U(t) = grounded_terminal_utility(t) - cumulative_observation_opportunity_cost_before_t`.

Choose the maximum-utility stop; ties choose the earlier stop.

Report utility, outcome class, mode/resource breakdown, and stop histogram.

### Safety-constrained success oracle

Among resource-feasible grounded-successful stopping states only, choose the maximum-utility stop; ties choose earlier. Report:

- success-oracle coverage;
- total utility over covered episodes;
- missing episodes;
- no-unique episodes where the unconstrained utility oracle chooses an unsafe commit even though a safe UNKNOWN stop is resource-feasible.

This distinguishes a representational/control failure from a conflict between the scalar utility objective and the strict safety gate.

## Audit 3 — exact dynamic continuation advantage

Using the frozen terminal policy and exact observation opportunity loss, compute by backward dynamic programming

`V(t) = max(U_terminal(t), -loss(t) + V(t+1))`

and

`A*(CONTINUE,t) = -loss(t) + V(t+1) - U_terminal(t)`

for feasible nonterminal states.

Report evaluator-only magnitude buckets:

- `<= -500`;
- `-499 .. -101`;
- `-100 .. -1`;
- `0`;
- `1 .. 100`;
- `101 .. 500`;
- `> 500`.

The buckets are reporting bins only and are never learner features or decision thresholds.

## Audit 4 — objective/safety conflict

For each reachable state, determine whether stopping now is grounded-successful and whether a later grounded-successful state remains resource-feasible.

Count states where:

- the current stop is unsuccessful;
- a later successful stop is resource-feasible;
- but the E51Y utility advantage is `<= 0` and therefore the binary E51Y target instructs STOP.

These are direct **utility-target versus safety/reachability conflicts**.

## Audit 5 — frozen-policy stopping errors

For E51Y arms B/C/D on their actually visited states, report:

- false-positive CONTINUE decisions (`predicted > 0` while exact utility advantage `<= 0`);
- false-negative CONTINUE decisions (`predicted <= 0` while exact utility advantage `> 0`);
- absolute-advantage-weighted false-positive and false-negative error;
- oracle regret;
- opportunity cost;
- stop before / at / after the utility-oracle stopping time;
- known correct/wrong/UNKNOWN and no-unique UNKNOWN/wrong outcomes;
- per-mode false positives, false negatives, regret, utility, and no-unique wrong counts;
- per-resource equivalents.

## Audit 6 — exact continuation-state conflicts

Hash the effective 32-feature E51Y continuation representation, but verify full feature equality before declaring a duplicate.

For exact-equal learner-visible continuation states, separately audit whether they require conflicting labels under:

1. exact utility-advantage sign (`A* > 0` versus `<= 0`);
2. resource-constrained success-preservation requirement (must continue to reach a later grounded-successful state versus need not continue).

Report exact duplicate rows, conflicting feature keys, and conflict rows. Hash collisions with unequal features must be resolved by probing and must not count as aliases.

## Integrity gates

Interpretation requires all of the following:

1. E50 parent integrity passes through the reproduced E51Y assembly;
2. E51Y terminal and continuation reconstruction identities pass;
3. stage-87 world/domain gate passes with zero assignment failures;
4. exactly 5,400 audit episodes / 91,800 states are built;
5. terminal and continuation parameter hashes before/after the audit are identical;
6. no evaluator truth, mode, resource label, world/stage identity, oracle action, future utility, or audit bucket is introduced into learner inference;
7. no learner updates occur during stage 87;
8. no topology, routing structure, feature set, action set, or UNKNOWN semantics change.

## Frozen outcomes

- `RESOURCE_CONSTRAINED_TERMINAL_REACHABILITY_VETO` — at least one required successful terminal outcome is absent from the resource-feasible stopping set.
- `UTILITY_SAFETY_OBJECTIVE_CONFLICT` — resource-feasible safe outcomes exist, but the scalar utility-optimal target explicitly prefers an unsafe stop on at least one required trajectory/state.
- `CONTINUATION_REPRESENTATION_CONFLICT` — exact learner-visible continuation states require incompatible stopping decisions.
- `CONTINUATION_VALUE_CALIBRATION_ERROR` — cost-feasible success exists, objective/safety conflict is absent, exact feature conflicts are absent, but learned preference makes material false-positive/false-negative errors.
- `MIXED_STOPPING_FAILURE` — more than one causal failure class is materially present.
- `INVALID_E51Z_INTEGRITY_FAILURE` — any integrity gate fails.

The audit does not promote R32 and does not establish AGI or consciousness. Dynamic graph/cross-context connectivity remains unjustified unless the stopping audit demonstrates a missing learner-visible information dependency that cannot be repaired by the existing training/objective path.