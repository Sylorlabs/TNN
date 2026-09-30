# RESULT: F3 REVISE Transfer/Reuse Clean Re-run (Pipeline Step 9 Remediation)

Verdict: REVISE-TRANSFER-PASS.

Prereg: revise_transfer_clean/PREREG_REVISE_TRANSFER_CLEAN.md (commit
6f95d7b1c, frozen alone before any clean re-run world file, build
script, binary, or run; K1 holds by commit ancestry, verified below).

This re-run remediates the step-9 K4 contamination disclosed in
c3c3e3bc8 (one stdout-only `python3 -c` hex-to-decimal calculator use
during authoring). Design, world files, frozen learner, verdict rule,
and honest scope are adopted unchanged from the frozen step-9 prereg
7e80e52e6.

## Provenance (purity remediation)

- world_stf.zag and world_sct.zag: extracted via `git show
  c3c3e3bc8:...` into revise_transfer_clean/, then `cmp`-verified
  byte-identical to the committed step-9 artifacts. No constant was
  recomputed by any tool or by hand; the magic literal 1414678085
  travels as a frozen literal inside the copied bytes.
- f3_revise_frozen.zag: extracted via `git show` from the committed
  revise_attack/ path; sha256
  354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392
  verified before every build (the build script aborts on mismatch).
- Toolchain for this re-run: sh, git, znc, sha256sum, md5sum, cmp,
  grep, wc, cut, head, and the shell-only
  worker_snippets/check_no_dash.sh. Zero Python invocations at every
  stage (authoring, world files, build, runs, analysis, byte checks).

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

The clean re-run md5s are identical to the step-9 contaminated run
md5s, as expected for byte-identical inputs. This independently
confirms the disclosed python3 calculator had no artifact contact.

## Verdict rule applied (frozen, no reinterpretation)

- V0 (harness validity): treatment lines 1..46 byte-identical to the
  V0 reference (revise_attack/raw_valid_n_r1.txt lines 1..46; cmp
  clean). PASS.
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

## Kill bars

- K1 (prereg strictly precedes re-run implementation): PASS. Prereg
  commit 6f95d7b1c contains only
  PREREG_REVISE_TRANSFER_CLEAN.md; all clean re-run world files,
  build script, binaries, and runs were created after (verified by
  `git merge-base --is-ancestor`).
- K2 (transfer tests run): PASS. Treatment and control each built
  from the hash-verified frozen learner and run 3x; raw logs
  committed.
- K3 (pure Zag, 3/3 identical): PASS. Zero Python at every stage;
  shell-only dash check clean on all new files; both configurations
  3/3 byte-identical with zero stderr bytes.

## Build-script note (cosmetic, disclosed)

TRANSFER_BUILD.sh exits 1 when invoked as `all` because the final
diagnostic glob `raw_"all"*_r*.txt` matches no files. All builds and
all six runs complete before that line; every measured artifact
above was produced by the script. The script is committed as run.

## Honest scope (as pre-registered)

This PASS remediates step 9 only: it restores a K4-clean
REVISE-TRANSFER-PASS as citable evidence for the narrowed
bounded-L2 reuse characterization. It claims no L3 and no
Criterion 0. It does not overturn the step-10 REVISE-REDTEAM-KILLS
of the generic causal-revision reading. A follow-up governance
re-audit of step 9 (step 11 re-run) is still required before any
promotion claim. The test measures reuse of one grown literal in
one novel goal configuration with unchanged causal truth, within
one process.
