# VERDICT: H-PI-REV2 step-5 re-execution under the AMENDED prereg (wave-20261001-2021pdt)

Lane: docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
Amended prereg (FROZEN, commit 72168c608):
docs/lab/rsi/runs/wave-20261001-1721pdt/HPIREV2/PREREG_PI_REV2_STEP5_BASELINE_AMENDED.md
Evidence: EXECUTION_LOG.md, run transcripts REV_run{1..3}.txt,
B0/B1/B1T/B2 run logs (this lane). All measurements below are from
3/3 byte-identical runs (sha256 in the execution log).

The original step-5 verdict (BASELINE-FAIL, wave-20261001-1421pdt) is
not relitigated and stands unchanged on its own provenance. This
verdict governs only the re-execution under the amended bars.

## Per-bar scorecard

Bar | Threshold | Measured | Result
K-SB1 (problem real): B0 must mispredict F1r (predict "bbb", not "rrr") | "B0 PREDICT rab -> bbb", 3/3 identical | PASS
K-SB2 (revision cheaper than re-search): revision_evals < b1_enumerated (1055, strict inequality) | revision_evals=5 (3 diagnosis candidates + 1 primitive-construction test + 1 SPECIALIZE application), B1 programs-evaluated=1055, first-fit -1 | PASS (5 < 1055)
K-SB3 (revision beats storage on reuse): revised procedure predicts "rqw"->"rrr" with zero new revisions; B2 mispredicts "rqw" or needs a new stored entry | REV: "PREDICT rqw -> rrr [ok]", "CHECK P8-F2-reuse-no-revision: PASS", zero DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines after the reuse check; B2: "B2 PREDICT rqw -> www" (mispredict, no stored entry) vs "B2 PREDICT rab -> rrr" (stored, correct) | PASS
K-SB4a (revised procedure correctness): fails=0 across the 5 checks ("abc"->"ccc", "xy"->"xx", "defg"->"gggg", "rab"->"rrr", "rqw"->"rrr") | all 5 emit [ok]: abc->ccc, xy->xx (conflict-rule update), defg->gggg, rab->rrr, rqw->rrr; "=== RESULT fails=0 ===", BUILD-PASS | PASS
K-SB4b (baseline competence): B1 over T alone returns first_fit >= 0 and the fitted program is correct on all of T (fails=0) | B1T: first-fit-index=38 (>= 0; matches frozen v1 discovery index 38 [N C1 SUB]), programs-evaluated=39, fails-on-T=0 | PASS
K-SB4c (verified-impossibility recheck): B1 over T+F1r returns first_fit=-1 with programs-enumerated=1055 | B1: first-fit-index=-1, programs-evaluated=1055 (3/3 identical; matches the K-RV2-1b verification in K_RV2_1B_VERIFICATION.md: the enumeration is exhaustive, no false negative) | PASS
K-SB5 (determinism): all 15 runs exit 0, 3/3 byte-identical stdout per binary, zero stderr bytes | 15/15 exit 0; cmp clean for all 5 binaries; all 15 stderr files 0 bytes | PASS
K-SB6 (purity and docs): pure Zag only, zero Python at any stage; zero em-dash and zero en-dash bytes in all lane files | executables used: safebin bash, awk, cat, cmp, cp, cut, date, diff, git, grep, head, mkdir, sha256sum, stat, tail, tee, timeout, touch, tr, uniq, wc, which, znc; `which python3`/`which python` print nothing under the safebin PATH; byte scan of all lane text files shows zero em-dash and zero en-dash bytes (compiler-emitted lint em-dash confined to /tmp build logs) | PASS

## Machine-greppable cost accounting

revision_evals=5
b1_enumerated=1055
b1_first_fit_index=-1
b1_wall_ms=4
b1t_wall_ms=3
revision_wall_ms=5
b0_wall_ms=5
b2_wall_ms=3
binary_bytes_rev2_r_bin=106770
binary_bytes_b0_bin=22331
binary_bytes_b1_bin=34776
binary_bytes_b1t_bin=34825
binary_bytes_b2_bin=26588
source_delta_lines=946
new_semantic_cases=0
new_modes=0
new_bridges=0

## Shared-code disclosure (sealing protocol)

Baselines share byte-exact extracts of the frozen Section A discovery
machinery from proc_revise2.zag at 847a8f10f (helpers, eval, program
store, benum, sequence staging); b0.zag, b1.zag, b2.zag are byte-exact
copies of the original step-5 baseline sources (sha256 match). b1t.zag
reuses b1.zag lines 1-224 byte-exact (verified by diff) and adds only
the new T-alone main (main_b1t.txt, 75 lines). No Section B
revision-machinery code (observe, diagnose, build_test, specialize,
branch predict, rollback) is shared with any baseline.

## Killing evidence

None under the amended bars. Every amended bar passes. The amended
K-SB4a/4b/4c triple reproduces the substance of the original failure
analysis: B1 cannot fit T+F1r (verified impossibility holds as a
checked numeric fact: first_fit=-1, 1055 evaluated), the revised
procedure is fully correct (fails=0 on all 5 checks), and B1 is a
working re-search baseline on the pre-counterexample data
(first_fit=38, fails-on-T=0). The re-execution does NOT reproduce
BASELINE-FAIL; no bar failed, so no bar was moved.

## Honest boundaries

Bounded L2 ceiling per the amended prereg: the revision machinery
repairs a supplied procedure after a counterexample; it does not
invent a representation, and the reconstruction template
(SPECIALIZE as IF(P_test, alt, v_old)) is researcher-authored. This
step-5 PASS means the revision is genuinely cheaper than re-search
and genuinely reuses beyond storage; it is not evidence toward L3
and must not be claimed as such. No protected-core changes
(new_semantic_cases=0, new_modes=0, new_bridges=0). Sealing held: the
F1r-reuse input "rqw" is presented only after VERSION v3 is ACTIVE.

## Verdict

step-5 PASS under the amended prereg. Failing bars: none.
All 8 amended bars pass (K-SB1, K-SB2, K-SB3, K-SB4a, K-SB4b, K-SB4c,
K-SB5, K-SB6). This is not SURVIVES; the 11-step pipeline continues to
step 6. The original BASELINE-FAIL verdict stands unchanged and is not
retroactively altered by this verdict.

No em-dashes in this documentation.
