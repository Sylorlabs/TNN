# RED TEAM — POST-RESULT POSITION

Date: 2026-09-22. Role unchanged: skeptic. Status: analysis only.
Read against: `verdict_brief.txt`, `scores_tcp.json`, `DEBATE_PRE.md`, and my
pre-result papers (`pos_red.md`, `rebut_red.md`).

---

## 1. The victory lap (brief), then the turn

My frozen predictions vs the measured numbers:

| Bar | I predicted | Measured | Hit? |
|---|---|---|---|
| F1 bits ≤ 0.15 | FIRES (70–75%) | 0.0000 | ✓ |
| F2 P(C\|Y=0) ≥ 0.70 | FIRES, spuriously (60–65%) | 1.0000, 40/40 | ✓ — stronger than my central estimate |
| F3 calibration | VOIDS ≥1 sense on ≥1 task (~70%) | B void, 77/93 | ✓ — stronger: a whole sense, not a task cell |
| F4 false-install ≥ 0.15 | FIRES (~60%) | 0.4348 | ✓ |
| C2 deploys? | No | Void as measurement; A1 incremental +0.0000 | ✓ |

C1 and C2 both predicted F2 would stay quiet on the grounds that the error is
noise-driven. F2 fired at the maximum possible value. Their mechanism story is
dead; mine survived contact with the data. I'll take the sweep.

Now the turn, and it's the honest one: **my predicted consequence did not
execute.** My warning was "spurious F2 firing via estimator-covariance →
permanent retirement on a confounded statistic; not a decision, a scheduled
accident." The first half happened at full strength — P(C|Y=0) = 1.0000, and
pooled P(C) = 1.0 on all 92 test fixtures, i.e. the probe's transformed
judgment NEVER deviated from L(J), even on adversarial near-boundary items.
The second half did not: every cell tripped the A2 vacuity rule (P(C) ≥ 0.98),
so F2-A2 has n_Y0 = 0, the retirement cannot fire on the frozen rules, and per
§7 the branch is "C2 void as a measurement; C3 decides."

Note the irony honestly: the A2 amendment — the one piece of my stand-down
list I granted as genuinely closing a confound path pre-run — is exactly what
blocked the accident. The tribunal was scheduled; the brake held. The live
question is now narrower and harder: **is the fired F2 spurious (my charge) or
genuine?** On that, the numbers alone do not acquit me, and I will not pretend
they do.

### Steelman: the coordinator's case for GENUINE

It is stronger than my pre-run rebuttal allowed. Two legs:

(a) **Non-identity-L cells exclude the silent killer.** On identity-L tasks, I
was right that P(C) = 1.0 is vacuous: an estimator that ignores T entirely —
or J's T-invariant systematic fool — also yields C = 1, so consistency carries
no information. But pitchdisc and motiondir use non-identity L. There, the
probe demonstrably moves the judge: Jt = L(J) ≠ J on every non-SAME fixture,
and a T-invariant systematic fool would score C = 0 and fail F3 instead of
contributing to F2. So P(C|Y=0) = 1.0 on the fooled fixtures in those cells is
NOT explainable by estimator T-invariance. The sense genuinely tracks the
transformed task quantity — and when it is fooled on q, it is fooled in
exactly the transformed way on T(q). That is structure-following error, not
noise. My §1b confound (smooth estimator gives high consistency "by
construction") survives only in the narrowed corner below.

(b) **DPI is the whole retirement in miniature.** Jt = L(J) identically on all
92 fixtures ⇒ the pair (J, Jt) is a deterministic relabeling of J ⇒ no
deterministic verdict V = f(J, Jt) can add information over J alone. The
measurement confirms it empirically: F1 = 0.0000 bits, A1 incremental +0.0000
vs same rows, resolution accuracy 0.5652, F4 = 0.4348 (nearly half of
"consistent" verdicts are wrong — the consistently-fooled population the
adversary exists to create is real). The retirement thesis, at its core, is
just this DPI point, and the data is the DPI point wearing work boots.

I grant both legs. They are real evidence against the vacuity reading and for
genuine transform-covariance of the errors on non-identity-L tasks.

### My strongest remaining objection

Even granting the steelman, three things stand — and the first is the one
that matters most right now:

(i) **The "17 non-vacuous fooled fixtures" is a post-hoc reclassification.**
The frozen scorer's vacuity map marks all six A cells vacuous; F2-A2 = n/a
with n_Y0 = 0. The frozen rule — P(C) ≥ 0.98 per cell ⇒ vacuous — exists
precisely to prevent what the coordinator's case now does: un-mark cells
after seeing the numbers because an argument can be made that *these*
P(C) = 1.0s are informative. If the vacuity rule is rewriteable post-hoc on
the basis of a good argument, then every bar is rewriteable post-hoc, and
frozen law is a suggestion. Either the retirement fires on F2-A2 as frozen
(it can't — n = 0), or the retirement waits for C3 (the §7 branch as
written). There is no third option that keeps the prereg frozen.

(ii) **Scope: the measurement exhausts transform-consistency channels, not
the judgment-side family.** The DPI leg proves that *this* probe's verdicts
are deterministic relabels of J. The leap from there to "retire the whole
judgment-side family permanently" was preregistered as a governance rule, not
derived as a theorem. Cross-sense A/B structure, SUSPECT-style meta-verdicts,
any judgment-side construction not built on (J, Jt) pairs of these transforms
— untouched by this measurement. I am not reviving the "looser band" defense
(I killed it myself in §3a). I am saying the legal scope of the retirement
exceeds the scientific scope of the evidence, which is exactly why the
auto-execution clause should become Micah's decision on converged evidence.

(iii) **The surviving corner of the spurious charge.** The coordinator's (a)
excludes T-invariant systematic fools and vacuous identity-L inflation. What
it does not exclude: a deterministic estimator whose boundary behavior is
noise-like yet T-symmetric — content-derived deterministic dither, the corner
case of my §1e/§1b. On this instrument, that regime also gives P(C) = 1.0
everywhere. Nothing in the measured numbers separates it from genuine
systematicity. C3 is precisely the instrument that can — *if* its
re-observations carry genuinely independent noise realizations. If C3
re-observes the same bytes through the same deterministic binary, the dither
reproduces and C3 cannot separate the corner either; the C3 design must be
checked for this before its verdict is treated as decisive.

---

## 2. The stand-down list: zero for five pre-run — any hits now?

My five falsifiers, checked against the measured numbers:

1. **Covariance-calibration control (orthogonal perturbation baseline):** NOT
   run. No F2-adjacent number separates covariance from systematicity. ✗
2. **In-band stratification of F1/F2:** not reported. ✗
3. **Law validation before F3 voiding:** B was voided at 77/93 with no refit of
   (T, L) to B's own primary behavior. Worse, the reported numbers don't even
   include per-(B, task) cal rows, so we cannot tell whether the void was my
   predicted law-misspecifications (t3 chiral shapes, t4 order effects, t5
   asymmetric envelopes) or genuine transform-fragility. The void is
   uninterpretable — my §1a warning, confirmed as a live ambiguity. ✗
4. **Stated oracle + σ′ ≪ δ budget for C1 before resources move:** C1 has
   produced neither. ✗
5. **Uncertainty / minimum-denominator guard on F2:** no CIs reported;
   F2-primary = 1.0000 is still a bare point estimate. But the *outcome* #5
   was meant to prevent — a permanent verdict firing on thin/confounded
   evidence — did not occur, via the vacuity rule rather than the requested
   guard. Half-credit on the spirit, zero on the letter.

Score: **0/5 as positive conditions; 0.5/5 on outcome-spirit.** The list
stands. In particular, #3 is now more urgent, not less: a sense was voided on
evidence that cannot distinguish "bad law" from "bad sense," and that
distinction is load-bearing for whether B's 77/93 means anything at all.

---

## 3. C3: what vindicates "spurious" vs what buries it

C3 is honest noise re-observation, both senses, preregistered. The conditions:

**Vindicates my spurious charge** — C3 recovers > 0.15 bits on **in-band**
fixtures (|q − b| ≲ δ) for either sense, with the error pattern across
independent re-observations showing the noise signature (errors decorrelate
across realizations; the A/B-style independence dividend appears). That would
mean the boundary error had a recoverable noise component all along, and F2's
"systematic" reading was the estimator-covariance artifact I charged it with
being: the retirement would have killed a family that works. Required
anti-leakage guard: the bits must survive in-band stratification — > 0.15 via
band-tail leakage alone is inconclusive and vindicates nothing.

**Buries my spurious charge** — C3 ≤ 0.15 bits on in-band fixtures for **both**
senses despite genuinely independent re-measurement, i.e. the δ/σ band
arithmetic binds even when the observation is honest. Equivalently: the same
fixtures are fooled identically across independent re-observations (error
correlation ≈ 1), the signature of structural rather than noise-driven error.
Then whatever F2 "really measured," the noise component is operationally
unrecoverable, and the systematic reading is the correct one for every purpose
the program has. My charge loses its mechanism.

**Design check that must precede either reading** (from §1(iii) above): C3's
re-observations must carry genuinely independent noise realizations. If C3 is
byte-identical reruns of the same deterministic binary on the same bytes,
deterministic T-symmetric dither reproduces exactly, and C3 is blind to the
one corner my charge still owns. Verify this in the C3 prereg before scoring.

---

## 4. If C3 ≤ 0.15 bits: do I stand down on the retirement?

**Yes — conditionally.** If C3 fails on in-band fixtures for both senses with
independent noise realizations, two independent instruments (T-consistency
covariance + honest re-observation) converge on the same cap, and the δ/σ
arithmetic is the binding constraint rather than any probe artifact. At that
point my spurious charge has no surviving mechanism, and I stand down on both
the charge and the retirement.

The conditions on the stand-down, stated plainly so they can't drift later:

- (a) **In-band only.** Pooled ≤ 0.15 that hides an in-band signal is not a
  failure; stratify or it doesn't count.
- (b) **Both senses.** One sense failing is a sense result, not a family
  result — especially with B already voided on uninterpretable grounds.
- (c) **Frozen threat model scope.** The retirement is recorded as "retired
  under the frozen adversary; re-opens if the threat model changes" — not as
  eternal law. My §3a stands: the claim is indexed to this adversary.
- (d) **Governance, not auto-execution.** The retirement is Micah's decision
  on the converged evidence (F1 = 0.0000, F2-primary = 1.0, C3 ≤ 0.15), not
  F2's automatic trip. The §7 auto-execution clause should be amended
  accordingly — the debate record (J, C2-rebuttal, and both my papers) is
  unanimous that the clause overreaches, and nothing in the measured numbers
  rehabilitates it.

If C3 fails pooled but in-band succeeds, or fails on one sense only, or its
re-observations aren't noise-independent: no stand-down. The charge stands and
the retirement waits.

— red team, post-result
