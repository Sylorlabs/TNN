# Shared Retention Substrate: Specification

**Status:** SPECIFICATION ONLY. Requirements, not design. No
implementation proposed, no variant built, no TNN-3 designed.
**Date:** 2026-10-01
**Parents:** Learning machinery (`3416ed218`), consequence re-entry
(`7eab34ff2`), three stops (`48cb843e5`), H3-lite Node 1
(`45c55ed83`)
**Verdict:** SHARED-SUBSTRATE-COMPLETE

---

## 0. What this document specifies

The learning machinery specification (`3416ed218`, section 3.3) names
the minimal viable set as: "shared source-tagged substrate + decline
gate + trial reorder + audited criteria for those two gates." The
consequence re-entry analysis (`7eab34ff2`, section 1.3) requires M2
(retention in queryable form) as the missing element for every
adaptation decision. The three-stops synthesis (`48cb843e5`, section
2) requires "one substrate, three gates": decline, abandonment, and
eviction input all consuming per-pursuit outcome records.

This document specifies that substrate: what is stored, how it is
keyed, who writes, who reads, how H3-lite's narrow counters converge
onto it, and how it stays bounded. It does not specify field offsets,
opcodes, or algorithms; that is TNN-3 design work and is explicitly
out of scope.

---

## 1. Definition

The shared retention substrate is one keyed store of pursuit and
strategy outcomes. Each record summarizes what happened when the
system pursued something: how many attempts, how many succeeded, how
many failed, in what mode the last failure occurred, what it cost,
and what source class the retained consequences came from.

**What makes it "shared":** one record format, one keyed lookup
mechanism, one source-tagging convention, one reclamation policy,
serving all adaptive decisions. The alternative is what exists now:
H3-lite Node 1 keeps a private rejection counter in field 32 of its
policy node; nothing else keeps any counter; each new adaptive
decision would need its own private counter with its own ad hoc
semantics. The learning machinery spec (section 2.2) adopts the
shared-substrate claim as a requirement on architectural-compression
grounds: narrow counters work for their node but do not compose.

**What makes it "retention" rather than "logging":** every record
has at least one production read path that can change a decision
(the read-path-first rule, `7eab34ff2` section 1.2). A record no
production decision consults is theater (T3/T4 pattern), regardless
of how carefully it is written.

**What it is not:** it is not the event log (theater T4: records
everything, keyed by nothing, read by nothing). It is not a second
FACT store (facts record world content; the substrate records
pursuit outcomes). It is not a policy node (policy nodes hold a
decision's current setting; the substrate holds the evidence the
setting is based on).

---

## 2. Record format

Each substrate record carries the following fields. All are fixed
width counters or small enumerations. No unbounded lists, no
histories, no traces. (Boundedness is section 7; the fixed width is
load-bearing, not incidental.)

### 2.1 Identity fields

- **key_type:** which namespace this record belongs to (section 3).
  Values: PURSUIT (an inquiry or repair campaign) or STRATEGY (a
  reusable decision option such as a trial family).
- **key:** the pursuit or strategy identity. For PURSUIT: the (s, r)
  pair for inquiries, or the MAP node id for repair campaigns (per
  `48cb843e5` section 2.3). For STRATEGY: the family id (trial
  assembler family) or topology id (repair topology).

### 2.2 Outcome fields

- **attempts:** total attempts recorded for this key. Incremented on
  every attempt (trial run, repair attempt, query answered or
  declined).
- **successes:** total successes. Incremented when the attempt meets
  the decision's audited success criterion (C5, `3416ed218` section
  2.5).
- **consec_fail:** consecutive failures. Incremented on failure,
  reset to zero on success. This is the primary gate input (decline
  and abandonment both consult it). The three-stops synthesis
  (section 2.1) requires the reset half: "retention of failure
  without retention of success produces a system that only ever
  becomes more pessimistic."
- **last_mode:** the failure mode of the most recent failure,
  using the F1-F7 vocabulary from failure retention (`d3e896c8c`
  section 1): trial candidate rejection, trial exhaustion, revision
  failure (five sub-modes), bootstrap disagreement (two sub-modes),
  resource exhaustion, activation miss. Zero when the last attempt
  succeeded. Enables future repeat-avoidance; not required for the
  minimal gates.

### 2.3 Cost fields

- **cost_nodes:** total nodes allocated across attempts for this key
  (capped at a saturating maximum; the exact cap is design detail).
- **cost_tries:** for STRATEGY keys, total candidate attempts (trial
  families tried). This generalizes H3-lite Node 1's field-32
  rejection count into the shared format.

### 2.4 Source fields (C6 integration)

- **src_taught:** attempts whose triggering consequence was
  harness-taught (per `8744796fb` source taxonomy).
- **src_observed:** attempts triggered by environmental observation.
- **src_self:** attempts triggered by self-generated consequences
  (bootstrap inference, revision output, MAP shadow).

These three counters partition `attempts` by source class. The
learning machinery spec (section 2.6) requires source tags from the
first write because the bootstrap-loop probe (`ee7815de8`) proved
untagged substrates learn from their own guesses. The minimal
consumer rule: the decline gate and the bootstrap must exclude
`src_self` attempts from their failure/success tallies (a guess
confirming itself is not evidence). Full per-consumer source policies
are downstream work; the tagging infrastructure and the
self-exclusion rule are the requirement.

### 2.5 Lifecycle fields

- **state:** ACTIVE, ABANDONED, or RE-ENGAGED (per `48cb843e5`
  section 2.3). Written by the abandonment gate; consulted by
  eviction (abandoned pursuits' structures are the safe-reclaim set)
  and by any re-engagement logic.
- **last_active:** event-sequence number of the most recent attempt.
  Used by the reclamation policy (section 7), not by any cognitive
  gate. (The genuine-state analysis found the clock is never
  compared; `last_active` uses the existing event counter, which is
  compared nowhere today. Its only consumer is reclamation.)

### 2.6 What is explicitly NOT in the record

- No per-event history (no G3 temporal sequences). Counters and
  summaries only.
- No graded failure (no G4 correctness grades). Binary
  success/failure per the audited criterion.
- No learner-derived categories (no G5). `last_mode` uses the
  fixed F1-F7 vocabulary; treating it as provisional scaffolding
  with a retirement condition is required (treadmill guard from
  `48cb843e5` section 3).
- No free-text, no traces, no provenance chains. The white-box
  event log (driver-side) remains the forensic record; the
  substrate is the production-consulted summary.

---

## 3. Key namespaces

Two namespaces share the substrate. Sharing means: same record
format (section 2), same lookup machinery, same source-tagging
convention, same reclamation policy. It does not mean the same keys.

### 3.1 PURSUIT keys (for the stopping decisions)

- **Inquiry pursuits:** keyed by (s, r). One record per queried
  (subject, relation) pair that has produced at least one miss or
  trial. Rationale: the decline gate asks "should I answer this
  query," and the query is identified by (s, r). (Three stops R1
  notes no keyed lookup by (s, r) for non-FACT nodes currently
  exists; building one is new machinery.)
- **Repair pursuits:** keyed by MAP node id. One record per MAP that
  has undergone at least one revision attempt. Rationale: the
  abandonment gate for repair asks "should this MAP's repair
  campaign continue," keyed by the structure under repair.

### 3.2 STRATEGY keys (for the selection decisions)

- **Trial families:** keyed by family id (0-5 in the current six
  family inventory). One record per family, aggregating outcomes
  across pursuits. This is where H3-lite Node 1's field-32 counter
  migrates (section 6).
- **Repair topologies:** keyed by topology id, when Node 3 exists.
  Reserved; not populated until the repair-topology decision has a
  sound criterion (C5 audit required first).

### 3.3 Why two namespaces, not one

A pursuit record answers "how is this going" (for stopping). A
strategy record answers "which option works" (for selection). They
are different questions over different keys, but they share the
write-path vocabulary (attempt/success/failure with source tags),
the read-path discipline (consulted before the decision), and the
boundedness regime. Unifying them into one key space would force
false commensurability (a family's global track record is not a
pursuit's local history). Keeping them as separate namespaces in one
substrate is the compression: one mechanism, two key types, all
consumers.

---

## 4. Write paths

### 4.1 Record creation

A record is created on the first attempt for its key:

- PURSUIT (s, r): created on the first miss or trial for that
  (s, r). The creating function is whichever production path first
  attempts the pursuit: `miss_inquire` for inquiries (currently
  writes T30 nodes; the substrate record is the keyed counterpart),
  `t2_trial` on trial entry.
- PURSUIT (MAP id): created on the first revision attempt for that
  MAP, in `t2_revise_graph` (currently returns 0 or 1 and discards
  the outcome per D1; the substrate record retains it).
- STRATEGY (family id): created on the first trial in which that
  family is attempted. The six family records exist from the first
  trial onward.

Creation initializes all counters to zero, `state` to ACTIVE,
`last_active` to the current event number. Creation is cheap by
construction: one node-equivalent per record (exact storage mapping
is design detail).

### 4.2 Record update

On every subsequent attempt for an existing key, exactly one of:

- **Success path:** increment `attempts` and `successes`, reset
  `consec_fail` to zero, set `last_mode` to zero, update
  `last_active`, increment the applicable `src_*` counter. The
  writing function is the one that determines success: the trial
  verification path for trials, the revision return path for
  repairs, the query-answer path for inquiries.
- **Failure path:** increment `attempts`, increment `consec_fail`,
  set `last_mode` to the failure mode, add the attempt's node cost
  to `cost_nodes` (saturating), update `last_active`, increment the
  applicable `src_*` counter. The writing function is the one that
  observes the failure: trial exhaustion in `t2_trial`, revision
  0-return in `t2_revise_graph`, miss in the query path.

**The reset-on-success rule is mandatory** (three stops section
2.1). A failure-only substrate makes every gate monotonically more
pessimistic; the system could never recover from a bad streak even
when the world changed. Both halves must be written.

**The source-tag rule is mandatory** (learning machinery C6). The
writing function must classify the attempt's triggering consequence
into taught, observed, or self-generated and increment the matching
counter. When the classification is ambiguous, the conservative
default is `src_self` (treat as self-generated; exclude from
evidence tallies). Rationale: the bootstrap loop proved
self-generated consequences masquerading as observations; the
failure mode of over-tagging as self is underconfidence, while the
failure mode of under-tagging is the confirmed self-referential
loop. Underconfidence is the safer error.

### 4.3 Who writes (function-level attribution)

| Event | Current behavior | Substrate write |
|---|---|---|
| Trial candidate rejected | return value discarded (D1) | failure path, STRATEGY (family), `last_mode`=F1 |
| Trial exhausts all families | hdr+16 incremented, write-only (T3) | failure path, PURSUIT (s, r), `last_mode`=F2; failure path per attempted STRATEGY (family) |
| Trial verifies | MAP promoted | success path, PURSUIT (s, r); success path, STRATEGY (successful family) |
| Revision returns 0 | return discarded (D1) | failure path, PURSUIT (MAP id), `last_mode`=F3 sub-mode |
| Revision succeeds | MAP retargeted | success path, PURSUIT (MAP id) |
| Query miss | T30 node written, never read (T5) | failure path, PURSUIT (s, r), `last_mode`=F6 |
| Query answered | shadow FACT or fact hit | success path, PURSUIT (s, r) |
| Contradiction observed | type-3 edge, revision fired or not | failure path, PURSUIT (affected MAP or (s, r)), `last_mode`=F4 |

The "current behavior" column is the discard inventory from failure
retention (`d3e896c8c`) and the theater audit. Every row is an
existing M1 consequence (consequence re-entry section 1.3: M1 is
present everywhere); the substrate write is the M2 that is
currently missing.

---

## 5. Read paths

Each consumer below must satisfy the read-path-first rule: the read
fires on transcript in normal production operation, and the decision
identifiably changes (or identifiably does not change) because of
what was read. A read path present in source but never exercised is
T5 again.

### 5.1 Decline gate (query path)

**Where:** in the query path, before the trial is attempted for a
pursuit with an existing record. (Exact placement is design detail;
the requirement is that it precedes expensive attempt, so that
declining saves the trial cost.)

**Query:** look up PURSUIT (s, r). Read `consec_fail`,
`src_taught` + `src_observed` successes vs failures (excluding
`src_self`), and `state`.

**Decision rule (minimum):** decline (return a distinguished
WITHHOLD, not -2 pipeline exhaust) when `consec_fail` exceeds a
threshold AND `state` is ACTIVE. The threshold value is
researcher-set scaffolding initially (honest labeling required per
three stops section 2.4); the requirement is that the gate exists,
reads the substrate, and withholds. Learner-owned thresholds are a
further gap (same standard as K-H2-3).

**Trace:** every decline writes a WITHHOLD-class trace naming the
pursuit key, the criterion value read, and the evidence consulted
(three stops section 2.2). The trace is driver-visible for
evaluation; whether it is also a substrate write (a declined attempt
counting as an attempt) is design detail, but the conservative rule
is: declined attempts do NOT increment `attempts` (the pursuit was
not attempted; recording it as an attempt would let the gate's own
caution inflate the failure count it reads).

### 5.2 Abandonment gate (inquiry and repair paths)

**Where:** before re-attempting a pursuit whose record shows prior
failures. For inquiries: in the miss path, before re-firing the
trial on a repeated (s, r) miss. For repairs: in the contradiction
path, before re-firing revision on a MAP whose campaign has failed.

**Query:** look up the PURSUIT record. Read `consec_fail` and
`state`.

**Decision rule (minimum, A1 class):** mark `state` ABANDONED when
`consec_fail` exceeds a (separately scaffolded) bound. An abandoned
pursuit is excluded from re-attempt: the trial does not fire for it,
revision does not re-fire for it. Re-engagement conditions are
recorded at abandonment time (three stops section 2.2: "resume if
new evidence of type E arrives"); the minimal re-engagement is:
any successful observation for the pursuit's key resets `state` to
RE-ENGAGED and `consec_fail` to zero.

**Ordering note:** the abandonment gate reuses the same
`consec_fail` the decline gate reads. Decline is per-query
(reversible, shallow); abandonment is per-pursuit (resumable,
middle). The decline gate's withholds do not increment
`consec_fail` (section 5.1), so the two gates do not
double-count: decline consults the count, abandonment advances the
lifecycle. This is the "one substrate, two gates at different
depths" structure from the dependency graph.

### 5.3 Retention input (eviction path)

**Where:** in the eviction selection logic, when choosing victims
under memory pressure.

**Query:** for each candidate structure, look up the PURSUIT record
of the pursuit that created it (MAPs carry their creating pursuit;
facts carry (s, r)). Read `state` and the per-structure utility
(C7, when it exists).

**Decision rule (minimum):** structures belonging to ABANDONED
pursuits are reclaimed before structures belonging to ACTIVE
pursuits, regardless of bid. This replaces the blind per-node bid
sweep as the primary deletion ordering (three stops section 2.3;
the bid sweep is kept as fallback, not removed).

**Dependency:** this read path additionally requires C7
(per-structure utility) for the full specification, because
pursuit-state alone does not distinguish a useful structure in an
active pursuit from a useless one. The minimal viable set (learning
machinery section 3.3) defers C7: until utility exists, eviction
keeps its current rule and the substrate serves decline,
abandonment, and trial reorder only. The retention read path is
specified here so the substrate's record format already carries
what eviction will need (`state`, and later utility).

### 5.4 Trial reorder (H3-lite Node 1 convergence)

**Where:** in `t2_trial`'s family dispatch, replacing the read of
field 32 on the tag-40 policy node.

**Query:** read all six STRATEGY (family id) records. Compute per
family the success rate over non-self source attempts:
`successes / (attempts - src_self)`, with a minimum-attempts floor
so that untried families are not ranked zero (exact floor is design
detail; the requirement is only that the rule not permanently bury
untried options).

**Decision:** attempt families in descending success-rate order.
This replaces the Hebbian swap-on-success plus demote-after-8
mechanism of the built Node 1 (`45c55ed83`): instead of a private
counter incremented on rejection and a fixed demotion threshold,
the order is derived from the shared substrate's per-family outcome
records.

**What remains of the policy node:** the node itself remains as the
decision point (the cached current order, readable by the driver
for the POLICY event log). What migrates is the evidence: from a
private counter on the node to keyed records in the substrate. The
node's write path becomes "recompute order from substrate" rather
than "increment private counter." This is the convergence the
learning machinery spec requires (section 4.4 item 1): narrow
counters are the prototype, the shared store is the target; do not
build both permanently.

**Why this is better than field 32:** the private counter records
only rejections (failure half, global, unsourced). The substrate
record carries successes and failures, per-pursuit attribution
(which pursuits did this family serve), source tags (excluding
self-generated confirmations), and cost. The reorder decision made
from the substrate is auditable per the C5 guardrails; the reorder
decision made from field 32 is not (success criteria analysis
section 2.2: masked mode learns executability order).

---

## 6. Boundedness and self-reclamation

The scaling analysis (`02804f782`) puts the node-budget wall at
hundreds of events. The learning machinery spec (section 3.4) states
the consequence plainly: "The learning machinery hastens saturation.
Every retained consequence consumes budget." Boundedness is a
feasibility condition, not an optimization.

### 6.1 Per-record cost cap

Each record is fixed width: the fields in section 2, no more. No
event lists, no histories, no variable-length data. The record
count, not the record size, is the quantity under management.

### 6.2 Record reclamation policy

When the substrate reaches its record budget (a fixed cap, researcher
set), the stalest record is reclaimed. "Stalest" is defined solely by
`last_active`: the record with the oldest last-activity event number
goes first. Ties broken by lowest `attempts` (least evidence).

**ABANDONED records are reclaimed before ACTIVE records** at equal
staleness: a pursuit the system has already judged not worth
pursuing is the first evidence to discard. This is the one place the
lifecycle `state` feeds reclamation, and it closes a loop: the
abandonment judgment that the substrate enabled becomes the
substrate's own garbage-collection priority.

### 6.3 The self-reference question

Does the substrate keep records about its own reclamation? No.
Reclamation follows the fixed stalest-first rule; it is not a
cognitive decision and gets no record. This terminates the regress
by construction: the substrate is infrastructure with a fixed
eviction rule, not a pursuit. (If a future design wants adaptive
reclamation, that is a new decision requiring its own C1-C7
treatment; it is not specified here.)

### 6.4 Cost accounting requirement

Any implementation of this substrate must report, per evaluation
run: substrate records created, substrate records reclaimed, and
the substrate's node/field cost as a fraction of total state growth.
The learning machinery spec (section 3.4) requires DYN-1 to bend the
right way; the substrate's overhead must be visible in that
measurement, not hidden. A substrate whose bookkeeping costs exceed
the decisions it informs fails the feasibility condition no matter
how sound its criteria.

---

## 7. Source tagging (C6) in the substrate

Section 2.4 defines the three source counters. This section states
the consumer rules that make the tags load-bearing rather than
decorative.

### 7.1 The bootstrap exclusion

Any consumer that computes a success or failure rate from a
substrate record MUST exclude `src_self` attempts from both the
numerator and the denominator, unless the consumer's preregistered
criterion explicitly includes self-generated consequences with
stated justification. Rationale: the bootstrap-loop probe proved
that self-generated consequences, counted as evidence, produce
100% self-referential confidence state-indistinguishable from
genuine confidence (`ee7815de8`). The default must be exclusion;
inclusion is the marked, justified exception.

### 7.2 Tagging at the write path

The writing function (section 4.3) classifies each attempt. The
classification rules, minimum version:

- The consequence was produced by `ev_teach` (harness teaching) or
  by a driver-supplied observation in a sealed evaluation:
  `src_taught`.
- The consequence was produced by `ev_observe` on a
  non-harness environmental input, or by a contradiction between a
  taught fact and an environmental observation: `src_observed`.
- The consequence was produced by bootstrap inference
  (`bootstrap_miss`), by revision output (`t2_revise_graph`
  writing a corrected fact), or by MAP shadow FACTs answering a
  query: `src_self`.

When the writer cannot determine the source, it tags `src_self`
(section 4.2: underconfidence is the safer error).

### 7.3 Interaction with the teach/observe conflation

The teach/observe analysis (`8744796fb`) proved five sources
collapse into indistinguishable tag-1 FACTs at the fact layer.
The substrate does NOT fix the fact layer; it tags at the
consequence layer (the attempt, not the fact). This is a narrower,
tractable requirement: the attempt's trigger is known at the write
path (the function knows whether it is running bootstrap,
revision, or answering from a taught fact), even though the fact's
provenance is lost downstream. Tagging attempts is feasible now;
retagging facts requires the fact-layer provenance work, which is
separately load-bearing and out of scope here.

---

## 8. What is explicitly NOT specified

- **Field offsets, node tags, header layouts.** Storage mapping is
  TNN-3 design work.
- **Threshold values.** The decline threshold, the abandonment
  bound, the substrate record cap, the minimum-attempts floor for
  strategy ranking: all researcher-set scaffolding initially, all
  honestly labeled as such (three stops section 2.4). Learner-owned
  thresholds are a further gap.
- **The decline criterion's correctness-substitute.** The minimal
  gate uses consecutive failures (binary, sound inputs). Graded
  failure (G4) needs the verification machinery that does not exist
  (`c2a48bee6`).
- **C7 per-structure utility.** Specified as a dependency of the
  retention read path (section 5.3) but deferred from the minimal
  viable set. Its record format is not specified here.
- **Re-engagement beyond the minimal rule.** Section 5.2 gives the
  minimal re-engagement (successful observation resets). Richer
  re-engagement conditions (new strategy available, N events pass)
  are downstream.
- **Cross-pursuit generalization.** Whether failure on (s1, r)
  should inform the gate for (s2, r) is not specified. The minimal
  substrate is per-key; similarity-weighted generalization is the
  learned-similarity frontier (`e8889bb17`), five capabilities deep.
- **Second-order learning.** Whether the gates' own thresholds
  should adapt based on gate outcomes (did declining avoid failure?)
  is downstream. The minimum is first-order: experience changes the
  records, the records change the gate behavior.

---

## 9. Evaluation: what would show the substrate working

The substrate is infrastructure; it is evaluated through its
consumers, per the read-path-first rule:

1. **Decline gate test:** pursuits with high `consec_fail` are
   withheld; withheld pursuits would have failed if attempted
   (counterfactual checked on a held-out sample where the gate is
   disabled). WITHHOLD traces name the evidence consulted.
2. **Abandonment test:** pursuits marked ABANDONED stop consuming
   trial/revision resources; a control without the gate shows
   continued re-attempt (the current behavior: failed inquiries
   accrete, `ae76a60a7`).
3. **Trial reorder test:** the weak K-LT-5 discrimination (R ratio)
   run against the substrate-backed reorder rather than the
   field-32 mechanism. Same prereg, same bar (R > 1.15); the
   comparison is mechanism-vs-mechanism on identical worlds.
4. **Falsifiability S2** (learning machinery section 5): if three
   narrow per-decision counters prove sufficient for decline,
   abandonment, and forgetting with no composition problems and no
   counter proliferation as decisions are added, the
   shared-substrate requirement is overstated. The substrate must
   earn its keep against this alternative; it is not assumed.
5. **Cost test:** substrate overhead visible in DYN-1 and bounded
   per section 6.4. A substrate that works cognitively but breaks
   the budget fails feasibility.

What would NOT show it working: records written but never read
(theater); gates reading but never changing behavior (the
counterfactual test fails); R ratio improving because the world got
easier (difficulty control).

---

## 10. Relation to H3-lite Nodes 2 and 3

- **Node 2 (guide default):** the reachability probe (`b0ad6c5d3`,
  UNREACHABLE) proved the frozen Node 2 write path cannot fire.
  The substrate does not repair Node 2. If a future Node 2
  amendment specifies a reachable action source, its resolution
  outcomes would be recorded as STRATEGY records (keyed by guide
  action) in the substrate rather than in a private counter. Until
  then, Node 2 has no substrate records.
- **Node 3 (repair topology):** the success criteria analysis
  proved its criterion is the confirmed-broken V2 (wrong-but-running
  repairs count as success). Recording V2-corrupt outcomes in the
  substrate would produce confident maladaptation (learning
  machinery C5). Node 3 gets STRATEGY records only after its
  criterion is fixed (`out == new_o` minimum). The substrate is
  ready for it; the criterion is not.

---

## 11. Standing architectural metric (this specification)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 added (specification
  only; the substrate is requirements, not code).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0 (C5 criteria are referenced, none
  built here).
- REUSE EVENTS: 0.
- REVISION EVENTS: 0.
- COGNITION LINES: 0.
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

Components specified: 1 substrate, 2 key namespaces, 4 read paths
(decline, abandonment, retention input, trial reorder), 1
convergence (Node 1 field-32 migration), 1 reclamation policy,
3 source-tag consumer rules. Write-path table: 8 rows mapping
existing discards to substrate writes. Explicit non-specifications:
8 items (section 8). Evaluation tests: 5 (section 9).

---

**Verdict: SHARED-SUBSTRATE-COMPLETE.**
