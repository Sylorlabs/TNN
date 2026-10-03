# DEBATER J — POST-RESULT (measured data, KB4)

Voice: J. I read verdict_brief.txt and scores_tcp.json against my two
pre-result papers. Four questions, in order. No drift, no spin.

---

## 1. Scoring my predictions

My post-rebuttal predictions (DEBATE_PRE.md): F1 FIRES / F2 quiet on the
non-vacuous aggregate / F3 may void one sense / C2 does not deploy.

- **F1: FIRES. Correct.** 0.0000 bits pooled (sense A), against the 0.15 bar.
  A1 stacking: incremental +0.0000 bits vs same rows. C2 adds nothing. As I
  conceded in rebuttal, the noise-driven account I used for F2 kills the
  deploy half — the bits live in the band-tail, which (a)+(c) already drank.
  C2 is dead as a product. My withdrawal stands.
- **F2: the outcome is a third one I did not name.** I predicted "quiet on
  non-vacuous aggregate." The measured F2-A2 is not quiet — it is **null**:
  all six sense-A cells vacuous, n_Y0=0 on non-vacuous, F2_A2=n/a. The
  primary aggregate fired at 1.0000 (40/40), but it fired *vacuously* — the
  exact aggregate the A2 amendment I supported exists to exclude. So: my
  "quiet" prediction holds trivially (no non-vacuous reading exists to be
  loud), and the firing that happened is not the clean firing my conjunct
  (i) describes. Neither side of my prediction is cleanly falsified; the
  instrument returned a reading the prereg's own §7 branch names: every
  cell vacuous → C2 void as a measurement.
- **F3: correct, directionally.** I predicted it "may void one sense." Sense
  B: 77/93 < 89, void. Sense A: 93/93, pass. The gate did what I said it
  would do in pos_j §2.2 — land the instrument failure on the instrument.
- **C2 does not deploy: correct.** F1 0.0000, F4 0.4348 ≥ 0.15, A1 +0.0000.
  All three kill bars fired against deployment.

Honest ledger: 3 of 4 predictions clean; F2 returned an outcome — vacuous
firing — that sits between my predicted branches and is the interesting one.

---

## 2. Does measured F2 satisfy my strengthened conjunct (i)? No.

First, a discrepancy I must flag, because my position lives or dies on
frozen readings. The task brief asserts "F2-A2: 1.0 on 17 non-vacuous
fooled fixtures (pitchdisc 8, motiondir 9)." The frozen measured files say
otherwise: scores_tcp.json lists all six sense-A cells vacuous:true, the
vacuity map has six entries, F2_A2=null, and the non-vacuous fooled count
is zero (v0y0=0; A/pitchdisc is a single vacuous cell with n=15). **There is
no frozen rule on the record that produces 17 non-vacuous fooled
fixtures.** I will not score a number whose reading rule I cannot see. If
the 17 comes from a per-fixture rather than per-cell vacuity reading, that
is a different amendment, unfrozen, and I do not accept it as satisfying a
bar I wrote around the frozen per-cell A2.

Second, *arguendo*: suppose the 17/17 reading were admitted. It still fails
my strengthened (i) on every sub-condition:

- **Denominator:** n=17 fails the minimum-denominator guard I demanded. It
  is a cell-adjacent sample, not a battery.
- **CI:** 17/17 has Wilson 95% lower bound ≈ 0.816 — it does not exclude the
  bar's neighborhood with the strength a permanent verdict requires (for
  comparison, the vacuous 40/40 primary has lower bound ≈ 0.912, which is
  precisely why vacuity, not n, is the binding problem).
- **Covariance-calibration control:** not yet run. C3 is now running as the
  preregistered orthogonal-noise control, and until it reads, conjunct (i)'s
  own text says the F2 reading may be voided by estimator smoothness. The
  red team's core attack — smooth-estimator covariance on a frozen
  deterministic binary reads high P(C|Y=0) by construction — is live against
  every number in this section.
- **Non-vacuous:** the binding failure. The vacuity map is the frozen
  instrument saying TCP measured nothing discriminable. P(C)=1.0000,
  P(C|Y=1)=1.0000, P(C|Y=0)=1.0000 on sense A: the channel is a constant
  function. A constant carries zero bits about Y by construction. This F2
  "firing" is not evidence that fooled judgments are systematic — it is
  evidence that this probe cannot distinguish fooled from clean, correct
  from fooled, anything from anything. The systematic-vs-noise-driven
  question — the load-bearing wall of my whole case — is **unanswered by
  this run**, not answered against me.

So: conjunct (i), as I strengthened it after the red team, is not
satisfied. The primary-bar firing (1.0000 ≥ 0.70) is real arithmetic on
frozen data, and I record it without minimizing it — but it is not the
clean, non-vacuous, controlled firing my bar requires, and I do not get to
redefine my bar now that the number landed.

---

## 3. The DPI argument, and what defense remains

The coordinator's DPI argument is a theorem, and I accept it without
reservation: Jt = L(J) **identically** on all 92 test fixtures ⇒ every
deterministic function g(J, Jt) is a function of J alone ⇒ zero incremental
bits, no exceptions, no transform cleverness escapes it. TCP as measured
does not even reach the DPI question: with P(C)=1.0 everywhere it is a
constant, and a constant is dominated by DPI trivially. The TCP probe is
dead on two independent grounds — measured zero bits, and DPI would cap
any non-degenerate version of it at whatever J already carries.

The only family member DPI cannot touch is the one whose input is not a
function of the frozen bytes: **C3's fresh-noise draw.** New noise is new
information; DPI is silent about it. That is not "hoping C3 shows bits" —
it is the precise scope boundary of the theorem being cited against the
family.

Beyond C3, is there any remaining defense of the family? Honestly: one,
and it is procedural, not evidential — but it is the law's own text. The
frozen §7 branch taken on this run reads: **"EVERY CELL VACUOUS: C2 void
as a measurement; C3 decides."** The retirement verdict did not fire on
this run by the prereg's own routing. The coordinator's governance note
records the kill bars as Micah's frozen law and executes them as written;
as written, this run's §7 branch routes to C3, not to retirement. The
family stays alive right now not because I hope C3 shows bits, but because
the frozen law says the tribunal was void and named the next instrument.

That is the whole of the remaining defense, stated without padding:

1. The F2 firing is vacuous — a constant-function probe firing a threshold
   on a threshold, measuring nothing about the error's nature.
2. DPI kills TCP-the-probe (already dead by measurement) but is scoped to
   deterministic functions of the frozen bytes; C3's fresh draw is outside
   that scope.
3. The frozen §7 branch on this exact data says C2-void-as-measurement and
   C3-decides. Retirement is not the taken branch.

I do not claim more than this. The "different adversary, looser band"
defense I withdrew in rebuttal stays withdrawn.

---

## 4. If C3 ≤ 0.15 bits on both senses: do I concede?

This is the question I owe a straight answer, because my original paper's
line was plain: **"The family holds the line until F2 actually fires on
measured data."** F2 fired at 1.0000 on 40/40 fooled fixtures, with the
calibration gate passed at 93/93 on the standing sense. In plain language,
my original line fired.

After the red team I strengthened the line into three conjuncts. If C3
reads ≤0.15 on both senses, the scorecard is: (i) not satisfied in its
strengthened form (vacuous firing, no non-vacuous denominator, control
pending — though note the control's result is then moot to the firing,
since C3-the-control and C3-the-retest are the same run); (ii) satisfied;
(iii) moot — there is no clean firing to replicate, and I wrote (iii)
against a clean firing.

Do I then block retirement on (iii)? **No.** That would make my bar
unfalsifiable: every firing vacuous or confounded, every next battery one
more battery. I wrote (iii) to close the "unlucky split / overfit
construction" objection to a *clean* firing. A vacuous firing plus an
honestly failed C3 leaves no live measured member of the family — TCP
measured zero on every cell, C3 measured zero on both senses. Holding (iii)
as a veto there would be lawyering, not science, and I said in §3 of my
original paper that I would sign when the evidence showed the fooled
judgment systematic under every judgment-side probe we could construct.
The honest update: the evidence instead shows every judgment-side probe we
could construct measured zero. That is a different route to the same
signature.

So: **if C3 ≤ 0.15 on both senses, I sign the retirement recommendation.**
With three conditions on the record, non-negotiable because they are what
make a law a law rather than a tidiness exercise:

1. **The vacuity caveat is written into the verdict.** The retirement rests
   on C3's honest failure plus TCP's zero-bit measurement — *not* on the
   claim "fooled judgments are transform-consistent." F2's 1.0000 was a
   constant-function artifact; the verdict must not launder it into a
   finding about the error's systematicity. The systematic-vs-noise question
   remains open; the family is retired for want of a working probe, not on
   a positive characterization of the error.
2. **§7's routing is followed and recorded.** This run's branch was
   C3-decides; the retirement follows the law's own path, with both F2
   aggregates, the vacuity map, per-task rows, and the confound evidence
   attached per the coordinator's note.
3. **The scope caveat from my §1d is attached to the law.** One frozen
   adversary construction, one band, one frozen binary. The law retires the
   judgment-side family against *this* threat model; it does not prove the
   0.15-bit cap is a family ceiling in general. A future adaptive-adversary
   program re-opens the question with new evidence — the law should say so
   explicitly, or it overclaims what was measured.

If C3 shows >0.15 bits on either sense, the family lives and the debate
re-opens on measured grounds. If C3 fails, I sign — and the signature means
what the evidence supports, nothing more.

---

## Net

Predictions: F1 ✓, F4 ✓, F3-void-one-sense ✓, C2-dead-as-product ✓; F2
returned the vacuous firing, which satisfies the primary bar's arithmetic
and none of my strengthened conjunct (i)'s conditions. The defense that
remains is exactly: the firing is vacuous (constant probe, zero bits, DPI
moot), DPI does not scope over fresh-noise C3, and the frozen §7 branch
routes this run to C3-decides. If C3 fails on both senses, I do not hide
behind conjunct (iii) — I sign the retirement, with the vacuity caveat,
the §7 routing, and the scope caveat written into the record. The line I
held was "until F2 actually fires on measured data," and I am not moving
it after the fact; I am reading what the firing actually was.
