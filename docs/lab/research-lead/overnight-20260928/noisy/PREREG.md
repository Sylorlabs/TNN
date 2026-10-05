# PREREG -- NOISY C1512-C1530

Lane `ownership`. Mechanism diagnostic. Frozen before implementation.

## 0. WHY THIS IS ONLY A DIAGNOSTIC

Per STANDING RULE R4 and program review: a noisy-label success
must NOT become a method-ownership result. Demonstrating

```
researcher search architecture
+ researcher scoring scheme with richer signal
-> better ranking
```

is still L2. This lane exists to answer one narrow question and
then close:

> Once the environment contains an informative gradient, does
> proposal machinery exploit anything beyond argmax ranking?

## 1. FALSIFIABLE PREDICTION (stated before running)

Theory: for any wrong linear parity f over GF(2) and true parity g,
f and g disagree on exactly half the rows, so
P(f == g) = 1/2 regardless of f. Label noise applied to the
labels does not change that: every candidate is scored against
the *same* noisy labels, and a wrong parity's expected score
stays near its clean expected score, while the true parity's
score rises toward 1-e.

Therefore:

* **P1** Noise creates a TRUE-vs-WRONG separation (threshold),
  because the true parity's score is strictly higher.
* **P2** Noise does NOT create WRONG-vs-WRONG ordering, because
  all wrong parities still share expected score 1/2.

If P2 is FALSE, something is wrong with my reasoning or the
implementation, and that is more interesting than a pass.

**P3** In a structurally different family (2-input gates, which
include monotone gates), wrong candidates get genuinely graded
scores, because a monotone gate is not a parity and its
disagreement fraction is neither 0 nor 1/2.

**P4** On such a graded family, descending-score ordering will
find the answer in 1 trial if and only if the answer is the
unique argmax. Since it is, the entire advantage over random is
explained by argmax, which is ranking, i.e. already-held L2
ability.

So the predicted verdict is PROMOTION=0 **with a specific
reason**: noise buys a threshold, not an ordering; and in the
graded family the whole gain is argmax.

## 2. DESIGN

Phases: A target = XOR(0,2). B target = XOR(1,4). 64 rows, 6 bits.

Family F1 (train family, unchanged from C1491):
* 15 PAIR  = bit_i XOR bit_j
* 20 TERN  = bit_i XOR bit_j XOR bit_k
* total 35. All parities.

Family F2 (structurally new transfer family):
* 6 gates x 15 pairs = 90.
* gates: AND, OR, XOR, NAND, NOR, XNOR over (bit_i, bit_j).
* F2 contains monotone gates (AND, OR, NAND, NOR), which are
  not parities, so P3 should hold.

Noise: labels corrupted independently with probability
e = epermille/1000, using Park-Miller, fixed seed. Print the
REALIZED corrupted count, never the nominal.

Noise levels: e = 0, 150, 350.

## 3. MEASUREMENTS

M1 F1 clean phase A: realized score of true, min and max over
   wrong candidates. Predicted true=64, wrong all 32.
M2 F1 noisy e=150 phase A: true score, min/max wrong.
M3 F1 noisy e=350 phase A: true score, min/max wrong.
   -> tests P1 and P2.
M4 F2 clean phase B: score of true, min/max wrong, and
   WRONG_SPREAD = max_wrong - min_wrong. -> tests P3.
M5 F2 noisy e=150 phase B: same, plus WRONG_SPREAD.
M6 Trials to solve phase B in F2 under three orders:
   DESC_SCORE, ENUM (gate-major then pair-major), RANDOM.
M7 ARGMAX_IS_TARGET: whether the unique argmax under DESC_SCORE
   is the true candidate. If 1, DESC_SCORE's advantage is fully
   explained by trying argmax first.
M8 Trials under ARGMAX-FIRST (try only the top-1, then fall back
   to enum). Reported so the argmax contribution is explicit.
M9 FO: given B's noisy labels, no search log, no class tags, FO
   builds DESC_SCORE itself. Trials. Tests whether the ordering
   is facts-recoverable.
M10 Learned-from-F1 rule applied to F2: the only rule F1's
   experience supports is "the answer lies in the class with
   maximal score". In F2 there is no class split of that kind,
   since all 90 are one class. Print whether the F1 rule even
   applies.

## 4. BARS

B1  3/3 identical sha256
B2  realized noise counts printed for each e and phase
B3  F1 wrong-vs-wrong spread printed at each e
B4  F2 wrong-vs-wrong spread printed
B5  DESC_SCORE, ENUM, RANDOM trials printed for F2 phase B
B6  RANDOM validated against closed form N=90
B7  ARGMAX_IS_TARGET printed
B8  FO trials printed
B9  PROMOTION printed; set 1 only if DESC_SCORE beats ENUM by
    more than the argmax effect, AND FO cannot match DESC_SCORE.
    Expected 0.
B10 L3 printed as a value
B11 verdict string printed

## 5. STOPPING RULE

If PROMOTION=0 for the predicted reason (noise buys threshold
not ordering; graded-family gain is argmax), the PROPGEN
direction is CLOSED and no further proposal-learning experiment
runs in parity worlds or noisy variants thereof.

## 6. DISCIPLINE

Pure Zag. `_zag_print`. Watchdog 300s. 3/3.
No bar hardcoded in a label string; R3 lint must pass.
Every realized noise count printed, never nominal.
Closed-form checks before reporting.