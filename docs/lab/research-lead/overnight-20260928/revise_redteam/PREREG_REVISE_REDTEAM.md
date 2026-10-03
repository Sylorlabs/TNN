# PREREG: F3 REVISE Independent Red Team (Pipeline Step 10)

Status: FROZEN. This prereg is committed alone before any red-team
world file, build script, binary, or run exists. K1.

Parent chain:
- Design: ca157c743. Builder prereg: c197e7cd8.
- Builder result: 7009d711c (REVISE-PASS, bounded L2).
- Sealed prereg: 8cdf0992a. Sealed result: 1df8addec (REVISE-SEALED-PASS).
- Repro: 7407dd4a7 (REVISE-REPRO-PASS).
- Baseline prereg: 4786633c5, amend db585360a. Baseline: c810d5f55
  (REVISE-BASELINE-PASS).
- Attack prereg: 12da75511. Attack: bbdb65c99 (REVISE-ATTACK-SURVIVES).
- OOD prereg: 7bf467d35. OOD: 1125be9bb (REVISE-OOD-PASS).
- Ablation prereg: 6dcb1f11b. Ablation: 96e22de82 (REVISE-ABLATION-PASS).
- Transfer prereg: 7e80e52e6. Transfer: c3c3e3bc8 (REVISE-TRANSFER-PASS).
This is pipeline step 10 (independent red team) only.

Step 0 name-check (LOOP_STATE.md standing rules): pure Zag only, zero
Python at every stage (authoring, world files, build, runs, analysis,
byte checks); shell-only dash check via
worker_snippets/check_no_dash.sh; no em/en dash bytes in new files;
commits local on tnn-native-lab, owned pathspec
docs/lab/research-lead/overnight-20260928/revise_redteam/ only;
nothing pushed; the contaminated research paper is not touched.

## 1. Red-team thesis (assumed false: the claim under attack)

The bounded-L2 claim: D1 goal-failure revision is a generic
mechanism that grows the causally correct guard literal on unseen
world structure (evidence: sealed S-NEG2 grew !Z@2, the true
inhibitor guard; ablation double dissociation; transfer reuse).

The red team attacks the causal reading. By source audit of the
frozen learner (f3_revise_frozen.zag, sha256
354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392),
F3_grow_search accepts the FIRST literal (deterministic order:
var index ascending, polarity negative first, delay ascending) that
satisfies (a) false at the refutation time and (b) true on all
passive-trace true positives. Criterion (a)+(b) CANNOT distinguish
the true cause of goal failure from a coincident goal-setup
context variable: any variable that is 0 throughout the passive
trace and 1 in the goal setup satisfies (a)+(b) exactly like the
true inhibitor. The trial-phase growth is protected (trials run on
w_reset state, so goal context is absent), but D1 growth reads the
post-failure goal ws, where the goal setup's context is present.

Prediction: on worlds in the same structural family as sealed
S-NEG2 (truth Y = X(t-2) AND NOT Z(t-2), same delays, goal mode 0)
but with inert confounder variables set to 1 in the goal setup,
D1 grows spurious literals (first-match in var order) instead of
the true inhibitor guard. The sealed/baseline/attack/OOD/ablation/
transfer evidence never tested confounders.

## 2. World designs (all derived from sealed world_sneg2.zag)

The frozen learner (f3_revise_frozen.zag, hash verified before
every build) is concatenated BEFORE each world file, unmodified.
All worlds: w_goal_mode()=0, w_plan_maxd=8, w_ctxvar=-1,
w_vname resolves X/Z/Y by exact name (learner D5 name ban intact;
w_worldname strings are new and never read by the learner).

### 2.1 W-CTRL (world_rt_ctrl.zag) - harness validity control

Byte-identical truth and schedules to sealed S-NEG2
(revise_sealed/world_sneg2.zag, commit 1df8addec); only the
w_worldname string differs. Vars: X(0), Z(1), Y(2); nctrl=2,
w_ctrl=[X,Z]. Truth: Y(t) = X(t-2) AND NOT Z(t-2). Passive: env
SETs X at t=3,9; Z never pulsed; Y=1 at t=5,11. Goal setup:
Z=1 at t=0. Expected: replicates sealed (GOAL_OK 1, FINALRULE
V=Y rule=0 [X@2 & !Z@2]).

### 2.2 W-CONF1 (world_rt_conf1.zag) - one confounder

Vars: X(0), C(1), Z(2), Y(3); nctrl=3, w_ctrl=[X,C,Z]. Truth:
Y(t) = X(t-2) AND NOT Z(t-2) (C is causally inert). Passive:
X at t=3,9; C and Z never pulsed; Y=1 at t=5,11. Goal setup:
C=1 AND Z=1 at t=0. The confounder C satisfies (a)+(b) exactly
like Z and precedes Z in var order.

### 2.3 W-CONF2 (world_rt_conf2.zag) - two confounders

Vars: X(0), C1(1), C2(2), Z(3), Y(4); nctrl=4,
w_ctrl=[X,C1,C2,Z]. Truth: Y(t) = X(t-2) AND NOT Z(t-2) (C1, C2
inert). Passive: X at t=3,9; C1, C2, Z never pulsed. Goal
setup: C1=1, C2=1, Z=1 at t=0. Two spurious first-matches
precede the true inhibitor; ATTEMPT_MAX=3 admits at most two
D1 growths after the initial failure.

### 2.4 W-2INH (world_rt_2inh.zag) - two true inhibitors

Vars: X(0), Z(1), W(2), Y(3); nctrl=3, w_ctrl=[X,Z,W]. Truth:
Y(t) = X(t-2) AND NOT Z(t-2) AND NOT W(t-2). Passive: X at
t=3,9; Z, W never pulsed; Y=1 at t=5,11. Goal setup: Z=1 AND
W=1 at t=0. Tests whether D1 chains correctly over genuine
multi-cause failure (disclosed-untested axis; honest in either
direction).

## 3. Predicted mechanism traces (non-governing)

- W-CTRL: GOAL_OK 1; FINALRULE V=Y rule=0 [X@2 & !Z@2].
- W-CONF1: attempt 1 grows !C@2 (first-match, spurious);
  attempt 2 fails (Z still 1); attempt 3 grows !Z@2 and
  succeeds. GOAL_OK 1 but FINALRULE V=Y rule=0
  [X@2 & !C@2 & !Z@2]: goal succeeds with a polluted rule.
- W-CONF2: attempt 1 grows !C1@2; attempt 2 grows !C2@2;
  attempt 3 fails (Z still 1, attempts exhausted). GOAL_OK 0;
  the true guard !Z@2 is never grown.
- W-2INH: attempt 1 grows !Z@2; attempt 2 grows !W@2;
  attempt 3 succeeds. GOAL_OK 1; FINALRULE V=Y rule=0
  [X@2 & !Z@2 & !W@2].

## 4. Verdict rule (frozen)

Validity gate (VOID, not a mechanism verdict):
- V0: W-CTRL shows GOAL_OK 1 and FINALRULE V=Y rule=0
  [X@2 & !Z@2]. If not, the harness diverged from sealed:
  VOID.

Definitions (measured per world, 3x runs):
- G(world): 1 iff every run's "F3P3 NEXPS" line contains
  " GOAL_OK 1 ".
- R(world, expected): 1 iff every run contains exactly the
  line "F3P3 FINALRULE V=Y rule=0 [expected]" and no other
  "F3P3 FINALRULE V=Y" line.

Correct outcomes (the claim's prediction under the causal
reading):
- W-CONF1 correct iff G=1 and R(W-CONF1, "X@2 & !Z@2").
- W-CONF2 correct iff G=1 and R(W-CONF2, "X@2 & !Z@2").
- W-2INH correct iff G=1 and R(W-2INH, "X@2 & !Z@2 & !W@2").

REVISE-REDTEAM-KILLS iff V0 holds and any attack world
(W-CONF1, W-CONF2, W-2INH) deviates from its correct outcome:
the grown structure is not the causally correct guard set,
so the "generic causal revision" reading is falsified and the
surviving claim is bounded to confounder-free goal contexts
with the true cause first in var order.

REVISE-REDTEAM-SURVIVES iff V0 holds and all three attack
worlds achieve their correct outcomes.

D1 (determinism): 3/3 byte-identical stdout per world; zero
stderr bytes on all twelve runs.

## 5. Kill bars

- K1 (prereg frozen before red-team implementation): PASS iff
  this file's commit strictly precedes every red-team world
  file, build script, binary, and run (verified by commit
  ancestry).
- K2 (attacks run): PASS iff all four worlds each ran 3x with
  committed raw logs and the verdict rule was applied to
  measured output.
- K3 (pure Zag, 3/3 identical): PASS iff zero Python
  invocations at every stage, shell-only dash check clean,
  every reported configuration 3/3 byte-identical with zero
  stderr bytes.

## 6. Honest scope (pre-registered bound)

A KILL keeps REVISE at bounded L2; it does not claim the
mechanism is useless, only that the causal-revision reading
is falsified and the surviving characterization is narrower
(confounder-free goal contexts). A SURVIVES keeps the
bounded-L2 claim intact through step 10. Steps 11 (governance
audit) remains open either way. No L3 and no Criterion 0 is
claimed in either outcome.
