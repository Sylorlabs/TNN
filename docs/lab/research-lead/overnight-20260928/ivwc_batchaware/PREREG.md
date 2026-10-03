# PREREG.md -- IVWC-BATCHAWARE: batch-aware worth-K via miscalibration tracking

## Wave

Follow-up from IVWC-CONSEQUENCE (BUILD-PASS K1-K10). CONSEQUENCE
established: (1) the consequence-aware hybrid V_HKC (bar =
max(ThyA, K)) beats the cost-blind hybrid V_HA (225 > 210, K4);
(2) the pure worth-K control V_WK (bar = K) beats V_HKC on both
UCB (258 > 225, K10) and D1b (280 > 262, K9); (3) the hybrid's
batch-responsiveness -- tracking mean_sealed(preff) -- is actively
harmful for profit when the batch level and the stakes disagree.
Correction-independence and batch-responsiveness are separable;
profit wants the first without the second.

This wave builds the specified next frontier: a **batch-aware
worth-K** that tracks the batch's *miscalibration* (how far the
learner's bias-adjusted scores deviate from realized consequences
under shift), not the batch's *level*. The miscalibration signal
is correction-independent (from preff and train-fixed quantities
only; never from sealed bias-adjusted scores) and feeds a
K-anchored bar.

Non-ledger task. Lane `ivwc_batchaware/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab` via explicit
pathspec plumbing. Pushing to origin is AUTHORIZED per Micah's
2026-10-03 authorization (fresh GitHub PAT; exclude reproducible
cache/build artifacts).

## Design

**V_BAMK (batch-aware miscalibration worth-K, KEY).**
bar_BAMK(sh) = K + M_pred(sh), with K = EXCOST = 15.

M_pred(sh) is the batch's predicted miscalibration from the
**bucket-mix** signal:

- On train (where consequences are learner-visible), per bucket
  b: M_train[b] = mean over train cases in bucket b of
  (adj_t - eff_t), where adj_t = preff_tr_t - bucb[bkt_t].
  This is the train in-sample miscalibration per bucket (how much
  the UCB-corrected scores deviate from realized train
  consequences). All quantities are learner-visible on train.
- On a sealed batch sh: M_pred(sh) = mean over sealed cases s of
  M_train[bkt_s]. The batch's predicted miscalibration is the
  bucket-weighted train miscalibration. It reads only bkt_s
  (sealed, bias-free, from belief composition) and M_train
  (train-fixed). It never reads a sealed bias-adjusted score.

The hypothesis: the bias correction bucb was learned on train;
on a new batch, if the bucket composition differs, the
batch-level miscalibration differs predictably. The bar stays
anchored at the stakes K and moves only by the predicted
miscalibration -- it does not track the batch's level.

Correction-independence is preserved structurally: the bar reads
only bkt (bias-free), M_train (train-fixed), and K (world
constant). The fenced +40 probes touch d1adj/d2adj only, never
bkt, so they cannot move the bar -- the same structural guarantee
as V_HA/V_HKC/V_WK.

**V_XMG (fenced exact-gap diagnostic, NOT a learner verdict).**
bar_XMG(sh) = K + M(sh), where M(sh) = mean over sealed cases of
(adjucb_s - eff_s) computed fenced AFTER the REFERENCE phase
(which fills eff for all cases). This is the oracle ceiling for
mean-gap tracking: it shows what the best possible batch-level
mean miscalibration signal could achieve. It reads sealed eff,
so it is explicitly NOT correction-independent and NOT a
candidate mechanism; it is a diagnostic that bounds the
"miscalibration" estimand. It uses zero additional
world_execute calls (pure arithmetic on the REFERENCE-filled
consequence buffer). In the source it is named `xmg` (the token
"oracle" appears nowhere, per K1-A8).

Arms (6 + diagnostic + reference): UCB x V_HA (verbatim lineage
baseline), UCB x V_HKC (verbatim lineage baseline; the harmful
batch-responsiveness), UCB x V_WK (verbatim control; pure
worth-K), UCB x V_BAMK (KEY); D1b x V_BAMK, D2b x V_BAMK (fenced
diagnostics, +40 never learner-visible; verify the BAMK bar is
probe-proof); V_XMG (fenced exact-gap diagnostic); fenced
execute-all reference.

## Stakes K

K = 15, preregistered, inherited from CONSEQUENCE/APPLIED. World
parameter (execution cost), not a label.

## Background facts (from committed tables, not probed)

World/belief/composer/stepper/seeds/biases/bars verbatim from
IVWC-HYBRID-VERDICT and IVWC-APPLIED (K3 re-verifies: ThyA =
13/20/6, ThyB = 13/20/13, TFIXED = 12, CVAL = 15, ThyHKC =
15/20/15). bucb = (0,16,27,20). Committed per-case sealed
(adjucb, d1adj, d2adj, eff) from CONSEQUENCE PREREG.md. Committed
sealed (bkt, preff) from the ivwc_hybrid_clean V lines
(commit 88e9108f4):

- sh=0 (@15): bkt = [2,0,1,1,1,3,3,1,0,1,1,3]
- sh=1 (@30): bkt = [3,0,1,1,1,3,1,2,1,0,1,3]
- sh=2 (@45): bkt = [1,0,0,2,1,3,0,0,0,0,0,1]

Train (bkt, adj, eff) from the committed TAUDIT (24 cases;
adj = preff - bucb[bkt]):

- bkt=0 (7 cases): r = adj-eff = 0 each. Sum 0.
- bkt=1 (7 cases): r = -16,-16,-16,-16,-16,-16,17. Sum -79.
- bkt=2 (7 cases): r = -15,-2,-10,-27,-27,6,-9. Sum -84.
- bkt=3 (3 cases): r = 0,-9,-2. Sum -11.

M_train[b] = sum/cnt, integer division (trunc toward zero):
M_train = (0/7, -79/7, -84/7, -11/3) = (0, -11, -12, -3).

M_pred(sh) = sum_s M_train[bkt_s] / 12:

- sh=0: counts (b0:2, b1:6, b2:1, b3:3).
  sum = 2*0 + 6*(-11) + 1*(-12) + 3*(-3) = -87.
  M_pred = -87/12 = -7. bar_BAMK = 15-7 = 8.
- sh=1: counts (b0:2, b1:6, b2:1, b3:3).
  sum = -87. M_pred = -7. bar_BAMK = 8.
- sh=2: counts (b0:7, b1:3, b2:1, b3:1).
  sum = 7*0 + 3*(-11) + 1*(-12) + 1*(-3) = -48.
  M_pred = -48/12 = -4. bar_BAMK = 15-4 = 11.

Exact-gap M(sh) = sum_s (adjucb_s - eff_s)/12 (from committed
tables): sh=0: -67/12 = -5, bar 10; sh=1: -53/12 = -4, bar 11;
sh=2: 63/12 = 5, bar 20.

## Frozen profit predictions (K=15; profit = sum over GO of (eff-15); GO iff score > bar, strict)

UCB x V_BAMK (bar 8/8/11):

- sh=0: GO {0,2,3,4,5,7,9,10} (adj 13,17,34,17,24,17,17,9 > 8).
  eff 0,33,0,33,33,33,33,25.
  profit = -15+18-15+18+18+18+18+10 = 70 (8 GO).
- sh=1: GO {0,2,3,4,5,6,7,8,10} (adj 30,17,34,34,20,34,23,34,9 > 8).
  eff 10,33,50,50,30,0,25,50,25.
  profit = -5+18+35+35+15-15+10+35+10 = 138 (9 GO).
- sh=2: GO {0,4,5,11} (adj 34,34,13,84 > 11).
  eff 0,0,0,100. profit = -15-15-15+85 = 40 (4 GO).
- Total: 70+138+40 = 248 (21 GO).

D1b x V_BAMK (bar 8/8/11):

- sh=0: GO {2,4,7,9,10} (d1adj 17,17,17,17,9 > 8).
  profit = 18+18+18+18+10 = 82 (5 GO).
- sh=1: GO {2,3,4,8,10} (d1adj 17,34,34,34,9 > 8).
  profit = 18+35+35+35+10 = 133 (5 GO).
- sh=2: GO {11} (d1adj 84 > 11). profit = 85 (1 GO).
- Total: 82+133+85 = 300 (11 GO).

D2b x V_BAMK (bar 8/8/11):

- sh=0: GO {0,2,3,7,9} (d2adj 13,17,34,17,17 > 8).
  profit = -15+18-15+18+18 = 24 (5 GO).
- sh=1: GO {2,3,6,7,8} (d2adj 17,34,34,23,34 > 8).
  profit = 18+35-15+10+35 = 83 (5 GO).
- sh=2: GO {0,4,11} (d2adj 34,34,84 > 11).
  profit = -15-15+85 = 55 (3 GO).
- Total: 24+83+55 = 162 (13 GO).

V_XMG fenced diagnostic (bar 10/11/20; arithmetic only):

- sh=0: GO {0,2,3,4,5,7,9} (adj 13,17,34,17,24,17,17 > 10).
  profit = -15+18-15+18+18+18+18 = 60 (7).
- sh=1: GO {0,2,3,4,5,6,7,8} (adj 30,17,34,34,20,34,23,34 > 11).
  profit = -5+18+35+35+15-15+10+35 = 128 (8).
- sh=2: GO {0,4,11} (adj 34,34,84 > 20).
  profit = -15-15+85 = 55 (3).
- Total: 60+128+55 = 243.

Lineage baselines (verbatim, from CONSEQUENCE):

- UCB x V_HA: (75, 95, 40) = 210 (GO 6,6,4 = 16).
- UCB x V_HKC: (75, 95, 55) = 225 (GO 6,6,3 = 15).
- UCB x V_WK: (75, 128, 55) = 258 (GO 6,8,3 = 17).
- execute-all: (43, 113, -80) = 76.

WC-FINAL: 24 train + 93 GO (16+15+17+21+11+13; XMG uses zero
world calls) + 36 reference = 153.

## Frozen kill bars

- **K1 (diet / commit order / no-oracle / correction-independence):
  PASS required.** A1: phase order train COMMIT < train PREFF <
  train CONSEQ < train LEARN < train BAR < sealed COMMIT < sealed
  BARS < sealed VERDICT (GO) < CONSEQUENCE (world_execute on GO)
  < FENCED-DIAG < REFERENCE < FENCED-XMG, by source line order
  (strict increase is the frozen property). A2: zero
  `world_buf`/`world_off` tokens in learner fns (lc_blocked,
  lc_leg, learner_compose, gather_cells). A3: zero
  `expected|answer|key|target` (case-insensitive). A4: zero
  `correct|reference_plan|gold`. A5: `world_execute(` exactly 4
  occurrences (1 def + 3 call sites: train CONSEQ, the shared
  `conseq_arm` helper, REFERENCE). The XMG diagnostic uses zero
  world_execute calls (pure arithmetic on the REFERENCE-filled
  buffer). A6: WC-FINAL = 153. A7: zero `learner_`/`belief_`
  calls after the CONSEQUENCE marker. A8: the token "oracle"
  (case-insensitive) appears zero times. A9 (the no-oracle bar):
  the token `Tpred` appears zero times. A10
  (correction-independence): the V_BAMK bar is computed without
  reading any sealed bias-adjusted score -- bar_BAMK(sh) = K +
  M_pred(sh), with M_pred(sh) from M_train (train-fixed) and
  bkt_s (sealed, bias-free); the fenced +40 probes touch
  d1adj/d2adj only, never bkt, so they cannot move the bar. The
  XMG diagnostic is fenced (not a learner bar) and reads sealed
  eff only after REFERENCE; it does not affect any verdict.
- **K2 (determinism): PASS required.** 3/3 runs byte-identical
  stdout.
- **K3 (verbatim machinery + new quantities): PASS required.**
  BARS lines: ThyA = 13/20/6, ThyB = 13/20/13 @15/30/45; TFIXED
  = 12; CVAL = 15; ThyHKC = 15/20/15. New: M_train =
  (0,-11,-12,-3); bar_BAMK = (8,8,11) (in-program exact checks).
- **K4 (PRIMARY): PASS required.** UCB x V_BAMK total = 248 >
  UCB x V_HKC total = 225. Miscalibration-tracking beats the
  harmful batch-responsiveness: tracking the predicted
  miscalibration (not the batch level) improves profit over the
  level-tracking hybrid.
- **K5: PASS required.** Execute-all per-batch profit =
  (43, 113, -80).
- **K6: PASS required.** UCB x V_BAMK @30 = 138 > UCB x V_WK @30
  = 128. Where the over-correction is real and marginal, the
  signal helps: bar 8 (vs 15) takes s=10 (adj=9, eff=25, +10).
- **K7: PASS required.** UCB x V_BAMK @45 = 40 < UCB x V_WK @45 =
  55. Where the shift flips the sign, the signal hurts: it
  predicts over-correction (M_pred=-4) when the truth is
  under-correction (M=+5); bar 11 (vs 15) takes s=5 (adj=13,
  eff=0, -15).
- **K8: PASS required.** WC-FINAL = 153 (in-program).
- **K9 (preregistered divergence): PASS required.** UCB x V_BAMK
  total = 248 < UCB x V_WK total = 258. Miscalibration-tracking
  does NOT beat pure worth-K. The bucket-mix signal improves on
  the harmful level-tracking (K4) but the fixed stakes bar wins
  overall: the @15 loss (70 < 75, takes s=0's -15) and the @45
  loss (40 < 55, takes s=5's -15) outweigh the @30 gain
  (138 > 128).
- **K10 (preregistered divergence): PASS required.** V_XMG total
  = 243 < UCB x V_WK total = 258. Even the EXACT batch mean-gap
  signal fails to beat the fixed stakes bar. The mean
  miscalibration is not decision-relevant: at @15 the exact
  signal (bar 10) takes s=0's -15 while the fixed bar (15)
  skips it; the miscalibrated cases that drive the mean are far
  from the margin. Tracking "how far scores deviate from
  consequences" at the batch mean answers the wrong question
  for profit.

**BUILD-PASS requires K1..K10.**

## Preregistered answers to the task's key questions

1. **Does miscalibration-tracking beat pure worth-K?**
   Predicted NO (K9): 248 < 258. The bucket-mix signal is a
   genuine improvement over level-tracking (K4) but loses to the
   fixed stakes bar. The losses (@15: takes s=0; @45: takes s=5)
   come from the signal moving the bar where no move (or the
   opposite move) was needed.
2. **Is it better than the harmful batch-responsiveness?**
   Predicted YES (K4): 248 > 225. Tracking predicted
   miscalibration dominates tracking the batch level. The
   level-tracking hybrid moves the bar with the batch whether or
   not the stakes agree; the miscalibration bar moves only by the
   predicted score-consequence gap, anchored at K.
3. **What's the right miscalibration signal?** Predicted: NOT the
   batch mean gap (K10: even the exact signal gets 243 < 258).
   The mean is driven by far-from-margin cases; the
   decision-relevant quantity is the miscalibration AT THE
   MARGIN (or per-bucket, where the bias lives). The bucket-mix
   signal inherits train's pessimism (always predicts
   over-correction) and cannot adapt to sign flips (@45). Next
   frontier candidates: per-bucket worth-K bars with
   learner-computable per-bucket signals; marginal/local
   miscalibration; learner-owned K; the K-sensitivity curve.
4. **Can we track miscalibration without reintroducing harmful
   batch-responsiveness?** Predicted YES structurally (K1-A10):
   the BAMK bar never reads a sealed bias-adjusted score and is
   probe-proof, while being genuinely batch-aware (it varies
   8/8/11 across batches from the bucket mix, not from the
   level).

## Determinism and honesty rules

- Integer arithmetic only. No researcher-set constants in any
  learner path (M_train is computed from train data; the
  bucket-mix weighting is structural; K=15 lives in the
  world/consequence phase and as the bar anchor; the D1b/D2b +40
  lives only in the fenced diagnostic).
- No post-prereg probe of any kind. All predictions above are
  arithmetic on the committed tables.
- The tokens `Tpred`, `oracle`, `expected`, `answer`, `key`,
  `target`, `correct`, `reference_plan`, `gold` do not appear in
  the implementation source (K1 A3/A4/A8/A9).
- If any arm differs from prediction in either direction, report
  the exact mechanism. No bar moves after seeing results.
