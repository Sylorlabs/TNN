# R32 E51U — Learner-Owned Local Interaction Foundry

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51P established that learner-grown local conditional feature weights are materially more expressive than global/scalar calibration. E51R/S showed that much longer optimization of those same linear experts gives only small capability movement. E51T then proved that 96->192 sweeps does not create a capability superset: on fresh no-unique worlds it gained 5 trajectories and lost 5 others while aggregate reachability remained unchanged. The residual decision boundary is therefore unstable under additional linear coordinate fitting.

A richer *local mapping* is now justified before any graph/topology rewrite.

## Question

Can TNN improve the residual commit-vs-UNKNOWN boundary by autonomously recruiting higher-order connections between already-visible learner features inside the existing routed contexts, while preserving known and switch/reversal reachability?

## Frozen substrate

All arms share:

- full native Zag v2;
- same 32 learner-visible terminal features;
- same E50 parent cognition and utility semantics;
- same first-1x absolute-utility KEEP/CURRENT/RESTORE ordering head;
- same full-4x global top-commit sign calibrator;
- same E51O learner-grown routing tree and first 32 routed cells;
- UNKNOWN score exactly zero, with no positive UNKNOWN target and no learned UNKNOWN parameters;
- evaluator truth/mode/resource/stage/partition/ambiguity labels absent from learner inputs;
- no graph topology, recurrent edge, cross-cell message, or new sensory feature.

## Fresh worlds

Use E51N's domain-separated transport:

- stage 72 development: 12,960 episodes / 220,320 states;
- stage 73 validation: 5,400 episodes / 91,800 states;
- stage 74 sealed confirmation: 10,800 episodes / 183,600 states.

## Matched controls

A. **96-sweep conditional linear expert** — the lower-resource E51T baseline.

B. **192-sweep conditional linear expert** — matched extra-optimization control.

Both are trained from zero on identical stage-72 development records with the same routing tree.

## Learner-created interaction arms

Start from the frozen 96-sweep expert, not from the validation set.

For each of the 32 routed cells, expose one generic interaction primitive over every unordered pair of *distinct* learner-visible features:

`interaction(i,j) = signed_div(feature_i * feature_j, 1000)`, for `0 <= i < j < 32`.

The primitive is generic substrate. Researchers do not select a pair, sign, coefficient, cell, or ambiguity condition.

Within each cell, the learner greedily searches all unused candidate pairs against the current development residual. For a candidate, estimate the bounded integer coefficient from residual correlation, then accept it only if applying it strictly reduces exact full development SSE for that cell. Ties are deterministic by feature-pair order. Accepted terms update residuals before the next search.

Recruit cumulatively up to two interaction terms per cell and freeze two capacity snapshots:

- C: at most **1 interaction per cell** (<=32 total terms);
- D: at most **2 interactions per cell** (<=64 total terms).

A cell may recruit fewer or zero terms if no candidate strictly improves development loss.

This is not a hardcoded graph: pair identities and weights are learner-selected, terms exist only where useful, and no cross-cell routing edge is introduced.

## Determinism / integrity

Before validation interpretation require:

1. E50 parent integrity PASS;
2. stage-72/73/74 world-domain separation PASS;
3. exact development/validation counts;
4. UNKNOWN target/parameters zero;
5. both positive and negative sign targets present;
6. base terminal fit, global scalar fit, routing tree, 96/192 linear expert fits forward/reverse identical;
7. interaction term identity, coefficient, accepted count, residual-loss trace, and 1/2-term snapshots forward/reverse identical;
8. every accepted linear or interaction update strictly lowers development SSE;
9. at least one nonzero interaction term is recruited for an experimental arm to be nondegenerate;
10. validation untouched by selection/fitting;
11. confirmation sealed unless exact validation succeeds.

## Validation measurements

For A/B/C/D report:

- development positive/negative sign accuracy;
- validation positive/negative sign accuracy;
- known reachability / 4,200;
- no-unique UNKNOWN reachability / 1,200;
- paired validation gains/losses relative to control A;
- per-mode reachability.

The preregistered switch/reversal audit group is evaluator modes 3,4,5,7,8. It is evaluation metadata only.

Report recruited term counts globally and by cell, pair/weight trace hashes, and resource footprint.

## Gates

**Exact rescue:** an interaction arm reaches 4,200/4,200 known and 1,200/1,200 no-unique with zero switch/reversal losses relative to A. Execute sealed confirmation only then.

**Partial interaction rescue:** an interaction arm has zero known losses and zero switch/reversal losses relative to A and strictly increases no-unique reachability relative to both A and B.

**Interaction tradeoff:** no-unique improves but known/switching loses, or known improves while no-unique regresses.

**No interaction rescue:** nondegenerate interactions fail to improve the matched capability frontier.

## Frozen outcomes

- `LOCAL_INTERACTION_RESCUE_CONFIRMED`
- `LOCAL_INTERACTION_VALIDATION_RESCUE_CONFIRMATION_FAIL`
- `LOCAL_INTERACTION_PARTIAL_RESCUE`
- `LOCAL_INTERACTION_TRADEOFF`
- `NO_TESTED_LOCAL_INTERACTION_RESCUE`
- `INVALID_LOCAL_INTERACTION_INTEGRITY_FAILURE`

## Next-step lock

If interaction capacity shows a clean partial rescue, extend learner-selected local interaction capacity before adding topology. If it plateaus/trades off, the next discriminator may compare richer local basis families or temporary/dynamic cross-context connectivity against the fixed-weight controls. Any graph-like mechanism must explicitly preserve switching/reversal flexibility and must compete against the strongest non-graph weighting system.

No E51U result can promote R32 or establish AGI/consciousness.
