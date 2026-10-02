# REPORT: L3 Verification with Learner-Owned Consequence Signal (L3-VERIFY)

Verdict: **L3-VERIFY-COMPLETE** (all five frozen kill bars pass, no
falsifier fires).

Date: 2026-10-02. Worker: L3 Verification Worker.
Prereg: `PREREG.md` (frozen 6467fc547; committed alone before any
implementation existed; zero amendments). Determinism: 3/3
byte-identical runs (sha256
5da749f753871627e72ef941bb8f7ce031841c05a2caf7a21facfe8e4f280368).

## What was built

Three Zag files, concatenated to `verify_full.zag`, compiled with the
pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`) to
`verify_bin`:

- `learner.zag`: NEW consequence-driven learner (no frozen ancestor;
  the FORAGE/RELAY/LEDGER learner is label-based and read-only, so it
  could not be reused). Generic machinery + learned state only: X
  episode recall (sequences only), register-machine executor
  (ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN), greedy construction over 80
  candidates per round (strictly positive gain, 8-instruction cap),
  consequence threshold fitting, M/Mprev slot bookkeeping, and the
  generic confidence policy (l_observe / l_revise / l_deploy_eval).
  It calls exactly two world-side symbols, `w_conseq_train` and
  `w_conseq_test`: aggregate coin oracles. No per-episode outcome, no
  margin computation, no supplied right-answer bit anywhere in it.
- `world.zag`: new SETTLE environment (experiment side only). Frozen
  episode tables, hidden margin rule margin = e0+e1-e2, the two coin
  oracles, and the five menu controls. The oracles return ONLY
  aggregate coin totals per deployment.
- `driver.zag`: new experiment-side driver. Teaches X, seeds the
  inherited wrong M0, runs the stage protocol (inherit, construct +
  revise, deploy held-out), evaluates the NOM and MENU arms, and
  prints the kill-bar summary. It never invents the intermediate: all
  construction goes through the learner's consequence-driven
  construct(). Output via one preallocated buffer and a single raw
  syscall write.

## The consequence-verified creation trace (K-V1, K-V2)

Stage 0: M0 = [ADD R0,R2] (bytes 1,0,2, FORAGE's solution, seeded
experiment-side as a plausible but wrong inheritance) is fit by
consequence only (t=4, C=8), deployed through the world oracle, and
recorded as incumbent (bestC=8, conf=1):

```
M0-SEED prog=1,0,2
M0-FIT t=4 C=8
M0-DEPLOY C=8 bestC=8 conf=1
```

Stage 1: the learner constructs from the empty program. Every
candidate score is an aggregate coin consequence from the oracle; no
label is ever consulted:

```
C-ROUND 1 base=8 eval=80 win=2,0,2 gain=9 score=17 t=-2
C-ROUND 2 base=17 eval=80 win=1,0,1 gain=1 score=18 t=3
C-ROUND 3 base=18 stop
M1-BUILT n=2 t=3 C=18 prog=2,0,2,1,0,1
REVISE old-C=8 new-C=18
M n=2 gen=1 sup=0 t=3 prog=2,0,2,1,0,1,...
MPREV n=1 gen=0 sup=1 prog=1,0,2,...
UNIQ-APPEND-18 n=1
```

Round 1: SUB R0,R2 is the UNIQUE 17/18 candidate (gain 9; next best
MAX R0,R2 at 15). Round 2: ADD R0,R1 is the UNIQUE 18/18 append
(gain 1; every other append at most 17). Round 3 stops. The final
intermediate M1 = [SUB R0,R2, ADD R0,R1] (R0 = e0+e1-e2 exactly)
appears nowhere in the learner source. Because 18 > 8, the learner
revises: M0 moves to Mprev with sup=1, M1 becomes incumbent
(bestC=18, conf=2).

Stage 2: M1 deployed on the four held-out episodes at t=3:

```
TEST-DEPLOY C=12 retained=1
M-BYTES-EQUAL 1
```

Consequence 12 (settle the two positive-margin episodes, hold the
two negative ones) is positive, so the learner retains M1; its
structural bytes are byte-identical across the deployment.

## Kill bars

- K-V1 (consequence-only verification): PASS. Shell grep audit on the
  committed `learner.zag`: all 8 frozen patterns return 0 hits
  (label, expected, w_tab, margin, correct, _mode, bridge, handler;
  case-insensitive). The only world-side symbols referenced are
  `w_conseq_train` (3 refs) and `w_conseq_test` (2 refs): the
  aggregate coin oracles. The verification path carries scalars only.
- K-V2 (wrong M revised): PASS. M0-DEPLOY C=8; two positive-gain
  rounds with the frozen winner bytes; M1-BUILT n=2 t=3 C=18
  prog=2,0,2,1,0,1; REVISE old-C=8 new-C=18; Mprev holds 1,0,2 with
  sup=1.
- K-V3 (correct M retained): PASS. TEST-DEPLOY C=12; retained=1;
  M-BYTES-EQUAL 1 (n, gen, sup, pad + 24 program bytes identical;
  threshold excluded per the FORAGE ERRATUM-1 rationale).
- K-V4 (necessity): PASS. ARM-NOM C=0 (wiped M: no decisions, no
  consequence); menu controls SUM 9, MAX 9, MIN 8, FIRST 8, LAST 8,
  all <= 9 < 18.
- K-V5 (determinism): PASS. 3/3 byte-identical (sha256 above).

No falsifier fired: F-LABEL (audit clean), F-ONEOP (round-1 best 17
< 18, final n=2, winner bytes 2,0,2), F-NOTUNIQUE
(UNIQ-APPEND-18 n=1), F-MENU-WIN (best menu 9), F-NOREVISE, F-NORETAIN,
F-NONDET, F-PYTHON (safebin PATH, `which python3 python` empty for
the whole task; all computation in pure Zag).

## Pre-prereg independent verification

Before the prereg was written, the frozen numbers were derived by an
independent pure-Zag reimplementation (/tmp/vcheck.zag, separate code
path from the learner: direct value formulas instead of the register
machine, standalone threshold sweeps). It confirmed: round-1 winner
SUB R0,R2 at C=17 t=-2 unique; round-2 winner ADD R0,R1 at C=18 t=3
unique; round-3 stop; M0 at C=8; menus at 9/9/8/8/8; test deployment
C=12. During that check it caught two design flaws before they could
freeze: (1) an early table let MAX R0,R1 reach 18 in round 1
(1-op sufficiency); (2) a later table let SUB R0,R2 append reach 18
in round 2 (non-unique winner). Both were fixed by table edits
(E5=[7,4,15,0], E8=[3,0,4,3]) and re-verified. It also caught a bug in
the check itself (s=0 appends must read R0's current value, not e0).

## Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, oracle-query loop,
  and confidence policy are researcher-authored generic machinery
  (PREREG.md section 3). The claim is that M1's FORM is
  source-underdetermined and history-determined, and that its
  verification used only downstream coin consequences.
- One world family (settlement). No generality claim beyond it.
- The consequence here is deterministic and immediate; delayed or
  stochastic consequences are not tested.
- This build targets the five L3-VERIFY bars. It does not claim
  Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.

## Files

All under `docs/lab/research-lead/overnight-20260928/l3_verify/`:
NAMECHECK.md (toolchain guard Step 0 + build record), PREREG.md
(frozen), REPORT.md (this file), learner.zag, world.zag, driver.zag,
verify_full.zag, verify_bin, verify_run1.txt, verify_run2.txt,
verify_run3.txt.
