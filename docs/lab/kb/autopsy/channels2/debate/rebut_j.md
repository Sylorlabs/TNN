# DEBATER J — REBUTTAL (pre-result, KB4)

Voice: J. One file, no drift. I read all four papers against my own.

---

## 1. The strongest attack on my position, steelmanned, and my answer

**The steelman.** The red team, backed by C1 and C2, says my §1a "the cap is
the adversary's" argument collapses into wishful thinking because the one
counterfactual it needs proves too much: if the band were loose enough for a
judgment-side channel to add information, it would be loose enough for the
raw judgment to resolve — and then no channel is needed at all. The defense's
success condition is indistinguishable from the channel being unnecessary. My
defense is therefore a counterfactual about an experiment that wasn't run,
offered against the frozen threat model the whole program froze. Under the
frozen model — this adversary, this band, these bytes — the 0.15-bit cap is
measured, decomposed into band-tail leakage plus the A/B dividend, and there
is no stated mechanism by which a judgment-side function of these bytes
escapes the δ/σ arithmetic. C1 adds: DPI is a theorem, not a hypothesis, and
every new judgment-side proposal is an argument that the theorem has an
exception for their transform.

**My answer.** I accept the success-condition critique — it is the best
argument made against me, and it genuinely stings: I have no named
band-width regime where the channel adds bits the raw judgment lacks. I will
not pretend otherwise. But the attack as framed conflates two different
things I said:

- Claim A (the bad one, now withdrawn): "a looser band would let
  judgment-side channels work." The critics are right — this is vacuous as a
  defense. A band loose enough for channels is loose enough for the judge.
  Withdrawn, no reservation.
- Claim B (the one I still hold): "the 0.15-bit cap is measured against one
  construction instance and one frozen adversary; treating it as a family
  ceiling is a scope error, and permanent retirement is a governance act
  that must be proportionate to the evidence."

Claim B is untouched by the steelman. It does not depend on looser bands, on
DPI exceptions, or on counterfactual adversaries. It depends on three facts
on the record: (a) one family member, honest re-observation-under-noise, was
never measured (native's own autopsy); (b) the red team shows F2's statistic
may measure estimator-covariance, not error-systematicity — the exact
confound the task brief flagged — with no control arm to separate them; (c)
92-fixture aggregate proportions with no minimum-denominator guard and no
uncertainty quantification should not trigger a permanent, program-wide
verdict. The steelman kills my bad argument about looser bands. It does not
touch my governance argument, which is now the whole of my position.

---

## 2. The weakest point in my own position, stated honestly

My weakest point is the pair of predictions in §2 of my original paper: F2
does NOT fire (noise-driven error) **and** F1 does NOT fire (C2 deploys on a
fresh axis). C2 nailed it: these two predictions are in tension, and the
red team explains why the tension is fatal to the deploy half. Under the
noise-driven model I myself used to ground the F2 prediction, band-center
consistency is agreement between two near-coin-flip draws — ~zero bits about
Y. The bits live in the band-tail, which (a)+(c) already drank. A fresh
question is not fresh information, and "the adversary never modeled T"
cannot manufacture bits from a draw that carried none. I needed the noise
story to keep F2 quiet and needed to forget it to keep F1 quiet. You cannot
have both.

Honest restatement of what I now predict: **F1 fires (C2 dies on the bits
bar), F2 likely stays quiet (aggregate, non-vacuous reading), and C2's
product is the F2 answer plus the per-task consistency map** — which is C2's
own position, and I now hold it as mine. What I still do NOT concede is
what follows: C1's claim that an F1-kill is a family-kill. F1 measures one
probe's bit yield against one construction. It does not measure the honest
C3 re-test that was never run, and it does not convert "this probe added
nothing" into "no judgment-side probe can." The family retirement question
stays open; the C2-as-deployable question is closed, by my own concession.

---

## 3. One concession, one hold

**I concede:** my deploy prediction for C2 (beats 0.15 bits, false-install
below 0.15). It was the weakest load-bearing beam in my paper, it
contradicted my own noise-driven account of the error, and after the red
team and C2 I can no longer defend it. Expect F1 to fire.

**I still hold:** that permanent retirement of the judgment-side family —
a law-level, program-wide, irreversible verdict — may not be executed on
F2's aggregate statistic in its current form. The red team strengthened
this hold, not weakened it: F2 has no covariance-calibration control, no
vacuous-task handling (C2's amendment A2 is the minimum fix and I now
support it explicitly), no minimum-denominator guard, and the most likely
misleading result in the program is an F2 misfire measuring estimator
smoothness. A tribunal with that many unpatched holes cannot issue a
permanent sentence.

---

## 4. My falsification bar after the red-team's governance critique

My original bar was a three-part conjunction: retire iff **(i)** F2 fires
cleanly, **(ii)** the honest C3 re-test fails, **and (iii)** F2 replicates
on an independent battery. After the governance critique, here is where I
stand — honestly, because the bar is now the position:

- **Conjunct (i): REVISED, strengthened, not dropped.** "F2 fires cleanly"
  now means: aggregate P(consistent|Y=0) ≥ 0.70 over **non-vacuous tasks
  only** (C2's A2 — vacuous-task exclusion, frozen before the run), with a
  minimum denominator per reported cell, a reported confidence interval,
  and the covariance-calibration control from the red team's stand-down
  list (task-orthogonal perturbation alongside the F2 statistic — if both
  read high, it was estimator smoothness, and (i) is void). The red team's
  §1a point about F3 stands as well: laws must be validated against the
  sense's own transformed-primary behavior before a void is declared;
  a calibration void caused by a misspecified law is not a theory failure.
- **Conjunct (ii): HELD, unchanged.** The honest C3 re-test — true
  re-observation of the SAME adversarial stimulus under fresh noise, not
  the mismeasured (b) — must be run, and must yield ≤ 0.15 bits with
  honest false-install reporting. I will not sign a family retirement
  while its most direct family member has zero clean measurements. This
  was the load-bearing plank of my original paper and it is now my whole
  position's load-bearing plank.
- **Conjunct (iii): HELD, and sharpened by the red team.** The F2
  measurement must replicate on a second, independently generated
  adversarial battery (different seed/construction instance, same frozen
  protocol). Given the red team's finding that the deck is stacked toward
  F2 firing (frozen deterministic binary + task-covariant T maximizes
  near-boundary consistency independent of the error's nature), a single
  un-replicated 0.70 aggregate is exactly the result most likely to be a
  confound artifact. Replication at ≥ 0.70 on the second battery, under
  the same strengthened (i) reading rules, closes the "estimator
  covariance flattered the first run" objection.

I hold all three conjuncts — (i) with a stronger, prereg-frozen reading
rule that the red team's critique forced, (ii) and (iii) as written. If
all three hold, I sign the retirement myself, exactly as I said in §3 of
my original paper. Short of that, the family stays alive, C2 runs as a
measurement (F1 will fire; the F2 answer is the product), and no law is
written on a confounded statistic.

---

## Net position after rebuttal

Dropped: the deploy prediction for C2; the "looser band" defense.
Kept: the governance position — no permanent retirement without the
three-part bar, with F2's reading rules hardened per the red team.
Changed: I now predict the same numbers C2 predicts. We disagree only on
what an F1-kill licenses: C2 and C1 say family death; I say run C3 first,
replicate F2 second, write the law third.

The family holds the line until the measurement — a properly controlled
measurement — says otherwise.
