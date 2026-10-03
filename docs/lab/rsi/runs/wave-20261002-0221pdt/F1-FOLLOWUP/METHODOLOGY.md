# METHODOLOGY.md - F1-FOLLOWUP wave-20261002-0221pdt

Committed after the prereg freeze (d7164c12b) and before any sealed
fixture generation or sealed run, per PREREG_F1FOLLOWUP.md ordering.

## Components (all pure Zag, pinned znc)

- dev/f1_wgen.zag + dev/f1_wgen: fixture generator, source copied
  read-only from the F1 lane's dev/ (wave-20261001-2321pdt/F1/dev/).
  Compiled by the pinned znc in this lane. Byte-identical
  reproduction of prior Part 2 fixtures verified: regenerating
  s2_train/hidden/truth for i = 0,1,2 (train seeds 5100,5102,5104)
  cmp-matches the prior lane's sealed2/ fixtures exactly.
- dev/f1_score.zag + dev/f1_score: scorer (`acc`, `sig`), source
  copied read-only from the F1 lane's dev/. Verified: reproduces the
  prior Part 2 hidden accuracies exactly on the prior lane's
  runs2/1 preds (i = 2: 5/30; 3: 0/30; 5: 2/30; 13: 0/30; 17: 1/30;
  18: 0/30; 0,1: 30/30).
- dev/f1f_analyze.zag + dev/f1f_analyze: seed-sensitivity analyzer
  implementing exactly the frozen normalization of PREREG_F1FOLLOWUP
  section 5 (operand classes 8->X0, 9->X1, 0->R0, else O; episode,
  burst index, node id dropped; op, operand classes, err transitions
  kept). Computes R (overfit count, acc < 100%), T (distinct
  first-trial classes), D (distinct normalized sequences), Cmax
  (largest sequence group), and the three frozen bar checks.
  Methodology dry run on prior Part 2 data (24 seeds + 16 duplicate
  traces, /tmp only, never committed): parsing verified by hand
  (ncons 6/3/4 on seeds 0/2/13 match grep counts; first-trial
  classes ADD_X1_X1 / ADD_X0_X0 match the raw traces; duplicate
  traces receive identical sequence group ids; R = 6 on the 24
  unique seeds). A cell-allocation bug (byte count vs cell count)
  found in the dry run was fixed before any sealed use; the fix is
  in the committed source.

## Scripts (pure shell)

- gen.sh: generates the 40 sealed fixtures (53xx series) and writes
  sealed/FIXTURE_SHA256.txt.
- nc_harness.sh: NC-HARNESS calibration (prereg section 6).
- run_sealed.sh: 40 seeds x 3 repetitions with the frozen F1 binary
  (sha256-checked), K-DET cmp verification, DETERMINISM_SHA256.txt.
- analyze.sh: scores hidden preds, builds the analyzer manifest,
  runs f1f_analyze, writes analysis/RESULTS.txt.

## Architecture accounting

0 cognition-substrate source lines added; no file outside this lane
touched; the F1 lane is read-only. New code is sealed characterization
methodology only. New hardcoded semantic cases 0; new modes 0; new
bridges 0; new routers 0; new task-specific handlers 0.

No em-dashes in this document.
