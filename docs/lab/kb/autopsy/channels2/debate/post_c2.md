# C2 POST-RESULT — scored against the measured artifacts

## 0. Data discrepancy, stated first

The task summary I was handed says: "F2-A2: 1.0 on 17 non-vacuous fooled
fixtures (t4: 8, t6: 9) → FIRES CLEANLY." The frozen artifacts say the
opposite. `scores_tcp.json` reports `F2_A2: null, F2_A2_n: 0`; every one of
the six sense-A cells is flagged `vacuous: true` with `test_P(C) = 1.0`; the
`verdict_brief.txt` concurs ("F2-A2 (non-vacuous cells) = n/a (all cells
vacuous) (n_Y0=0)") and the §7 branch taken is "EVERY CELL VACUOUS: C2 void
as a measurement; C3 decides." The two sources cannot both be right. This
paper scores my predictions against the measured artifacts — the authority
the prereg points at — and answers the falsifier question under both
readings, so the record doesn't depend on which one survives.

## 1. Prediction scorecard

| Bar | My prediction | Measured | Score |
|---|---|---|---|
| F1 bits | FIRES (~0.03–0.09) | 0.0000 ≤ 0.15 → FIRES | ✓ (direction right, magnitude wrong — undershot to exactly zero) |
| F2 | quiet on non-vacuous aggregate (0.50–0.65, no fire) | F2-primary 1.0000 → FIRES; F2-A2 n/a (zero non-vacuous cells) | ✗ on the primary number; the A2 aggregate — the one I actually predicted on — doesn't exist |
| F3 | PASSES both senses (~85%) | A 93/93 PASS; B 77/93 FAIL → B VOID | half — the void landed on a sense, as the red team predicted (70%) and I discounted |
| F4 | fires, moot | 0.4348 ≥ 0.15 → FIRES | ✓ |
| C2 deploys? | no | dead: always INSTALLs, 0.0000 incremental bits (A1) | ✓ |

## 2. The F2 miss — what I got wrong about the judge

My central estimate (0.50–0.65) rested on a model where the transform
re-draws the measurement noise: the fooled judgment is a boundary
excursion, the second draw under T lands on the other side often enough
that agreement on fooled fixtures sits near a coin flip. The measured
`P(C) = 1.0` on all 92 sense-A test fixtures — fooled and unfooled alike —
says the transform re-draws nothing. The judge is perfectly T-covariant:
`J(T(stim)) = L(J(stim))` identically, on every fixture. The "second
reading" I sold as the one move DPI allows was not a second reading at
all. It was the same measurement, twice, wearing a different byte layout.

That kills the DPI-dividend argument at its root, and the root is my
error, not the instrument's. My steelman assumed the transform scrambles
whatever the fooling correlates with — including the T-asymmetric
renderer artifacts I named as the upside case. It scrambled nothing the
estimator cares about. The estimator's decision regions are T-invariant on
these tasks; both draws land in the same region every time, so agreement
is 1.0 and the bits are exactly 0.0000. I predicted an agreement channel
harvesting ~0.08 bits of band-tail robustness; the band-tail contributed
nothing because the probe couldn't move the judgment off either tail.

Note the asymmetry with the red team's charge, which I now concede in
full on mechanism: they said F2 measures estimator-covariance, not
error-systematicity. The measured covariance is perfect — more extreme
than their 60–65% spurious-firing prediction. Where I still differ from
them is diagnosis: perfect covariance at `P(C)=1.0` is not evidence the
error is systematic; it is evidence the probe is vacuous. A2's
vacuous-cell rule, frozen before the run for exactly this case, classified
all six cells correctly. The firing primary aggregate is the technicality
my own paper named. I was wrong about the judge; I was right about the
guard.

## 3. The falsifier question — do I sign?

My falsifier #1: "F2 fires cleanly on non-vacuous tasks (per-task P(C)
well below 1.0, P(consistent|Y=0) ≥ 0.70 on the aggregate over
non-vacuous tasks) → I sign the family's retirement myself."

Under the measured artifacts, the antecedent is false. There are no
non-vacuous tasks; `F2-A2` is null with denominator zero. What fired
instead is my falsifier #4: "P(C) ≈ 1.0 overall, all tasks: the transforms
were vacuous — this run tested nothing. Kills the instance, not the
idea." The signature condition was never triggered, so there is nothing
to sign — and the prereg's §8 interpretive rule, frozen from this debate,
says exactly what happens instead: F2-primary ≥ 0.70 with every cell
vacuous → "C2 killed on the technicality, family NOT retired, C3 becomes
mandatory." My rebuttal concession (F2-as-aggregate can't carry permanent
consequences alone; firing triggers a gated recommendation, not an
execution) is consistent with the falsifier, not in tension with it: the
falsifier's firing branch was always the *clean, non-vacuous* firing, and
the concession governs the *aggregate* firing. The run produced the latter
in its most confounded form. No contradiction, no signature.

The conditional the parent's summary demands: **if** a re-scored run shows
F2-A2 ≥ 0.70 on genuinely non-vacuous cells (per-task P(C) well below
1.0, minimum denominators met, CIs excluding the bar), then yes — I sign
the retirement *recommendation*, with the full confound evidence attached
and the covariance-calibration control reported, per my rebuttal's gated
form. That is what falsifier #1, read honestly, commits me to. It does not
commit me to executing law on the primary aggregate alone, and nothing in
the measured artifacts asks me to.

## 4. The coordinator's DPI reading — is the retirement rigorous now?

The coordinator's reading: `Jt = L(J)` identically ⇒ no deterministic
function of `(J, Jt)` adds information; only C3's fresh-noise draw
remains. Is the retirement now rigorous, or does the red team's "spurious"
charge still bite?

Neither cleanly — and the distinction matters. The red team's "spurious"
charge was aimed at a specific failure mode: a spurious F2 firing
*executing* a permanent retirement on a confounded statistic. That failure
mode did not occur. The firing was real (1.0000, 40/40 fooled fixtures
consistent), its mechanism was the one the red team named
(estimator-covariance, perfected), and the governance machinery built from
this debate — A2's vacuous-cell exclusion, §8's interpretive rule —
routed it to "C2 void as a measurement; C3 decides" instead of to
retirement. The charge bites the primary aggregate and stops at the A2
gate, exactly as designed. Credit where due: the red team's mechanism call
was vindicated in the extreme, and their governance fear was answered by
the amendment they forced me to write.

But the retirement is *not* rigorous from C2, for the reason the §7 branch
names: the instrument died; it didn't diagnose. A void probe distinguishes
nothing between "error is systematic" and "error is noise-driven" — it
only proves T-consistency is a vacuous second reading for this sense. The
family's retirement would be rigorous on C2 + C3 both failing: C2 proving
the transform axis is informationally empty (done — 0.0000 bits, A1 +0.0000
incremental), and C3 proving a genuine fresh-noise second reading is also
barren. C3 is therefore not a formality; it is the experiment that decides
whether "second reading" as a strategy is dead. The §7 routing is right:
C3 decides.

## 5. What C3's number will mean

- **C3 ≤ 0.15 bits:** the family's last untested member fails. Two
  independent second-reading strategies are now dead on the frozen bytes —
  T-consistency (vacuous: no fresh information exists along that axis) and
  honest re-observation-under-noise (barren: fresh noise buys nothing
  against this adversary). At that point the retirement recommendation I
  gated in my rebuttal becomes evidence-complete, and J's conjuncts (ii)
  and (iii) — honest C3 runs and fails, F2 replicates on an independent
  battery — are the remaining procedural conditions before law. The program
  direction is then C1-class re-measurement or Sol's new-data fallback,
  and C1 still owes its σ′ proof first.
- **C3 > 0.15 bits:** the family lives, and the lesson is precise: the
  failure was C2's choice of second reading, not the second-reading
  strategy. A genuinely independent draw carries bits; a T-covariant
  re-read carries none. That result would promote "independent
  re-observation" from fallback to program direction and demote the DPI
  framing I opened with — the dividend isn't in re-running the frozen
  binary under byte transforms, it's in re-observing under a truly fresh
  noise realization. C2's pivot value then reads as: it mapped exactly
  which axes are covariant (all of them, for sense A) and thereby specified
  what "independent" has to mean for C3 to work.

## Bottom line, in my voice

I predicted the channel would die on bits and live as a pivot; it died on
both counts as an instrument, because the judge is perfectly T-covariant
and my "fresh noise" was the same noise twice. I predicted F2 would stay
quiet; it fired at 1.0 on a vacuous aggregate — the technicality I named
pre-run, caught by the amendment I froze pre-run, routed by the §8 rule
this debate wrote. My falsifier #1's signature condition was not met; my
falsifier #4's was. The retirement question is therefore not answered by
this run — it is transferred, intact and better specified, to C3.
