# RESULT_AUTOSCI2: F2 Retry with Harder World B Goal

Date: 2026-09-30. Prereg: b9ab0acb6 (committed before implementation).
Implementation: autosci2_learner.zag + world_a2.zag + world_b2.zag.

## Verdict: BUILD-PASS

All seven kill bars (K2-R1 through K2-R7) pass in both worlds.

## World A (confounded chain; identical to F2)

- K2-R1 PASS: NHYP 6 (>=2)
- K2-R3 PASS: zero world calls during search (2 experiments, both with logged disagreement)
- K2-R4 PASS: true_h=2 alive, nalive=2, exhausted=1 (observational equivalence class, as in F2)
- K2-R5a PASS: PLAN [SX,W,W,W,SX], GOAL_REAL 1
- K2-R5b PASS: RANDOM_BASELINE 0/20
- K2-R6 PASS: OBS_USED 6 <= 18
- K2-R7: 3/3 runs byte-identical (md5 156d4ea8fefa74443502d5592ac89e91)

## World B (contextual delay; harder B2 goal)

- K2-R1 PASS: NHYP 2 (>=2; candidates [X->Y d2; X->Y d2 ctx K=0])
- K2-R3 PASS: zero world calls during search (1 experiment [SX,SK,W,W,OY] with logged disagreement: hyp0 predicts [1], hyp1 predicts [0], actual [0], KILLED [0])
- K2-R4 PASS: true_h=1 alive, nalive=1, exhausted=0 (exactly one survivor = true law {(X,2,K=0)})
- K2-R5a PASS: PLAN_B2 M=[SX,CK,W,SX,W,SX] (6 manipulations) + SUFFIX (9 primitives), full_len=15. GOAL_REAL_B2 1 with obs=[1,0,1,0,1,0] (three consecutive (Y=1,K=0) steps, verified for real).
- K2-R5b PASS: RANDOM_BASELINE_B2 0/20 (7-symbol alphabet, length 17, fixed seed 12345)
- K2-R6 PASS: OBS_USED 7 <= 18 (1 experiment + 6 goal verification)
- K2-R7: 3/3 runs byte-identical (md5 52cd392ca369bbdfcb3f3f9c0ffd5ac7)

## Why the harder goal matters

F2's World B goal (transient Y=1) had a ~5% random base rate; the frozen bar
caught a weak goal instance, not a broken mechanism. The B2 sustained triple
goal (three consecutive steps with Y=1 AND K=0) has a measured 0/160 random
base rate across 8 seeds in pre-freeze calibration, while remaining achievable
by the model-based planner (depth-6 M found via iterative deepening over
488K sequences). The learner must understand the delay-2 timing AND maintain
the K=0 context across three steps; luck cannot sustain it.

## Design vs results

The implementation was written after prereg freeze. The planner found
M=[SX,CK,W,SX,W,SX], a valid depth-6 manipulation sequence (lexicographically
first valid M; differs from the calibration M=[CK,SX,W,SX,W,SX] but equally
valid). No prereg amendment was needed.

## Purity and determinism

- Pure Zag. No Python in source, build, execution, or analysis.
- No em dashes in wave documentation.
- 3/3 byte-identical per world (md5 checksums above).
- K2-R2 (construction): source audit confirms no experiment or plan literals;
  experiments composed by iterative-deepening base-B enumeration; M found by
  search; SUFFIX is the preregistered fixed measurement protocol (constructed
  programmatically, contains no manipulations).

## Classification

BUILD-PASS. This wave does not claim SURVIVES (promotion pipeline steps 4-11
remain for the parent to schedule). The mechanism remains L2 structural
learning (bounded), as established in F2.
