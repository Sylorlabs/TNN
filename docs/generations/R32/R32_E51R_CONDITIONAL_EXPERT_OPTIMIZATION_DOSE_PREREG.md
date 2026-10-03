# R32 E51R — Conditional Expert Optimization-Dose Curve

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51P's learner-grown 32-cell conditional-weight expert reached exact 4,200/4,200 known reachability but only 1,170/1,200 no-unique UNKNOWN reachability. E51Q reconstructed that same architecture on fresh audit worlds and found 26 blocked no-unique trajectories, no exact learner-state aliases, and no feasible uniform score shift that preserves all known reachability while exposing UNKNOWN on every no-unique trajectory.

E51P's 32-cell expert also hit its 12-sweep optimization resource ceiling. Before adding feature interactions, routing state, dynamic connections, or any topology change, E51R tests whether the residual local margin geometry is simply unfinished optimization of the same conditional-weight architecture.

## Frozen cognition

Every arm keeps exactly the E51P mechanism:

- native Zag v2 only;
- same 32 learner-visible terminal features;
- frozen E50 auxiliary cognition;
- absolute-utility KEEP/CURRENT/RESTORE ordering head fit only on the first 1x development prefix;
- full-4x global sign calibrator;
- the same E51O learner-grown cumulative routing algorithm;
- exactly 32 active routing cells;
- one local linear residual expert per routed cell;
- one shared scalar correction applied equally to KEEP/CURRENT/RESTORE, so commit identity/order cannot change;
- UNKNOWN score exactly 0, with no positive UNKNOWN target or learned UNKNOWN parameters;
- evaluator truth/mode/resource/stage/partition/ambiguity labels absent from learner features;
- no graph or connection-topology change.

Only the conditional-expert optimizer resource ceiling changes.

## Fresh evaluator worlds

Use E51N's validated domain-separated evaluator transport:

- stage 65: development = 12,960 episodes / 220,320 sequential states;
- stage 66: validation = 5,400 episodes / 91,800 sequential states;
- stage 67: sealed confirmation = 10,800 episodes / 183,600 sequential states.

All world identities and evaluator RNG domains must be disjoint from prior stages and from one another.

## Matched sweep-dose arms

Fit three independent 32-cell expert banks from zero on the identical stage-65 development records and identical frozen routing tree:

- A: 12 coordinate sweeps;
- B: 24 coordinate sweeps;
- C: 48 coordinate sweeps.

A sweep ceiling is an experimental compute/resource ceiling, not cognitive knowledge. Each coordinate update is accepted only when it strictly lowers development squared sign-target residual within its routed cell. The optimizer otherwise matches E51P.

## Integrity gates

Before interpreting validation require:

1. E50 parent integrity PASS;
2. stage-65/66/67 world/domain separation PASS with zero assignment failures;
3. exact development and validation counts;
4. UNKNOWN target and learned UNKNOWN parameters exactly zero;
5. both positive and negative development sign targets present;
6. frozen terminal ordering fit forward/reverse identical;
7. global sign calibrator forward/reverse identical;
8. learner-grown 32-cell routing tree forward/reverse identical;
9. for every sweep arm, expert weights/biases, accepted updates, accepted sweep count, stop reason, loss and trace hash forward/reverse identical;
10. every accepted expert coordinate update strictly lowers development SSE;
11. all three arms use the same records, global calibrator, routing tree and 32 cells;
12. validation untouched by fitting;
13. confirmation remains sealed unless an arm reaches exact validation.

## Measurements

For every arm report:

- requested and actually accepted sweeps;
- accepted coordinate updates;
- final development loss hash;
- development positive/negative sign accuracy;
- validation positive/negative sign accuracy;
- validation known reachability / 4,200;
- validation no-unique UNKNOWN reachability / 1,200.

Also report the uncalibrated base and global-linear controls.

## Frozen outcomes

`EXPERT_OPTIMIZATION_RESCUE_CONFIRMED`: the first arm in 12→24→48 order reaches 4,200/4,200 known and 1,200/1,200 no-unique on validation and then repeats exact reachability on sealed stage-67 confirmation.

`EXPERT_OPTIMIZATION_VALIDATION_RESCUE_CONFIRMATION_FAIL`: exact validation does not replicate on confirmation.

`EXPERT_OPTIMIZATION_SIGNAL`: higher sweep dose gives a Pareto improvement in validation reachability without worsening either dimension, and the highest-dose arm still ends at the resource ceiling or has not clearly plateaued. Continue optimization before changing mechanism.

`EXPERT_OPTIMIZATION_TRADEOFF`: higher sweep dose improves one reachability dimension while worsening the other, without exact rescue.

`EXPERT_OPTIMIZATION_PLATEAU`: additional sweeps do not produce a meaningful Pareto movement toward exact reachability, especially if optimization stops early or 48 sweeps fails to dominate 12.

`INVALID_EXPERT_OPTIMIZATION_INTEGRITY_FAILURE`: any integrity gate fails.

## Next-step lock

If E51R plateaus while development sign error remains substantial, the next justified mechanism is a learner-owned **local interaction Foundry** inside the same routed cells: generic feature-pair or other recombinable bases selected only by development residual utility. Dynamic routed connections / graph-like topology remain downstream and must be compared as one arm rather than assumed superior.

If E51R shows a clear optimization signal and still reaches the resource ceiling, extend the sweep curve before adding mechanism.

No E51R result can promote R32 or establish AGI/consciousness.
