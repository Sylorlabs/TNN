# LI Modes Debate Cross-Check — Independent Steelman FOR (b)

**Date:** 2026-09-23. **Role:** independent cross-checker of the 13 recorded
takes in `DEBATES_LI_MODES.md` (the debate coordinator authored the six
native-Muse takes directly; this take is an independent review). **Frozen
prereg untouched:** this file is a record, not an amendment.

**Position taken:** steelman (b) — one unified human-like mode, no separate
training/production modes — and attack (a) separate modes. Specifically I
defend the position that "figuring out what to learn" is implementable as a
deterministic, auditable scheduler over the refusal ledger, not a reward
signal; and that a mode bit is strictly worse architecture than a unified
learner with a work queue.

---

## 1. The strongest objection, head-on: "curiosity/novelty is a reward signal in a trench coat"

Sol-B2 and Muse-B2 are right that the objection is real and that any honest
(b) must answer it. Here is the answer: the objection kills *novelty
maximization*. It does not kill *corroboration-seeking*. The two are
opposites, and confusing them is the error on which the objection rests.

**A reward signal has a precise shape.** It is a scalar objective whose
maximization steers behavior through feedback: the policy adapts so that
outcomes scoring higher on the metric become more likely, and the pressure
continues whether or not the metric tracks the true goal (Goodhart). Novelty,
surprise, and expected-information-gain criteria all have this shape: they
score candidates, rank them, and push behavior toward the score's maximizer.
Worse, the maximizers of "surprising to this ledger" are systematically the
confident falsehoods — flat-Earth prose is more surprising than a beginner
guide — so the signal's maximizer points AWAY from truth. That is a genuine
standing-law violation, and I concede it unconditionally: **any criterion
that ranks by novelty/surprise/information-gain is dead on arrival.**

**What (b) needs is not a ranking heuristic but a scheduler.** Concrete
formulation — *refusal-ledger-driven directed corroboration-seeking*:

1. **The refusal ledger is an auditable inventory of ignorance.** Every
   withheld singleton (e.g. the 55 NO_CORROBORATION clusters) is a row:
   claim, normalized sentence, asserting host(s), denial status (never
   refuted / refuted / unknown).
2. **The scout policy is a pure deterministic function of ledger state:**
   `next_target = head(queue)`, where the queue is the withheld-singleton
   set sorted by a FROZEN preregistered priority: (i) claims previously
   REFUTED or denied are excluded entirely; (ii) larger withheld clusters
   first; (iii) topic-coverage gaps (topics with zero installs) after;
   (iv) stable tiebreak (e.g. first-seen order). No learned weights, no
   scoring model, no adaptive update. Frozen in the prereg, byte-identically
   replayable, fully auditable: every fetch is traceable to one ledger row
   plus the published ordering.
3. **The INSTALL predicate never moves.** The scheduler cannot install, cannot
   loosen, cannot whitelist, and does not feed anything but fetch requests.
   Scouting outputs candidates; acceptance is untouched G4/G6. Every attack
   that fails against frozen G4 today fails identically.
4. **The criterion is anti-sensational by construction.** Corroboration-
   seeking pursues claims that already have at least one witness and asks
   for a second. Novelty-seeking pursues the unwitnessed. A confident
   falsehood that no honest source repeats can never rise in a
   corroboration queue — there is no first witness, so it never enters it.
   The queue cannot be gamed toward sensationalism because it has no
   sensationalism dimension: it has cluster size (evidentiary weight) and
   coverage gaps (completeness), both fixed.
5. **No feedback loop toward any objective.** Nothing in the scheduler adapts
   on outcomes. Installs change the ledger (state evolves — that is learning),
   but no policy parameter is adjusted by any outcome measure. There is no
   metric being maximized. A to-do list with a frozen ordering is not a
   reward signal, however much it resembles curiosity from the outside.

**Why this preserves deliberate agency rather than violating it.** The
program's main line (MA1, RC1) is deliberate agency: TNN has explicit,
auditable, owned reasons for its actions. The work queue IS deliberation
implemented at scale: "I do not know X; X was asserted by one witness; I
choose to seek a second witness before deciding." That is deliberate (an
explicitly recorded information need, acted on by fixed rules) rather than
reward-driven (implicit pressure toward a score). Deliberate agency is about
*whose reasons* govern the action — the system's own explicit, inspectable
rules — versus reasons smuggled in by a metric. The queue's reasons are
written in the ledger; a reward signal's reasons live in the maximizer's
implicit bias. Human analogy, stated honestly thinly: this is not "being
curious" in the rich sense; it is what a researcher does with a lead, and it
is the most the no-reward law permits. The word "curiosity" is doing
aspirational work in the debate; drop it. Keep "directed corroboration-
seeking," which is executable.

**Self-kill condition (honest):** if any version of the queue is amended to
rank by novelty, surprise, engagement, or any learned/learned-adjacent score —
i.e. if "what to investigate" ever becomes an outcome-scored maximizer — the
objection is sustained and (b) in that form dies. The queue survives only as
long as it stays a frozen scheduler. That is a bright line a red team can
enforce: any adaptive scoring in the scout policy = INTEGRITY-FAIL.

**Answer to "this is a scouting strategy, not a position" (Muse-B2's
salvage):** conceded and embraced. The strongest form of (b) is not a
philosophy of unified modes — it is the claim that you need neither modes
nor loosenings: a strict instrument plus a deterministic pursuit strategy.
That the salvage is position-independent is not a weakness; it means (b)'s
thesis ("no modes needed") is falsifiable by one cheap experiment (H1),
whereas (a)'s thesis requires building the whole two-mode machine to even
test.

---

## 2. Attack on (a): the mode bit is worse than a unified learner with a work queue

The (a)-FOR case has one genuine point: an explicit mode flag is legible.
Legibility is real but it is buying the wrong thing. Here is why a global
mode bit on which epistemic standards depend is bad architecture, answered
against the "quarantine + merge gate" defense point by point.

**(i) The merge gate has no stable third setting — and both sides already
conceded it.** The debate record shows the (a) camp itself split on this:
Muse-A1 concedes adjudicated merge IS a loosening. The dilemma is binary:
strict merge (byte-identical G4) means production graduation is ~0/213 — the
entire training-mode machinery becomes a candidate generator for a bar that
never fires, i.e. expensive heat with extra storage and replay costs
(H3-K1/K2 are preregistered to measure exactly this); adjudicated merge
(trainer/diagnoser decides) means the production bar has been loosened
toward human judgment in the loop — which is deliberate teaching, which
already exists and needs no mode bit. The mode bit is load-bearing nowhere:
in the strict setting it changes nothing production-side; in the loose
setting the work is being done by the human, not the bit. A bit that
contributes nothing to the winning setting is not "honest architecture," it
is a switch nobody pulls.

**(ii) Quarantine does not answer the read-side contamination objection, and
(a)-FOR knows it.** The defense says quarantine absorbs the looseness. But
quarantine partitions ledger *rows*; it does not partition the learner's
derived state. The AGAINST case (Sol-A2, Muse-A2) is that training-mode claims
are read during training and shape priorities, summaries, hypotheses,
retrieval paths — downstream state a merge gate cannot revoke, because
revocation applies to rows, not to the mind's evolved dispositions. H3-K3's
read-instrumentation can enforce "no quarantine reads by the reasoner," but
then the training mode's entire value proposition — hypothesis formation,
discovery, training signal from the quarantined material — evaporates: either
provisional claims do work (contamination returns) or they don't (the fork is
a more expensive withhold — Muse-C2's dilemma, one level down). Quarantine is
not a solution to contamination; it is a relabeling of it.

**(iii) The autonomy contradiction is fatal, not cosmetic.** The (a) design
needs *somebody* to set the flag. If the trainer/scheduler sets it: TNN's
stated autonomy default is "TNN does all; humans are backup/override" — a
training mode that is only safe while a human babysits the flag fails the
program's own autonomy bar, and the strict mode's safety has been downgraded
from an intrinsic property of the instrument to scheduler discipline across
the whole glue stack (one compromised wrapper, one stale config, and the
loose rulebook is production). If TNN sets the flag itself: it is a
self-modifying epistemic standard — the system deciding when its own memory
law may be suspended — which is exactly the class of self-change the RC line
exists to govern with extreme care. The work queue needs no such thing: the
scheduler changes WHAT is investigated (information needs, from the system's
own refusal ledger) and never WHETHER it is believed. Deliberate agency is
preserved because the acceptance standard is not a setting at all — it is
simply what the system does, always.

**(iv) Everything becomes mode-relative, including the audit trail.** Under
one strict instrument, a verdict means one thing. Under two modes, every
artifact — installs, reads, derived state, red-team results, replay behavior,
deletion records — carries a mode label, and every historical question
("was the flag correct at time T?") needs the whole flag-selection audit.
Judge-Step's H-J1 proposal adds a quarantined training partition with a
merge gate — more states, more provenance, more explanations per result. The
A9 boundary is already hard to interpret under one rulebook; two modes double
the explanatory surface an adversary can hide behind. Simplicity is a
security property; the mode bit spends it for no measured gain.

Net: (a)'s legibility argument is real but secondary. A legible bad
architecture is not better than a strict simple one. (b) keeps one ledger, one
predicate, one agency — and its throughput proposal (H1) touches none of the
integrity surface at all.

---

## 3. Stress-testing H1: is the throughput claim testable, or an empirical bet?

Honest answer: **it is an empirical bet, and the prereg is honest about
being one.** H1-K1 (≥1 install on C1+C2 under strict G4) is a binary wager on
"directed pursuit finds byte-identical cross-host sentences at usable
density." That is fine — it is the only fork whose experiment risks nothing
(instrument untouched; H1-K4 proves it) — but the bet should be *measured*,
not just settled. I propose decomposing the funnel so a failure diagnoses
itself:

1. **Instrument stage-wise yields** on the V-SCOUT run: withheld singleton
   clusters → queued scout targets → pages fetched → pages containing a
   byte-identical normalized sentence of a queued claim → installs. The
   load-bearing stage is second-source hit rate: P(a targeted fetch finds a
   byte-identical sentence on a distinct host | claim was a withheld
   singleton). Report it per cluster; a 0% hit rate kills the *corpus*
   strategy while a partial rate localizes where syndication exists.
2. **Run the "syndication census" first, cheaply:** take the 55
   NO_CORROBORATION clusters' normalized sentences and run quoted
   exact-match searches against the live web (document the search method:
   quoted queries, which engines, date). The census measures the bet directly
   — fraction of withheld claims with ≥2 distinct hosts carrying a
   byte-identical sentence — before the fork runs. If the census reads ~0%,
   H1 is expected-dead and the fork's kill is a formality; if it reads
   nontrivial, H1-K1 has a real shot. The census is diagnostic, H1-K1 is the
   verdict; do both.
3. **Separate C1 from C2 in the analysis.** C1's re-scout is the honest test
   (historical withholds, fresh directed pursuit). C2 is only meaningful for
   H1 if the fixture crew builds it from real syndicated/mirrored text
   (press releases, mirrored documentation, carried wire copy) — see caveat
   §5 below. If C2's facts are fixture-authored sentences, no live host will
   carry them byte-identically and a zero there measures the fixture, not
   the scouting. Report H1-K1 on C1 and C2 separately; failure on C2-alone is
   a fixture artifact unless the fixture's novelty claims document
   findable-on-≥2-hosts phrasings.

**What cleanly kills H1's claim:** census hit rate ≈ 0% AND V-SCOUT installs
= 0 on C1 — i.e., directed pursuit finds no byte-identical corroboration even
when it is the only thing being looked for. Then the math objection
(Muse-B2's "curiosity doesn't create identical sentences") is sustained
empirically, D1 is dead, and (b)'s throughput story is over. Note what this
does NOT imply: it implies the instrument cannot learn from THIS live-web
corpus under G4 — the honest next move is representational (D4,
triple-level corroboration, its own prereg), not a loosening. Zero installs
is information; a loosened bar is hope.

---

## 4. Honest verdict

**I would bet on H1 (V-SCOUT) as the immediate experiment and on H2
(V-PARA, with the quantitative/qualitative ablation) as the second bet.**

- H1 is the cheapest possible test of the unified position: no instrument
  change, no integrity downside, one empirical bet. If it passes, directed
  scouting ships as the default policy and (b) has won its throughput story
  without touching the rulebook.
- If H1 fails cleanly (census ~0% + zero installs), the paraphrase gap is the
  confirmed binding constraint and H2 is the honest next shot: the D2
  conjunction is the only proposal with adversarial structure (numeric-
  exactness fails only against truth-telling-numbers liars; the lie must then
  live in qualitative prose — a measurably weaker attack class) rather than a
  naked threshold. H2's ablation (quantitative vs qualitative installs) is
  the make-or-break: if ALL installs are numeric-bearing, Muse-C2's "sieve
  with a reinforced rim" is sustained and the fork's scope is formally
  restricted instead of silently generalized.

**What kills my position** (in order of finality):

1. H1 fails cleanly per §3 (census ≈ 0% + 0 installs on C1). Then pursuit was
   never the bottleneck; (b)'s salvage is dead and I concede it. The honest
   fallback is D4 (representational shift), not loosening.
2. Any amendment to the scout queue that ranks by novelty/surprise/IG/learned
   scores — my own §1 self-kill. If "curiosity" creeps from frozen scheduler
   to maximizer, the trench-coat objection is sustained and I abandon (b) in
   that form.
3. H2's red-team parity (H2-K3/K4) fails: the conjunction admits a
   paraphrase-sockpuppet that frozen G4 withholds. Then no loosening —
   structured or not — is admissible on the production rulebook, and the
   program faces the structural question (better evidence sources: trusted
   datasets, cryptographic provenance, human adjudication) rather than any
   mode or fork question.

**On the independent judge's pick:** Judge-Step chose (a) with a merge gate
of "byte-identical match against the frozen trusted guide set." That
mechanism contains a contradiction worth flagging (see §5): the fixture's
novel facts are by definition not in G1–G6, so the merge gate admits exactly
zero of them — H-J1's own kill bar (≥1 install on the novel-facts fixture)
cannot fire. The judge's (a) either installs nothing new (tautological) or
its merge gate must be loosened, at which point the (a)-AGAINST dilemma
applies. I read the judge's take as actually supporting the (b) diagnosis:
the only safe merge is one that changes nothing, which is just strict G4
with better scouting.

---

## 5. Caveats to the coordinator (holes, not prereg amendments)

1. **C2 fixture phrasing hole (H1 at risk):** if the fixture crew authors
   novel-fact sentences themselves, H1 on C2 is untestable — no live host
   will carry a fixture-authored sentence byte-identically, and a zero there
   cannot distinguish "scouting failed" from "fixture unfindable." The
   fixture crew must either build C2's novel facts from real multi-host
   syndicated/mirrored text (documenting per-fact findability) or H1's
   kill-bar report must be read on C1-only. Flag to coordinator: clarify
   before fork crews run.
2. **Judge-Step's merge-gate contradiction:** per §4 — a merge gate that
   only passes guide-matching claims cannot install anything novel, so
   H-J1(i) as written is unsatisfiable under the judge's own mechanism.
   Needs repair (loosen the gate → inherits the (a) merge dilemma; keep it
   → H-J1 is a null test) or withdrawal.
3. **H1-K1's "≥1" bar is weak by design** — a single install on 400+ URLs is
   still a starving pipeline. If H1 passes at exactly 1, the debate is not
   settled: report the stage-wise funnel (§3) so the program knows whether
   it found a trickle or a tap.
4. **The "human-like" label should be retired from (b)'s name** once H1
   runs. What is actually being tested is a deterministic scout scheduler;
   the human analogy is motivational, not load-bearing. Naming it "human-like
   mode" invites the (b)-AGAINST critique that humans fall for cults — a
   critique that misses a scheduler that excludes refuted claims and cannot
   install anything unwitnessed twice.
