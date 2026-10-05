# REPORT -- NOISY C1512-C1530

Prereg `0c37e6e83`. Mechanism diagnostic only (STANDING RULE R4).
3/3 sha256 `e04b765c9dfb6197a7204cfdb7674e5b9be899d8206ab4f8cbfc9f5cabb8120b`
R3 lint: CLEAN.

## TWO MORE SELF-CAUGHT DEFECTS

**Noise generator inverted.** First run printed
`realized_corrupt=64` at nominal e=0.15: every label corrupted.
Cause: `u = z/2147483647` is always 0 because `z` never reaches the
modulus, so `u<150` was always true. Fixed to `z mod 1000`.

Caught only because the prereg required printing **realized**
corruption counts, never nominal ones. Nominal would have looked
fine.

**M12 was a misleading bar.** My reversal metric printed
`truth_rank_under_inverted_labels=1`, which by my own prereg
annotation means "the orderer is immune to reversal". That is
false. Inverting labels makes the truth and its complement
(XNOR of the same pair) score identically, so rank 1 was a
tie-break artifact. I rewrote the metric to report the tie.

This is the R3 failure mode again, in a new costume: a bar whose
name and annotation implied a strong claim, computed by a method
that could not support it. Lint cannot catch this one; only
reading the number against the mechanism catches it.

## PREREG PREDICTIONS vs OUTCOMES

| | Prediction | Measured | Verdict |
|---|---|---|---|
| P1 | noise separates true from wrong | true 53, wrong max 37 | **CONFIRMED** |
| P2 | noise does NOT order wrong vs wrong | wrong spread 12 (e=150), 16 (e=350) | **FALSIFIED** |
| P3 | gate family is genuinely graded | spread 48 clean, 38 noisy | **CONFIRMED** |
| P4 | graded gain is entirely argmax | DESC=1, argmax IS target, FO=1 | **CONFIRMED** |

## P2 FALSIFIED, AND WHY IT MATTERS

```
F1 phaseA e=0    true=64  wrong 32..32  spread=0
F1 phaseA e=150  true=53  wrong 25..37  spread=12
F1 phaseA e=350  true=42  wrong 22..38  spread=16
```

My prediction was that wrong parities stay tied at 32 under
noise. They do not. The **expected** score is still identical for
all wrong parities, but for a single realized noise draw they
differ, because each wrong parity's agreement with the specific
flipped rows differs.

So noise produces an *apparent* within-wrong gradient that is
pure sampling variance. It looks learnable and is not.

The decisive evidence that it is variance and not signal:

```
M9 FO_trials = 1        (same labels, no log, no class tags)
M11 cross_realization: order_from_draw_555_on_draw_666 = 1
```

Facts-only rebuilds the same ordering for free and gets the same
answer. A gradient that FO reproduces exactly from the same
labels carries no ownership.

The cross-realization result needs care: the ordering does
transfer (1 trial on a fresh noise draw). But that is a property
of the true function outranking its competitors in expectation,
not of anything learned. It would transfer identically for a
learner that learned nothing.

## THE GRADED FAMILY, AND WHY IT BUYS NOTHING

```
F2 phaseB e=0    true=64  wrong 0..48  spread=48
F2 phaseB e=150  true=57  wrong 7..45  spread=38
M6 DESC_SCORE=1  ENUM=38  RANDOM=42
M7 argmax_id=37  ARGMAX_IS_TARGET=1
M8 argmax_first_trials=1
M9 FO_trials=1
```

The gate family really is graded: XNOR of the true pair is the
exact complement and scores 0, monotone gates land in between,
so wrong candidates genuinely differ.

Descending-score order solves it in 1 trial. But that is
*entirely* argmax: `argmax_first_trials=1`. And FO gets 1 too.

So the whole apparent advantage of a learned proposal order on
an informative-gradient family reduces to "try the best-scoring
candidate first", which is **ranking** — an ability TNN already
demonstrates at L2.

## GRADIENT REVERSAL

```
M12 truth_score=7  top_score=57  n_at_top=2  truth_unique_at_top=0
```

Under inverted labels the truth collapses from 57 to 7, and the
complement ties at the top. There is no residual robustness at
all: the ordering is entirely gradient-dependent. Reverse the
signal and the orderer confidently proposes the complement.

## VERDICT

```
B7_argmax_is_target=1
B9_beyond_argmax=0  fo_matched=1  PROMOTION=0
B10_L3=0
B11 NOISE_BUYS_THRESHOLD_NOT_ORDERING;GRADED_GAIN_IS_ARGMAX;PROPGEN_CLOSED
```

**Noise buys a threshold, not an ordering. The graded-family gain
is argmax. FO matches exactly. L3=0. PROPGEN closed.**

Per the prereg stopping rule, no further proposal-learning
experiment runs in parity worlds or noisy variants.

## WHAT WAS ACTUALLY ESTABLISHED

1. Parity worlds have no gradient, and no noise level fixes that,
   because expected score is flat across all wrong parities.
2. Noise creates realized variance that mimics a gradient. It is
   fully reproducible by facts-only, so it is not ownership.
3. When a genuinely graded family is supplied, the entire win is
   argmax, which is L2 ranking, already held.
4. Proposal ordering has no robustness: gradient reversal flips it
   completely.

The frontier implication is that **"learn a better search order"
is not a viable route to L3**, in any of these worlds, for a reason
that is now measured rather than guessed. Ranking is already
owned; ordering on top of ranking adds nothing that survives
facts-only or reversal.

## THE REAL TARGET, RESTATED

The judge's framing is the correct one and this lane sharpens it:
the missing capability is not choosing among candidates the
researcher generated. It is **changing what gets generated, and how,
in a way that survives facts-only rebuild and gradient reversal.**

That is the BORROW program's target, and the flagship test for it
is bridge-free recruitment: can a structure learned in one
functional context be used in another with no bridge written for
that pair of roles?