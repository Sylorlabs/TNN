# R32 E51S — Extended Conditional-Expert Optimization Curve

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51R held the learner-owned 32-cell conditional-weight mechanism fixed and increased optimizer dose from 12 to 24 to 48 sweeps. Known reachability stayed exact at 4,200/4,200. No-unique UNKNOWN reachability moved only 1,165 -> 1,166 -> 1,166 / 1,200, while the 48-sweep run still accepted strict development-loss improvements and hit its resource ceiling.

The training-first protocol therefore permits one wider optimization extension before adding any representational or connection mechanism. E51S asks whether very long optimization of the *same* conditional weights eventually moves capability reachability, or whether training loss can continue improving after capability has plateaued.

## Frozen cognition

Every snapshot uses exactly the E51R/E51P 32-cell mechanism:

- full native Zag v2;
- same 32 learner-visible terminal features;
- same frozen E50 auxiliary cognition;
- absolute-utility KEEP/CURRENT/RESTORE ordering fit on only the first 1x development prefix;
- full-4x global top-commit sign calibrator;
- one E51O learner-grown cumulative routing tree;
- exactly 32 active routing cells;
- one local linear residual expert per cell;
- local correction applied equally to KEEP/CURRENT/RESTORE, preserving commit identity/order;
- UNKNOWN fixed at score zero with no positive target and no learned UNKNOWN parameters;
- no evaluator truth/mode/resource/stage/partition/ambiguity label in learner state;
- no new feature, interaction, recurrence, graph, or topology change.

Only optimizer compute grows.

## Fresh evaluator worlds

Use E51N's domain-separated world transport:

- stage 68: development = 12,960 episodes / 220,320 states;
- stage 69: validation = 5,400 episodes / 91,800 states;
- stage 70: sealed confirmation = 10,800 episodes / 183,600 states.

All world IDs and RNG domains must be disjoint and valid.

## Cumulative sweep snapshots

Fit one expert bank from zero and freeze exact parameter snapshots after accepted optimizer sweeps:

- snapshot A: 48 sweeps;
- snapshot B: 96 sweeps;
- snapshot C: 192 sweeps.

If an entire sweep accepts no update before a snapshot, later snapshots are byte-identical copies of the converged expert and retain the actual stop sweep. Otherwise optimization continues cumulatively. This is equivalent to increasing compute on the same learner and avoids redundant early sweeps.

Run the entire cumulative fit independently under forward and reverse record traversal. At every snapshot require identical expert weights, biases, accepted-update count, sweep count, loss, and trace hash.

## Required measurements

At each snapshot report:

- requested and actual sweep count;
- cumulative accepted coordinate updates;
- development loss hash;
- development positive/negative decision-side sign accuracy;
- validation positive/negative sign accuracy;
- validation known reachability / 4,200;
- validation no-unique UNKNOWN reachability / 1,200.

Also report base and global-linear controls on the same validation worlds.

## Integrity gates

Before interpretation require:

1. E50 parent integrity PASS;
2. stage-68/69/70 world and domain separation PASS; zero assignments fail;
3. exact development/validation counts;
4. UNKNOWN target/parameters zero;
5. positive and negative development sign support;
6. base terminal fit forward/reverse identical;
7. global sign calibrator forward/reverse identical;
8. learner-grown routing tree forward/reverse identical;
9. all three cumulative expert snapshots forward/reverse identical;
10. every accepted coordinate update strictly lowers development SSE;
11. all snapshots use exactly the same state, data, routing, 32 cells, global calibrator, and expert architecture;
12. validation remains untouched by fitting;
13. confirmation remains sealed unless exact validation occurs.

## Frozen outcomes

`EXTENDED_OPTIMIZATION_RESCUE_CONFIRMED`: first snapshot in 48->96->192 order reaches 4,200/4,200 known and 1,200/1,200 no-unique on validation, then repeats exact reachability on sealed confirmation.

`EXTENDED_OPTIMIZATION_VALIDATION_RESCUE_CONFIRMATION_FAIL`: exact validation fails sealed confirmation.

`EXTENDED_OPTIMIZATION_SIGNAL`: a later snapshot gives a strict Pareto capability improvement over 48 sweeps and the 192-sweep optimizer remains at its resource ceiling. Continue optimization only if the capability curve is still materially moving.

`EXTENDED_OPTIMIZATION_TRADEOFF`: later optimization improves one capability dimension while harming the other.

`EXTENDED_OPTIMIZATION_CAPABILITY_PLATEAU`: training loss / sign fit may continue improving, but 96 and 192 sweeps fail to produce a meaningful Pareto reachability movement beyond the 48-sweep capability frontier, or optimization converges without exact reachability.

`INVALID_EXTENDED_OPTIMIZATION_INTEGRITY_FAILURE`: any integrity gate fails.

## Next-step lock

A capability plateau with residual training error justifies learner-owned **local interaction capacity** inside the same 32 routed cells. The first interaction experiment must compare the frozen linear conditional expert to a bounded learner-selected interaction Foundry on the same state and same worlds. Graph-like or dynamic cross-region connectivity remains downstream and may only enter as a matched experimental arm after local interaction evidence.

No E51S result can promote R32 or establish consciousness/AGI.
