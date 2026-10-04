# Learning from Experience: Minimal Machinery Specification

**Status:** SPECIFICATION ONLY. Requirements, not design. No
implementation proposed, no variant built, no TNN-3 designed.
**Date:** 2026-10-01
**Parents:** Genuine state (`a5b66a376`), consequence re-entry
(`7eab34ff2`), success criteria (`04af42736`), scaling
(`02804f782`), H3-lite frozen prereg (`9084a7760`)
**Verdict:** LEARNING-MACHINERY-COMPLETE

---

## 0. What this document is and is not

This document specifies the minimal machinery a system needs for its
behavior to change because of its experience, where the change is
causally attributable to the experience rather than to a fixed program
that would have behaved identically without it. It names components,
their required properties, and how they interact. It does not specify
field layouts, opcodes, or algorithms; that is TNN-3 design work and is
explicitly out of scope. Every requirement below is traceable to a
confirmed empirical finding in the parent analyses.

---

## 1. Definition of "learning from experience"

### 1.1 Storage is not learning

TNN-2 stores facts, guides, MAPs, edges, and counters. The state
dynamics analysis (`ee238d8d4`) found write-mostly growth with no
convergence and repeated identical misses. The theater audit
(`e0423538a`, empirically confirmed by ablation) found six recorded
structures that no production decision reads. Storage that no decision
consults is accumulation, not learning. The minimal definition must
exclude it.

### 1.2 The counterfactual test (minimal observable difference)

A system learns from experience iff all three hold:

1. **Behavioral difference:** two instances with identical starting
   state, exposed to different experience histories, then given the
   same probe, behave differently (different return value, different
   structure built, different action taken, or a withheld response
   where the other answers).
2. **State mediation:** the behavioral difference is mediated by a
   learner-state difference (white-box traceable), not by a difference
   in the current input or in harness configuration.
3. **Causal attribution:** the learner-state difference was written by
   a production write path firing on the differing experience (not
   initialized differently, not written by test scaffolding). Removing
   that write path (ablation) removes the behavioral difference.

Condition 3 is the K-H3 write-path audit (`9084a7760`, section 4)
generalized beyond policy nodes. It is what separates learning from
coincidence: the experience must have caused the state change through
the system's own production machinery.

Note what this definition does not require: it does not require the
learned behavior to be correct, optimal, or general. A system that
learns the wrong lesson from experience (the corrupted-consequence
case, section 2.5) still learns; it learns badly. Correctness of what
is learned is a separate requirement (sound success criteria), treated
in section 2.5.

### 1.3 What does not count (negative definition)

- **L0 accumulation:** facts stored and retrieved, no decision changed.
  (TNN-2's FACT store.)
- **Fixed-program drift:** behavior changing over time for reasons
  independent of experience content. Example: PRO TTL decay changes
  which nodes are protected, but the decay schedule is fixed; no
  experience content alters it. Time passing is not experience.
- **Harness-supervised updating:** a policy value changing because the
  harness supplied the right answer (unmasked Node 1, per
  `04af42736` section 2.3). The state change is experience-caused but
  the experience is the supervisor's judgment, not the learner's. This
  is supervised tuning, a subset of learning but not autonomous
  learning from experience.
- **Executability-order learning:** reordering by "what runs" rather
  than "what works" (masked Node 1, per `04af42736` section 2.2). The
  criterion is vacuous; the system adapts to a signal with no
  correctness content.
- **Incumbency without content:** guide USE self-edges making past
  winners win ties (genuine state's "weak USE incumbency"). This
  passes the counterfactual test in the letter (behavior differs by
  history) but the retained signal carries no information about
  whether the past selection was good. It is learning in the
  degenerate sense: history-dependent but content-free. The
  specification below requires consequence content (section 2.1),
  which incumbency lacks.

The last two cases matter because they show the definition's three
conditions are necessary but not sufficient for *useful* learning.
Sections 2.5 (sound criteria) and 2.6 (source provenance) supply the
sufficiency direction.

### 1.4 Relation to the L0/L1/L2/L3 taxonomy

- **L0 (storage):** fails condition 1 or 3. Ruled out.
- **L1 (parameter learning):** passes all three within
  researcher-fixed forms. H3-lite Node 1, if it works, is L1:
  parameters (order slots) fitted to experience within an enumerated
  family.
- **This specification's target:** the machinery that makes L1
  possible at all, plus the stopping decisions (decline, abandonment,
  forgetting), which are L1 over the policy of *whether to act*.
  The specification does not reach L2 (structural invention) or L3
  (representational invention); those need open structural forms,
  which are explicitly out of scope (H3-lite non-claims 1-3, 6).
- **Boundary:** a system satisfying this specification learns from
  experience in the minimal sense. It does not thereby invent
  procedures, representations, or concepts. Those are further
  frontiers requiring additional machinery (open construction,
  representational substrate) that this document does not specify.

---

## 2. Minimal machinery: the components

Seven components. The first four are the M1-M4 anatomy from
consequence re-entry (`7eab34ff2`, section 1.3), restated as
requirements. The last three are prerequisites the parent analyses
proved necessary for the four to produce sound learning rather than
theater or corrupted learning.

### 2.1 C1: Consequence generation (M1)

**Requirement:** the system's activity must produce outcomes that
carry information about success, cost, or repeat-worthiness, keyed to
the decision or structure that produced them.

**Present in TNN-2:** yes. Trial candidates verify or fail (F1),
revision succeeds or returns 0 (F3), bootstrap agrees or disagrees
(F4), queries hit or miss, observations confirm or contradict. The
genuine state inventory lists every production outcome site.

**What is missing:** keying. Outcomes occur but are not tagged with
*which* pursuit, *which* query shape, or *which* structure produced
them. A trial failure is an event; "chain k=4 failed on (s,r) with
these properties" is a keyed consequence. TNN-2 generates the former,
not the latter. Requirement C1 therefore includes: every generated
consequence must carry the identity of the decision point and the
pursuit it belongs to. Unkeyed outcomes cannot be retained usefully
(theater T4: the event log records everything keyed by nothing).

**Non-requirement:** C1 does not require new outcome types. The
existing F1-F7 inventory suffices as the consequence vocabulary for
the decisions that exist.

### 2.2 C2: Shared retention substrate (M2)

**Requirement:** keyed consequences must be retained in queryable form:
findable by decision point and pursuit, readable by production code,
with both success and failure halves.

**The shared-substrate claim:** the three-stops synthesis
(`48cb843e5`) argues decline, abandonment, and forgetting should draw
on one per-pursuit outcome record, not three separate counters. This
specification adopts that claim as a requirement: the substrate is
one keyed store of pursuit outcomes (attempts, successes, failures,
costs), consulted by every stopping and policy decision. Separate
per-node counters (H3-lite's field 32 here, another counter there)
are the narrow alternative; they work for their node but do not
compose, and each new decision needs a new counter. The shared
substrate is the architectural-compression choice.

**Required properties:**
- **Keyed by pursuit and decision:** a later query for "how did
  attempts at this pursuit go" must find the record. Pursuit identity
  needs definition (same (s,r)? same query shape? same structure
  under revision?), but the requirement is that *some* stable key
  exists; unkeyed tallies do not satisfy C2.
- **Both halves:** success records AND failure records. H3-lite Node 3
  as preregistered records only successes ("on total failure: no
  counter changes"); the success criteria analysis (`04af42736`,
  section 4.2) flags this as one-sided learning. A substrate that
  cannot represent "this failed" cannot support decline or
  abandonment, which are failure-driven decisions.
- **Bounded:** the scaling analysis (`02804f782`) puts the node budget
  wall at hundreds of events. Every retained consequence costs nodes
  or fields. C2 therefore requires a bounded per-pursuit record
  (counters and recency summaries, not unbounded event lists) and a
  reclamation policy for stale pursuits. Unbounded retention
  accelerates saturation; the substrate must be cheaper than the
  decisions it informs.
- **Source-tagged:** see C6. The retention write path must record the
  source of the consequence (see section 2.6).

**What TNN-2 has:** nothing satisfying these properties. The two
existing consequence channels (PRO refresh, guide USE incumbency) are
local, unkeyed, success-only, and content-free.

### 2.3 C3: Production read paths (M3)

**Requirement:** every decision named in C4 must consult C2 in its
normal production operation, via a code path exercised on ordinary
world interaction (not test-only).

**The read-path-first rule** (theater audit, failure retention
`d3e896c8c` section 4.3): a retained consequence no production
decision consults is theater, regardless of how carefully it is
written. C3 is therefore stated as a negative requirement with teeth:
for each claimed read path, the evaluation must show the path firing
on transcript and the decision changing (or identifiably not changing)
because of what was read. H3-lite's K-H3 audit conditions (b) and (c)
are the instance of this rule for policy nodes; C3 generalizes it to
all adaptive decisions.

**Required properties:**
- ** exercised, not merely existing:** source presence of a read is
  insufficient (T5: UNCERTAINTY nodes had a real read path in source
  that production never exercised; ablation `408bcfaa5` changed zero
  of 62 return values).
- **Keyed lookup, not ambient scan:** the read must find the record
  for *this* pursuit. A global counter consulted identically for all
  pursuits is not a read path for per-pursuit adaptation.

### 2.4 C4: Decision points (M4)

**Requirement:** the architecture must contain gates where consulted
consequences change behavior. Minimal set:

1. **Decline gate (query path):** "should I answer?" Consults C2 for
   the pursuit; withholds (returns a distinguished decline, not -2
   pipeline exhaust) when predicted failure likelihood is high. The
   decline-signal analysis (`9e0ae81d1`) found zero withhold events
   and no gate; this is the missing M4 for the query path.
2. **Abandonment gate (inquiry/revision path):** "should I keep
   trying?" Consults per-pursuit attempt/failure counts; stops
   re-attempting after a bound. The abandonment analysis
   (`ae76a60a7`) found zero attempt counters; failed inquiries
   accrete unboundedly.
3. **Retention input (eviction path):** "what is worth keeping?"
   Consults per-structure utility (C7) at reclamation. The forgetting
   analysis (`2726baf74`) found eight researcher-fixed retention
   rules with zero learner input.
4. **Policy reorder (existing H3-lite decisions):** trial order,
   guide default, repair topology. These are the H3-lite nodes; C4
   includes them as the "which action" decisions complementing the
   three "whether/when" stops.

**Ordering:** the three-stops synthesis ranks implementation
decline-substrate first, then abandonment, then forgetting driven by
abandonment. This specification concurs: C2 (with failure halves) is
the prerequisite; the decline gate is the first M4 to build on it;
abandonment reuses the same substrate; eviction input is last because
it additionally needs C7 (utility).

**Non-requirement:** C4 does not require any particular threshold
values or update rules. Thresholds are researcher-set initially (as in
H3-lite's demotion-at-8 and margin-2); the requirement is that the
gate exists, reads C2, and changes behavior.

### 2.5 C5: Sound success criteria (correctness-substitute)

**Requirement:** the "success" and "failure" events retained in C2
must measure what the decision needs to know, not a vacuous,
supervised, correlational, or broken proxy.

**Why this is load-bearing:** the success criteria analysis
(`04af42736`) proved that all three H3-lite nodes' criteria are
unsound as preregistered: Node 1 learns executability or
harness-approval, Node 2 learns correlation (possibly never firing),
Node 3 learns from the confirmed-broken V2 criterion (wrong-but-running
repairs count as success). Consequence re-entry amplifies criterion
quality in both directions ("garbage in, garbage re-entered,"
`7eab34ff2` section 2.6). C1-C4 with corrupt C5 produce *confident
maladaptation*: the system learns the wrong lesson efficiently. That
is worse than not learning, because it is harder to detect (the
machinery works; the signal lies).

**Minimum sound criteria per decision** (from `04af42736` section 6):
- **Repair (Node 3):** the repaired graph must compute the observed
  value (`out == new_o`). The information is already present; the
  check is unperformed. This is the tractable fix: not a treadmill,
  because it completes the criterion the code already intends. The
  Probe-2 subtlety (a defensible repair where the count genuinely did
  not change) is noted but does not block the simple check as the
  minimum.
- **Trial order (Node 1):** needs a learner-internal correctness
  judgment (verification Component A, `c2a48bee6` section 7), which
  does not exist. Minimum honest proxy with existing machinery: track
  which families' promoted structures survive without later
  contradiction (are not revised away). Delayed, noisy, but
  learner-internal and causally downstream of the family's work. Any
  researcher-defined shape preference ("prefer families whose outputs
  look like X") is one step from a domain detector; treadmill risk
  HIGH.
- **Guide default (Node 2):** needs causal attribution of resolutions
  to actions, which needs action variation (currently every guide gets
  the default; nothing to learn from) and a with/without comparison.
  Both need experimentation machinery that does not exist
  (`3bf4d7bb4`). Treadmill risk HIGH for any researcher-specified
  "good action."
- **Decline/abandonment:** needs predicted failure likelihood, which
  needs per-pursuit failure history (C2) plus a mapping from history to
  prediction. The mapping can start as a fixed researcher function
  (e.g., decline after k consecutive failures); the requirement is
  only that its *inputs* are retained consequences, not researcher
  constants.

**Honest consequence:** C5 is the deepest requirement. C1-C4 are
plumbing; C5 is the water quality. A system can satisfy C1-C4 with
corrupt C5 and thereby fail the *intent* of learning from experience
while passing its letter (the counterfactual test). Any evaluation of
learning machinery must therefore audit C5 per decision (the section 7
guardrails of `04af42736`) in addition to checking M1-M4 presence.

### 2.6 C6: Source provenance on retained consequences

**Requirement:** every consequence retained in C2 must be tagged with
its source: taught (harness-supplied), observed (environmental), or
self-generated (bootstrap inference, revision output, MAP shadow).

**Why this is load-bearing:** the teach/observe analysis (`8744796fb`)
proved five sources collapse into indistinguishable tag-1 FACTs, and
the bootstrap-loop probe (`ee7815de8`) proved the consequence: after
kickstart, unanimity verdicts rested on purely self-generated
evidence, state-indistinguishable from genuine confidence. A C2
substrate without source tags would retain the system's own guesses
as if they were evidence and then learn from them: a closed
self-referential loop that the counterfactual test cannot detect
(behavior differs by history; the history is self-generated; the
white-box trace shows the write path firing; all three conditions
pass, yet nothing was learned from the world).

**Required properties:**
- **Tags at write time:** the retention write path must record which
  of the (at least) three source classes produced the consequence.
  Source identity currently exists only in the write-only event log
  (theater T4); C6 requires it on the retained record itself.
- **Per-consumer source policies:** different decisions need different
  source weightings. Bootstrap must not count self-generated guesses
  as observations (the confirmed loop). Revision must distinguish
  teaching conflict from environmental contradiction. The requirement
  is the tagging infrastructure plus at least the bootstrap exclusion;
  full per-consumer policies are downstream work.
- **Interaction with C5:** a success criterion computed over
  self-generated "evidence" is corrupt by construction. C6 is
  therefore a prerequisite for C5 soundness wherever the consequence
  stream can contain self-generated entries (bootstrap, revision
  outputs, MAP shadows).

**Scope note:** C6 is listed as a separate component rather than a
property of C2 because the teach/observe conflation is independently
load-bearing (it also breaks revision semantics and bootstrap
validity outside any learning machinery) and because retrofitting tags
onto the existing five-writer FACT store is a distinct work item from
building the retention substrate.

### 2.7 C7: Per-structure utility signal

**Requirement:** structures (MAPs, and eventually guides and facts)
must carry a utility measure that reflects their contribution to
successful cognition, distinct from their birth bid, updated by
experience, and consulted at retention decisions.

**Why:** the bid analysis (`1538eeefe`) proved MAP bid is a birth
certificate (fixed at promotion, never updated by use), and no
production logic adds bid-relevant evidence to a MAP after promotion.
Eviction therefore cannot prefer useful structures; it rations by
accident of birth order and protection TTL. C4's retention input has
nothing sound to consult without C7.

**Minimum content:** for MAPs, at minimum: execution count (how often
the structure's answers were used), contradiction count (how often its
answers were contradicted), revision count (how often it needed
repair). These are computable from existing events (query hits via
shadow FACTs, `ev_observe` contradictions, `t2_rev -e_graph` calls)
but are not currently recorded per structure. The requirement is the
per-structure record and its consultation at eviction; the exact
utility function combining the counts is downstream.

**Dependency:** C7 needs C1 (the outcome events) and C6 (so that
uses driven by self-generated shadows are not counted as genuine
utility). It is downstream of C2 in implementation order but is
listed separately because "utility of a structure" and "outcome of a
pursuit" are different keys: C2 is keyed by pursuit, C7 by structure.
A MAP used by many pursuits needs both.

### 2.8 How the components interact

The normal lifetime loop with all seven components in place:

1. An event arrives (teach, query, observe, act). C1 generates
   keyed consequences: what was tried, what it cost, whether it
   succeeded by the decision's C5 criterion, tagged with source (C6).
2. The consequences are written to C2 (per-pursuit outcome record)
   and to C7 (per-structure utility), both bounded and source-tagged.
3. Before the next decision at any C4 gate, the gate reads C2 (and
   C7 for retention): decline consults pursuit failure history;
   trial order consults family outcome records; eviction consults
   structure utility.
4. The gate's behavior changes accordingly: withhold, reorder,
   abandon, or reclaim. The change is white-box traceable to the
   retained consequences (condition 3 of the counterfactual test).
5. The gate's own outcome becomes a new C1 consequence (did the
   decline avoid a failure? did the reorder help?), closing the loop.
   Second-order learning (learning about the gates) is downstream;
   the minimum is first-order.

The data flow is: experience -> C1 (keyed, sourced) -> C2/C7
(retained, bounded) -> C4 (gates) via C3 (reads), with C5 judging
every success/failure event and C6 tagging every retained entry.
Remove any one component and the loop degrades to a known failure:
no C1, nothing to learn from; no C2, theater; no C3, write-only;
no C4, no behavioral change; corrupt C5, confident maladaptation;
no C6, self-referential loops; no C7, blind retention.

---

## 3. Gap mapping

### 3.1 The nine gaps (from `a5b66a376`, section 5)

1. No consequence re-entry (M2/M3/M4 absent; only two local ungraded
   channels).
2. No failure memory (seven signals, five discards, zero counters).
3. No source provenance (five writers, one tag; load-bearing
   conflation).
4. No query-time execution (MAP graphs inert on query path).
5. No utility signal for structures (MAP bid is a birth certificate).
6. Write-once policy substrate (POLICY_ROOT set at first miss, never
   revised).
7. Vestigial edge types and dead code (5 of 13 edge types dead weight;
   sum family unreachable).
8. Context is four raw integers (no abstraction or salience).
9. Clock without comparison (timestamps stored, never compared).

### 3.2 Prerequisites vs independent

**Prerequisite chain (must be built in this order):**

- **Gap 1 (C2 substrate) is the root prerequisite.** Every adaptive
  decision needs retained consequences. Build the shared per-pursuit
  outcome store first, with failure halves (gap 2 is the failure half
  of gap 1; they are one work item, not two).
- **Gap 3 (C6 provenance) is co-prerequisite with gap 1.** The
  substrate must be source-tagged from its first write; retrofitting
  tags onto an untagged substrate repeats the conflation. The
  bootstrap exclusion (self-generated entries do not count as
  observations) must hold before any success criterion consumes the
  substrate, or C5 is corrupt from the start.
- **Gap 5 (C7 utility) is prerequisite for the retention gate only.**
  Decline, abandonment, and policy reorder do not need per-structure
  utility; eviction input does. Build after C2, before touching the
  eviction rule.
- **Gap 6 (policy substrate) is the H3-lite work item.** It is a
  narrow instance of C2/C3/C4 for three decisions. It can proceed in
  parallel with the shared substrate but should converge onto it: the
  narrow counters are the prototype, the shared store is the target.
  Do not build both permanently (architectural compression).
- **C5 (sound criteria) is prerequisite per decision, not globally.**
  Each gate needs its criterion audited before its learning claim is
  interpreted (the `04af42736` guardrails). The Node 3 fix
  (`out == new_o`) is the only tractable one with existing machinery;
  Node 1 needs Component A, Node 2 needs experimentation machinery.
  A gate built on an unaudited criterion must be reported as
  "revisability machinery with unsound signal," not as learning.

**Independent (can be built in any order relative to the chain):**

- **Gap 4 (query-time execution):** forward machinery. The backward
  loop (C1-C7) operates on the decisions that exist; making MAPs
  execute on the query path adds new decisions (execute vs cache)
  that then need their own C1-C7 treatment, but their absence does
  not block learning about trial order, decline, or retention. The
  consequence re-entry boundary (`7eab34ff2`, section 3.3) applies:
  this is a capability gap, not an adaptation gap.
- **Gap 7 (vestigial types, dead code):** hygiene. Removing dead edge
  types and the unreachable sum family reduces scan cost (every dead
  type still occupies the type space; unreachable code still misleads
  readers) but changes no adaptive behavior. Do it for compression,
  not for learning.
- **Gap 8 (context):** limits what pursuits can be keyed and matched
  on, which caps the *discrimination* of C2 keys, not their
  existence. A richer context improves learning quality later; four
  raw integers suffice for the minimal loop.
- **Gap 9 (clock):** recency-weighted retention and forgetting curves
  need temporal comparison eventually, but the minimal substrate can
  key on allocation order and outcome counts first. Secondary.

### 3.3 Minimal viable set

The smallest component set satisfying the counterfactual test for at
least one "whether" decision and one "which" decision:

1. **C2:** shared per-pursuit outcome store, success and failure
   halves, bounded, with C6 source tags from the first write
   (gaps 1, 2, 3 together).
2. **C3:** one production read path: the decline gate consulting the
   pursuit record before answering.
3. **C4:** two gates: decline (whether to answer) and trial reorder
   (which family first; the H3-lite Node 1 mechanism pointed at the
   shared store rather than its narrow counter).
4. **C5:** audited criteria for exactly those two gates: decline uses
   consecutive-failure count (researcher-fixed mapping, sound inputs);
   trial reorder uses the survival-without-contradiction proxy
   (section 2.5) or is reported as unsound-signal revisability.
5. **C7 deferred:** eviction keeps its current rule until utility
   exists; the minimal set does not touch retention.

This set is deliberately narrow: it proves the loop
(experience -> retained consequence -> changed decision) twice, once
for stopping and once for selection, with sound inputs. Everything
else (abandonment, Node 2, Node 3, utility, query-time execution) is
a further gate on the same substrate, not new machinery.

### 3.4 Cost interaction (scaling constraint)

The scaling analysis puts the node-budget wall at hundreds of events
and per-event scan cost linear in table size. C2 writes add nodes or
fields per pursuit; C7 adds fields per structure. Two consequences:

1. **The learning machinery hastens saturation.** Every retained
   consequence consumes budget. An unbounded C2 (per-event records)
   would fill the table faster than the current write-mostly growth.
   The boundedness requirement in section 2.2 is therefore not an
   optimization; it is a feasibility condition. Counters and
   summaries, fixed small per pursuit, with reclamation of stale
   pursuits.
2. **The machinery does not fix scaling.** Nothing in C1-C7 makes
   retrieval sublinear or reclamation non-destructive (scaling
   requirements 1-3, `02804f782` section 6). Learning from experience
   and lifetime viability are distinct problems: this specification
   addresses whether behavior improves with experience *within* the
   feasible envelope (~10^2-10^3 events); the lifetime scoper
   (parallel worker) addresses what fits in that envelope. Do not
   claim this machinery extends the envelope.

---

## 4. Distinguishing from H3-lite

### 4.1 H3-lite as narrow consequence re-entry

Each H3-lite node is a narrow M1-M4 instance (consequence re-entry
`7eab34ff2`, sections 2.4-2.6): Node 1 retains family rejection
outcomes and reorders trials; Node 2 retains resolution co-occurrences
and revises the guide default; Node 3 retains repair outcomes and
revises topology preference. In this specification's vocabulary, each
node implements C1 (its outcome events), a narrow C2 (its counters),
C3 (its read path), and C4 (its decision). H3-lite is therefore a
proper subset of learning-from-experience machinery: three "which"
decisions, no "whether" decisions, narrow per-node stores instead of a
shared substrate.

### 4.2 What H3-lite lacks for the full specification

1. **Shared substrate (C2):** three separate counters, not one
   per-pursuit store. The decline/abandonment/forgetting decisions
   have no substrate at all.
2. **Stopping decisions (C4):** decline, abandonment, and retention
   input are out of scope (H3-lite non-claim 5 partially; the stops
   are simply not addressed).
3. **Sound criteria (C5):** as preregistered, all three nodes'
   success criteria are unsound (`04af42736`). H3-lite as frozen
   tests revisability *machinery*; whether the nodes learn the right
   lesson depends on criteria the prereg does not supply (except the
   tractable Node 3 fix, which is not in the frozen prereg).
4. **Source provenance (C6):** no tagging; the bootstrap loop hazard
   applies to any node whose consequence stream includes
   self-generated entries.
5. **Utility (C7):** untouched.
6. **Open forms:** explicitly disclaimed (H3-lite non-claims 1-3, 6).
   This specification likewise does not reach L2/L3; the distinction
   is noted so that H3-lite passing is not misread as structural
   learning.

### 4.3 Interpretation rule for H3-lite results

- **If a node passes K-H3 with its guardrail satisfied** (`04af42736`
  section 7): that decision is revisable by experience. This is
  evidence for the consequence re-entry principle's necessity claim
  (F2 not triggered for that decision) and a prototype of C1-C4. It
  is not evidence of learning from experience in the full sense
  (C5-C7 and the stops remain open) and not evidence of L2/L3.
- **If a node passes K-H3 but fails its guardrail** (e.g., Node 3
  preference shifts on wrong-but-running repairs): the machinery
  works and the signal is corrupt. Report as "revisability with
  unsound criterion," i.e., confident maladaptation, not learning.
  This outcome confirms the C5 requirement rather than refuting the
  principle.
- **If a node fails K-H3 despite correct M2/M3/M4 implementation:**
  F2 is triggered for that decision; the principle's necessity claim
  fails there and the program must look elsewhere (per the prereg's
  diagnostic purpose, section 1).

### 4.4 What goes beyond H3-lite (ordered)

1. Shared C2 substrate replacing narrow counters (compression).
2. Decline gate (first stopping decision; reuses C2).
3. Abandonment gate (same substrate, failure half).
4. C5 audits per decision; Node 3 criterion fix.
5. C6 source tags on the substrate; bootstrap exclusion.
6. C7 per-structure utility; eviction input.
7. Node 1 criterion via Component A or survival proxy; Node 2 via
   experimentation machinery (both currently blocked; listed for
   completeness, not as near-term work).
8. Open structural forms (L2/L3 frontier; outside this
   specification).

Items 1-6 are the learning-from-experience program. Items 7-8 are
the deeper frontiers. H3-lite is item 0: the diagnostic prototype.

---

## 5. What would show this specification wrong

The specification is a requirements document, but its load-bearing
claims are falsifiable:

- **S1 (necessity of M2/M3/M4):** if H3-lite Node 1 (or any decision)
  shows causal adaptation with correct M2/M3/M4 absent, the
  consequence re-entry necessity claim fails. (Same as F2 in
  `7eab34ff2`.)
- **S2 (shared substrate):** if three narrow per-decision counters
  prove sufficient for decline, abandonment, and forgetting with no
  composition problems and no counter proliferation as decisions are
  added, the shared-substrate requirement is overstated; narrow
  counters suffice.
- **S3 (C6 co-prerequisite):** if a node learns soundly (passes its
  guardrail) while its consequence stream includes untagged
  self-generated entries, source provenance is not the load-bearing
  hazard the bootstrap loop suggests; it can be deferred.
- **S4 (C5 priority):** if corrupt-criterion learning is reliably
  detected and corrected by the learner itself without an external
  audit (i.e., the system notices its repairs are wrong despite the
  criterion saying success), then second-order correction exists and
  C5 strictness can be relaxed.
- **S5 (minimal set):** if the decline gate plus trial reorder
  (section 3.3) proves insufficient to demonstrate the loop, i.e.,
  the counterfactual test passes but no downstream decision
  benefits, the minimal set is misidentified.

What would NOT show it wrong: H3-lite failing for implementation
reasons; forward-machinery gaps (transfer, query-time execution)
remaining; L2/L3 not emerging. The specification claims necessity
for adaptation, not sufficiency for invention.

---

## 6. Standing architectural metric (this specification)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 added (specification only;
  the components are requirements, not code).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0 (C5 specifies what sound criteria
  would be; none are built here).
- REUSE EVENTS: 0.
- REVISION EVENTS: 0.
- COGNITION LINES: 0.
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

Functions specified: 7 components (C1-C7). Gaps mapped: 9 (from
`a5b66a376`). Prerequisite chain: C2+C6 first, then C4 gates, then
C7; C5 audited per decision; gaps 4, 7, 8, 9 independent. Minimal
viable set: 5 items (section 3.3). Falsifiability conditions: 5
(S1-S5).

---

**Verdict: LEARNING-MACHINERY-COMPLETE.**
