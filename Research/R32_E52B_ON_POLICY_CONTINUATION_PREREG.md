# R32 E52B — On-Policy Joint Continuation Value

Date: 2026-08-29
Status: `PREREGISTERED NATIVE DISCRIMINATOR — FROZEN BEFORE EXECUTION`
Canonical: R27 step 60,423
Parents: E52 diagnostic negative; E52A exact-coefficient diagnostic

## Causal question

E52A's learner-owned terminal Foundry grew deterministically and improved net terminal utility, but its sequential arm still spent more observation value than it recovered. The continuation head was fit uniformly over every temporal state while runtime visits only states induced by its own stop/continue decisions. E52B asks whether deterministic on-policy fitted continuation value can remove this policy-distribution mismatch.

## Fixed architecture

E52A's protected action set, UNKNOWN=0 geometry, generic pair-product Foundry, terminal training data, terminal Foundry procedure, and four A/B/C/D arms remain fixed. No evaluator label, truth, mode, resource ID, time index, remaining horizon, or ambiguity class enters policy features.

## Treatment

For B and D independently:

1. fit the complete-development continuation baseline;
2. roll that policy through each development episode using only its predicted continuation value and observed feasibility;
3. retain only decision states actually reached by that policy;
4. deterministically resample the reached-state ledger to a fixed complete-dataset size;
5. refit integer action value from zero on that ledger;
6. repeat for at most four iterations or until the reached-state hash stabilizes;
7. allow the same bounded learner-owned sparse interaction Foundry to reduce residual loss on the final reached-state ledger.

Forward/reverse sufficient statistics, parameters, reached-state hashes, Foundry structure, and exact losses must match.

## Fresh-world allocator v2

The original component-disjoint one-million-state allocator is exhausted after reserving E46–E52 streams. E52B does not change the world generator. It replaces only the allocator's over-strong independence rule:

- every new validation/confirmation world must have a base seed never used by any reserved prior world;
- therefore the complete `(seed, mode, resource)` world is new;
- overlaps in subordinate evidence/resource PRNG states are counted and reported rather than treated as identical-world reuse;
- A/B/C/D receive the exact same new worlds.

This preserves exact-world separation while acknowledging partial simulator-substream dependence. Consequently, E52B remains diagnostic and cannot promote R32 without later confirmation under an expanded generator namespace or independent external world source.

Streams:
- development: frozen E52 development, 3,240 episodes;
- validation: 2,700 new base-seed-unique worlds, 10 per cell;
- sealed confirmation: 5,400 new base-seed-unique worlds, allocated but not executed.

## Success gate

D must beat A and B in net grounded utility, not worsen A's no-unique wrong commitments, preserve/improve A's known success and known wrong commitments, improve terminal reachability, exhibit nontrivial continuation, and pass every-cell no-unique safety. Integrity and allocator gates are mandatory. A pass remains diagnostic, not promotion.
