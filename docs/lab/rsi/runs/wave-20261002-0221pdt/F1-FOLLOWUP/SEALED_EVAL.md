# SEALED_EVAL.md - F1-FOLLOWUP wave-20261002-0221pdt

## 1. Provenance

- Prereg: d7164c12b (PREREG_F1FOLLOWUP.md + NAMECHECK.md alone)
- Methodology: 742081f93 (dev/, scripts, METHODOLOGY.md)
- Fixtures + NC: a920ba752 (sealed/, ncharness/)
- This eval: sealed runs + analysis (runs/, analysis/, SEALED_EVAL.md,
  REDTEAM_SELF.md)
- Branch tnn-native-lab, local only. No file outside this lane touched;
  the F1 lane was read-only throughout.

## 2. Sealed run record

- Binary under test: docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn,
  sha256 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847
  (hash-verified by run_sealed.sh before any run; constructor read-only).
- Fixtures: sealed/s3_{train,hidden,truth}_<i>.ep, i = 0..39, frozen
  53xx series (train 5300+2i, hidden/truth 5301+2i), manifest
  sealed/FIXTURE_SHA256.txt verified before runs.
- NC-HARNESS (prereg section 6): PASS. 6/6 regenerated prior Part 2
  fixtures byte-identical to the prior lane's sealed2/; 3/3
  byte-identical reruns; hidden acc 5/30, 0/30, 2/30 on known overfits
  (i = 2,3,5) and 30/30 on known corrects (i = 0,1,4); hidden preds
  byte-identical to the prior lane's runs2/1. The harness measures
  the constructor.
- K-DET: PASS. All 40 seeds x 3 repetitions byte-identical
  (cmp-verified on state, trace, pred for train and hidden).
  runs/DETERMINISM_SHA256.txt recorded.
- Analysis: pure-Zag scorer + f1f_analyze on the frozen manifest;
  analysis/RESULTS.txt, analysis/manifest.txt.

## 3. Frozen bar checks (PREREG_F1FOLLOWUP.md section 6)

Measured: R = 3, T = 2, D = 37, Cmax = 2 (N = 40).

- K-SENS-RATE (R >= 4): FAIL. R = 3/40 = 7.5 percent. Overfit seeds:
  10, 12, 23, all hidden 0/30; the other 37 seeds are 30/30.
- K-SENS-TRIAL (T >= 2): PASS. T = 2: first-trial class ADD_X0_X0 on
  25 seeds, ADD_X1_X1 on 15 seeds. The constructor's first greedy
  trial choice varies with the seed.
- K-SENS-CONV (D >= 3 AND Cmax <= 34): PASS. D = 37, Cmax = 2.
- K-DET: PASS. NC-HARNESS: PASS.

CANDIDATE-BARS: NOT-ALL-PASS.

## 4. What the numbers say

The constructor is qualitatively seed-sensitive but below the frozen
behavioral magnitude. The 3 overfit seeds (10, 12, 23) fail with the
same greedy-compounding mechanism documented in prior Part 2:
seed 10 builds 2x1 then re-adds x1 (3x1 + 2 late x0 adds, 0/30);
seed 12 doubles x0 then doubles the accumulator (4x0 + x1, 0/30);
seed 23 compounds 2x0 -> 3x0 then adds x1 twice more (0/30).
All other seeds converge to the correct law at 30/30.

The measured magnitude X = (overfit rate 3/40 = 7.5 percent;
2 first-trial classes; 37 normalized convergence paths;
concentration 2/40 = 5 percent).

Context: prior Part 2 measured 6/24 = 25 percent on the same family
and geometry. Pooled across both sealed batteries: 9/64 = 14.1
percent. The overfit rate is itself seed-set-dependent; the 25
percent figure must not be reified as the constructor's rate.

## 5. Diagnostics (reported, not bars)

- First TRIGGER episode: ep 1 on 34/40 seeds, ep 2 on 6/40. The
  trigger fires immediately on every seed, so the constructor's
  greedy trial is the variable under test throughout.
- Fixture sanity: 13 to 19 distinct (x0,x1,y) lines per 24-episode
  train fixture across all 40; no degenerate fixtures (diagnostic
  only; all 40 seeds in every denominator).
- CONSTRUCT counts: 32 seeds with 3 events, 2 with 4, 3 with 5,
  3 with 6. The longer runs (5-6 events) still converge to 30/30.
- Post-hoc op/operand-only grouping diagnostic (dev/f1f_diag,
  pure Zag, NOT the frozen metric): D_ops = 10, Cmax_ops = 21.
  The two canonical correct op/operand patterns cover 31/40 seeds
  (21 in the X0-first pattern, 10 in the X1-first pattern); the 3
  overfit seeds each form a singleton group, structurally distinct
  from every correct seed and from each other. See REDTEAM_SELF.md
  Attack 2 for what this implies about the frozen D/Cmax bar.

## 6. Verdict: BUILD-FAIL

Governing bars (frozen in PREREG_F1FOLLOWUP.md, committed alone at
d7164c12b before any methodology existed): K-SENS-RATE trips
(R = 3 < 4). Per the frozen verdict rule, any failing SENS bar
means BUILD-FAIL. The bar is not weakened: 3/40 is below the
10 percent floor set before seeing data.

What stands as evidence: the F1 constructor's greedy trial is
seed-sensitive in its trial choices (T = 2 first-trial classes;
overfit vs correct outcome is seed-dependent; the 3 overfits show
the documented greedy-compounding failure mode), with a measured
behavioral overfit rate of 7.5 percent on this 40-seed sealed
battery, below the frozen 10 percent floor for filing the
SENSITIVE finding. F1's BUILD-FAIL is untouched. No promotion,
no L3 claim.

## 7. Architecture accounting

0 cognition-substrate source lines added; no file outside this lane
touched. New code in this lane is sealed characterization
methodology only. New hardcoded semantic cases 0; new modes 0;
new bridges 0; new routers 0; new task-specific handlers 0.

No em-dashes in this document.
