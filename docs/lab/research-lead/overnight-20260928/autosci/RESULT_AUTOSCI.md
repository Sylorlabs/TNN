# RESULT_AUTOSCI: Autonomous Scientific Discovery (F2)

Date: 2026-09-30. Prereg: 2a87efa77 (committed alone before implementation).
Verdict: **BUILD-FAIL** (K-AS5b: random control 1/20 in World B; bar requires 0/20).

This is a bar failure, not a loop failure. The autonomous-scientist loop
(hypotheses from passive data, disagreement-driven experiment construction,
execution, update, predictive model, goal use) worked as designed in both
sealed worlds. The frozen control caught a weak goal instance in World B.
That is the control doing its job.

## What was built

- `autosci_learner.zag`: generic learner. No world knowledge. Primitive
  alphabet (SET/CLR per controllable, WAIT, OBSERVE per variable); candidate
  rules from sufficiency + 2-firing filter on the passive trace; hypotheses
  as cross-product rule sets (data, no per-hypothesis code); iterative
  deepening base-B sequence composition to depth 6; disagreement search by
  pure simulation (zero world calls); single real execution; elimination;
  goal planner (manipulations + WAIT, depths to 8/6); fixed-seed LCG random
  control.
- `world_a.zag`: sealed confounded chain. Truth: (X->Z,d2), (Z->Y,d1),
  (X->D,d1). D confounds. Goal: X=1,Y=1,D=0 simultaneously.
- `world_b.zag`: sealed contextual delay. Truth: (X->Y,d2 iff K==0).
  Goal: from K=1, reach Y=1 within 6 steps.
- Raw logs: `world_a_run.log`, `world_b_run.log` (a priori seed 12345).

## World A trace (all bars pass)

- Candidates: Z:2, Y:3, D:1, X:0. NHYP=6. K-AS1 PASS.
- Round 1: constructed [SD,W,OZ] (depth 3, first disagreeing sequence in
  lexicographic order). Predictions split 0/1 across the Z-rule hypotheses.
  Actual [0]. Killed hyps 1,3,5 (D->Z). Zero world calls during search.
- Round 2: constructed [SD,W,W,OY] (depth 4). Killed hyp 4 (D->Y d2).
- Round 3: search exhaustion to depth 6 (597,870 sequences simulated, zero
  world calls). Survivors [0,2]: the true hypothesis and its observational
  twin Y:(X,3). K-AS4 PASS (truth alive, exhaustion, 2 survivors).
- Goal: planned [SX,W,W,W,SX] (depth 5, unique minimal), both survivors
  agree, executed for real, GOAL_REAL=1. Random control 0/20 (also 0/20 on
  seeds 1,2,3). OBS_USED=6 (2 experiment + 4 verification). K-AS6 PASS.

## World B trace (K-AS5b fails)

- Candidates: Y:2 ([X->Y d2], [X->Y d2 ctx K=0]), X:0, K:0. NHYP=2. K-AS1 PASS.
- Round 1: constructed [SX,SK,W,W,OY] (depth 5, 2 manipulations). hyp0
  (no-context) predicts [1], hyp1 (K==0) predicts [0]. Actual [0]. Killed
  hyp0. One survivor = the true contextual law. K-AS4 PASS. Zero world
  calls during search.
- Goal: planned [SX,CK,W,W] (depth 4), executed for real, GOAL_REAL=1.
- Random control: **1/20** with the a priori seed 12345. The hitting
  sequence was [SX,CK,W,CK,SK,W], which contains the solution pattern
  [SX,CK,W,W] as a subsequence. Follow-up across seeds 1,2,3,7,42,99,777
  and resource-matched length (rlen=plen) shows a base rate near 5%, not a
  fluke. Goal B (transient Y=1) is a weak goal instance: it does not cleanly
  separate contextual understanding from luck at n=20. K-AS5b FAIL.

## Kill-bar scorecard

- K-AS1 (passive ambiguity, >=2 hypotheses): PASS both worlds (6 and 2).
- K-AS2 (construction, not enumeration): PASS by source audit. No complete
  experiment literal appears in any source file; construction is exclusively
  iterative-deepening base-B composition over primitives. Executed
  experiments differ across worlds ([SD,W,OZ], [SD,W,W,OY] vs
  [SX,SK,W,W,OY]). Hypotheses are cross-product rule sets built from
  observations, not authored rule branches.
- K-AS3 (disagreement-driven, zero search actions): PASS. Every executed
  experiment logged with per-hypothesis predicted observation vectors
  showing disagreement before execution; world-call counters prove zero
  real-world actions during search in every round.
- K-AS4 (convergence): PASS both worlds (A: truth survives, exhaustion,
  2-member equivalence class; B: exactly one survivor = true law).
- K-AS5 (model to goal): World A PASS (GOAL_REAL=1, 0/20). World B
  **FAIL** (GOAL_REAL=1, 1/20).
- K-AS6 (observation economy, <=12): PASS (A:6, B:4; total 10).
- K-AS7 (determinism and purity): PASS. 3/3 runs byte-identical per world
  (md5 0c6ec390c10daf7c4fd19a68e198be04 and 8d810241fa3696141a57e0ffd8af8b32).
  Pure Zag; no Python at any stage; no em dashes in wave documentation.

## Harder-case coverage (as preregistered)

- 2-manipulation interventions: B experiment [SX,SK,W,W,OY]; A goal plan.
- 4+ primitive interventions: B experiment (5), A goal plan (5).
- Confounder: D in World A (killed D->Z and D->Y d2 hypotheses by experiment).
- Delayed effects: delays 1,2,3 (A); delay 2 (B).
- Contextual law: K-gated rule in World B, isolated by constructed experiment.
- Observation cost: hard budget 12, used 6 (A) and 4 (B).

## What this shows and what it does not

Shows: a learner with only generic primitives can (1) hold multiple causal
explanations of passive data, (2) construct distinguishing experiments that
exist nowhere in its source, (3) update by elimination, (4) build a
predictive model from survivors, (5) use it to achieve assigned goals. The
constructed experiments ([SD,W,OZ], [SD,W,W,OY], [SX,SK,W,W,OY]) are genuine
inventions of the search, verified absent from source.

Does not show: L3 representational invention (the rule substrate is
researcher-authored; the learned content is edges/delays/contexts, which is
L2 structural learning). No SURVIVES claim is made; promotion steps 4-11
(reproduction, baseline, attack, OOD, ablation, transfer, adversary,
governance audit) remain for the parent to schedule.

## Follow-up recommendation

Re-run World B with a harder goal instance (e.g., requiring sustained
contextual control rather than transient Y=1) under a re-frozen prereg.
The learner and worlds need no architectural changes; only the goal
predicate and its control validation change.
