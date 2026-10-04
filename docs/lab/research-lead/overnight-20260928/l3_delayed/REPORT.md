# REPORT: L3 Invention with Delayed Consequences (L3-DELAYED)

Verdict: **L3-DELAYED-COMPLETE** (all five frozen kill bars pass, no
falsifier fires).

Date: 2026-10-02. Worker: L3 Delayed Consequence Worker.
Prereg: `PREREG.md` (frozen 759be20f7; committed alone before any
implementation existed; zero amendments). Determinism: 3/3
byte-identical runs (sha256
02f8c47232f126f6dd9d180a958205cd89d2212a18522179dd387c7b71abab5c).

## What was built

Four Zag-adjacent files, concatenated to `delayed_full.zag`,
compiled with the pinned znc
(`src/tools/toolchain/znc_linux_x86_64_abed8aa1`) to `delayed_bin`:

- `learner_d.zag`: NEW delayed-ledger learner (no frozen ancestor;
  the L3-VERIFY learner is immediate-oracle based and read-only, so
  it could not be reused). Generic machinery + learned state only: X
  episode recall (sequences only), register-machine executor
  (ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN), in-flight LEDGER (per
  deployment step: job tag, candidate index, threshold index),
  per-job score tables, delayed threshold sweep (one (prog,t)
  deployment per step, arrival polling each step, N=3 drain,
  first-max over attributed scores), greedy construction over 80
  candidates per round (strictly positive gain, 8-instruction cap),
  M/Mprev slot bookkeeping, and the generic confidence policy
  (l_observe / l_revise / l_deploy_eval). It calls exactly two
  world-side symbols, `w_sched` and `w_arrive`: the delayed
  consequence channel. `w_sched` returns nothing; each consequence
  arrives exactly 3 steps after its deployment and is attributed by
  ledger lookup on the schedule step, never by recency.
- `world_d.zag`: new SETTLE-D environment (experiment side only).
  Frozen episode tables (identical to L3-VERIFY), hidden margin rule
  margin = e0+e1-e2, the delayed schedule store (`w_init`,
  `w_sched`, `w_arrive`), the experiment-side immediate oracle
  `w_conseq` (arms and the uniqueness sweep only; forbidden to the
  learner), and the five menu controls.
- `driver_d.zag`: new experiment-side driver. Teaches X train+test,
  seeds the inherited wrong M0, creates the world state, runs the
  learner's `l_experiment` (inherit, construct+revise, deploy
  held-out), evaluates the NOM and MENU arms, runs the
  experiment-side uniqueness sweep, and prints the kill-bar summary.
  It never invents the intermediate: all construction goes through
  the learner's delayed consequence queries.
- `audit_attr.awk`: frozen attribution audit over the run logs.

Output via one preallocated 1MB buffer and a single raw syscall
write. 1707 deployments, 1707 arrivals, every arrival attributed.

## The delayed verification trace (K-D1, K-D2)

Stage 0: M0 = [ADD R0,R2] (bytes 1,0,2, seeded experiment-side) is
fit through the delayed channel only: 8 threshold deployments at
steps 0..7, arrivals interleaved at steps 3..10 (each arrival
carrying its schedule step, e.g. `ATTR arr=3 sched=0 tag=1 C=8 t=4`
arriving while step-3's deployment is still in flight). First-max
over attributed scores:

```
M0-FIT t=4 C=8
M0-DEPLOY-ATTR C=8 bestC=8 conf=1
```

Stage 1: the learner constructs from the empty program. Every
candidate score is an aggregate coin consequence arriving 3 steps
after its deployment; no label and no immediate consequence is ever
consulted:

```
D-ROUND 1 base=8 eval=80 win=2,0,2 gain=9 score=17 t=-2
D-ROUND 2 base=17 eval=80 win=1,0,1 gain=1 score=18 t=3
D-ROUND 3 base=18 eval=80 stop
M1-BUILT n=2 t=3 C=18 prog=2,0,2,1,0,1
REVISE old-C=8 new-C=18
M n=2 gen=1 sup=0 t=3 prog=2,0,2,1,0,1,...
MPREV n=1 gen=0 sup=1 prog=1,0,2,...
UNIQ-APPEND-18 n=1
```

Round 1: SUB R0,R2 is the UNIQUE 17/80 candidate (gain 9; next best
15; all 60 d!=0 candidates at 8). Round 2: ADD R0,R1 is the UNIQUE
18/80 append (gain 1; all d!=0 appends at 17). Round 3 stops (no
program exceeds the positive-margin bound of 18). The final
intermediate M1 = [SUB R0,R2, ADD R0,R1] (R0 = e0+e1-e2 exactly)
appears nowhere in the learner source. Because 18 > 8, the learner
revises: M0 moves to Mprev with sup=1, M1 becomes incumbent
(bestC=18, conf=2).

Attribution check: under naive recency attribution the frozen
round-1 winner would have been index 37 = bytes 2,1,1 (verified by
the independent pre-prereg /tmp/dcheck.zag). The ledger attributed
correctly: winner bytes are 2,0,2. F-MISATTR does not fire.

Stage 2: M1 deployed once on the four held-out episodes at t=3:

```
DEPLOY step=2432 tag=6 cand=0 thri=0 t=3 region=1
ATTR arr=2435 sched=2432 tag=6 C=12 t=3
TEST-DEPLOY C=12 retained=1
M-BYTES-EQUAL 1
```

The consequence arrives 3 steps later, is attributed to the M1
deployment by schedule step, is positive, so the learner retains
M1; its structural bytes are byte-identical across the deployment.

## Kill bars

- K-D1 (delayed consequence-only verification): PASS. Shell grep
  audit on the committed `learner_d.zag`: all 11 frozen patterns
  return 0 hits (label, expected, w_tab, margin, correct, _mode,
  bridge, handler, w_conseq, w_val, menu_; case-insensitive). The
  only world-side symbols referenced are `w_sched` and `w_arrive`.
  The frozen awk attribution audit passes on all 3 run logs
  (ATTR-AUDIT PASS, nattr=1707 each): every ATTR line satisfies
  arr - sched == 3 with a matching DEPLOY tag, and no ATTR-BAD line
  exists. The verification path carries delayed scalars only.
- K-D2 (delayed consequence attributed; wrong M revised): PASS.
  M0-FIT t=4 C=8 with 8 ATTR lines at sched 0..7;
  M0-DEPLOY-ATTR C=8 bestC=8 conf=1; D-ROUND 1 win=2,0,2 gain=9
  score=17 t=-2; D-ROUND 2 win=1,0,1 gain=1 score=18 t=3; D-ROUND 3
  stop; M1-BUILT n=2 t=3 C=18 prog=2,0,2,1,0,1; REVISE old-C=8
  new-C=18; Mprev holds 1,0,2 with sup=1.
- K-D3 (delayed test consequence attributed; correct M retained):
  PASS. TEST-DEPLOY C=12; retained=1; ATTR line tag=6 with
  sched = arr - 3 (2435 - 2432); M-BYTES-EQUAL 1 (n, gen, sup, pad
  + 24 program bytes identical; threshold excluded per the FORAGE
  ERRATUM-1 rationale).
- K-D4 (necessity): PASS. ARM-NOM C=0 (wiped M: no decisions, no
  deployment, no consequence); menu controls SUM 9, MAX 9, MIN 8,
  FIRST 8, LAST 8, all <= 9 < 18.
- K-D5 (determinism): PASS. 3/3 byte-identical (sha256 above).

No falsifier fired: F-LABEL (audit clean), F-ATTR (awk audit pass,
no ATTR-BAD), F-MISATTR (winner bytes 2,0,2, not the recency winner
2,1,1), F-ONEOP (round-1 best 17 < 18, final n=2), F-NOTUNIQUE
(UNIQ-APPEND-18 n=1), F-MENU-WIN (best menu 9), F-NOREVISE,
F-NORETAIN, F-NONDET, F-PYTHON (safebin PATH, `which python3
python` empty for the whole task; all computation in pure Zag).

## Pre-prereg independent verification

Before the prereg was written, all frozen numbers were derived by
an independent pure-Zag reimplementation (/tmp/dcheck.zag, direct
value formulas, no register machine, separate code path from the
learner). It confirmed: M0 at (t=4, C=8); empty at (t=1, C=8);
round-1 winner SUB R0,R2 at (t=-2, C=17) unique across all 80 (all
60 d!=0 at C=8); round-2 winner ADD R0,R1 at (t=3, C=18) unique
across all 80 (all 60 d!=0 appends at C=17); round-3 stop via the
positive-margin bound 18; M1 test deployment C=12; menus at
9/9/8/8/8; and the recency-misattribution simulation yielding
index 37 = bytes 2,1,1, which the ledger design must and did avoid.

## Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, ledger, delayed
  sweep, and confidence policy are researcher-authored generic
  machinery (PREREG.md section 3). The claim is that M1's FORM is
  source-underdetermined and history-determined, and that its
  VERIFICATION used only delayed downstream coin consequences
  correctly attributed to the deployments that caused them.
- One world family (delayed settlement). No generality claim beyond
  it. Stochastic consequences are not tested; only deterministic
  delayed ones.
- The consequence VALUES are identical to the immediate-oracle
  case; the experiment isolates arrival timing as the single
  variable. The learner reaches the same M1, revision, and
  retention as L3-VERIFY, but through a 3-step-delayed channel with
  up to 3 deployments in flight.
- This build targets the five L3-DELAYED bars. It does not claim
  Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.

## Files

All under `docs/lab/research-lead/overnight-20260928/l3_delayed/`:
NAMECHECK.md (toolchain guard Step 0 + build record), PREREG.md
(frozen), REPORT.md (this file), learner_d.zag, world_d.zag,
driver_d.zag, audit_attr.awk, delayed_full.zag, delayed_bin,
delayed_run1.txt, delayed_run2.txt, delayed_run3.txt.
