# PREREG.md -- IVWC-NONTRANSDUCTIVE: non-transductive verdicts

## Wave

Follow-up from IVWC-CASEBIAS-RETRY. That wave closed the case-level-bias
line four ways and established: (a) the transductive mean-bar verdict
actively destroys even a PERFECT phantom signal (D1: 8/12 @15, worse than
UCB's 11/12; the bar chase-down flips true-negatives s=1, s=8, s=10 that
the bias never touched); (b) D1 scores 12/12 @45, so phantom-ness IS
sufficient signal. Preregistered recommendation: "the bar, not the bias,
is now the measured bottleneck."

This wave tests the #1 structural hypothesis: **non-transductive
verdicts**. The verdict, not the bias, changes. Everything else
(world/belief/composer/stepper/verifier/seeds, UCB bias, D1/D2 fenced
diagnostics) is verbatim from IVWC-CASEBIAS-RETRY (sealed pairs
bit-identical; K3/K4 anchors verify).

Non-ledger task. Lane `ivwc_nontransductive/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab`, never pushed.

## Background facts (from committed reports, not probed)

- IVWC-SCOREBIAS: V-UCB 11/12 @15 (sole error s=3: phantom, P=50,
  bkt=1), 10/12 @45 (errors s=0,s=4). Verdict family throughout:
  adjV = P - bias(case), PASS iff adjV > TV, TV = mean adjV over the
  sealed batch (transductive mean bar, strict margin).
- IVWC-CASEBIAS-RETRY: D1 (fenced; bias = UCB_b + 40 iff nphantom > 0,
  nphantom = planned gathers at cells where the TRUE world has no item)
  scores 8/12 @15 with errors {s=1,s=5,s=8,s=10}: fixes s=3, but the
  +40 corrections drag the mean bar down and flip true-negatives s=1,
  s=8 (adjV=0) and s=10 (adjV=9) to wrong PASS; s=5 (nph=1, ge=1) is
  crushed by the binary +40 to wrong FAIL. D1 @45 = 12/12. D2
  (shuffled) @15 = 6/12.

## The non-transductive verdict

Transductive (current): v_i = 1 iff adjV_i > TV, TV = mean(adjV over the
sealed batch). The bar is a function of the batch AND of the bias
corrections: large corrections move the bar, which re-ranks untouched
cases (chase-down).

Non-transductive (this wave): v_i = 1 iff adjV_i > T_fixed, where
T_fixed = mean over the 24 TRAIN cases of (preff_tr - bucb[bkt_tr]),
the train-scoped mean of the UCB-adjusted score. Learner-computed,
train-only, no sealed-batch quantity enters, no researcher-set constant.
It is the direct non-transductive analog of TV: the same statistic,
train scope instead of batch scope. Each case is judged independently
against a bar the corrections cannot move.

From the committed retry train table (FA lines) and recomputed
bucb = (0,16,27,20): train adjV sums to 306, T_fixed = 306/24 = 12
(integer division). This value is DERIVED in-program, not set; 12 is
stated here as the preregistered expectation so the mechanism
predictions below are checkable.

## Arms (2x2 + shuffled controls)

Biases: B0 = UCB (bucb[bkt]); B1 = D1b (bucb[bkt] + 40 iff nphantom>0,
fenced harness diagnostic, never learner-visible); B2 = D2b (same with
the phantom indicator rotated by 7, fenced).

Verdicts: V_T = transductive mean bar (adjV > mean sealed adjV);
V_N = non-transductive fixed bar (adjV > T_fixed).

- A1 = B0 x V_T (anchor; = V-UCB of prior waves).
- A2 = B0 x V_N (does the fixed bar alone help/hurt UCB?).
- A3 = B1 x V_T (anchor; = D1 of the retry).
- A4 = B1 x V_N (KEY TEST: perfect phantom signal under a
  non-transductive verdict).
- A5 = B2 x V_T (anchor; = D2 of the retry).
- A6 = B2 x V_N (control: is A4's effect signal content or bar?).

Anchors re-scored in-program: OF (P >= Tpred), X3 (frozen bucket
table), HYB, MG.

## Frozen mechanism predictions (from committed retry per-case tables)

@15 (wp=15). D1b adjV: s=0:-27, s=1:0, s=2:17, s=3:-6, s=4:17, s=5:-16,
s=6:-34, s=7:17, s=8:0, s=9:17, s=10:9, s=11:-38; ge=1 on {2,4,5,7,9}.
UCB adjV: s=0:13, s=1:0, s=2:17, s=3:34, s=4:17, s=5:24, s=6:6, s=7:17,
s=8:0, s=9:17, s=10:9, s=11:2.

- A1: 11/12, errors {s=3} (reproduce).
- A2: 10/12, errors {s=0, s=3}. s=0's adjV=13 clears T_fixed=12 (under
  V_T the bar sat at exactly 13 and the strict margin flipped it to
  FAIL). The fixed bar LOSES the load-bearing tie-break.
- A3: 8/12, errors {s=1,s=5,s=8,s=10} (reproduce).
- A4: 11/12, errors {s=5}. The three chase-down errors (s=1,s=8,s=10)
  vanish: their adjV (0,0,9) sit below the unmoved bar. s=3 is fixed
  (-6 < 12). s=5 remains: the binary +40 crushes a TRUE-POSITIVE
  phantom (adjV=-16, ge=1). NOTE: no single-threshold verdict on D1b
  adjV can exceed 11/12 @15 (s=5 at -16 must PASS while s=3 at -6 must
  FAIL: inverted). 11/12 is the THEORETICAL CEILING of the
  (D1b x threshold-verdict) family; V_N attains it, V_T scores 3 below
  it.
- A5: 6/12 (reproduce).
- A6: 8/12, errors {s=0,s=3,s=4,s=5}.

@30 (wp=30). Committed D1b adjV: s=0:-10, s=1:0, s=2:17, s=3:34, s=4:34,
s=5:-20, s=6:-6, s=7:-17, s=8:34, s=9:0, s=10:9, s=11:-35; ge=1 on
{3,4,8}.

- A1: 9/12 (reproduce). A2: 7/12, errors {s=0,s=2,s=5,s=6,s=7}. A3:
  10/12 (reproduce). A4: 11/12, errors {s=2} (s=2: adjV=17 > 12 PASS,
  but ge=0 since Tpred@30=35 > eff=33; the fixed bar cannot track the
  batch-relative label under shift). A5: 8/12 (reproduce). A6: 8/12,
  errors {s=2,s=4,s=6,s=7}.

@45 (wp=45). Committed D1b adjV: s=0:-6, s=1:0, s=2:0, s=3:-42, s=4:-6,
s=5:-27, s=6..10:0, s=11:84; ge=1 on {11}.

- A1: 10/12, errors {s=0,s=4} (reproduce). A2: 9/12, errors {s=0,s=4,s=5}
  (s=5: UCB adjV=13 > 12 PASS, ge=0). A3: 12/12 (reproduce). A4: 12/12
  (the phantom correction is strong enough that any sane fixed bar
  separates; T_fixed=12 does). A5: 10/12 (reproduce). A6: 10/12,
  errors {s=0,s=4}.

## Frozen kill bars

- **K1 (diet / commit order): PASS required.** A1: train COMMIT < PREFF
  < CONSEQ < BAR < sealed COMMIT < SCORING by source line order. A2:
  zero `world_buf`/`world_off` tokens in learner fns. A3: zero
  `expected|answer|key|target` (case-insensitive). A4: zero
  `correct|reference_plan|gold`. A5: `world_execute(` exactly 3
  occurrences (1 def + 2 call sites). A6: WC-FINAL = 60 (24 train + 36
  sealed). A7: zero `learner_`/`belief_` calls after the SCORING marker.
  A8: the token "oracle" (case-insensitive) appears zero times (the word
  is avoided entirely; diagnostics are named D1/D2 as in the retry).
- **K2 (determinism): PASS required.** 3/3 runs byte-identical stdout.
- **K3 (anchor @15): PASS required.** acc_OF = 10, acc_X3 = 9.
- **K4 (anchor @45): PASS required.** acc_OF = 8, acc_X3 = 10.
- **K5 (PRIMARY): PASS required.** A4 @15 = 11/12 with error set exactly
  {s=5}. (Predicted PASS: the non-transductive verdict eliminates the
  three bar-chase errors; the remaining error is the binary bias's
  crudeness on a true-positive phantom, not the verdict.)
- **K6: PASS required.** A3 @15 = 8/12 (reproduces the
  bar-destroys-signal anchor; confirms the signal is unchanged).
- **K7: PASS required.** A2 @15 <= 10/12 (predicted exactly 10/12,
  errors {s=0,s=3}). The fixed bar ALONE is not a general improvement;
  it specifically un-blocks large corrections while losing UCB's
  load-bearing tie-break.
- **K8: PASS required.** A6 @15 < A4 @15 (predicted 8/12 < 11/12). The
  A4 gain is phantom-signal content, not a bar artifact.
- **K9: PASS required.** A4 @45 = 12/12. The phantom correction
  generalizes under the wp=15->45 law change with a fixed bar.
- **K10: PASS required.** A4 @30 = 11/12 and A3 @30 = 10/12 (A4 > A3).
  The bar fix also helps @30.

**BUILD-PASS requires K1,K2,K3,K4,K5,K6,K7,K8,K9,K10.**

## Preregistered answers to the task's key questions

1. Can a non-transductive verdict achieve 12/12 @15 with perfect phantom
   information (D1)? Predicted NO: 11/12, the theoretical ceiling of
   (D1b x threshold-verdict). The bar was the bottleneck for 3 of D1's
   4 @15 errors; the 4th (s=5) is the binary +40 crushing a
   true-positive phantom, a bias-crudeness error no threshold verdict
   can fix. If A4 reaches 12/12, the ceiling proof is wrong and the
   report says so loudly.
2. What is the right non-transductive verdict structure? The
   train-scoped mean bar: same statistic as TV, train scope. It removes
   chase-down (corrections cannot move it) while staying
   learner-computed with no researcher-set constant.
3. Does it generalize or overfit to the phantom signal? Predicted: the
   verdict does not overfit (K8: shuffled signal gains nothing from it),
   but it does not adapt to law change either (K7 @15, A2 @30 = 7/12:
   the fixed bar is miscalibrated when the adjV distribution shifts;
   the transductive bar's virtue is adaptation, its vice is
   chase-down). @45 the D1b correction is robust enough that the fixed
   bar holds 12/12 (K9).

## Determinism and honesty rules

- Integer arithmetic only. No researcher-set constants in any learner
  path (the +40 lives only in the fenced diagnostic, as in the retry).
- No post-prereg probe of any kind. All predictions above are derived
  from the committed ivwc_casebias_retry REPORT.md and runs/
  per-case tables, never re-read as new data.
- If A4 differs from prediction in either direction, report the exact
  mechanism. No bar moves after seeing results.
