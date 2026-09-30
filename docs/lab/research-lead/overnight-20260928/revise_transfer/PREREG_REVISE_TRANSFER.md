# PREREG: F3 REVISE Transfer/Reuse Test (Pipeline Step 9)

Status: FROZEN. This prereg is committed alone before any transfer
world file, build script, binary, or run exists. K1.

Parent chain:
- Design: ca157c743. Builder prereg: c197e7cd8.
- Builder result: 7009d711c (REVISE-PASS).
- Sealed prereg: 8cdf0992a. Sealed result: 1df8addec (REVISE-SEALED-PASS).
- Repro: 7407dd4a7 (REVISE-REPRO-PASS).
- Baseline prereg: 4786633c5, amend db585360a. Baseline: c810d5f55
  (REVISE-BASELINE-PASS).
- Attack prereg: 12da75511. Attack: bbdb65c99 (REVISE-ATTACK-SURVIVES).
- OOD prereg: 7bf467d35. OOD: 1125be9bb (REVISE-OOD-PASS).
- Ablation prereg: 6dcb1f11b. Ablation: 96e22de82 (REVISE-ABLATION-PASS).
This is pipeline step 9 (transfer/reuse) only.

Step 0 name-check (LOOP_STATE.md standing rules): pure Zag only, zero
Python at every stage (authoring, world files, build, runs, analysis,
byte checks); shell-only dash check via
worker_snippets/check_no_dash.sh; no em/en dash bytes in new files;
commits local on tnn-native-lab, owned pathspec
docs/lab/research-lead/overnight-20260928/revise_transfer/ only;
nothing pushed; the contaminated research paper is not touched.

## 1. Claim under test

The D1-grown inhibitor guard `!Z@2` is a persistent, reusable
cognitive structure, not a one-shot patch. Concretely: after the
learner grows `!Z@2` onto Y's rule on a first goal episode (S-NEG2
inhibitor setup), it REUSES the grown guard to solve a second, novel
goal episode on the first attempt, without firing D1 a second time.

This is a deliberately minimal transfer test (bounded L2). It does
not test cross-domain transfer, new variables, or changed causal
truth. The causal truth is identical in both episodes:
Y(t) = X(t-2) AND NOT Z(t-2).

## 2. World designs

Two new world files, both derived from the sealed S-NEG2 world
(w_sneg2_ref.zag, sealed commit 1df8addec). The frozen learner
(f3_revise_frozen.zag, sha256
354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392)
is concatenated BEFORE the world file, unmodified and hash-verified
before every build.

### 2.1 Episode counter (disclosed harness mechanism)

The frozen L_run() calls w_goal_setup(ws) exactly once per goal
attempt, after w_reset(ws). The transfer worlds keep a per-process
episode counter in ws bytes 92..103 (magic 0x54524645 at bytes
92..95, counter at bytes 96..99). The world's w_reset clears bytes
0..91 and preserves bytes 92..103. This is safe because the learner
never advances the world clock past t=11 in any phase (passive 12
steps; trial/plan search depth at most 8), so Y's history bytes
84..103 are never read or written by the learner. w_goal_setup
increments the counter and selects the setup by its new value.
w_passive, w_act, w_snapshot behave exactly as S-NEG2 in all
phases; only w_goal_setup is episode-dependent. The learner source
is untouched; all multiplexing lives in the world (harness) file
and is disclosed here.

### 2.2 S-TRF (treatment), file world_stf.zag

- Learning segment (counter 0): byte-identical behavior to S-NEG2.
  Passive: X pulsed at t=3,9; Z never pulsed; Y=X(t-2) AND NOT Z(t-2).
- w_goal_setup call 1 (setup S1): Z=1 at t=0, X=0, Y=0.
  (Identical to the sealed S-NEG2 goal setup.)
- w_goal_setup call 2 and later (setup S2): Z=1 at t=0, X=1 at t=0,
  Y=0. Novelty vs S1: X is pre-set, so the successful plan has a
  different shape (no SET X needed; the inhibitor must still be
  cleared). The grown guard remains necessary: without it the
  planner simulates [W,W] as successful and fails in reality.
- w_vname, w_nvars=3, w_nctrl=2, w_ctrl=[X,Z], w_ctxvar=-1,
  w_goal_mode=0, w_goal_met (Y=1), w_plan_maxd=8, w_worldname=
  "SQ10-eps-transfer" (the learner never reads it; D5 ban intact).
- main() calls L_run() once and emits "TRANSFER DONE mask=".

### 2.3 S-CTF (control), file world_sct.zag

- Learning segment (counter 0): byte-identical behavior to S-NEG2.
- w_goal_setup call 1 and later: setup S2 directly (Z=1@0, X=1@0,
  Y=0). No prior inhibitor episode; the guard is not pre-grown.
- w_worldname="SQ11-eps-control". Otherwise identical to S-TRF.

## 3. Predicted mechanism traces

### 3.1 Treatment (S-TRF)

Learning segment replicates the sealed S-NEG2 run, so attempt 1 is
predicted byte-identical to the sealed trace through the D1 block:
- F3P3 PLAN [SX,W,W] (attempt 1)
- F3P3 GOAL_REAL 0 (attempt 1)
- F3P3 GOAL_FAIL_GROW_ATTEMPT
- F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@2
- F3P3 REVISED_GROWN replanned
Attempt 2 (setup S2, grown rule [X@2 & !Z@2] in hyp1):
- F3P3 GOAL_REAL 1 (attempt 2)
- NO second F3P3 GOAL_FAIL_GROW_ATTEMPT anywhere in the run.
- NO second F3P3 GROW_OK (goal-fail) anywhere in the run.
- F3P3 FINALRULE V=Y rule=0 [X@2 & !Z@2]
- F3P3 NGROW 1, F3P3 GOAL_OK 1.
Rationale: the grown rule matches the world truth exactly, so the
planner's simulation equals reality; whatever plan it finds first
with simulated Y=1 succeeds in reality. A successful plan exists
within depth 8 (e.g. [CZ,CZ,W]).

### 3.2 Control (S-CTF)

Attempt 1 (setup S2, rule [X@2], no guard):
- F3P3 PLAN [W,W] (attempt 1): with rule [X@2] the planner
  simulates Y(2)=X(0)=1 and selects [W,W] first.
- F3P3 GOAL_REAL 0 (attempt 1): real Y(2)=X(0) AND NOT Z(0)=0.
- F3P3 GOAL_FAIL_GROW_ATTEMPT
- F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@2
  (deterministic D1 search: (Z,0,2) is the first candidate false at
  t_ref=2 and true on all passive true positives)
- F3P3 REVISED_GROWN replanned
Attempt 2: F3P3 GOAL_REAL 1 (attempt 2).
- F3P3 FINALRULE V=Y rule=0 [X@2 & !Z@2]
- F3P3 NGROW 1, F3P3 GOAL_OK 1.

## 4. Verdict rule (frozen)

Let T = treatment run output, C = control run output (each 3x).

Validity gates (VOID, not a mechanism verdict):
- V0: T lines 1..46 (through "F3P3 REVISED_GROWN replanned") are
  byte-identical to sealed S-NEG2 raw output lines 1..46. If not,
  the harness diverged: VOID.
- V1: C attempt 1 shows F3P3 GOAL_REAL 0 (attempt 1). If C attempt 1
  shows GOAL_REAL 1, setup S2 does not require the guard and the
  test cannot measure transfer: VOID.

REVISE-TRANSFER-PASS iff V0 and V1 hold and ALL of:
- T1: T contains, in order: "F3P3 GOAL_REAL 0 (attempt 1)",
  "F3P3 GOAL_FAIL_GROW_ATTEMPT",
  "F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@2",
  "F3P3 REVISED_GROWN replanned".
- T2: T contains "F3P3 GOAL_REAL 1 (attempt 2)".
- T3: T contains exactly one "F3P3 GOAL_FAIL_GROW_ATTEMPT" line and
  exactly one "F3P3 GROW_OK (goal-fail)" line (the guard is reused,
  not re-derived).
- T4: T contains "F3P3 FINALRULE V=Y rule=0 [X@2 & !Z@2]".
- C1: C contains, in order: "F3P3 GOAL_REAL 0 (attempt 1)",
  "F3P3 GOAL_FAIL_GROW_ATTEMPT",
  "F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@2".
- C2: C contains "F3P3 GOAL_REAL 1 (attempt 2)".
- C3: C contains "F3P3 FINALRULE V=Y rule=0 [X@2 & !Z@2]".
- D1: 3/3 byte-identical stdout per configuration; zero stderr
  bytes on all six runs.

REVISE-TRANSFER-FAIL iff V0 and V1 hold and any of T1..T4, C1..C3,
D1 fails. (A second D1 firing on S2 in T is the canonical transfer
failure signature.)

## 5. Kill bars

- K1 (prereg frozen before transfer implementation): PASS iff this
  file's commit strictly precedes every transfer world file, build
  script, binary, and run (verified by commit ancestry).
- K2 (transfer tests run): PASS iff treatment and control each ran
  3x with committed raw logs and the verdict rule was applied to
  measured output.
- K3 (pure Zag, 3/3 identical): PASS iff zero Python invocations at
  every stage, shell-only dash check clean, every reported
  configuration 3/3 byte-identical with zero stderr bytes.

## 6. Honest scope (pre-registered bound)

PASS keeps REVISE at bounded L2; it claims no L3 and no Criterion 0.
The test measures reuse of one grown literal in one novel goal
configuration with unchanged causal truth. It does not test reuse
across changed delays, new variables, disjunctive truths,
multi-inhibitor worlds, or cross-world rule carryover (the frozen
L_run builds its rule set fresh per process; persistence is
within-process). Steps 10-11 (independent red team, governance
audit) remain open either way.
