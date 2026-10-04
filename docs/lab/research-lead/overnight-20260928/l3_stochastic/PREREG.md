# PREREG: L3 Invention with Stochastic (Noisy) Consequences (L3-STOCHASTIC)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l3_stochastic/` only.
Worker: L3 Stochastic Worker (subagent, 2026-10-02).
Parent mandate: test L3 invention with STOCHASTIC consequences
(Micah boundary note: "stochastic untested"). L3-VERIFY used
immediate deterministic consequences; L3-DELAYED used delayed
deterministic consequences. Open question: can the learner verify
M when consequences are noisy?

## 1. What is being tested

Whether the learner can invent the intermediate M AND verify it when
every consequence observation is corrupted by noise. The world is the
same SETTLE settlement task as L3-VERIFY (same frozen episode tables,
same hidden margin rule margin = e0+e1-e2), but the coin oracles now
return C_true + noise, with noise drawn from a seeded counter-based
PRNG (section 2). A single deployment therefore gives an unreliable
estimate of a candidate's value. The learner must average over
multiple deployments (K=64) to estimate true value, and must demand a
significance margin before acting on a measured gain. The learner must:

(a) deploy an inherited wrong intermediate M0 through the noisy
    channel, observe its averaged consequence, and record it;
(b) construct a fresh M1 guided ONLY by averaged noisy consequence
    queries, compare averaged consequences, and revise (replace M0)
    because avgC(M1) > avgC(M0);
(c) deploy M1 on held-out episodes through the noisy channel,
    observe a positive averaged consequence, and retain it
    byte-identical.

The consequence reaching the learner is always a K-sample SUM of
noisy aggregate coin totals (order-identical to the K-sample mean).
The learner never observes a label, a per-episode outcome, the seed,
or the noise draws.

## 2. Frozen world (SETTLE-NZ; environment, hidden from learner)

Same frozen train episodes 1..8 and test episodes 9..12 as
l3_verify/PREREG.md section 2. Hidden margin rule unchanged.

Noise model (disclosed, frozen): each oracle call takes a sample
index k (0..K-1) and returns

  w_conseq_train_nz(prog,n,t,k) = C_true(prog,n,t) + nz_draw(7000, acc, k)
  w_conseq_test_nz(prog,n,t,k)  = C_true(prog,n,t) + nz_draw(7000, acc, k)

where C_true is the deterministic aggregate coin consequence
(l3_verify world.zag w_conseq_train/test logic), and

  nz_acc(region,key,kn,t):
    a = t + 1007 + region*1000003            (region 0=train, 1=test)
    for i in 0..kn*3-1: a = (a*31 + key[i]) mod 2147483647
    a = (a*31 + kn) mod 2147483647
    return a
  nz_draw(seed,acc,k):
    h = seed
    h = (h*1103515245 + acc) mod 2147483647
    h = (h*1103515245 + k) mod 2147483647
    h = (h*1103515245 + 12345) mod 2147483647
    return (h mod 3) - 1

All intermediate values are kept non-negative (i64 arithmetic, mod
2147483647 after each step), so each draw is in {-1,0,1}: symmetric,
zero-mean, per-deployment coin noise of at most 1 coin. The draw is a
pure function of the frozen seed, the query key (region, program
bytes, threshold), and the sample index: independent draws per
deployment, order-independent, fully deterministic across runs. The
learner never receives the seed and never computes a draw.

Seed selection rule (disclosed, frozen): seeds were tried in order
from 7000 upward; the first seed at which (i) the K=64 construction
yields exactly M1 = [SUB R0,R2, ADD R0,R1] with the L3-VERIFY winner
bytes and round structure, and (ii) the K=1 control arm fails to
select M1, was frozen. Seed 7000 was the first seed tried and it
satisfied both; no further search was needed.

## 3. Frozen learner machinery (new, disclosed, researcher-authored)

`learner_s.zag` is NEW code for this experiment. Disclosed generic
machinery: everything in l3_verify learner.zag (X recall, register
machine ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN, greedy construction over 80
candidates per round in op-major order, 8-instruction cap,
M/Mprev slot bookkeeping, the confidence policy), PLUS the noisy
consequence machinery below. The learner calls exactly two world-side
symbols: `w_conseq_train_nz` and `w_conseq_test_nz`. It never calls
the deterministic oracles (they do not exist in world_s.zag).

New generic machinery (frozen):

- l_avg_eval(prog,n,t,K,train): returns the SUM over k=0..K-1 of the
  noisy oracle outputs for (prog,t). Ordering of sums is identical to
  ordering of K-sample means (K fixed and positive). The K-sample loop
  is the averaging mechanism; it is the only way the learner observes
  consequences.
- fit_conseq_nz: threshold sweep exactly as in L3-VERIFY, but each
  candidate threshold is scored by l_avg_eval (a K-sample sum).
  First-max over ascending unique program outputs wins. Returns the
  best sum and its threshold.
- construct: greedy loop as in L3-VERIFY, but scores are K-sample
  sums, and the append rule requires gain > K/2 (integer division):
  the measured gain (a sum over K deployments) must exceed half a coin
  per deployment on average. Rationale (disclosed): with noisy gains,
  the deterministic strictly-positive-gain rule would append
  noise-driven junk; the margin is a fixed significance rule that
  depends only on K, not on the world. K=64 gives margin 32.
- l_deploy_nz(prog,n,t,K,test): K-sample sum through the noisy oracle
  for deployment observations (M0 deploy, test deploy).

Frozen K=64 for the main arm. The control arm runs the IDENTICAL
learner code with K=1 (hence margin K/2 = 0, i.e. the plain
positive-gain rule): a learner that trusts a single noisy deployment.

## 4. Frozen numbers (independent check BEFORE this commit)

Derived by /tmp/scheck.zag (pure Zag, separate code path: direct
value formulas, no register machine, fresh threshold/sum/selection
logic; the K=64 winner sums were additionally cross-checked against
an independent register-machine evaluation: XCHECK-BAD=0). The
implementation must reproduce every number below; any deviation is a
falsifier, not a tuning opportunity.

Seed 7000, K=64, margin 32. All C values are 64-sample sums.

M0 = [ADD R0,R2] (bytes 1,0,2): fit t=4, sum=513. Deploy sum=513
(same query key, identical draws).

Round 1 (from empty; base sum=510), 80 candidates:
winner SUB R0,R2 (bytes 2,0,2), gain=578, sum=1088, t=-2,
margin (winner sum minus runner-up sum) = 192 > 0. Gain 578 > 32.

Round 2 (from [SUB R0,R2]; base sum=1088), 80 appends:
winner ADD R0,R1 (bytes 1,0,1), gain=63, sum=1151, t=3,
margin = 61 > 0. Gain 63 > 32.

Round 3 (from [SUB R0,R2, ADD R0,R1]; base sum=1151): best measured
gain = 3 <= 32: stop. No third append.

M1 = [SUB R0,R2, ADD R0,R1] (bytes 2,0,2,1,0,1), n=2, t=3,
sum=1151. REVISE: 1151 > 513.

K=1 control arm (same code, K=1, margin 0): final n=1,
prog=2,0,2 (stalls after round 1; the single-sample round-2 gains
cannot clear the noise). It does NOT select M1.

Test deployment of M1 at t=3 on held-out episodes 9..12, K=64:
sum=769 > 0.

Menu controls (experiment-side, K=64 noisy sums, train):
SUM 574, MAX 576, MIN 514, FIRST 514, LAST 510. Each < 1151.

ARM-NOM (M slot wiped): C=0, no decision.

## 5. Frozen stage protocol

- STAGE 0 (inherit): teach X train 1..8. Seed M0 (1,0,2)
  experiment-side. Learner fits M0's threshold by averaged noisy
  consequence (t=4, C=513), deploys M0 via l_deploy_nz K=64
  (C=513), l_observe(513): bestC=513, conf=1. Log M0-DEPLOY C=513.
- STAGE 1 (construct + revise): learner constructs from empty through
  the noisy channel only (K=64). Log C-ROUND lines with the section-4
  numbers, M1-BUILT n=2 t=3 C=1151 prog=2,0,2,1,0,1. Since
  1151 > 513: REVISE old-C=513 new-C=1151; Mprev = [1,0,2] sup=1;
  M = M1 gen=1; bestC=1151; conf=2.
- STAGE 1b (single-sample control): fresh learner state, teach X
  train, construct with K=1. Log K1-BUILT n=1 prog=2,0,2 and
  K1-SELECT-M1 0.
- STAGE 2 (deploy held-out): teach X test 9..12. Snapshot M bytes.
  Deploy M1 at t=3 via w_conseq_test_nz K=64: C=769.
  l_deploy_eval(769): retained=1. M-BYTES-EQUAL 1.
- ARMS: ARM-NOM (wiped M, C=0); ARM-MENU (5 controls, K=64 noisy
  sums, each < 1151).

## 6. Kill bars

- K-S1 (noisy-channel hygiene): shell grep audit on the committed
  `learner_s.zag` returns zero case-insensitive hits for each pattern
  in section 7, AND `grep -c 'w_conseq_train('` and
  `grep -c 'w_conseq_test('` on learner_s.zag are both 0 (the
  deterministic oracles are never referenced), AND the only
  world-side symbols referenced are `w_conseq_train_nz` and
  `w_conseq_test_nz`. Every construction score in the run log is a
  64-sample sum.
- K-S2 (averaging is load-bearing): log shows K1-BUILT n=1
  prog=2,0,2 with K1-SELECT-M1 0 (the single-sample learner does not
  select M1), while the K=64 arm selects M1 per K-S3. Driver requires
  both.
- K-S3 (correct M constructed via noisy channel despite noise): log
  shows M0-DEPLOY C=513; construction trace with exactly two
  positive-gain rounds (gains 578 and 63, both > 32) and the frozen
  winner bytes (2,0,2 then 1,0,1); round 3 stops (maxgain 3 <= 32);
  M1-BUILT n=2 t=3 C=1151 prog=2,0,2,1,0,1; REVISE old-C=513
  new-C=1151; Mprev holds prog 1,0,2 with sup=1.
- K-S4 (retained under noise): TEST-DEPLOY C=769; retained=1;
  M structural bytes (n, gen, sup, pad + 24 program bytes; threshold
  excluded per the FORAGE ERRATUM-1 rationale) byte-identical before
  and after the test deployment.
- K-S5 (necessity): ARM-NOM C=0 AND every menu control sum < 1151
  (frozen: 574, 576, 514, 514, 510).
- K-S6 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict L3-STOCHASTIC-COMPLETE requires all six PASS with no
falsifier firing.

## 7. Frozen K-S1 grep audit spec (run on the committed learner_s.zag)

Each pattern must return zero matches (grep -c -i == 0):
1. `label` 2. `expected` 3. `w_tab` 4. `margin` 5. `correct`
6. `_mode` 7. `bridge` 8. `handler`
Plus (case-sensitive): `w_conseq_train(` == 0 and
`w_conseq_test(` == 0 (deterministic oracles never referenced; the
_nz suffixed symbols do not match these patterns).

## 8. Frozen falsifiers

- F-LABEL: any section-7 pattern matches in learner_s.zag, or
  learner_s.zag references a world-side symbol other than the two
  noisy oracles. Voids the whole build.
- F-NOAVG: the K=1 arm selects M1 (n=2 with bytes 2,0,2,1,0,1), or
  K1-BUILT deviates from the frozen n=1 prog=2,0,2. Averaging would
  not be load-bearing. Voids the whole build.
- F-WRONGM: round-1 winner bytes != 2,0,2, round-2 winner bytes !=
  1,0,1, final n != 2, or any frozen sum/gain/t in section 4 is not
  reproduced exactly. Voids the whole build.
- F-NOMARGIN: round-3 maxgain > 32 (no stop), or any winner margin
  <= 0. Voids the whole build.
- F-NOREVISE: no REVISE event, Mprev wrong, or M1 bytes !=
  2,0,2,1,0,1. Voids K-S3.
- F-NORETAIN: retained != 1, TEST-DEPLOY C != 769, or M bytes differ
  across the test deployment. Voids K-S4.
- F-MENU-WIN: any menu control sum >= 1151. Voids K-S5.
- F-NONDET: the three runs differ by even one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the whole build.

## 9. Determinism spec

Seeded counter-based PRNG (section 2): every noise draw is a pure
function of the frozen seed, the query key, and the sample index, so
there is no RNG stream state and no evaluation-order dependence.
Fixed candidate order (op-major), fixed threshold sweep (sorted unique
outputs ascending, first-max), fixed K=64, single preallocated output
buffer, one raw-syscall write. 3/3 byte-identical required.

## 10. Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, K-sample averaging
  loop, the gain margin K/2, the confidence policy, and the
  counter-based noise model with its seed are researcher-authored
  generic machinery, disclosed in sections 2 and 3. The claim is that
  the intermediate's FORM (2,0,2,1,0,1) is source-underdetermined and
  history-determined, that its construction and verification used only
  noisy downstream coin consequences, and that averaging over repeated
  deployments (not single samples) is what makes the selection work.
- One world family (settlement). No generality claim beyond it.
- The noise is small (at most 1 coin per deployment) relative to the
  round-1 gain; the binding test is the round-2 gain of 1 coin per
  deployment, which single samples cannot resolve and 64-sample
  averaging can.
- The driver and world files are new experiment-side code; only the
  noisy consequence-query boundary constrains the learner.
- This build targets the six L3-STOCHASTIC bars above. It does not
  claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
