# PREREG.md -- IVWC-KSENSITIVITY: the K-sensitivity curve

## Wave

Follow-up to IVWC-LEARNERK (BUILD-PASS K1-K10). LEARNERK closed
"learner-owned K": the global revealed bar (14) ties fixed-K (15) at
258 with identical GO sets (ownership without loss), the per-bucket
revealed bars (0,16,5,9) overfit to 228, and the preregistered NULL
held (owning K does not beat being given K). The arc pattern is now
nine waves deep: every learner-computable adjustment to the worth-K
bar loses to or ties the fixed stakes bar. LEARNERK explicitly named
the remaining frontier and did not test it: **the K-sensitivity curve**
-- for which K do the rankings change? This wave builds it.

Non-ledger task. Lane `ivwc_ksensitivity/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab` via explicit
pathspec plumbing. Pushing to origin is AUTHORIZED per Micah's
2026-10-03 authorization (fresh GitHub PAT; exclude reproducible
cache/build artifacts). NOTE: a previous worker found the
`gh_push_api.py` credential lacks git-database write scope (HTTP 403);
the remote ref appears to be at `99c5691d`. Do NOT push via the API
script; document the blockage for the parent.

## Design: measurement wave on committed tables

No world, no learner, no new mechanism, no new verdict arms. The
sealed (adjucb, eff) per-case tables are committed data (IVWC-LEARNERK
PREREG.md, citing IVWC-MARGINAL/IVWC-PERBUCKET). This wave is pure
measurement over those frozen tables:

**TABLE A -- decision-bar sweep.** For each integer decision bar K in
[-3, 85] (data-driven range: [min sealed adj - 1, max sealed adj + 1]
= [-3, 85]), the fixed-bar verdict GO iff `adjucb > K` on each of the
three sealed batches (@15/@30/@45), scored at the frozen world cost 15
(profit = sum over GO of (eff - 15)). Per-batch profits, total, GO
counts. This maps the full profit-vs-K curve: the two tested points
(14, 15) become two rows of 89.

**TABLE B -- revealed-bar-vs-train-cost.** For each hypothetical train
cost c in [-3, 40] (preregistered analytic window: negative through
2.6x the true cost), recompute the LEARNERK global revealed bar
b*(c) = argmax over integer b in [min train adj - 1, max train adj]
= [-11, 84] of P_c(b) = sum over train cases with tadj > b of
(teff - c), ties toward the larger bar (the frozen LEARNERK rule),
then score b*(c) on the sealed batches at the TRUE world cost 15.
This tests whether K-sensitivity is a useful signal: does the
revealed-preference machinery track the sealed optimum as the
experienced cost varies?

The binary embeds the train (t, bkt, adj, teff) and sealed
(sh, s, bkt, adj, eff) tables as literals, prints TAUDIT lines for
both, runs the two sweeps, prints in-program kill flags KS3-KS7.
KS1 (diet) is a worker-performed pre-build textual audit; KS2 is the
3/3 byte-identical runs check. No `world_execute` anywhere in this
wave (there is no world to call; the tables are the committed
evidence).

## Committed tables (verbatim from IVWC-LEARNERK PREREG.md)

Train (bkt, adj, net=eff-15); teff = net + 15:
- b0 (7): (0,-15) x7 -> teff 0 x7.
- b1 (7): (34,35) (17,18) (84,85) (34,35) (34,35) (34,35) (17,-15)
  -> teff 50,33,100,50,50,50,0.
- b2 (7): (-9,-9) (23,10) (-10,-15) (6,18) (15,27) (6,-15) (0,-6)
  -> teff 6,25,0,33,42,0,9.
- b3 (3): (5,-10) (7,1) (9,-4) -> teff 5,16,11.

Sealed (bkt, adj, eff); profit per GO case = eff - 15:
- sh=0 (@15): s0:(2,13,0) s1:(0,0,0) s2:(1,17,33) s3:(1,34,0)
  s4:(1,17,33) s5:(3,24,33) s6:(3,6,20) s7:(1,17,33) s8:(0,0,0)
  s9:(1,17,33) s10:(1,9,25) s11:(3,2,13).
- sh=1 (@30): s0:(3,30,10) s1:(0,0,0) s2:(1,17,33) s3:(1,34,50)
  s4:(1,34,50) s5:(3,20,30) s6:(1,34,0) s7:(2,23,25) s8:(1,34,50)
  s9:(0,0,0) s10:(1,9,25) s11:(3,5,20).
- sh=2 (@45): s0:(1,34,0) s1:(0,0,0) s2:(0,0,0) s3:(2,-2,0)
  s4:(1,34,0) s5:(3,13,0) s6:(0,0,0) s7:(0,0,0) s8:(0,0,0)
  s9:(0,0,0) s10:(0,0,0) s11:(1,84,100).

## Frozen derivations (arithmetic on the committed tables)

Per-batch fixed-bar profit (GO iff adj > K), cumulative from top adj:

sh=0: K>=34: 0; 24..33: -15; 17..23: 3; 13..16: 75; 9..12: 60;
  6..8: 70; 2..5: 75; 0..1: 73; K<=-1: 43.
sh=1: K>=34: 0; 30..33: 90; 23..29: 85; 20..22: 95; 17..19: 110;
  9..16: 128; 5..8: 138; 0..4: 143; K<=-1: 113.
sh=2: K>=84: 0; 34..83: 85; 13..33: 55; 0..12: 40; -2..-1: -65;
  K<=-3: -80.

Total profit by K (sh0+sh1+sh2):
- K<=-3: 76 (execute-all anchor: (43,113,-80))
- K=-2,-1: 91
- K=0,1: 256
- K=2,3,4: 258
- K=5: 253 = (75,138,40)
- K=6,7,8: 248
- K=9..12: 228
- K=13,14,15,16: 258
- K=17,18,19: 168
- K=20,21,22: 153
- K=23: 143
- K=24..29: 125
- K=30..33: 130
- K=34..83: 85
- K>=84: 0

Global maximum 258, attained exactly at
K in {2,3,4} U {13,14,15,16}.

Per-batch argmax sets: sh=0: {2,3,4,5,6,13,14,15,16} (75);
sh=1: {0,1,2,3,4} (143); sh=2: {34..83} (85). Total intersection
is EMPTY (sh=2 wants K>=34; the others want K<=16).

Revealed bar b*(c) (train cost c; P_c(b) = S(b) - c*N(b) with the
cumulative (teff, count) above b: (84: 100,1), (34: 300,5),
(23: 325,6), (17: 358,8), (15: 400,9), (9: 411,10), (7: 427,11),
(6: 460,13), (5: 465,14), (0: 474,22), (-9: 480,23),
(-10: 480,24)):
- b*(-3) = -11; b*(0) = -10; b*(4) = 4; b*(5) = 5; b*(10) = 5;
  b*(14) = 5; b*(15) = 14; b*(16) = 14; b*(20) = 14;
  b*(30) = 33; b*(40) = 33 (all with the larger-bar tie-break).
Sealed profit of b*(c) at true cost 15: c=-3 -> 76; c=0 -> 76;
c=4 -> 258; c=5 -> 253; c=10 -> 253; c=14 -> 253; c=15 -> 258;
c=16 -> 258; c=20 -> 258; c=30 -> 130; c=40 -> 130.

**Erratum carried by this wave:** the LEARNERK PREREG disclosed the
aggressive-tie-break (b=5) sensitivity as sealed (75,138,-40) = 173
("arithmetic on the committed tables, not run"). That arithmetic was
wrong: with bar 5, sh=2 takes s0,s4,s5 (adj 34,34,13 > 5, eff 0 ->
-15 each) and s11 (adj 84, eff 100 -> +85), for -15-15-15+85 = 40,
not -40. The correct value is (75,138,40) = 253. The tie-break is
LESS load-bearing than disclosed (253 vs 258, not 173 vs 258).
KS7 checks the sweep row K=5 against (75,138,40)=253.

## Frozen kill bars

- **KS1 (diet / commit order / no-exact-signal): PASS required**
  (worker-performed pre-build textual audit, recorded in REPORT).
  A1: phase order TABLES < TAUDIT < SWEEPA < SWEEPB < KFLAGS by
  source line order (strict increase is the frozen property; actual
  line numbers recorded in the report). A2: zero `world_buf` /
  `world_off` tokens. A3: zero `expected|answer|key|target`
  (case-insensitive). A4: zero `correct|reference_plan|gold`.
  A5: zero `world_execute(` occurrences. A6: zero `oracle`.
  A7: zero `Tpred`. A8 (measurement honesty): the only sweep
  variables are the decision bar K and the hypothetical train cost
  c; every profit is scored at the frozen world cost 15 (the sealed
  batches were generated and scored under it -- a measurement given,
  not a learner input).
- **KS2 (determinism): PASS required.** 3/3 runs byte-identical
  stdout; sha256 recorded.
- **KS3 (verbatim tables + anchors): PASS required** (in-program).
  24/24 train TAUDIT lines and 36/36 sealed TAUDIT lines
  byte-identical to the committed tables above (worker-verified
  against this PREREG); K=15 -> (75,128,55) = 258; K=14 -> 258
  with per-case GO sets identical to K=15 (in-program per-case
  equality); K=-3 -> (43,113,-80) = 76.
- **KS4 (PRIMARY -- curve shape): PASS required** (in-program).
  Decision rule frozen pre-build: the curve is FLAT iff (a) the
  maximum total profit is 258, AND (b) the longest contiguous run
  of integer K attaining 258 has length >= 4, AND (c) at least 8
  distinct K have total >= 246 (0.95 x 258 = 245.1, integer
  threshold 246); otherwise SHARP. Predicted FLAT: max set is
  {2,3,4} U {13,14,15,16} (longest run {13,14,15,16}, length 4);
  13 values >= 246 ({0,1}: 256, {2,3,4}: 258, {5}: 253,
  {6,7,8}: 248, {13,14,15,16}: 258).
- **KS5 (batch stability of the optimum): PASS required**
  (in-program). Decision rule frozen pre-build: the optimum is
  STABLE iff there exists a K whose per-batch profits are all
  three batch maxima simultaneously; otherwise SHIFTED. Predicted
  SHIFTED: no K is optimal for all three batches (sh=2 wants
  K>=34; sh=0/sh=1 want K<=16).
- **KS6 (revealed-bar tracking / K-sensitivity as signal): PASS
  required** (in-program). b*(15) == 14 AND sealed-total(14) ==
  sweep maximum (258) AND sealed-total(b*(14)) >= 246 AND
  sealed-total(b*(16)) >= 246. Predicted PASS: (14 -> 258;
  b*(14)=5 -> 253; b*(16)=14 -> 258). The revealed bar at the true
  train cost attains the sweep maximum, and unit cost perturbations
  keep sealed profit within 5% of max even though the bar itself
  jumps (14 -> 5).
- **KS7 (erratum confirmation): PASS required** (in-program).
  Sweep row K=5 is exactly (75,138,40) = 253, confirming the
  corrected aggressive-tie-break value and the LEARNERK erratum.

**BUILD-PASS requires KS1..KS7.**

## Preregistered answers to the task's key questions

1. **What does the K-sensitivity curve look like?** Predicted: a
   broad plateau, not a sharp peak (KS4 FLAT). Maximum 258 on
   {2,3,4} U {13,14,15,16}; 13 of 89 K values within 5% of max;
   profit falls off steeply below K=0 (91, 76) and above K=16
   (168 -> 153 -> 143 -> 125 -> 130 -> 85 -> 0).
2. **Is the optimum stable or does it shift?** Predicted: it
   shifts by batch (KS5 SHIFTED). sh=0 and sh=1 want low bars
   (0..6 / 0..4); sh=2 (@45) wants K>=34 (take only the (84,85)
   case). The global optimum {2,3,4} U {13,14,15,16} is a
   cross-batch compromise, sacrificing 30 on sh=2 (55 vs 85) to
   hold sh=0/sh=1.
3. **Can K-sensitivity inform better verdicts?** Predicted: the
   signal is in the flatness, not the peak. The revealed bar
   b*(c) is violently sensitive to train cost (unit changes flip
   14 <-> 5), but sealed profit is flat over the landing region
   (253..258 for c in [4,20]). So the fixed-K 15 sits inside a
   broad optimum: the LEARNERK tie (14 vs 15) was not luck, any
   bar in [2,16] does nearly as well, and no fixed bar beats 258.
   The exact lineage bounds (283/288/318) remain above every
   fixed bar -- the information is real but not reachable by any
   threshold verdict.

## L2 vs L3 assessment (preregistered)

This wave makes no learning claim: L0 measurement (a sweep over
frozen tables) feeding an L1 interpretation. Not L2 (no structure
is learned or adapted here), not L3 by any reading.

## Determinism and honesty rules

- Integer arithmetic only. K range [-3,85] is data-driven
  ([min-1, max+1] over sealed adjs); c range [-3,40] is a
  preregistered analytic window; the larger-bar tie-break is the
  frozen LEARNERK rule, never tuned.
- No post-prereg probe of any kind. All predictions above are
  arithmetic on the committed tables.
- The tokens `world_execute`, `Tpred`, `oracle`, `expected`,
  `answer`, `key`, `target`, `correct`, `reference_plan`, `gold`,
  `world_buf`, `world_off` do not appear in the implementation
  source (KS1 A2-A7).
- If any sweep row differs from prediction in either direction,
  report the exact mechanism. No bar moves after seeing results.
