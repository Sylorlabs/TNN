# PREREG.md -- IVWC-SCOREBIAS: score-side bias-estimator improvements

Frozen: 2026-10-03. This prereg is committed alone before any
implementation. The implementation commit must strictly follow it
(K1 commit-order self-check).

## 1. Question

IVWC-PERBUCKET closed the bar-boundary line: the margin variant
ties the per-regime winners (10/12 = OF @wp15, 10/12 = X3 @wp45)
and the remaining errors are structural SCORE errors, not bar
artifacts: s=0 confident optimism (adj=25) and s=3 phantom items
(adj=46) @wp15; s=0/s=4 confident optimism (adj=46) @wp45.
"Strict-dominance ceiling is set by the scores, not the bars."

This wave tests SCORE-side improvements to the hybrid's bias
estimates: does a better bias estimator achieve strict dominance,
i.e. HYB' > OF @wp15 AND HYB' > X3 @wp45?

## 2. What the bias estimate is (honest description)

The hybrid's bias is per-bucket mean overconfidence learned from
24 train cases at wp=15: for train case t, d_t = preff_tr[t] -
teff[t] (predicted eff minus true eff, percentage points);
bias[b] = floor(mean of d_t over train cases in bucket b),
trained values (0, 4, 15, 16). The sealed adjusted score is
C = P - bias[bkt]; verdict PASS iff C > T (strict margin,
inherited from the MG variant; T = mean C over the sealed
batch, learner-computed, no world data).

Why the mean fails here: the residual errors are TAIL events.
Bucket 1's train overconfidence is {0,0,0,0,0,0,33}: six exact
cases and one 33-point miss. The mean (4) prices none of the
tail risk, so phantom/confident-optimism cases (d ~= 46) sail
over the bar. Under law change (wp=15 -> 45) the overconfidence
distribution shifts up and the stale mean undercorrects
systematically.

## 3. Frozen bias-estimator variants (all computed from the 24
## train cases only; no sealed data; no researcher-set constant
## except the declared 1/2 shrinkage factor)

Let m_b = bias[b] (integer mean, as trained), n_b = train count
in bucket b, gbias = floor(global mean of d_t) = 7.

- V-SHR0 (shrinkage to zero): B0[b] = m_b / 2. The textbook
  recommendation: with n_b in {7,7,7,3}, raw means overfit
  sampling noise; shrinkage trades bias for variance.
- V-SHRG (shrinkage to global mean): BG[b] = (m_b + gbias) / 2.
  Partial pooling: bucket 0 (m=0) is pulled up, bucket 3
  (m=16, n=3) is pulled toward the global mean.
- V-MAX (worst-case / tail bias): BM[b] = max_{t in b} d_t.
  The largest overconfidence the bucket exhibited in training.
  Law-change-robust in the precise sense: it prices the observed
  tail, which is the direction the wp=15 -> 45 shift moves.
- V-UCB (uncertainty-adjusted): BU[b] = m_b + isqrt(S_b/(n_b-1))
  for n_b > 1 else m_b, where S_b = sum_{t in b} (d_t - m_b)^2
  and isqrt is integer floor sqrt. A one-sided uncertainty
  hedge: with tiny n_b the mean may underestimate the true
  bucket overconfidence; UCB corrects in the failure direction
  without the full aggression of the max.

Trained values (hand-derived from the published train T-lines,
which are learner-visible; the program recomputes them):
SHR0 = (0,2,7,8); SHRG = (3,5,11,11); MAX = (0,33,33,20);
UCB = (0,16,27,20).

Each variant's sealed rule: adjV[s] = preff[s] - BV[bkt[s]];
TV = mean adjV over the sealed batch; verdict = adjV > TV
(strict). Shuffled-bias ablations of all four (same rotate-by-7
consequence shuffle as IVWC-HYBRID) isolate consequence content.

In-program arms on one shared label ge = (eff >= Tpred):
OF, X3, HYB (original, >=), MG (margin, >), plus the four
variants and four shuffled ablations. World/belief/composer/
stepper/verifier/seeds are verbatim copies of IVWC-HYBRID, so
K3/K4 anchors verify bit-identical sealed pairs.

The median was considered and rejected: train medians
(0,0,17,18) are nearly the mean (0,4,15,16); the action is in
the tail, which the median ignores by construction.

## 4. Frozen kill bars

- K1 (commit before signal / diet): in-program K1T/K1P/K1S
  STRUCT-PASS markers preserved from the hybrid; shell audits
  A1-A7 with the same frozen counts (world_execute( x3,
  WC-FINAL=60, zero expected/answer/correct/gold tokens).
- K2 (determinism): 3/3 byte-identical stdout (shell sha256).
- K3 (replication anchor, wp=15): acc_of=10 AND acc_x3=9.
- K4 (replication anchor, wp=45): acc_of=8 AND acc_x3=10.
- K5 (STRICT DOMINANCE, headline): exists variant V in
  {SHR0,SHRG,MAX,UCB} with accV@15 > acc_of@15 AND
  accV@45 > acc_x3@45.
- K6 (@15 GAIN): exists V with accV@15 > 10.
- K7 (@45 GAIN): exists V with accV@45 > 10.
- K8 (consequence-content): V* = argmax_V accV@15 (tie-break
  order UCB, MAX, SHR0, SHRG, declared); accV*sh@15 <
  accV*@15 strictly.
- K9 (non-degenerate, wp=15): accV*@15 > maj@15.
- K10 (MAX self-defeat, mechanism): accMAX@15 < acc_of@15.
  Rationale: worst-case bias overcorrects the genuine positives
  while the transductive mean bar chases the correction down,
  leaving the phantom (largest P) still on top.

## 5. Frozen mechanism predictions (derived pre-implementation
## from the published per-case error sets; the sealed V-lines of
## the hybrid run were NOT read)

- V-UCB @15: 11/12. bias_2 = 27 >= 20 pulls s=0 (P=40) to
  adj=13, exactly the bar (T=13), flipped to FAIL by the
  strict margin; all other verdicts hold (bucket-1 positives
  keep margin 4 above the bar).
- V-UCB @45: 10/12 (ties X3). s=0/s=4 (P=50, bkt=1) need
  bias_1 > 44 to flip; the train tail only supports 33, so
  the UCB-corrected adj=34 stays far above the bar.
- V-MAX @15: 5/12. Overcorrection flips the four genuine
  bucket-1 positives to FAIL; the bar drops to 4 and the
  phantom s=3 (adj=17) still passes. Self-defeating.
- V-MAX @45: 9/12 (adds s=5 to the error set).
- V-SHR0 @15: 10/12 (= OF). V-SHRG @15: 10/12 (= OF).
  Shrinkage moves the wrong way for confident-optimism
  errors: it preserves both structural FPs.
- V-SHR0 @45: 9/12. V-SHRG @45: 9/12.
- K5: FAIL (no variant clears both regimes; UCB gains @15
  but ties @45). K6: PASS (UCB 11/12 @15). K7: FAIL.
  K8: PASS (shuffled UCB collapses). K9: PASS (11 > 7).
  K10: PASS (5 < 10).

Predicted scoreboard. wp=15: UCB 11, SHR0 10, SHRG 10, MAX 5
vs OF 10, X3 9, MG 10. wp=45: UCB 10, SHR0 9, SHRG 9, MAX 9
vs OF 8, X3 10, MG 10.

## 6. Verdict rule

BUILD-PASS requires K5 (strict dominance). Predicted verdict:
BUILD-FAIL (K5 and K7 fail), with K6 passing as a documented
partial gain: better bias strictly improves the hybrid
in-distribution but does not dominate under law change. If the
run contradicts the predictions, the verdict follows the frozen
bars, not the predictions.

## 7. Scope limits (inherited)

One wall-density law-change axis; item law, belief noise, energy
budget fixed. Bars computed over the sealed batch (transductive)
from predictions + learned biases only; no world data enters any
bar. 12 sealed cases per regime. Consequence-training diet: 24
true train outcomes at wp=15, declared here not hidden. Mechanism
test, not a composition-novelty or L3 claim; the composer is
fixed.

## 8. Frozen audits

A1: train COMMIT/PREFF call sites precede train CONSEQ
world_execute; sealed COMMIT precedes SCORING world_execute.
A2: zero world_buf/world_off tokens in the LEARNER section.
A3: zero expected/answer/key/target tokens (case-insensitive).
A4: zero correct/reference_plan/gold tokens.
A5: sha256 equality across runs/ivwc_scorebias-run{1,2,3}.txt.
A6: world_execute( count = 3 (def + 2 call sites);
WC-FINAL=60 (24 train + 36 sealed).
A7: zero learner_* calls after the sealed COMMIT phase.
No post-prereg probe of any kind; the hybrid's committed
per-case sealed run outputs were not read pre-prereg (only the
published REPORT.md per-case details, which are task context,
and the train T-lines, which are learner-visible).
