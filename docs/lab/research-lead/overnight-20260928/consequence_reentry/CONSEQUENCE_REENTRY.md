# Consequence Re-entry: A General Architectural Principle

**Status:** ANALYSIS ONLY. DRAFT-NOT-FROZEN. No implementation designed or proposed.
**Date:** 2026-10-01
**Parent:** Three-stops synthesis (`48cb843e5`)
**Verdict:** CONSEQUENCE-REENTRY-COMPLETE

---

## 0. Thesis

The three-stops synthesis (`48cb843e5`, section 0) states the single
underlying incapacity as: "TNN-2 has no machinery by which the consequences
of its own activity re-enter its future decisions." This document asks
whether that formulation is the right level of abstraction: what exactly it
claims, what other cognitive functions it covers beyond stopping, where its
boundary lies, and what would falsify it.

The central finding: consequence re-entry is a falsifiable principle about
**adaptation**, not capability. It explains why TNN-2 does not improve with
experience. It does not explain why TNN-2 cannot do things it has no
machinery for. This boundary is what makes the principle testable rather
than vacuous.

---

## 1. Definitions

### 1.1 What is a "consequence"?

A consequence is an outcome of the system's own activity that carries
information about whether that activity was successful, costly, or
worth repeating. In TNN-2's vocabulary:

- **Success/failure:** trial candidate verified or rejected (F1),
  revision succeeded or returned 0 (F3), bootstrap agreed or disagreed (F4).
- **Cost:** nodes/edges allocated per operation, trial candidates tried
  per query (F2 counts in hdr+16).
- **Side effects:** contradiction detected (type-3 edge added), eviction
  performed (rec_evict written), uncertainty recorded (T30 node created).

What is NOT a consequence in this sense: the input data itself (taught
facts, observations), the static structure of the world, or the researcher's
harness configuration. A consequence is produced by the system's activity,
not given to it.

### 1.2 What is "re-entry"?

Re-entry means a consequence is:

1. **Retained** in queryable form (not just written, but stored such that
   a future decision can find it by the relevant key).
2. **Consulted** by a production decision (a read path exists AND is
   exercised in the normal operation of the system, not just in test code).
3. **Effective** at a decision point (the consulted consequence can change
   what the system does: a different branch taken, a different value
   returned, a different structure built).

All three are necessary. The theater audit (`e0423538a`) and the failure
retention analysis (`d3e896c8c`, section 4.3) establish this as the
read-path-first rule: a record no production decision consults is theater,
regardless of how carefully it is written.

### 1.3 The minimal machinery

For consequences to re-enter, four elements must exist:

- **M1. Consequence generation.** The system must produce the outcome.
  (TNN-2 HAS this: F1-F7 fire constantly.)
- **M2. Retention.** The outcome must be stored in queryable form, keyed
  by the relevant unit (pursuit, query shape, structure, strategy).
  (TNN-2 LACKS this: D1-D5 discard or de-key everything.)
- **M3. Read path.** A production decision must consult the retained
  consequence in its normal operation. (TNN-2 LACKS this: T3/T4/T5 are
  write-only.)
- **M4. Decision point.** There must be somewhere in the architecture
  where the consulted consequence can change behavior. (TNN-2 LACKS this
  for stopping: no decline gate, no abandonment gate, no retention-aware
  eviction.)

The three-stops synthesis shows that TNN-2 has M1 everywhere and M2/M3/M4
nowhere (for the stopping decisions). The pattern generalizes: wherever
TNN-2 fails to adapt, the missing elements are M2, M3, M4, never M1.

### 1.4 The forward/backward distinction

This principle draws a sharp line between two kinds of architectural work:

- **Forward machinery:** what the system CAN do. Trial assembly, graph
  execution, fact retrieval, revision operators, eviction sweeps. These
  transform inputs to outputs. They work or they do not, independent of
  experience.
- **Backward machinery (consequence re-entry):** how the system LEARNS
  from what it did. Retention of outcomes, consultation at decision
  points, behavior change driven by history. These transform experience
  into improved future performance.

Consequence re-entry is a claim about backward machinery. It predicts that
TNN-2's adaptation failures (not improving with experience) are caused by
missing M2/M3/M4, not by deficient M1. It makes no claim about forward
machinery gaps.

---

## 2. Function survey: what else requires consequence re-entry?

Beyond the three stops (decline, abandonment, forgetting), surveyed by
whether TNN-2 has M1-M4 for each function.

### 2.1 Learning from mistakes (failure → future attempts)

**Requires:** When attempt N fails, attempt N+1 for the same pursuit
should differ (different candidate, different strategy, or no attempt).

**TNN-2 status:** M1 yes (failures occur), M2 no (no per-pursuit failure
record), M3 no, M4 no. The fixed trial order re-attempts identical
candidates on every identical miss. The re-fired revision (D1) is the
canonical instance.

**Missing:** Per-pursuit failure memory (G1) with a read path before
re-attempt (U2: repeat-avoidance).

### 2.2 Confidence calibration (past accuracy → current confidence)

**Requires:** The system's expressed confidence in an answer should track
its historical accuracy on similar queries. Overconfident errors should
reduce future confidence; reliable successes should increase it.

**TNN-2 status:** M1 partial (success/failure occurs, but "accuracy" needs
a correctness signal that does not exist per `c2a48bee6`), M2 no, M3 no,
M4 no. There is no confidence representation at all: `ev_query` returns a
bare i32. The decline analysis (G6) shows right and wrong answers are
white-box indistinguishable.

**Missing:** Everything. Confidence is not represented, accuracy is not
tracked, and no calibration loop exists. This is downstream of the
verification gap: without a correctness-substitute, "accuracy" cannot be
computed from learner state.

### 2.3 Strategy selection (past outcomes → current choice)

**Requires:** When multiple strategies exist for a pursuit, the choice
among them should reflect their track records.

**TNN-2 status:** M1 yes (strategies succeed or fail), M2 no, M3 no, M4
moot. TNN-2 has exactly one strategy per decision (fixed trial order,
single-schema revision, fixed eviction sweep), so there is nothing to
select between. Strategy selection presupposes a strategy inventory that
does not exist.

**Missing:** The forward machinery (multiple strategies) AND the backward
machinery (outcome records per strategy). This is a case where the
principle's boundary matters: the primary gap is forward (no strategies),
not backward. Consequence re-entry explains why TNN-2 would not LEARN
which strategy works, not why it has only one.

### 2.4 Trial-order learning (H3-lite Node 1)

**Requires:** The order in which trial families are attempted should
reflect which families have succeeded for similar queries.

**TNN-2 status:** This is what H3-lite Node 1 builds. The frozen prereg
(`9084a7760`) specifies field 32 (first-choice rejection count) with a
production write path (increment on rejection) and a production read path
(demote after 8 rejections, reordering the trial sequence).

**Analysis:** H3-lite Node 1 IS a narrow instance of consequence re-entry:
M1 (rejections occur), M2 (count retained per family), M3 (read before
trial ordering), M4 (order changes). It is the only planned M2/M3/M4
machinery in the current research program for any decision.

**Implication for the principle:** If Node 1 works (order flips to
counts-first after experience, causally attributable to the rejection
count), it confirms that the M1-M4 pattern is the right unit of analysis:
supplying the missing backward machinery enables the adaptation. If Node 1
fails despite correct M1-M4 implementation, it suggests the principle is
incomplete (something beyond re-entry is needed).

### 2.5 Guide learning (H3-lite Node 2)

**Requires:** The content of inquiry guides should reflect which guide
actions have resolved uncertainty.

**TNN-2 status:** H3-lite Node 2 builds this narrowly: `resolve_uncertainty`
writes on observation match, incrementing a resolution count that the guide
selection reads.

**Analysis:** Same pattern as 2.4: a narrow M1-M4 instance. The three-stops
synthesis (section 4) notes this is "the success half of the pursuit
lifecycle" while abandonment is the failure half. From the re-entry
perspective: Node 2 retains success consequences; the missing abandonment
machinery would retain failure consequences. They are the same principle
applied to opposite outcomes.

### 2.6 Repair-topology learning (H3-lite Node 3)

**Requires:** The choice of repair topology should reflect which topologies
have succeeded for similar contradictions.

**TNN-2 status:** H3-lite Node 3 builds the policy node; the write path
records repair outcomes per topology.

**Analysis:** Narrow M1-M4 again. Note the interaction with the V2 hole
(`705833a27`, CONFIRMED): if the repair criterion accepts wrong-but-running
repairs, then the "success" consequences recorded by Node 3 are corrupted.
Consequence re-entry amplifies whatever the criterion measures, correct or
not. This is a dependency the principle predicts: re-entry machinery is
only as good as the consequence signal it retains. Garbage in, garbage
re-entered.

### 2.7 Uncertainty-guided inquiry (ignorance → action)

**Requires:** Recorded ignorance should guide what the system does next
(which question to pursue, what evidence to seek).

**TNN-2 status:** M1 yes (misses occur), M2 partial (T30 nodes record
ignorance per (s,r), but unkeyed for lookup), M3 no (theater T5: zero
production readers), M4 no (`ev_act` keys off guides, never uncertainty).

**Missing:** The read path (M3). The write half exists; the T30 ablation
(`408bcfaa5`) proved it changes zero behavior. This is the canonical
"write half without read half" case.

### 2.8 Retention decisions (utility → eviction)

**Requires:** What to keep under memory pressure should reflect the
usefulness of structures, as revealed by experience.

**TNN-2 status:** M1 partial (structures are used or not, but "usefulness"
is not measured), M2 no, M3 no, M4 no. Eviction uses bid, which for MAPs
is a birth certificate (bid semantics `1538eeefe`), not a utility meter.

**Missing:** A utility signal (M1 for usefulness), retention of that
signal (M2), and consultation at eviction (M3/M4). The fossil census
(active worker) is measuring the consequence: structures retained without
function.

### 2.9 Verification (prediction error → criterion update)

**Requires:** When the system's correctness judgments prove wrong, the
criterion itself should update.

**TNN-2 status:** The verification criterion analysis (`c2a48bee6`)
found zero learner-internal criteria. There is no correctness-substitute
computation, so there is nothing to update.

**Missing:** The forward machinery (a correctness-substitute) AND the
backward machinery (updating it from error). The learned-similarity
analysis (`e8889bb17`) identified this as the root dependency: without
autonomous ground truth, any learned metric learns to predict harness
approval. Consequence re-entry cannot bootstrap a criterion from nothing;
it can only refine one that exists.

### 2.10 Transfer (past success → new domain attempt)

**Requires:** Success in domain A should increase the propensity to try
A's structures in domain B, and the outcomes should update that propensity.

**TNN-2 status:** M1 no (transfer never succeeds; zero transfer in
`cbd7bc803`), M2 no, M3 no, M4 no. The barriers (exact lookup, baked
literals) prevent the forward machinery from attempting transfer at all.

**Missing:** Primarily forward (similarity retrieval, rebinding). The
principle's boundary applies: consequence re-entry explains why TNN-2
would not IMPROVE at transfer with experience, but the reason it cannot
transfer AT ALL is missing forward machinery, not missing feedback.

### Summary table

| Function | M1 (gen) | M2 (retain) | M3 (read) | M4 (decide) | Primary gap |
|---|---|---|---|---|---|
| Decline | yes | no | no | no | backward |
| Abandonment | yes | no | no | no | backward |
| Forgetting | partial | no | no | no | backward |
| Learn from mistakes | yes | no | no | no | backward |
| Confidence calibration | partial | no | no | no | backward+forward* |
| Strategy selection | yes | no | no | moot | forward |
| Trial-order (H3-lite N1) | yes | planned | planned | planned | being built |
| Guide (H3-lite N2) | yes | planned | planned | planned | being built |
| Repair-topology (H3-lite N3) | yes | planned | planned | planned | being built |
| Uncertainty-guided inquiry | yes | partial | no | no | backward (M3) |
| Retention decisions | partial | no | no | no | backward+forward* |
| Verification update | no | no | no | no | forward |
| Transfer learning | no | no | no | no | forward |

*Forward gap noted: confidence needs a correctness-substitute; retention
needs a utility signal. These are M1 gaps (the consequence itself cannot
be generated), distinct from M2/M3/M4 gaps (the consequence is generated
but not retained/consulted/acted on).

---

## 3. Is consequence re-entry the right level of abstraction?

### 3.1 The generality risk

The danger: "the system doesn't learn from experience" is true of every
system that doesn't learn. If consequence re-entry merely restates "TNN-2
doesn't adapt," it explains everything and predicts nothing.

Three things keep it specific:

1. **The M1-M4 decomposition.** The principle does not just say "no
   learning"; it locates the absence at M2/M3/M4 while M1 is present.
   This is a falsifiable anatomical claim: it predicts that supplying
   M2/M3/M4 (without changing M1) will enable adaptation. H3-lite Node 1
   is the test.

2. **The forward/backward boundary.** The principle explicitly does NOT
   explain forward-machinery gaps (section 1.4, and the table above).
   Strategy selection, transfer, and verification-update have primary
   forward gaps. A principle that claimed to explain those too would be
   vacuous; this one disclaims them.

3. **The theater guard.** The principle includes a precise criterion for
   what counts as re-entry (M2+M3+M4 jointly, read-path-first). This rules
   out fake instances: a counter with no read path is not re-entry, it is
   T3 again. The principle is strict enough to classify its own
   counterfeits.

### 3.2 What would falsify it?

**F1. Adaptation without re-entry.** Find a TNN-2 capability that improves
with experience where M2/M3/M4 are absent. This would show that adaptation
does not require the machinery the principle claims is necessary. (Note:
the frozen battery scores do not qualify; they measure fixed capability,
not improvement with experience. The L2L2 transfer, `a530028ea`, is
unfrozen-variant evidence and its mechanism is `form_known`, a retained
consequence with a read path, consistent with the principle.)

**F2. Re-entry without adaptation.** Build correct M2/M3/M4 for a decision
(per the read-path-first standard) and observe zero causal improvement in
that decision's adaptivity. This would show that retention is not the
bottleneck. H3-lite Node 1 is the cleanest upcoming test: if the rejection
count is correctly retained and consulted but the trial order does not
causally improve, F2 is triggered for that decision.

**F3. A gap with full M1-M4 that still does not adapt.** Find a decision
where all four elements exist (by the strict standard) but experience
still does not improve performance. This would show the principle is
insufficient: something beyond re-entry is needed. No such case is
currently known in TNN-2, because no decision has full M1-M4.

**F4. A better unifying principle.** Propose an alternative that explains
all the backward gaps the principle explains, plus gaps it cannot, with
equal or fewer assumptions. The principle stands until displaced.

What would NOT falsify it:

- H3-lite failing for implementation reasons (wrong key, corrupted
  consequence signal as in 2.6, test design flaw). These falsify the
  instance, not the principle.
- Forward-machinery gaps remaining after re-entry is supplied. The
  principle predicts exactly this (section 1.4).
- Re-entry proving insufficient for L3. The principle claims necessity
  for adaptation, not sufficiency for representational invention.

### 3.3 The boundary, stated precisely

Consequence re-entry explains **adaptation failures**: the system does X,
X has outcomes, but the system does not do X better over time.

It does not explain:

- **Capability failures:** the system cannot do X at all (no forward
  machinery). Example: cross-domain transfer (no similarity/rebinding).
- **Representation failures:** the system cannot represent X. Example:
  learner-authored procedure semantics (no representational substrate).
- **Origination failures:** the system cannot generate X spontaneously.
  Example: self-initiated goals (no learner tick, per `3bf4d7bb4`).

The test for which side of the boundary a gap falls on: if the system
already performs the activity and generates the outcome (M1 present), but
does not improve, the gap is backward and the principle applies. If the
system does not perform the activity at all, the gap is forward and the
principle is silent.

This boundary is what prevents vacuity. The principle does not claim that
all of TNN-2's problems are one problem; it claims that all of TNN-2's
*adaptation* problems are one problem (missing M2/M3/M4), while its
capability, representation, and origination problems are different problems
requiring different analyses.

### 3.4 Alternatives considered

**"Write-mostly disease"** (state dynamics `ee238d8d4`). Describes the
symptom (lots of writing, no reading) but does not decompose it into
M1-M4 or distinguish backward from forward gaps. Consequence re-entry
is the more precise formulation: it specifies WHAT must be written
(consequences, keyed), WHERE it must be read (production decision paths),
and WHAT it must change (behavior at decision points).

**"No learner-owned criteria"** (criterion mechanism `8a2ff4b77`). Covers
the decision-point gap (M4) but not the retention gap (M2) or the read-path
gap (M3). A learner-owned criterion with no failure history to consult is
still blind. Consequence re-entry is broader: it includes the criterion
problem as the M4 element but adds the informational prerequisites.

**"No feedback loop"** (control theory). Equivalent in spirit but less
actionable: "feedback loop" does not specify the M1-M4 anatomy or the
theater guard. Consequence re-entry is the operationalized version: it
names the four elements, the keying requirement, and the read-path-first
test that distinguishes real loops from theater.

None of the alternatives is wrong; consequence re-entry is the most
precise. It survives as the working formulation until F4 (a better
principle) is produced.

---

## 4. What the principle predicts

If consequence re-entry is the right abstraction, the following should hold:

1. **H3-lite Node 1 should work** (for its narrow decision). It supplies
   M2/M3/M4 for trial-ordering. The principle predicts causal improvement
   in order adaptivity. Failure triggers F2.

2. **Supplying M2/M3/M4 for decline should enable withholding.** A
   per-pursuit failure history with a production read path at a query-path
   gate should produce withhold decisions that correlate with actual
   failure likelihood. This is untested; no such machinery exists.

3. **Forward-only fixes will not produce adaptation.** Adding a second
   repair topology (forward) without outcome retention (backward) will not
   make repair selection adaptive. The system will have more options and
   the same blindness. This predicts the failure mode of treadmill
   repairs: they add M1 variety without M2/M3/M4.

4. **The stops will come as a package or not at all.** Because they share
   the M2 substrate (per-pursuit failure retention), building decline
   without the substrate is impossible, and building the substrate makes
   abandonment and forgetting-inputs nearly free. The principle predicts
   that the marginal cost of the second and third stops, given the first,
   is low. This is the "one substrate, three gates" claim of the
   three-stops synthesis, restated as a prediction.

5. **Corrupted consequences will produce corrupted adaptation.** Per 2.6:
   if the V2 hole lets wrong-but-running repairs count as "success," then
   any re-entry machinery that retains repair outcomes will learn the
   wrong lesson. The principle predicts that re-entry amplifies criterion
   quality in both directions. This is testable once Node 3 exists.

Prediction 3 is the most practically important: it is the principled
statement of the no-patch-treadmill rule. A repair that adds forward
machinery without backward machinery is predicted to not produce
adaptation, no matter how clever the forward machinery is. This is why
"one more assembler" or "one more repair schema" cannot fix what ails
TNN-2: they are M1 additions to a system missing M2/M3/M4.

---

## 5. Relation to the lifetime vision

The north star is "one persistent learner whose intelligence grows because
its internal world becomes richer and more interconnected over experience."
Consequence re-entry is the mechanism by which "over experience" does work
in that sentence. Without M2/M3/M4:

- The internal world grows (nodes/edges accumulate) but does not become
  richer (no utility differentiation; fossils accumulate alongside live
  structures).
- It does not become more interconnected in the decision-relevant sense
  (edges exist, but none carry consequence information to decision points).
- Experience happens (260+ unsealed experiences in state dynamics) but
  does not compound (constant per-experience cost, repeated identical
  failures).

The lifetime protocol v2 (`dd745851e`) K-LT-5 (learning to learn) is, in
this vocabulary, the demand for consequence re-entry at the cross-task
level: experience with A must change the propensity to try A's structures
in B, and the outcomes must update that propensity. The weak/strong K-LT-5
split is a split in how far the re-entry reaches (same-relation vs
cross-relation), not in whether re-entry exists.

---

## 6. Standing architectural metric (this analysis)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (analysis only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0 added
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 added
- MODES: 0
- BRIDGES: 0
- HANDLERS: 0
- SEMANTIC CASES: 0

Functions surveyed: 13 (3 stops + 10 others). M1-M4 status tabulated for
each. Falsifiability conditions stated: 4 (F1-F4). Predictions: 5.
Alternatives considered: 3.

## 7. Explicit non-claims

- This analysis does not design consequence re-entry machinery. The M1-M4
  anatomy is a diagnostic framework, not a blueprint.
- It does not claim consequence re-entry is sufficient for any L3, SUF,
  or C0 bar. It claims necessity for adaptation, not sufficiency for
  invention.
- It does not claim the 13 surveyed functions are exhaustive. Opcode-level
  execution failures, multi-pursuit scheduling, and developmental
  trajectories are not surveyed here.
- It does not predict H3-lite outcomes. Prediction 1 is a conditional
  (IF M2/M3/M4 correctly implemented, THEN causal improvement expected),
  not a forecast.
- It does not alter any frozen prereg, including H3-lite `9084a7760`.
- DRAFT-NOT-FROZEN.

---

**Verdict: CONSEQUENCE-REENTRY-COMPLETE.**
