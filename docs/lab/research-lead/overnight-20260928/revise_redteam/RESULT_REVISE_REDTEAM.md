# RESULT: F3 REVISE Independent Red Team (Pipeline Step 10)

Verdict: REVISE-REDTEAM-KILLS.

Prereg: revise_redteam/PREREG_REVISE_REDTEAM.md (commit fc57bb738,
frozen alone before any red-team world, build, or run; K1 PASS).
Frozen learner: f3_revise_frozen.zag, sha256
354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392
(hash re-verified before every build; the learner source is
unmodified and byte-identical to the attack step's frozen copy).

## 1. What was attacked

The bounded-L2 claim that D1 goal-failure revision is a generic
mechanism which grows the causally correct guard literal on unseen
world structure. The red-team thesis: F3_grow_search accepts the
FIRST literal in deterministic var order that is (a) false at the
refutation time and (b) true on all passive-trace true positives.
Any variable that is 0 throughout the passive trace and 1 in the
goal setup satisfies (a)+(b) exactly like the true inhibitor, so
the criterion cannot distinguish cause from coincident goal-setup
context.

## 2. Measured outcomes (3/3 byte-identical per world, zero stderr)

W-CTRL (harness validity, S-NEG2 replica):
- GOAL_OK 1; FINALRULE V=Y rule=0 [X@2 & !Z@2]; growth: !Z@2.
- V0 holds: the harness replicates the sealed result.

W-CONF1 (one inert confounder C, goal setup C=1,Z=1):
- Attempt 1 plan [SX,W,W] failed; grew !C@2 (SPURIOUS, first-match).
- Attempt 2 plan [SX,CC,W,W] failed; grew !Z@2 (true guard).
- Attempt 3 plan [W,SX,W,W] succeeded.
- GOAL_OK 1; FINALRULE V=Y rule=0 [X@2 & !C@2 & !Z@2].
- Deviation: the grown rule is polluted with the confounder
  literal; the correct outcome required exactly [X@2 & !Z@2].

W-CONF2 (two inert confounders C1,C2, goal setup C1=C2=Z=1):
- Attempt 1 plan [SX,W,W] failed; grew !C1@2 (SPURIOUS).
- Attempt 2 plan [SX,CC1,W,W] failed; grew !C2@2 (SPURIOUS).
- Attempt 3 plan [W,SX,W,W] succeeded.
- GOAL_OK 1; FINALRULE V=Y rule=0 [X@2 & !C1@2 & !C2@2].
- Deviation: the true inhibitor guard !Z@2 was NEVER grown;
  both growths were spent on spurious confounder literals.

W-2INH (two true inhibitors Z,W, goal setup Z=W=1):
- Attempt 1 failed; grew !Z@2. Attempt 2 failed; grew !W@2.
- Attempt 3 plan [W,SX,W,W] succeeded.
- GOAL_OK 1; FINALRULE V=Y rule=0 [X@2 & !Z@2 & !W@2].
- Correct outcome: D1 chains correctly over genuine
  multi-cause failure.

## 3. The timing side-step (red-team mechanism analysis)

On W-CONF1 attempt 3, W-CONF2 attempt 3, and W-2INH attempt 3,
the successful plan was [W,SX,W,W]: pulse X at t=1 and observe
at t=3, where the delay-2 read sees Z(1)=0 and W(1)=0 because
the goal setup's SETs are non-persistent (present only at t=0).
The planner did NOT clear the inhibitors; it routed around them
in time. Contrast the sealed S-NEG2 flagship trace, where
attempt 2 was [SX,CZ,W,W]: a genuine guard-driven clear of Z.

Consequence: on the confounder worlds, GOAL_OK 1 does not show
the grown guard doing the work. On W-CONF1 the true guard !Z@2
was grown but unused by the winning plan; on W-CONF2 the true
guard was never grown at all and the goal still succeeded.
The D1 growths constrained the planner's search away from the
failing [SX,W,W] shape, which accidentally produced the timing
dodge. The grown literals on W-CONF1/W-CONF2 are causally wrong
(they name inert variables), yet the goal was achieved.

## 4. Verdict application

V0 holds (W-CTRL replicates sealed). Per the frozen rule,
REVISE-REDTEAM-KILLS because W-CONF1 and W-CONF2 deviate from
their correct outcomes:
- W-CONF1: spurious literal !C@2 grown first and retained in
  the final rule.
- W-CONF2: both D1 growths spent on confounders; the true
  guard !Z@2 never grown; goal achieved via planner timing,
  not revision.
W-2INH is honest counter-evidence (correct chaining), and it
bounds the kill: D1 handles genuine multi-cause failure but
cannot tell cause from coincident goal-setup context.

## 5. Honest scope (pre-registered)

This KILL keeps REVISE at bounded L2. It does not claim the
mechanism is useless: on confounder-free worlds (S-NEG2,
S-TRF) D1 grew the true guard and the planner used it to
clear the inhibitor (sealed attempt-2 trace). What is falsified
is the generic causal-revision reading: the surviving
characterization is narrower, D1 revision is reliable only when
no inert variable that is 0 in the passive trace and 1 in the
goal setup precedes the true cause in var order. The transfer
prereg's "persistent, reusable cognitive structure" claim for
the grown guard is weakened: on W-CONF1 the persisted
structure contains a spurious literal; on W-CONF2 it misses
the true guard entirely.

## 6. Kill bars

- K1 (prereg frozen before red-team implementation): PASS.
  fc57bb738 strictly precedes all world/build/run commits.
- K2 (attacks run): PASS. Four worlds, 3x each, raw logs
  committed (raw_{ctrl,conf1,conf2,inh2}_r{1,2,3}.txt/.err).
- K3 (pure Zag, 3/3 identical): PASS. Zero Python at every
  stage (authoring, worlds, build script, runs, md5/wc checks
  via shell only). All twelve runs byte-identical per world
  (md5: ctrl 061dddb72ea25d71948b1c48826af900,
  conf1 d9b562db013f01ed6f7587026a6e2584,
  conf2 f14bf28d449db42352f1e6bdf25d6ee9,
  inh2 a85158918bfb90dc809723f3aedc25f6). All twelve stderr files 0 bytes.
  Dash check clean on all new files.

## 7. Governance note (step-9 contamination, restated)

Step-9 transfer (c3c3e3bc8, REVISE-TRANSFER-PASS) disclosed a
prohibited stdout-only python3 -c hex-to-decimal invocation.
Under the literal pure-Zag rule that result cannot stand as
K3-clean evidence. This red-team step is pure-Zag clean and
its verdict does not depend on the transfer result; the
contamination is preserved here so step 11 does not inherit
it silently.

Scope: bounded L2 only. No L3, no Criterion 0 claimed.
Step 11 (governance audit) remains open.
