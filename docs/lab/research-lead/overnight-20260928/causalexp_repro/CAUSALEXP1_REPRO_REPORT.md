# H-CAUSALEXP1 Independent Reproduction Report

Date: 2026-09-30. Reproducer: independent reproduction worker (subagent eacba55a).

## Verdict: REPRODUCED

The builder's BUILD-PASS claim for H-CAUSALEXP1 reproduces exactly from
committed source. This completes step 4 of the 11-step frontier promotion
pipeline. The claim now proceeds to step 5 (simple-baseline comparison) and
step 6 (alternative-explanation attack), which the parent schedules.

This report is a reproduction verdict, not a promotion. The mechanism remains
BUILD-PASS, bounded L2, and is NOT promoted to SURVIVES.

## Method (pure Zag verification only)

Tools used: git, znc, grep, awk, md5sum, cmp, wc. Zero Python at every stage.
No em dashes in this report (byte-checked before commit).

## Evidence, item by item

1. SOURCE FROM COMMITTED BLOB, NOT WORKING TREE. Extracted
   `causalexp.zag` via
   `git show ce8f1eddb:docs/lab/research-lead/overnight-20260928/causalexp_frontier/causalexp.zag`.
   The working tree copy was never read or compiled.

2. FROZEN TOOLCHAIN. Built with
   `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`,
   reporting `znc 2026.07.0-dev (edition 2026)`, matching the builder's
   frozen toolchain. Build exit 0.

3. THREE RUNS, BYTE-IDENTICAL, MD5 MATCH. Three consecutive runs of the
   reproducer-built binary:
     - exit code 0 on all three runs, stderr empty (0 bytes) on all three
     - output md5 `612580bd641860d021dd48b453e2295b` on all three runs
     - cmp confirms run_1 == run_2 == run_3 byte-for-byte
     - the committed raw log at
       `ce8f1eddb:docs/lab/research-lead/overnight-20260928/causalexp_frontier/CAUSALEXP1_RAW.txt`
       has md5 `612580bd641860d021dd48b453e2295b`, identical to the
       reproduced output
   The builder's claimed md5 `612580bd641860d021dd48b453e2295b` matches
   exactly. K-CX-7 determinism claim confirmed.

4. PREREG ANCESTRY. `git merge-base --is-ancestor bd883d969 ce8f1eddb`
   returns true. Prereg commit `bd883d969` (2026-09-30 00:39:57 +0000) is a
   strict ancestor of result commit `ce8f1eddb` (2026-09-30 00:42:15 +0000).
   The implementation files (`causalexp.zag`, `CAUSALEXP1_RAW.txt`,
   `CAUSALEXP1_RESULT.md`) first appear in `ce8f1eddb`; they do not exist in
   the prereg commit. Prereg-before-implementation ordering is intact.

5. PYTHON CONTAMINATION CHECK. `git diff --name-only bd883d969..ce8f1eddb`
   filtered for `*.py` returns no files. The range contains concurrent
   workers' files (cu7_adversary, devint_worker2, u11_adversary, paper
   updates) but zero `.py` files. The causalexp implementation path contains
   only `causalexp.zag` (Zag source), the raw output, and the result report.

6. THE 7 FROZEN KILL BARS ARE THE BUILDER'S CLAIMED BARS. The 7 bars below
   were read directly from the committed prereg file
   `bd883d969:docs/lab/research-lead/overnight-20260928/causalexp_frontier/PREREG_CAUSALEXP1.md`
   and verified against the reproduced output:

   K-CX-1 (passive indistinguishability): PASS. Reproduced output shows 6
   PASSIVE-CHECK lines (3 per world), all `ev=6/6`, all three hypotheses
   LIVE entering the active loop in both worlds. No passive elimination.

   K-CX-2 (explicit representation): PASS. HYPO lines present for all three
   edge codes (X2Y, Y2X, NONE) with status=LIVE and ev=6/6 in each world;
   8 PRED lines give live-hypothesis predicted outcomes for the selected
   experiments.

   K-CX-3 (discriminating selection): PASS. SELECT lines:
   `SELECT seq=[2] split=2` (W1 round 1), `SELECT seq=[2] split=2` (W2 round 1),
   `SELECT seq=[5] split=2` (W2 round 2). Every selected experiment has
   split >= 2. No non-discriminating selection.

   K-CX-4 (elimination correctness): PASS. ELIM lines:
   W1: id=1 and id=2 eliminated (predicted (0,1), observed (0,0));
   W2 round 1: id=0 eliminated (predicted (0,0), observed (0,1));
   W2 round 2: id=2 eliminated (predicted (0,1), observed (1,1)).
   Exactly the mismatching hypotheses are eliminated. Final:
   W1 CONVERGED id=0 edges=X2Y (true world mask bit0);
   W2 CONVERGED id=1 edges=Y2X (true world mask bit1).

   K-CX-5 (planning from surviving model): PASS. W1 PLAN seq=[2]; W2 PLAN
   seq=[4]. Both execute in the true world reaching (0,0):
   `PLAN-EXEC -> (0,0)` then `PLAN-OK goal=(0,0)` in each world. Same goal,
   different plans, matching the prereg's frozen expected plans.

   K-CX-6 (transfer, one binary): PASS. K-CX-1..K-CX-5 hold for W1 and W2 in
   the single reproduced run (WORLD 1 and WORLD 2 blocks, WORLD-DONE 1 and
   WORLD-DONE 2). Grep audit of the committed source for `wid`: the token
   appears in comments, in the oracle functions `true_mask(wid)` and
   `world_step(wid, ...)`, in the main world-loop variable, in WORLD /
   WORLD-DONE labeling lines, and as an argument passed to `world_step`.
   The learner functions (predict, sim_seq, selection, elimination,
   planning) never take `wid`; they take hypothesis masks, states, and
   actions. No world-conditional learner logic exists.

   K-CX-7 (determinism): PASS, per item 3 above.

## Builder honesty check (non-binding, for the record)

The builder's own report classifies the mechanism as bounded L2, NOT L3,
with authored hypothesis vocabulary, experiment vocabulary, and tie-breaks.
The reproduced evidence is consistent with that classification. No claim to
L3 or representational invention is made or reproduced here.

## Notes for the parent

- The prereg commit `bd883d969` also contains
  `proclang_frontier/PREREG_PROCLANG1.md` from a concurrent worker. That
  file does not affect this reproduction: the causalexp implementation and
  results are absent from the prereg commit and appear only in the result
  commit, which is a strict descendant.
- No em dashes in the source, prereg, raw output, or this report
  (byte-checked).
- No binaries were committed. Build artifacts lived only in /tmp.
- The concurrent `cu7_adversary`, `devint_worker2`, and `u11_adversary`
  files in the prereg..result range belong to other workers and were not
  touched by this reproduction.

## Commits (tnn-native-lab, local only)

This report is committed at
`docs/lab/research-lead/overnight-20260928/causalexp_repro/CAUSALEXP1_REPRO_REPORT.md`,
owned path only. No other paths touched.
