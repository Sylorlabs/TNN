# H5 Debate — AGAINST the adjudicated position

Date: 2026-09-24. Task: defend the counter-position against the strongest
attacks. Pure argument from frozen evidence — no new experiments. Every
arithmetic claim below was re-verified from the raw per-run records in
`~/workspace/scratch-h5/sweep/` (A-run jsonl), recomputing accuracy from
`verdict==ground_truth`. Commit nothing.

## 0. Verified facts (from raw records, not from the summary docs)

| Claim | Re-derived from raw records | Status |
|---|---|---|
| Trap acc d1/d2/d4/d8/deep16/adaptive | 0/127, 42/127, 122/127, 127/127, 127/127, 127/127 | exact |
| Pooled acc | 750/877, 792/877, 872/877, 877/877, 877/877, 877/877 | exact |
| Trap mean rounds | 1.00 / 2.00 / 3.48 / 3.81 / 3.81 / 3.81 | exact |
| d4→d8 gain = 5 wason items (TRAP-C6-001..005) | wrong at d4 (4/7 evidence), right at d8; evidence_consumed=7, rounds_used=8 at d8/deep16/adaptive | exact |
| §6 early stops (adaptive rounds < deep16 rounds, item-wise) | admit 181/248, revoke 63/113, logic 3/264, trap 0/127, cost 40/125 | exact |
| Cap-hit rate (cap=1 in adaptive ledgers) | 0/877 | exact |
| Trap adaptive round lengths | 2:24, 3:18, 4:58, 5:22, 8:5 — all 100% evidence consumed | exact |
| Items per *actual* round on trap | d1→d2: 42/1.00 = 42.0; d2→d4: 80/1.48 = 54.0; d4→d8: 5/0.33 = 15.1 | exact |
| Pooled d1 = 750/877 | exactly = 750 non-trap all correct + 127 trap all wrong | exact |

## 1. Concessions (genuine, made up front)

1. **The pooled knee is the trap curve diluted.** Pooled d1 = 750/877 is
   exactly the 750 non-trap items all correct plus the 127 trap items all
   wrong. Four of five batteries are ceilinged at depth 1. A "pooled knee"
   is not a system property. Conceded in full.
2. **The doc's "knee at depth 4" was never the frozen rule's output.** The
   mechanical frozen rule (labeling fix pending) yields 8 on pooled and 16
   on traps — the 4 was eyeball-on-curvature, the 16 was a labeling
   off-by-one, and the truth was 8. The knee number was a mess. Conceded.
3. **The sensor is uncalibrated.** Confidence takes only 7 distinct values
   across all batteries ({400,500,700,710,764,800,1000}); ε=20 is in
   incomparable score units; "stable" ≠ "correct". Conceded.
4. **§6 was vacuous on traps.** 0/127 early stops — the margin honestly
   moved until evidence exhaustion, and a stability rule correctly refused
   to stop. Conceded, and used below as evidence FOR §6, not against it.
5. **§8.3's non-generalization caveat stands.** One harness, one item
   distribution, one score mechanic. The knee — and cap 8 — must be
   re-tested on harness variations. Conceded.
6. **k=3 cannot distinguish a mid-stream plateau from exhaustion.** This
   design never contained a plateau-then-flip. Conceded.

## 2. A CONSTANT is justified: cap 8 (answering attack (a))

Attack (a) says: the knee is set by evidence-set lengths (max 9 items) in
this distribution, not by deliberation; change the distribution, change
the knee; cap 8 is one distribution's accident; §8.3 concedes
non-generalization.

**Answer: this attack misunderstands what the constant is derived from.**
The constant I defend is not derived from the knee *curve*. It is derived
from the harness's longest natural adversarial run:

- Trap natural round-lengths (measured, adaptive): 2/3/4/5/8, set entirely
  by evidence-set sizes. Max observed: 8. Max possible: 9.
- Cap 16 never binds because no stream is longer than 9 items. Cap 8 binds
  no measured run either (longest is exactly 8 = evidence 7 + final
  elimination/refutation round).
- d8 achieves 1.000 on all 877 items; d4 leaves exactly 5/127 trap items
  wrong; d16 buys nothing.

So: **cap 8 is the minimal depth achieving 1.000 on every measured item,
and it sits exactly at the harness's longest natural adversarial run
length.** That is not an accident of the curve — it is a harness-derived
safety bound: cap ≥ longest natural run on the depth probe. If a new
distribution has longer evidence sets, the constant is *falsified in the
open, in one line* (an item hits the cap), and revised. That falsifiability
is a virtue, not a bug — it is exactly Micah's "when in doubt, test both"
made operational.

The attack's "nothing distinguishes 8 from 16 on this data" is true and
irrelevant: on this evidence-length distribution, any cap ≥9 is
behaviorally identical. The question is never "which of the identical
caps is truest" but "what is the *minimal safe* cap," and that is 8, with
a derivation that survives a change of distribution *better* than any
curve-derived knee: it points at the quantity to re-measure (longest
natural run), not at a sacred number.

**The off-by-one has a clean answer, not a reason to abandon constants.**
Fix the rule: the knee labels the *saturated state* at p, not the
*arriving interval*. Applied mechanically: trap saturates at 8 (the 16 was
the labeling error — note trap mean rounds are 3.81 at *both* d8 and
deep16, so nothing physical distinguishes them), pooled gives 8. The doc's
eyeball-4 then reads honestly as a *separate* quantity: the cost-efficiency
elbow (per-round returns decline 54.0 → 15.1 items/round, ~3.6×, past d4).
Constant for accuracy: 8. Elbow for cost: ~4. Two numbers, two purposes,
no contradiction — and no "envelope" needed.

Finally: "envelope" is not a setting. The harness ships a config value
somewhere. The adjudication's envelope *already contains* cap 8 ("saturation
at cap 8, ~3.8 mean trap rounds, d4 at 96.1%, the d4-vs-d8 choice = exactly
5 wason items"). I am not asking for a number the envelope forbids — I am
asking that the number the envelope already reports be given the status
its accuracy justification earns: the minimal depth proven safe on all
877 measured items. An envelope that reports 8 but refuses to enshrine it
defers the decision without improving it.

## 3. §6 suffices; the residual-flip bound adds nothing (answering attack (b))

Attack (b) says: the bound strictly dominates §6 on safety, fires no later
than §6 on easy batteries, preserves the 284/486 savings, and is
denominated in the decision-relevant quantity (leader-flippability).

**Answer in three parts.**

**Part 1 — The bound is well-defined exactly where it is unneeded.**
The bound's premise is a known, finite, pre-listed evidence stream whose
remaining items have bounded weights. In this harness, that is true — and
in this harness, all 127 trap adaptive runs already consumed 100% of their
evidence, so "stop on exhaustion" is the observed policy and the bound's
residual-flip half never fires before it. In open-ended deliberation —
the real architecture — "remaining evidence" is *undefined*, because the
system generates its own considerations. There the bound collapses to
"never stop early except on exhaustion" plus whatever heuristic it was
trying to replace. Well-defined where unneeded; undefined where it would
matter. That is not a stopping rule, it is a restatement of exhaustion.

**Part 2 — The bound's firing set is empirically identical to §6 ∪ natural
termination.** On the easy batteries, the attack correctly notes the bound
would fire where contenders are eliminated (conf=1000) — but §6 already
fires there too: conf clamped at 1000 with no hypotheses left to move the
margin means zero gains, i.e., gains < ε for 3 rounds. The 284/486 §6
firings (181 admit, 63 revoke, 40 cost) all carried zero accuracy loss vs
deep16 — verified item-wise against the raw records, and adaptive == deep16
accuracy (1.000) on all five batteries. On conflict streams, §6 correctly
refused to fire while the margin honestly moved (0/127 — the behavior the
attack's own authors praise). So on every measured battery, the bound's
firing set ⊆ {§6 firings ∪ natural terminations}. New rule, same behavior,
more code, zero measured delta. And on the one point where the attack
claims the bound *would* differ (firing before exhaustion mid-stream on
insurmountable leader) — that is the eliminated-contender case where §6
fires anyway via conf=1000 → gains of 0. There is no measured item where
the bound stops earlier than §6 and later than §6's correctness requires.

**Part 3 — The sensor critique is real but mis-aimed.** I concede the
sensor is uncalibrated (§1.3). But the attack concedes — its own words —
that on traps §6 was vacuous *by correctness*: no tighter ε or smoother
score would have created safe early exits there, because the margin was
honestly moving. So the sensor's calibration is not the load-bearing
quantity for the trap policy at all; the load-bearing quantity is
evidence exhaustion, which the harness already implements. Recalibration
is worth doing *for the cost heuristic on easy items* (thresholds should
mean something), not as a prerequisite for safety. Adopting the bound as
law now means enshrining an untested rule — the adjudication's own
undecided Q3 admits the bound "is a paragraph in the adjudication, not
code; no firing data exists." §6, by contrast, is tested on 877 items
with byte-identical A/B reruns and zero accuracy loss wherever it fired.
Keep the tested rule; recalibrate the sensor as a separate, honest
experiment.

## 4. ADAPTIVE-WINS stands prereg-valid; no new battery is needed
(answering attack (c))

Attack (c) says: the delayed-disconfirmation battery is the one input
class the frozen design never contained; one battery, three decisive
branches (wrong-plateau stop / overthinking flip / exhaustion confirmed).

**Answer: decisive ≠ informative.**

**The plateau-then-flip branch is a theorem, not an experiment.** Any
fixed-k stability rule is defeatable by a (k+1)-round plateau *by theorem*:
the encoder simply builds a k+1-round wrong plateau. The battery therefore
tests the encoder's ability to defeat §6, not a property of deliberation.
And the *overthinking* branch cuts against the program's own evidence:
the sweep shows monotone convergence on all 877 items, and the wason
mechanics prove depth = evidence consumption (4/7 seen → wrong, 7/7 seen
→ right). A matched set where late evidence flips correct→wrong measures
the encoder's malice budget — how adversarial can we make a single item —
not the system's stopping policy. Hand-building adversarial existence
proofs cannot supply what actually matters for an operating envelope:
the **base rate** of plateau-then-flip in natural evidence streams.
That requires harness variations with different score mechanics and
longer/noisier streams — which is §8.3's stated generalization gap, not
a bespoke attack battery.

**The prereg criteria are met mechanically and need no rescuing.**
|acc_adaptive − acc_deep| = 0 ≤ 1pt on all five batteries; mean rounds lower
on 4 of 5 (admit 54%, revoke 34%, logic 2%, cost 12%; trap 0% where §6 was
correctly vacuous — the verdict never required savings there); censoring
0/877 ≪ 1/3. The verdict is prereg-valid. "§6 might have stopped in a
wrong plateau" is a true statement about a counterfactual battery, and
it is exactly as true of *any* fixed-k rule including the proposed bound
(plateau the margin for k+1 rounds and any stability-flavored rule eats
it). If the worry is universal to stopping rules, it is not an argument
for re-running *this* verdict — it is an argument for the distributional
base-rate experiment, which is the same harness-variation work both
sides agree is the real open question (§4.1).

**Opportunity cost is the deciding vote.** The same effort spent on §8.3's
stated gap — different score mechanics, longer/noisier streams, different
item distributions — gives distributional evidence on whether
saturation-at-8 and ~3.8 mean trap rounds replicate, which is the actual
open question (§4.1). The bespoke battery gives a guaranteed existence
proof we already have by construction plus a malice-budget measurement.
Spend the runs where the evidence can surprise us.

## 5. What I held, what I conceded

**Held:**
- Cap 8 as the minimal safe depth constant: 1.000 on all 877 items, the
  smallest depth that achieves it (d4 provably leaves 5/127 trap items
  wrong), d16 buys nothing (trap rounds 3.81 at both d8 and deep16).
- The off-by-one is fixed by relabeling the saturated state at p, not by
  abandoning constants; the doc's 4 reads honestly as the separate
  cost-elbow (~3.6× decline in items/round past d4: 54.0 → 15.1).
- §6 suffices: on all measured data the bound's firing set is identical
  to §6 ∪ natural termination; the bound is undefined in open-ended
  deliberation and a restatement of exhaustion in finite streams.
- ADAPTIVE-WINS is prereg-valid without a new battery; the
  plateau-then-flip battery is a theorem-guaranteed adversarial existence
  proof (defeats any fixed-k rule by construction) that cannot supply
  the base rates that actually matter.

**Conceded:**
- The pooled knee is the trap curve diluted (750/877 = exactly
  non-trap-correct + trap-wrong); four batteries are ceilinged at d1.
- The "knee at 4" was never the frozen rule's output; the knee number was
  a three-way mess (4 rhetoric / 8 pooled / 16 off-by-one), truth was 8.
- The sensor is uncalibrated (7 distinct values, ε in incomparable units).
- §6 was vacuous on traps by correctness; k=3 cannot distinguish plateau
  from exhaustion; §8.3's non-generalization caveat stands — cap 8 must
  be re-tested on harness variations.

**The single strongest remaining reason a constant (not an envelope)
should be law:** a shipped system needs a concrete cap value, and the
envelope position cannot name a better one. The adjudication's envelope
already reports "saturation at cap 8" as its accuracy anchor — the only
disagreement is whether that number gets the status its evidence earns.
Cap 8 is the *minimal depth proven safe on every measured item* (d4 is
provably unsafe on the one battery that actually probes depth; 16 buys
nothing), and — unlike any curve-derived knee — it is *falsifiable in
the open*: the next battery either holds 1.000 at cap 8 or hits the cap
and falsifies it in one line. An envelope absorbs everything and predicts
nothing; a constant takes a position the next experiment can kill. That
is the posture the program's own testing standards demand.
