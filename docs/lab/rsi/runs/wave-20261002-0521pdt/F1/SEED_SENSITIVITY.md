# SEED_SENSITIVITY.md - F1 greedy-trial seed-sensitivity constructor finding

Lane F1, wave wave-20261002-0521pdt. The constructor finding filed
per the RT-EXEC recommendation: greedy-trial seed-sensitivity as a
SEPARATE CONSTRUCTOR FINDING, not an F1 defect.

## 1. Provenance

- Prereg: 3ced819d8 (PREREG_SEEDSENS.md + NAMECHECK.md alone)
- Methodology: ad82a9a4b (dev/, scripts, METHODOLOGY.md)
- Fixtures: 71954c6bc (sealed5/, 55xx series, FIXTURE_SHA256.txt
  120/120 verified before any sealed run)
- This eval: sealed runs + analysis (runs/, analysis/,
  SEED_SENSITIVITY.md, REDTEAM_SELF.md)
- Branch tnn-native-lab, local only. No file outside this lane
  touched except the append-only T-A erratum in the 2321pdt F1
  SEALED_EVAL.md (authorized by the wave task; original text
  untouched).

## 2. Sealed run record

- Binary under test: docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn,
  sha256 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847
  (hash-verified by run_sealed.sh before any run; constructor read-only).
- Fixtures: sealed5/s5_{train,hidden,truth}_<i>.ep, i = 0..39, frozen
  55xx series (train 5500+2i, hidden/truth 5501+2i), manifest
  sealed5/FIXTURE_SHA256.txt verified before runs.
- NC-HARNESS (prereg section 6): PASS. 6/6 regenerated prior Part 2
  fixtures byte-identical to the 2321pdt lane's sealed2/; 3/3
  byte-identical reruns; hidden acc 5/30, 0/30, 2/30 on known
  overfits (i = 2,3,5) and 30/30 on known corrects (i = 0,1,4);
  hidden preds byte-identical to the prior lane's runs2/1. The
  harness measures the constructor.
- K-DET: PASS. All 40 seeds x 3 repetitions byte-identical
  (cmp-verified on state, trace, pred for train and hidden).
  runs/DETERMINISM_SHA256.txt recorded. Zero run-to-run noise: 100
  percent of the measured variance is seed-driven, not stochastic.
- Analysis: pure-Zag scorer + f1s_analyze on the frozen manifest;
  analysis/RESULTS.txt, analysis/manifest.txt.

## 3. Frozen bar checks (PREREG_SEEDSENS.md section 6)

Measured: R = 13, T = 2, D_ops = 9, Cmax_ops = 15 (N = 40).

- K-SS-TRIAL (T >= 2): PASS. T = 2: first-trial class ADD_X0_X0 on
  28 seeds, ADD_X1_X1 on 12 seeds. The constructor's first greedy
  trial choice varies with the seed, on all three sealed batteries.
- K-SS-OVERFIT (R >= 1 plus white-box check): PASS. R = 13/40 =
  32.5 percent, and the white-box check is satisfied: every one of
  the 13 overfit seeds shows the documented greedy-compounding
  failure mode in its raw trace (section 4).
- K-SS-CONV (D_ops >= 2 AND Cmax_ops <= 32): PASS. D_ops = 9
  distinct structural convergence paths; the largest single path
  (canonical x0-first correct) covers 15/40 = 37.5 percent.
- K-DET: PASS. NC-HARNESS: PASS.

CANDIDATE-BARS: ALL-PASS.

## 4. White-box evidence: the greedy-compounding failure mode

The 13 overfit seeds (0, 5, 10, 12, 17, 18, 23, 25, 26, 29, 31, 34,
35; hidden 0/30 on ten, 1/30 on two, 3/30 on one) fall into 4
structural groups, all overfit-only, each showing the same
mechanism: every individual trial strictly reduces the
seed-driven buffer error, yet compounds an incorrect partial law.

- seqg3 (7 seeds), e.g. seed 5:
  ADD(0,8,8) err 14->4; ADD(0,0,8) err 4->1 [2x0 then 3x0];
  then ADD(0,0,9) err 8->7; ADD(0,0,9) err 7->6 [x1 added twice
  onto the 3x0 base]. Final law 3x0+2x1, hidden 0/30.
- seqg0 (2 seeds), e.g. seed 0: the x1-first mirror:
  ADD(0,9,9); ADD(0,0,9) [2x1 then 3x1]; then ADD(0,0,8) twice
  [x0 added twice onto the 3x1 base]. Final law 3x1+2x0, 0/30.
- seqg5 (2 seeds), e.g. seed 23: ADD(0,9,9); ADD(0,0,0) [accumulator
  double]; ADD(0,0,8). Doubling the accumulator instead of adding
  the missing feature, 0/30 and 1/30.
- seqg6 (2 seeds), e.g. seed 26: ADD(0,8,8); ADD(0,0,8) [3x0];
  ADD(0,0,9) once [3x0+x1]. One missing x1: hidden 1/30 and 3/30,
  partially right by accident.

The compounding also occurs within a single KB burst (seeds 18,
23, 26, 29 build their full overfit in 3 events), so it is not a
multi-burst artifact. After the wrong law is built, later bursts
STALL: the trigger keeps firing (8+ triggers on seed 0) but no
depth-1 trial improves the buffer error, so the wrong structure
is never unbuilt.

Contrast the correct seeds (27/40, 30/30): the canonical patterns
[ADD(0,8,8); ADD(0,0,9); ADD(0,0,9)] (seqg1, 15 seeds) and the
x1-first mirror (seqg4, 8 seeds) plus longer correct paths (seqg2,
seqg7, seqg8). Structural grouping separates outcomes perfectly:
every overfit seed is in an overfit-only group, every correct seed
in a correct-only group. The outcome classes are structural, not
noise.

## 5. Constructor diagnosis (findings, not a repair)

What the evidence says about the greedy-trial constructor's
design, stated as a diagnosis. Nothing here is patched; the
no-patch-treadmill rule holds and F1's BUILD-PASS stands on its
own bars.

1. Depth-1 greedy argmin over a seed-driven, state-dependent
   buffer. Each trial is evaluated against the current
   experience buffer (last up-to-8 episodes) under the current
   partial law. A trial that strictly reduces buffer error is
   kept. The seed controls the buffer's x-values; the buffer
   contents decide which trial wins the argmin. This is why the
   first-trial class is seed-dependent (T = 2 on all three
   batteries): the data, not a researcher rank, drives the
   choice.
2. No lookahead, no coverage memory. The constructor does not
   remember which features a partial law already covers, and
   cannot evaluate a trial's effect on the final law. Adding
   the same feature twice (2xi -> 3xi) reduces buffer error on
   the seeded buffer, so it is kept; the damage (an
   overweightable base) is invisible to depth-1 evaluation.
3. The wrong law is then a trap. Later trials can only add on
   top of the wrong base; each is locally error-reducing
   (err 8->7, 7->6 on seed 5) yet globally compounding. No
   unbuild/revision operation exists in the constructor: STALL
   lines show bursts that find no improving trial, and the
   trigger's repeated repair attempts change nothing.
4. The trigger is not implicated. It fires at episode 1 on all
   sampled seeds, keeps firing on the overfit seeds, and the
   constructor is the variable throughout. This is a
   constructor-side property, exactly as filed.

Design implications for any successor constructor: a depth-1
greedy trial without lookahead or coverage tracking will show
this seed sensitivity on any family where two features can be
compounded asymmetrically; evaluating trials against a held-out
buffer (not the buffer that motivated the partial law), or
tracking feature coverage, or adding a trial whose effect is
evaluated over more than one step, are the structural directions
the evidence points to. This lane files the diagnosis; it does
not build the successor.

## 6. The rate, pooled and not reified

This battery: 13/40 = 32.5 percent. Prior batteries on the same
family and geometry: 6/24 = 25.0 percent, 3/40 = 7.5 percent.
Pooled sealed evidence: 22/104 = 21.2 percent. The rate is
seed-set-dependent (7.5 to 32.5 percent across three sealed
batteries); no single figure is reified as the constructor's
rate. The filed finding is the qualitative constructor property
(seed-dependent trial choices; seed-dependent compounding
overfits via the documented mechanism), whose magnitude X =
(13/40, T = 2, D_ops = 9, Cmax_ops = 15) is reported on this
battery.

## 7. Verdict: FINDING CONFIRMED

Governing bars (frozen in PREREG_SEEDSENS.md, committed alone at
3ced819d8 before any methodology existed): K-SS-TRIAL, K-SS-OVERFIT
(including the white-box compounding check), and K-SS-CONV all
pass, with K-DET and NC-HARNESS passing. No bar was weakened.

What is filed: greedy-trial seed-sensitivity is a constructor
property of the F1 constructor. The constructor's first greedy
trial choice varies with the train seed (T = 2, stable across all
three sealed batteries); on some seeds the greedy compounding
failure mode builds an incorrect law that hidden evaluation
exposes (13/40 on this battery; pooled 22/104); structural
convergence paths are diverse (D_ops = 9) with the largest
single path at 37.5 percent concentration; and the mechanism is
visible white-box in every overfit trace. This is a knowledge /
architecture diagnosis of the constructor, not a promotion, not
an L3 claim, and not a change to any prior verdict: F1's
0221pdt BUILD-PASS stands, and the 0221pdt F1-FOLLOWUP BUILD-FAIL
on the 10-percent behavioral claim stands unaltered.

## 8. Architecture accounting

0 cognition-substrate source lines added; no file outside this lane
touched except the append-only T-A erratum in the 2321pdt F1
record (original text untouched). New code in this lane is sealed
characterization methodology only. New hardcoded semantic cases 0;
new modes 0; new bridges 0; new routers 0; new task-specific
handlers 0.

No em-dashes in this document.
