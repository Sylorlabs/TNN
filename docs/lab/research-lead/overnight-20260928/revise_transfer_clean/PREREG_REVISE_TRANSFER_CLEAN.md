# PREREG: F3 REVISE Transfer/Reuse Clean Re-run (Pipeline Step 9 Remediation)

Status: FROZEN. This prereg is committed alone before any clean
re-run world file, build script, binary, or run exists. K1.

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
- Transfer prereg: 7e80e52e6. Transfer: c3c3e3bc8
  (REVISE-TRANSFER-PASS on measured output, K4-contaminated: the
  committed result discloses one stdout-only `python3 -c` hex-to-decimal
  calculator use during authoring, 0x54524645 to 1414678085).
- Red-team prereg: fc57bb738. Red team: 4a2b8ef43
  (REVISE-REDTEAM-KILLS the generic causal-revision reading; the
  bounded-L2 reuse characterization survives, narrowed).
- Audit prereg: 62f6a9c31. Audit: 85fe2043c (REVISE-AUDIT-FAIL:
  A3 fails at step 9; steps 1-8 and 10 remain governance-clean).

This is a pure purity remediation of pipeline step 9. The claim,
world designs, predicted traces, verdict rule, and honest scope are
adopted verbatim from the frozen step-9 prereg 7e80e52e6. No design
change is made. The only change is authorship provenance: zero
Python at every stage.

Step 0 name-check (LOOP_STATE.md standing rules): pure Zag only, zero
Python at every stage (authoring, world files, build, runs, analysis,
byte checks); shell-only dash check via
worker_snippets/check_no_dash.sh (2026-09-30 standing rule; no
python3 byte checks; disclosure does not cure use); no em/en dash
bytes in new files; commits local on tnn-native-lab, owned pathspec
docs/lab/research-lead/overnight-20260928/revise_transfer_clean/
only; nothing pushed; the contaminated research paper is not touched.

## 1. Claim under test (adopted from 7e80e52e6)

The D1-grown inhibitor guard `!Z@2` is a persistent, reusable
cognitive structure, not a one-shot patch. Concretely: after the
learner grows `!Z@2` onto Y's rule on a first goal episode (S-NEG2
inhibitor setup), it REUSES the grown guard to solve a second, novel
goal episode on the first attempt, without firing D1 a second time.

This is a deliberately minimal transfer test (bounded L2). It does
not test cross-domain transfer, new variables, or changed causal
truth. The causal truth is identical in both episodes:
Y(t) = X(t-2) AND NOT Z(t-2).

## 2. World designs (adopted from 7e80e52e6, copied byte-verbatim)

Two world files, byte-identical to the committed step-9 artifacts
(commit c3c3e3bc8), extracted via `git show` with no modification:

- world_stf.zag: S-TRF (treatment). Learning segment byte-identical
  to S-NEG2; w_goal_setup call 1 = S1 (Z=1@0); calls 2+ = S2 (Z=1@0,
  X=1@0). w_worldname="SQ10-eps-transfer".
- world_sct.zag: S-CTF (control). Learning segment byte-identical
  to S-NEG2; w_goal_setup always = S2. w_worldname="SQ11-eps-control".

Episode counter in ws bytes 92..103 (magic literal 1414678085 at
92..95, counter at 96..99) travels as a frozen literal inside the
copied bytes. It is not recomputed by any tool or by hand in this
re-run; its provenance is the committed step-9 artifact, and its
correctness was already established by the step-9 V0 byte-identity
gate.

The frozen learner (f3_revise_frozen.zag, sha256
354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392)
is extracted from its committed path
docs/lab/research-lead/overnight-20260928/revise_attack/f3_revise_frozen.zag
via `git show`, hash-verified before every build, and concatenated
BEFORE the world file, unmodified.

## 3. Predicted mechanism traces (adopted from 7e80e52e6)

### 3.1 Treatment (S-TRF)

- F3P3 PLAN [SX,W,W] (attempt 1)
- F3P3 GOAL_REAL 0 (attempt 1)
- F3P3 GOAL_FAIL_GROW_ATTEMPT
- F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@2
- F3P3 REVISED_GROWN replanned
- F3P3 GOAL_REAL 1 (attempt 2)
- NO second F3P3 GOAL_FAIL_GROW_ATTEMPT anywhere in the run.
- NO second F3P3 GROW_OK (goal-fail) anywhere in the run.
- F3P3 FINALRULE V=Y rule=0 [X@2 & !Z@2]
- F3P3 NGROW 1, F3P3 GOAL_OK 1.

Note (carried from the step-9 disclosure): attempt 2 may emit plan
[SX,CZ,W,W] rather than a plan with no SET X, because L_run()
snapshots `init` once before the attempt loop and never refreshes
it; attempt 2 plans against the stale S1 init. Plan shape does not
govern any verdict bar.

### 3.2 Control (S-CTF)

- F3P3 PLAN [W,W] (attempt 1)
- F3P3 GOAL_REAL 0 (attempt 1)
- F3P3 GOAL_FAIL_GROW_ATTEMPT
- F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@2
- F3P3 REVISED_GROWN replanned
- F3P3 GOAL_REAL 1 (attempt 2)
- F3P3 FINALRULE V=Y rule=0 [X@2 & !Z@2]
- F3P3 NGROW 1, F3P3 GOAL_OK 1.

## 4. Verdict rule (frozen, adopted from 7e80e52e6)

Let T = treatment run output, C = control run output (each 3x).
The V0 reference is the committed step-6 setup-validation raw
output (docs/lab/research-lead/overnight-20260928/revise_attack/
raw_valid_n_r1.txt, byte-identical to sealed S-NEG2 per bbdb65c99).

Validity gates (VOID, not a mechanism verdict):
- V0: T lines 1..46 (through "F3P3 REVISED_GROWN replanned") are
  byte-identical to the V0 reference lines 1..46 (cmp clean). If not,
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

Red-team note (4a2b8ef43): the step-10 red team found the planner
can route around inhibitors in time, confounding GOAL_OK as
guard-efficacy evidence on some worlds. No bar here depends on
GOAL_OK alone as guard evidence: T3 (exactly one growth) and T4
(FINALRULE) are the reuse evidence, and the control proves S2
requires the guard. The bars are applied as frozen.

## 5. Kill bars

- K1 (prereg frozen before transfer re-run implementation): PASS
  iff this file's commit strictly precedes every clean re-run world
  file, build script, binary, and run (verified by commit ancestry).
- K2 (transfer tests run): PASS iff treatment and control each ran
  3x with committed raw logs and the verdict rule was applied to
  measured output.
- K3 (pure Zag, 3/3 identical): PASS iff zero Python invocations at
  every stage (authoring, world files, build, runs, analysis, byte
  checks), shell-only dash check clean, every reported configuration
  3/3 byte-identical with zero stderr bytes.

## 6. Honest scope (pre-registered bound)

A PASS here remediates step 9 only: it restores a K4-clean
REVISE-TRANSFER-PASS as citable evidence for the narrowed bounded-L2
reuse characterization. It claims no L3 and no Criterion 0. It does
not overturn the step-10 REVISE-REDTEAM-KILLS of the generic
causal-revision reading, and it does not certify the pipeline: a
follow-up governance re-audit (step 11 re-run) is still required
before any promotion claim. The test measures reuse of one grown
literal in one novel goal configuration with unchanged causal
truth, within one process.
