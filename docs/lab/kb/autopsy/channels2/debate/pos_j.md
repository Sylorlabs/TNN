# DEBATER J — Position paper: the judgment-side channel family is not dead

Debate: KB4 pre-result. Author: Debater J (defending the judgment-side family).
Read: SYNTHESIS.md, PREREG_OUTLINE_TCP.md. Date: 2026-09-22.

## The line I hold

The judgment-side channel family — channels that repair the SUSPECT gate using
only the judgment stream plus transformations of the frozen adversarial bytes,
no new sensors, no human oracles, no per-task analytic models — must not be
retired until F2 actually fires on measured data. Agreement between two
investigators is not a measurement. A ~0.15-bit cap against ONE adversary
construction is not a family ceiling. And permanent retirement on a single
falsifier measurement is governance overreach.

---

## 1. The steelman

### 1a. The 0.15-bit cap is a property of the adversary, not of the family

This is not my claim — it is native's own finding, and it cuts against the
"exhausted" verdict. Native characterized the adversary from its own
generator: a boundary-straddling stimulus author sampling the task quantity q
from a band around the decision boundary with band half-width δ ≲ the judge's
measurement noise σ. Native then showed the ~0.15-bit cap is a property of the
δ/σ construction parameters: **a tighter band would drive it to zero.**

Read that sentence twice. If tightening the band drives the cap to zero, then
the cap is measuring the adversary's construction, not the judgment-side
family's potential. By symmetry, a looser band — or a different construction
entirely (an adversary that fools with mislabeled saliency, with context
framing, with anything other than boundary-straddling) — could raise the cap
well above 0.15 bits. The shootout champion's 0.1483 bits tells us how much
information THIS adversary's construction leaks through THESE probes. It does
not bound what judgment-side channels can extract from a different adversary,
or from this adversary under a probe it never modeled.

Sol and native both scoped their verdicts to the FROZEN adversarial
construction — the synthesis says so explicitly, and both demand a separate
red-team for an adaptive adversary. A family retirement is permanent; the
measurement it rests on is explicitly threat-model-scoped. Those two facts do
not belong in the same decision.

### 1b. The shootout did not exhaust the family — one member was never tested at all

Native's own autopsy: shootout (b), "re-observation under noise," was
mismeasured. J_n was the judgment on the noise variant of the PRIMARY
stimulus — an independently generated image — not a noisy re-observation of
the ADVERSARIAL stimulus. The recorded "0.0110 bits" is therefore not evidence
that re-observation-under-noise is useless. **It was never tested.** That is
exactly why native's C3 is framed as "the honest re-test."

So the record stands: the family member that most directly probes the
noise-driven-error hypothesis — the hypothesis native's own accounting
supports (band-tail leakage plus the A/B noise-independence dividend, both
noise-driven) — has zero clean measurements against it. You cannot declare a
family exhausted while one of its members has never been honestly run. F2
retiring the family permanently before C3's re-test even executes would be
killing an untested channel by association.

### 1c. "Sub-additive" is evidence of saturation of THESE probes, not of the family

Native's steelmanning shows (a)+(c)'s 0.1483 ≈ 0.0695 + 0.0797 is sub-additive
— both probes drink the same band-tail leakage. Correct. That proves the two
probes are informationally overlapping, i.e., that the probe SET is
redundant. It does not prove the information is absent from the judgment
stream. TCP (C2) taps a fresh axis — transform-consistency — that neither (a)
nor (c) touches. Declaring the family dead because two overlapping probes
saturate is like declaring a well dry because two buckets drawn from the same
rope came up equally full.

### 1d. Permanent retirement on one F2 measurement is too strong

F2 is a single number — P(consistent | Y=0) on 92 test fixtures, one
adversary, one transform set, one frozen sense binary — and its consequence is
PERMANENT retirement of an entire channel family, recorded as law. Consider
what has to be true for that consequence to be proportionate:

- The 92-fixture test split must be representative of every adversary the
  family will ever face. It is representative of exactly one construction.
- The six hand-authored (T, L) pairs must be the right probes. If h-flip is a
  poor transform for t2's judgment (F3 exists precisely because this might be
  true), a family dies on a bad instrument, not a bad theory.
- "Fooled judgments are transform-consistent" must imply "no judgment-side
  channel can ever work." It implies no such thing in general: it implies that
  THIS judge's fooled judgments are invariant under THESE six transforms. A
  noise-re-observation channel (C3), a confidence-free margin channel, a
  cross-sense disagreement channel under a DIFFERENT perturbation class — none
  of these are touched by F2's logic. F2 tests the transform-consistency probe;
  it does not test the family.

Retirement-as-law is also a governance act. The program's own rules put
irreversible decisions and law-changes in front of Micah. F2 firing should
trigger a recommendation to retire, with the evidence attached — not an
automatic permanent execution written into the prereg as a foregone
conclusion.

---

## 2. My prediction for C2

**F2 will NOT fire. F1 will not fire either. C2 deploys — beats 0.15 bits with
false-install below 0.15.**

Reasons, in order of strength:

1. **Native's own accounting says the error is noise-driven.** The 0.1483
   bits decompose into band-tail leakage (finite-width bands; fixtures whose
   q fell outside the noise floor, where the judgment genuinely works) and
   the A/B noise-independence dividend (two partially independent noisy draws
   of the same near-boundary q). Both terms are noise stories, not systematic-
   fool stories. If the judge's boundary error is dominated by noise — δ ≲ σ,
   the adversary lives inside the judge's noise floor — then the fooled
   judgment is a noise realization, and a deterministic transform T to a
   different byte image re-samples the judge's effective noise. J(T(stim)) will
   NOT equal L(J(stim)) on fooled fixtures at anywhere near 0.70 consistency.
   The adversary constrained J(stim); it never modeled T. Wrong twice,
   consistently, under an unmodeled transform is exactly what a noise-driven
   error cannot do.

2. **The calibration gate (F3) protects the prediction asymmetrically.** If a
   transform breaks the judge, F3 voids that sense — the failure mode lands on
   the instrument, not on my position. The senses that pass F3 are, by
   construction, the ones where T is task-covariant and the judge is
   T-respecting on clean primaries. On those senses, inconsistency under T is
   informative, not artifactual.

3. **TCP's information is on a fresh axis.** The shootout probes all squeezed
   the judgment stream itself (J, J_n, confidence, agreement). TCP asks a
   question none of them asked: does this judgment survive a symmetry of the
   task? The band geometry that saturated (a) and (c) does not saturate
   transform-consistency, because the adversary's construction never
   constrained it. Fresh axis, unmodeled by the adversary, noise-driven error
   → the channel clears 0.15 bits.

4. **False-install stays low** because INSTALL requires exact consistency
   J(T(stim)) == L(J(stim)); noise-driven fooled judgments fail this check and
   WITHHOLD. The failure mode that would inflate false-install — systematic
   fools that are transform-consistent — is precisely what F2 measures, and I
   predict it measures low.

My honest uncertainty: F3 may void one sense (time-reversal on pitchdisc is
the riskiest pair — if the judge's pitch features are not time-reversal-
covariant, calibration catches it, and that is the gate working as designed,
not evidence against the family). A partial void plus deployment on the
remaining senses still defends the family.

---

## 3. What would falsify my position

I concede the family should be retired — permanently, as law — if and only if
ALL of the following hold on measured, frozen, byte-identical-rerun data:

1. **F2 fires cleanly:** P(consistent | Y=0) ≥ 0.70 on the 92-fixture TEST
   split, with the calibration gate PASSED (≥95% per sense) so the result
   cannot be blamed on a broken instrument. This would show fooled judgments
   are a systematic deterministic function of the bytes under unmodeled
   transforms — the noise-driven-error hypothesis, which is the load-bearing
   wall of my case, would be dead.

2. **C3 (the honest re-observation-under-noise re-test) is run and yields
   ≤ 0.15 bits.** F2 alone kills TCP's theory of the error; C3's failure
   kills the last untested family member. I will not concede on F2 alone
   while (b)'s honest test has never run — retiring an untested channel by
   association is not falsification, it is tidiness.

3. **The F2 measurement replicates on a second, independently generated
   adversarial battery** (different seed/construction instance, same frozen
   protocol). One 92-fixture measurement against one construction instance is
   enough to kill a channel; it is not enough to retire a family permanently.
   A replication at ≥ 0.70 closes the "unlucky split / overfit construction"
   objection that 1d raises.

If all three hold, I will sign the retirement myself: the evidence would then
show the fooled judgment is systematic under every judgment-side probe we
could construct, and only stimulus re-measurement (C1 class) can repair it.
Short of that, the family stays alive.

---

## 4. Attacks

### On C1 (stimulus-analytic verification)

C1 is the "correct" long-term repair that nobody can afford to build. Its
weakest points:

- **Who builds the analytic re-measurement — for every task?** C1 requires a
  per-task analytic model of the true quantity q: a color-science model for
  colordisc, an acoustics model for pitchdisc, a motion model for motiondir.
  That is six bespoke human-engineered oracles, each one a research project,
  each one needing its own verification. The program would trade one hard
  problem (judgment-side channels) for six harder ones, each scaling linearly
  with every new task TNN ever faces. Judgment-side channels, by contrast,
  are task-generic machinery: TCP's (T, L) table is six rows of byte
  transforms, not six scientific models.

- **It reintroduces the judge it distrusts.** The analytic model is itself a
  judge — with its own boundary, its own noise, its own adversary-vulnerable
  construction. Who verifies the verifier? C1 does not eliminate the
  trust problem; it moves it one level up and declares victory. A channel the
  adversary cannot correlate (the synthesis's stated requirement) is not
  achieved by building a second correlatable judge by hand.

- **It concedes the research question prematurely.** The program's standing
  direction is TNN verifying itself — deliberate, native, self-contained. C1
  outsources verification to human-built analytic models. If judgment-side
  channels work, TNN checks its own work with its own machinery; that is the
  prize, and abandoning it before F2 even measures would be abandoning the
  program's own thesis on investigators' agreement alone.

- **Cost and latency.** Even if C1 works, it is the most expensive repair on
  the table — per-task modeling effort plus runtime analytic computation —
  against TCP's near-zero marginal cost (one extra frozen-binary run on
  transformed bytes). Deployability matters; the 0.1483-bit champion was
  rejected partly for not being deployable, and C1's deployability story is
  "hire a physicist per task."

### On C2 (the transform-consistency probe) — friendly fire, since I predict it deploys

I defend the family, not the probe's infallibility. C2's weakest points, which
the rebuttal round should press and which my prediction must survive:

- **It trusts the same fooled judge, just twice.** This is the sharpest
  attack and I do not dodge it: if the adversary's fool is a deterministic
  function of the stimulus bytes and T preserves the features the judge
  actually uses, then J(T(stim)) == L(J(stim)) holds on fooled fixtures too,
  and "consistency" is the same fool wearing a mirror. My defense is
  empirical, not logical: native's noise-driven accounting predicts this
  won't happen, F2 measures exactly this, and I predict it measures low. But
  if the judge's features are T-invariant in the wrong way — e.g., a global
  color histogram judge under h-flip — C2 is fooled twice by construction.
  The calibration gate does NOT catch this: F3 runs on clean primaries, where
  judge-correctness and transform-covariance coincide. A judge that is
  consistently wrong in a T-invariant way passes F3 and defeats C2 silently.
  That is the hole in the design, and F2 is the only instrument that sees it.

- **The "parameter-free" claim smuggles six human judgments.** The L laws
  (HIGHER↔LOWER, N↔S, identity elsewhere) were authored by a human reasoning
  about each task's symmetries. If any L is wrong — if time-reversal does NOT
  negate the pitchdisc judgment for the frozen binary's actual features —
  the channel misfires on correct judgments (false WITHHOLD, lost
  resolution) or, worse, a wrong L could manufacture spurious consistency.
  F3 mitigates but does not eliminate this: 95% on primaries leaves 5% of
  fixtures where the human's symmetry theory and the binary's behavior
  disagree, and adversaries live in exactly such cracks.

- **Transform coverage is thin.** One transform per task. An adversary that
  never modeled h-flip is today's adversary; the threat model explicitly
  excludes the adaptive one. C2 deploying against the frozen construction
  proves the channel works where the adversary is blind — valuable, but the
  victory does not transfer to an adversary that reads the prereg. (This cuts
  against permanent-retirement-via-F2 as well: both directions are
  construction-scoped.)

- **F4's margin is doing quiet work.** False-install < 0.15 with the bar at
  ≤ 0.10: the prereg demands margin, correctly. But note the asymmetry — F2's
  0.70 kill threshold against F4's 0.15: the prereg is built to kill the
  channel far more readily than to doubt the family. I accept the bars as
  written; I dispute only the automatic permanent-retirement consequence.

---

## Summary of the J position

1. The 0.15-bit cap measures this adversary's δ/σ construction (native's own
   finding); it is not a family ceiling.
2. One family member — honest re-observation-under-noise — was never tested;
   the family is not exhausted.
3. F2 has not fired. Agreement is not measurement. The family is not dead
   until it does, cleanly, with F3 passed and (ideally) replicated.
4. My prediction: F2 does not fire (errors are noise-driven; the transform is
   an unmodeled axis), F1 does not fire (fresh informational axis), C2
   deploys.
5. I concede permanent retirement iff: F2 fires cleanly AND the honest C3
   re-test fails AND the F2 result replicates on an independent battery.
6. C1 is unaffordable as a first move (per-task analytic oracles, infinite
   regress of trust, abandons self-verification); C2's real weakness is that
   a T-invariant systematic fool passes F3 and defeats it silently — which is
   exactly what F2 is built to detect.

The family holds the line until the measurement says otherwise.
