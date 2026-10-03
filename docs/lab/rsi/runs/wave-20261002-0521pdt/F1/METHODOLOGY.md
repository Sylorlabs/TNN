# METHODOLOGY.md - F1 seed-sensitivity finding wave-20261002-0521pdt

Committed after the prereg freeze (3ced819d8) and before any sealed
fixture generation or sealed run, per PREREG_SEEDSENS.md ordering.

## Components (all pure Zag, pinned znc)

- dev/f1_wgen.zag + dev/f1_wgen: fixture generator, source copied
  read-only from the 0221pdt F1-FOLLOWUP lane's dev/ (identical to
  the F1 lane's wgen). Compiled by the pinned znc in this lane.
  Dry-run verification (in /tmp, never committed): regenerated
  s2_train/hidden/truth for i = 0,1,2 (train seeds 5100, 5102, 5104)
  cmp-match the 2321pdt F1-FOLLOWUP lane's sealed2/ fixtures
  exactly. (NC-HARNESS extends this to i = 0..5 before sealed runs.)
- dev/f1_score.zag + dev/f1_score: scorer, source copied read-only
  from the 0221pdt F1-FOLLOWUP lane's dev/. Verified: reproduces the
  known Part 2 hidden accuracies on the prior lane's runs2/1 preds
  (i = 2: 5/30).
- dev/f1s_analyze.zag + dev/f1s_analyze: seed-sensitivity analyzer
  implementing exactly the frozen normalization of PREREG_SEEDSENS
  section 5 (op/operand-only grouping: normalized event
  `OP C(p1) C(p2) C(p3)`; episode, burst index, node id, AND err
  transitions dropped; op and operand classes kept). This is the
  owned calibration fix from the 0221pdt red-team Attack 2: the
  frozen D/Cmax metric no longer fragments on error-magnitude
  noise. Bar checks in the analyzer are the frozen ones:
  K-SS-TRIAL T>=2, K-SS-OVERFIT R>=1, K-SS-CONV D_ops>=2 AND
  Cmax_ops<=32. The white-box compounding check of K-SS-OVERFIT is
  done at evaluation time against raw traces (documented in
  SEED_SENSITIVITY.md), not inside the analyzer.
- Methodology dry run on prior Part 2 data (24 seeds + 16 duplicate
  traces, /tmp only, never committed): parsing verified by hand
  (ncons 3 on seed 2 matches the grep count; first-trial class
  ADD_X0_X0 matches the raw trace; duplicate traces receive
  identical sequence group ids; seed 13 and seed 18 share one
  op/operand group; R = 10 = 6 unique + 4 duplicated overfits;
  T = 2; D_ops = 10; Cmax_ops = 13). No analyzer bugs found.

## Scripts (pure shell)

- gen.sh: generates the 40 sealed fixtures (55xx series) and writes
  sealed5/FIXTURE_SHA256.txt.
- nc_harness.sh: NC-HARNESS calibration (prereg section 6). Runs in
  /tmp only: regenerates Part 2 i = 0..5 (seeds 5100..5110),
  cmp-verifies byte-identical against the 2321pdt F1-FOLLOWUP
  lane's sealed2/ fixtures, runs all 6 through the frozen binary
  (3/3 byte-identical), requires the known hidden accuracies
  (2: 5/30, 3: 0/30, 5: 2/30, 0/1/4: 30/30), and requires hidden
  preds byte-identical to that lane's runs2/1 preds.
- run_sealed.sh: 40 seeds x 3 repetitions with the frozen F1 binary
  (sha256-checked against 6f2b155b...be8882847; constructor
  read-only), K-DET cmp verification, DETERMINISM_SHA256.txt.
- analyze.sh: scores hidden preds, builds the analyzer manifest,
  runs f1s_analyze, writes analysis/RESULTS.txt.

## Architecture accounting

0 cognition-substrate source lines added; no file outside this lane
touched; the F1 lanes are read-only. New code is sealed
characterization methodology only. New hardcoded semantic cases 0;
new modes 0; new bridges 0; new routers 0; new task-specific
handlers 0.

No em-dashes in this document.
