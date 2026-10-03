# PREREG: L3 Invention with Delayed Consequences (L3-DELAYED)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l3_delayed/` only.
Worker: L3 Delayed Consequence Worker (subagent, 2026-10-02).
Parent mandate: test L3 invention with DELAYED consequences.
Boundary from L3-VERIFY (L3-VERIFY-COMPLETE, same directory tree):
there the consequence of a deployment was observable immediately
through the coin oracle. Untested: can the learner verify M when the
consequence arrives N steps AFTER the deployment, with other
deployments in flight meanwhile? This experiment isolates exactly
that variable: same settlement world family, same episode tables,
same hidden margin rule, same op basis, but the ONLY
learner-facing consequence channel is delayed by N=3 steps and
returns nothing at schedule time.

## 1. What is being tested

Whether the learner can invent the intermediate M AND verify it when
every consequence is delayed. The learner deploys a candidate at step
s and learns its aggregate coin consequence only at step s+3, while
deploying further candidates at steps s+1, s+2. It must:

(a) deploy the inherited wrong intermediate M0, and, when M0's
    consequence arrives 3 steps later interleaved with other
    deployments, attribute it to M0 (not to a more recent
    deployment) and record it as incumbent;
(b) construct a fresh M1 through delayed consequence queries only,
    attributing each arriving consequence to the step that scheduled
    it, and revise (replace M0) because the attributed C(M1) > C(M0);
(c) deploy M1 on held-out episodes, observe its consequence 3 steps
    later, attribute it to the M1 deployment, and retain M1
    byte-identical.

The consequence is a scalar P&L per deployment, delivered late. The
learner never observes a label, a margin, or an immediate consequence.

## 2. Frozen world (SETTLE-D; environment, hidden from learner)

Same frozen episode tables and hidden margin rule as L3-VERIFY
(margin(ep) = e0 + e1 - e2; learner source never computes it and
never receives it per episode):

Train episodes (id: [e0,e1,e2,e3], margin):
1: [2,7,3,0] m=6    2: [8,1,4,1] m=5
3: [1,6,3,5] m=4    4: [6,0,3,3] m=3
5: [7,4,15,0] m=-4  6: [4,3,10,1] m=-3
7: [3,2,7,2] m=-2   8: [3,0,4,3] m=-1

Held-out test episodes:
9: [4,5,2,0] m=7    10: [1,1,5,0] m=-3
11: [6,2,3,1] m=5   12: [2,3,8,2] m=-3

Frozen delay: N = 3 steps. Consequence of deploying program P with
threshold t on a region: coins = sum of margins of episodes with
P(ep) >= t, delivered exactly 3 steps after the deployment step.

World-side symbols:
- `w_init()` -> world-state buffer (opaque schedule store; the
  driver creates it and hands it to the learner; it is environment,
  not learner memory).
- `w_sched(wst, step, prog, n, thr, region)`: schedule a deployment.
  Returns NOTHING. No consequence is observable at schedule time.
  Learner-facing. This is the only way the learner deploys.
- `w_arrive(wst, step, out) -> i32`: if a deployment was scheduled at
  step-3, compute its aggregate coin consequence NOW and write
  out[0]=sched_step, out[4]=coins, out[8]=thr; return 1. Else
  return 0 and write nothing. Learner-facing. Polling a future step
  early is impossible: the slot is empty until its step arrives, and
  the learner protocol polls only the current step.
- `w_conseq(prog, n, thr, region) -> i32`: immediate aggregate coins.
  EXPERIMENT-SIDE ONLY (driver arms and the experiment-side
  uniqueness sweep). The learner must never reference it (K-D1
  audit). It exists so arms do not need the delayed channel.
- `w_val`, `w_n`, `w_id`, `w_margin`, `menu_agg`, `menu_name`:
  experiment-side tables/helpers (driver only; forbidden in learner).

Frozen oracle rule for threshold candidacy (unchanged from
L3-VERIFY): candidate thresholds are the sorted unique program
outputs on the evaluated episode set, ascending; first-max wins.
Deterministic; no RNG.

## 3. Frozen learner machinery (new, disclosed, researcher-authored)

`learner_d.zag` is NEW code written for this experiment (the
L3-VERIFY learner is read-only and immediate-oracle based, so it
cannot be reused). Disclosed generic machinery: X episode recall
(sequences only), register-machine executor (ops 0=CPY 1=ADD 2=SUB
3=MAX 4=MIN, R0..R3 preloaded, output R0), in-flight LEDGER (per
step: job tag u8, candidate index u8, threshold index u8; 4096-step
capacity), per-job score tables (threshold values and attributed
consequences), delayed threshold sweep (deploy one (prog,t) per step,
poll arrivals each step, drain N steps, first-max over attributed
scores), greedy construction over 80 candidates per round (op-major
order 0..4, d 0..3, s 0..3; strictly positive gain; 8-instruction
cap), M slot bookkeeping [n,u8 gen,u8 sup,u8 pad, threshold i32, 24
program bytes] plus Mprev, and the confidence policy below. The
learner calls exactly two world-side symbols: `w_sched` and
`w_arrive`. No other world reference exists in learner_d.zag.

Job tags (frozen): 1=M0FIT, 2=R1, 3=R2, 4=R3, 5=CURFIT, 6=M1TEST.

Frozen confidence policy (generic, no modes; same as L3-VERIFY):
- l_observe(C): if C > bestC { bestC = C; conf++; } (conf unchanged
  otherwise).
- l_revise after construction: if C_new > bestC { Mprev = incumbent
  with sup=1; M = new with gen = old gen + 1; bestC = C_new; conf++;
  log REVISE }.
- l_deploy_eval(C): retained = (C > 0) ? 1 : 0; M never modified here.

Attribution rule (frozen): when w_arrive(step) reports
(sched_step, C, thr), the learner reads ledger[sched_step] ->
(tag, cand, thri), records C in that job/candidate/threshold score
cell, and logs
`ATTR arr=<step> sched=<sched_step> tag=<tag> C=<C> t=<thr>`.
Every deployment logs
`DEPLOY step=<s> tag=<tag> cand=<c> thri=<j> t=<t> region=<r>`.
Correct attribution means sched_step = arr - 3 and the tag matches
the DEPLOY line at step sched_step (checked by the frozen shell awk
audit, section 7).

The inherited wrong intermediate M0 = [ADD R0,R2] (bytes 1,0,2) is
seeded experiment-side (L3-VERIFY's wrong inheritance); the learner
does not invent it. Its consequence is measured through the delayed
channel, not stipulated.

## 4. Frozen hand-derived numbers (independent check BEFORE this commit)

Verified by an independent pure-Zag reimplementation
(/tmp/dcheck.zag, direct value formulas, no register machine,
separate code path from the future learner) before this prereg was
written. The implementation must reproduce every number below
through the DELAYED channel; any deviation is a falsifier, not a
tuning opportunity. Consequence VALUES are identical to the
immediate-oracle case; only their arrival time differs.

M0 = [ADD R0,R2] delayed fit: 8 threshold deployments; first-max
gives t=4, C=8.

Empty program delayed fit (CURFIT): t=1, C=8 (baseline).

Round 1 (from empty; baseline C=8 t=1), all 80 candidates in
op-major order (index = op*16+d*4+s):
d=0 (20): CPY R0,R0 8 t=1; CPY R0,R1 10 t=6; CPY R0,R2 8 t=3;
CPY R0,R3 8 t=0; ADD R0,R0 8 t=2; ADD R0,R1 11 t=6; ADD R0,R2 8 t=4;
ADD R0,R3 8 t=2; SUB R0,R0 8 t=0; SUB R0,R1 8 t=-5; SUB R0,R2 17 t=-2;
SUB R0,R3 8 t=-4; MAX R0,R0 8 t=1; MAX R0,R1 14 t=6; MAX R0,R2 15 t=6;
MAX R0,R3 8 t=2; MIN R0,R0 8 t=1; MIN R0,R1 8 t=0; MIN R0,R2 8 t=1;
MIN R0,R3 8 t=0.
d!=0 (60): every 1-op program with d!=0 leaves R0=e0, hence C=8
t=1 for all 60 (verified: R1-DNONZERO-ALL8 = 1).
Winner: SUB R0,R2 (bytes 2,0,2, index 34), C=17, t=-2, gain 9.
UNIQUE across all 80 (next best 15). No 1-op reaches 18.

Round 2 (from [SUB R0,R2]; baseline C=17 t=-2), all 80 appends:
d=0 (20): CPY 17 t=-2; CPY R0,R1 17 t=-2; CPY R0,R2 17 t=-2;
CPY R0,R3 17 t=-2; ADD R0,R0 13 t=1; ADD R0,R1 18 t=3; ADD R0,R2 8 t=1;
ADD R0,R3 17 t=-1; SUB R0,R0 17 t=-4; SUB R0,R1 15 t=-8;
SUB R0,R2 17 t=-5; SUB R0,R3 14 t=-1; MAX R0,R0 8 t=1; MAX R0,R1 11 t=3;
MAX R0,R2 8 t=3; MAX R0,R3 11 t=3; MIN R0,R0 17 t=-2; MIN R0,R1 17 t=-2;
MIN R0,R2 17 t=-2; MIN R0,R3 17 t=-2.
d!=0 (60): each writes R1/R2/R3, R0 stays e0-e2, hence C=17 t=-2
for all 60 (verified: R2-DNONZERO-ALL17 = 1).
Winner: ADD R0,R1 (bytes 1,0,1, index 17), C=18, t=3, gain 1.
UNIQUE across all 80 (all others at most 17, gain 0).

Round 3 (from [SUB R0,R2, ADD R0,R1]; baseline C=18 t=3): no program
can exceed 18 on the train set (sum of positive margins = 6+5+4+3
= 18, verified POS-MARGIN-BOUND = 18); d!=0 appends keep R0 =
e0-e2+e1 and score exactly 18. Best append C=18, gain 0, stop.

M1 = [SUB R0,R2, ADD R0,R1] (bytes 2,0,2,1,0,1),
threshold t=3, train C=18.

M0 = [ADD R0,R2] (bytes 1,0,2): train C=8, t=4 (poor; revision target).

Recency-confound discriminator (frozen): under naive recency
attribution (an arrival at step a credited to the deployment at
step a instead of step a-3), round-1 candidate k>=3 would receive
C_{k-3}; the winner would be index 37 = bytes 2,1,1 (SUB R1,R1) at
score 17 (verified by dcheck: RECENCY-WINNER idx=37 bytes=2,1,1).
Correct ledger attribution must yield bytes 2,0,2. Any other winner
bytes void the build (F-MISATTR).

Menu controls (experiment-side, via w_conseq at frozen thresholds):
SUM 9 t=12; MAX 9 t=6; MIN 8 t=0; FIRST 8 t=1; LAST 8 t=0.
Each strictly below 18.

Test deployment of M1 at t=3 (single delayed deployment on TEST):
arrival 3 steps later with C = 7 + 0 + 5 + 0 = 12.

ARM-NOM (M slot wiped): C=0, no deployment, NO_DECISION.

## 5. Frozen stage protocol

All learner stages run inside the learner's l_experiment (the driver
teaches X train+test, seeds M0, creates the world state, then runs
arms and the kill-bar summary). One deployment per step; every step
polls w_arrive for the current step before deploying.

- STAGE 0 (inherit, delayed): compute M0's 8 candidate thresholds
  from recalled episodes. Deploy (M0, t_j) at steps 0..7 (tag=1),
  polling each step; drain 3 steps. Arrivals at steps 3..10 carry
  (sched=j, C_j, t_j). First-max over attributed scores: M0-FIT t=4
  C=8. l_observe(8): bestC=8, conf=1. Log M0-DEPLOY-ATTR C=8
  bestC=8 conf=1.
- STAGE 1 (construct + revise, delayed): CURFIT of the empty program
  (tag=5): t=1 C=8. Round 1: 80 candidates (tag=2), each delayed-fit
  through the channel; after the drain pick the strictly-positive
  gain winner; log D-ROUND 1 base=8 eval=80 win=2,0,2 gain=9
  score=17 t=-2. Round 2 (tag=3): D-ROUND 2 base=17 eval=80
  win=1,0,1 gain=1 score=18 t=3. Round 3 (tag=4): D-ROUND 3 base=18
  eval=80 stop. Log M1-BUILT n=2 t=3 C=18 prog=2,0,2,1,0,1. Since
  18 > 8: REVISE old-C=8 new-C=18; Mprev = [1,0,2] sup=1; M = M1
  gen=1; bestC=18; conf=2. Driver runs experiment-side uniqueness
  sweep (via w_conseq): exactly 1 of the 20 d=0 appends reaches
  C=18.
- STAGE 2 (deploy held-out, delayed): snapshot M bytes. Deploy
  (M1, t=3) on TEST at step S (tag=6); drain; arrival at S+3 carries
  (sched=S, C=12, t=3); attribute to M1; l_deploy_eval(12):
  retained=1. Log TEST-DEPLOY C=12 retained=1; M-BYTES-EQUAL 1.
- ARMS: ARM-NOM (wiped M, C=0, no deployment); ARM-MENU (5 controls
  via w_conseq, each C <= 9).

## 6. Kill bars

- K-D1 (delayed consequence-only verification): shell grep audit on
  the committed `learner_d.zag` returns zero case-insensitive hits
  for each pattern in section 7, AND the only world-side symbols
  referenced in learner_d.zag are `w_sched` and `w_arrive`, AND the
  frozen shell awk audit over the run log verifies every ATTR line:
  arr - sched == 3 and a DEPLOY line exists at step sched with the
  same tag, and no ATTR-BAD line appears. No immediate consequence,
  per-episode outcome, margin, or correct-answer token crosses the
  learner boundary.
- K-D2 (delayed consequence attributed; wrong M revised): log shows
  M0-FIT t=4 C=8 with 8 ATTR lines at sched 0..7; M0-DEPLOY-ATTR
  C=8 bestC=8 conf=1; D-ROUND 1 win=2,0,2 gain=9 score=17 t=-2;
  D-ROUND 2 win=1,0,1 gain=1 score=18 t=3; D-ROUND 3 stop;
  M1-BUILT n=2 t=3 C=18 prog=2,0,2,1,0,1; REVISE old-C=8 new-C=18;
  Mprev holds prog 1,0,2 with sup=1.
- K-D3 (delayed test consequence attributed; correct M retained):
  TEST-DEPLOY C=12; retained=1; an ATTR line with tag=6 and
  sched = arr - 3; M-BYTES-EQUAL 1 (n, gen, sup, pad + 24 program
  bytes identical across the test deployment; threshold excluded
  per the FORAGE ERRATUM-1 rationale).
- K-D4 (necessity): ARM-NOM C=0 AND every menu control C <= 9 < 18.
- K-D5 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict L3-DELAYED-COMPLETE requires all five PASS with no
falsifier firing.

## 7. Frozen audit specs (run on the committed learner_d.zag and logs)

Grep audit: each pattern must return zero matches (grep -c -i == 0)
in learner_d.zag:
1. `label` (no label token anywhere in the learner)
2. `expected` (zero in the learner verification path)
3. `w_tab` (no episode table access)
4. `margin` (no world-hidden margin computation)
5. `correct` (no correctness bit; only coin scalars)
6. `_mode` (zero modes allowed)
7. `bridge` (never used in code at all)
8. `handler` (never used in code at all)
9. `w_conseq` (the immediate oracle is experiment-side only)
10. `w_val` (no episode table access)
11. `menu_` (no control aggregation in the learner)

Positive symbol check: `grep -o 'w_[a-z_]*' learner_d.zag | sort -u`
must list exactly `w_arrive` and `w_sched`.

Awk attribution audit (frozen logic; runs over each run log):
for every line matching `^ATTR `: require (arr - sched) == 3;
require a line matching `^DEPLOY step=<sched> ` with the same tag;
fail the run if any ATTR-BAD line exists or any check fails.

## 8. Frozen falsifiers

- F-LABEL: any section-7 grep pattern matches in learner_d.zag, the
  positive symbol check lists anything but w_sched/w_arrive, or
  learner_d.zag references another world-side symbol. Voids the
  whole build.
- F-ATTR: the awk attribution audit fails on any run log, or any
  ATTR-BAD line appears. Voids the whole build.
- F-MISATTR: round-1 winner bytes are not exactly 2,0,2 (the frozen
  recency-misattribution winner is 2,1,1). Voids the whole build.
- F-ONEOP: round-1 best C >= 18, or final program has n != 2, or the
  round-1 winner bytes are not 2,0,2. Voids the whole build.
- F-NOTUNIQUE: the experiment-side append sweep finds != 1
  candidates at C=18 among the 20 d=0 appends. Voids the whole
  build.
- F-MENU-WIN: any menu control C >= 18. Voids K-D4.
- F-NOREVISE: no REVISE event, Mprev wrong, or M1 bytes !=
  2,0,2,1,0,1. Voids K-D2.
- F-NORETAIN: retained != 1, TEST-DEPLOY C != 12, or M bytes differ
  across the test deployment. Voids K-D3.
- F-NONDET: the three runs differ by even one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the whole build.

## 9. Determinism spec

No RNG. Fixed candidate order (op-major), fixed threshold order
(sorted unique outputs ascending, first-max), fixed poll/deploy
order (poll current step, then at most one deploy per step), fixed
drain of exactly N steps per fit, single preallocated output buffer,
one raw-syscall write. 3/3 byte-identical required.

## 10. Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, ledger, delayed
  sweep, and confidence policy are researcher-authored generic
  machinery, disclosed in section 3. The claim is that the
  intermediate's FORM (2,0,2,1,0,1) is source-underdetermined and
  history-determined, and that its VERIFICATION used only delayed
  downstream coin consequences correctly attributed to the
  deployments that caused them.
- One world family (delayed settlement). No generality claim beyond
  it. Stochastic consequences are not tested; only deterministic
  delayed ones.
- The driver and world files are new experiment-side code; only the
  delayed consequence-query boundary constrains the learner.
- This build targets the five L3-DELAYED bars above. It does not
  claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
