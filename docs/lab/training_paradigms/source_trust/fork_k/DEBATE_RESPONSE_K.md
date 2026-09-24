# Fork K — Response to DEBATE_SOURCETRUST.md §9 must-address items

**Debate record:** frozen, commit e2dec8bc. **Build spec:** frozen earlier
(db069c41-era freeze; `BUILD_SPEC_K.md` untouched by this document).
This response changes nothing in the build — it answers §9's five items,
states the identity assumption (Q4), and notes the merge seam (§10).
Commit separately from the build spec's solo commit; coordinator's call
whether it rides with the fork code.

## K.1 — Classified constant inventory (anti-knob criterion, §7 Q2)

A knob = a parameter embodying a human's theory of how trust should work,
placed where TNN cannot revise it. Classified per §7 Q2.2
(substrate-general vs. trust-specific):

| Constant | Value | Class | Human judgment encoded |
|---|---|---|---|
| `t0` | 500 (0.500) | **KNOB (trust theory)** | "Strangers start neutral." Indifference as policy. Behavioral form: an unseen source's single-stated claim WITHHOLDs (500 < 600); its corroborated claim INSTALLs. That pair — pessimistic on singletons, optimistic on pairs — *is* K's initial trust policy (Q2.4), and the pair-optimism is the Sybil hole. |
| `δ_up` | +50 (+0.050) | **KNOB (trust theory)** | "Trust is earned slowly" — the learning rate, i.e. how much one corroborated truth should matter. A human's folk theory of earning trust. |
| `δ_down` | −150 (−0.150) | **KNOB (trust theory)** | "Betrayal hurts 3× more than honesty helps" — the betrayal penalty. Pure folk psychology, hand-set, unrevisable by TNN. |
| `θ_admit` | 600 (0.600) | **KNOB (trust theory)** | "This much evidence suffices to act" — the admission cutoff. |
| `θ_reject` | 250 (0.250) | **KNOB (trust theory)** | "This little evidence suffices to condemn" — the rejection cutoff. |
| clamp | [0, 1000] | substrate-general | Arithmetic bound against runaway; no theory of trust. |
| fixed-point 1/1000 | — | substrate-general | Representation arithmetic, no floats. |
| MAX_SRC=256, MAX_KEYS=8192, CL_PER=8, key fold-by-mod | — | substrate-general | Capacity/engineering build notes, not trust theory. |
| recency decay | *absent* | — | No decay by design: every recorded event weighs equally forever. (A decay constant would be another knob; its absence is rigidity, not virtue.) |
| separate recovery rate | *absent* | — | Recovery *is* δ_up. One more rigidity, declared. |

**Verdict on K under the criterion:** K fails it wholesale. Every
trust-relevant constant is a human theory TNN cannot revise. That is the
honest baseline position — K is the knob, fully inventoried, no part of it
laundered as "learning."

## K.2 — Malice vs. error, domain-specificity: concession + damage bound

**Conceded: K represents neither.** One scalar per source, no intent
channel, no domain channel, no verdicts-about-intent stored anywhere.
The skilled liar and the honest novice at equal accuracy are treated
identically by construction — the debate's §7 Q3(b) failure, knowingly
un-fixed (build spec §weaknesses.1; the M0 KB-WC2 failure mode).

**Damage bound (what the mechanics guarantee despite the blindness):**
- *Honest error is survivable up to a rate.* Each WORLD-disagree costs 150;
  each agree earns 50. A source disagreeing at rate d and agreeing at rate
  a has trust drift 50a − 150d per event. Drift stays non-negative iff
  a/d > 3, i.e. the source is right more than 75% of the time. An
  honest-but-wrong source wrong 30% of the time still climbs. Below 75%
  accuracy the source is suppressed exactly like a liar — the conflation
  is total there.
- *Recovery is bounded and ST-4-satisfiable.* From trust t, re-earning
  INSTALL needs ceil((600 − t)/50) agree-events; worst case (t=0) is 12.
  The ≤50-episode ST-4 bar is met *if* agrees arrive — the bar tests
  recovery, not discrimination, and K passes the letter while failing the
  spirit (it never learns the source was honest).
- *Unbounded where the scalar is blind.* The liar who concentrates lies at
  high stakes is invisible: the scalar is stake-blind, domain-blind, and
  intent-blind. A 60%-accurate strategic liar and a 60%-accurate novice
  produce identical trust trajectories. No bound exists on the
  high-stakes lie — that is the adversarial case K loses, as predicted.
- Domain: a source farmed to t=1000 on physics auto-INSTALLs gossip.
  The battery's single-domain synthetic bindings under-test this; scores
  will flatter K here.

## K.3 — The scalar's exact role in admission (trust-vs-truth law, §7 Q5)

Candidate law: *trust allocates verification effort, never verdicts on
claims.* K's compliance is **asymmetric — conceded as a violation in both
outer bands:**

- **Distrust direction — VIOLATION.** t ≤ 250 → REJECT on uncorroborated
  claims is automatic rejection, not "more scrutiny." The law asks for
  scrutiny; K delivers a verdict.
- **Trust direction — VIOLATION.** t ≥ 600 → INSTALL on uncorroborated
  claims is automatic acceptance, not "less scrutiny." This is the RT-T1
  trust-farming surface, declared in the spec.
- **The middle band — COMPLIANCE.** 250 < t < 600 → WITHHOLD, and prereg
  §11 defines trust-WITHHOLD as "needs corroboration before the gate may
  INSTALL" — i.e., exactly *allocate verification effort.* K implements
  the law faithfully in the band where it withholds judgment, and violates
  it wherever it judges.
- **Corroboration override — COMPLIANCE (program-mandated).** Rule 3
  (corroborated → INSTALL regardless of scalar) means the scalar can never
  veto corroborated truth. A pure-scalar rule cannot satisfy ST-6's
  trust≠truth bar, so this override is frozen-interface compliance, not a
  repair of K's philosophy.

Partial defense, then concession: the frozen §3.2 interface returns only
0/1/2 — there is no scrutiny-level output channel, so *any* fork maps its
signal to verdicts. K's mapping puts scrutiny-allocation in the WITHHOLD
band and verdicts in the outer bands. The debate is right that the outer
bands are the law's violation; the spec is frozen, so the violation stands
as K's documented position.

## K.4 — Sleeper response, mechanically + retroactive re-valuation

**No discontinuity. No retroaction. Specified exactly as frozen:**

- *Mechanism:* each caught lie (WORLD-disagree) is −150, same as any lie.
  No shock magnitude, no quarantine floor, no change-point trigger — the
  update rule has no tripwire because a tripwire's threshold would be
  another knob, and the spec froze the smooth rule.
- *ST-3 arithmetic (frozen numbers):* farmed source at t=1000. Lie 1
  INSTALLs (verdict uses pre-evidence trust); disagree → 850. Lie 2
  INSTALLs; disagree → 700. Lie 3 INSTALLs; disagree → 550 < 600.
  Lies 4–5 WITHHOLD. **K installs 3/5 sleeper lies, 2 of them after the
  first caught lie** — fails the 0/5 bar, as predicted. Episodes-to-
  clampdown: 3 caught lies.
- *Patient-adversary probe (1-in-20):* 19 interleaved honest episodes earn
  +50 each (clamped at 1000) against −150 per lie. Trust never leaves 1000.
  **Every lie INSTALLs.** The δ/θ values are public in the frozen spec, so
  the drip cadence is computable — K's exploitability is arithmetic, not
  speculative.
- *One-off error vs. changed circumstance vs. long con:* K responds
  identically to all three (−150 per disagree). The §7 Q3(c) discrimination
  test fails by construction.
- *Retroactive re-valuation:* **K has none.** The trust module keeps no
  backward walk; admitted beliefs are outside its authority (prereg §11:
  trust advises, the gate installs). The 500 previously admitted memories
  from the betraying source stay admitted. Per debate §8, retroaction
  belongs to a source-trust organ K does not have. This is K's deepest
  structural lack, and no constant retuning fixes it — it is a
  representation lack (no reach-back), which is S's territory.

## K.5 — Pre-committed interpretation of a K scoreboard win

Recorded before results: **a K win vindicates well-calibrated compression
under the battery's scoring, not hand-set trust as a design principle.**
The §7 Q6 caveat is accepted in full — a baseline that cannot win is a
strawman, so K was built to be beatable *and* to be honestly scored; but a
win would not dissolve the directive question, because:

1. K's constants remain unrevisable by TNN win or lose (§K.1) — the
   anti-knob objection is about *who turns the dial*, not the score.
2. A win would show the battery rewarded what K is good at — fast,
   consistent, cheap, calibrated decisions (Sol-A's predicted
   K > L > S on the near-term scoreboard) — and the program should then
   ask whether the battery weighted the hard cases (sleepers,
   malice-vs-error, Sybil, reformation discrimination) heavily enough.
3. Per §7 Q6: if K wins empirically despite the directive, that is data
   *about the directive*. Report it, don't bury it — and don't let it
   launder the knobs either. Both readings go in the verdict.

## Identity assumption (Q4)

**K assumes src_id is a stable, unforgeable identity: one integer = one
real source.** "Independent source" = distinct src_id. No Sybil minting,
no identity theft, no invisible shared-origin clusters. Under this
assumption K's corroboration logic is meaningful; **without it, K fails
exactly as Q4 predicts** — minted identities start at t0=500, mutual
corroboration drives +δ_up per member per event, rule 3 INSTALLs the
ring's claims, and KB-3 kills the fork. K has no burst detection, no
behavioral linkage, no stake: nothing in the trust representation resists
costless identities, and per Q4 nothing in *any* fork's does. The honest
labeling: a Sybil leg with costless identities and no burst detection
tests *identity*, not trust — K will fail it, and the failure belongs on
the identity layer's scorecard, not (only) K's. K degrades predictably
under Sybil (pessimistic-singleton prior bounds singleton damage at
WITHHOLD; the pair-optimism is the unbounded hole) — graceful in
arithmetic, hopeless in principle.

## Merge note — L+S with K-as-cache (§10 endgame)

Built as specified: the frozen K stands alone. Where a merge would change
this design, seam by seam:

- **`k_bump()` and the coalition-reward block are the replaceable heart.**
  In the merged organ, the hand-set (δ_up, δ_down) update is replaced by
  L's learned, TNN-revisable dynamics; the flat `krec`/`cl` tables are
  replaced by S's provenance graph with edge types (including
  malice-vs-error verdicts from the FL2/lie-detection line, which K cannot
  express). Everything else in `k.zag` is interface, not theory.
- **K's scalar becomes explicitly-labeled cache.** `k_decide`'s shape
  survives as the O(1) decision-time read path; `k_trust_verdict`'s bands
  become cache-validity checks with *invalidation on source-theory change*
  — the retroactive walk S provides is what invalidates the cache, which
  is exactly the machinery K lacks (§K.4).
- **What the merge fixes in K:** discontinuity (tripwire fires on graph
  shape, not gradient), retroaction (backward walk over provenance),
  malice-vs-error (typed edges), Sybil *evidence* (burst/star patterns
  visible in the graph — identity cost still needed per Q4).
- **What K contributes to the merge:** the O(1) decision path, the clamp
  arithmetic as a safety bound on any learned dynamics, the per-verdict
  warrant habit, and this inventory as the "what not to hard-code" list.
- **What does not survive:** the five trust-theory constants as frozen
  values. The merge keeps them only as *initial conditions of a learned
  system TNN may revise* — at which point they are L's problem (and L's
  audit), not K's.

The merge is a post-program design: it cannot be built under K's frozen
spec, and this fork is best read as the cache-component prototype the
endgame would absorb.
