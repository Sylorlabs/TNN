# R32 E51N — Domain-Separated World RNG Repair + E51M Replication

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51M's native program compiled, executed, and preserved its evidence, but its scientific integrity failed because the inherited approximately one-million-state allocator could not assign 2,440 of 29,160 requested fresh worlds. The failure is evaluator infrastructure exhaustion. E51M's printed dose/capacity measurements are therefore non-authoritative and must not influence learner selection or promotion.

The old freshness contract conflates transient PRNG states from truth, history, passive evidence, active evidence, and resources into one globally exclusive namespace. That contract becomes progressively impossible as experimental dose grows. PRNG internal states are evaluator implementation details, not learner examples.

E51N repairs only that infrastructure and then repeats the frozen E51M scientific question.

## Evaluator-only world identity contract

Each episode receives a deterministic 64-bit world identity:

`world_id = stage * 1,000,000 + canonical_episode_index`

Fresh stages are:

- stage 55: development, 12,960 episodes / 220,320 sequential states;
- stage 56: validation, 5,400 episodes / 91,800 sequential states;
- stage 57: confirmation, 10,800 episodes / 183,600 sequential states, sealed unless exact validation succeeds.

These numerical world-id intervals are disjoint by construction. Stage, partition, seed, world identity, and evaluator mode/resource labels are evaluator-only and never learner features.

## Domain-separated RNG

The evaluator receives five independent deterministic random domains per world:

1. truth / latent temporal state;
2. history evidence;
3. passive evidence;
4. active evidence;
5. resource environment.

Initial RNG state is an injective function of `(world_id, domain)` over the complete E51N allocation and is strictly below the native 64-bit RNG modulus. Domains therefore cannot collide at initialization, and train/validation/confirmation cannot share a world identity.

The new evaluator RNG uses native i64 arithmetic and a deterministic affine recurrence in a much larger state space. Its range mapping preserves the same categorical/range definitions used by E45-E51M. The purpose is not to make worlds easier; it is to stop treating internal substream PRNG states as globally scarce examples.

Freshness is henceforth defined at the **world identity and evaluator-domain identity** level. Coincidental equality of a transient random draw or a partial observation is allowed, just as two genuinely independent real examples may share attributes.

## Learner invariants

E51N must not change:

- the primary 32-feature learner-visible state;
- frozen auxiliary cognition from E50;
- terminal action set KEEP/CURRENT/RESTORE/UNKNOWN;
- UNKNOWN score = exactly 0;
- grounded terminal utilities;
- top-commit sign target;
- scalar calibration semantics;
- learner-selected data-mean hinge family;
- parameter/resource ceilings;
- commit ordering preservation;
- validation gates;
- topology (none added);
- graph status (not privileged).

Evaluator truth and ambiguity membership are used only to generate worlds and grounded consequences. They are never learner inputs.

## Matched E51M replication

Fit the base absolute-utility terminal ordering head only on the first 1x development prefix. Then fit top-commit sign calibration at:

- 1x = 55,080 states;
- 2x = 110,160 states;
- 4x = 220,320 states.

At each dose evaluate scalar boundary capacities:

- linear only / 0 hinges;
- 4 learner-selected hinges;
- 8 learner-selected hinges;
- 16 learner-selected hinges.

All twelve arms use one untouched common stage-56 validation partition.

## Integrity gates

Before interpreting any scientific result require:

1. E50 parent integrity passes;
2. exactly 29,160 world identities allocated;
3. world-id partition ranges are disjoint and counts exact;
4. all five domain-initial-state ranges are injective and mutually disjoint;
5. native i64 RNG state range is valid and nonzero;
6. development = 12,960 episodes / 220,320 states;
7. validation = 5,400 episodes / 91,800 states;
8. confirmation allocated = 10,800 and executed = 0 before a validation pass;
9. base UNKNOWN targets and parameters remain exactly zero;
10. each dose has positive and negative sign-target support;
11. base terminal fit is deterministic;
12. scalar fits are forward/reverse identical;
13. hinge means/structures/coefficients/losses/traces are forward/reverse identical;
14. evaluator identifiers never become learner features.

## Validation outcomes

Exact rescue requires one arm to reach both:

- known correct-commit reachability = 4,200 / 4,200;
- no-unique UNKNOWN reachability = 1,200 / 1,200.

If exact rescue occurs, execute only the first preregistered winning arm on sealed stage-57 confirmation. Confirmation must also be exact before this mechanism can advance to the five-way sequential controller.

If exact rescue does not occur, classify the valid grid:

- `DOMAIN_RNG_VALID_CALIBRATION_DOSE_SIGNAL` if higher dose gives a Pareto improvement at fixed capacity;
- `DOMAIN_RNG_VALID_CALIBRATION_CAPACITY_SIGNAL` if higher capacity gives a Pareto improvement at fixed dose;
- `DOMAIN_RNG_VALID_CALIBRATION_DOSE_CAPACITY_PLATEAU` if neither direction provides a monotone causal signal;
- `DOMAIN_RNG_VALID_CALIBRATION_RESCUE` if exact validation and sealed confirmation pass;
- `INVALID_DOMAIN_RNG_INTEGRITY_FAILURE` if any infrastructure gate fails.

A plateau with substantial development sign error justifies a learner-owned local/prototype calibration memory on the same state before any graph/topology rewrite. A dose signal requires training-first follow-up. A capacity signal requires extending learner-owned boundary capacity before topology changes.

No E51N result promotes R32 or establishes AGI.
