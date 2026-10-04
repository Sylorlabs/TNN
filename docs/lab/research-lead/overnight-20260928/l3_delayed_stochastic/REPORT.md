# REPORT: L3 Invention with Delayed AND Stochastic Consequences (L3-DELAYED-STOCHASTIC)

Verdict: **L3-DELAYED-STOCHASTIC-COMPLETE** (all seven frozen kill bars
pass, no falsifier fires).

Date: 2026-10-02. Worker: L3 Delayed-Stochastic Worker.
Prereg: `PREREG.md` (frozen fdac1ee31; committed alone before any
implementation existed; zero amendments). Determinism: 3/3
byte-identical runs (sha256
ec65aa17397ee55a72412d830792747a884df41076c5327a29d2fc89f39ffa92).

## What was built

Four new files, concatenated to `ds_full.zag`, compiled with the
pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`) to
`ds_bin`:

- `learner_ds.zag`: NEW delayed+noisy learner (no frozen ancestor;
  it fuses the L3-DELAYED ledger with the L3-STOCHASTIC K-averaging).
  Generic machinery + learned state only: X episode recall (sequences
  only), register-machine executor (ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN),
  in-flight LEDGER (per deployment step: job tag, candidate index,
  threshold index, sample index; 262144-step capacity), per-job score
  tables holding threshold values, attributed K-sample sums, and
  per-cell arrival counts, delayed noisy threshold sweep (K
  deployments per threshold, one per step, arrival polling each step,
  N=3 drain, per-cell count verification, first-max over attributed
  sums), greedy construction over 80 candidates per round (append
  requires measured gain > K/2; 8-instruction cap), M/Mprev slot
  bookkeeping, and the generic confidence policy (l_observe /
  l_revise / l_deploy_eval). It calls exactly two world-side symbols,
  `w_sched_ds` and `w_arrive_ds`: the delayed noisy consequence
  channel. `w_sched_ds` returns nothing; each noisy consequence
  arrives exactly 3 steps after its deployment and is routed by
  ledger lookup on (schedule step, sample index), never by recency;
  each threshold score provably sums exactly K routed arrivals.
- `world_ds.zag`: new SETTLE-DS environment (experiment side only).
  Frozen episode tables (identical to l3_verify / l3_delayed /
  l3_stochastic), hidden margin rule margin = e0+e1-e2, the delayed
  noisy schedule store (`w_init_ds`, `w_sched_ds`, `w_arrive_ds`),
  the seeded counter-based noise (seed 7000; identical spec to
  l3_stochastic; each draw a pure function of seed, query key, and
  sample index, so delay preserves values), the experiment-side
  deterministic immediate oracle `w_conseq_det` (uniqueness sweep
  only; forbidden to the learner), and the five menu controls.
- `driver_ds.zag`: new experiment-side driver. Teaches X train+test,
  seeds the inherited wrong M0, creates the world state, runs the
  learner's `l_experiment` (K=64 main arm: inherit, construct+revise,
  deploy held-out), evaluates the NOM and MENU arms (menu via
  experiment-side immediate noisy K=64 sums; delay shifts arrival
  time only, never values), runs the K=1 single-sample control arm
  through the delayed channel, runs the experiment-side uniqueness
  sweep, and prints the kill-bar summary. It never invents the
  intermediate: all construction goes through the learner's delayed
  noisy queries.
- `audit_attr_ds.awk`: frozen attribution audit over the run logs
  (every ATTR: arr - sched == 3, DEPLOY at sched with same tag and
  same k, no ATTR-BAD / ATTR-COUNT-BAD).

Output via one preallocated 16MB buffer and a single raw syscall
write. 110337 deployments, 110337 arrivals, every arrival attributed
by (schedule step, sample index).

## The delayed noisy verification trace (K-DS1 through K-DS5)

Stage 0: M0 = [ADD R0,R2] (bytes 1,0,2, seeded experiment-side) is
fit through the delayed noisy channel only: 8 thresholds x 64
samples deployed at consecutive steps, arrivals interleaved 3 steps
later (e.g. `ATTR arr=3 sched=0 tag=1 k=0 C=9 t=4` arriving while
later samples are still in flight), each arrival routed by
(sched_step, k) and added to its threshold cell. First-max over the
attributed 64-sample sums:

```
M0-FIT t=4 C=513
M0-DEPLOY-ATTR C=513 bestC=513 conf=1
```

Stage 1: the learner constructs from the empty program. Every
candidate score is a 64-sample sum of delayed noisy arrivals; no
label, no immediate consequence, no seed, and no draw is ever
consulted:

```
DS-ROUND 1 base=510 eval=80 win=2,0,2 gain=578 score=1088 t=-2 mgn=192
DS-ROUND 2 base=1088 eval=80 win=1,0,1 gain=63 score=1151 t=3 mgn=61
DS-ROUND 3 base=1151 eval=80 stop maxgain=3
M1-BUILT n=2 t=3 C=1151 prog=2,0,2,1,0,1
REVISE old-C=513 new-C=1151
M n=2 gen=1 sup=0 t=3 prog=2,0,2,1,0,1,...
MPREV n=1 gen=0 sup=1 prog=1,0,2,...
UNIQ-APPEND-18 n=1
```

Round 1: SUB R0,R2 is the winner (gain 578 > 32; winner-to-runner-up
192). Round 2: ADD R0,R1 is the winner (gain 63 > 32; margin 61).
Round 3 stops (maxgain 3 <= 32). The final intermediate
M1 = [SUB R0,R2, ADD R0,R1] (R0 = e0+e1-e2 exactly) appears nowhere
in the learner source. Because 1151 > 513, the learner revises: M0
moves to Mprev with sup=1, M1 becomes incumbent (bestC=1151,
conf=2).

Attribution check: the round-1 winner bytes are 2,0,2, not any
misattribution artifact. F-MISATTR does not fire.

Stage 1b (control): the identical learner code with K=1 through the
delayed channel:

```
K1-ROUND 1 base=7 eval=80 win=2,0,2 gain=11 score=18 t=-2 mgn=4
K1-ROUND 2 base=18 eval=80 stop maxgain=0
K1-BUILT n=1 prog=2,0,2
K1-SELECT-M1 0
```

The single-sample delayed learner stalls at n=1 and does not select
M1: averaging is load-bearing under delay, not just under noise.

Stage 2: M1 deployed 64 times (k=0..63) on the four held-out
episodes at t=3:

```
TEST-DEPLOY C=769 retained=1
M-BYTES-EQUAL 1
```

The 64 noisy consequences arrive 3 steps after their deployments,
are routed by (schedule step, k), sum to 769 > 0, so the learner
retains M1; its structural bytes are byte-identical across the
deployment.

## Kill bars

- K-DS1 (delayed-noisy consequence-only verification): PASS. Shell
  grep audit on the committed `learner_ds.zag`: all 12 frozen
  patterns return 0 hits (label, expected, w_tab, margin, correct,
  _mode, bridge, handler, w_conseq, w_val, menu_, nz_;
  case-insensitive). The only world-side symbols referenced are
  `w_sched_ds` and `w_arrive_ds`. The verification path carries
  delayed noisy scalars only.
- K-DS2 (every arrival attributed; every score a true K-sum):
  PASS. The frozen awk attribution audit passes on all 3 run logs
  (ATTR-AUDIT PASS, nattr=110337 each): every ATTR line satisfies
  arr - sched == 3 with a matching DEPLOY tag and k, and no
  ATTR-BAD or ATTR-COUNT-BAD line exists. Every threshold score
  used in construction is therefore a sum of exactly 64 properly
  attributed noisy arrivals.
- K-DS3 (averaging is load-bearing under delay): PASS (in-Zag).
  K1-BUILT n=1 prog=2,0,2 with K1-SELECT-M1 0, while the K=64 arm
  selects M1 (revised=1, n=2, t=3, C=1151, bytes 2,0,2,1,0,1).
- K-DS4 (correct M constructed via the delayed noisy channel):
  PASS (in-Zag). M0-FIT t=4 C=513; DS-ROUND 1 win=2,0,2 gain=578
  score=1088 t=-2 mgn=192; DS-ROUND 2 win=1,0,1 gain=63 score=1151
  t=3 mgn=61; DS-ROUND 3 stop maxgain=3; M1-BUILT n=2 t=3 C=1151
  prog=2,0,2,1,0,1; REVISE old-C=513 new-C=1151; Mprev holds 1,0,2
  with sup=1; UNIQ-APPEND-18 n=1.
- K-DS5 (retained under delay+noise): PASS (in-Zag). TEST-DEPLOY
  C=769; retained=1; 64 ATTR lines with tag=6, each satisfying
  sched = arr - 3; M-BYTES-EQUAL 1 (n, gen, sup, pad + 24 program
  bytes identical; threshold excluded per the FORAGE ERRATUM-1
  rationale).
- K-DS6 (necessity): PASS (in-Zag). ARM-NOM C=0 (wiped M: no
  decisions, no deployment, no consequence); menu controls SUM 574,
  MAX 576, MIN 514, FIRST 514, LAST 510, all < 1151.
- K-DS7 (determinism): PASS. 3/3 byte-identical (sha256 above;
  11,449,091 bytes per run log).

No falsifier fired: F-LABEL (audit clean), F-ATTR (awk audit pass,
no ATTR-BAD / ATTR-COUNT-BAD), F-MISATTR (winner bytes 2,0,2),
F-NOAVG (K=1 arm n=1 prog=2,0,2, K1-SELECT-M1 0), F-WRONGM (every
frozen sum/gain/t/bytes reproduced exactly), F-NOMARGIN (round-3
maxgain 3 <= 32, winner margins 192 and 61), F-NOREVISE, F-NORETAIN,
F-MENU-WIN (best menu 576), F-NONDET, F-PYTHON (safebin PATH,
`which python3 python` empty for the whole task; all computation in
pure Zag).

## Pre-prereg independent verification

Before the prereg was written, all frozen numbers were derived by
an independent pure-Zag checker (/tmp/dscheck.zag: closed-form
program evaluation, no register machine, reimplemented noise spec,
fresh threshold/sum/selection logic). It confirmed: M0 at (t=4,
sum=513); empty at (t=1, sum=510); round-1 winner SUB R0,R2 at
(t=-2, sum=1088, gain=578, mgn=192); round-2 winner ADD R0,R1 at
(t=3, sum=1151, gain=63, mgn=61); round-3 maxgain 3; K=1 arm at
(n=1, prog=2,0,2) with round-1 (t=-2, sum=18, gain=11) and round-2
maxgain 0; M1 test deployment sum=769; menus at
574/576/514/514/510; and the step budget (110233 main-arm
deployments). The implementation reproduced every number through
the delayed noisy channel.

## Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, ledger, delayed
  noisy sweep, K-sample averaging loop, the gain bound K/2, the
  confidence policy, and the counter-based noise model with its seed
  are researcher-authored generic machinery (PREREG.md sections 2
  and 3). The claim is that M1's FORM is source-underdetermined and
  history-determined, and that its construction and verification
  used only delayed noisy downstream coin consequences: each
  arrival routed by schedule step (never recency) and each score
  averaged over exactly 64 routed arrivals.
- One world family (delayed noisy settlement). No generality claim
  beyond it.
- The K-sample sums are identical to the l3_stochastic frozen
  values because the draws are pure functions of (seed, key, k)
  and delay preserves values; the experiment isolates the
  conjunction: attribution under delay AND averaging under noise,
  simultaneously.
- The K1-ROUND log tag text is a log-label parameter of the
  identical construct code path, disclosed in the prereg; it is not
  a behavioral mode.
- This build targets the seven L3-DELAYED-STOCHASTIC bars. It does
  not claim Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.

## Files

All under `docs/lab/research-lead/overnight-20260928/l3_delayed_stochastic/`:
NAMECHECK.md (toolchain guard Step 0 + build record), PREREG.md
(frozen), REPORT.md (this file), learner_ds.zag, world_ds.zag,
driver_ds.zag, audit_attr_ds.awk, ds_full.zag, ds_bin,
ds_run1.txt, ds_run2.txt, ds_run3.txt.

Commit record:
- fdac1ee31: PREREG.md + NAMECHECK.md alone (frozen,
  pre-implementation).
- a183745df: implementation + REPORT (explicit pathspecs for
  `git add`; note: the shared branch index held 10 pre-staged
  contract_drift_detect files from a concurrent worker, which were
  swept into the same commit; no data lost, directories separate).
- Nothing pushed; branch tnn-native-lab.

## Shared-index incident note

During the implementation commit, the tnn-native-lab branch index
was shared with concurrent workers. Ten contract_drift_detect files
pre-staged by another worker were committed together with the ten
l3_delayed_stochastic deliverables under the l3_delayed_stochastic
commit message. All twenty files are intact in the repo; the two
directories are separate. No history rewrite was attempted (shared
branch, concurrent writers, and a WATCHDOG commit already sits on
top).
