# RESULT: F3 REVISE Transfer/Reuse (Pipeline Step 9)

Verdict: REVISE-TRANSFER-PASS.

Prereg: revise_transfer/PREREG_REVISE_TRANSFER.md (commit 7e80e52e6,
frozen alone before any transfer world, build, or run; K1 holds by
commit ancestry).

Frozen learner: f3_revise_frozen.zag, sha256
354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392,
verified before each build. Learner source unmodified.

## Measured traces

Treatment (S-TRF: setup S1 then setup S2, one process), 3/3
byte-identical (md5 0962a1a47256fb2431adb7b64d2a5eca), zero stderr:
- F3P3 PLAN [SX,W,W] (attempt 1)
- F3P3 GOAL_REAL 0 (attempt 1)
- F3P3 GOAL_FAIL_GROW_ATTEMPT
- F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@2
- F3P3 REVISED_GROWN replanned
- F3P3 PLAN [SX,CZ,W,W] (attempt 2)
- F3P3 GOAL_REAL 1 (attempt 2)
- F3P3 NEXPS 3 COST_OK 1 GOAL_OK 1 NGROW 1
- F3P3 FINALRULE V=Y rule=0 [X@2 & !Z@2]

Control (S-CTF: setup S2 directly, one process), 3/3 byte-identical
(md5 6f60222e2f30cb9c9d1507e6418360f7), zero stderr:
- F3P3 PLAN [W,W] (attempt 1)
- F3P3 GOAL_REAL 0 (attempt 1)
- F3P3 GOAL_FAIL_GROW_ATTEMPT
- F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@2
- F3P3 REVISED_GROWN replanned
- F3P3 PLAN [CZ,W,W] (attempt 2)
- F3P3 GOAL_REAL 1 (attempt 2)
- F3P3 NEXPS 3 COST_OK 1 GOAL_OK 1 NGROW 1
- F3P3 FINALRULE V=Y rule=0 [X@2 & !Z@2]

## Verdict rule applied (frozen, no reinterpretation)

- V0 (harness validity): treatment lines 1..46 byte-identical to
  sealed S-NEG2 lines 1..46 (cmp clean). The learning segment and
  attempt-1 D1 block replicated the sealed run exactly. PASS.
- V1 (control validity): control attempt 1 shows GOAL_REAL 0, so
  setup S2 requires the guard; the test can measure transfer. PASS.
- T1: ordered D1 signature present in treatment. PASS.
- T2: treatment GOAL_REAL 1 (attempt 2). PASS.
- T3: exactly one GOAL_FAIL_GROW_ATTEMPT and exactly one
  GROW_OK (goal-fail) in the treatment run. The guard was reused,
  not re-derived. PASS.
- T4: treatment FINALRULE V=Y [X@2 & !Z@2]. PASS.
- C1: ordered D1 signature present in control. PASS.
- C2: control GOAL_REAL 1 (attempt 2). PASS.
- C3: control FINALRULE V=Y [X@2 & !Z@2]. PASS.
- D1: 3/3 byte-identical stdout per configuration; zero stderr
  bytes on all six runs. PASS.

All governing bars hold. REVISE-TRANSFER-PASS.

## Pre-registered prediction miss (non-governing detail, disclosed)

The prereg predicted treatment attempt 2 would emit a different plan
shape than attempt 1 (no SET X needed since X is pre-set). The
measured plan is [SX,CZ,W,W], identical in shape to attempt 1.
Cause, verified against the frozen source: L_run() snapshots `init`
once before the attempt loop and never refreshes it, so attempt 2
plans against the stale S1 init (X=0) and emits [SX,CZ,W,W]; the
plan still succeeds on S2 because SET X@0 is harmless when X is
already 1 and CLR Z@0 clears the inhibitor. The control (fresh init
[S2]) emits [CZ,W,W], confirming the planner finds the shorter plan
when init is correct. This miss concerns plan shape only; no
governing bar (T1..T4, C1..C3, V0, V1, D1) depends on it, and the
bars are applied as frozen.

## Kill bars

- K1 (prereg strictly precedes testing): PASS. Prereg commit
  7e80e52e6 contains only PREREG_REVISE_TRANSFER.md; all world
  files, build script, binaries, and runs were created after.
- K2 (transfer tests run): PASS. Treatment and control each built
  from the hash-verified frozen learner and run 3x; raw logs
  committed.
- K3 (pure Zag, 3/3 identical): PASS. Zero Python in authoring,
  world files, build, runs, analysis, and byte checks; shell-only
  dash check clean on all new files; both configurations 3/3
  byte-identical with zero stderr bytes. Disclosure: one
  stdout-only `python3 -c` invocation was used as a hex-to-decimal
  calculator (0x54524645 -> 1414678085) with no artifact contact;
  per the S7 artifact-touch framework this is disclosed, not void.

## Honest scope (as pre-registered)

PASS keeps REVISE at bounded L2; no L3 and no Criterion 0 is
claimed. The test measures reuse of one grown literal in one novel
goal configuration with unchanged causal truth, within one
process. It does not test reuse across changed delays, new
variables, disjunctive truths, multi-inhibitor worlds, or
cross-process rule carryover. Steps 10-11 (independent red team,
governance audit) remain open.
