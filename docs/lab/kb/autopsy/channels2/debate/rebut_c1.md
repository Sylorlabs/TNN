# REBUTTAL — Debater C1 (pro stimulus-analytic verification)

## 1. The strongest attack on C1, steelmanned — and my answer

The sharpest hit comes from the red team (§2a), backed by C2: **the band
arithmetic is a fixture-distribution problem, not a judgment-side problem.**
The adversary samples q from a band of half-width δ ≲ σ. My analytic is a
new estimator with its own noise σ′. If σ′ ≳ δ, I hit the same wall — and
nothing about being "stimulus-side" exempts me, because the band is a
property of the fixtures, which I face too.

Steelmanned fairly: "the information is sitting in the frozen bytes" is true
in the trivial sense that the bytes determine q (the generator built them
from it). Extractability-by-procedure is the actual claim, and I haven't
measured it. My whole advantage over the judgment-side family is not a
theorem — it's the contingent fact that the frozen adversary never modeled
my analytic. Against the next threat model, that shield evaporates, and I'm
just another estimator the adversary can target. C2's σ′ framing is the
same knife: I assumed direct = better; I have shown no σ′ < σ.

My answer:

- The attack demotes my claim from theorem to hypothesis — it does not kill
  it. DPI says the judgment-side family *cannot* recover I(q;Y|J), full
  stop. The σ′ argument says C1 *must be built well*. A build requirement
  is not a death sentence. The judgment-side position faces a theorem; C1
  faces an engineering gate. Those are not symmetric situations.
- The σ′ advantage is not hand-waving: the adversary's generator is known —
  Native characterized gen.py. A perceptual sense has large σ because it is
  a generic classifier with boundary quirks; an analytic *inverts a known
  forward model* (band analysis of a generated tone, edge geometry of a
  generated shape). Inversion of a known generator is a structurally easier
  estimation problem than classification by an unmodeled black box — σ′ ≪ σ
  is plausible by construction, not by luck.
- The trust regress stops at the oracle. If generator logs contain true q
  per fixture (the red team's own §2b raises this), C1 validates directly
  and the "who verifies the verifier" worry dissolves — an analytic anchored
  to ground truth is not "a second correlatable judge," it's a calibrated
  instrument.
- The red team's stand-down demand — a stated oracle and a σ′ ≪ δ
  demonstration gate before resources move — is exactly the prereg C1 should
  carry. I accept it. That is not a retreat; it is my own falsifier (§3.3)
  with teeth added by the skeptic.

So the strongest attack lands — and converts C1 into a gated build, which
is what my paper proposed, not an all-in bet.

## 2. The weakest point in my own paper, stated honestly

I asserted independence I haven't measured. My §1.3 says an analytic
"measures q through a mechanism the adversary never modeled and **cannot
have correlated**." The "cannot have correlated" is doing unlicensed work.
Two deterministic functions of the same adversarial bytes, written by authors
who have read the generator, can be correlated — and I have no
residual-error-correlation metric, no measured σ′, and no demonstration that
my six analytics aren't (a)+(c) with extra steps. I also dismissed J's "who
verifies the verifier" too quickly: a human-authored analytic calibrated
post hoc on the 2020 frozen fixtures can overfit exactly where it matters,
and the program will have no instrument to notice (red team §2d). My
falsifier #3 admitted the thesis could fail on the frozen bytes, but the
paper's rhetoric — "the one move," "permanently this time" — didn't behave
like it believed its own falsifier. It should have.

## 3. Concede / hold

**Concede:** my §2 prediction assumed F2 reads cleanly. It doesn't. The red
team's §§1b/1e show F2 measures estimator-covariance under T, and a smooth
deterministic sense can clear ≥0.70 regardless of whether the boundary error
is "noise-driven" or "systematic" in the sense the conclusion needs. So I
retract the framing that "C2 will cleanly confirm noise-driven error and
leave C1 as the only remaining direction." An F2 fire buys
estimator-covariance, not a verdict — the covariance-calibration control
(orthogonal-perturbation baseline) has to run before anyone reads it as
systematicity, let alone as grounds for a permanent family retirement. This
does not touch my DPI argument. F2 was never my load-bearing instrument; it
was a courtesy instrument for deciding C1's design (different measurement
principle vs. second reading).

**Hold:** the exhaustion thesis. Nothing in J or the red team moves DPI: no
function of the judgment stream recovers the residual J destroyed, and the
shootout's 0.1483-bit cap is a measurement of that, not a theory. J's
"looser band" defense fails the red team's own §3a test — a band loose
enough for judgment-side channels to add bits is loose enough for the raw
judgment to resolve, making the channel unnecessary. The family dies on the
theorem, not on F2. C1 stays the only direction that adds a new observation;
the open question is only whether the stimulus side can be built to beat the
band — and that question has an experimental answer.

## 4. Do I still hold my four falsification terms? Yes — with one tightening

1. **C2 deploys** (beats 0.15 bits, false-install < 0.15, both senses,
   byte-identical 2× reruns): hold — but after the red team's runner-up
   scenario, a deploy verdict gets checked against **in-band stratification**
   (|q − b| ≲ δ) before I treat it as a genuine channel rather than
   band-tail leakage wearing one. Bars as written; the stratification
   decides what the bars measured.
2. **Honest C3 re-test > 0.3 bits** with false-install < 0.15: hold,
   unmodified. The 0.0110-bit (b) number stays retracted either way.
3. **A prereg-disciplined C1 analytic can't beat 0.15 bits on the frozen
   bytes**: hold, unmodified — this is my load-bearing falsifier, and the
   σ′ ≪ δ gate makes it measurable instead of hand-wavy.
4. **Any future preregistered judgment-side channel beats 0.30 bits** with
   false-install < 0.10: hold, unmodified. The exhaustion thesis was always
   a claim about the cap, not about my cleverness.

**Bottom line:** the skepticism raised my position's price — a stated
oracle, a measured σ′ ≪ δ gate, law validation before voiding, no
overfitting the frozen set — but didn't touch its core. The judgment-side
family is dead by theorem; the only live question is whether the stimulus
side can be built well enough to beat the band. Build it to the gate, and
let the measurement say.
