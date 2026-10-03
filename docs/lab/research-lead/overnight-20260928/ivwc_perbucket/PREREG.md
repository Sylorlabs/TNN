# PREREG.md -- IVWC-PERBUCKET: per-bucket worth-K bars

## Wave

Follow-up from IVWC-BATCHAWARE (BUILD-PASS K1-K10). BATCHAWARE
established: (1) tracking predicted miscalibration (V_BAMK, 248)
beats the harmful level-tracking hybrid (V_HKC, 225, K4) but
loses to the fixed stakes bar (V_WK, 258, K9); (2) even the
EXACT batch mean gap fails (V_XMG, 243, K10): the mean is driven
by far-from-margin cases, and profit asks which side of the bar
the marginal cases are on; (3) the bucket-mix signal inherits
train's pessimism and cannot adapt to sign flips (@45).
BATCHAWARE's named next frontier: "per-bucket worth-K bars (a
per-bucket exact-gap signal scores 283 > 258 on committed
tables -- the information is real but lives below batch level)".

This wave builds the specified next frontier: **per-bucket
worth-K bars**. Instead of one bar for the whole batch, each
bucket gets its own bar, worth-K calibrated for that bucket's
characteristics, from learner-visible train quantities only.
Two learner-computable designs are tested against the fixed-K
control and against the fenced per-bucket exact bound.

Non-ledger task. Lane `ivwc_perbucket/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab` via explicit
pathspec plumbing. Pushing to origin is AUTHORIZED per Micah's
2026-10-03 authorization (fresh GitHub PAT; exclude reproducible
cache/build artifacts).

## Design

**V_PBK (per-bucket worth-K, KEY-1).** bar_b = K + mcalib[b],
K = EXCOST = 15. mcalib[b] is the train in-sample miscalibration
per bucket (mean over train cases in bucket b of (adj_t -
eff_t), all learner-visible). The miscalibration-corrected
score is adj - mcalib[b]; GO iff adj_s > K + mcalib[bkt_s].
This is the direct below-batch-level analog of V_BAMK: instead
of averaging the bucket miscalibrations into one batch bar, each
bucket keeps its own. Reads only bkt_s (sealed, bias-free),
mcalib (train-fixed), K (world constant). Never reads a sealed
bias-adjusted score; probe-proof by structure (K1-A10).

**V_PBOPT (train-optimal per-bucket bars, KEY-2).** Per bucket
b, bar*_b = the train-profit-optimal bar: maximizes sum over
train cases in bucket b with adj_t > bar of (eff_t - K), using
only train consequences (learner-visible). Tie-break: among
optimal bars, the one closest to K (ties: the larger bar). This
is the empirical, nonparametric version of "worth-K calibrated
for that bucket's characteristics": the bar that would have
been optimal on train for that bucket, with no researcher
constants and no sealed data. Probe-proof by structure
(K1-A10). Candidate bars are integers in
[min_adj_b - 1, max(max_adj_b, K)]; the K-closest optimal bar
always lies in this range (argued in the derivation below).

**V_PBX (fenced per-bucket exact diagnostic, NOT a learner
verdict).** bar_b(sh) = K + G(sh,b), where G(sh,b) is the exact
sealed per-bucket gap: mean over sealed cases in bucket b of
(adjucb_s - eff_s), computed fenced AFTER the REFERENCE phase
(which fills eff for all cases). This bounds the per-bucket
estimand: the best any per-bucket miscalibration signal could
achieve. It reads sealed eff, so it is explicitly NOT
probe-proof and NOT a candidate mechanism; it is a diagnostic.
Zero world_execute calls (pure arithmetic on the
REFERENCE-filled buffer). In the source it is named `pbx` (the
token "oracle" appears nowhere, per K1-A8).

Arms (3 + diagnostic + reference): UCB x V_WK (verbatim lineage
control; pure worth-K), UCB x V_PBK (KEY-1), UCB x V_PBOPT
(KEY-2); V_PBX (fenced per-bucket exact diagnostic); fenced
execute-all reference. The V_HA/V_HKC verdict arms are not
re-run (their bars are still computed and printed for the K3
verbatim-machinery check); the D1b/D2b +40 probe arms are not
re-run (correction-independence for the per-bucket bars holds
by the same structure as V_BAMK -- bkt-driven bars, and the
probes touch adjusted scores only, never bkt -- and is audited
as K1-A10).

## Stakes K

K = 15, preregistered, inherited from the IVWC lineage. World
parameter (execution cost), not a label.

## Background facts (from committed tables, not probed)

World/belief/composer/stepper/seeds/biases/bars verbatim from
the IVWC lineage (K3 re-verifies: ThyA = 13/20/6, ThyB =
13/20/13, TFIXED = 12, CVAL = 15, ThyHKC = 15/20/15).
bucb = (0,16,27,20). Committed sealed (bkt, adjucb, eff) from
CONSEQUENCE PREREG.md (12-tuple eff for sh=2 read from the
per-case listing):

- sh=0 (@15): bkt = [2,0,1,1,1,3,3,1,0,1,1,3]
  (adj,eff): s0:(13,0) s1:(0,0) s2:(17,33) s3:(34,0) s4:(17,33)
  s5:(24,33) s6:(6,20) s7:(17,33) s8:(0,0) s9:(17,33)
  s10:(9,25) s11:(2,13)
- sh=1 (@30): bkt = [3,0,1,1,1,3,1,2,1,0,1,3]
  (adj,eff): s0:(30,10) s1:(0,0) s2:(17,33) s3:(34,50)
  s4:(34,50) s5:(20,30) s6:(34,0) s7:(23,25) s8:(34,50)
  s9:(0,0) s10:(9,25) s11:(5,20)
- sh=2 (@45): bkt = [1,0,0,2,1,3,0,0,0,0,0,1]
  (adj,eff): s0:(34,0) s1:(0,0) s2:(0,0) s3:(-2,0) s4:(34,0)
  s5:(13,0) s6:(0,0) s7:(0,0) s8:(0,0) s9:(0,0) s10:(0,0)
  s11:(84,100)

Train (adj, eff) by bucket from the committed train TAUDIT
(`ivwc_batchaware/runs/ivwc_batchaware-run1.txt`, 24/24 lines):

- bkt=0 (7 cases): (0,0) x7.
- bkt=1 (7 cases): (34,50),(17,33),(84,100),(34,50),(34,50),
  (34,50),(17,0).
- bkt=2 (7 cases): (-9,6),(23,25),(-10,0),(6,33),(15,42),
  (6,0),(0,9).
- bkt=3 (3 cases): (5,5),(7,16),(9,11).

mcalib[b] = mean(adj - eff) on train (integer division, trunc
toward zero): b0: 0/7 = 0; b1: -79/7 = -11; b2: -84/7 = -12;
b3: -11/3 = -3. So mcalib = (0,-11,-12,-3) and the V_PBK bars
are K + mcalib = **(15,4,3,12)**.

V_PBOPT bars: train profit P_b(bar) = sum over train cases in
bucket b with adj > bar of (eff - 15):

- b0: bar >= 0: 0 (no GO); bar <= -1: 7x(0-15) = -105. Max 0
  for bar >= 0; candidates [-1,15]; K-closest optimal: **15**.
- b1: bar >= 84: 0; 34 <= bar <= 83: {84}: 85;
  17 <= bar <= 33: {84,34x4}: 85+4x35 = 225; bar <= 16: all:
  225+18-15 = 228. Max 228 for bar <= 16; candidates [16,84];
  K-closest optimal: **16**.
- b2: bar >= 23: 0; 15 <= bar <= 22: {23}: 10;
  6 <= bar <= 14: {23,15}: 37; 0 <= bar <= 5: {23,15,6,6}:
  40; -9 <= bar <= -1: 34; bar = -10: 25; bar <= -11: 10.
  Max 40 for 0 <= bar <= 5; candidates [-11,23]; K-closest
  optimal: **5**.
- b3: bar >= 9: 0; 7 <= bar <= 8: {9}: -4; 5 <= bar <= 6:
  {9,7}: -3; bar <= 4: {9,7,5}: -13. Max 0 for bar >= 9;
  candidates [4,15]; K-closest optimal: **15**.

So bar* = **(15,16,5,15)**. (On the candidate-range claim: the
argmax set of a stepwise profit is a union of intervals with
breakpoints at adj values, plus possibly the rays (-inf,
min_adj-1] ("take all") and [max_adj, +inf) ("take none"); the
K-closest point of each piece lies in [min_adj-1,
max(max_adj, K)]: the left ray contributes min_adj-1, the right
ray contributes K if K >= max_adj else max_adj, interior pieces
contribute adj-valued endpoints. Hence the restricted search
finds exactly the defined bar*.)

Exact sealed per-bucket gaps G(sh,b) = mean(adj - eff) over
sealed cases in bucket b (integer division, trunc toward zero):

- sh=0: b0: {s1,s8} gaps (0,0) -> 0, bar 15. b1:
  {s2,s3,s4,s7,s9,s10} gaps (-16,34,-16,-16,-16,-16) = -46 ->
  -46/6 = -7, bar 8. b2: {s0} gap 13 -> bar 28. b3:
  {s5,s6,s11} gaps (-9,-14,-11) = -34 -> -34/3 = -11, bar 4.
  PBX bars sh=0: **(15,8,28,4)**.
- sh=1: b0: {s1,s9} gaps (0,0) -> 0, bar 15. b1:
  {s2,s3,s4,s6,s8,s10} gaps (-16,-16,-16,34,-16,-16) = -46 ->
  -7, bar 8. b2: {s7} gap -2 -> bar 13. b3: {s0,s5,s11}
  gaps (20,-10,-15) = -5 -> -5/3 = -1, bar 14.
  PBX bars sh=1: **(15,8,13,14)**.
- sh=2: b0: {s1,s2,s6,s7,s8,s9,s10} gaps all 0 -> 0, bar 15.
  b1: {s0,s4,s11} gaps (34,34,-16) = 52 -> 52/3 = 17,
  bar 32. b2: {s3} gap -2 -> bar 13. b3: {s5} gap 13 ->
  bar 28. PBX bars sh=2: **(15,32,13,28)**.

## Frozen profit predictions (K=15; profit = sum over GO of (eff-15); GO iff score > bar, strict)

UCB x V_WK (bar 15; verbatim lineage control):

- sh=0: GO {2,3,4,5,7,9} (6). profit 75.
- sh=1: GO {0,2,3,4,5,6,7,8} (8). profit 128.
- sh=2: GO {0,4,11} (3). profit 55.
- Total: **258** (17 GO).

UCB x V_PBK (bars (15,4,3,12); KEY-1):

- sh=0: s0 b2 13>3 GO eff0 -15; s1 b0 0 no; s2 b1 17>4 GO
  eff33 +18; s3 b1 34>4 GO eff0 -15; s4 b1 17>4 GO eff33 +18;
  s5 b3 24>12 GO eff33 +18; s6 b3 6 no; s7 b1 17>4 GO eff33
  +18; s8 b0 0 no; s9 b1 17>4 GO eff33 +18; s10 b1 9>4 GO
  eff25 +10; s11 b3 2 no.
  GO {0,2,3,4,5,7,9,10} (8).
  profit = -15+18-15+18+18+18+18+10 = **70**.
- sh=1: s0 b3 30>12 GO eff10 -5; s1 b0 0 no; s2 b1 17>4 GO
  eff33 +18; s3 b1 34>4 GO eff50 +35; s4 b1 34>4 GO eff50
  +35; s5 b3 20>12 GO eff30 +15; s6 b1 34>4 GO eff0 -15;
  s7 b2 23>3 GO eff25 +10; s8 b1 34>4 GO eff50 +35; s9 b0 0
  no; s10 b1 9>4 GO eff25 +10; s11 b3 5 no.
  GO {0,2,3,4,5,6,7,8,10} (9).
  profit = -5+18+35+35+15-15+10+35+10 = **138**.
- sh=2: s0 b1 34>4 GO eff0 -15; s1 b0 0 no; s2 b0 0 no;
  s3 b2 -2 no; s4 b1 34>4 GO eff0 -15; s5 b3 13>12 GO eff0
  -15; s6..s10 b0 0 no; s11 b1 84>4 GO eff100 +85.
  GO {0,4,5,11} (4).
  profit = -15-15-15+85 = **40**.
- Total: **248** (21 GO).

UCB x V_PBOPT (bars (15,16,5,15); KEY-2):

- sh=0: s0 b2 13>5 GO eff0 -15; s1 b0 0 no; s2 b1 17>16 GO
  eff33 +18; s3 b1 34>16 GO eff0 -15; s4 b1 17>16 GO eff33
  +18; s5 b3 24>15 GO eff33 +18; s6 b3 6 no; s7 b1 17>16 GO
  eff33 +18; s8 b0 0 no; s9 b1 17>16 GO eff33 +18; s10 b1 9
  no; s11 b3 2 no.
  GO {0,2,3,4,5,7,9} (7).
  profit = -15+18-15+18+18+18+18 = **60**.
- sh=1: s0 b3 30>15 GO eff10 -5; s1 b0 0 no; s2 b1 17>16 GO
  eff33 +18; s3 b1 34>16 GO eff50 +35; s4 b1 34>16 GO eff50
  +35; s5 b3 20>15 GO eff30 +15; s6 b1 34>16 GO eff0 -15;
  s7 b2 23>5 GO eff25 +10; s8 b1 34>16 GO eff50 +35; s9 b0 0
  no; s10 b1 9 no; s11 b3 5 no.
  GO {0,2,3,4,5,6,7,8} (8).
  profit = -5+18+35+35+15-15+10+35 = **128**.
- sh=2: s0 b1 34>16 GO eff0 -15; s1 b0 0 no; s2 b0 0 no;
  s3 b2 -2 no; s4 b1 34>16 GO eff0 -15; s5 b3 13 no;
  s6..s10 b0 0 no; s11 b1 84>16 GO eff100 +85.
  GO {0,4,11} (3).
  profit = -15-15+85 = **55**.
- Total: **243** (18 GO).

V_PBX fenced diagnostic (bars above; arithmetic only):

- sh=0 (bars (15,8,28,4)): s0 13>28 no; s1 0 no; s2 17>8 GO
  eff33 +18; s3 34>8 GO eff0 -15; s4 17>8 GO eff33 +18;
  s5 24>4 GO eff33 +18; s6 6>4 GO eff20 +5; s7 17>8 GO
  eff33 +18; s8 0 no; s9 17>8 GO eff33 +18; s10 9>8 GO
  eff25 +10; s11 2>4 no.
  GO {2,3,4,5,6,7,9,10} (8).
  profit = 18-15+18+18+5+18+18+10 = **90**.
- sh=1 (bars (15,8,13,14)): s0 30>14 GO eff10 -5; s1 0 no;
  s2 17>8 GO eff33 +18; s3 34>8 GO eff50 +35; s4 34>8 GO
  eff50 +35; s5 20>14 GO eff30 +15; s6 34>8 GO eff0 -15;
  s7 23>13 GO eff25 +10; s8 34>8 GO eff50 +35; s9 0 no;
  s10 9>8 GO eff25 +10; s11 5>14 no.
  GO {0,2,3,4,5,6,7,8,10} (9).
  profit = -5+18+35+35+15-15+10+35+10 = **138**.
- sh=2 (bars (15,32,13,28)): s0 34>32 GO eff0 -15; s4 34>32
  GO eff0 -15; s11 84>32 GO eff100 +85; s5 13>28 no; rest 0
  no.
  GO {0,4,11} (3).
  profit = -15-15+85 = **55**.
- Total: **283** (20 GO).

Lineage reference:

- execute-all: (43, 113, -80) = 76.

WC-FINAL: 24 train + 56 GO (17 + 21 + 18; PBX uses zero world
calls) + 36 reference = **116**.

## Frozen kill bars

- **K1 (diet / commit order / no-exact-signal / probe-proofness):
  PASS required.** A1: phase order train COMMIT < train PREFF <
  train CONSEQ < train LEARN < train BAR < sealed COMMIT <
  sealed BARS < sealed VERDICT (GO) < CONSEQUENCE
  (world_execute on GO) < REFERENCE < FENCED-PBX, by source
  line order (strict increase is the frozen property). A2: zero
  `world_buf`/`world_off` tokens in learner fns (lc_blocked,
  lc_leg, learner_compose, gather_cells). A3: zero
  `expected|answer|key|target` (case-insensitive). A4: zero
  `correct|reference_plan|gold`. A5: `world_execute(` exactly 4
  occurrences (1 def + 3 call sites: train CONSEQ, the shared
  `conseq_arm` helper, REFERENCE). The PBX diagnostic uses zero
  world_execute calls (pure arithmetic on the REFERENCE-filled
  buffer). A6: WC-FINAL = 116. A7: zero `learner_`/`belief_`
  calls after the CONSEQUENCE marker. A8: the token "oracle"
  (case-insensitive) appears zero times. A9 (the no-exact-
  signal bar): the token `Tpred` appears zero times. A10
  (probe-proofness): the V_PBK bar is computed without reading
  any sealed bias-adjusted score -- bar_b = K + mcalib[b], with
  mcalib train-fixed and the bar selected by bkt_s (sealed,
  bias-free); the V_PBOPT bars are computed from train
  (adj, eff) only and likewise selected by bkt_s. The fenced
  probes of the lineage touch adjusted scores only, never bkt,
  so they cannot move either per-bucket bar. The PBX diagnostic
  is fenced (not a learner bar) and reads sealed eff only after
  REFERENCE; it does not affect any verdict.
- **K2 (determinism): PASS required.** 3/3 runs byte-identical
  stdout.
- **K3 (verbatim machinery + new quantities): PASS required.**
  BARS lines: ThyA = 13/20/6, ThyB = 13/20/13 @15/30/45; TFIXED
  = 12; CVAL = 15; ThyHKC = 15/20/15; mcalib = (0,-11,-12,-3).
  New: V_PBK per-bucket bars = (15,4,3,12); V_PBOPT per-bucket
  bars = (15,16,5,15); UCB x V_WK = (75,128,55) = 258;
  V_PBX = (90,138,55) = 283; execute-all = (43,113,-80)
  (in-program exact checks).
- **K4 (PRIMARY): PASS required.** UCB x V_PBK total = 248 <
  258 AND UCB x V_PBOPT total = 243 < 258. No learner-
  computable per-bucket bar beats the fixed stakes bar. The
  below-batch-level information is real (K10) but not
  learner-usable from train alone: the train->sealed
  per-bucket gap shift (b2: -12 on train vs +13 sealed @15;
  b1: -11 on train vs +17 sealed @45; b3: -3 on train vs +13
  sealed @45 and -11 sealed @15) is not predictable from bucket
  identity plus train.
- **K5: PASS required.** Execute-all per-batch profit =
  (43, 113, -80).
- **K6: PASS required.** UCB x V_PBK total = 248, coinciding
  with the V_BAMK lineage total. Mechanism: the differential
  bands between the per-bucket bars (15,4,3,12) and the
  batch-mix bars (8,8,11) contain no sealed cases on these
  batches (e.g. @15: no b0 case with adj in (8,15], no b1 case
  with adj in (4,8], no b2 case with adj in (3,8], no b3 case
  with adj in (8,12]), so the GO sets coincide exactly.
- **K7: PASS required.** UCB x V_PBOPT total = 243 < 248 =
  UCB x V_PBK total. Train-profit-optimal per-bucket bars
  overfit train: the b1 bar 16 (optimal on train, exploiting
  the train (17,0) case) misses sealed s10's +10 at @15 and
  @30, while the b3 bar 15 avoids s5's -15 at @45 only once --
  net worse than gap-adjustment.
- **K8: PASS required.** WC-FINAL = 116 (in-program).
- **K9 (preregistered divergence): PASS required.** UCB x V_PBK
  total = 248 < UCB x V_WK total = 258. Per-bucket worth-K
  does NOT beat pure worth-K: the @15 loss (takes s0's -15 via
  the b2 bar 3) and the @45 loss (takes s5's -15 via the b3
  bar 12) mirror the batch-mix signal's failures, now at
  bucket resolution.
- **K10 (preregistered divergence): PASS required.** V_PBX
  total = 283 > UCB x V_PBK total = 248. The exact per-bucket
  signal beats the learner per-bucket signal by 35, decomposed
  as: @15, the exact b2 bar 28 avoids s0's -15 and the exact
  b3 bar 4 takes s6's +5 (20); @30, 0 (the learner already
  matches); @45, the exact b3 bar 28 avoids s5's -15 (15).
  The per-bucket information is real -- the exact gaps gain 25
  over fixed-K (283 > 258) -- but it lives below what train
  alone can supply.

**BUILD-PASS requires K1..K10.**

## Preregistered answers to the task's key questions

1. **Do per-bucket bars beat fixed-K?** Predicted NO (K4/K9):
   248 and 243 < 258. Neither the gap-adjusted nor the
   train-optimal per-bucket bar beats the fixed stakes bar.
   Going below batch level does not fix the fundamental
   problem: the bar moves on train's bucket miscalibration,
   and the shift moves the sealed bucket miscalibration
   differently.
2. **Do they approach the per-bucket exact bound (283)?**
   Predicted NO (K10): the learner's best per-bucket total
   (248) trails the exact bound by 35. The bound is approached
   exactly at @30 (138 = 138) but missed at @15 (70 vs 90)
   and @45 (40 vs 55), both misses coming from
   train->sealed per-bucket gap sign/magnitude shifts.
3. **Is the information actually usable (not just exact)?**
   Predicted NO as a verdict input: every learner-computable
   per-bucket bar tested (gap-adjusted and train-optimal)
   fails to beat fixed-K, while the exact per-bucket signal
   gains 25 over it. The below-batch-level information is
   real but not extractable from {train, bucket identity, K}
   on these shifts. Usable directions named for the next
   frontier: marginal (decision-boundary-local) per-bucket
   miscalibration, learner-owned K, the K-sensitivity curve.

## Determinism and honesty rules

- Integer arithmetic only. No researcher-set constants in any
  learner path (mcalib and bar* are computed from train data;
  the per-bucket application is structural; K=15 lives in the
  world/consequence phase and as the bar anchor).
- No post-prereg probe of any kind. All predictions above are
  arithmetic on the committed tables.
- The tokens `Tpred`, `oracle`, `expected`, `answer`, `key`,
  `target`, `correct`, `reference_plan`, `gold` do not appear in
  the implementation source (K1 A3/A4/A8/A9).
- If any arm differs from prediction in either direction, report
  the exact mechanism. No bar moves after seeing results.
