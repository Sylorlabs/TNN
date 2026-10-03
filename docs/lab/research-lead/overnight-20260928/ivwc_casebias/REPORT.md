# IVWC-CASEBIAS -- Report

**Wave:** case-level (not bucket-level) bias signals for phantom-type errors (follow-up #1 from IVWC-SCOREBIAS).
**Verdict: BUILD-FAIL** -- K5 FAIL (no case-level variant reaches 12/12 @15); K6 FAIL additionally (two case-level variants harm @15 relative to UCB).
**Date:** 2026-10-03. Pure Zag, safebin, 3/3 byte-identical runs. Commits local on `tnn-native-lab`, never pushed.

## 1. Results

Accuracy = fraction of 12 sealed cases where the variant verdict matches the shared label `ge = (eff >= T_pred)`.

| variant | @15 (wp=15) | @30 (wp=30, exploratory) | @45 (wp=45) |
|---|---|---|---|
| V-UCB vv=0 (anchor) | **11** | 9 | 10 |
| V-CONDC vv=1 (bucket,preff) | 11 | 10 | 10 |
| V-AGREE vv=2 (agreement) | 10 | 9 | 10 |
| V-STRUCT vv=3 (bucket,bumps) | 10 | 8 | 10 |
| V-CONDCsh vv=4 | 4 | 4 | 5 |
| V-AGREEsh vv=5 | 10 | 9 | 10 |
| V-STRUCTsh vv=6 | 4 | 4 | 5 |
| anchors OF / X3 / HYB / MG | 10 / 9 / 9 / 10 | 8 / 9 / 8 / 8 | 8 / 10 / 9 / 10 |
| harness sealed-label diagnostic | 10 | 7 | 12 |

Error sets: @15 UCB and CONDC both err only on {s=3}; AGREE and STRUCT err on {s=0, s=3}. @45 every variant errs on {s=0, s=4} (both bkt=1, preff=50, eff=0 phantoms).

## 2. Kill-bar adjudication

- **K1 PASS** -- diet/commit-order audits A1-A8 all pass (details section 6). Phase order verified by source line numbers (train COMMIT 690 < PREFF 725 < CONSEQ 757 < sealed COMMIT 1112 < SCORING 1269). `world_execute(` appears exactly 3x; WC-FINAL=60. No learner calls after SCORING.
- **K2 PASS** -- 3/3 runs byte-identical (sha256 `fc7edca7e93442946cbe50f77347edd31fa87b1ed9b2e0687e74c3f2a114bd64`).
- **K3 PASS** -- acc_of=10, acc_x3=9 @15 (anchors reproduce scorebias exactly).
- **K4 PASS** -- acc_of=8, acc_x3=10 @45 (anchors reproduce scorebias exactly).
- **K5 FAIL** -- no case-level variant reaches 12/12 @15. Best is V-CONDC at 11/12, tied with UCB.
- **K6 FAIL** -- V-AGREE and V-STRUCT score 10/12 @15, below UCB's 11. Case-level variants HARM @15. (Prereg predicted PASS; the miss is in the FAIL direction and reinforces the verdict.)
- **K7 FAIL** -- no variant exceeds 10/12 @45 (all tie UCB at 10).
- **K8 PASS** -- all case-level variants >= 10 @45.
- **K9 PASS** -- in-program check: exactly 4 train cases have (bkt=1, preff=50), and all 4 have d=0. The mechanism fact is confirmed inside the binary, not just in analysis.
- **K10 PASS** -- harness sealed-label per-(bucket,preff)-cell bias @15 scores 10/12, does not beat 11.

BUILD-PASS required K1,K2,K3,K4,K9 plus K5/K6/K8; K5 and K6 fail. **BUILD-FAIL.**

## 3. Why V-CONDC cannot fix s=3: the train diet protects the phantom

V-CONDC is the sharpest possible test of the case-level idea: it conditions on the exact (bucket, preff) cell, the finest learner-visible signature available. Result: 11/12 @15 with the identical error set {s=3} as UCB.

The mechanism, from the in-program residual table (R1 lines):
- Train cell (bkt=1, preff=50): 4 cases (t=3,9,10,13), all genuine, all d=0. Mean residual vs UCB = -16.
- s=3's bias under V-CONDC = UCB_1 + (-16) = 16 - 16 = 0. Its adjusted score RISES from 34 to 50; the variant bar TV becomes 14; s=3 (ge=0) still verdicts PASS. Wrong.
- The four genuine (bkt=1,preff=33) positives keep bias = 16 + 0 = 16 (cell resid 0), adjV=17 > 14, still correct.

So the train-fit case-level bias does not merely fail to fix s=3 -- it moves s=3's score in the WRONG direction, because the train diet says the (1,50) signature is perfectly safe. **Any bias function trained on this diet must treat s=3's exact signature as genuine.** The failure is not overfitting noise; it is the diet's base rate, confirmed by K9 inside the program. A future phantom wearing the (1,50) signature would be protected the same way. This is underfitting-the-phantom by construction of the diet, and it is robust to the centering choice (residual-on-mean would give bias(s=3) = 4 + (-4) = 0, same conclusion).

## 4. Why V-AGREE and V-STRUCT harm @15: feature degeneracy

Both variants score 10/12 @15, breaking s=0 (a case UCB gets right) while still missing s=3. The root cause is not subtle -- the candidate case-level features are **constant across the entire train set**:

- **Agreement:** all 24 train cases agree 3/3 across the three composer paths (R2: a=1 cnt=0, a=2 cnt=0, a=3 cnt=24). The single populated cell's mean residual vs UCB is -7, so V-AGREE = UCB - 7 uniformly: a global bias reduction, not a case-level signal. s=0's bias drops 27 -> 20, its adjV rises 13 -> 20 > TV=19, flipping it to a wrong PASS. Errors {s=0, s=3}.
- **Believed bumps:** all 24 train cases have bumps=0 from the internal simulation (R3: bb=1 and bb=2 have cnt=0 in every bucket). V-STRUCT = UCB minus per-bucket constants {0,-11,-12,-3}. s=0's bias drops 27 -> 15, adjV = 40-15 = 25 > TV=20, wrong PASS. Errors {s=0, s=3}.

The shuffled twins confirm the tables carry real train signal (not noise): V-CONDCsh = 4/12 and V-STRUCTsh = 4/12 @15 -- shuffling destroys them. V-AGREEsh = V-AGREE = 10/12 because a single global cell's shuffle is the identity. The honest reading: multi-policy agreement and internal-simulation friction are computable from the learner's own state (the machinery works -- three composer paths run, rev and nn plans are produced), but they carry **zero case-level information** in this world. All three policies see the same believed item, so they agree; the internal simulation runs on the belief, so it never sees the true world's friction.

## 5. Feature audit: nothing the learner can see separates phantoms from genuine positives

Per-case TA lines (train, learner-visible features only):

Bucket-1 train cases -- phantom t=17 (P=33, d=33, L=3, bumps=0, walls=7, items=8, agree=3) vs six genuine cases (P in {33,50,100}, L in {1,2,3}, walls in {4,5,6,7}, items in {2,4,6,7}, all bumps=0, agree=3). Every feature value of the train phantom falls inside or adjacent to the genuine ranges.

s=3's sealed feature values (P=50, L=2, bumps=0, walls=5, items=4, agree=3) all fall **inside** the train-genuine ranges: P=50 matches t=3,9,10,13; L=2 matches t=3,9,10,13; walls=5 matches t=13; items=4 matches t=5,6.

**No learner-visible feature separates the train phantom from train genuine cases, and s=3 is feature-identical to genuine train cases.** This is the expected consequence of the generative process: the phantom arises from independent belief noise (the belief doesn't know it's wrong), which leaves no observable trace in beliefs, plans, internal simulations, or policy agreement. The audit verifies empirically what the generator design implies.

## 6. Oracle diagnostic: even perfect case-level knowledge cannot beat 11/12

The harness-side sealed-label per-(bucket,preff)-cell bias (fenced in SCORING, never learner-visible) scores 10/12 @15: adjO = {0,0,33,0,33,33,20,33,0,33,25,13}, bar=18. It fixes s=3 (cell (1,50) sealed resid is large) but breaks s=6 and s=10, whose cells' sealed means pull them across the shifted bar. K10 PASS.

This is the strongest statement of the wave: **even with sealed truth, per-(bucket,preff)-cell bias cannot beat UCB's 11/12 @15 under the transductive mean-bar verdict.** The ceiling is not an estimator problem -- it is structural to (train-fit cell tables) x (mean-bar verdict). At @45 the diagnostic reaches 12/12, but only because the label skew (11/12 FAIL) makes the bar trivially low; no learner variant approaches this.

## 7. @45: case-level machinery changes nothing

All seven variants score 10/12 @45 with the identical error set {s=0, s=4} -- both (bkt=1, preff=50, eff=0) phantoms wearing the diet-protected signature (R1[1][50] = -16 gives them bias 0 under V-CONDC, adjV=50). The @45 ceiling remains train-tail coverage (need bias_1 > 44; train tail caps at 33), exactly as scorebias diagnosed. Case-level features add nothing where the binding constraint is tail coverage.

Exploratory (unscored shift @30): V-CONDC = 10 vs UCB = 9, fixing s=7 (bkt=2, preff=50, eff=25) by the strict margin (adjV=25 vs TV=25, not >). One case, one shift, no bar -- noted, not claimed.

## 8. Answers to the task's key questions

1. **What case-level features distinguish phantoms from genuine positives?** None available to the learner. Agreement is constant, bumps are constant, and L/walls/items/preff all overlap between the train phantom and genuine cases. The phantom-generating process is informationally invisible.
2. **Can the learner compute these features from its own internal state?** Yes -- the machinery works (three composer paths, internal simulation, belief census all run with zero world cost in COMMIT phases). The features are computable but carry no signal. Computability was never the bottleneck; information was.
3. **Does case-level bias generalize or overfit?** Neither, in the usual sense -- it **underfits the phantom by diet construction**. The (1,50) -> "safe" mapping is a true property of the train diet (4/4 genuine), so the variant correctly learns it and would misclassify any future phantom with that signature. Two of three variants additionally harm @15 through feature degeneracy (uniform bias reduction undoing UCB's conservatism on s=0).

## 9. What would be needed (not claimed, directions only)

The wave closes the case-level-bias line as formulated: no train-fit bias function of (bucket, preff, agreement, bumps, L, walls, items) can fix s=3, and the oracle diagnostic shows even sealed-label cell means can't beat 11/12 under this verdict structure. Three structurally different hypotheses for the phantom problem, in the order the evidence suggests trying them:
- H1: a signal correlated with belief-noise magnitude -- but the belief carries no uncertainty annotation, and all internal consistency checks (agreement, simulation) run on the belief itself, so they cannot see its wrongness. This hypothesis predicts continued failure; it is listed to be killed, not pursued.
- H2: a different verdict structure -- the transductive mean bar shifts under every variant (TV 13 -> 14 -> 19 -> 20 across vv=0..3 @15), which is what breaks s=0 under AGREE/STRUCT and s=6/s=10 under the oracle. A non-transductive or per-case-calibrated bar is a different family, not a better bias.
- H3: train diets that contain phantoms with the to-be-fixed signature -- but that is teaching the answer, and the wave's honest finding is that the DIET, not the estimator, is where the phantom's fate is decided.

## 10. Governance and audit log

- Prereg committed alone first (`0d0713ad`), implementation strictly after; lane `ivwc_casebias/`, explicit pathspecs, local commits only.
- Safebin active; `which python3 python` returns nothing; pinned znc `znc_linux_x86_64_abed8aa1`; no forbidden interpreter invoked.
- A1 phase order PASS (690 < 725 < 757 < 1112 < 1269). A2 0 world_buf/world_off tokens in learner fns. A3 0 expected/answer/key/target. A4 0 correct/reference_plan/gold. A5 3/3 byte-identical. A6 `world_execute(` count 3, WC-FINAL=60. A7 zero learner_/belief_/verifier_ calls after SCORING (line 1269); all call sites in COMMIT/PREFF phases. A8: the token "oracle" appears exactly twice, both inside the fenced HARNESS-ORACLE-DIAGNOSTIC block (lines 1361, 1365); zero before the SCORING marker.
- A8 self-correction, reported transparently: the first-assembled source contained "oracle" in two pre-SCORING comments ("expand3/oracle-free" at old line 1104; "K10: oracle ..." at old line 1527) -- my own wording slip, not an oracle leak (the line-1104 comment asserted the ABSENCE of oracle use). Both comments were reworded; the binary rebuilt byte-identical (sha256 unchanged), so the three runs stand as produced by the identical binary. The frozen audit was complied with, not moved.
- World/learner/verifier sections verified byte-identical to IVWC-SCOREBIAS (modulo the header comment); K3/K4 anchors reproduce scorebias exactly (OF 10/8, X3 9/10 @15/@45).

## 11. Bottom line

Case-level bias was the recommended fix for scorebias's structural ceiling #1. Tested three ways, it fails three ways: the fine-grained variant is diet-blocked (the phantom's signature is 4/4 genuine in train, K9-confirmed in-program), and the two novel-signal variants degenerate to uniform bias reduction because their features are constant across train (breaking s=0, K6 FAIL). The feature audit shows the phantom is informationally identical to genuine cases from the learner's view. The oracle diagnostic shows even sealed truth can't beat 11/12 @15 in this family. **The s=3 error is not an estimator problem and not a granularity problem -- it is a diet problem wearing an estimator's clothes.** The case-level line is closed; the score-side line stays closed with it.
