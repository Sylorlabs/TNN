# SEALED_CPRIME.md - Sealed World C-prime (F2v3 adversary design)

Date: 2026-10-01. Status: SEALED. Designed post-freeze by the independent
adversary from the frozen prereg family spec (PREREG_F2V3.md section 5)
only. The implementer never sees this world. The sealed file below was
written and its sha256 recorded here BEFORE any sealed evaluation run.

## Sealed file

- Path: docs/lab/rsi/runs/wave-20261001-2021pdt/F2v3/sealed/f2v3_world_cprime.zag
- sha256 (pre-run): c018fc657346a9771cd41315dbedb855755225e7ee552990e3595b1a4acad78a
- Lines: 185. Interface: the v2 w_* interface plus w_ngoalvars /
  w_goalvar / w_goalval and the K4-R4 w_verify contract (prereg section 5).

## Sealed laws

- Variables: X=0 (controllable pulse variable), Y1=1, Y2=2 (effects),
  J=3, K=4 (declared persistent context variables, controllable).
- True laws: (X -> Y1, delay 2, J == 1) and (X -> Y2, delay 3, K == 1).
  d1=2, d2=3 (d1 != d2, both in 1..4), j1=1, k1=1. No law governs X
  (X decays to 0 unless SET at the current step).
- Context enumeration (world-declared): ALWAYS, J==0, J==1, K==0, K==1.

## Passive schedule

- 16 steps (t = 0..15), satisfying the >= 12 step minimum.
- Environment X pulses at t = 2, 7, 12 (3 pulses, spacing 5).
- J = 1, K = 1 throughout (established at t = 0; both persistent).
- Resulting candidate structure (generic v3 rule; verified on the
  calibration run, see below):
  X: 6 [Y1->X d3; Y1->X d3 ctx J=1; Y1->X d3 ctx K=1;
        Y2->X d2; Y2->X d2 ctx J=1; Y2->X d2 ctx K=1]
  Y1: 6 [X->Y1 d2; X->Y1 d2 ctx J=1; X->Y1 d2 ctx J=1(true);
         Y2->Y1 d4; Y2->Y1 d4 ctx J=1; Y2->Y1 d4 ctx K=1]
  Y2: 6 [X->Y2 d3; X->Y2 d3 ctx K=1(true);
         Y1->Y2 d1; Y1->Y2 d1 ctx J=1; Y1->Y2 d1 ctx K=1]
  (ctx variants shown are those with >= 2 firings; J==0/K==0 never hold
  on the passive trace.) NHYP = 216.

## Goal setup (disclosed schema)

- Environment establishes J = 1 - j1 = 0 and K = 1 - k1 = 0 (both gating
  contexts WRONG), then RESET to t = 0. Implemented as w_reset followed
  by w_goal_setup (both values hold by reset; written explicitly).
- Goalvar interface: [Y1, Y2, J, K] with target values [1, 1, 1, 1].
- w_verify implements the K4-R4 contract: exactly one survivor whose
  Y1 rule is (X, 2, J==1) and whose Y2 rule is (X, 3, K==1).

## How C-prime differs from every previously seen instance

- v2 World C (retired): (d1=2,d2=3), gates (0,1), npass=14, pulses
  {2,6,10} spacing 4, passive J=0,K=1, setup J=1,K=0.
- Cdev1 (implementer dev): (d1=3,d2=2), gates (1,0), npass=13, pulses
  {1,5,9} spacing 4, passive J=1,K=0, setup J=0,K=1, goalvals [1,1,1,0].
- Cdev2 (implementer dev): (d1=2,d2=3), gates (1,0), npass=13, pulses
  {1,5,9} spacing 4.
- C-prime (this world): (d1=2,d2=3), gates (1,1), npass=16, pulses
  {2,7,12} spacing 5, passive J=1,K=1, setup J=0,K=0, goalvals
  [1,1,1,1]. Spurious X delays are (3,2); the distinguishing sequences
  and the goal plan share no structure with any dev world.

## Design rationale (adversary notes, recorded honestly)

Two candidate designs were calibrated in /tmp (never in the lane dir)
before sealing. The first draft used (d1=4,d2=1): it produced the
intended 6/6/6 candidate structure, but analysis of the frozen
L_advance semantics (context evaluated at cause time; X decays on WAIT)
showed delay 1 makes the sustained C2 goal physically impossible (the
third SUFFIX observation needs X=1 after the plan ends), and the
calibration run confirmed GOAL_REAL_C2=0 with exactly the predicted
failure signature. Delay 1 was therefore rejected as violating the
non-vacuity goal-achievability requirement, not as a mechanism test.
A (d1=4) draft also showed the standard depth-6 phase cannot pin a
delay-4 Y-rule (distinguishing needs depth 7), which would have moved
Y-rule variants into DPDS scope and muddied the prereg's intended
X-rule-equivalence-class challenge. The sealed (d1=2,d2=3) design keeps
the prereg's intended structure: the standard phase pins Y1/Y2 (all
Y-rule distinguishing sequences fit in depth 6) and the residual
X-rule equivalence class is DPDS's challenge. No calibration step tuned
the world toward DPDS success or failure; the sealed parameters were
fixed before the outcome below was known.

## Non-vacuity certificate (prereg section 5)

Verified pre-delivery with scratch calibration programs (pure Zag;
the v3 learner binary, the frozen v2 learner binary, and a standalone
8-seed random-control program replicating the learner's exact LCG,
alphabet, trajectory, and predicate). All four conditions hold:

1. Candidate generation under the v3 generic rule yields X:6, Y1:6,
   Y2:6 (each >= 2). The X-rule distinguishability bar is non-vacuous.
   (Observed on the calibration run: NHYP 216, candidate lists above.)
2. The v2-frozen loop (standard depth-6 search only, no DPDS)
   terminates with nalive = 6 >= 2 (SURVIVORS [78,79,80,81,82,83],
   EXHAUSTION, Y1/Y2 pinned to truth, X-variant equivalence class
   intact). The v2 failure mode reproduces.
3. The sustained goal is achievable with len(M) = 9 <= 9:
   PLAN_C2 M=[SX,SJ,SK,W,SX,W,SX,W,SX], GOAL_REAL_C2=1
   (obs all ones across the three SUFFIX reps).
4. Random control 0/160 across 8 seeds (12345 plus 7 adversary-chosen:
   7, 99, 1234, 55555, 987654, 20261001, 42) with the frozen LCG,
   7-symbol alphabet, length len(M)+17 = 26, semantic trajectory
   predicate. (The sealed binary's own control covers seed 12345 at
   0/20; the standalone scratch program covers all 8 seeds; both use
   the identical LCG stream, alphabet mapping, and predicate.)

The world is solvable in principle (a learner that resolves the
X-class achieves the goal for real) and not trivially (the ablation
stalls at 6, random control scores 0/160).

## Adversary independence

The dev world files were read solely to learn the exact w_* interface
the sealed world must implement. C-prime's laws, delays, gates,
schedule, and setup were chosen independently and differ materially
from all prior instances as tabulated above. The implementer has no
access to F2v3/sealed/.
