# RESULT: F3 REVISE OOD Test (Pipeline Step 7)

Verdict: REVISE-OOD-PASS.

Parent prereg: revise_ood/PREREG_REVISE_OOD.md (commit 7bf467d35),
frozen alone before any OOD world file, build script, binary, or run
existed. K1 holds by commit ancestry (prereg commit strictly
precedes all OOD artifacts). Parent chain: design ca157c743,
builder prereg c197e7cd8, builder result 7009d711c (REVISE-PASS),
sealed prereg 8cdf0992a, sealed result 1df8addec
(REVISE-SEALED-PASS), repro 7407dd4a7 (REVISE-REPRO-PASS), baseline
prereg 4786633c5 plus amendment db585360a, baseline result c810d5f55
(REVISE-BASELINE-PASS), attack prereg 12da75511, attack result
bbdb65c99 (REVISE-ATTACK-SURVIVES). Pipeline: this completes step 7
(OOD test) only.

## 1. What was tested

Two distribution-shift axes, both outside every world the learner
had previously seen:

- S-OOD-D3: Y(t) = X(t-3) AND NOT Z(t-3). Delay shift WITHIN the
  frozen delay currency (dcur=4). Tests delay-parameter
  generalization of discovery, trial, D1 growth, and replanning.
- S-OOD-D6: Y(t) = X(t-6). Delay shift BEYOND the frozen delay
  currency. Tests graceful degradation: the mechanism must not
  invent a rule, crash, or hang.

The frozen learner (sha256
354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392,
verified by the build script before each build) was concatenated
unmodified with each OOD world. No learner modification of any kind.

## 2. S-OOD-D3 results (3/3 byte-identical, md5 5ab8218bde5fbb2e76733ef4b476729a)

Frozen bar OOD-D3-PASS, all items verified on all 3 runs:

- (a) "F3P3 GOAL_REAL 0 (attempt 1)": present.
- (b) "F3P3 GOAL_FAIL_GROW_ATTEMPT": present.
- (c) "F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@3": present.
- (d) "F3P3 GOAL_REAL 1 (attempt 2)": present.
- (e) "F3P3 FINALRULE V=Y rule=0 [X@3 & !Z@3]": present.
- (f) 3/3 byte-identical stdout, exit 0, zero stderr bytes.

The full predicted trace occurred: discovery found [X@3], the
trial confirmed it, attempt 1 failed on the Z=1 inhibitor, D1 grew
the !Z@3 guard, attempt 2 replanned around the inhibitor and
succeeded. The D1 revision mechanism generalizes across the delay
parameter within the frozen currency.

RESULT-line note (disclosed, verdict-excluded): the prereg
predicted the RESULT line would read REVISE-FAIL on the
world-calibrated REFUTE-DRILL blemish theory. On S-OOD-D3 the
drill actually passed ("F3P3 DRILL_RESULT DRILL-PASS") and the
RESULT line reads "F3P3 RESULT REVISE-PASS". The prereg explicitly
excluded the RESULT line from the verdict, so this misprediction
about the drill's world calibration does not affect the verdict.
Every mechanism line matches the frozen bar exactly.

## 3. S-OOD-D6 results (3/3 byte-identical, md5 a3729a0233600d6069574419812a1d43)

Frozen bar OOD-D6-PASS, all items verified on all 3 runs:

- (a) "F3P3 RESULT PHASE3-FAIL no-effect-vars": present.
- (b) No "GOAL_REAL" line anywhere: confirmed (0 matches, all runs).
- (c) "SEALED DONE mask=1": present.
- (d) 3/3 byte-identical stdout, exit 0, zero stderr bytes.

The predicted boundary failure occurred: OP-PROP found no
candidate literal for any var at delays 1..4 (the d=6 truth is
inexpressible), ne=0, and the learner halted with the disclosed
no-effect-vars stop before the validation loop, drills, and goal
phase. No rule was invented, no crash, no hang.

## 4. Verdict rule application (frozen)

Per PREREG_REVISE_OOD.md section 4: REVISE-OOD-PASS iff
OOD-D3-PASS and OOD-D6-PASS both hold. Both hold. No crash, hang,
non-determinism, or stderr bytes on any run.

Verdict: REVISE-OOD-PASS.

## 5. Kill bars

- K1 (prereg frozen before implementation): PASS. Commit 7bf467d35
  contains only PREREG_REVISE_OOD.md and strictly precedes every
  OOD world file, build script, binary, and run (verified by commit
  ancestry).
- K2 (OOD tests run): PASS. Both worlds 3x each against the frozen
  learner, all raw logs committed.
- K3 (pure Zag, 3/3 identical): PASS. Shell, znc, git, grep, diff,
  md5sum, sha256sum only; zero Python at every stage (authoring,
  world files, build, run, analysis, byte checks via shell-only
  check_no_dash.sh). Every reported configuration is 3/3
  byte-identical with zero stderr bytes. No em/en dash bytes in any
  new file.

## 6. Honest scope

This tested two OOD axes: delay-parameter generalization within
the frozen currency (D1 revision works at delay 3 exactly as
predicted) and graceful degradation beyond it (honest
no-effect-vars stop, no hallucinated rule). It does not test
multi-inhibitor worlds, the 3-literal cap boundary, delays beyond
6, disjunctive truths, or transfer/reuse. REVISE-OOD-PASS keeps
REVISE at bounded L2; it claims no L3, no Criterion 0, and
advances the pipeline past step 7 only. Steps 8-11 remain open.
The contaminated research paper was not touched.

## 7. Evidence index (all under revise_ood/)

- PREREG_REVISE_OOD.md (commit 7bf467d35, frozen alone first)
- OOD_BUILD.sh (build script; verifies frozen learner sha256)
- world_ood_d3.zag, world_ood_d6.zag (OOD worlds, authored post-freeze)
- run_ood_d3.zag / bin_ood_d3 /
  raw_ood_d3_r{1,2,3}.txt/.err (md5 5ab8218bde5fbb2e76733ef4b476729a)
- run_ood_d6.zag / bin_ood_d6 /
  raw_ood_d6_r{1,2,3}.txt/.err (md5 a3729a0233600d6069574419812a1d43)
- build_ood_d3.err, build_ood_d6.err (znc notices only; no errors)
- RESULT_REVISE_OOD.md (this file)
