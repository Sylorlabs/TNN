# DEBATER C1 — pro stimulus-analytic verification (stimulus-side repair)

Position: **C1 — re-measure the task quantity directly from the raw stimulus
bytes with an independent analytic procedure — is the real repair for the KB4
channel gap. C2 is at best a stopgap diagnostic, not a deployable channel.**

## 1. Steelman: why re-measuring the stimulus beats probing the same fooled judge

**The argument in one sentence:** the information we need is I(q;Y|J) — the
sub-boundary residual of the true task quantity given the judgment — and by
the data-processing inequality, no function of the judgment stream can
recover it, because J already threw it away.

Concretely:

1. **The judge's failure is information-theoretic, not motivational.** Native
   characterized the adversary from its own generator: a boundary-straddling
   stimulus author sampling q from a band of half-width δ ≲ the judge's
   measurement noise σ. Below the noise floor, the judgment's output carries
   ~zero bits about which side of the boundary q is on. The ~0.15 bits the
   champion squeezed are band-tail leakage (fixtures whose q happened to fall
   outside the noise floor) plus the A/B noise-independence dividend. That
   leakage is luck in the fixture draw, not a channel property — a tighter
   band drives it to zero.

2. **Every judgment-side channel drinks from the same poisoned well.** Sol
   put it plainly: these channels are "alternate summaries of the same
   adversarially generated judgment process, not independent observations of
   the stimulus's underlying property." Perturbation classes, multi-source
   agreement, transform consistency — all are functions of J. The shootout
   spent its budget proving this: 0.1483 bits from (a)+(c), with (a)+(c) ≈
   0.0695+0.0797 being sub-additive — both channels drink the same leakage.

3. **The information we need is still sitting in the frozen bytes.**
   Native's decisive finding: 2020 raw stimulus fixtures (`.img`/`.pcm`/`.vid`)
   exist frozen on this VM under a SHA256 manifest. The "no raw signal"
   constraint applied to the frozen KB4 *input tables*, not the VM. The
   stimulus bytes contain q by construction — the adversary *generated* the
   stimuli from q. An independent analytic procedure (band analysis on the PCM
   for pitchdisc, edge/geometry analysis on the .img for shape tasks, optical
   flow sign on the .vid for motiondir) measures q through a mechanism the
   adversary never modeled and cannot have correlated. This is the one move
   that adds a genuinely new observation of the underlying property, which is
   exactly what both investigators said the repair must be.

4. **C1 survives the threats that kill every judgment-side channel.**
   Confidence was not merely uninformative but *adversarially inverted* —
   high confidence predicts error, because the band conflates true margin with
   noise magnitude. Any future channel that smuggles a margin statistic out of
   the same noisy estimate inherits this. An independent analytic measurement
   derives its own margin from the bytes; the inversion doesn't transfer.
   And against the adaptive-adversary threat model both investigators scoped:
   an adversary would have to corrupt *two independent measurement principles*
   of the same physical quantity, which is strictly harder than fooling one
   judge twice.

5. **C2, at best, is a stopgap — and its own prereg admits it.** C2's channel
   signal is (J(stim), J(T(stim))): still two outputs of the same fooled
   judge. It adds information only insofar as the judge's error is
   transform-decorrelated noise — which is exactly the A/B noise-independence
   dividend the (a)+(c) champion already captured (~0.08 bits), sub-additive.
   There is no third source here. C2's real contribution is F2: the
   systematic-vs-noise diagnostic. That's a *measurement about the family*,
   not a deployable channel. Run it, read the verdict, then build C1.

## 2. Prediction: C2 fires F1 (bits kill) — with F4 close behind

I predict **F1 fires: I(verdict;Y) ≤ 0.15 bits on TEST**, and C2 dies on the
bits bar. My reasons:

- The channel verdict is a deterministic function of (J(stim), J(T(stim))).
  Under the δ≲σ construction, T permutes which side of the boundary the noise
  realization lands the two draws, but neither draw carries information about
  q beyond what J already carried. The transform-consistency verdict
  correlates with |q−b| versus noise magnitude — i.e., with *whether the judge
  is confident*, which we already proved is adversarially inverted. The
  channel will at best re-capture the same band-tail leakage the (a)+(c)
  champion found, and nothing new. No new independent observation → no new
  information. Bits land at or below the 0.1483 champion level.
- I predict **F4 will also be near or over the line** (false-install ≥ 0.15,
  or close): INSTALL-on-consistent is precisely the rule that false-installs
  when the judge is *consistently* fooled — and the boundary band exists to
  make the judge consistently fooled. Consistency is a property of the
  judge, not of correctness.
- I do **not** predict F2 fires strongly. The errors under δ≲σ are
  noise-driven by construction; transform-decorrelated noise gives
  P(consistent|Y=0) well under 0.70. F1-fires-without-F2 lands in the
  coordinator's "C1 is the only remaining direction" branch — which is my
  position's winning branch.
- F3 stays green (≥95% on primaries): the transforms are genuinely
  task-covariant for the listed tasks. A void on F3 would be a calibration
  artifact, not evidence for or against either family, and I'd disregard it
  as uninformative rather than claim it.

Net prediction: **C2 does not deploy. It serves as a diagnostic that
confirms noise-driven boundary error, and then the judgment-side family
retires on the bits bar — permanently this time.**

## 3. What would falsify my position

I will concede — specifically, in these terms, and no weaker:

1. **If C2 deploys (beats 0.15 bits, false-install < 0.15 on TEST, both
   senses, byte-identical 2× reruns):** I concede the judgment-side family
   had a live, deployable member for this threat model, and C1-class work
   becomes the defense-in-depth layer rather than the primary repair. I
   would still hold the adaptive-adversary caveat (a future adversary that
   models T needs its own red-team), but I would not claim C1 was the
   *necessary* repair. The kill bars are preregistered; I will read them as
   written.

2. **If the honest C3 re-test (true re-observation of the SAME adversarial
   stimulus under fresh noise — not the mismeasured (b)) recovers >0.3 bits
   with false-install < 0.15:** I concede the judgment stream was not
   exhausted and the family's core member was never actually tested. The
   0.0110-bit (b) result must be retracted as evidence either way — it
   measured a different stimulus, not re-observation.

3. **If an independent analytic C1 probe, built to the same prereg
   discipline (frozen inputs, calibration-before-test, no fitted
   thresholds), cannot beat 0.15 bits on the frozen bytes either:** then my
   claim that the missing information is *extractable* from the stimulus is
   falsified, and I concede Sol's fallback — human verification or a second
   physical sensor, with new data collection — is the real repair. Note the
   asymmetry: C1 failing kills *analytic* verification specifically, not the
   stimulus-side thesis; but I will not hide behind that. If the bytes won't
   yield q to an independent procedure, judgment-side is not thereby
   vindicated — the shootout's DPI argument still stands — we're just in a
   harder world than I claimed.

4. **If any future preregistered judgment-side channel beats 0.30 bits on
   the frozen adversarial split with false-install < 0.10:** the cap was
   methodological, not informational, and I concede the whole "exhausted"
   thesis.

What does NOT falsify me: F3 voiding a sense (calibration artifact), C2
landing between 0.10–0.15 bits ("close but killed" is still killed — the bar
is the bar), or an argument that C1 is "more expensive" (the bytes are
already frozen on the VM; no new collection needed).

## 4. Attack on the C2 and judgment-side positions

**On C2 — its weakest points:**

- **It conflates agreement with correctness.** INSTALL-iff-consistent is the
  rule "trust the judge when it agrees with itself." But the adversary's
  entire construction produces judges that are *wrong and self-consistent*.
  The F2 falsifier exists precisely because the prereg authors knew this —
  C2's own document admits that if P(consistent|Y=0) ≥ 0.70, the channel AND
  its whole family die. A channel whose prereg contains a clause for the
  entire family's execution is a diagnostic wearing a channel's clothes.
- **It has no new information source.** (J, J′) are two draws from one
  adversarial judgment process. The maximum it can ever add is the
  noise-independence dividend — ~0.08 bits, sub-additive with the rest, and
  driven by fixture luck (band tails), not by a mechanism that survives a
  tighter band. δ is an adversary parameter; nothing stops δ → 0.
- **The (T,L) law is a per-task frozen tax that buys fragility.** Six
  task-specific transform laws must hold for both senses on calibration
  primaries, or results void. Any law/judge mismatch burns a sense — and a
  future adaptive adversary just needs to model T, which is public and
  frozen, to correlate against the channel itself.
- **C2's ceiling is my floor.** Even if C2 deployed at, say, 0.2 bits, that
  is still ~20% of the ~1 bit needed, while a direct analytic measurement of
  q from the bytes has the full bit in principle. C2 can never close the gap
  it is being asked to close; it can only shave the last judgment-side
  sliver off it.

**On the judgment-side family — its weakest points:**

- **Sol's premise was factually wrong, and the expensive program was built on
  it.** "The current corpus has no raw signal" — checked, wrong: 2020
  manifest-verified fixture bytes on this VM. The human-verification and
  second-sensor proposals were the correct *fallback*, not the first move,
  and they were sequenced first only because an unchecked assumption went
  untested. A family whose flagship proposals rest on an unchecked premise
  should not be trusted with the repair budget.
- **The data-processing inequality is not a hypothesis.** It is a theorem.
  I(q;Y|J) — the residual the channels need — is, by construction of the
  δ≲σ band, exactly the information J destroyed. No function of J recovers
  it. Every additional judgment-side proposal is an argument that the
  theorem has an exception for their transform. It does not.
- **The shootout is already the family's autopsy.** 0.1483 bits from the
  champion, with the two members sub-additive on the same leakage, is not "a
  promising start" — it is the measured ceiling, and Native showed the
  ceiling is a property of the adversary's parameters, not of insufficient
  cleverness. Squeezing the same orange harder is not a research program.
- **The family's evidence base is contaminated by mismeasurement.** The (b)
  0.0110-bit result — the "re-observation is useless" datum — measured an
  independently generated primary variant, not a noisy re-observation of the
  adversarial stimulus. The family has been citing against its own best
  remaining member. And confidence, its natural auxiliary signal, turned out
  adversarially inverted. The family's remaining proposals all route through
  the one instrument the adversary was built to fool.

**Bottom line:** run C2 — I endorse the run, the prereg, and the kill bars
as written. It will do exactly one useful thing: confirm the boundary error
is noise-driven, kill the transform probe on F1, and leave stimulus-analytic
verification (C1) as the only remaining direction. Then build C1 against the
frozen bytes, and retire the judgment-side family to the red-team shelf
where it belongs.
