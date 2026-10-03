# PREREG.md -- IVWC-HYBRID-VERDICT: batch-responsive, correction-independent verdicts

## Wave

Follow-up from IVWC-NONTRANSDUCTIVE (BUILD-PASS, K1-K10). That wave
established the honest tradeoff:

- V_T (transductive): PASS iff adjV > mean(sealed adjV). The bar moves
  with the batch AND with the bias corrections (chase-down). Punishes
  corrections (D1b: 8/12 @15) but adapts (UCB: 11/9/10 @15/30/45).
- V_N (non-transductive): PASS iff adjV > T_fixed (T_fixed=12,
  train-only). Permits corrections (D1b: 11/12 @15, the theoretical
  ceiling) but cannot adapt (UCB: 10/7/9; the s=0 tie-break lost @15,
  miscalibrated @30/@45).

This wave tests the preregistered synthesis: **a bar that is
batch-responsive yet correction-independent**. The candidate mechanism
is preff-scoping: the bar is computed from `preff` (which bias
corrections cannot move) rather than from `adjV` (which they do move).

Non-ledger task. Lane `ivwc_hybrid_verdict/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab`, never pushed.

## Background facts (from committed reports/runs, not probed)

- IVWC-NONTRANSDUCTIVE, committed run
  `runs/ivwc_nontransductive-run1.txt`: per-case (bkt, preff, nph,
  a1..a6, eff, ge) for all 12 sealed cases at sh=0/1/2 (wp=15/30/45),
  train TA lines (t, bkt, preff, eff, d, adj), BARS lines
  (TVucb=13/20/13, Tfixed=12, Tpred=28/35/21). All predictions below
  are arithmetic on these committed tables. No new data was generated
  or read before this prereg.
- bucb (train-learned UCB bias) = (0,16,27,20). Train bucket counts:
  7/7/7/3 (bkt 0/1/2/3).
- D1b: bias = bucb[bkt] + 40 iff nphantom>0 (fenced harness
  diagnostic, never learner-visible). D2b: same with the phantom
  indicator rotated by 7: +40 iff nphantom[(s+7)%12] > 0.
- Committed D1b adjV @15: s=0:-27, s=1:0, s=2:17, s=3:-6, s=4:17,
  s=5:-16, s=6:-34, s=7:17, s=8:0, s=9:17, s=10:9, s=11:-38;
  ge=1 on {2,4,5,7,9}.
- Committed D1b adjV @30: s=0:-10, s=1:0, s=2:17, s=3:34, s=4:34,
  s=5:-20, s=6:-6, s=7:-17, s=8:34, s=9:0, s=10:9, s=11:-35;
  ge=1 on {3,4,8}.
- Committed D1b adjV @45: s=0:-6, s=1:0, s=2:0, s=3:-42, s=4:-6,
  s=5:-27, s=6..10:0, s=11:84; ge=1 on {11}.
- Committed UCB adjV @15: s=0:13, s=1:0, s=2:17, s=3:34, s=4:17,
  s=5:24, s=6:6, s=7:17, s=8:0, s=9:17, s=10:9, s=11:2.
- Derived UCB adjV @30 (D1b + 40 where nph>0; nph>0 on {0,5,6,7,11}):
  s=0:30, s=1:0, s=2:17, s=3:34, s=4:34, s=5:20, s=6:34, s=7:23,
  s=8:34, s=9:0, s=10:9, s=11:5. Sum=240, mean=20=TVucb. Consistent.
- Derived UCB adjV @45 (nph>0 on {0,3,4,5}): s=0:34, s=1:0, s=2:0,
  s=3:-2, s=4:34, s=5:13, s=6:0, s=7:0, s=8:0, s=9:0, s=10:0,
  s=11:84. Sum=163, mean=13 (truncated)=TVucb. Consistent.
- Derived D2b adjV @15 (+40 on {4,5,8,10,11}): s=0:13, s=1:0, s=2:17,
  s=3:34, s=4:-23, s=5:-16, s=6:6, s=7:17, s=8:-40, s=9:17, s=10:-31,
  s=11:-38. (Check: mean=-44/12->-3=TVd2; >-3 verdicts reproduce the
  committed a5 column exactly.)
- Derived D2b adjV @30 (+40 on {0,4,5,10,11}): s=0:-10, s=1:0, s=2:17,
  s=3:34, s=4:-6, s=5:-20, s=6:34, s=7:23, s=8:34, s=9:0, s=10:-31,
  s=11:-35.
- Derived D2b adjV @45 (+40 on {5,8,9,10}): s=0:34, s=1:0, s=2:0,
  s=3:-2, s=4:34, s=5:-27, s=6:0, s=7:0, s=8:-40, s=9:-40, s=10:-40,
  s=11:84.
- Committed sealed preff sums: @15: 339 (mean 28); @30: 423
  (mean 35); @45: 258 (mean 21). All integer division truncated.

## The hybrid verdicts

Verdict family throughout: v_i = 1 iff adjV_i > BAR (strict margin),
adjV = preff - bias(case). The experimental variable is BAR.

**V_HA (primary): preff-scoped bar.**
BAR = ThyA(sh) = (sum of sealed preff)/12 - C,
C = (sum over the 24 train cases of bucb[bkt_tr])/24 (integer
division, train-fixed).
Correction-independence: the bar is a function of sealed preff (which
the +40 corrections cannot move) and the train-fixed scalar C (which
nothing in the sealed batch can move). No sealed adjV, no nphantom,
no +40 enters the bar computation -- verifiable by code audit.
Batch-responsiveness: the bar is computed per sealed batch from that
batch's preff mean; it moves when the batch's plan mix moves.
Preregistered expectations: C = 361/24 = 15 (truncated); ThyA =
28-15 = 13 @15, 35-15 = 20 @30, 21-15 = 6 @45.

**V_HB (secondary): frozen-baseline-scoped bar.**
BAR = ThyB(sh) = (sum over the sealed batch of
(preff - bucb_frozen[bkt]))/12, bucb frozen at train.
Correction-independence: the bar may respond to the sealed batch's
bucket composition, but only through the FROZEN baseline bias --
never through the experimental +40 corrections. Algebraically
ThyB == TVucb; it is computed explicitly as its own sum so the
construction is auditable.
Batch-responsiveness: full -- the bar tracks the sealed batch's
(preff, bucket) joint distribution.
Preregistered expectations: ThyB = 13/20/13 @15/30/45 (== TVucb).

The decomposition this tests:
- V_T  = batch-responsive + correction-DEPENDENT (bar includes +40s).
- V_HB = batch-responsive + correction-INDEPENDENT (bar excludes +40s).
- V_HA = batch-responsive-to-preff-only + correction-independent.
- V_N  = batch-UNresponsive + correction-independent.
V_HA is the task's candidate ("scoped to preff"). V_HB isolates how
much of V_T's adaptation is recoverable without the chase-down.

## Arms (6 anchors + 6 hybrid)

Biases: B0=UCB, B1=D1b, B2=D2b (verbatim from nontransductive).
Verdicts: V_T, V_N (anchors), V_HA, V_HB.
- A1=B0xV_T, A2=B0xV_N, A3=B1xV_T, A4=B1xV_N, A5=B2xV_T, A6=B2xV_N
  (verbatim anchors; the three-way comparison requires them).
- A7a=B0xV_HA, A7b=B0xV_HB (learner-side; adjucb vs ThyA/ThyB).
- A8a=B1xV_HA, A8b=B1xV_HB, A9a=B2xV_HA, A9b=B2xV_HB (fenced;
  d1adj/d2adj vs ThyA/ThyB).
Anchors OF/X3/HYB/MG re-scored in-program.

## Frozen mechanism predictions

@15 (ThyA=13, ThyB=13, Tfixed=12, TVucb=13, Tpred=28):
- A7a: adjV>13 on {2,3,4,5,7,9} (s=0: 13 not > 13); ge=1 on
  {2,4,5,7,9} -> errors {s=3} -> 11/12. (== A1; the s=0 tie-break is
  preserved.)
- A7b: identical bar -> 11/12, errors {s=3}. (== A1 by construction.)
- A8a: d1adj>13 on {2,4,7,9} -> errors {s=5} -> 11/12. The untouched
  true-negatives (s=1: 0, s=8: 0, s=10: 9) stay below the unmoved bar;
  s=3 (-6) stays below it. V_N's un-blocking, batch-computed.
- A8b: identical -> 11/12, errors {s=5}.
- A9a: d2adj>13 on {2,3,7,9} -> errors {s=3,s=4,s=5} -> 9/12.
- A9b: identical -> 9/12.

@30 (ThyA=20, ThyB=20, Tfixed=12, TVucb=20, Tpred=35):
- A7a: adjV>20 on {0,3,4,6,7,8}; ge=1 on {3,4,8} -> errors
  {s=0,s=6,s=7} -> 9/12. (== A1; recovers V_T fully vs A2's 7/12.)
- A7b: identical -> 9/12.
- A8a: d1adj>20 on {3,4,8} -> 12/12. The batch's preff mean rises
  (35 vs 28) and the label threshold rises with it (35 vs 28); ThyA
  tracks the preff rise (20 vs 13) while T_fixed stays at 12. s=2
  (adjV=17, ge=0 since eff=33<35) is correctly failed by the higher
  bar. BEATS V_N's 11/12.
- A8b: identical -> 12/12.
- A9a: d2adj>20 on {3,6,7,8} -> errors {s=4,s=6,s=7} -> 9/12.
- A9b: identical -> 9/12.

@45 (ThyA=6, ThyB=13, Tfixed=12, TVucb=13, Tpred=21):
- A7a: adjV>6 on {0,4,5,11}; ge=1 on {11} -> errors {s=0,s=4,s=5} ->
  9/12. (== A2's verdicts exactly: no UCB adjV lies in (6,12].)
  V_HA does NOT recover V_T's 10/12 here -- the predicted LIMIT.
  Mechanism: the @45 batch is bucket-0 heavy (7 of 12 cases bkt=0,
  bias 0); the sealed mean bias (~7.9) is far below train's C
  (15.04), so ThyA=6 undershoots the batch's adjV level (13) and
  s=5 (adjV=13, ge=0) clears it. Preff-scoping recovers adaptation
  to plan-density (preff-level) shifts but NOT to bias-mix shifts,
  because the calibration offset must be train-fixed to stay
  correction-independent.
- A7b: adjV>13 on {0,4,11} -> errors {s=0,s=4} -> 10/12. (== A1;
  V_HB recovers V_T fully on UCB by responding to the sealed bucket
  mix through the frozen baseline bias.)
- A8a: d1adj>6 on {11} -> 12/12. (== A4.)
- A8b: d1adj>13 on {11} -> 12/12.
- A9a: d2adj>6 on {0,4,11} -> errors {s=0,s=4} -> 10/12.
- A9b: d2adj>13 on {0,4,11} -> errors {s=0,s=4} -> 10/12.

## Frozen kill bars

- **K1 (diet / commit order): PASS required.** A1: train COMMIT <
  train PREFF < train CONSEQ < train BAR (T_fixed AND C) < sealed
  COMMIT < sealed BARS (ThyA, ThyB) < SCORING world_execute, by
  source line order (exact numbers recorded post-build; the
  property -- strict increase across the marker sequence -- is the
  frozen bar). A2: zero `world_buf`/`world_off` tokens in learner
  fns (lc_*, learner_compose*, belief_execute, gather_cells,
  verifier_*). A3: zero `expected|answer|key|target`
  (case-insensitive). A4: zero `correct|reference_plan|gold`. A5:
  `world_execute(` exactly 3 occurrences (1 def + 2 call sites).
  A6: WC-FINAL = 60 (24 train + 36 sealed). A7: zero `learner_`/
  `belief_` calls after the SCORING marker. A8: the token "oracle"
  (case-insensitive) appears zero times.
- **K2 (determinism): PASS required.** 3/3 runs byte-identical stdout.
- **K3 (anchor @15): PASS required.** acc_of = 10, acc_x3 = 9.
- **K4 (anchor @45): PASS required.** acc_of = 8, acc_x3 = 10.
- **K5 (PRIMARY): PASS required.** A8a @15 = 11/12 with error set
  exactly {s=5} (in-program: k5e=1, k5s=5). V_HA keeps V_N's
  un-blocking: the hybrid reaches the (D1b x threshold-verdict)
  theoretical ceiling.
- **K6: PASS required.** A3 @15 = 8/12 (reproduces the
  bar-destroys-signal anchor; the signal is unchanged).
- **K7: PASS required.** A7a @15 = 11/12 with error set exactly {s=3}
  (in-program: k7e=1, k7s=3). V_HA recovers V_T on UCB @15 --
  unlike V_N (10/12), the hybrid preserves the s=0 tie-break.
- **K8: PASS required.** A9a @15 < A8a @15 (predicted 9/12 < 11/12).
  The A8a gain is phantom-signal content, not a bar artifact.
- **K9: PASS required.** A8a @30 = 12/12 (in-program: k9e=0).
  V_HA's batch responsiveness beats V_N's fixed bar (11/12) under
  the @30 law shift -- the adaptation recovery.
- **K10: PASS required.** A7a @45 = 9/12 with error set exactly
  {s=0,s=4,s=5} (in-program: k10e=3, k10s=5). The LIMIT is confirmed
  as predicted: preff-scoping does not recover V_T's 10/12 @45.
  If A7a @45 scores 10/12, the bucket-mix mechanism story is wrong
  and the report says so loudly.

**BUILD-PASS requires K1,K2,K3,K4,K5,K6,K7,K8,K9,K10.**

Preregistered secondary findings (reported, not kill bars):
- S1: ThyB = 13/20/13 @15/30/45 (bar identity with TVucb, verified in
  the BARS line).
- S2: A7b == A1 everywhere: 11/9/10 @15/30/45, error sets
  {s=3}/{s=0,s=6,s=7}/{s=0,s=4}.
- S3: A8b: 11/12 {s=5} @15, 12/12 @30, 12/12 @45.
- S4: A9b: 9/12 @15, 9/12 @30, 10/12 @45.
- S5: A9a: 9/12 @15, 9/12 @30, 10/12 @45.

## Preregistered answers to the task's key questions

1. Can a hybrid verdict get the best of both (V_N's un-blocking +
   V_T's adaptation)? Predicted YES with one documented limit:
   V_HA un-blocks D1b (11/12 @15, the ceiling; 12/12 @30, beating
   V_N) AND recovers V_T's UCB adaptation @15 (11/12) and @30 (9/12),
   but NOT @45 (9/12 = V_N < V_T's 10/12). V_HB recovers V_T fully
   on UCB (11/9/10) while keeping the un-blocking (11/12, 12/12,
   12/12 on D1b) -- full best-of-both, at the cost of letting the
   sealed bucket mix (through the frozen baseline bias) move the bar.
2. Is preff-scoping the right mechanism? Predicted: it is the right
   mechanism for correction-independence (the +40s provably cannot
   move ThyA), and it buys back adaptation to plan-density shifts;
   but pure preff-scoping is NOT sufficient for full adaptation --
   the calibration offset's train-fixedness is exactly what blinds
   it to bias-mix shifts. The (HA vs HB) comparison measures the
   price of purity.
3. What are the limits? K10 is the preregistered limit: when the
   sealed batch's bias-relevant composition shifts far from train
   (@45: bucket-0 heavy), any train-calibrated offset miscalibrates,
   and only a bar that reads the sealed batch's bias mix (HB, or
   VT's chase-down-prone full responsiveness) recovers. A second
   limit, inherited: the label ge = (eff >= Tpred) stays
   transductive, so no verdict in this family tracks label shifts
   that preff doesn't reflect.

## Determinism and honesty rules

- Integer arithmetic only. No researcher-set constants in any learner
  path (the +40 lives only in the fenced diagnostic, as in the
  retry/nontransductive).
- No post-prereg probe of any kind. All predictions above are
  arithmetic on the committed nontransductive per-case tables, never
  re-read as new data.
- If any arm differs from prediction in either direction, report the
  exact mechanism. No bar moves after seeing results.
