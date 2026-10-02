# RESULT: F2 Ablation + Adversary

Date: 2026-09-30. Worker: F2 Ablation Worker.
Prereg: `a3fc27c4c` (committed alone before implementation; verified strict
ancestor of the implementation commit).

## Verdict: ABLATION-TESTED

All three kill bars pass. Eight configurations (3 ablations x 2 frozen
worlds + 2 sealed adversary worlds), each 3/3 byte-identical, pure Zag,
zero Python, zero em-dash bytes.

## Kill bars

- **K1 PASS.** All three variants built from the frozen learner
  (`1eb66765d`) with ONLY the preregistered edits, verified by diff:
  ABL1 changed 8 lines (experiment loop guarded off), ABL2 added 57 lines
  (`L_find_rand` + seed buffer + call-site switch), ABL3 changed 5 lines
  (context forced to -1). Worlds `world_a2_frozen.zag` and
  `world_b2_frozen.zag` used byte-identical to the frozen commit.
- **K2 PASS.** ADV1 and ADV2 implemented as sealed in the prereg (variable
  lists, conjunctive truth, passive schedules, goals), with the learner used
  verbatim from `1eb66765d`. One prereg arithmetic slip is disclosed below:
  ADV1 NHYP is 2, not 4 (Z has 1 candidate, Y has 2; I miscounted in the
  prereg). The sealed FOOLED prediction did not depend on the count and is
  confirmed as observed.
- **K3 PASS.** Pure Zag in source, build, execution, and analysis. No Python
  anywhere. Zero em-dash bytes in wave docs. All 8 configurations 3/3
  byte-identical (md5s below), exit codes recorded, zero stderr except one
  documented harness panic in ABL3-B.

## Results

| Config | md5 (3/3) | NHYP | Exps | nalive | GOAL | Mask |
|---|---|---|---|---|---|---|
| ABL1-A (no experiments, World A) | e9b05f2e8d818828d9500d0dcd016431 | 6 | 0 | 6 | GOAL_REAL=1 | 31 |
| ABL1-B (no experiments, World B) | f6a9a333d86daa4f6d508b3dd3c26bd2 | 2 | 0 | 2 | GOAL_REAL_B2=0 | 27 |
| ABL2-A (random experiments, World A) | 32b5a411d9c10096e6ad32ac829f8de9 | 6 | 14, 0 kills | 6 | GOAL_REAL=1 | 15 |
| ABL2-B (random experiments, World B) | 7b3ea11663f30afa385bf25a95d78fa6 | 2 | 14, 0 kills | 2 | GOAL_REAL_B2=0 | 11 |
| ABL3-A (no context, World A) | db6f4f5ac7e7218801b2e5da7ac0fb49 | 6 | 2 | 2 | GOAL_REAL=1 | 63 |
| ABL3-B (no context, World B) | 15c58d5447e0e45e22cc1df31d46512e | 1 | 0 | 1 | (harness panic, see note) | - |
| ADV1 (conjunctive truth) | 1ef522ec38c9f735fae860a8f9edfeb5 | 2 | 1 | 1 | GOAL_REAL=0 | 27 |
| ADV2 (silent cause) | fa06e777f300a6b8a7bd4b76adf92936 | 1 | 0 | 1 | PLAN none found | 18 |

## Ablation findings

### ABL1: the experiment loop

- **World A: prediction REFUTED.** ABL1-A achieves GOAL_REAL=1 with zero
  experiments, planning under hyp0 (the lexicographically first candidate
  combination, whose Y rule (X->Y d3) is wrong; the truth is (Z->Y d1)).
  The plan [SX,W,W,W,SX] works in reality because the true chain X->Z->Y
  has total delay 3, exactly matching the spurious direct rule. The wrong
  model is observationally equivalent to the truth under the controllable
  interface (Z is not manipulable), so the goal cannot distinguish them.
  The experiment loop is NOT load-bearing for goal achievement on World A;
  its value there is identificational (K2-R4: K2-R4 FAIL with nalive=6 vs
  PASS with nalive=2 in the frozen run).
- **World B: prediction CONFIRMED.** ABL1-B plans under the K-blind hyp0,
  finds M=[SX,W,SX,W,SX], and GOAL_REAL_B2=0 (first triple observation is
  Y=0 because K starts at 1). The frozen run's single disagreement experiment
  ([SX,SK,W,W,OY]) kills hyp0 and the goal succeeds. The experiment loop IS
  load-bearing for the World B goal.

Honest caveat: World A does not test whether experiments are needed for
goals. World B does. Future goal designs should ensure the goal
discriminates the true model from delay-matched or confounded alternatives.

### ABL2: disagreement targeting

14 random experiments (fixed seed 777) on each world killed ZERO hypotheses
and exhausted the observation budget (OBS_USED 22 and 24 > 18; BUDGET_OUT).
Typical draws ([OX], [OZ,SD,SD], [OK]) observe variables on which all live
hypotheses agree, so nothing is ever eliminated. Convergence never happens
(nalive stays 6 and 2). **Disagreement targeting is essential**: the guided
run converges in 2 experiments (A) and 1 experiment (B); random
experimentation cannot replicate this even with 7-14x the experiments.
Goals match ABL1 (GOAL_REAL=1 on A via hyp0 robustness, 0 on B2), confirming
the goal outcomes are driven by the model, not the experiment count.

### ABL3: context machinery

- **World A: prediction CONFIRMED.** ABL3-A output is byte-identical to the
  frozen World A run (md5 156d4ea8fefa74443502d5592ac89e91 after removing
  the one "ABL3 NO_CONTEXT" emit line), MASK 63, all bars pass. The variant
  is a true no-op control (World A has ctxvar=-1), verifying the harness
  introduces no behavioral difference.
- **World B: prediction CONFIRMED in substance.** ABL3-B generates NHYP=1:
  with K=0 throughout passive data, only (X->Y d2 ALWAYS) fits, and the true
  contextual law has no candidate. K2-R1 FAILs as predicted. NOTE: the run
  then panics in the FROZEN world's `w_verify` ("slice index out of bounds")
  because it indexes `alive[true_h]` with true_h=-1. The panic is in harness
  adjudication code (which assumes the truth is always among the candidates),
  not in the learner. The substantive finding stands: without the context
  machinery, F2 cannot represent World B's law at all.

## Adversary findings

### ADV1: conjunctive truth (out of family) -- FOOLED=1, prediction CONFIRMED

Sealed truth Y(t)=X(t-2)&Z(t-1). The learner generated NHYP=2
((X->Y d2), (Z->Y d1)), ran one disagreement experiment ([SZ,W,OY]) that
killed (Z->Y d1), and stopped at nalive==1 with the wrong single-cause rule
(X->Y d2). It never considers that the family itself is inadequate. It then
planned [SX,W,W] under the wrong model with PLAN_AGREEMENT 1 (single
survivor) and GOAL_REAL=0 in reality. **F2 fails confidently, not honestly,
when the truth is outside its hypothesis family**: convergence on one
survivor is treated as success, and the sim-to-real gap is discovered only
at goal execution. There is no graceful degradation path (no "none of my
hypotheses explains the data" verdict at plan time).

### ADV2: silent cause (invisible to passive data) -- MISSED=1, prediction CONFIRMED

Sealed truth Y(t)=X(t-2)&Z(t-1) with Z never set in passive. NHYP=1, ne=0,
zero experiments, "PLAN none found FAIL", OBS_USED 0. Yet the goal IS
achievable: the real plan [SX,W,SZ,W] yields Y(2)=1. **F2 cannot discover a
cause that passive data never implicates.** Hypotheses come only from passive
correlations; the experiment loop discriminates among enumerated hypotheses
but never proposes manipulating an unvaried variable to test a new causal
link. This is the enumerate-then-select boundary: no de-novo causal
discovery.

## Which components are load-bearing

1. **Experiment loop: YES for World B goals and for model correctness
   (K2-R4); NO for World A goal achievement** (the World A goal is robust to
   the specific misspecification because of delay matching). The loop's
   demonstrated value is identification of the true law, which matters when
   the goal discriminates models.
2. **Disagreement targeting: YES, strongly.** Random experiments (14 rounds)
   eliminate nothing and burn the budget; guided search converges in 1-2
   experiments. Targeting is the difference between convergence and
   BUDGET_OUT.
3. **Context machinery: YES for contextual laws (World B); no-op for
   non-contextual worlds (World A control).** Without it, the true
   contextual law is not even a candidate.
4. **Out-of-family truth: F2 is fooled confidently (ADV1).** Single-cause
   family + stop-at-one-survivor yields wrong-model planning with no
   honesty signal.
5. **Silent causes: F2 misses them entirely (ADV2).** No mechanism exists
   for proposing new candidate causes beyond passive correlations.

## Files

All under `docs/lab/research-lead/overnight-20260928/f2_ablation/`:
`PREREG_F2ABLATION.md`, `RESULT_F2ABLATION.md` (this file),
`learner_abl1.zag`, `learner_abl2.zag`, `learner_abl3.zag`,
`learner_frozen.zag`, `world_a2_frozen.zag`, `world_b2_frozen.zag`,
`world_adv1.zag`, `world_adv2.zag`, `run_*.zag`, `bin_*`, `build_*.err`,
`raw_*_*.txt`, `raw_*_*.err`.

## Promotion relevance

Feeds promotion steps 6 (alternative-explanation attack: ABL1/ABL2/ABL3 show
which machinery carries the effect) and 7 (OOD: ADV1/ADV2 are out-of-family
and silent-cause OOD probes). F2's enumerate-then-select boundary is now
empirically mapped: strong within-family (exact-fit + disagreement search is
sound, as the BUILD-PASS showed), blind outside it. No SURVIVES claim is
made.
