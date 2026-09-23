# C2 REBUTTAL — pre-result

## 1. The strongest attack, steelmanned, and my answer

The red team's §1b + §1c + §4 is the strongest attack any camp made on my
position — stronger than C1's or J's, because it doesn't dispute my numbers;
it disputes what my numbers *mean*, and it targets the consequence, not the
channel.

Steelman: F2 does not measure error-systematicity. It measures
estimator-covariance — whether a deterministic smooth estimator returns the
transformed label when fed transformed bytes. The sense is a fixed binary;
the adversary never modeled T, but the estimator doesn't need the
adversary's help to be T-covariant — smoothness gives it that for free. So
P(consistent|Y=0) ≥ 0.70 can fire when the error is noise-driven-but-chaotic
just as easily as when it is systematic, and the prereg attaches its most
irreversible consequence — permanent family retirement, recorded as law —
to a statistic with no validated mapping to the diagnosis, no uncertainty
quantification, no minimum-denominator guard, and calibration done in a
regime (fat-margin primaries) where the boundary artifacts that dominate
scoring are invisible. The single most likely misleading result is a
spurious F2 firing that leaves the program certain and wrong, shutting a
door permanently on the exact regime where channels could have worked.

My answer, in three parts:

(a) **The red team is right about the tribunal; I was wrong to write the
consequence as automatic.** My paper already granted J half the governance
point — "automatic permanent retirement on one aggregate number IS too
strong" — and then under-applied it, keeping the permanent-retirement
branch intact behind A2. That's inconsistent. Correction: F2 firing now
triggers a retirement *recommendation with evidence attached* (the per-task
map, the covariance-control result, the CIs), not an execution. The law
question goes to Micah with the measurements, per the program's own
governance rule for irreversible decisions. J's demand for replication
before law stands accepted in substance.

(b) **The run survives the downgrade intact.** Notice what the red team's
own recommendation is: "run C2 as a *measurement*, not as a *tribunal*.
Take the numbers." That is my bottom line verbatim — "run C2 — not as the
deployable, but as the pivot." The red team and I disagree on zero
measurements and one governance clause. And the pivot value never required
the tribunal framing: the per-task consistency map, the stacking analysis
(A1), and the F1/F4 readings all land the same under a recommendation
reading. The branches still decide what gets built next — they just do it
by evidence to Micah rather than by automatic execution.

(c) **The spurious-firing branch is the one where I already lose.** My
central prediction is F2 does *not* fire (0.50–0.65, noise-driven). If F2
fires spuriously via estimator-covariance, the red team's own accounting
says the reading is uninterpretable without a control — and my amendment A2
was precisely a pre-registered rule to separate interpretable from
uninterpretable F2 readings. I now extend it: A2 carries the red team's
covariance-calibration control (task-orthogonal perturbation baseline,
reported alongside F2) and per-cell confidence intervals with a minimum
denominator. F2 fires *and* the control separates → the systematicity
reading earns its recommendation. F2 fires *without* separation → recorded
as confounded, retirement recommendation withheld, per (a). The attack is
absorbed into the amendment rather than answered past it.

## 2. The weakest point in my own position, stated honestly

The red team's §1e exposed it: my entire branching logic assumes the
noise-driven vs systematic dichotomy is exhaustive. A deterministic,
near-boundary chaotic estimator breaks it — fixed function of bytes (so
"systematic") with unpredictable behavior under perturbation (so
"noise-like"). In that regime my two branches misdiagnose in opposite
directions: F2-quiet reads as "channels can work" when they can't (the
error is deterministic, just chaotic), and C1-class re-measurement succeeds
only if σ′ ≪ δ, which nothing F2 measured has any bearing on. My prereg
treats the F2 reading as deciding between "judgment-side can work" and
"only re-measurement can," but there is a third regime where *neither*
branch's prescription is sound, and I have no instrument in the run that
detects it. The covariance-control baseline in the amended A2 gives partial
coverage — a chaotic estimator should show low consistency under the
orthogonal perturbation too, while a covariant-but-systematic one shows
high under T and low under the orthogonal baseline — but I did not design
for this regime, and I won't pretend A2 fully covers it. The honest
statement: my pivot experiment can still leave the program in the chaotic
regime with a confident-sounding wrong branch. That is the load-bearing
risk I accepted without naming it, and naming it now.

## 3. One concession, one hold

**Concede:** F2 as a bare aggregate statistic cannot carry a
program-permanent consequence, and my original prereg let it. The firing
branch is now a gated recommendation — F2 ≥ 0.70 *on non-vacuous tasks*,
*with* the orthogonal-perturbation control separating, *with* CIs and
minimum denominators — and even then it recommends, it doesn't execute.
(J: this is your governance point, taken in full. The family stays alive
until Micah reads the evidence.)

**Hold:** C2 still runs first, and C1 still owes its σ′ proof before any
resources move. The red team's §2a is my attack now, sharpened: the band
math applies to the analytic measurer too. C1's whole advantage reduces to
"the frozen adversary didn't target it" — a real but unmeasured hope —
and σ′ ≳ δ hits the same wall the shootout hit. Nobody has measured σ′
against δ for any of the six tasks. Until that measurement exists, "go
all-in on C1" is a bet justified by a confounded statistic, and I will not
let F2's retirement branch — even in its downgraded form — be spent as
currency to buy C1 without the σ′ demonstration the red team demands. The
sequencing stands: cheapest measurement first, expensive per-task builds
after evidence, not before.

## A1 and A2 — status

- **A1 (stacking analysis): yes, still frozen before the run.** Unchanged.
  It decides "diagnostic vs complementary channel" and costs one analysis
  line on TEST. The red team raised no objection to it; J's fresh-axis
  claim and C1's redundancy claim make opposite predictions about it, so
  it arbitrates between the camps.
- **A2 (vacuous-task exclusion): yes, but as amended — it must now carry
  the red team's covariance control.** The vacuous-task rule (P(C) ≥ 0.98
  → VACUOUS → excluded from aggregate F2) stays, because without it the
  aggregate can fire on a technicality I predicted in my own paper. Added
  to it: (i) a task-orthogonal perturbation baseline reported alongside
  every F2 cell, (ii) per-cell confidence intervals with a frozen minimum
  denominator, (iii) in-band stratification (|q − b| ≲ δ) for the F1 and
  F2 statistics, since the red team's runner-up concern (leakage-driven
  deploy verdict) is real and per-class rows alone only partially guard
  it. I insist A2-as-amended be frozen before the run — otherwise the
  guards will be negotiated after the numbers land, which is exactly the
  drift my original paper was written to prevent.
