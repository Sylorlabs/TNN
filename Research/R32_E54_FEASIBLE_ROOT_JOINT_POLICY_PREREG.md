# R32 E54 — Feasible-Root Conservative Joint Policy

Date: 2026-08-30  
Status: `PREREGISTERED NATIVE DISCRIMINATOR — FROZEN BEFORE EXECUTION`  
Canonical: **R27 step 60,423**  
Parent: E53 conservative average-cost native negative

## Why E54 exists

E53 resolved the naive on-policy oscillation/cost pathology for its conservative continuation arm, but the joint arm accepted zero continuation updates. The joint incumbent was initialized with the full E52A terminal interaction coefficients. On the frozen E53 development set that incumbent already had fewer known successes than the safety baseline (997 versus 1015), while every proposed update was required to recover baseline known-success immediately. This creates a possible feasibility-barrier confound: conservative local updates may be unable to enter the safe set when initialized outside it.

E54 asks only whether that initialization barrier explains the joint-policy failure.

## Single causal change

E54 keeps E53's optimizer, utility, replay, shadow-price candidates, damping candidates, action set, feature boundary, E52A learner-selected pair identities, UNKNOWN=0 geometry, development worlds, and external safety gates fixed.

**Only the joint-arm initialization changes:**

- E53 D: initialize the eight E52A terminal pair coefficients at their E52A learned values.
- E54 D: initialize those same eight pair coefficients at **zero**, exactly matching the safe terminal control; the learner may then grow/re-estimate them through the already-preregistered conservative development optimizer.

The pair identities remain the E52A learner-selected basis. Researchers do not add a new ambiguity feature, new pair, threshold, mode route, observation count, or UNKNOWN reward.

## Matched arms

1. A — frozen terminal-only control.
2. B — E52B-style naive on-policy continuation control.
3. C — E53 conservative continuation with frozen terminal geometry.
4. D — **feasible-root conservative joint** terminal+continuation policy, with the E52A pair basis initialized at zero.

## Learning and acceptance

Identical to the frozen E53 preregistration:

- current/prior reached-state replay;
- exact continuation fitting;
- bounded generic continuation pair Foundry;
- re-estimation only on the eight E52A terminal pair identities in D;
- learner-selected observation shadow price from observed opportunity loss;
- full/half/quarter/eighth update damping;
- complete-development delayed net utility as the objective;
- external known/no-unique safety non-regression before promotion of a candidate;
- exact rollback on rejected candidates;
- policy/reached-state cycle detection;
- maximum six conservative rounds.

Policy features still cannot receive evaluator truth, mode, resource ID, target, ambiguity class, time index, remaining horizon, fixed observation count, or validation information.

## Fresh validation namespace

Because E53 validation has now been observed, E54 must not reuse it.

E54 uses a separate deterministic evaluator namespace with RNG modulus **2,100,001** and the same world-family semantics. Namespace identity is part of provenance, so E54 component states are disjoint from legacy and E53 reservations. Within E54, raw/evidence/resource components must have zero collisions or allocation failures.

- development: frozen 3,240 episodes;
- validation: 2,700 fresh episodes, 10 per base/mode/resource cell;
- sealed confirmation: 5,400 fresh episodes allocated and hashed, **not executed** unless every validation/integrity gate passes.

## Success gates

D must:

- accept at least one nontrivial learner-owned update;
- have stable deterministic reached-state/policy hashes;
- have positive validation net utility and beat A and B after actual observation cost;
- known success >= A and known wrong <= A;
- no-unique wrong < A;
- pass strict every-populated-no-unique-cell safety;
- improve terminal reachability relative to A;
- exhibit continuation in a strict subset of feasible episodes;
- pass native source/compiler/double-build, fit identity, allocator, and provenance gates.

Confirmation remains sealed on any failure.

## Interpretation

- If D begins accepting safe beneficial updates but still fails no-unique safety, the E53 joint failure was partly a **feasible-initialization problem**, and the next discriminator should test learner-owned structural capacity/credit rather than another hand-authored feature.
- If D still accepts no update, the issue is not the unsafe E52A initialization; investigate target/optimizer geometry before increasing connectivity.
- A validation pass earns one sealed confirmation only. It does not promote R32 over R27 by itself.
