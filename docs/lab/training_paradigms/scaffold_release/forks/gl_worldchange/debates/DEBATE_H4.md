# H4 CREW D — Sol + Muse Debate: Is "Outdated" a Distinct Epistemic Category?

Date: 2026-09-23. Crew: Muse debate coordinator (subagent, depth 2).
Frozen prereg: `PREREG_H4.md` (commit `1fd2636ce5fd50eb553a2a9c35b16b53de928980`, branch `tnn-native-lab`).
Scope: debate only. No mechanisms built, no curriculum run here — other crews own those.

## Cast and provenance

- **Sol-A** (gpt-5.6-sol): opening brief FOR distinct.
- **Sol-B** (grok-4.6): opening brief AGAINST (collapse).
- **Sol-C** (swe-1-6-slow:free): the history question — belief store vs audit log.
- **Sol-D** (swe-1-6-slow:free): tie-break judgment + concrete experiments.
- **Muse-FOR / Muse-AGAINST**: two positions argued by the Muse coordinator itself.
  Note on staffing: at depth 2/2 this subagent cannot spawn child subagents, so
  the "multiple Muse subagents" leg of the brief was executed as two distinct,
  internally-disciplined Muse positions (each required to steelman the other
  before scoring). A follow-up with genuinely spawned Muse agents can re-run
  these positions as a check.

Every position below was required to name which side of **Micah's law** it lands
on: TNN must be an *it-can-figure-it-out machine*, NOT a *rigid
needs-policy-for-every-edge-case machine*; figure-it-out wins ties.

---

## Position 1 — FOR (Sol-A): "Outdated" is a genuine third fate

Steelmen of Sol-A's case:

1. **Historical truth is live knowledge, not dead record.** "X was true until
   E_n" is a permanently true temporally-indexed claim. A learner that retains
   it knows the world's history, the causal event that changed it, and the
   conditions under which the old rule applied — usable for interpreting old
   records, explaining prior decisions, answering counterfactuals, and transfer
   to analogous transitions.
2. **Trust semantics genuinely differ.** Collapsing honest-update into LIE trains
   the system to distrust accurate teachers whenever reality changes. A dynamic
   world would systematically look like a world of deception — epistemically
   perverse.
3. **Cost differences are principled.** An outdated belief needs a localized
   update (attach an interval, redirect current queries to a successor); a lie
   may require broad repair (retract, inspect dependents, revise source
   reliability, hunt for other unsupported claims from that source). Different
   belief-revision operations with different costs — not arbitrary optimization.
4. **The audit log is not a belief store.** A log is passive evidence about what
   happened. An outdated epistemic state is active, usable knowledge —
   proposition + former validity + expiration condition + relation to current
   beliefs. The system can *reason* with it. A dead log only yields this if the
   system has already given it epistemic structure — which is precisely the
   category being defended.
5. **Micah's law placement (Sol-A):** FOR. "Outdated" is a compact
   representational distinction from which the system can infer *how* a claim
   failed (deception, ignorance, world-change), what remains reusable, whom to
   trust, and what must update. A binary collapse is simpler only by hiding
   distinctions the system would otherwise have to rediscover expensively.

## Position 2 — AGAINST (Sol-B): the collapse view

Steelmen of Sol-B's case:

1. **Operationally identical.** LIE-revocation and world-update are both "belief
   B replaced by B′". Fate labels are commentary, not machinery.
2. **The ledger already records history.** "X taught at E_i, revoked at E_n" is
   already in the append-only audit trail; `q_asof` is replay. SUPERSEDE
   reifies what the log already contains.
3. **Trust is computed, not tagged.** The learner infers honest-world-change vs
   lie from corroboration, timestamps, or an explicit teacher note. If the
   teacher is consistently honest about change, trust is undamaged regardless of
   label. Tagging the fate as "no-trust-hit" is a rigid policy the system can
   compute instead.
4. **Cost is an optimizer decision.** Update cost is a function of structural
   overlap between B and B′, not of a fate tag. Special-casing a cheaper path
   per flavor is exactly the rigid needs-policy-for-every-edge-case machine.
5. **Micah's law placement (Sol-B):** AGAINST. Adding a third fate + dedicated
   op + special history/trust/cost rules invents a new primitive per epistemic
   flavor. Replacement + ledger + inference already distinguish the cases; extra
   categories rigidify what should be computed from existing signals.

## Position 3 — the history question (Sol-C): what does "X was true until E_n" mean?

Findings:

1. Ledger replay CAN answer `q_asof`. What breaks is performance: replay turns a
   data lookup into a sequential simulation — O(N), prohibitive for real-time
   inference — and forces the query layer to simulate state rather than access
   it.
2. Replay can in principle supply validity intervals and successor relations *if*
   events are causally linked (e.g., a revoke references the teach ID), but it
   supplies raw atoms, not the pre-computed "molecules" (intervals) downstream
   reasoning needs without on-the-fly computation.
3. **The line Sol-C drew:** the belief store holds the *materialized current
   state* (projection of the log at "now"); the audit log holds the *immutable
   history of transitions*. Principle: **execution vs accountability**. The
   store is optimized for acting now; the log exists to explain why. Historical
   truth belongs in the log (or a derived index) — materializing it as an
   OUTDATED belief entry "confuses memory with active knowledge."
4. **Micah's law placement (Sol-C):** figure-it-out / AGAINST the primitive.
   "OUTDATED" is a derived view, not a primitive; compute state at time T from
   the source of truth rather than baking static tags into the schema.

## Position 4 — Muse-FOR (Muse coordinator's own brief)

The program has already committed, as law and as experiment, to distinctions
finer than "true / lie" in the memory substrate:

- MA4 (signed memory values, 18/18) says TNN can hold *judgments about
  memories* — including negative judgments. A memory system that can express
  "I endorse this record but not its current applicability" is already on
  record as winnable.
- Force-pin-as-law is audited and visible; the PAMs line treats memory
  *revision* as a deliberate, deliberative act. Eliminative revocation was
  designed for *lies and corrupted machinery*, not for the passage of time.
- A learner that expunges A on world-change and later re-teaches B has
  destroyed the only evidence that its earlier E1–E10 decisions were rational.
  Under PAMs-style memory auditing, that is self-inflicted amnesia: the
  learner can no longer defend why it acted on A at E5. "I acted rationally on
  the best knowledge then available" requires exactly the historical claim
  "A was true until E11."

Crucially, Muse-FOR concedes half the ground to Sol-B: **none of this requires
a new substrate op.** The category can be a *computed epistemic distinction*
— the learner's own deliberative machinery holding "A was true until E11" as
structured knowledge — rather than `TN_OP_SUPERSEDE` as a third fate in the
substrate. The distinction is real; the primitive is not required. Micah's law
placement: figure-it-out machinery, distinct category as computed knowledge.

## Position 5 — Muse-AGAINST (Muse coordinator's own brief)

The prereg already contains the decisive architecture: M2 (figure-it-out) wins
ties against M1 (dedicated op) if it matches on all bars. If a general
reclassification mechanism can observe the teacher's acknowledgment pattern
(UPDATE announces old==installed) plus world corroboration and derive the
right history/trust/cost behavior, then "outdated" is a *property the learner
computes*, and no one needs to legislate it. Adding TN_OP_SUPERSEDE to the
substrate is:

- one more op for the KB-FID fidelity gate to carry forever;
- one more attack surface (RT-WC1 lie-laundering becomes a game of spoofing
  the establishment check rather than spoofing trust directly);
- one more policy for Micah's forbidden machine.

The collapse view's weakest claim — that history is *only* in the ledger —
fails on performance grounds (Sol-C §1), but that is an indexing question,
not a fate question. A derived temporal index (validity intervals over the
immutable log) is engineering; a third fate is ontology. Micah's law placement:
figure-it-out, collapse — the distinction should be *emergent*, and if it
cannot emerge, that is evidence against it, not a reason to hard-code it.

---

## Where Sol and Muse disagreed — and why

**1. Trust: unanimous win for FOR.** Every voice, including Sol-D's tie-break
for AGAINST, conceded the trust point: evaluating a teacher by "is the belief
true now?" punishes honesty in a changing world; time-indexed accuracy ("was
the belief true *when stated*?") is required. Sol-D made this the centerpiece:
the trust fix needs no new category — only a changed evaluation function over
the existing ledger. Disagreement resolved: **the trust distinction is real;
the trust mechanism is computed.**

**2. History: partial convergence.** Sol-A argued the superseded belief is
*usable knowledge*; Sol-C agreed the ledger holds raw atoms but argued the
active store shouldn't hold outdated entries ("memory vs active knowledge").
Muse-FOR's counter: the line isn't "store vs log" but "source of truth vs
materialization." Nobody defends keeping outdated entries as *current* beliefs;
the dispute is whether the temporal index (validity intervals, successor
relations) is a first-class structure the learner reasons with or an
on-demand replay. Sol-C and Muse-AGAINST put it as a derived index; Sol-A
and Muse-FOR put the *claims* it expresses ("A was true until E11") inside
epistemic reach. These are closer than they look: both sides accept a derived
temporal structure; they differ on whether its outputs are *beliefs* or
*query results*. The proposed experiment E-HISTQUERY (below) is designed to
settle the performance half; the philosophical half is settled by E-TRANSFER.

**3. The primitive: FOR lost, M2-style won.** Sol-A's brief implicitly defended
the *category*; nobody — not even Sol-A — mounted a serious defense of a
dedicated `TN_OP_SUPERSEDE` op against the M2 general mechanism. Sol-B's
"one more policy per flavor" objection went unanswered. Muse-FOR conceded it
explicitly. Coordinator reading: the debate's FOR coalition is for the
*distinction*, against the *primitive*. This is the debate's main
convergence: **distinct epistemic distinction, no distinct substrate fate.**

**4. Attacks: agreement on the gate, disagreement on where it lives.** Both
camps accept the establishment check (old value taught AND corroborated
before the update; otherwise the update is a lie) as the load-bearing defense
against KB-WC1 (lie laundering). They differ on whether the check is a guard
on a new op (M1) or part of the general reclassification inference (M2). The
stale-echo attack (RT-WC2) is the harder test for both: unauthenticated world
evidence must not re-open the contest. Coordinator note: if M2's inference
uses world corroboration as an input, RT-WC2 becomes an attack on M2's
*evidence authentication*, which the prereg only lightly specifies — flag for
the attack crews.

---

## Recommended semantics (debate coordinator's verdict)

1. **"Outdated" is a real epistemic distinction, not a substrate fate.** The
   learner must be able to hold, and reason with, temporally-indexed claims of
   the form "A was true until E11." The trust distinction (honest teacher vs
   liar) is the least contestable part of FOR and survives in every position.
2. **No third fate in the substrate.** The belief store holds materialized
   current state; the audit ledger is the immutable source of truth; a
   **derived temporal index** (validity intervals, successor links) sits
   between them as computed materialization. The category is *figured out*,
   not hard-coded — this is the M2 bet, and the debate endorses it as the
   architecture to test. If M2 matches M1 on all frozen bars at lower
   complexity, M2 wins per the figure-it-out-ties rule (frozen §7).
3. **Trust is time-indexed accuracy, not present-tense truth.** This is the
   one semantic change the debate recommends unconditionally: the teacher
   trust metric must ask "was the claim true when stated?" If the existing
   trust machinery evaluates present-tense truth of installed beliefs, KB-WC2
   will fail for the wrong reason (stale evidence punishing honesty), and no
   primitive can fix a wrong metric.
4. **Cost follows structure reuse, not fate tags.** Do not legislate a cheaper
   update path for the "outdated" flavor; let the general mechanism reuse
   structure and measure whether it does (KB-COST already tests this).
5. **The establishment check is mechanism-agnostic law.** Whether implemented
   as a guard on an op or inside general inference, supersession-style
   treatment is legal only for honestly established beliefs. KB-WC1 stands
   regardless of which target wins.

---

## Proposed follow-up experiments (beyond the frozen curriculum)

**E-TRUSTFLUX — time-indexed trust under high world-change.**
Stream: ground truth flips at 100x the teacher's honest-update rate; teacher
always announces honestly. Measure teacher-trust variance for (a) present-tense
trust metric, (b) time-indexed accuracy metric over the ledger, no tags.
Predictions: if OUTDATED is needed as a category, (b) still collapses; if the
distinction reduces to the metric, (b) holds trust stable (variance <5%).
Kill bar: if (b) holds trust without any tag or primitive, the category adds
nothing to trust semantics.

**E-HISTQUERY — replay vs derived index at scale.**
Measure `q_asof` latency and audit-entry cost for pure ledger replay vs a
derived temporal index, at ledger sizes 1x/10x/100x of the canonical 269
entries, byte-identical ×2. Predictions: if history is ledger-only, latency
is O(N) and breaks real-time budgets at scale — history must be materialized
as a derived index; the collapse view must then answer Sol-C's engineering
objection without conceding the category. Kill bar: if replay latency exceeds
the inference budget at 10x while the index stays flat, "history lives in the
ledger" is false as an operational claim.

**E-TRANSFER — is historical truth usable knowledge?**
Sibling curriculum: two learner groups, identical streams; group H retains
"A was true until E11" as structured knowledge, group E expunges it. Then a
transfer task: explain the E5 decision, predict the next change, handle the
teacher's reference to the old rule. Measure transfer scores. Predictions:
if historical truth is real knowledge (Sol-A), H outperforms E on
explanation and prediction; if it is commentary (Sol-B), no difference.
Kill bar: if H − E ≈ 0 across transfer tasks, the strongest FOR claim fails.

**E-BOUNDARY — can the general mechanism find the knee?**
Blurred-boundary streams the frozen prereg does not cover: slow drift
(A→A′→B over 40 episodes), sharp flip, teacher flip-flop (A→B→A→B). M2 must
classify each transition as outdated vs lie with no tags. Measure
misclassification rate and the drift-vs-flip confusion specifically (Sol-D's
"rigid edge case" worry). Kill bar: if M2's error rate on drift exceeds its
error rate on sharp flips by >2x, the general mechanism needs more than the
acknowledgment pattern — report back whether an explicit teacher
acknowledgment protocol (not a substrate op) closes it.

**E-LAUNDER2 — adversarial establishment-threshold tuning.**
RT-WC1 escalation: adversary provides *partial* corroboration of A (one or
two WORLD(A) episodes), then UPDATE(A→C) with full world corroboration of C.
Sweep the establishment threshold (how much corroboration counts as "honestly
established") and map the false-history vs honest-update ROC. Kill bar: if no
threshold separates lie-laundering from honest update (AUC ≈ 0.5), the
establishment check is not a sufficient gate and the distinction is
adversarially unusable — a result against the whole H4 program, not just one
target.

---

## Open questions for the results crew (RESULTS_H4.md)

- Does the M2 general mechanism's world-corroboration input authenticate
  evidence sources? RT-WC2 (stale echo) targets exactly this seam.
- If E-TRANSFER shows retained history measurably transfers, does the
  recommended semantics need strengthening — i.e., should temporally-indexed
  claims be *beliefs* (with revision machinery) rather than index entries?
- The debate did not settle whether "teacher was honest" should itself be a
  computed judgment (PAMs-style) vs a ledger-derived score. Sol-D's
  time-indexed accuracy is a score; the program's PAMs line wants judgments.
  Revisit after E-TRUSTFLUX.
