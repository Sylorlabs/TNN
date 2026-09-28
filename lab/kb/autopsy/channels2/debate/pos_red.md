# RED TEAM — pre-result attack paper on KB4 channels (C2 / C1 / judgment-side defense)

Role: skeptic. Target: every camp. Status: analysis only; no code, no trial runs.
Read against: `SYNTHESIS.md`, `PREREG_OUTLINE_TCP.md` (this directory).

The program is about to bet its direction on one experiment. C2's F2 bar does
not merely kill a channel — it permanently retires an entire family of
approaches and redirects all resources. A falsifier with program-wide,
irreversible consequences needs to be airtight. It is not. What follows is
every load-bearing weak point I can find, in plain language.

---

## 1. AGAINST C2 (the transform-consistency probe)

### 1a. F3 is the experiment's silent killer — and it tests the wrong thing

The calibration gate demands ≥95% transform-consistency on the 93 **primary**
(calibration) stimuli, per sense. If a sense fails, its results are VOID —
the channel is declared invalid, "not merely weak," and the experiment
"fails" without ever testing its hypothesis.

But the gate measures covariance on the **easy** items and the experiment
needs it on the **hard** ones. Primaries sit far from the decision boundary;
adversarial fixtures live within δ of it. Estimator behavior at the boundary
is routinely qualitatively different from behavior off it — thresholds,
rounding, tie-breaks, and saturation all bite exactly where the margin is
thin. A sense can be 99% covariant on primaries and 60% covariant on
adversarial items, for reasons that have nothing to do with the C2
hypothesis (see 1c). The gate certifies the wrong regime.

Worse, the gate **voids the sense instead of fixing the law**. Two entries in
the (T, L) table are law misspecifications waiting to happen:

- **t3 shapetrans, L = identity under h-flip.** Identity is only a valid law
  if the shapes are achiral. If any fixture shape is handed (chiral), h-flip
  changes the shape the sense sees, and J(T(stim)) == J(stim) is the *wrong*
  expectation. The gate will read this as "transform breaks the judge" and
  void the sense for t3 — punishing the channel for the prereg's own bad law.
- **t5 timbredisc, L = identity under time-reversal.** The prereg notes the
  stimulus is "a single 0.8 s tone," as if that settles it. It doesn't. A
  tone with an amplitude envelope (attack/decay) is not time-reversal
  symmetric, and any judge even mildly sensitive to envelope shape — onset
  detection, temporal weighting, a causal filter bank — will shift its
  judgment under reversal. Same for **t4 pitchdisc**: time-reversing a pitch
  *discrimination* pair reverses presentation order, and the law
  HIGHER↔LOWER handles the label swap, but any order effect in the judge
  (adaptation, forward masking, primacy in the comparison) breaks covariance
  for reasons unrelated to boundary systematicity.

The honest version of F3 would calibrate the law against the sense's own
behavior and allow law revision before voiding. As written, F3 is a
misspecification amplifier: bad (T, L) choices masquerade as "channel
invalid," and C2 dies in calibration without its hypothesis being touched.

### 1b. F2 commits a category error — it measures estimator-covariance and claims error-systematicity

F2's logic: if P(consistent | Y=0) ≥ 0.70 on test, the sense's boundary error
is *systematic, not noise-driven*, so no judgment-side channel can ever work,
so retire the whole family permanently and go all-in on C1.

That chain has a broken link. What F2 actually measures is whether a
**deterministic estimator is covariant under T near the boundary** — i.e.,
whether feeding transformed bytes through the same fixed function yields the
transformed label. The adversary never modeled T, true. But the sense doesn't
need the adversary's help to be T-covariant: the *same biased estimator* run
on transformed input produces transformed bias **by construction**. That is
estimator-covariance, and it is a property of the estimator's smoothness, not
a diagnosis of the error process.

Consider the two cases F2 claims to separate:

- **Noise-driven error, in Native's sense.** For a deterministic sense binary
  (byte-identical reruns are required), "measurement noise σ" has to live
  somewhere concrete: either genuine internal stochasticity, or extreme
  sensitivity to irrelevant byte details near the boundary — a deterministic
  but effectively chaotic estimator. In the chaotic case, T perturbs exactly
  those irrelevant details (mirror-axis rounding, reversed sample order
  through causal filters — see 1c), so consistency can *break* even though the
  error is "systematic" in the fixed-function-of-bytes sense. F2 then reads
  low consistency as "noise-driven, channels can work" — the opposite of the
  truth.
- **Systematic error.** A smooth, T-covariant estimator with a systematic
  boundary bias gives high consistency. F2 fires. But high consistency is
  equally produced by a covariant estimator whose errors are driven by
  byte-level chaos that happens to be T-symmetric (e.g., deterministic dither
  derived from content). The statistic cannot tell these apart.

So F2's ≥0.70 threshold does not measure what its conclusion claims. And its
conclusion is the strongest claim in the whole program: **permanent,
program-wide retirement** of the judgment-side family. A permanent verdict
demands a validated mapping from statistic to diagnosis. That mapping is
asserted, not derived, and 1c below shows concrete mechanisms that break it
in both directions. F2 as written can "prove" systematicity when it is really
measuring estimator-covariance — the exact confound the task brief flagged —
and the prereg contains no control to separate the two (no noise-perturbation
control arm, no non-task-covariant transform baseline to calibrate what
"covariance" means for this estimator).

### 1c. The transform is not free — T injects its own noise exactly where the items live

The C2 story treats T as a clean mathematical operation. It isn't; it's a
byte-level rewrite, and every adversarial fixture sits within δ of the
boundary, where judgments are maximally fragile:

- **h-flip on images:** the mirror axis lands mid-pixel or between pixels;
  row-mirroring changes byte layout, and any position-sensitive processing
  (convolution padding, edge handling, sub-pixel interpolation in a resize
  step) shifts the estimator's input in ways that are *not* the task quantity.
  Near the boundary, a one-LSB-class shift flips judgments.
- **time-reversal on PCM:** any causal processing in the sense (filters with
  state, onset detectors, running normalizers) is definitionally not
  time-symmetric. Reversal doesn't just transform the task quantity — it
  transforms the processing artifacts too.
- **frame-reversal on video:** same, plus any temporal smoothing or
  motion-energy computation with a causal window.

The consequence cuts both ways, which is what makes it dangerous rather than
merely noisy: transform artifacts can **break** consistency on adversarial
items (F1 fires, channel "adds nothing," program misreads a bad transform as
a dead hypothesis) or the estimator's smoothness can **preserve** consistency
through them (F2 fires, program misreads covariance as systematicity). The
calibration gate cannot catch this because it runs on primaries, where
margins are fat and artifacts don't flip anything (1a). The experiment is
calibrated in a regime where the confound is invisible and scored in the
regime where it dominates.

### 1d. Small denominators, thin per-class rows

P(consistent | Y=0) is conditioned on the sense being wrong on test
adversarial items — 92 fixtures, split across 6 classes and 2 senses. A
sense that is wrong on, say, 8 test items in a class gives an F2-relevant
estimate with enormous variance; the ≥0.70 threshold then fires or misses on
sampling luck. The prereg requires per-class rows reported, which is good
hygiene, but the **decision rule** (retire the family permanently) is written
at the aggregate level. A permanent program-wide verdict should not be
triggerable by a noisy conditional proportion on a thin slice. There is no
minimum-denominator guard and no uncertainty quantification on the F2
statistic.

### 1e. The dichotomy may be false

F2's branching assumes the error is either noise-driven (channels can work)
or systematic (only re-measurement can). A deterministic, near-boundary
chaotic estimator is neither in the usable sense: it is a fixed function of
bytes (so "systematic") whose behavior under perturbation is unpredictable
(so "noise-like"). For such an estimator, *neither* branch's prescription is
sound — judgment-side channels fail for a different reason than F2 names,
and C1-style re-measurement succeeds only if its σ′ ≪ δ (see 2a), which is
independent of everything F2 measured. If this is the actual regime, F2
delivers a confident wrong diagnosis with a permanent prescription attached.

---

## 2. AGAINST C1 (stimulus-analytic verification)

C1 is the consensus fallback — both investigators, both prior crews, and the
coordinator's branching logic all point at it. Consensus is not evidence.
Here are the attacks.

### 2a. The band math applies to the analytic measurer too

Native's characterization: the adversary samples the task quantity q from a
band of half-width δ ≲ σ around the boundary, where σ is the judge's
measurement noise. The ~0.15-bit cap is a property of the δ/σ ratio, not of
judgments per se. An analytic re-measurement of q from stimulus bytes is a
new estimator with its own noise σ′. **If σ′ ≳ δ, C1 hits the same wall**,
and nothing about being "stimulus-side" exempts it — the band is a property
of the fixture distribution, which C1 also faces.

C1's entire advantage, stated honestly, is one thing: *the frozen adversary
didn't target it.* That is a real advantage against a frozen threat model,
but it is not the principled escape from the information cap that the
SYNTHESIS language ("only stimulus re-measurement can repair it") implies.
C1 works iff someone can write an estimator with σ′ ≪ δ for these fixtures.
That is currently an unmeasured hope, not a result. Until σ′ is measured
against δ, "go all-in on C1" is a bet, and F2's firing would be used to
justify that bet on the basis of a confounded statistic (1b).

### 2b. Who writes the measurer — and where the regress stops

An analytic check is a human-authored (or crew-authored) estimator. Three
problems:

1. **Authorship is a trust bottleneck.** The program demands the sense be
   distrusted because an adversary shaped its inputs. The analytic measurer
   is written by people who have read the adversary's generator. Its
   correctness on the frozen fixtures is verifiable *post hoc* — but its
   generality is not, and every fix to it is another human judgment call
   about what the stimulus "really" contains. The program that set out to
   remove human judgment from the loop ends up with human judgment as the
   load-bearing component.
2. **The regress.** If the analytic check disagrees with the sense, what
   adjudicates? A second analytic check? The threat model is frozen, so the
   adversary can't adapt — but the *author* can overfit, consciously or not,
   to the 2020 frozen fixtures. The regress stops only at a ground-truth
   oracle with σ ≪ δ. Do the generator logs contain true q per fixture? If
   yes, C1 can be validated directly and much of this dissolves — but then
   say so in the prereg, because "analytic verification" without a stated
   oracle is just a new uncalibrated judge. If no, C1's "independence" is
   asserted, not anchored.
3. **Calibration discipline must apply to C1 too.** Both investigators
   demand calibration-before-test. A C1 prereg needs its own validity gate
   (does the analytic measurer recover q on primaries? on held-out
   generator-known fixtures?), its own falsifiers, and its own bar against
   overfitting the frozen set. The current program treats C1 as the safe
   harbor that needs no scrutiny because everything else failed. Safe harbors
   need the most scrutiny.

### 2c. The taxonomy collapses: the sense already observes stimulus bytes

"Stimulus-side" vs "judgment-side" is doing load-bearing work in the
program's reasoning, and it doesn't survive contact with the architecture.
The sense binaries *take raw stimulus bytes as input* — a_raw and b_percept
are already stimulus-side estimators. C1's "analytic check of the stimulus"
is not a new observation of an unobserved property; it is **a second
estimator on the same bytes**. If it succeeds, what succeeded is "a better
estimator with σ′ ≪ δ," full stop — and then the channel framing dissolves:
the honest conclusion is "fix the sense," not "add a channel." The program
should be clear about which claim it's testing, because they have different
costs: a better estimator *replaces* the judgment path; a channel
*supervises* it.

Relatedly, the data-processing argument cuts both ways. Native correctly
notes that no function of the judgment stream recovers I(q; Y | J). But an
analytic function of the *same adversarial bytes the adversary authored* is
not obviously outside the adversary's reach in principle — the bytes are the
adversary's artifact. C1's shield is only that the frozen adversary didn't
model it (2a). Against the *next* threat model both investigators flag (an
adaptive adversary), C1 has no principled advantage over a good channel —
both are estimators the adversary can target. The program's "C1 is the
long-term repair" story leans on a frozen-adversary assumption it doesn't
name.

### 2d. "Independent observation" is unmeasured

Sol's and Native's language — "independent observations of the stimulus's
underlying property," "a channel the adversary cannot correlate" — needs an
operational definition before C1 is declared the answer. Independence from
*what*? From the sense's estimator? Measured how — residual correlation of
errors on fixtures where truth is known? Without a metric, C1 risks being
(a)+(c) with extra steps: another correlated summary of the same adversarial
byte string, drinking the same band-tail leakage (Native's own accounting of
the 0.1483 bits), and the program will have no instrument to notice.

---

## 3. AGAINST THE JUDGMENT-SIDE DEFENSE ("the band could be looser")

The defense, as I understand it: the 0.15-bit cap is a property of this
adversary's δ/σ parameters; a looser band would let judgment-side channels
work; so the family shouldn't be retired on this evidence alone.

### 3a. The threat model is frozen — this is wishful thinking, not an empirical claim

The program froze the adversary. "A different adversary would let the
channel work" is a counterfactual about an experiment that wasn't run, and
it **proves too much**: if the band were loose enough for a judgment-side
channel to add bits, it would be loose enough for the raw judgment to resolve
— and then no channel is needed at all. The defense's success condition is
indistinguishable from the channel being unnecessary. An empirical defense
would name a band-width regime where the channel adds information the raw
judgment lacks *and* show a mechanism by which the channel exploits something
the adversary didn't constrain. No such mechanism has been stated — because
the adversary constrained J(stim) on these exact bytes, and any
judgment-side function of these bytes faces the same δ/σ arithmetic.

### 3b. The cap is measured, not hypothesized

Native's accounting is the defense's real problem: the 0.1483 bits are
decomposed into band-tail leakage (finite-width bands; fixtures whose q fell
outside the noise floor) plus the A/B noise-independence dividend, with the
SUSPECT gate's 20 resolved fixtures *all* colorconst. The cap isn't a theory
about what judgment-side channels could do — it's a measurement of what they
did, with the leakage sources identified. "The band could be looser" doesn't
rebut a measurement; at best it proposes a new experiment.

### 3c. The narrow valid core — conceded

One point for the defense, stated carefully: band-width δ/σ *is* a genuine
moderator variable, and a future program should parametrize channel
evaluations by it rather than treating "0.15 bits" as a universal constant.
But that is a proposal for the next prereg, not a defense of the
judgment-side family under this one. Under the frozen threat model, the
defense has no empirical leg to stand on.

---

## 4. THE SINGLE MOST LIKELY MISLEADING RESULT

**F2 fires spuriously via estimator-covariance, and the program permanently
retires the judgment-side family on a confounded reading.**

Mechanism: the sense is a deterministic binary. The (T, L) transforms are
genuinely task-covariant as mathematical operations. A smooth estimator run
on transformed bytes returns the transformed judgment — the same computation,
transformed input, transformed output — regardless of whether its boundary
errors are "noise-driven" or "systematic" in the sense F2's conclusion
needs. Near-boundary consistency then clears the ≥0.70 bar easily, F2 fires,
and the program records as law: *boundary error is systematic; no
judgment-side channel can ever work; all resources to C1.*

Why this is *misleading* rather than merely null: a null (F1) leaves the
program uncertain and pointed at C1 as "the only remaining direction" —
cautious language. An F2 misfire leaves the program *certain and wrong*:
it shuts a door permanently ("retire the whole judgment-side family
permanently," "record the retirement as law") on evidence that measured
estimator smoothness, not error systematicity. If the true regime is
noise-driven error with a covariant estimator — exactly the regime where
Native says channels *can* work — F2's firing destroys the program's ability
to discover that, by law.

Why it's the *most likely*: it requires no exotic failure. It requires only
that the sense be a reasonably smooth deterministic function — the default
expectation for these binaries — and that T be implemented without
boundary-flipping artifacts (the calibration gate selects for exactly this
on primaries). The prereg's own discipline (frozen deterministic binary,
byte-identical reruns, task-covariant T) *maximizes* the chance of high
consistency conditional on being wrong, independent of the error's nature.
The deck is stacked toward F2 firing.

**How the prereg guards against it:** it doesn't. There is no control arm
that separates estimator-covariance from error-systematicity — e.g., a
non-task-covariant perturbation baseline (consistency under pixel noise or a
task-orthogonal transform) that would calibrate what "consistent" means for
this estimator, or a stratification of the F2 statistic by band membership
(|q − b| vs δ) to check whether consistency is uniform across the band or
concentrated where the estimator is smooth. The ≥0.70 threshold is a bare
number with no uncertainty quantification and no minimum-denominator guard
(1d). The branching consequence it triggers is the most irreversible action
in the program, attached to the least validated inference.

**Runner-up misleading result** (less likely, partially guarded): C2 appears
to *deploy* — beats 0.15 bits with false-install < 0.15 — on the back of the
same band-tail leakage that inflated the shootout champion. If the 92-test
split contains out-of-band fixtures (q outside the noise floor), the probe's
verdicts correlate with Y through leakage, not through the transform
mechanism, and the program "scales the methodology" of a channel that adds
nothing. Guard status: the prereg requires per-class rows, which would show
the bits concentrated in the leaky class — partial guard. What's missing is
a preregistered requirement that the bit gain survive **in-band
stratification** (items with |q − b| ≲ δ only). Without it, a deploy verdict
can be leakage wearing a channel's clothes.

---

## What would make me stand down (falsifiers for the skeptic)

- A **covariance-calibration control**: report P(consistent | Y=0) under a
  task-orthogonal perturbation alongside the F2 statistic. If task-covariant
  T gives high consistency and orthogonal perturbation gives low
  consistency, the systematicity reading gains real support. If both give
  high consistency, F2 is measuring estimator smoothness — stand the
  retirement down.
- **In-band stratification** preregistered for F1 and F2: all statistics
  recomputed on fixtures with |q − b| ≲ δ. Leakage-driven results evaporate;
  mechanism-driven results survive.
- **Law validation before voiding**: F3 re-run with laws fit to the sense's
  own transformed-primary behavior; void only what still fails. Separates
  "transform breaks the judge" from "the prereg's law was wrong."
- **A stated oracle and σ′ budget for C1** before resources move: what is
  true q's source per fixture, and what σ′ ≪ δ demonstration gates the
  all-in decision.
- **Uncertainty on F2**: minimum denominator per reported cell and a
  confidence interval; no permanent program-wide verdict fires on a point
  estimate from a thin slice.

Absent these, my recommendation: run C2 as a *measurement*, not as a
*tribunal*. Take the numbers; do not let F2 execute the judgment-side family
on its current evidentiary basis.

— red team
