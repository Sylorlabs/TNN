# POST-RESULT — Debater C1 (pro stimulus-analytic verification)

Measured data in hand: F1 0.0000 bits (FIRES), F2-primary P(C|Y=0)=1.0000 (FIRES),
F2-A2 1.0 on the 17 non-vacuous fooled fixtures (FIRES CLEANLY), F4 false-install
0.4348 (FIRES), F3 sense-A green / sense-B void, A1 +0.0000 incremental bits.

## 1. Prediction scorecard

| Bar | My prediction | Measured | Score |
|---|---|---|---|
| F1 (bits ≤ 0.15) | fires, ~0.03–0.09 bits | 0.0000 bits | ✓ correct, and stronger than I dared (a constant function) |
| F2 (P(C|Y=0) ≥ 0.70) | does NOT fire — errors noise-driven | 1.0000 (40/40); 1.0 on 17 non-vacuous fooled fixtures | ✗ FAILED, both directions |
| F3 | green both senses | A 93/93 PASS, B 77/93 VOID | ◑ half — I said a void would be a calibration artifact and to disregard it; B voids on spatial transforms (shapetrans 16/23, motiondir 6/15 cal consistency). It is exactly the artifact I named. Sense-A stands. |
| F4 (false-install ≥ 0.15) | near/over the line | 0.4348 | ✓ correct |

On F2: I was wrong, and the red team was right — 60–65% spurious-fire call
against my central estimate. The errors are **deterministically
transform-covariant, not noise-decorrelated**. My "noise-driven by
construction" prior came from the δ≲σ generator story: I assumed the noise
realization would de-correlate across T, so fooled draws would disagree
under transformation. The measurement says otherwise: on the non-identity-L
tasks (t4/t6), fooled fixtures get fooled *identically* under T. The probe
demonstrably moves the judge (Jt = L(J) ≠ J) — so these cells are
non-vacuous — and the judge's error covaries with the transform rather than
washing out. My mechanism story for F2 is falsified, retracted, and
replaced: **estimator-covariance under T, measured.**

Note the asymmetry, honestly: F2 was never my load-bearing instrument —
I said so in both papers — but the load-bearing part did land: **C2 is dead
on its own bars**. F1 fired at literally 0.0000 bits and F4 fired at
0.4348. C2 did not deploy. My prediction "C2 does not deploy" survives on
the strongest possible version of the evidence: the channel verdict is a
constant function — INSTALL on everything — which is precisely my paper's
§2 claim ("the rule 'trust the judge when it agrees with itself'")
instantiated.

## 2. Is P(C|Y=0) = 1.0 "systematic error" or "estimator-covariance, spurious"?

The red team's label is right, and I take the consequence.

"Systematic error" as a diagnostic category was supposed to license a
corrective: if the errors are systematic (shared bias), maybe a
judgment-side transform could undo them. But P(C|Y=0)=1.0 here does not buy
that. The consistency is a property of the estimator's covariance with T:
a smooth deterministic sense satisfies J(T(x)) ≈ L(J(x)) on exactly the
fixtures where the (T,L) law holds — including the fooled ones. The judge
is wrong and self-consistent, which is the threat model's whole design
(consistently fooled judges are what the boundary band manufactures). So
the statistic measures **the estimator's geometry under the transform, not
the semantic character of its error**. It contains no corrective handle:
consistency tells you the law held, and the law held on fooled fixtures
too.

Either label is fatal to C2-as-channel — that was always my point. A
constant verdict yields zero bits and a 0.4348 false-install rate. The
disagreement between the camps now is only about the *governance*
consequence (permanent family retirement), and on that I side with J and
the red team: F2's aggregate, even the clean A2 reading, is a
confounded statistic for family-execution purposes. But it is a
dead-on-arrival statistic for C2-the-channel, which is what I predicted
would die. It died. Retire the channel; keep the family-retirement question
on J's conjuncts (honest C3 must run and fail; F2 must replicate on an
independent battery).

## 3. The coordinator's DPI argument — any remaining judgment-side member?

None. This is now a measurement, not an argument.

Under the measured regime, J(T(x)) = L(J(x)) holds identically on the
non-void sense. Then (J, Jt) is a deterministic function of J alone, and
I((J,Jt); Y) = I(J; Y) — no deterministic function of (J, Jt) adds
information. The A1 stacking number is the empirical signature: **+0.0000
incremental bits over (a)+(c) on the same rows**. The channel added
literally nothing, exactly as the theorem requires.

The only conceivable judgment-side member left is one that brings a new
observation, not a new function: **honest C3 re-observation of the same
adversarial stimulus under fresh noise** — the genuinely untested
narrowband member whose absence the mismeasured (b) falsely filled in. C3's
ceiling is the noise-independence dividend (~0.08 bits, sub-additive), not
a channel property; it can only ever be a small diagnostic of the noise
budget. Past C3 there is no theorem-compatible judgment-side member.
Anything else is a function of J wearing a new transform. The family's
budget is: C3, then done.

## 4. What the live follow-ups would mean for C1's thesis

**C3 (honest re-observation-under-noise, both senses):**
- > 0.3 bits with false-install < 0.15: my exhaustion thesis as I
  phrased it takes a hit — the judgment stream was not exhausted; its
  narrowband member was simply never tested. I concede that per my
  falsifier #2. But it does not revive C2 or any deterministic
  (J,Jt)-function channel — the DPI argument for that class stands
  measured. And it does not displace C1: a ~0.3-bit narrowband noise
  dividend is still a sliver next to the full residual the bytes hold
  in principle. Judgment-side becomes "has one narrowband trick";
  stimulus-side remains the repair.
- ≤ ~0.15 bits: the narrowband member fails too, and the exhaustion
  thesis is confirmed on all tested members. The judgment-side family
  is exhausted by measurement as well as by theorem. Build C1.

**C1-scout (pitchdisc analytic on frozen bytes, preregistered):**
- Beats 0.15 bits with the σ′ ≪ δ gate measured and the oracle stated:
  the extractability claim survives its first real test and the
  stimulus-side repair is validated as a direction; scale to the other
  five tasks with the same discipline. This is my falsifier #3's
  antecedent turned into a build gate, and the scout is the gate.
- Cannot beat 0.15 bits: falsifier #3 fires as written. I concede the
  analytic-repair thesis for this fixture regime and Sol's fallback
  (second physical sensor / human verification, new collection) becomes
  the real repair. What I will not concede on that outcome: that
  judgment-side is thereby vindicated — the shootout's DPI result and
  C2's 0.0000-bit corpse still stand. We'd just be in a harder world
  than I claimed, with no channel family living in it.

One design lesson the failed F2 forces onto the scout: the analytic's
error must not covary with the judge's. An analytic that is just a
clean-room reimplementation of the same estimation principle would
inherit the judge's covariance structure and be a constant channel with
extra steps. The σ′ gate must therefore be measured **on the fooled
fixtures**, not on calibration clean ones — the residual the channel
needs is exactly the sub-boundary residual where the judge died.

## 5. Updated falsifiers

1. **C2 deploys** (beats 0.15 bits, false-install < 0.15, both senses,
   byte-identical 2× reruns): MOOT — C2 is dead on its own bars
   (F1 0.0000, F4 0.4348). The antecedent failed. What remains live in
   its place: **if honest C3 (>0.3 bits, false-install <0.15) or any
   future preregistered judgment-side channel beats 0.30 bits on the
   frozen adversarial split with false-install < 0.10**, the exhaustion
   cap was methodological, not informational — I concede the thesis.
   The in-band stratification check (|q−b| ≲ δ) still applies before I
   read any such result as a genuine channel rather than band-tail
   leakage.
2. **Honest C3 > 0.3 bits, false-install < 0.15**: hold, unmodified —
   partial concession of the exhaustion thesis (narrowband member
   exists), no revival of deterministic channel functions.
3. **Prereg-disciplined C1 analytic can't beat 0.15 bits on the frozen
   bytes**: hold, unmodified, now live as the C1-scout test — this is
   the load-bearing one, with the stated oracle and the σ′ ≪ δ gate
   measured on fooled fixtures.
4. **Any future preregistered judgment-side channel beats 0.30 bits**
   with false-install < 0.10: hold, unmodified (folded into #1's
   remainder).

**Bottom line:** I missed F2's direction; the red team read the
mechanism better than I did. It doesn't move the verdict: C2 fired
every kill bar it had, added exactly +0.0000 bits, and died as a
constant function — which is the channel I said it was. The
judgment-side family's only remaining live member is honest C3's
fresh-noise draw, and then the theorem closes the door. The only live
repair direction is stimulus-side, gated on the scout proving σ′ ≪ δ
where the judge actually died. Run C3, run the scout, read the bars.
