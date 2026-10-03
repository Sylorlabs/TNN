# PREREG: L3 Verification with Learner-Owned Consequence Signal (L3-VERIFY)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l3_verify/` only.
Worker: L3 Verification Worker (subagent, 2026-10-02).
Parent mandate: test L3 invention with LEARNER-OWNED verification
(Micah priority #5): the learner constructs M, DEPLOYS it, and world
consequences (not harness-supplied correct answers) verify it.

## 1. What is being tested

Whether the learner can invent the intermediate M AND verify it using
only downstream world consequences. Boundary from FORAGE / RELAY /
LEDGER: there, construction and verification scored candidates against
train labels (harness-provided correct CLEAR/HOLD answers). Here, no
label exists anywhere in the learner's path. The world is a settlement
task: deploying a decision CLEAR on an episode settles it for its true
margin in coins (positive margin earns, negative margin loses);
HOLD settles nothing. The learner's only verification signal is the
aggregate coin consequence of a deployment. The learner must:

(a) deploy an inherited wrong intermediate M0, observe its poor
    consequence, and record it as incumbent;
(b) construct a fresh M1 guided ONLY by consequence queries,
    compare consequences, and revise (replace M0) because C(M1) > C(M0);
(c) deploy M1 on held-out episodes, observe a positive consequence,
    and retain it byte-identical.

The consequence is a scalar P&L per deployment, never a per-episode
correct/incorrect bit. The learner never observes a label.

## 2. Frozen world (SETTLE; environment, hidden from learner)

Hidden margin rule: margin(ep) = e0 + e1 - e2 (world-hidden; the
learner source never computes it and never receives it per episode).

Consequence of deploying program P with threshold t on a region:
for each episode: v = P(ep) (register machine, R0 output);
decision = CLEAR iff v >= t else HOLD;
coins += (decision == CLEAR) ? margin(ep) : 0.
Total coins is the ONLY value crossing into the learner.

Frozen train episodes (id: [e0,e1,e2,e3], margin):
1: [2,7,3,0] m=6    2: [8,1,4,1] m=5
3: [1,6,3,5] m=4    4: [6,0,3,3] m=3
5: [7,4,15,0] m=-4  6: [4,3,10,1] m=-3
7: [3,2,7,2] m=-2   8: [3,0,4,3] m=-1

Frozen held-out test episodes:
9: [4,5,2,0] m=7    10: [1,1,5,0] m=-3
11: [6,2,3,1] m=5   12: [2,3,8,2] m=-3

Frozen oracle rule: for a candidate program, candidate thresholds are
the sorted unique program outputs on the evaluated episode set,
ascending; first-max wins; C(t) = sum of margins of episodes with
v >= t. Deterministic; no RNG.

## 3. Frozen learner machinery (new, disclosed, researcher-authored)

`learner.zag` is NEW code written for this experiment (nothing frozen
to copy; the FORAGE learner is read-only and label-based, so it cannot
be reused). Disclosed generic machinery: X episode recall (sequences
only), register-machine executor (ops 0=CPY 1=ADD 2=SUB 3=MAX 4=MIN,
R0..R3 preloaded, output R0), greedy construction over 80 candidates
per round (op-major order 0..4, d 0..3, s 0..3; strictly positive gain;
8-instruction cap), consequence threshold fitting (section 2 rule),
M slot bookkeeping [n,u8 gen,u8 sup,u8 pad, threshold i32, 24 program
bytes] plus Mprev, and the confidence policy below. The learner calls
exactly two world-side symbols: `w_conseq_train(prog,n,t)` and
`w_conseq_test(prog,n,t)` (aggregate coin oracles, defined in
world.zag). No other world reference exists in learner.zag.

Frozen confidence policy (generic, no modes):
- l_observe(C): if C > bestC { bestC = C; conf++; } (conf unchanged
  otherwise).
- l_revise after construction: if C_new > bestC { Mprev = incumbent
  with sup=1; M = new with gen = old gen + 1; bestC = C_new; conf++;
  log REVISE }.
- l_deploy_eval(C): retained = (C > 0) ? 1 : 0; M never modified here.

The inherited wrong intermediate M0 = [ADD R0,R2] (bytes 1,0,2) is
seeded experiment-side (it is FORAGE's solution, plausible but wrong
here); the learner does not invent it. Its consequence is measured,
not stipulated.

## 4. Frozen hand-derived numbers (independent check BEFORE this commit)

Verified by an independent pure-Zag reimplementation
(/tmp/vcheck.zag, separate code path from the future learner) before
this prereg was written. The implementation must reproduce every
number below; any deviation is a falsifier, not a tuning opportunity.

Round 1 (from empty; baseline C=8 t=1), all 20 d=0 candidates:
CPY R0,R0 8 t=1; CPY R0,R1 10 t=6; CPY R0,R2 8 t=3; CPY R0,R3 8 t=0;
ADD R0,R0 8 t=2; ADD R0,R1 11 t=6; ADD R0,R2 8 t=4; ADD R0,R3 8 t=2;
SUB R0,R0 8 t=0; SUB R0,R1 8 t=-5; SUB R0,R2 17 t=-2; SUB R0,R3 8 t=-4;
MAX R0,R0 8 t=1; MAX R0,R1 14 t=6; MAX R0,R2 15 t=6; MAX R0,R3 8 t=2;
MIN R0,R0 8 t=1; MIN R0,R1 8 t=0; MIN R0,R2 8 t=1; MIN R0,R3 8 t=0.
Winner: SUB R0,R2 (bytes 2,0,2), C=17, t=-2, gain 9. UNIQUE (next
best 15). No 1-op reaches 18.

Round 2 (from [SUB R0,R2]; baseline C=17 t=-2), all 20 d=0 appends:
CPY R0,R0 17; CPY R0,R1 10 t=6; CPY R0,R2 8 t=3; CPY R0,R3 8 t=0;
ADD R0,R0 17 t=-4; ADD R0,R1 18 t=3; ADD R0,R2 8 t=1; ADD R0,R3 17 t=-1;
SUB R0,R0 8 t=0; SUB R0,R1 12; SUB R0,R2 17 t=-5; SUB R0,R3 14 t=-1;
MAX R0,R0 17 t=-2; MAX R0,R1 12; MAX R0,R2 8 t=3; MAX R0,R3 11 t=3;
MIN R0,R0 17 t=-2; MIN R0,R1 17 t=-2; MIN R0,R2 17 t=-2; MIN R0,R3 17 t=-2.
Winner: ADD R0,R1 (bytes 1,0,1), C=18, t=3, gain 1. UNIQUE (all
others at most 17, gain 0).

Round 3: best append C=18, gain 0, stop.

M1 = [SUB R0,R2, ADD R0,R1] (bytes 2,0,2,1,0,1),
threshold t=3, train C=18.

M0 = [ADD R0,R2] (bytes 1,0,2): train C=8, t=4 (poor; revision target).

Menu controls (experiment-side; profit-fit thresholds on train):
SUM 9 t=12; MAX 9 t=6; MIN 8 t=0; FIRST 8 t=1; LAST 8 t=0.
Each strictly below 18.

Test deployment of M1 at t=3: decisions clear,hold,clear,hold;
C = 7 + 0 + 5 + 0 = 12.

ARM-NOM (M slot wiped): C=0, all NO_DECISION.

## 5. Frozen stage protocol

- STAGE 0 (inherit): teach X train 1..8. Seed M0 (1,0,2). Learner
  fits M0's threshold by consequence (t=4, C=8), deploys via oracle,
  l_observe(8): bestC=8, conf=1. Log M0-DEPLOY C=8.
- STAGE 1 (construct + revise): learner constructs from empty through
  the consequence oracle only. Log C-ROUND lines, M1-BUILT
  n=2 t=3 C=18 prog=2,0,2,1,0,1. Since 18 > 8: REVISE old-C=8
  new-C=18; Mprev = [1,0,2] sup=1; M = M1 gen=1; bestC=18; conf=2.
  Driver runs experiment-side uniqueness sweep: exactly 1 of the 20
  d=0 appends reaches C=18.
- STAGE 2 (deploy held-out): teach X test 9..12. Snapshot M bytes.
  Deploy M1 at t=3 via w_conseq_test: C=12. l_deploy_eval(12):
  retained=1. M-BYTES-EQUAL 1.
- ARMS: ARM-NOM (wiped M, C=0); ARM-MENU (5 controls, each C <= 9).

## 6. Kill bars

- K-V1 (consequence-only verification): shell grep audit on the
  committed `learner.zag` returns zero case-insensitive hits for each
  pattern in section 7, AND the only world-side symbols referenced in
  learner.zag are `w_conseq_train` and `w_conseq_test` (the aggregate
  coin oracles). No per-episode outcome, margin, or correct-answer
  token crosses the boundary.
- K-V2 (wrong M revised): log shows M0-DEPLOY C=8; construction trace
  with exactly two positive-gain rounds and the frozen winner bytes;
  M1-BUILT n=2 t=3 C=18 prog=2,0,2,1,0,1; REVISE old-C=8 new-C=18;
  Mprev holds prog 1,0,2 with sup=1.
- K-V3 (correct M retained): TEST-DEPLOY C=12; retained=1;
  M structural bytes (n, gen, sup, pad + 24 program bytes; threshold
  excluded per the FORAGE ERRATUM-1 rationale) byte-identical before
  and after the test deployment.
- K-V4 (necessity): ARM-NOM C=0 AND every menu control C <= 9 < 18.
- K-V5 (determinism): three runs of the binary are byte-identical
  (sha256 equal).

Verdict L3-VERIFY-COMPLETE requires all five PASS with no falsifier
firing.

## 7. Frozen K-V1 grep audit spec (run on the committed learner.zag)

Each pattern must return zero matches (grep -c -i == 0):
1. `label` (no label token anywhere in the learner)
2. `expected` (zero in the learner verification path)
3. `w_tab` (no episode table access)
4. `margin` (no world-hidden margin computation)
5. `correct` (no correctness bit; only coin scalars)
6. `_mode` (zero modes allowed)
7. `bridge` (never used in code at all)
8. `handler` (never used in code at all)

## 8. Frozen falsifiers

- F-LABEL: any section-7 pattern matches in learner.zag, or learner.zag
  references a world-side symbol other than the two oracles. Voids the
  whole build.
- F-ONEOP: round-1 best C >= 18, or final program has n != 2, or the
  round-1 winner bytes are not 2,0,2. Voids the whole build.
- F-NOTUNIQUE: the experiment-side append sweep finds != 1 candidates
  at C=18 in round 2. Voids the whole build.
- F-MENU-WIN: any menu control C >= 18. Voids K-V4.
- F-NOREVISE: no REVISE event, Mprev wrong, or M1 bytes !=
  2,0,2,1,0,1. Voids K-V2.
- F-NORETAIN: retained != 1, TEST-DEPLOY C != 12, or M bytes differ
  across the test deployment. Voids K-V3.
- F-NONDET: the three runs differ by even one byte. Voids the build.
- F-PYTHON: any python/python3 invocation in the worker process tree.
  Voids the whole build.

## 9. Determinism spec

No RNG. Fixed candidate order (op-major), fixed threshold sweep
(sorted unique outputs ascending, first-max), single preallocated
output buffer, one raw-syscall write. 3/3 byte-identical required.

## 10. Disclosed residual footprint and non-claims

- The op basis, register machine, greedy search, oracle-query loop,
  and confidence policy are researcher-authored generic machinery,
  disclosed in section 3. The claim is that the intermediate's FORM
  (2,0,2,1,0,1) is source-underdetermined and history-determined, and
  that its VERIFICATION used only downstream coin consequences.
- One world family (settlement). No generality claim beyond it.
- The driver and world files are new experiment-side code; only the
  consequence-query boundary constrains the learner.
- This build targets the five L3-VERIFY bars above. It does not claim
  Micah's full 12-criterion L3 bar.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag.
  No em/en dashes in loop documentation. Paper untouched. Nothing
  pushed. Commits local on tnn-native-lab.
