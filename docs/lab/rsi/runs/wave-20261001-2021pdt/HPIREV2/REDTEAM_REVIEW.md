# REDTEAM REVIEW: H-PI-REV2 step-5 PASS under amended prereg (wave-20261001-2021pdt)

Reviewer role: independent red team, second opinion on the lane worker's step-5 PASS claim.
Method: safebin-only shell, pinned znc untouched for builds; independent re-runs of lane binaries;
frozen-code reads; git provenance checks. Toolchain guard recorded in NAMECHECK_REDTEAM.md
(Step 0: `which python3` prints nothing under safebin PATH). No em-dashes in this file.

## Verdict: EVIDENCE HOLDS

The step-5 PASS under the amended prereg survives scrutiny. Every axis below was attacked
directly; no killing evidence was found. The PASS is adoptable as what it claims to be:
step-5 PASS under the amended bars, not SURVIVES, with the original BASELINE-FAIL unchanged
and an explicit bounded-L2 ceiling.

## Axis 1: Amendment integrity (did the amendment weaken K-SB4?)

Finding: NO. The amendment corrects a genuine design flaw and preserves discriminating power.

What changed, exactly (original PREREG_PI_REV2_STEP5_BASELINE.md vs AMENDED):

- K-SB1: unchanged verbatim.
- K-SB2: unchanged threshold (strict inequality). The comparator is pinned to the verified
  numeric value "(1055 with first-fit -1)". This is a fact pin, not a threshold move.
- K-SB3: unchanged verbatim.
- K-SB4 (unsatisfiable): "B1's fitted program is correct on T+F1r" presupposes a fitted
  program. K-RV2-1b (verified against frozen code in K_RV2_1B_VERIFICATION.md: "abc"->"ccc"
  requires eval=2 and "rab"->"rrr" requires eval=0 at identical (prog, k=0, n=3) arguments,
  and eval_prog is a deterministic pure function, so no program can fit both) proves no such
  program exists. The clause is unsatisfiable as written. Genuine design flaw, confirmed.
- K-SB4a: keeps the revision-correctness conjunct verbatim, strengthened numerically to
  "fails=0 across the 5 prediction checks" with the exact 5 checks enumerated. Same
  discriminating power as the original's first conjunct.
- K-SB4b: NEW. B1 over T alone must return first_fit >= 0 with fails=0 on T. Real kill
  condition (kills if the baseline is broken on pre-counterexample data). Low bar by design,
  but its stated role is comparison-validity (pins B1 as working, not broken), and it is
  stated honestly. Measured first_fit=38 matches the frozen v1 discovery index 38 [N C1 SUB].
  The threshold is not tuned to 38 (any index >= 0 with fails=0 passes).
- K-SB4c: NEW. B1 over T+F1r must return first_fit=-1 with programs-enumerated=1055.
  Real kill condition (kills if the verified impossibility is falsified). This keeps the
  amendment honest instead of silently dropping the unsatisfiable conjunct.
- K-SB5: same kill conditions; run matrix expanded 12 to 15 runs (B1-on-T x3 added for 4b).
- K-SB6: unchanged verbatim.

Non-killing observations: (a) the amendment was drafted with knowledge of the 1421pdt
outputs (REV fails=0, B1 -1/1055 were already recorded), but the thresholds are the natural
ones (fails=0, >= 0, -1/1055 as verified fact), not tuned to a number; (b) the 1421pdt judge
ruling said to "preserve the 12-run matrix", while the amendment expanded to 15 runs
transparently (stated in the amendment as a run-matrix note for the coordinator to rule on);
the added runs are a superset and strictly strengthen the determinism evidence, and the
lane executed under the amended text. Neither observation weakens any bar.

## Axis 2: Metric gaming (is revision_evals=5 suspiciously low?)

Finding: NO gaming. The number is the true count under the frozen formula, verified
against frozen code.

Prereg formula (identical in original and amended prereg): diagnosis (p, byte) candidates
ranked + primitive-construction byte-equality tests + the single SPECIALIZE application.

Verified against the frozen proc_revise2.zag (committed 847a8f10f, working-tree sha256
dd3cb02dbd883243e350a89e328e570c35e2dc7a71f49f4e3aa51f0603a99a12, git cat-file match):

- diagnose (lines 380-478): candidates are deduped (pos, byte) pairs covering all failing
  records. For the P8 failing set (single record "rab"), positions 0,1,2 give (0,114),
  (1,97), (2,98): 3 candidates ranked position-ascending, winner (0,114). Transcript
  shows exactly "DIAGNOSIS pos=0 byte=114 conflicts=0". 3 confirmed.
- build_test: constructs exactly one byte-equality test, one emit. 1 confirmed.
- SPECIALIZE: one "VERSION v3 ACTIVE (parent v2)". 1 confirmed.
- revision_evals = 3 + 1 + 1 = 5. Correct per the frozen formula.

The lane additionally disclosed the P8 alt search (3 programs evaluated, first fit at
index 2 C0, "CHECK P8-F2-alt-C0: PASS"). Even 5+3=8 is far below 1055. The strict
inequality 5 < 1055 has enormous headroom, but that is the nature of the comparison
(direct diagnosis of one counterexample vs exhaustive re-enumeration), and the threshold
was not moved from the original prereg.

## Axis 3: Knowledge vs architecture (is the PASS built on smuggled knowledge?)

Finding: NO smuggled knowledge. Checks performed:

- b0.zag, b1.zag, b2.zag sha256 (c6ccc64a..., 532ec1df..., 9c476796...) match the
  EXECUTION_LOG record: byte-exact copies of the original 1421pdt baseline sources.
- b1t.zag lines 1-224 diff against b1.zag lines 1-224: empty (byte-exact). The new
  main_b1t.txt (75 lines, read in full) stages only the frozen T fixtures
  ("abc"->"ccc", "xy"->"yy", "defg"->"gggg"), enumerates in frozen dsearch order,
  takes the first fit, verifies. No hardcoded index 38, no "rab"/"rqw", no byte 114.
- b1.zag stages ("rab","rrr") only as sequence index 3 (the T+F1r set the prereg
  requires); grep finds no byte-114 special-casing and no "rqw".
- b2.zag stores only ("rab"->"rrr") (line 155); "rqw" is predicted through the
  lookup-miss path and mispredicts ("B2 PREDICT rqw -> www") exactly as the L0-storage
  control is designed to. No new-entry mechanism exists in the B2 binary.
- REV binary built from the frozen proc_revise2.zag (hash match above); the 'r' arrives
  via argv[1] per the frozen interface; the reuse probe "rqw" is presented by the frozen
  binary after "VERSION v3 ACTIVE" (transcript lines 62-69), and zero
  DIAGNOSIS/PRIMITIVE-CONSTRUCTED/VERSION lines appear after the reuse check.
- Adversary byte 'r' disjointness rests on the frozen ADVERSARY_BYTE_SET4.md audit,
  inherited, not re-decided here.

## Axis 4: Determinism re-verification (independent re-runs)

Finding: CONFIRMED byte-identical. I re-ran the lane's binaries from scratch:

- ./b1_bin: exit 0, stdout byte-identical to B1_run1.txt, stderr 0 bytes,
  sha256 0c5f9370256fcb37b3e92730fd44e8d98bb645c84fa8eefaba0d78ae844043c4.
- ./rev2_r_bin r: exit 0, stdout byte-identical to REV_run1.txt, stderr 0 bytes,
  sha256 d5eb722d8b0a204ce155e7d82f237fa6682d88d9d0d885b930629e1c69913801.
- ./b1t_bin: exit 0, stdout byte-identical to B1T_run1.txt.

Both hashes match the EXECUTION_LOG record AND the wave-20261001-1421pdt debate record
hashes (d5eb722d..., c910b187..., 0c5f9370..., ca3df82d...), confirming the lane's
cross-lane byte-identity claim. No mismatch anywhere.

## Axis 5: Commit-order (did the amended prereg predate all implementation?)

Finding: PASS. Independently verified:

- `git log` on PREREG_PI_REV2_STEP5_BASELINE_AMENDED.md returns exactly one commit:
  72168c60803b95b3b586eb1cf6f1fc9bd001b174 (2026-10-02 00:39:47 UTC), whose stat shows
  only 4 docs files (AMENDMENT_STEP5_TRANSPARENT.md, K_RV2_1B_VERIFICATION.md,
  NAMECHECK.md, PREREG_PI_REV2_STEP5_BASELINE_AMENDED.md): a pure-docs, writing-only
  re-freeze, committed alone before any re-execution.
- `git log --diff-filter=A` under docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
  is empty, and the whole lane dir is untracked working-tree state: every baseline
  source, binary, run log, and lane doc was created after the freeze. No implementation
  work predates 72168c608. No commits, no push, no reset, no rebase performed by me.

## Axis 6: Scope honesty (does the lane overclaim?)

Finding: NO overclaim. All three lane docs state, in plain terms:

- The verdict governs only the re-execution under the amended bars; the original
  BASELINE-FAIL (wave-20261001-1421pdt) is not relitigated and stands unchanged.
- This is step-5 PASS, not SURVIVES; the 11-step pipeline continues to step 6.
- Bounded L2 ceiling: the revision machinery repairs a supplied procedure after a
  counterexample; the SPECIALIZE template is researcher-authored; a PASS is not
  evidence toward L3 and must not be claimed as such.
- new_semantic_cases=0, new_modes=0, new_bridges=0.

No language implies the original failure is overturned or that the bar was moved to
force a pass.

## Decisive reason (for the coordinator)

EVIDENCE HOLDS. The amendment fixes a provably unsatisfiable clause (K-RV2-1b verified
against frozen code: no program can fit T+F1r under the frozen evaluator) with a
4a/4b/4c triple that keeps every kill condition live (4a fails=0 unchanged, 4b kills on
a broken baseline, 4c kills on falsification of the impossibility); revision_evals=5 is
the true count under the frozen formula (3 deduped diagnosis candidates + 1 primitive
test + 1 SPECIALIZE, verified in frozen code); independent re-runs of b1_bin, b1t_bin,
and rev2_r_bin are byte-identical to the lane transcripts and to the 1421pdt record
hashes; the amended prereg sits in a single pure-docs commit (72168c608) that predates
all untracked lane implementation; and the lane claims only step-5 PASS under the
amended bars with the original BASELINE-FAIL explicitly unchanged and a bounded-L2,
not-L3 ceiling.
