# PREREG: L3 Invention with Delayed AND Stochastic Consequences (L3-DELAYED-STOCHASTIC)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l3_delayed_stochastic/`
only.
Worker: L3 Delayed-Stochastic Worker (subagent, 2026-10-02).
Parent mandate: test L3 invention when consequences are BOTH delayed
and stochastic.
Boundary from the sibling builds: L3-DELAYED (L3-DELAYED-COMPLETE)
showed the learner can attribute consequences delayed 3 steps through
a ledger, with deterministic values. L3-STOCHASTIC
(L3-STOCHASTIC-COMPLETE) showed the learner can average K=64 noisy
samples to select M1, with immediate arrival. Open: does the learner
handle BOTH at once, attributing each noisy arrival to the deployment
that caused it AND averaging enough arrivals to resolve the true
value? This experiment isolates exactly that conjunction: the same
settlement world family, same episode tables, same hidden margin
rule, same op basis, but the ONLY learner-facing consequence channel
delays every consequence by N=3 steps AND corrupts each one with
seeded noise.

## 1. What is being tested

Whether the learner can invent the intermediate M AND verify it when
every consequence observation arrives 3 steps late AND carries noise.
The learner deploys a candidate at step s with sample index k and
learns its noisy aggregate coin consequence only at step s+3, while
deploying further candidates at steps s+1, s+2. It must:

(a) deploy the inherited wrong intermediate M0 through the
    delayed noisy channel, attribute each arriving noisy consequence
    to the M0 deployment step that scheduled it (not to a more
    recent deployment), accumulate exactly K=64 attributed arrivals
    per threshold, and record the averaged consequence;
(b) construct a fresh M1 guided ONLY by K-sample sums of delayed
    noisy consequences, attributing every arrival by schedule step,
    demanding a significance margin (gain > K/2) before appending,
    and revise (replace M0) because avgC(M1) > avgC(M0);
(c) deploy M1 on held-out episodes through the delayed noisy
    channel, observe its K-sample summed consequence 3 steps after
    the last deployment, attribute it to the M1 deployment, and
    retain M1 byte-identical.

The consequence reaching the learner is always a K-sample SUM of
noisy aggregate coin totals, each sample arriving 3 steps after its
own deployment. The learner never observes a label, a margin, an
immediate consequence, the seed, or a noise draw.

The two failure modes this discriminates: (a) recency
misattribution, crediting an arrival at step a to the deployment at
step a rather than step a-3 (the L3-DELAYED failure mode); (b)
single-sample trust, acting on one noisy deployment instead of
averaging (the L3-STOCHASTIC failure mode). The K=1 control arm runs
the IDENTICAL learner code with K=1 through the delayed channel and
must fail to select M1, proving averaging is load-bearing under
delay too.

## 2. Frozen world (SETTLE-DS; environment, hidden from learner)

Same frozen train episodes 1..8 and test episodes 9..12, same hidden
margin rule margin = e0+e1-e2, as l3_verify / l3_delayed /
l3_stochastic. Frozen delay: N = 3 steps.

Noise model (disclosed, frozen; identical spec to l3_stochastic):
each deployment carries a sample index k (0..K-1, assigned by the
learner at schedule time) and its arrival reports

  C_true(prog,n,t,region) + nz_draw(7000, acc, k)

where C_true is the deterministic aggregate coin consequence and

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

Draws are in {-1,0,1}: symmetric, zero-mean, at most 1 coin per
deployment. Each draw is a pure function of the frozen seed, the
query key (region, program bytes, threshold), and the sample index:
independent draws per deployment, order-independent, fully
deterministic across runs. Delay changes WHEN a draw is observed,
never its value. The learner never receives the seed and never
computes a draw.

Seed selection: seed 7000 is inherited frozen from l3_stochastic,
where it was the first seed tried and satisfied (i) K=64 selects M1
with the L3-VERIFY winner bytes and round structure, (ii) K=1 fails
to select M1. Because the draws are pure functions of (seed, key,
k) and delay preserves values, the same seed yields the same
K-sample sums here; the independent checker (/tmp/dscheck.zag)
re-derived every number below from scratch before this prereg.

World-side symbols:
- `w_init_ds()` -> world-state buffer (opaque schedule store,
  262144 slots x 40 bytes [prog 24B][n i32][thr i32][region i32]
  [k i32]; n = -1 marks empty; environment, not learner memory).
- `w_sched_ds(wst, step, prog, n, thr, region, k)`: schedule one
  deployment. Returns NOTHING. No consequence is observable at
  schedule time. Learner-facing. The only way the learner deploys.
- `w_arrive_ds(wst, step, out) -> i32`: if a deployment was
  scheduled at step-3, compute its noisy aggregate coin consequence
  NOW and write out[0]=sched_step, out[4]=coins, out[8]=thr,
  out[12]=k; return 1. Else return 0 and write nothing.
  Learner-facing. Polling a future step early is impossible: the
  slot is empty until its step arrives, and the learner protocol
  polls only the current step.
- `w_conseq_det(prog, n, thr, region) -> i32`: deterministic
  immediate aggregate coins. EXPERIMENT-SIDE ONLY (the uniqueness
  sweep). The learner must never reference it (K-DS1 audit).
- `w_val`, `w_n`, `w_id`, `w_margin`, `menu_agg`, `menu_name`,
  `nz_acc`, `nz_draw`: experiment-side tables/helpers (driver only;
  forbidden in learner).

Frozen oracle rule for threshold candidacy (unchanged): candidate
thresholds are the sorted unique program outputs on the evaluated
episode set, ascending; first-max wins. Deterministic; the only
randomness is the seeded counter-based noise.

## 3. Frozen learner machinery (new, disclosed, researcher-authored)

`learner_ds.zag` is NEW code for this experiment. Disclosed generic
machinery: X episode recall (sequences only), register-machine
executor (ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN, R0..R3 preloaded,
output R0), in-flight LEDGER (per step: job tag u8, candidate index
u8, threshold index u8, sample index u8; 262144-step capacity),
per-job score tables (threshold values, attributed K-sample sums,
per-cell arrival counts), delayed noisy threshold sweep (deploy one
(prog,t,k) per step, K deployments per threshold, poll arrivals each
step, drain N steps, count-verify, first-max over attributed sums),
greedy construction over 80 candidates per round (op-major order
0..4, d 0..3, s 0..3; append requires measured gain > K/2;
8-instruction cap), M slot bookkeeping [n,u8 gen,u8 sup,u8 pad,
threshold i32, 24 program bytes] plus Mprev, and the confidence
policy below. The learner calls exactly two world-side symbols:
`w_sched_ds` and `w_arrive_ds`. No other world reference exists in
learner_ds.zag.

Job tags (frozen): 1=M0FIT, 2=R1, 3=R2, 4=R3, 5=CURFIT, 6=M1TEST.

Attribution plus averaging rule (frozen): when w_arrive_ds(step)
reports (sched_step, C, thr, k), the learner reads
ledger[sched_step] -> (tag, cand, thri, k2), requires k2 == k, ADDS
C into that job/candidate/threshold score cell, increments its
arrival count, and logs
`ATTR arr=<step> sched=<sched_step> tag=<tag> k=<k> C=<C> t=<thr>`.
Every deployment logs
`DEPLOY step=<s> tag=<tag> cand=<c> thri=<j> k=<k> t=<t> region=<r>`.
After each fit's 3-step drain, the learner verifies every threshold
cell received exactly K arrivals; any shortfall logs
`ATTR-COUNT-BAD`. Correct attribution means sched_step = arr - 3,
the tag and k match the DEPLOY line at step sched_step (checked by
the frozen shell awk audit, section 7), and every score is a sum of
exactly K properly attributed arrivals.

Frozen confidence policy (generic, no modes; same as the siblings):
- l_observe(C): if C > bestC { bestC = C; conf++; } (conf unchanged
  otherwise).
- l_revise after construction: if C_new > bestC { Mprev = incumbent
  with sup=1; M = new with gen = old gen + 1; bestC = C_new; conf++;
  log REVISE }.
- l_deploy_eval(C): retained = (C > 0) ? 1 : 0; M never modified here.

Frozen K=64 for the main arm. The control arm runs the IDENTICAL
learner code with K=1 (hence margin K/2 = 0, the plain positive-gain
rule) through the delayed channel: a learner that trusts a single
noisy delayed deployment. Its round log lines use the K1-ROUND
label (a log-label parameter only; identical code path, disclosed).

The inherited wrong intermediate M0 = [ADD R0,R2] (bytes 1,0,2) is
seeded experiment-side; the learner does not invent it. Its
consequence is measured through the delayed noisy channel, not
stipulated.

## 4. Frozen numbers (independent check BEFORE this commit)

Derived by /tmp/dscheck.zag (pure Zag, separate code path: closed-
form program evaluation, no register machine, reimplemented noise
spec, fresh threshold/sum/selection logic) before this prereg was
written. The implementation must reproduce every number below
through the DELAYED NOISY channel; any deviation is a falsifier,
not a tuning opportunity. K-sample sums are identical to the
l3_stochastic frozen values because the draws are pure functions of
(seed, key, k) and delay preserves values; arrival TIMING is the new
variable under test.

Seed 7000, K=64, margin 32. All C values are 64-sample sums of
delayed noisy arrivals.

M0 = [ADD R0,R2] (bytes 1,0,2): fit t=4, sum=513 (8 thresholds).

Round 1 (from empty; base sum=510, t=1), 80 candidates:
winner SUB R0,R2 (bytes 2,0,2), gain=578, sum=1088, t=-2,
margin (winner sum minus runner-up sum) = 192 > 0. Gain 578 > 32.

Round 2 (from [SUB R0,R2]; base sum=1088), 80 appends:
winner ADD R0,R1 (bytes 1,0,1), gain=63, sum=1151, t=3,
margin = 61 > 0. Gain 63 > 32.

Round 3 (from [SUB R0,R2, ADD R0,R1]; base sum=1151): best measured
gain = 3 <= 32: stop. No third append.

M1 = [SUB R0,R2, ADD R0,R1] (bytes 2,0,2,1,0,1), n=2, t=3,
sum=1151. REVISE: 1151 > 513.

K=1 control arm (same code, K=1, margin 0, delayed channel):
K1-EMPTY t=1 sum=7; K1-ROUND 1 winner SUB R0,R2 (bytes 2,0,2),
gain=11, sum=18, t=-2; K1-ROUND 2 maxgain=0 (not > 0): stop.
K1-BUILT n=1 prog=2,0,2; K1-SELECT-M1 0. It does NOT select M1.

Test deployment of M1 at t=3 on held-out episodes 9..12, K=64
delayed noisy deployments: sum=769 > 0.

Menu controls (experiment-side, immediate noisy K=64 sums, train):
SUM 574, MAX 576, MIN 514, FIRST 514, LAST 510. Each < 1151.
(Delay shifts arrival time only, never values; the immediate noisy
oracle is the honest experiment-side control.)

Experiment-side uniqueness sweep (deterministic): exactly 1 of the
20 d=0 appends after [SUB R0,R2] reaches C=18.

ARM-NOM (M slot wiped): C=0, no deployment, NO_DECISION.

Step budget (checker-counted): main arm 110233 deployments +
drains; K=1 arm about 1500 steps; total under 112000 steps.
Ledger and world-store capacity 262144 steps (2.3x headroom).
Output buffer 16MB (about 112000 DEPLOY+ATTR line pairs).

## 5. Frozen stage protocol

All learner stages run inside the learner's l_experiment (the driver
teaches X train+test, seeds M0, creates the world state, then runs
arms and the kill-bar summary). One deployment per step; every step
polls w_arrive_ds for the current step before deploying.

- STAGE 0 (inherit, delayed noisy): M0's 8 candidate thresholds
  from recalled episodes. For each threshold, K=64 deployments
  (k=0..63) at consecutive steps (tag=1), polling each step; drain 3
  steps. Each arrival is attributed by (sched_step, k) and added to
  its threshold cell; counts verified at 64. First-max over
  attributed sums: M0-FIT t=4 C=513. l_observe(513): bestC=513,
  conf=1. Log M0-DEPLOY-ATTR C=513 bestC=513 conf=1.
- STAGE 1 (construct + revise, delayed noisy): CURFIT of the empty
  program (tag=5): t=1 C=510. Round 1 (tag=2): 80 candidates, each a
  delayed noisy K-sample fit; log DS-ROUND 1 base=510 eval=80
  win=2,0,2 gain=578 score=1088 t=-2 mgn=192. Round 2 (tag=3):
  DS-ROUND 2 base=1088 eval=80 win=1,0,1 gain=63 score=1151 t=3
  mgn=61. Round 3 (tag=4): DS-ROUND 3 base=1151 eval=80 stop
  maxgain=3. Log M1-BUILT n=2 t=3 C=1151 prog=2,0,2,1,0,1. Since
  1151 > 513: REVISE old-C=513 new-C=1151; Mprev = [1,0,2] sup=1;
  M = M1 gen=1; bestC=1151; conf=2. Driver runs experiment-side
  uniqueness sweep (via w_conseq_det): exactly 1 of the 20 d=0
  appends reaches C=18.
- STAGE 2 (deploy held-out, delayed noisy): snapshot M bytes.
  Deploy (M1, t=3) on TEST region with K=64 (k=0..63) at consecutive
  steps (tag=6); drain 3 steps; the 64 arrivals attribute to the M1
  deployment steps and sum to 769; l_deploy_eval(769): retained=1.
  Log TEST-DEPLOY C=769 retained=1; M-BYTES-EQUAL 1.
- STAGE 1b (single-sample control, delayed noisy): fresh learner
  state, teach X train, fresh world state, construct with K=1
  through the delayed channel. Log K1-ROUND 1 base=7 eval=80
  win=2,0,2 gain=11 score=18 t=-2; K1-ROUND 2 base=18 eval=80 stop
  maxgain=0; K1-BUILT n=1 prog=2,0,2; K1-SELECT-M1 0.
- ARMS: ARM-NOM (wiped M, C=0, no deployment); ARM-MENU (5 controls,
  experiment-side immediate noisy K=64 sums, each < 1151).

## 6. Kill bars

- K-DS1 (delayed-noisy consequence-only verification): shell grep
  audit on the committed `learner_ds.zag` returns zero
  case-insensitive hits for each pattern in section 7, AND the only
  world-side symbols referenced in learner_ds.zag are `w_sched_ds`
  and `w_arrive_ds`. No immediate consequence, per-episode outcome,
  margin, seed, or noise draw crosses the learner boundary.
- K-DS2 (every arrival attributed; every score a true K-sum): the
  frozen shell awk audit over each run log verifies every ATTR
  line: arr - sched == 3, a DEPLOY line exists at step sched with
  the same tag and same k, and no ATTR-BAD or ATTR-COUNT-BAD line
  appears. Every threshold score used in construction is therefore
  a sum of exactly 64 properly attributed noisy arrivals.
- K-DS3 (averaging is load-bearing under delay): log shows
  K1-BUILT n=1 prog=2,0,2 with K1-SELECT-M1 0 (the single-sample
  delayed learner does not select M1), while the K=64 arm selects
  M1 per K-DS4. Driver requires both.
- K-DS4 (correct M constructed via the delayed noisy channel): log
  shows M0-FIT t=4 C=513; DS-ROUND 1 win=2,0,2 gain=578 score=1088
  t=-2 mgn=192; DS-ROUND 2 win=1,0,1 gain=63 score=1151 t=3 mgn=61;
  DS-ROUND 3 stop maxgain=3; M1-BUILT n=2 t=3 C=1151
  prog=2,0,2,1,0,1; REVISE old-C=513 new-C=1151; Mprev holds prog
  1,0,2 with sup=1; UNIQ-APPEND-18 n=1.
- K-DS5 (retained under delay+noise): TEST-DEPLOY C=769;
  retained=1; the 64 ATTR lines with tag=6 satisfy sched = arr - 3;
  M-BYTES-EQUAL 1 (n, gen, sup, pad + 24 program bytes identical
  across the test deployment; threshold excluded per the FORAGE
  ERRATUM-1 rationale).
- K-DS6 (necessity): ARM-NOM C=0 AND every menu control sum < 1151
  (frozen: 574, 576, 514, 514, 510).
- K-DS7 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict L3-DELAYED-STOCHASTIC-COMPLETE requires all seven PASS with
no falsifier firing.

## 7. Frozen audit specs (run on the committed learner_ds.zag and logs)

Grep audit: each pattern must return zero matches (grep -c -i == 0)
in learner_ds.zag:
1. `label` (no label token anywhere in the learner)
2. `expected` (zero in the learner verification path)
3. `w_tab` (no episode table access)
4. `margin` (no world-hidden margin computation)
5. `correct` (no correctness bit; only coin scalars)
6. `_mode` (zero modes allowed)
7. `bridge` (never used in code at all)
8. `handler` (never used in code at all)
9. `w_conseq` (no immediate oracle reference; the _ds channel
   symbols do not match this pattern)
10. `w_val` (no episode table access)
11. `menu_` (no control aggregation in the learner)
12. `nz_` (no seed and no noise-draw computation in the learner)

Positive symbol check: `grep -o 'w_[a-z_]*' learner_ds.zag | sort -u`
must list exactly `w_arrive_ds` and `w_sched_ds`.

Awk attribution audit (frozen logic in audit_attr_ds.awk; runs over
each run log): for every line matching `^ATTR `: require
(arr - sched) == 3; require a line matching `^DEPLOY step=<sched> `
with the same tag AND the same k; fail the run if any ATTR-BAD or
ATTR-COUNT-BAD line exists or any check fails or no ATTR line exists.

## 8. Frozen falsifiers

- F-LABEL: any section-7 grep pattern matches in learner_ds.zag,
  the positive symbol check lists anything but w_sched_ds /
  w_arrive_ds, or learner_ds.zag references another world-side
  symbol. Voids the whole build.
- F-ATTR: the awk attribution audit fails on any run log, or any
  ATTR-BAD or ATTR-COUNT-BAD line appears. Voids the whole build.
- F-MISATTR: round-1 winner bytes are not exactly 2,0,2 (the
  attribution-failure signature; the ledger design is unchanged from
  L3-DELAYED, where the recency failure mode was established).
  Voids the whole build.
- F-NOAVG: the K=1 arm selects M1 (n=2 with bytes 2,0,2,1,0,1), or
  K1-BUILT deviates from the frozen n=1 prog=2,0,2. Averaging would
  not be load-bearing. Voids the whole build.
- F-WRONGM: round-1 winner bytes != 2,0,2, round-2 winner bytes !=
  1,0,1, final n != 2, or any frozen sum/gain/t/threshold in
  section 4 is not reproduced exactly. Voids the whole build.
- F-NOMARGIN: round-3 maxgain > 32 (no stop), or any winner margin
  <= 0. Voids the whole build.
- F-NOREVISE: no REVISE event, Mprev wrong, or M1 bytes !=
  2,0,2,1,0,1. Voids K-DS4.
- F-NORETAIN: retained != 1, TEST-DEPLOY C != 769, or M bytes differ
  across the test deployment. Voids K-DS5.
- F-MENU-WIN: any menu control sum >= 1151. Voids K-DS6.
- F-NONDET: the three runs differ by even one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the whole build.

## 9. Determinism spec

Seeded counter-based PRNG (section 2): every noise draw is a pure
function of the frozen seed, the query key, and the sample index, so
there is no RNG stream state and no evaluation-order dependence.
Fixed delay N=3, fixed candidate order (op-major), fixed threshold
sweep (sorted unique outputs ascending, first-max), fixed K=64 /
K=1, fixed poll/deploy order (poll current step, then at most one
deploy per step), fixed drain of exactly N steps per fit, single
preallocated output buffer, one raw-syscall write. 3/3 byte-identical
required.

## 10. Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, ledger, delayed
  noisy sweep, K-sample averaging loop, the gain margin K/2, the
  confidence policy, and the counter-based noise model with its seed
  are researcher-authored generic machinery, disclosed in sections
  2 and 3. The claim is that the intermediate's FORM (2,0,2,1,0,1)
  is source-underdetermined and history-determined, and that its
  construction and verification used only delayed noisy downstream
  coin consequences: each arrival attributed by schedule step (never
  recency) and each score averaged over exactly 64 attributed
  arrivals.
- One world family (delayed noisy settlement). No generality claim
  beyond it.
- The noise is small (at most 1 coin per deployment) relative to the
  round-1 gain; the binding test is the round-2 gain of 1 coin per
  deployment, which single samples cannot resolve and 64-sample
  averaging can, now with every sample arriving 3 steps late.
- The K1-ROUND log label is a log-label parameter of the identical
  construct code path, disclosed here; it is not a behavioral mode.
- The driver and world files are new experiment-side code; only the
  delayed noisy consequence-query boundary constrains the learner.
- This build targets the seven L3-DELAYED-STOCHASTIC bars above. It
  does not claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
