# R32 E51F — Learner-Visible Terminal State Aliasing Audit (Preregistered)

Date: 2026-08-30
Status before execution: `PREREGISTERED — NATIVE CAUSAL AUDIT`
Canonical brain: R27 at developmental step 60,423. E51F cannot promote R32.

## Why this audit exists

E51E refit the terminal value head over sequential states using the frozen grounded terminal utility geometry. On fresh validation, the primary representation made a correct terminal action reachable in 4,200/4,200 known episodes but UNKNOWN remained unreachable in 75/1,200 no-unique episodes. The richer representation missed 6 known episodes and 73 no-unique episodes.

That narrows the bottleneck but does not distinguish two causes:

1. **representation aliasing** — learner-visible states that require incompatible optimal terminal actions are exactly identical under the current representation; or
2. **value-function/capacity/generalization** — the states are distinguishable, but the tested linear action-value head cannot learn the required boundary reliably.

E51F tests cause (1) directly before adding nonlinear capacity, new sensory features, or connection topology.

## Fixed architecture and isolation

No cognition mechanism, reward, topology, or policy is changed. The audit uses the exact terminal learner-visible representations already consumed by E51E models 0 and 1.

Evaluator truth is used only by the audit to calculate each state's set of optimal terminal actions under the already-frozen utility geometry. It is never written into learner state and never influences state construction.

No ambiguity label, evaluator mode identity, resource regime identity, phase label, fixed observation count, confidence threshold, graph rule, or task-specific rule enters the representation.

## Fresh data

Use a fresh collision-checked seed namespace `33`, disjoint from E51E development (30), validation (31), and sealed confirmation (32).

Audit 5,400 fresh episodes across the same six presentation orders, evaluator modes, and resource regimes used by the sequential frontier. Every sequential state t=0..E45_TAPE is included.

## Exact alias definition

For each model independently, the audit inserts the complete learner-visible terminal feature vector into a native exact-key table.

For each state, calculate evaluator-only terminal utilities for KEEP/CURRENT/RESTORE/UNKNOWN and form the bit mask of all actions tied for maximum utility.

For every exact feature-vector equivalence class, track the intersection of these optimal-action masks.

An **irreducible exact alias conflict** exists iff the intersection becomes zero: there is no single terminal action that is optimal for every state sharing that exact learner-visible representation.

A **cross-class alias conflict** additionally contains both known-truth and no-unique states.

Hashing is only an index. Every hash hit must pass exact feature-by-feature equality before two states are considered aliases; hash collisions cannot create a scientific conflict.

## Preregistered interpretation

- If exact cross-class alias conflicts occur, current terminal representation is provably insufficient for those states. The next experiment should add or preserve generic learner-visible information that separates the aliased histories, not merely increase classifier depth.
- If exact alias conflicts are absent or too rare to account for the residual E51E failure, the next discriminator should test generic value-function capacity/factorization using the same inputs and rewards. This does not prove the representation is ideal; it only rejects exact-state aliasing as the dominant cause.

No graph-like or other topology receives preferential treatment from either outcome.
