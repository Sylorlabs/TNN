# R32 E51W — Trajectory-Critical Optimization-Dose Curve

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51V changed only the training objective and produced the largest terminal-reachability movement of the E51 line without changing representation or topology. On fresh validation it moved from 4,174 / 4,200 known and 1,160 / 1,200 no-unique UNKNOWN for the 96-sweep state-SSE control to 4,191 / 4,200 and 1,195 / 1,200 after three accepted trajectory-critical rounds. It also reduced development trajectory violations from 105 to 17.

The E51V trajectory candidate fitter, however, reused E51P's 12-sweep local-expert resource ceiling. Earlier E51S/T experiments established that the same 32-cell linear expert continues to accept meaningful coordinate updates well beyond 12 sweeps. Training-first protocol therefore requires an optimization-dose curve on the **trajectory objective itself** before adding connectivity or a new representation.

## Fixed cognition

Every arm keeps exactly the E51V cognitive substrate:

- full native Zag v2 only;
- same 32 learner-visible terminal features;
- same E50 parent cognition and grounded terminal utilities;
- same first-1x frozen absolute-utility KEEP/CURRENT/RESTORE ordering head;
- UNKNOWN fixed at score 0, with zero UNKNOWN target/parameters;
- same full-4x global top-commit sign calibrator;
- same learner-grown routing tree, first 32 cells only;
- same per-cell linear conditional-weight expert architecture;
- same trajectory-critical state selection rule and trajectory violation loss;
- no feature interaction, recurrent state, cross-cell edge, graph, or new sensory input.

Only the maximum coordinate-descent sweeps allowed inside each critical-state refit changes.

## Fresh worlds

Use the domain-separated E51N transport:

- stage 78 development: 12,960 episodes / 220,320 states;
- stage 79 validation: 5,400 episodes / 91,800 states;
- stage 80 sealed confirmation: 10,800 episodes / 183,600 states.

World and all evaluator RNG domains must be disjoint across partitions. Validation is common and untouched. Confirmation executes only after an exact validation pass.

## Arms

A. 96-sweep state-SSE 32-cell expert control.

B. trajectory-critical refit with maximum **12 sweeps** per critical round, reproducing E51V's treatment mechanism on fresh worlds.

C. identical trajectory-critical learner with maximum **48 sweeps** per critical round.

D. identical trajectory-critical learner with maximum **96 sweeps** per critical round.

E. identical trajectory-critical learner with maximum **192 sweeps** per critical round.

Each trajectory arm starts from arm A for critical-state selection. It may accept at most four trajectory rounds. Each candidate expert is fit from zero on the currently selected critical records exactly as in E51V; the candidate is accepted only when it strictly lowers the exact full-development trajectory violation loss. Otherwise it is rolled back and that arm stops.

The coordinate optimizer is the same integer residual coordinate descent used by E51P/S, parameterized only by the maximum sweep count. It must stop earlier if a full sweep accepts no update.

## Determinism

For every trajectory dose, independently fit forward and reverse development traversal. Require exact identity of:

- selected critical-state trace per round;
- candidate expert parameters;
- accepted coordinate update count and sweep count;
- candidate fit-loss trace;
- accepted trajectory-round count;
- trajectory violation-loss trace and final loss;
- rollback/stop decision.

The 12-sweep implementation must reproduce the E51P fitter semantics under the same critical records; any mismatch is an integrity failure.

## Required measurements

For A–E report:

- accepted trajectory rounds;
- attempted/accepted coordinate sweeps and updates;
- development trajectory reachable count and violation loss;
- validation positive/negative state sign accuracy;
- validation known reachability / 4,200;
- validation no-unique UNKNOWN reachability / 1,200;
- paired gains/losses against A and B;
- per-mode reachability;
- losses on switching/reversal modes 3,4,5,7,8.

## Gates

**Exact dose rescue:** any B–E reaches 4,200/4,200 known and 1,200/1,200 no-unique with zero switch/reversal losses against A. Run sealed confirmation.

**Stable partial dose signal:** a higher-dose arm has zero paired losses against the lower-dose trajectory arm, zero switching/reversal losses against A, and strictly increases total validation reachability.

**Aggregate dose signal with instability:** higher dose improves aggregate reachability but loses at least one previously solved trajectory.

**Dose plateau:** 48/96/192 sweeps fail to produce a meaningful capability improvement beyond the 12-sweep trajectory arm.

## Frozen outcomes

- `TRAJECTORY_DOSE_RESCUE_CONFIRMED`
- `TRAJECTORY_DOSE_VALIDATION_RESCUE_CONFIRMATION_FAIL`
- `TRAJECTORY_DOSE_STABLE_PARTIAL_SIGNAL`
- `TRAJECTORY_DOSE_AGGREGATE_SIGNAL_WITH_INSTABILITY`
- `TRAJECTORY_DOSE_PLATEAU`
- `INVALID_TRAJECTORY_DOSE_INTEGRITY_FAILURE`

## Next-step lock

If a higher dose moves monotonically toward exact reachability, continue the training/optimization diagnosis before changing mechanism. If dose plateaus or continues to exchange solved trajectories, the next conservative experiment is a generic learner-owned **preservation/replay acceptance objective** that rejects a development update which increases the number of violated trajectories, with margin loss secondary. Only after that objective family plateaus is temporary cross-context connectivity justified.

No E51W result can promote R32 or establish AGI/consciousness.