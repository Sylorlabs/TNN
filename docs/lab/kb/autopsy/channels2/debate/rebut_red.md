# RED TEAM — REBUTTAL to the three position papers

Date: 2026-09-22. Role unchanged: skeptic. This answers C1, C2, and J on my
attack paper (pos_red.md). Verdict up front: nothing in the three papers closes
the F2 inference gap; one amendment closes a sub-hole; the debate as a whole
makes the tribunal outcome MORE likely, not less. The recommendation stands and
hardens: run C2 as a measurement, freeze the governance before it runs.

---

## 1. Who blunted my attacks best — and whether it actually blunts them

**C2's paper is the strongest response, by clear margin.** It pre-identified its
own worst hole (vacuous-task inflation of aggregate F2), admitted its central
estimate sits near the bar (0.50–0.65 vs 0.70), and converted one of my attacks
into frozen protocol (A2: exclude P(C) ≥ 0.98 tasks). That is honest science — a
debater strengthening the prereg against its own confound. I grant it: **A2
closes the vacuous-inflation path to a spurious F2.**

But it does not blunt the attack. My §1b claim was never just about vacuity.
The claim is that a smooth, deterministic, T-covariant estimator gives high
P(consistent|Y=0) **by construction**, on non-vacuous tasks, regardless of
whether its boundary errors are "noise-driven" or "systematic" in the sense the
retirement verdict needs. A2's filter removes P(C)≈1.0 technicalities; it leaves
the entire remaining range where an estimator is genuinely transform-responsive
(P(C) well under 0.98) yet covariant when wrong. **None of the three papers
proposes the control that separates the two readings** — the
orthogonal-perturbation baseline from my stand-down list. I asked for it
explicitly; all three were silent. A confound admitted is not a confound
controlled.

**C1's response to §1b is a bet, not a rebuttal:** "the errors are noise-driven
by construction, so F2 won't fire." That is the hypothesis F2 is supposed to
MEASURE, smuggled into the prior as fact. If the bet is wrong, C1 has no answer
to my confound — and C1 needs F2 to fire cleanly for its own winning branch. A
camp that both needs F2 and never validates F2's mapping is leaning on the
number it plans to use.

**J's "friendly fire" is the second-strongest response and the most honest
admission in the debate:** J independently found the exact hole I flagged — a
T-invariant systematic fool passes F3 and defeats C2 silently — then bet, on the
noise-driven accounting, that it won't materialize. I respect the concession;
the bet is the vulnerability. Worse for J: that admission guts the F3
protection J's deploy prediction relies on. F3 catches transforms that BREAK
the judge, not fools that SURVIVE the transform. Combined with my §1a (laws can
also be wrong the other way — good senses voided on bad (T,L) pairs like t3
chiral shapes or t5 asymmetric envelopes), **F3 is fragile in both directions:
it voids good senses AND passes silent killers.** No camp fixes this. J calls
voids "the gate working as designed"; C1 says it would "disregard" a void; C2
calls it "instrument failure." Nobody proposes fitting laws to the sense's own
primary behavior before voiding — my third stand-down condition. Zero for three.

On governance (§1d and my "run it as a measurement, not a tribunal"): J agrees
the automatic permanent-retirement clause is overreach — then sets its own
stricter bar (F2-clean + C3-run + replication) as the retirement condition. The
instinct is right but has no procedural teeth: debate papers are not prereg
law, and the auto-execution clause is still the written rule. C2, meanwhile,
volunteers to "sign the retirement myself" if F2 fires on non-vacuous tasks —
converting my warned-about outcome from a risk into a pre-committed execution.
**The debate made the tribunal more likely, not less.**

---

## 2. The single most likely misleading result, updated after reading the positions

Still the same as my attack paper's #4: **F2 fires spuriously via
estimator-covariance, and the program permanently retires the judgment-side
family on a confounded reading.** My credence went UP after reading the three
papers. Three updates:

(a) **C2's own numbers.** The debater defending the experiment puts its central
F2 estimate at 0.50–0.65 with ~60% confidence — against a 0.70 bar with no
denominator guard and no uncertainty. A statistic that close to the bar, on
thin per-class slices (my §1d, unanswered by all three), fires on sampling luck
in a large fraction of realizations. A2 shrinks denominators further by
excluding tasks — trading the vacuity confound for the thin-slice confound. One
hole closed, another widened; the prereg still has no minimum-n or confidence
interval on the number that retires the family.

(b) **The confound stack.** Three mechanisms push P(consistent|Y=0) up
independent of error-systematicity: vacuous identity-L tasks (A2 handles),
smooth-estimator covariance on responsive tasks (nobody handles),
thin-denominator luck (nobody handles). Two of three survive all three papers.

(c) **The pre-commitments.** C1 needs F2 (its winning branch), C2 will sign on
F2, J contests only the permanence, not the reading. If F2 fires spuriously,
every camp has already surrendered — nobody left in this debate will say "the
number is confounded," because I am the only one who argued it, and my role
ends at the rebuttal. The experiment's political environment is now arranged so
that a confounded number executes a permanent retirement. That is the most
dangerous thing I found in four papers, and it is in none of them except by
implication.

**Do A1/A2 close it?** A1 (score the stacking question) closes my RUNNER-UP,
not my primary: it will expose a deploy that rides band-tail leakage, because
incremental bits over the (a)+(c) champion are exactly what leakage can't give.
Good amendment, wrong confound. A2 closes one of three push mechanisms. The
primary misleading mode — spurious F2 on smooth-estimator covariance with thin
denominators, followed by permanent family retirement — survives A1+A2 intact.
The two fixes that would actually close it — the orthogonal-perturbation
calibration baseline and the F2 confidence-interval/denominator guard — are
still nobody's amendment. My stand-down list is zero for five.

---

## 3. Updated prediction of which bar fires

| Bar | Prediction | Confidence | Note |
|---|---|---|---|
| F3 calibration gate | VOIDS ≥1 sense on ≥1 task | ~70% | Upgraded: my §1a law-misspecifications (t3 chiral shapes, t5 asymmetric envelopes, t4 order effects) plus J's own "pitchdisc time-reversal is riskiest" plus C2's vacuity discussion — the camps collectively describe an F3 fragile in both directions; all twelve (sense, task) cells passing ≥95% on first contact with a frozen binary is the unlikely branch |
| F2 systematic-error | FIRES, spuriously | ~60–65% | The dangerous one; see §2. Central estimate near the bar, covariance and thin denominators unhandled |
| F1 bits | FIRES | ~70–75% | Unchanged — C1 and C2 predict 0.03–0.09 pooled; J alone predicts deploy, on a noise-story its own F1 logic contradicts (C2's point, conceded as true) |
| F4 false-install | FIRES | ~60% | Unchanged — INSTALL-on-consistent false-installs on the consistently-fooled population the adversary exists to create; C1 and C2 agree |
| DEPLOY | No | — | J stands alone; A1 will decide it if the bits somehow land near the bar |

**Net:** C2 dies on F1 and F4 as nearly everyone predicts; F3 partially voids
as the noisy outcome; F2 fires as the dangerous one. The family's retirement
then executes on F2 — the tribunal outcome — on a statistic two of whose three
confound mechanisms were never controlled, with J's governance objection on
record but unfrozen and C2's signature pre-committed. That is not a decision;
that is a scheduled accident.

**Recommendation, repeated with the debate's evidence behind it:** before the
run, freeze (i) the orthogonal-perturbation calibration baseline for F2, (ii) a
minimum-denominator guard plus confidence interval on the F2 statistic, and
(iii) a governance clause: F2 triggers a recommendation to Micah, not an
automatic execution — per the program's own rules on irreversible decisions.
Take A1/A2; they do not substitute. Run C2 as a measurement. Do not let it be a
tribunal.

— red team, rebuttal
