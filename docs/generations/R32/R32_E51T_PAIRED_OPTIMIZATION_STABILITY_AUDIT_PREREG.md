# R32 E51T — Paired Optimization Stability Audit

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51S extended the same 32-cell conditional-weight expert from 48 to 96 to 192 optimizer sweeps. Aggregate validation reachability moved from 4,195/1,163 to 4,197/1,163 to 4,197/1,165 (known/no-unique), while the simpler global-linear control retained 4,200/4,200 known reachability. The 192-sweep snapshot therefore shows small aggregate progress but does not robustly dominate the simpler control.

Aggregate counts cannot tell whether later optimization monotonically repairs trajectories or swaps successes and failures. E51T is a parameter-frozen diagnostic of that question.

## Frozen learner

Reconstruct the exact E51S learner from stage-68 development:

- native Zag v2 only;
- same E50 parent cognition;
- same 32 learner-visible features;
- same first-1x terminal ordering fit;
- same full-4x global top-commit sign calibrator;
- same learner-grown routing tree and first 32 cells;
- same cumulative local linear expert optimizer;
- snapshots at 96 and 192 accepted sweeps;
- UNKNOWN fixed at zero, no positive target / no learned UNKNOWN parameters;
- no representation, interaction, topology, graph, or policy change.

Reconstruction must reproduce forward/reverse identity for both snapshots before the audit is interpreted.

## Fresh audit population

Use E51N domain-separated world IDs at stage 71:

- audit = 5,400 episodes / 91,800 sequential states;
- 20 episodes for every base-index x evaluator-mode x resource cell, matching the established validation lattice.

Stage 71 is evaluator-only and is never a learner feature. No learner parameter is updated on the audit population.

## Paired measurements

For each audit episode record whether the frozen 96-sweep snapshot and frozen 192-sweep snapshot have at least one valid stopping state:

- known episode: top commit has grounded utility +1000 and calibrated commit score >= neutral UNKNOWN;
- no-unique episode: calibrated commit score < neutral UNKNOWN at least once.

Report separately for known and no-unique:

- total;
- success at 96;
- success at 192;
- gained by 192 (96 fail -> 192 success);
- lost by 192 (96 success -> 192 fail).

Also report these paired transitions by evaluator mode. Mode labels are audit-only and never enter learner scoring.

For switching/reversal robustness, preregister evaluator modes 3, 4, 5, 7, and 8 as the key dynamic-mode aggregate because their generators include truth changes, historical/current disagreement, misleading early evidence, or reversal-like evidence schedules. This grouping is evaluation metadata only.

## Integrity gates

1. E50 parent integrity PASS.
2. E51S stage-68 development reconstruction uses exact counts and zero UNKNOWN warrant.
3. base terminal, global scalar, routing tree, and 96/192 expert snapshots reproduce forward/reverse identically.
4. stage-71 world/domain allocation is valid and disjoint.
5. audit count = 5,400 episodes / 91,800 states.
6. no learner parameter changes while stage-71 audit is evaluated.
7. evaluator mode/truth/group labels never enter learner features.
8. no graph/topology/interaction change.

## Frozen outcomes

`STRICT_SUPERSET_OPTIMIZATION_SIGNAL`: 192 sweeps loses zero previously reachable episodes in both known and no-unique sets, gains at least one episode, and has zero lost episodes in the preregistered switch/reversal aggregate. Further optimizer dose remains justified before mechanism change.

`OPTIMIZATION_BOUNDARY_INSTABILITY`: 192 sweeps gains at least one episode but also loses at least one previously reachable episode in either known/no-unique, or loses any switch/reversal episode. More coordinate optimization is rearranging the capability boundary; learner-owned richer local structure is justified before another brute-force sweep doubling.

`OPTIMIZATION_CAPABILITY_PLATEAU`: 96 and 192 have identical paired reachability on all audit episodes despite lower development loss at 192. Local interaction capacity is justified.

`OPTIMIZATION_REGRESSION`: 192 loses at least one episode and gains none.

`INVALID_PAIRED_STABILITY_AUDIT`: any integrity gate fails.

No E51T result can promote R32 or establish AGI/consciousness.
