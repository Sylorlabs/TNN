# RESULT: F3 REVISE Ablation (Pipeline Step 8)

Verdict: REVISE-ABLATION-PASS.

Parent prereg: revise_ablation/PREREG_REVISE_ABLATION.md (commit
6dcb1f11b), frozen alone before any ablation learner file, build
script, binary, or run existed. K1 holds by commit ancestry
(prereg commit contains only the prereg file and strictly
precedes all ablation artifacts). Parent chain: design
ca157c743, builder prereg c197e7cd8, builder result 7009d711c
(REVISE-PASS), sealed prereg 8cdf0992a, sealed result 1df8addec
(REVISE-SEALED-PASS), repro 7407dd4a7 (REVISE-REPRO-PASS),
baseline prereg 4786633c5 plus amendment db585360a, baseline
result c810d5f55 (REVISE-BASELINE-PASS), attack prereg 12da75511,
attack result bbdb65c99 (REVISE-ATTACK-SURVIVES), OOD prereg
7bf467d35, OOD result 1125be9bb (REVISE-OOD-PASS). Pipeline: this
completes step 8 (ablation) only.

## 1. What was ablated

Two independent single-line excisions from the frozen learner
(sha256 354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392,
verified by the build script before derivation):

- A1 (no D1): f3_revise_noD1.zag. Frozen line 1231
  `      if(attempt<ATTEMPT_MAX){` replaced with
  `      if(0==1){`. The goal-fail growth block never executes;
  a failed attempt ends in the honest-stop else branch.
- A2 (no OP-GROW): f3_revise_noGROW.zag. Frozen line 994
  `        if((rs[grb] as i32)<3){` replaced with
  `        if(0==1){`. On rule refutation the GROW_FAIL path
  runs (rule dropped); F3_grow_search is never called from the
  trial loop.

diff against the frozen learner shows exactly one changed line
per ablated learner (1231c1231 and 994c994 respectively); the
construction passes the frozen check. The Zag compiler accepted
`if(0==1){` with no errors.

## 2. H-A1N: A1 on S-NEG2 (D1 causally necessary for S-NEG2)

All items hold on all 3 runs (md5
f06836e9d8753518f4de2943fdd0c456, 3/3 byte-identical):

- (a) exactly one "F3P3 GOAL_REAL" line:
  "F3P3 GOAL_REAL 0 (attempt 1)". No attempt 2 exists.
- (b) zero "GOAL_FAIL_GROW_ATTEMPT" lines.
- (c) zero "GROW_OK (goal-fail)" lines.
- (d) "F3P3 FINALRULE V=Y rule=0 [X@2]" (single literal; no
  "&", no "!Z@2").
- (e) "F3P3 GOAL_OK 0" present (NEXPS 2, NGROW 0).
- (f) "F3P3 RESULT REVISE-FAIL" present.
- (g) exit 0, zero stderr bytes, all 3 runs.

Without D1, S-NEG2 fails exactly as predicted: the inhibitor is
never guarded against, no replan occurs. D1 is causally
necessary for the sealed S-NEG2 success.

## 3. H-A1C: A1 on S-CONJ2 (control)

stdout md5 84ab277e7535c740c5210c2065a8cef6 on all 3 runs:
byte-identical to the frozen sealed S-CONJ2 output. The A1
excision is behaviorally inert where D1 never fired. Control
holds; the excision did not perturb anything else.

## 4. H-A2C: A2 on S-CONJ2 (OP-GROW causally necessary for S-CONJ2)

All items hold on all 3 runs (md5
2d5e060e079a7ffc9871103b116cd266, 3/3 byte-identical):

- (a) zero lines matching "F3P3 GOAL_REAL 1".
- (b) no "F3P3 FINALRULE" line contains both "X@3" and "Z@2".
  In fact no V=Y FINALRULE line exists at all.
- (c) "F3P3 RESULT REVISE-FAIL" present.
- (d) exit 0, zero stderr bytes, all 3 runs.

Observed internal path (documented, not verdict-bearing): the
discovered singletons were refuted and dropped one by one
(GROW_FAIL path each time, NGROW 0); the goal phase found
"F3P3 PLAN none found (attempt 1)"; NEXPS 4, GOAL_OK 0. No
conjunction can form without the Phase 3 growth call site.
OP-GROW is causally necessary for the sealed S-CONJ2 success.

## 5. H-A2N: A2 on S-NEG2 (control)

stdout md5 85ebb436b4f7d6eac370466bc98a878c on all 3 runs:
byte-identical to the frozen sealed S-NEG2 output. The A2
excision is behaviorally inert where no Phase 3 growth
occurred. Control holds.

## 6. Verdict rule application (frozen)

Per PREREG_REVISE_ABLATION.md section 6: REVISE-ABLATION-PASS
iff H-A1N, H-A1C, H-A2C, H-A2N all hold and K1, K2, K3 pass.
All four harnesses hold. Neither control world deviated, so no
construction failure occurred.

Verdict: REVISE-ABLATION-PASS.

## 7. Kill bars

- K1 (prereg frozen before ablation): PASS. Commit 6dcb1f11b
  contains only PREREG_REVISE_ABLATION.md and strictly precedes
  every ablation learner file, build script, binary, and run
  (verified by commit ancestry; no ablation artifact existed at
  freeze time).
- K2 (ablations run): PASS. Four configurations (a1n, a1c,
  a2c, a2n) each built once and run 3x; all 12 raw stdout and
  12 raw stderr files committed, plus build logs.
- K3 (pure Zag, 3/3 identical): PASS. Shell, znc, git, grep,
  diff, cmp, md5sum, sha256sum, wc, sed, chmod only; zero
  Python invocations at every stage (authoring, derivation,
  build, run, analysis, byte checks). Every reported
  configuration is 3/3 byte-identical with zero stderr bytes
  and exit 0. No em/en dash bytes in any new file (checked
  with the shell-only worker_snippets/check_no_dash.sh).

## 8. Honest scope

This step confirms the causal necessity of the two growth call
sites by clean double dissociation: removing D1 kills S-NEG2
only; removing OP-GROW kills S-CONJ2 only; each control world
is byte-identical to the frozen run. Together with the sealed
F-RABLN result (removing the shared condition (b) gate kills
both worlds), all three growth-related claims now have direct
causal evidence. REVISE-ABLATION-PASS keeps REVISE at bounded
L2; it claims no L3, no Criterion 0, and advances the pipeline
past step 8 only. Steps 9-11 (transfer/reuse, independent red
team, governance audit) remain open. The contaminated research
paper was not touched.

## 9. Evidence index (all under revise_ablation/)

- PREREG_REVISE_ABLATION.md (commit 6dcb1f11b, frozen alone first)
- ABLATION_BUILD.sh (derive + run; verifies frozen sha256)
- f3_revise_noD1.zag (A1; one-line diff vs frozen)
- f3_revise_noGROW.zag (A2; one-line diff vs frozen)
- run_a1n.zag / bin_a1n / raw_a1n_r{1,2,3}.txt/.err
  (md5 f06836e9d8753518f4de2943fdd0c456)
- run_a1c.zag / bin_a1c / raw_a1c_r{1,2,3}.txt/.err
  (md5 84ab277e7535c740c5210c2065a8cef6, control)
- run_a2c.zag / bin_a2c / raw_a2c_r{1,2,3}.txt/.err
  (md5 2d5e060e079a7ffc9871103b116cd266)
- run_a2n.zag / bin_a2n / raw_a2n_r{1,2,3}.txt/.err
  (md5 85ebb436b4f7d6eac370466bc98a878c, control)
- build_a1n.err, build_a1c.err, build_a2c.err, build_a2n.err
  (znc notices only; no errors)
- RESULT_REVISE_ABLATION.md (this file)
