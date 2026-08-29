# R32 E52 — Joint Terminal + Continuation Decision Foundry

Date: 2026-08-29
Status: `PREREGISTERED_NATIVE_DISCRIMINATOR — SOURCE FROZEN BEFORE EXECUTION`
Canonical parent: R27 step 60,423
Experimental parent: E50 valid native terminal negative; E51B/C continuation negatives; E51D native oracle-ceiling audit

## Causal question

E51D showed that continuation has large delayed utility, but frozen E50 terminal geometry makes an appropriate UNKNOWN or correct commit unreachable in a material subset of episodes. E52 asks whether a learner-owned, bounded sparse interaction Foundry can improve terminal action-value geometry and then learn continuation value against that improved terminal policy.

## Arms

- A: frozen E50 M0 terminal-only control.
- B: frozen E50 M0 terminal head plus learner-owned sparse continuation Foundry.
- C: learner-owned sparse terminal Foundry, terminal-only.
- D: learner-owned sparse terminal Foundry plus a separately learned continuation Foundry whose delayed-utility targets are recomputed against C.

## Fixed protected substrate

The generic action set remains `KEEP`, `CURRENT`, `RESTORE`, `UNKNOWN`, and `CONTINUE`. UNKNOWN has fixed neutral value 0 and receives no positive target, learned bias, or learned interaction. Evaluator mode, truth, seed, resource identifier, remaining horizon, and ambiguity labels are not policy inputs.

The protected Foundry primitive is a bounded product of two existing TNN-visible features. The learner selects feature pairs and coefficients by residual correlation on development experience, accepts a proposal only if full-development delayed-utility loss strictly falls, and stops when no proposal improves loss or the resource cap is reached. This is generic topology search rather than researcher-selected feature engineering.

## Data and separation

E51B development, validation, and sealed-confirmation effective streams are reserved first. E52 then allocates collision-checked fresh streams:

- development: 3,240 episodes / 55,080 temporal records;
- validation: 2,700 episodes / 10 episodes per base-mode-resource cell;
- sealed confirmation: 1,080 episodes / 4 per cell, allocated but not executed unless validation passes.

Terminal Foundry proposals and continuation targets use E52 development only. Validation does not update any parameter.

## Determinism

Terminal and continuation Foundry searches run in forward and reverse traversal. Selected pairs, coefficients, accepted counts, trace hashes, and exact full-data losses must match. The underlying integer batch fit must also match forward/reverse statistics and parameters.

## Required reporting

Report all four arms on success, UNKNOWN, wrong commitment, known success/wrong, no-unique UNKNOWN/wrong, observations, opportunity loss, and net grounded utility. Report terminal reachability across the full observation tape for both frozen and Foundry terminal heads. Report per-cell no-unique safety, selected interactions, target variation, and all integrity gates.

## Validation success gate

D earns sealed confirmation only if all integrity gates pass and it simultaneously:

1. improves net grounded utility over A and B;
2. does not worsen A's no-unique wrong commitments;
3. preserves or improves A's known success and known wrong commitments;
4. exhibits nontrivial continuation rather than always-stop or always-continue;
5. improves terminal reachability for no-unique UNKNOWN and known correct decisions;
6. passes every-cell no-unique safety.

A validation pass is not promotion. Promotion would still require sealed confirmation, a direct R27-vs-R32 retained capability battery, deterministic state continuity, regression parity, and clean-room packaging.

## Disallowed rescue tactics

No ambiguity classifier, evaluator label, positive UNKNOWN reward, fixed observation count, post-validation threshold, mode-specific route, truth-aware feature, hidden-set tuning, or change to the world/scoring generator after execution.
