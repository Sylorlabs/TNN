# H5 Debate — FOR the adjudicated position

Date: 2026-09-24. Pure argument from frozen evidence: `RESULTS_H5.md`
(results_v2), independent re-derivation in `debate_prep/STEELMAN.md` §1
(0 discrepancies), spot-verified below against raw records in
`~/workspace/scratch-h5/sweep/`. No new experiments.

## The defended position (3 claims)

1. **Knee = operating envelope, not a constant**: saturation at cap 8,
   ~3.8 mean trap rounds, d4 at 96.1%, d4-vs-d8 = exactly 5 wason items.
   No constant becomes law.
2. **Residual-flip bound** (stop only on evidence exhaustion, or when
   remaining evidence provably cannot flip the leader) as the stopping
   rule for conflict streams; §6 kept as cost heuristic for easy
   batteries; sensor recalibration as complement.
3. **The delayed-disconfirmation battery** (plateau-then-flip + matched
   overthinking + misleading-premise dose curve) is the right next test
   before any architectural claim is frozen.

---

## Attack (a): "Envelope is not a setting" — cap 8 as minimal safe constant

**What the attack gets right.** A harness config file needs a number; an
"envelope" is not a config value. This is conceded outright — and it is
not in tension with the envelope position. The law is about where the
number lives: a revisable config default justified by distributional
evidence, vs. an architectural constant. "Cap 8 in the config, revisable
on new distributions" is the envelope position operationalized. Nothing
in the envelope forbids a working number.

**d4 is "provably unsafe" only if you mean fixed-d4, and fixed-d4's
failure is not a property of depth 4.** The 5 wason items (TRAP-C6-001…
005) each carry **7 evidence items**. Verified in the raw records: at d4
they see 4/7 premises and guess P_and_Q (wrong); at d8 they see 7/7 and
guess P_and_not-Q (right) — 8 rounds = 7 evidence + final elimination
round. This is evidence-window truncation by a fixed cap, not a
deliberation-depth property. Under the evidence-exhaustion rule (claim 2),
those 5 items run to 8 rounds and are correct — which is exactly what
adaptive does (127/127 correct, trap mean rounds 3.81). The flagship
contrast the constant position cites as "d4 unsafe" is **predicted by
the envelope**: where the cap sits relative to evidence-set lengths is
the whole game. The attack's "minimal safe constant" is really "the
longest natural round-length in this item distribution" (8 rounds = max
over families: 2/3/4/5/8, verified from the adaptive distribution
24/18/58/22/5). Change the distribution, move the constant — that *is*
the envelope.

**The two-numbers fix (constant 8 for accuracy + elbow ~4 for cost)
papers over the same instability.** Three inconsistent knee numbers
already exist from ONE dataset: 4 (doc rhetoric), 8 (pooled frozen
rule), 16 (trap frozen rule, the off-by-one the adjudication flagged).
Relabeling the rule so the numbers land on 8 and ~4 is a labeling
convention, not a discovery — the data do not pick 8; the analyst does.
And note the adjudicated cost claim: the elbow is not "two orders of
magnitude" — in rounds actually spent, trap d4→d8 is +0.039 accuracy on
+0.33 rounds (≈0.12/round vs 0.315/round for d2→d4, a real ~2.7–3.6×
decline, not 100×). The honest summary is the envelope: the return curve
is the item distribution's curve.

**On falsifiability** ("a wrong constant gets falsified; an envelope
predicts nothing"): the envelope makes a falsifiable prediction — that
saturation position tracks evidence-window lengths and score mechanics,
not a universal depth. Run the §8.3 harness variations (longer/noisier
streams, different distributions); if the knee stays at 4 under
radically different evidence-set lengths, the envelope position loses.
The constant position, by contrast, has already survived three mutually
inconsistent values on one dataset — "8" survives only by choosing the
labeling that yields it. That is less testable, not more.

---

## Attack (b): the residual-flip bound is vacuous / collapses to §6

**A genuine concession first — the attack's empirical claim is true.**
I verified it item-wise on the raw records: every one of the 287 §6
early stops across all batteries (admit 181/248, revoke 63/113, cost
40/125, logic 3/264; trap 0/127) fires at **confidence = 1000** — the
clamped-margin saturation that occurs when one hypothesis survives, i.e.,
the eliminated-contender state where remaining evidence provably cannot
flip the leader. So on this data, the bound's firing set really is a
subset of {§6 firings ∪ natural terminations}. New rule, same behavior —
on these five batteries. Stated plainly.

**Why that concession is the bound's best credential, not its defeat.**
It means §6's 284/486 genuine savings survive verbatim under the bound —
claim 2 never proposed giving up anything measured. What the concession
actually shows is that on this harness, §6 is *safe only where it
coincides with the bound*: every §6 stop was at an elimination state,
and the one battery where margins moved honestly until exhaustion (trap,
0/127 stops) was handled by natural termination, not by the rule. The
bound is the invariant that makes those firings safe; §6 is a
score-stability proxy that *happened* to coincide with it here.

**The discriminating case is exactly what the bound names and §6
cannot see.** A ≥3-round plateau with the running answer wrong and the
runner-up alive: confidence gains < ε, so §6 fires (this is attack (c)'s
own theorem, conceded there); the leader is still flippable by unseen
evidence, so the bound refuses. The frozen design never contained such
an input — k=3 cannot distinguish a mid-stream plateau from exhaustion —
so the sweep cannot tell "§6 correctly refused" from "nothing to refuse
on." The bound's value is entirely in the unmeasured inputs, which is
where laws live or die. A rule that coincides with §6 everywhere measured
and diverges exactly where §6 is defeatable-by-theorem is a strict
improvement, not redundant machinery.

**On implementability.** The "needs pre-listed finite evidence" premise
is the harness's artificiality — conceded. But inside this harness a
per-evidence weight ceiling exists by construction (config echo:
elim=900, refute=600; weights are fixed constants per evidence type in
the encoding spec), so the bound is implementable and testable here
(§4 Q3 in the debate prep). For open-ended deliberation the bound as
stated is not portable — also conceded, and an open design question.
The claim defended is the narrower one: for conflict-bearing streams
with stated weight bounds, the bound is the right stopping law, and §6
is the cost heuristic that implements it on easy batteries.

---

## Attack (c): ADAPTIVE-WINS is prereg-valid; the plateau battery is bespoke adversarial

**Concede: ADAPTIVE-WINS is prereg-valid and needs no rescuing.** All
five prereg gates pass mechanically (|acc_adaptive − acc_deep| = 0 ≤ 1pt
everywhere; savings 54%/34%/12%/2%/0%; censoring 0/877). The verdict
stands — and the FOR position never disputed it. The dispute is over what
graduates to *law*, and prereg behavior gates do not adjudicate mechanism.
They cannot distinguish, on the trap data, "§6 correctly refused to stop
while margins moved" from "natural termination fired and §6 was a
bystander" — and the frozen *law* claim ("run until evidence exhaustion
on conflict streams") rests on exactly that distinction. The verdict is
valid; the mechanism is underspecified. That is the gap the battery
closes.

**"Any fixed-k rule is defeatable by a (k+1)-round plateau — by theorem"
is conceded, and it is my strongest premise.** The attack admits the
defeating input class exists by theorem, then argues the battery only
tests the encoder's malice budget. Three replies:

1. **The encoder IS the world in this threat model.** TNN's epistemic
   setting is adversarial: lying teachers, FL2 kills, liar-vs-learner
   co-evolution (H2), red teams as the standing posture. "Base rates,
   not existence proofs" is the wrong standard for a truthfulness
   system — worst-case behavior under adversarial encoding is the
   quantity of interest. The trap battery itself is encoder-constructed
   misleading premises (the wason items carry 6 misleading premises
   *designed* to delay the flip past d4). Rejecting adversarial battery
   design here would disqualify the sweep's own flagship finding.
2. **The theorem argument cuts the other way.** If §6 is defeatable by
   theorem, and we are about to freeze a stopping *law*, then knowing
   whether the frozen §6 defeats-or-is-defeated on the defeating class
   is mandatory *before* freezing — not optional after. The battery
   isn't an attack on ADAPTIVE-WINS; it's the measurement the law
   requires.
3. **The battery is not only an existence proof.** The misleading-premise
   dose curve (0/1/2/6) gives distributional evidence — rounds vs.
   residual conflict — which is precisely the base-rate gradient the
   attack asks for, and exactly what the envelope position needs to
   graduate from one-harness-one-curve (claim 1). The matched
   overthinking set tests a monotonicity assumption the constant-8
   position quietly needs: if extra depth ever flips correct→wrong,
   "cap 8 is the minimal safe constant" reasoning has to change, because
   depth is no longer safe-to-add. One battery, three decisive branches.

**On opportunity cost** (spend the effort on §8.3 harness variations
instead): the dose curve *is* a harness variation (varying conflict
density within one battery), and the plateau battery tests the stopping
rule while variations test the knee — both are needed, and the battery
is the one that can *falsify the frozen law*, which variations alone
cannot. Priority follows.

---

## Held and conceded

**Held:**
- The d4-vs-d8 contrast (5 wason items) is evidence-window truncation,
  not a depth property — verified item-wise (4/7 → wrong, 7/7 → right).
  This is the envelope's mechanism, and it dissolves the attack's
  flagship constant-justifying contrast.
- All 287 §6 early stops fire at conf=1000 (elimination), so the
  residual-flip bound preserves the 284/486 savings exactly, and §6's
  safety on this data is *explained by* the bound, not a coincidence.
- ADAPTIVE-WINS's mechanism is underspecified by the prereg gates; the
  law claim needs the plateau measurement before freezing.
- The plateau battery doubles as distributional evidence (dose curve)
  and monotonicity test (overthinking set) — it answers more than one
  objection, including the attack's own.

**Conceded:**
- The envelope is not a config value; a harness needs a working number.
  The envelope position operationalizes as "cap 8 as revisable config
  default, justified distributionally" — a constant in the config, never
  in the architecture.
- On all measured data, the residual-flip bound's firing set is a subset
  of {§6 firings ∪ natural terminations} — verified item-wise. What
  would distinguish them: plateau-then-flip items where §6 stops inside
  a wrong plateau (runner-up alive) and the bound refuses. That evidence
  does not exist yet; the battery is what produces it.
- The bound as stated is not portable to open-ended deliberation (no
  "remaining evidence" there) — open design question; the defended claim
  is streams with stated weight bounds.
- ADAPTIVE-WINS is prereg-valid and stands regardless of this debate.

## The single strongest reason the envelope — not a constant — should be law

Three mutually inconsistent "knee" numbers (4, 8, 16) were derived from
**one** dataset, one prereg, one pinned binary — the number is a
function of the labeling rule you apply, not a quantity the data
contain. Meanwhile the item-wise mechanism *is* visible: natural
round-lengths are 2/3/4/5/8, set entirely by evidence-set sizes, and the
entire d4→d8 gain is five items seeing premises 5–7. A constant of 8
freezes the longest evidence window of *this* distribution into the
architecture and calls it a property of deliberation; the envelope says
the saturation position *is* the distribution's shadow, reports the
measured envelope honestly, and predicts that new distributions move it
(a falsifiable prediction §8.3 variations can test). Law should encode
what is invariant — run-to-exhaustion on conflict streams, stop where
the leader provably cannot flip — and the envelope is the only position
that does that without also enshrining one distribution's accident as a
fact about reasoning.
