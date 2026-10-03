# PREREG.md -- IVWC-CASEBIAS-RETRY: case-level bias, second attempt

## Wave

Follow-up #1 from IVWC-SCOREBIAS ("case-level (not bucket-level) bias
signals for phantom-type errors like s=3"), retried after IVWC-CASEBIAS
(BUILD-FAIL: V-CONDC diet-blocked, V-AGREE/V-STRUCT degenerate, oracle
10/12 @15). This wave tests a genuinely new learner signal class
(counterfactual perturbation fragility, V-SENS) and, via fenced harness
diagnostics, whether a PERFECT phantom signal can succeed under the
transductive mean-bar verdict (D-ORACLE-BIAS) or not.

Non-ledger task. Lane `ivwc_casebias_retry/`. Pure Zag, safebin, 3/3
byte-identical. Commits local on `tnn-native-lab`, never pushed.

## Background facts (from committed reports, not probed)

- IVWC-SCOREBIAS: V-UCB 11/12 @15 (sole error s=3: phantom, P=50, bucket 1,
  sharing the bucket with four genuine P=33 positives), 10/12 @45 (errors
  s=0,s=4: phantoms with the (1,50) signature, P=50, eff=0). Ceilings:
  bucket coarseness @15, train-tail coverage @45.
- IVWC-CASEBIAS: V-CONDC 11/12 @15 (train cell (1,50) is 4/4 genuine, so
  s=3's train-fit bias moves the wrong way); V-AGREE/V-STRUCT 10/12 @15
  (features constant across train; degenerate to global bias reduction,
  breaking s=0); sealed-label oracle 10/12 @15.
- New observation from the committed @15/@45 sealed tables (this prereg):
  s=0 @15 (bkt=2, P=40, eff=0) is ALSO phantom-driven (g=2, 0 collected)
  but UCB catches it via bias_2=27; it sits EXACTLY at the bar
  (adjV=13=TV). The @45 errors are phantom-type, not just tail-coverage.

## What is built

`src/ivwc_casebias_retry.zag` (single file, pure Zag, pinned znc).
World/belief/composer/stepper/verifier/seeds copied verbatim from
IVWC-CASEBIAS (sealed (bucket, eff) pairs bit-identical; K3/K4 anchors).
New machinery:

1. **V-SENS (vv=1, learner).** For each case, fragility
   F = max_i (P - P_{-i}) over leave-one-out recompositions: for each
   gathered item i (via gather_cells on the committed plan), zero that
   cell's believed item, re-run learner_compose, record preff P_{-i}.
   Train-fit: residual_t = d_t - UCB_{bkt(t)}; bin F into {0, 1..25, >25};
   excess_bin = mean_bin - mean_global; bias_SENS(case) = UCB_b +
   excess_{bin(F)}. Mean-centering guarantees a constant-F world
   reproduces UCB exactly (no AGREE-style degenerate global shift).
   Shuffled twin V-SENSsh (vv=2): residuals rotated by 7.
2. **D-ORACLE-BIAS (fenced, SCORING only).** Harness counts nphantom(s):
   planned gathers at cells where the true world has no item (uses wseal;
   never learner-visible). B_orc = UCB_b + 40 if nphantom > 0 else UCB_b.
   Verdict (adjV_orc > TV_orc), TV_orc = mean adjV_orc. Tests whether a
   perfect phantom-conditioned bias succeeds under the mean bar.
3. **D-ORACLE-SH (fenced, SCORING only).** Same with the phantom indicator
   rotated by 7. Ablation: content vs procedure.

Anchors re-scored in-program: OF (P >= Tpred), X3 (frozen bucket table),
HYB, MG. Variant verdicts: adjV > TV (strict), TV = mean adjV per variant.

## Frozen kill bars

- **K1 (diet / commit order): PASS required.** A1: train COMMIT < PREFF <
  CONSEQ < sealed COMMIT < SCORING by source line order. A2: zero
  `world_buf`/`world_off` tokens in learner fns. A3: zero
  `expected|answer|key|target` (case-insensitive). A4: zero
  `correct|reference_plan|gold`. A5: `world_execute(` exactly 3
  occurrences (1 def + 2 call sites). A6: WC-FINAL = 60
  (24 train + 36 sealed). A7: zero `learner_`/`belief_` calls after the
  SCORING marker. A8: the token "oracle" (case-insensitive) appears only
  inside the fenced diagnostic block.
- **K2 (determinism): PASS required.** 3/3 runs byte-identical stdout.
- **K3 (anchor @15): PASS required.** acc_OF = 10, acc_X3 = 9.
- **K4 (anchor @45): PASS required.** acc_OF = 8, acc_X3 = 10.
- **K5 (12/12 @15 via case-level bias): predicted FAIL.** V-SENS does not
  reach 12/12 @15. (If it does, the information-bound thesis is wrong
  and the report says so loudly.)
- **K6 (V-SENS no harm @15): PASS required.** acc_SENS >= 11 (UCB level).
  The mean-centered residual design must not degenerate into a harmful
  global shift.
- **K7 (oracle cannot beat 11/12 @15 under mean bar): predicted TRUE.**
  D-ORACLE-BIAS @15 acc <= 11. Mechanism: fixing s=3 drops the
  transductive bar, flipping a boundary true-negative (predicted s=10).
- **K8 (V-SENS no harm @45): PASS required.** acc_SENS >= 10 (UCB level).
- **K9 (fragility audit): predicted TRUE.** s=3's F lies within the range
  of the four genuine positives' F, and train bin excess residuals are
  ≈ 0. (Printed FA lines.)
- **K10 (oracle improves @45 but not to 12): predicted TRUE.**
  D-ORACLE-BIAS @45 acc >= 11 (fixes the (1,50) phantoms s=0,s=4).

**BUILD-PASS requires K1,K2,K3,K4,K6,K8,K9 and K5.** K5 is predicted
FAIL, so the expected verdict is BUILD-FAIL with K7/K10 confirming the
structural (verdict, not estimator) characterization. A K5 PASS would be
a major surprise and would overturn the preregistered thesis.

## Determinism and honesty rules

- Integer arithmetic only. No researcher-set constants in any learner
  path (the +40 lives only in the fenced diagnostic).
- The fragility recomposition runs in COMMIT phases (beliefs only, zero
  world cost); K1 audits cover it.
- If V-SENS succeeds, report it as overturning. If D-ORACLE-BIAS reaches
  12/12 anywhere, report the mechanism precisely. No bar moves after
  seeing results.
