# PREREG: Verification Machinery at Delay N=1 (VERIFY-N1)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/verify_n1/`
only.
Worker: Verify N1 Worker (subagent, 2026-10-02).
Parent mandate: test the verification machinery with N=1 delay
(envelope boundary).
Boundary from the completed builds: L3-DELAYED-STOCHASTIC
(L3-DELAYED-STOCHASTIC-COMPLETE) showed ledger + K=64 averaging works
on SETTLE-DS (delay N=3, seed 7000); VERIFY-TRANSFER
(VERIFY-TRANSFER-COMPLETE) showed the SAME unmodified learner works
on SETTLE-DN2 (delay N=2, seed 109). Open: does N=1 work? Is the
transfer envelope N<=3 inclusive of N=1, the minimal positive delay
with the least in-flight overlap? This experiment isolates exactly
that boundary: a new world SETTLE-DN1 with delay N=1 (not 2, not 3)
and the SAME noise (seed 109, draws in {-2,-1,0,1,2}), while the
learner file is a BYTE-IDENTICAL copy of the frozen
`verify_transfer/learner_ds.zag` (sha256
45ad35d892d629971a4679ffd2085b8bd54bf9c328d1e8eb1cededcc3ef3ae65,
itself byte-identical to `l3_delayed_stochastic/learner_ds.zag`),
not modified, not rewritten, not adapted. If the machinery is
general, the unmodified learner attributes every arrival by schedule
step through the N=1 timing and averages the noise to the same
intermediate form.

## 1. What is being tested

Whether the ledger + averaging verification machinery works at the
minimal positive delay N=1 with ZERO learner changes. The learner
deploys a candidate at step s with sample index k and learns its
noisy aggregate coin consequence only at step s+1, while deploying
further candidates at step s+1 (poll happens before the deploy at
each step). It must:

(a) deploy the inherited wrong intermediate M0 through the new
    delayed noisy channel, attribute each arriving noisy consequence
    to the M0 deployment step that scheduled it (arr - sched == 1,
    not 2, not 3), accumulate exactly K=64 attributed arrivals per
    threshold, and record the averaged consequence;
(b) construct a fresh M1 guided ONLY by K-sample sums of delayed
    noisy consequences under the same noise, attributing every
    arrival by schedule step, demanding a significance margin
    (gain > K/2) before appending, and revise (replace M0) because
    avgC(M1) > avgC(M0);
(c) deploy M1 on held-out episodes through the N=1 delayed noisy
    channel, observe its K-sample summed consequence 1 step after
    the last deployment, attribute it to the M1 deployment, and
    retain M1 byte-identical.

The consequence reaching the learner is always a K-sample SUM of
noisy aggregate coin totals, each sample arriving 1 step after its
own deployment. The learner never observes a label, a margin, an
immediate consequence, the seed, or a noise draw. Its log labels
("DS-ROUND", "K1-ROUND", "M0-FIT", etc.) are unchanged because the
file is unchanged; only the arrival TIMING (arr - sched == 1)
differs.

Transfer envelope (disclosed): the frozen learner drains exactly 3
steps after each fit and after the test deployment, and polls every
step before deploying. A world delay N with 1 <= N <= 3 is therefore
covered by the unmodified poll/drain schedule; N=1 is the smallest
positive delay the unmodified machinery supports, and it exercises
the LEAST in-flight overlap (exactly one deployment in flight at
each poll during continuous deployment, versus two at N=2 and three
at N=3), so ledger routing by schedule step (never recency) is
tested at the envelope edge where a recency heuristic would be
hardest to distinguish from correct attribution. The boundary claim
is exactly: the envelope N<=3 includes N=1.

The K=1 control arm runs the IDENTICAL learner code with K=1 through
the N=1 delayed channel and must fail to select M1, proving
averaging is load-bearing at N=1 too.

## 2. Frozen world (SETTLE-DN1; environment, hidden from learner)

Same frozen train episodes 1..8 and test episodes 9..12, same hidden
margin rule margin = e0+e1-e2, as l3_verify / l3_delayed /
l3_stochastic / l3_delayed_stochastic / verify_transfer. Frozen
delay: N = 1 step.

Noise model (disclosed, frozen; SAME spec as SETTLE-DN2): each
deployment carries a sample index k (0..K-1, assigned by the learner
at schedule time) and its arrival reports

  C_true(prog,n,t,region) + nz_draw(109, acc, k)

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
    return (h mod 5) - 2

Draws are in {-2,-1,0,1,2}: symmetric, zero-mean, at most 2 coins per
deployment. Each draw is a pure function of the frozen seed, the
query key (region, program bytes, threshold), and the sample index:
independent draws per deployment, order-independent, fully
deterministic across runs. Delay changes WHEN a draw is observed,
never its value. The learner never receives the seed and never
computes a draw.

Seed selection (inherited, frozen): seed 109 is the first candidate
seed satisfying ALL of (i) K=64 selects M1 with winner bytes 2,0,2
then 1,0,1, round-3 maxgain <= 32, c1 > c0; (ii) K=1 appends exactly
[2,0,2] then stalls (round-2 maxgain <= 0), never selecting M1;
(iii) test sum > 0; (iv) all menu sums < c1 (established by the
verify_transfer worker; seeds 100..108 rejected there). Every
criterion is a function of the noise draws only, which are
delay-independent, so seed 109 carries over unchanged. The
independent checker (/tmp/n1check.zag, pure Zag, separate code path:
independently written register machine, reimplemented noise spec,
fresh threshold/sum/selection logic, NO delay, NO channel) re-derived
every number below from scratch before this prereg.

World-side symbols (same names and signatures the frozen learner
calls; the learner file is unchanged, so the names MUST match):
- `w_init_dn1()` -> world-state buffer (opaque schedule store,
  262144 slots x 40 bytes [prog 24B][n i32][thr i32][region i32]
  [k i32]; n = -1 marks empty; environment, not learner memory).
- `w_sched_ds(wst, step, prog, n, thr, region, k)`: schedule one
  deployment. Returns NOTHING. No consequence is observable at
  schedule time. Learner-facing. The only way the learner deploys.
  (Name kept identical to the frozen learner's call site.)
- `w_arrive_ds(wst, step, out) -> i32`: if a deployment was
  scheduled at step-1, compute its noisy aggregate coin consequence
  NOW and write out[0]=sched_step, out[4]=coins, out[8]=thr,
  out[12]=k; return 1. Else return 0 and write nothing.
  Learner-facing. (Name kept identical to the frozen learner's call
  site. THE delay constant is the only behavioral difference from
  SETTLE-DN2.)
- `w_conseq_det(prog, n, thr, region) -> i32`: deterministic
  immediate aggregate coins. EXPERIMENT-SIDE ONLY (the uniqueness
  sweep). The learner must never reference it (K-N1-1 audit).
- `w_val`, `w_n`, `w_id`, `w_margin`, `menu_agg`, `menu_name`,
  `nz_acc`, `nz_draw`: experiment-side tables/helpers (driver only;
  forbidden in learner).

Frozen oracle rule for threshold candidacy (unchanged): candidate
thresholds are the sorted unique program outputs on the evaluated
episode set, ascending; first-max wins. Deterministic; the only
randomness is the seeded counter-based noise.

## 3. Frozen learner machinery (byte-identical copy, disclosed)

`learner_ds.zag` in this directory will be a BYTE-IDENTICAL copy of
the frozen `verify_transfer/learner_ds.zag` (sha256 above): X
episode recall (sequences only), register-machine executor (ops
0=CPY 1=ADD 2=SUB 3=MAX 4=MIN, R0..R3 preloaded, output R0),
in-flight LEDGER (per step: job tag u8, candidate index u8,
threshold index u8, sample index u8; 262144-step capacity), per-job
score tables (threshold values, attributed K-sample sums, per-cell
arrival counts), delayed noisy threshold sweep (deploy one
(prog,t,k) per step, K deployments per threshold, poll arrivals each
step, drain 3 steps, count-verify, first-max over attributed sums),
greedy construction over 80 candidates per round (op-major order
0..4, d 0..3, s 0..3; append requires measured gain > K/2;
8-instruction cap), M slot bookkeeping [n,u8 gen,u8 sup,u8 pad,
threshold i32, 24 program bytes] plus Mprev, and the confidence
policy. The learner calls exactly two world-side symbols:
`w_sched_ds` and `w_arrive_ds`. No other world reference exists.

Attribution plus averaging rule (frozen, unchanged): when
w_arrive_ds(step) reports (sched_step, C, thr, k), the learner reads
ledger[sched_step] -> (tag, cand, thri, k2), requires k2 == k, ADDS
C into that job/candidate/threshold score cell, increments its
arrival count, and logs
`ATTR arr=<step> sched=<sched_step> tag=<tag> k=<k> C=<C> t=<thr>`.
Every deployment logs
`DEPLOY step=<s> tag=<tag> cand=<c> thri=<j> k=<k> t=<t> region=<r>`.
After each fit's 3-step drain (which covers the N=1 delay with two
spare poll steps), the learner verifies every threshold cell received
exactly K arrivals; any shortfall logs `ATTR-COUNT-BAD`. Correct
attribution under the new timing means sched_step = arr - 1, the tag
and k match the DEPLOY line at step sched_step (checked by the
frozen shell awk audit, section 7), and every score is a sum of
exactly K properly attributed arrivals.

Frozen confidence policy (generic, no modes; unchanged):
- l_observe(C): if C > bestC { bestC = C; conf++; } (conf unchanged
  otherwise).
- l_revise after construction: if C_new > bestC { Mprev = incumbent
  with sup=1; M = new with gen = old gen + 1; bestC = C_new; conf++;
  log REVISE }.
- l_deploy_eval(C): retained = (C > 0) ? 1 : 0; M never modified here.

Frozen K=64 for the main arm. The control arm runs the IDENTICAL
learner code with K=1 (hence margin K/2 = 0, the plain positive-gain
rule) through the N=1 delayed channel: a learner that trusts a
single noisy delayed deployment. Its round log lines use the K1-ROUND
label (a log-label parameter only; identical code path, disclosed).

The inherited wrong intermediate M0 = [ADD R0,R2] (bytes 1,0,2) is
seeded experiment-side; the learner does not invent it. Its
consequence is measured through the N=1 delayed noisy channel, not
stipulated.

## 4. Frozen numbers (independent check BEFORE this commit)

Derived by /tmp/n1check.zag (pure Zag, separate code path, no delay,
no channel: immediate noisy K-sums from the frozen noise spec) before
this prereg was written. Every number equals the VERIFY-TRANSFER
frozen number, as required by the delay-independence of the noise
draws: the implementation must reproduce every number below through
the NEW delayed noisy channel (N=1); any deviation is a falsifier,
not a tuning opportunity. Arrival TIMING is the new variable under
test (arr - sched == 1 on every ATTR line).

Seed 109, K=64, margin 32. All C values are 64-sample sums of
delayed noisy arrivals under the same noise.

M0 = [ADD R0,R2] (bytes 1,0,2): fit t=4, sum=509 (8 thresholds).

Round 1 (from empty; base sum=512, t=1), 80 candidates:
winner SUB R0,R2 (bytes 2,0,2), gain=573, sum=1085, t=-2,
margin (winner sum minus runner-up sum) = 189 > 0. Gain 573 > 32.

Round 2 (from [SUB R0,R2]; base sum=1085), 80 appends:
winner ADD R0,R1 (bytes 1,0,1), gain=66, sum=1151, t=3,
margin = 58 > 0. Gain 66 > 32.

Round 3 (from [SUB R0,R2, ADD R0,R1]; base sum=1151): best measured
gain = 6 <= 32: stop. No third append.

M1 = [SUB R0,R2, ADD R0,R1] (bytes 2,0,2,1,0,1), n=2, t=3,
sum=1151. REVISE: 1151 > 509.

K=1 control arm (same code, K=1, margin 0, N=1 delayed channel):
K1-EMPTY t=1 sum=8; K1-ROUND 1 winner SUB R0,R2 (bytes 2,0,2),
gain=11, sum=19, t=-2, mgn=3; K1-ROUND 2 maxgain=0 (not > 0): stop.
K1-BUILT n=1 prog=2,0,2; K1-SELECT-M1 0. It does NOT select M1.

Test deployment of M1 at t=3 on held-out episodes 9..12, K=64
delayed noisy deployments: sum=771 > 0.

Menu controls (experiment-side, immediate noisy K=64 sums, train):
SUM 578, MAX 576, MIN 510, FIRST 512, LAST 508. Each < 1151.
(Delay shifts arrival time only, never values; the immediate noisy
oracle is the honest experiment-side control.)

Experiment-side uniqueness sweep (deterministic): exactly 1 of the
20 d=0 appends after [SUB R0,R2] reaches C=18.

ARM-NOM (M slot wiped): C=0, no deployment, NO_DECISION.

Step budget (checker-counted): main arm about 110233 deployments +
drains (same count as SETTLE-DS/SETTLE-DN2: the deployment schedule
is delay-independent); K=1 arm about 1500 steps; total under 112000
steps. Ledger and world-store capacity 262144 steps (2.3x headroom).
Output buffer 16MB (about 112000 DEPLOY+ATTR line pairs).

## 5. Frozen stage protocol

All learner stages run inside the learner's l_experiment (the driver
teaches X train+test, seeds M0, creates the world state, then runs
arms and the kill-bar summary). One deployment per step; every step
polls w_arrive_ds for the current step before deploying. Arrivals
now land 1 step after deployment.

- STAGE 0 (inherit, delayed noisy): M0's 8 candidate thresholds
  from recalled episodes. For each threshold, K=64 deployments
  (k=0..63) at consecutive steps (tag=1), polling each step; drain 3
  steps (covers N=1 with two spare polls). Each arrival is
  attributed by (sched_step, k) and added to its threshold cell;
  counts verified at 64. First-max over attributed sums: M0-FIT t=4
  C=509. l_observe(509): bestC=509, conf=1. Log M0-DEPLOY-ATTR C=509
  bestC=509 conf=1.
- STAGE 1 (construct + revise, delayed noisy): CURFIT of the empty
  program (tag=5): t=1 C=512. Round 1 (tag=2): 80 candidates, each a
  delayed noisy K-sample fit; log DS-ROUND 1 base=512 eval=80
  win=2,0,2 gain=573 score=1085 t=-2 mgn=189. Round 2 (tag=3):
  DS-ROUND 2 base=1085 eval=80 win=1,0,1 gain=66 score=1151 t=3
  mgn=58. Round 3 (tag=4): DS-ROUND 3 base=1151 eval=80 stop
  maxgain=6. Log M1-BUILT n=2 t=3 C=1151 prog=2,0,2,1,0,1. Since
  1151 > 509: REVISE old-C=509 new-C=1151; Mprev = [1,0,2] sup=1;
  M = M1 gen=1; bestC=1151; conf=2. Driver runs experiment-side
  uniqueness sweep (via w_conseq_det): exactly 1 of the 20 d=0
  appends reaches C=18.
- STAGE 2 (deploy held-out, delayed noisy): snapshot M bytes.
  Deploy (M1, t=3) on TEST region with K=64 (k=0..63) at consecutive
  steps (tag=6); drain 3 steps; the 64 arrivals attribute to the M1
  deployment steps (arr - sched == 1) and sum to 771;
  l_deploy_eval(771): retained=1. Log TEST-DEPLOY C=771 retained=1;
  M-BYTES-EQUAL 1.
- STAGE 1b (single-sample control, delayed noisy): fresh learner
  state, teach X train, fresh world state, construct with K=1
  through the N=1 delayed channel. Log K1-ROUND 1 base=8 eval=80
  win=2,0,2 gain=11 score=19 t=-2 mgn=3; K1-ROUND 2 base=19 eval=80
  stop maxgain=0; K1-BUILT n=1 prog=2,0,2; K1-SELECT-M1 0.
- ARMS: ARM-NOM (wiped M, C=0, no deployment); ARM-MENU (5 controls,
  experiment-side immediate noisy K=64 sums, each < 1151).

## 6. Kill bars

- K-N1-1 (new-channel consequence-only verification): shell grep
  audit on the committed byte-identical `learner_ds.zag` returns
  zero case-insensitive hits for each pattern in section 7, AND the
  only world-side symbols referenced in learner_ds.zag are
  `w_sched_ds` and `w_arrive_ds`. No immediate consequence,
  per-episode outcome, margin, seed, or noise draw crosses the
  learner boundary. (The file is unchanged from the frozen sibling;
  the audit re-runs on the copy.)
- K-N1-2 (every arrival attributed under the new timing; every score
  a true K-sum): the frozen shell awk audit over each run log
  verifies every ATTR line: arr - sched == 1, a DEPLOY line exists
  at step sched with the same tag and same k, and no ATTR-BAD or
  ATTR-COUNT-BAD line appears. Every threshold score used in
  construction is therefore a sum of exactly 64 properly attributed
  noisy arrivals under delay N=1.
- K-N1-3 (averaging is load-bearing at N=1): log shows K1-BUILT n=1
  prog=2,0,2 with K1-SELECT-M1 0 (the single-sample delayed learner
  does not select M1), while the K=64 arm selects M1 per K-N1-4.
  Driver requires both.
- K-N1-4 (M constructed via the N=1 delayed noisy channel): log
  shows M0-FIT t=4 C=509; DS-ROUND 1 win=2,0,2 gain=573 score=1085
  t=-2 mgn=189; DS-ROUND 2 win=1,0,1 gain=66 score=1151 t=3 mgn=58;
  DS-ROUND 3 stop maxgain=6; M1-BUILT n=2 t=3 C=1151
  prog=2,0,2,1,0,1; REVISE old-C=509 new-C=1151; Mprev holds prog
  1,0,2 with sup=1; UNIQ-APPEND-18 n=1.
- K-N1-5 (retained under the N=1 delay+noise): TEST-DEPLOY C=771;
  retained=1; the 64 ATTR lines with tag=6 satisfy
  sched = arr - 1; M-BYTES-EQUAL 1 (n, gen, sup, pad + 24 program
  bytes identical across the test deployment; threshold excluded per
  the FORAGE ERRATUM-1 rationale).
- K-N1-6 (necessity): ARM-NOM C=0 AND every menu control sum < 1151
  (frozen: 578, 576, 510, 512, 508).
- K-N1-7 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict VERIFY-N1-COMPLETE requires all seven PASS with no
falsifier firing.

Frozen prediction (not a kill bar; confirmed or refuted in REPORT):
the N=1 run log equals the VERIFY-TRANSFER run log byte-for-byte
except (a) every ATTR line's arr field is exactly 1 less, and
(b) the N1-* run markers replace the VT-* markers. This is the
mechanical consequence of the timing-only theory: the deployment
schedule is delay-independent, every (sched,k,C,t) tuple is
delay-independent, and only arr = sched + N changes.

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

Awk attribution audit (frozen logic in audit_attr_n1.awk; runs over
each run log): for every line matching `^ATTR `: require
(arr - sched) == 1; require a line matching `^DEPLOY step=<sched> `
with the same tag AND the same k; fail the run if any ATTR-BAD or
ATTR-COUNT-BAD line exists or any check fails or no ATTR line exists.

## 8. Frozen falsifiers

- F-N1-LABEL: any section-7 grep pattern matches in learner_ds.zag,
  the positive symbol check lists anything but w_sched_ds /
  w_arrive_ds, or learner_ds.zag references another world-side
  symbol. Voids the whole build.
- F-N1-ATTR: the awk attribution audit fails on any run log, or any
  ATTR-BAD or ATTR-COUNT-BAD line appears. Voids the whole build.
- F-N1-MISATTR: round-1 winner bytes are not exactly 2,0,2 (the
  attribution-failure signature). Voids the whole build.
- F-N1-NOAVG: the K=1 arm selects M1 (n=2 with bytes 2,0,2,1,0,1), or
  K1-BUILT deviates from the frozen n=1 prog=2,0,2. Averaging would
  not be load-bearing. Voids the whole build.
- F-N1-WRONGM: round-1 winner bytes != 2,0,2, round-2 winner bytes !=
  1,0,1, final n != 2, or any frozen sum/gain/t/threshold in
  section 4 is not reproduced exactly. Voids the whole build.
- F-N1-NOMARGIN: round-3 maxgain > 32 (no stop), or any winner margin
  <= 0. Voids the whole build.
- F-N1-NOREVISE: no REVISE event, Mprev wrong, or M1 bytes !=
  2,0,2,1,0,1. Voids K-N1-4.
- F-N1-NORETAIN: retained != 1, TEST-DEPLOY C != 771, or M bytes differ
  across the test deployment. Voids K-N1-5.
- F-N1-MENU-WIN: any menu control sum >= 1151. Voids K-N1-6.
- F-N1-NONDET: the three runs differ by even one byte. Voids the build.
- F-N1-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the whole build.

## 9. Determinism spec

Seeded counter-based PRNG (section 2): every noise draw is a pure
function of the frozen seed, the query key, and the sample index, so
there is no RNG stream state and no evaluation-order dependence.
Fixed delay N=1, fixed candidate order (op-major), fixed threshold
sweep (sorted unique outputs ascending, first-max), fixed K=64 /
K=1, fixed poll/deploy order (poll current step, then at most one
deploy per step), fixed drain of exactly 3 steps per fit (covers
N=1), single preallocated output buffer, one raw-syscall write. 3/3
byte-identical required.

## 10. Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, ledger, delayed
  noisy sweep, K-sample averaging loop, the gain margin K/2, the
  confidence policy, and the counter-based noise model with its seed
  are researcher-authored generic machinery. The boundary claim is
  that the intermediate's FORM (2,0,2,1,0,1) is constructed through
  the minimal-delay channel with the learner file byte-identical:
  each arrival attributed by schedule step under N=1 timing (never
  recency) and each score averaged over exactly 64 attributed
  arrivals under the same noise.
- One new world (SETTLE-DN1). The transfer demonstrated is across
  delay characteristics within the settlement world family (same
  episodes, same hidden rule, same noise as SETTLE-DN2); no claim
  beyond that.
- N=1 exercises the least in-flight overlap of the tested envelope:
  exactly one deployment in flight at each poll during continuous
  deployment. Passing here plus N=2 and N=3 passing bounds the
  envelope 1<=N<=3 for the frozen poll/drain schedule.
- The K1-ROUND log tag text is a log-label parameter of the
  identical construct code path, disclosed here; it is not a
  behavioral mode. The "DS-" log labels persist because the learner
  file is unchanged; they name the code path, not the world.
- The driver and world files are new experiment-side code; only the
  delayed noisy consequence-query boundary constrains the learner.
- This build targets the seven VERIFY-N1 bars above. It does not
  claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
