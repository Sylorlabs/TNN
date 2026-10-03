# REPORT: L3 Invention with Stochastic (Noisy) Consequences (L3-STOCHASTIC)

Verdict: **L3-STOCHASTIC-COMPLETE** (all six frozen kill bars pass,
no falsifier fires).

Date: 2026-10-02. Worker: L3 Stochastic Worker.
Prereg: `PREREG.md` (frozen 68c590d32; committed alone before any
implementation existed; zero amendments). Determinism: 3/3
byte-identical runs (sha256
162e59a60a71c154af12cba7f23d22918b2aee0fe517bfd4f8f5fc9a067997ba).

## What was built

Three Zag files, concatenated to `stochastic_full.zag`, compiled
with the pinned znc
(`src/tools/toolchain/znc_linux_x86_64_abed8aa1`, one benign analyzer
warning, the same discarded-`x_get`-return note L3-VERIFY's learner
carries) to `stochastic_bin`:

- `learner_s.zag`: NEW noisy-consequence learner (no frozen ancestor
  fits: the L3-VERIFY learner trusts single deterministic
  observations). Generic machinery + learned state only: X episode
  recall (sequences only), register-machine executor (ops 0=CPY 1=ADD
  2=SUB 3=MAX 4=MIN), the K-sample averaging loop `l_avg_eval` (the
  ONLY consequence observation path: every score is a sum of K noisy
  oracle outputs), consequence threshold fitting over K-sample sums,
  greedy construction over 80 candidates per round with the frozen
  significance bound (append only if measured gain > K/2),
  M/Mprev slot bookkeeping, and the generic confidence policy
  (l_observe / l_revise / l_deploy_eval). It calls exactly two
  world-side symbols, `w_conseq_train_nz` and `w_conseq_test_nz`:
  one-deployment noisy aggregate coin oracles. No per-episode
  outcome, no margin computation, no seed, no noise draw, no
  supplied right-answer bit anywhere in it.
- `world_s.zag`: new SETTLE-NZ environment (experiment side only).
  Frozen episode tables (same as L3-VERIFY), hidden margin rule
  margin = e0+e1-e2, the seeded counter-based noise (seed 7000,
  draws in {-1,0,1}, pure function of seed + query key + sample
  index), the two noisy oracles, and the five menu controls. The
  deterministic coin oracles exist only as world-side helpers with
  no learner-visible symbol.
- `driver_s.zag`: new experiment-side driver. Teaches X, seeds the
  inherited wrong M0, runs the stage protocol (inherit, construct +
  revise at K=64, single-sample K=1 control arm, deploy held-out),
  evaluates the NOM and MENU arms, and prints the kill-bar summary.
  It never invents the intermediate: all construction goes through
  the learner's noisy consequence-driven construct(). Output via one
  preallocated buffer and a single raw syscall write.

## The noisy consequence-verified creation trace (K-S2, K-S3)

Stage 0: M0 = [ADD R0,R2] (bytes 1,0,2, seeded experiment-side) is
fit by averaged noisy consequence only (t=4, C=513, a 64-sample sum),
deployed K=64 through the noisy oracle (C=513, identical draws: same
query key), and recorded as incumbent (bestC=513, conf=1):

```
M0-SEED prog=1,0,2
M0-FIT t=4 C=513
M0-DEPLOY C=513 bestC=513 conf=1
```

Stage 1: the learner constructs from the empty program. Every
candidate score is a 64-sample sum of noisy coin consequences; no
label is ever consulted. The significance bound is 32:

```
C-ROUND 1 base=510 eval=80 win=2,0,2 gain=578 score=1088 t=-2 mgn=192
C-ROUND 2 base=1088 eval=80 win=1,0,1 gain=63 score=1151 t=3 mgn=61
C-ROUND 3 base=1151 eval=80 stop maxgain=3
M1-BUILT n=2 t=3 C=1151 prog=2,0,2,1,0,1
REVISE old-C=513 new-C=1151
M n=2 gen=1 sup=0 t=3 prog=2,0,2,1,0,1,...
MPREV n=1 gen=0 sup=1 prog=1,0,2,...
```

Round 1: SUB R0,R2 is the winner (gain 578 > 32; winner sum 1088,
runner-up margin 192 > 0). Round 2: ADD R0,R1 is the winner (gain
63 > 32; the binding 1-coin-per-deployment gain, resolved by
averaging; margin 61 > 0). Round 3: best measured gain 3 <= 32,
stop. The final intermediate M1 = [SUB R0,R2, ADD R0,R1]
(R0 = e0+e1-e2 exactly) appears nowhere in the learner source.
Because 1151 > 513, the learner revises: M0 moves to Mprev with
sup=1, M1 becomes incumbent (bestC=1151, conf=2).

Stage 1b (control): the IDENTICAL learner code with K=1 (single
noisy deployment per evaluation, bound 0):

```
C-ROUND 1 base=7 eval=80 win=2,0,2 gain=11 score=18 t=-2 mgn=4
C-ROUND 2 base=18 eval=80 stop maxgain=0
K1-BUILT n=1 prog=2,0,2
K1-SELECT-M1 0
```

The single-sample learner stalls after round 1: the 1-coin
round-2 gain cannot be distinguished from per-deployment noise, so
no append clears even the plain positive-gain rule. It never
selects M1. Averaging is load-bearing, not decorative.

Stage 2: M1 deployed K=64 on the four held-out episodes at t=3:

```
TEST-DEPLOY C=769 retained=1
M-BYTES-EQUAL 1
```

Averaged consequence 769 > 0, so the learner retains M1; its
structural bytes are byte-identical across the deployment.

## Kill bars

- K-S1 (noisy-channel hygiene): PASS. Shell grep audit on the
  committed `learner_s.zag`: all 8 frozen patterns return 0 hits
  (label, expected, w_tab, margin, correct, _mode, bridge, handler;
  case-insensitive); `w_conseq_train(` and `w_conseq_test(` return 0
  hits (deterministic oracles never referenced); the only `w_`
  symbols present are `w_conseq_train_nz` (2 refs) and
  `w_conseq_test_nz` (2 refs), both inside the K-sample averaging
  loop `l_avg_eval`. Every construction score in the log is a
  64-sample sum.
- K-S2 (averaging is load-bearing): PASS. K1-BUILT n=1 prog=2,0,2
  with K1-SELECT-M1 0 (single-sample construction does not select
  M1), while the K=64 arm selects M1 per K-S3. Driver requires both.
- K-S3 (correct M constructed via noisy channel despite noise):
  PASS. M0-DEPLOY C=513; two positive-gain rounds (578 and 63, both
  > 32) with the frozen winner bytes; round 3 stops (maxgain 3);
  M1-BUILT n=2 t=3 C=1151 prog=2,0,2,1,0,1; REVISE old-C=513
  new-C=1151; Mprev holds 1,0,2 with sup=1.
- K-S4 (retained under noise): PASS. TEST-DEPLOY C=769; retained=1;
  M-BYTES-EQUAL 1 (n, gen, sup, pad + 24 program bytes identical;
  threshold excluded per the FORAGE ERRATUM-1 rationale).
- K-S5 (necessity): PASS. ARM-NOM C=0 (wiped M: no decisions, no
  consequence); menu control 64-sample sums 574, 576, 514, 514, 510,
  all < 1151.
- K-S6 (determinism): PASS. 3/3 byte-identical (sha256 above).

No falsifier fired: F-LABEL (audit clean), F-NOAVG (K=1 ends n=1,
never selects M1), F-WRONGM (all frozen bytes/sums/gains/t
reproduced exactly), F-NOMARGIN (margins 192 and 61 > 0; round 3
maxgain 3 <= 32), F-NOREVISE, F-NORETAIN, F-MENU-WIN (best menu
576), F-NONDET, F-PYTHON (safebin PATH, `which python3 python`
empty for the whole task; all computation in pure Zag).

## Pre-prereg independent verification

Before the prereg was written, the frozen numbers were derived by an
independent pure-Zag check (/tmp/scheck.zag, separate code path from
the learner: direct value formulas instead of the register machine,
fresh threshold/sum/selection logic). It searched seeds from 7000
upward with the disclosed rule (first seed where K=64 yields exactly
M1 with the L3-VERIFY winner bytes AND the K=1 arm fails to select
M1); seed 7000 was the first tried and satisfied both, so no
further search was needed. A second, independent register-machine
evaluation of the K=64 winner fits agreed exactly (XCHECK-BAD=0),
so the direct formulas are validated. The check confirmed: round-1
winner SUB R0,R2 (gain 578, sum 1088, t=-2, margin 192); round-2
winner ADD R0,R1 (gain 63, sum 1151, t=3, margin 61); round-3 stop
(maxgain 3); M0 at t=4 sum 513; K=1 arm stalls at n=1 prog=2,0,2;
test deployment sum 769; menu sums 574/576/514/514/510.

## Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, K-sample averaging
  loop, the gain significance bound K/2, the confidence policy, and
  the seeded counter-based noise model are researcher-authored
  generic machinery (PREREG.md sections 2-3). The claim is that M1's
  FORM is source-underdetermined and history-determined, that its
  construction and verification used only noisy downstream coin
  consequences, and that averaging over repeated deployments is what
  makes the selection succeed where single samples fail.
- One world family (settlement). No generality claim beyond it.
- The noise is small (at most 1 coin per deployment); the binding
  test is the round-2 gain of 1 coin per deployment, which the K=1
  arm demonstrably cannot resolve.
- This build targets the six L3-STOCHASTIC bars. It does not claim
  Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.

## Files

All under `docs/lab/research-lead/overnight-20260928/l3_stochastic/`:
NAMECHECK.md (toolchain guard Step 0 + build record), PREREG.md
(frozen), REPORT.md (this file), learner_s.zag, world_s.zag,
driver_s.zag, stochastic_full.zag, stochastic_bin,
stochastic_run1.txt, stochastic_run2.txt, stochastic_run3.txt.
