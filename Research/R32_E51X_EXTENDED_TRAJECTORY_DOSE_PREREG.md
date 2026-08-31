# R32 E51X — Extended Trajectory Optimization-Dose Curve

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51W held the cognitive substrate fixed and increased only the coordinate-descent dose inside the E51V trajectory-critical learner. On untouched validation the 96- and 192-sweep arms preserved **4,200 / 4,200 known reachability** and reached **1,198 / 1,200 no-unique UNKNOWN reachability**. The 96-sweep arm was a preregistered stable Pareto improvement over 48 sweeps. The 192-sweep arm tied validation but improved development trajectory reachability to 12,957 / 12,960 and consumed the full four-round sweep ceiling (768 total sweeps), so the optimizer had not demonstrated an internal no-update convergence stop.

The E51W next-step lock requires one more training/optimization diagnosis before changing mechanism when higher dose moves stably toward exact reachability. E51X therefore extends the **same learner and same trajectory objective** to higher optimization dose.

## Fixed cognition

Every arm preserves E51W exactly:

- native Zag v2 only;
- same 32 learner-visible terminal features;
- same E50 grounded terminal utilities;
- same first-1x frozen KEEP/CURRENT/RESTORE ordering head;
- UNKNOWN fixed at value 0, with zero learned UNKNOWN target/parameters;
- same full-4x global top-commit sign calibrator;
- same learner-grown routing tree, first 32 cells only;
- same per-cell linear conditional-weight experts;
- same trajectory-critical state selector;
- same exact trajectory reachability/margin loss;
- same four-round maximum trajectory refit process;
- no new features, recurrence, cross-cell edges, graph topology, ambiguity detector, confidence threshold, evaluator label, or validation-membership input.

Only maximum coordinate-descent sweeps per critical refit changes.

## Fresh worlds

Use the domain-separated E51N transport:

- stage 81 development: 12,960 episodes / 220,320 states;
- stage 82 validation: 5,400 episodes / 91,800 states;
- stage 83 sealed confirmation: 10,800 episodes / 183,600 states.

World IDs and evaluator RNG domains must be disjoint across partitions. Validation is common and untouched. Confirmation executes only after an exact validation pass.

## Arms

A. trajectory-critical refit with **192 sweeps** per critical round — matched lower-dose control.

B. identical learner with **384 sweeps** per critical round.

C. identical learner with **768 sweeps** per critical round.

All three arms start from the same 96-sweep state-SSE 32-cell expert control used by E51W before the trajectory rounds. Candidate experts are trained from zero on the same learner-selected critical records and accepted only if exact full-development trajectory loss strictly decreases; otherwise they are rolled back and that arm stops.

## Determinism and integrity

For every dose independently require forward/reverse development traversal to reproduce exactly:

- critical-state selection trace;
- candidate parameters;
- accepted coordinate updates and sweeps;
- coordinate trace;
- accepted trajectory rounds;
- exact trajectory loss trace/final loss;
- rollback/stop decisions.

The 192-sweep arm must preserve the E51W learner semantics. It need not numerically reproduce E51W because E51X uses fresh worlds.

Required integrity gates:

1. E50 parent integrity passes;
2. domain-separated world partition passes with zero assignment failures;
3. exact development/validation/confirmation allocation counts;
4. UNKNOWN target/parameters remain zero;
5. global calibrator, routing tree, and state-SSE starting expert are deterministic;
6. every dose passes forward/reverse identity;
7. no evaluator-only value enters learner-visible state;
8. confirmation executes zero episodes unless exact validation succeeds.

## Required measurements

For the state-SSE starting control and each trajectory-dose arm report:

- accepted trajectory rounds;
- accepted coordinate updates and sweeps;
- development reachable count and trajectory loss;
- untouched validation known reachability / 4,200;
- untouched validation no-unique UNKNOWN reachability / 1,200;
- total validation reachability;
- paired gains/losses versus 192 sweeps and previous dose;
- switching/reversal losses;
- per-mode reachability;
- whether each arm stopped internally before its sweep ceiling.

## Gates

**Exact rescue:** any trajectory arm reaches 4,200 / 4,200 known and 1,200 / 1,200 no-unique UNKNOWN with zero switching/reversal losses. Execute sealed confirmation using that frozen arm.

**Stable extended-dose signal:** a higher-dose arm strictly increases total validation reachability relative to the preceding dose with zero paired losses and zero switching/reversal losses.

**Extended-dose plateau:** neither 384 nor 768 sweeps improves untouched validation beyond the 192-sweep arm, even if development loss/reachability moves.

**Instability:** higher dose improves aggregate validation but loses one or more previously solved trajectories.

## Frozen outcomes

- `EXTENDED_TRAJECTORY_DOSE_RESCUE_CONFIRMED`
- `EXTENDED_TRAJECTORY_DOSE_VALIDATION_RESCUE_CONFIRMATION_FAIL`
- `EXTENDED_TRAJECTORY_DOSE_STABLE_PARTIAL_SIGNAL`
- `EXTENDED_TRAJECTORY_DOSE_PLATEAU`
- `EXTENDED_TRAJECTORY_DOSE_INSTABILITY`
- `INVALID_EXTENDED_TRAJECTORY_DOSE_INTEGRITY_FAILURE`

## Next-step lock

If E51X reaches exact validation and confirmation, freeze the winning terminal learner and proceed to direct five-way KEEP/CURRENT/RESTORE/CONTINUE/UNKNOWN sequential policy evaluation.

If E51X plateaus or exchanges solved trajectories, **do not increase dose again**. The next experiment is a generic learner-owned preservation/replay acceptance objective: candidate updates must first avoid increasing the number of violated development trajectories, with trajectory margin loss only secondary. This remains on the same state and same 32-cell conditional-weight substrate.

No E51X result may promote R32 or establish AGI/consciousness by itself.
