# R32 E53 — Conservative Average-Cost Joint Policy Stabilization

Date: 2026-08-30
Status: `PREREGISTERED NATIVE DISCRIMINATOR — FROZEN BEFORE FULL EXECUTION`
Canonical: R27 step 60,423
Parents: E51D terminal-reachability audit; E52A exact-coefficient joint Foundry; E52B on-policy continuation negative

## Causal question

E52B found real correctness leverage but failed because repeated on-policy refitting oscillated between endogenous reached-state distributions and spent more observation utility than it recovered. E53 asks whether a generic conservative average-cost policy-improvement substrate can retain the correctness gain while pricing observation cost and suppressing distribution oscillation.

E53 is deliberately representation-neutral. It does not add graph cognition, an ambiguity detector, a task-specific feature, a fixed stopping count, or a positive UNKNOWN bias.

## Frozen inherited geometry

The following remain frozen from E52A/E52B:

- terminal actions KEEP / CURRENT / RESTORE;
- continuation action CONTINUE;
- grounded no-commit action UNKNOWN with value exactly `0`;
- E52A learner-selected terminal pair interactions and coefficients;
- learner-visible state/features, provenance, temporal state, option state, and resource evidence;
- evaluator/world generator semantics.

No terminal Foundry growth is allowed during E53. The experiment changes only how the continuation/current policy is updated and accepted.

## Treatment

The treatment maintains learner-owned mutable state:

1. a running average delayed net-utility baseline;
2. a learned resource shadow price;
3. replay sufficient statistics spanning previously reached policy distributions;
4. a bounded continuation/current value update;
5. a candidate-policy acceptance ledger based on complete-development net delayed utility.

For each reached learner-visible state, the generic continuation target is:

`delayed terminal-utility improvement - actual observation cost - learned long-run resource shadow price - running average utility baseline`.

No evaluator truth or ambiguity label enters that target.

Updates are conservative:

- temporal-difference residuals are clipped before changing mutable policy parameters;
- replay mixes the current reached distribution with retained prior reached distributions;
- a proposed policy replaces the incumbent only when complete-development grounded net utility strictly improves;
- rejected proposals leave the incumbent policy bit-for-bit unchanged;
- UNKNOWN remains an immutable zero-value boundary.

The treatment may update the resource shadow price only from learner-visible resource consumption and later grounded utility/regret. It may not consume resource IDs or evaluator regimes as features.

## Matched arms

- **A** — frozen terminal-only baseline.
- **B** — E52B-style naive repeated on-policy continuation refitting.
- **C** — frozen E52A Foundry terminal-only baseline.
- **D** — E53 conservative average-cost continuation/current learning on the frozen E52A terminal geometry.

A/B/C/D receive matched worlds.

## Forbidden cognition inputs and rescue tactics

The learner may not consume:

- evaluator mode;
- truth state or answer key;
- ambiguity / no-unique label;
- target label;
- seed identity;
- resource ID;
- absolute tape time;
- remaining horizon;
- fixed observation count or fixed duration;
- manually chosen confidence threshold;
- positive UNKNOWN target;
- graph/topology identity as a privileged task hint.

No benchmark-specific branch, lookup table, oracle routing, or hardcoded world-family rule is permitted.

## Required audit outputs

The full native discriminator must emit, for every arm and required cell:

- success / UNKNOWN / wrong;
- known success and known wrong commit;
- no-unique UNKNOWN and no-unique wrong commit;
- observations and realized opportunity cost;
- net grounded utility;
- reached-state ledger hashes for every policy iteration;
- incumbent/candidate policy hashes;
- accepted/rejected proposal count;
- average-reward and shadow-price trajectories;
- policy action-switch rate;
- reached-distribution churn;
- forward/reverse deterministic sufficient-statistic identity;
- two-build native binary identity.

## Primary success gate

D must simultaneously:

1. beat B and C in complete-development and untouched validation net grounded utility;
2. preserve or improve A/C known wrong commitments;
3. retain a substantial fraction of E52B's known-success gain rather than solving cost by never observing;
4. not worsen A/C no-unique wrong commitments;
5. reduce E52B observation opportunity cost materially;
6. reduce reached-distribution churn relative to E52B;
7. exhibit nontrivial learned continuation;
8. preserve UNKNOWN=0 and pass integrity/determinism gates.

Every-cell no-unique safety remains required for qualification. A diagnostic pass is not promotion: R27 remains canonical until fresh confirmation and the complete successor capability contract pass.

## Interpretation boundary

A failure means this conservative average-cost update is insufficient. It does not imply that active investigation, self-modification, or richer connectivity is useless. A pass would justify testing learner-controlled connectivity substrates next; it would not privilege graph cognition.