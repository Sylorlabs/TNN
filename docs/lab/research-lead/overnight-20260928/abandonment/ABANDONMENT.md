# Abandonment Analysis

**Status:** ANALYSIS ONLY. DRAFT-NOT-FROZEN. No implementation designed or proposed.
**Date:** 2026-10-01
**Frozen source:** `tnn2_build/tnn2.zag` (1591 lines), read-only. Never modified.
**Verdict:** ABANDONMENT-COMPLETE

---

## 0. Thesis

TNN-2 has no "stop" decisions anywhere. It cannot stop answering (no decline
capability, per `9e0ae81d1`), cannot stop pursuing (no abandonment, this
analysis), and cannot stop retaining (no forgetting, only eviction, per
`2726baf74`). Every "stop" in the system is an accident (pipeline exhaust,
budget pressure) rather than a decision. Abandonment, the middle "stop"
(stop trying), is the decision layer whose absence makes the other two gaps
unfillable: principled forgetting needs to know what has been abandoned, and
goal lifecycles need abandonment as their termination condition.

---

## 1. Current non-abandonment (white-box characterization)

### 1.1 Failed inquiry: accumulate, never abandon

Trace of a miss through frozen source:

1. `ev_query` (line 813): activate fails, trial returns -2, bootstrap
   returns -2.
2. Line 832-834: `log_ev` records failure, `miss_inquire(W,s,r)` is called,
   -2 returned.
3. `miss_inquire` (line 795): unconditionally allocates a fresh T30
   UNCERTAINTY node (`ns(W,u,0,30)`), then a guide node linked to
   POLICY_ROOT. No check for an existing uncertainty on the same (s, r).
4. Nothing further happens. Per the ignorance-dedup analysis (`8510e327b`),
   the T30 node has no production read path: `ev_act` never consults
   uncertainty keys, `bid` does not count type-1 links to uncertainty nodes,
   no `resolve_uncertainty` exists. Ablating all T30 nodes changes zero
   production behavior.

On the next identical harness query, the identical path fires again: another
miss, another T30 node, another guide. There is no deduplication, no
escalation ("this has failed before, try differently"), no satisfaction
check ("was this resolved?"), and no abandonment ("stop recording this").
The state-dynamics finding (duplicate UNCERTAINTY nodes for already-known
keys, constant +14/+6 per-miss cost across 260 experiences) is the empirical
signature.

The inquiry does not "retry forever" in the active sense, because nothing
self-initiates (goal origination `3bf4d7bb4`, section 1.1: zero internal
callers on all four handlers). It is worse than retrying: each harness-poked
repetition writes another inert record. The pursuit neither advances nor
terminates. It accretes.

### 1.2 Unrepairable contradiction: stale MAP persists, same repair re-fires

Trace of a contradiction through frozen source:

1. `ev_observe` (line 836): `activate` finds the fact, stored value differs
   from observation.
2. Line 843: type-3 self edge added to the fact (lowers its bid; the
   researcher-authored "contradicted facts are cheaper to keep" criterion).
3. Line 844: `revise_on_contradict(W,n,o)` fires. For every live MAP with
   a type-1 provenance edge to the contradicted fact, `t2_revise_graph` is
   called (whole-MAP broadcast, no ranking; blame analysis `0917f3e25`).
4. `t2_revise_graph` (line 706): finds the stale SETREG cell via provenance,
   tombstones it, inserts a corrected step, rewires, re-executes. On any
   failure (no stale cell found, no guard found, literal allocation failed,
   re-execution returns -999999), the graph is reverted in place and **0 is
   returned**. The return value is discarded by `revise_on_contradict`
   (line 699: bare call, no check).
5. Regardless of revision outcome, line 851: the contradicting observation
   is taught as a new fact via `ev_teach_in(W,s,r,o)`.

Consequences of an unrepairable contradiction:

- The MAP keeps its stale answer. Its root, its field-28 answer, and its
  (now possibly evicted) graph cells are untouched by the failed repair.
- A second fact for the same (s, r) now exists with the new value. The old
  fact carries a type-3 self edge (lower bid); the new fact carries a fresh
  PRO edge. The next query's `activate` picks by max bid, so the new fact
  usually wins. The stale MAP is bypassed, not repaired, not retired, not
  abandoned. It persists as a candidate fossil.
- No record of the revision failure is kept. The 0 return is discarded. No
  failure counter increments (trial stats are write-only, theater T3; no
  revision-attempt counter exists anywhere in the 1591 lines).
- On the next contradiction for the same (s, r), `revise_on_contradict`
  re-fires the identical blame walk and the identical single-schema repair.
  Per the blame analysis: "the system cannot learn its blame is
  systematically wrong." There is no "this repair strategy has failed N
  times" state, so there is no basis for trying differently or for stopping.

The unrepairable hypothesis is therefore never abandoned. It is shelved by
bid arithmetic (accident) while remaining fully eligible for future
re-repair attempts (no memory of failure). Pursuit continues without
progress and without termination.

### 1.3 The supersede path: the closest thing to abandonment, and it is not one

`is_superseded` (line 132) checks for a type-3 self edge on a node. The
revision substrate work (`880c87c4c`) uses supersede edges to skip failed
revision candidates. `ev_act` skips superseded guides.

Superseding is exclusion from selection, not abandonment of pursuit:

- A superseded MAP still occupies its node, its edges, and its budget. It
  is skipped by lookup, not reclaimed or retired.
- Nothing records *why* it was superseded, *when*, or *whether the
  superseding structure actually succeeded*. The supersede edge is a flag
  without a reason.
- Nothing ever un-supersedes. There is no "the replacement failed too, go
  back" path and no "enough time has passed, reconsider" path.
- Most importantly: superseding is applied to structures, not to pursuits.
  There is no representation of "I am trying to resolve X" that could be
  marked abandoned. The unit of supersede is the node; the unit of
  abandonment would be the goal.

### 1.4 Exhaustive grep: no give-up machinery exists

Search of the cognition region (lines 1-918) for attempt counters, retry
limits, give-up conditions, or abandonment logic: zero hits (the single
"give" match is a test-code comment at line 1204, "give it positive bid via
self-loop"). Specifically absent:

- No counter of revision attempts per MAP.
- No counter of inquiry attempts per (s, r).
- No counter of trial failures per query shape.
- No threshold on any of the above (nothing to count with).
- No "mark as unresolvable" state distinct from supersede.
- No re-engagement condition ("revisit if new evidence arrives").

The system has exactly two terminal states for a pursuit: success (an
answer is produced or a repair verifies) and indefinite silent persistence
(the records accumulate, the stale structures linger, the same failed
repair re-fires on each new trigger). There is no third state.

---

## 2. The abandonment problem

### 2.1 Definitions: abandonment vs forgetting vs declining

Three distinct "stop" functions. TNN-2 has none of them as decisions.

| | Declining | Abandonment | Forgetting |
|---|---|---|---|
| **Operates on** | A query (output) | A pursuit (effort) | A structure (storage) |
| **Decision** | "I will not answer this now" | "I will no longer try to resolve this" | "This is gone" |
| **Reversibility** | Per-query; next query re-decides | Resumable on new evidence or capability | Expensive or impossible |
| **What is kept** | The query, the candidate, the reason | The records, the failure history | Nothing (or a tombstone) |
| **TNN-2 status** | Absent (`9e0ae81d1`); -2 is exhaust | Absent (this analysis) | Absent (`2726baf74`); eviction is accident |

Distinctions that matter:

- **Decline vs abandon.** Decline is about output: withhold an answer to
  this query. Abandonment is about pursuit: stop spending effort on this
  inquiry, this repair strategy, this goal. You decline a query; you
  abandon an investigation. A declined query may be retried next tick with
  no prejudice; an abandoned pursuit requires a re-engagement reason to
  restart. The decline analysis's G3 (UNCERTAINTY write-only) blocks both:
  you cannot decline on the basis of recorded ignorance you never read,
  and you cannot abandon a pursuit you never represented.
- **Abandon vs forget.** Abandonment stops effort; forgetting removes
  storage. You can abandon without forgetting (keep the failure records;
  they are evidence about what does not work). You can forget without
  abandoning (eviction deletes structures whose pursuits are still active;
  this is how fossils and amputated MAPs are manufactured). Principled
  forgetting presupposes abandonment judgments: the retention system needs
  to know which pursuits are live (protect their structures) and which are
  abandoned (their structures are deletion candidates).
- **"I don't know yet" vs "I'll never know this way."** Decline says the
  first: provisional, evidence-reversible, no judgment on the approach.
  Abandonment says the second: a judgment that the current approach will
  not succeed, based on failure history. The difference is the criterion:
  decline needs an epistemic threshold ("confidence too low"); abandonment
  needs a pursuit-level judgment ("N failures, no progress, approach
  exhausted"). TNN-2 has neither threshold, and it has no failure history
  to judge from.

### 2.2 When SHOULD a learner abandon? (Candidate criteria, analytical)

Five candidate abandonment criteria, in increasing demand on machinery.
Stated as what a principled decider would need, not as a design.

- **A1. Repeated failure.** The same pursuit has failed N times. Requires:
  a pursuit record, a failure counter, a threshold. TNN-2 has none of the
  three. (The trial-stats header field is write-only, theater T3.)
- **A2. No progress.** Failures are not merely repeated; they are
  non-improving. Each attempt costs as much as the last and gets no
  closer. Requires: a progress measure (distance to goal, partial credit),
  which presupposes a goal representation with a satisfaction gradient
  (goal origination R1, R6). TNN-2's outcomes are binary (answer or -2,
  repair verifies or reverts); there is no "closer."
- **A3. Premise undermined.** The pursuit's licensing assumptions are
  contradicted. Requires: premise tracking (which facts license this
  pursuit) and a check of premise liveness. TNN-2 has provenance edges
  (type-1 DEP) but nothing checks whether a pursuit's premises are still
  alive before re-firing it. The stale-MAP re-repair loop (section 1.2)
  is the instance: the repair re-fires against premises that may have
  been evicted.
- **A4. Approach exhaustion.** All available strategies for this pursuit
  have been tried. Requires: a strategy inventory and per-strategy
  outcome records. TNN-2 has exactly one repair operator (single-schema,
  researcher-authored); exhaustion is immediate but unrecognized. With
  one strategy, "exhaustion" and "first failure" coincide, which is why
  the current system cannot distinguish "try harder" from "give up."
- **A5. Opportunity cost.** Other pursuits have higher expected value for
  the next unit of effort. Requires: a goal scheduler (goal origination
  R4), value estimates per pursuit, and a comparison. This is the
  full cognitive form of abandonment and presupposes nearly everything
  else in this analysis.

A1 is the minimal viable abandonment criterion. A5 is the asymptote. The
honest note: A1 alone, with a source-fixed N, would be a researcher
decision (another constant like the 12-event protection window), not a
learner-owned judgment. Learner-owned abandonment needs the threshold
itself to satisfy the K-H3 six-element standard (read path, exercised
write path, prediction-error update), exactly as the decline analysis
requires for its gate (G2).

### 2.3 What abandonment would change (descriptive, not prescriptive)

For the record, the jointly necessary elements of principled abandonment.
Not a work order; no implementation undertaken.

1. **Pursuit records.** A persistent structure representing "trying to X"
   with attempt history, distinct from the uncertainty record (which
   records ignorance, not effort). The T30 node is the write half of this;
   it lacks attempt counts, strategy tags, and outcome history.
2. **Failure accounting.** Which attempts failed, how, at what cost. The
   discarded 0-return of `t2_revise_graph` is the information currently
   thrown away.
3. **An abandonment criterion** satisfying the learner-internal standard:
   read path on the pursuit path, exercised write path from experience,
   update on prediction error, ablation flips the stop/continue decision.
4. **An abandonment action** with defined semantics: stop creating
   duplicate records for this pursuit; exclude its structures from
   re-repair eligibility; optionally schedule re-engagement conditions.
   Distinct from supersede (which excludes structures from selection but
   says nothing about the pursuit) and from eviction (which reclaims
   storage without consulting pursuit state).
5. **Re-engagement conditions.** "Resume if: new evidence of type E
   arrives; a new repair strategy becomes available; N events pass without
   the contradiction recurring." Without this, abandonment is
   indistinguishable from permanent deletion, and the system loses the
   ability to be wrong about giving up.

Items 1-5 are jointly necessary. Any subset is theater by the K-H3 audit
standard: pursuit records no decision reads are logging (the T30 failure
mode); a criterion with a source-fixed threshold is a researcher decision;
an abandonment action with no re-engagement path is just deletion with
extra steps.

---

## 3. Gap analysis

### 3.1 What is missing (ranked by dependency)

- **P1. Pursuit representation.** No structure represents an ongoing
  effort. (Goal origination R1 covers goals; pursuits are the
  finer-grained unit: a single inquiry thread, a single repair campaign.)
- **P2. Failure memory.** Attempt outcomes are discarded (the 0-return)
  or never recorded (no per-pursuit counters). Without P2, criterion A1
  cannot even be stated.
- **P3. Progress measure.** Binary outcomes only. Without P3, criterion
  A2 cannot be stated, and A1 cannot distinguish "failing" from
  "failing usefully."
- **P4. Abandonment criterion.** No threshold, no gate, no decision
  point. The same absence as the decline gate (G1/G2 in `9e0ae81d1`),
  applied to pursuits rather than queries.
- **P5. Abandonment action semantics.** What "stop" does to state:
  record freezing, re-repair exclusion, re-engagement scheduling.
- **P6. Scheduler integration.** Abandonment frees effort; something must
  reallocate it (goal origination R4). Otherwise abandonment merely
  converts active waste into passive waste.

### 3.2 The one-bit version (what the data already supports)

The cheapest true statement this analysis can make: TNN-2 already
generates the raw material for P2 (failure events occur: trial
exhaustions, revision 0-returns, bootstrap disagreements) and discards
all of it. The gap between "no abandonment" and "A1-class abandonment"
is not missing experience; it is missing retention of experience about
failure. The system experiences failure constantly and remembers none
of it. This is the same write-mostly disease the state-dynamics analysis
(`ee238d8d4`) diagnosed: the learner writes records of its ignorance and
its evictions and its trial statistics, and no decision reads any of
them.

---

## 4. Relation to the three source analyses

Is abandonment the missing piece that connects them? Yes, as the
decision layer between pursuit and storage.

**Goal origination (`3bf4d7bb4`).** R6 names the goal lifecycle:
satisfaction detection and abandonment. Without abandonment, any future
goal system inherits TNN-2's accumulation disease at the goal level:
goals would be created (R3), never satisfied-detected or
abandoned (R6), and pile up like T30 nodes. Abandonment is the
termination half of R6, and it is the harder half: satisfaction is
recognizing success, abandonment is judging failure, and judging failure
requires the failure memory (P2) that does not exist. The goal analysis's
option (c), opportunistic pursuit, makes abandonment more urgent, not
less: if the learner diverts harness-given computation toward its own
goals, it needs a stop rule for the diversion, or every goal becomes a
permanent tax on every handler call.

**Decline signal (`9e0ae81d1`).** Decline and abandonment share the
criterion machinery (a learner-internal threshold with read and write
paths) but differ in unit and reversibility. The decline gate asks "answer
or withhold this query"; the abandonment gate asks "continue or stop this
pursuit." Two interactions: (i) repeated declines on the same (s, r)
should feed the abandonment criterion (A1 counts declines as failures);
(ii) an abandoned pursuit should change decline behavior (a query about
an abandoned inquiry is not "unknown," it is "investigated and closed,"
which is a different epistemic state than -2-as-exhaust). Currently both
collapse to -2. The decline analysis's G5 (sentinel overloading) is thus
partly an abandonment gap: the output vocabulary cannot express "I
stopped trying" because the system never stops trying.

**Forgetting (`2726baf74`).** Abandonment is the cognitive precursor to
forgetting. The forgetting analysis's R2 (utility-grounded deletion)
needs abandonment judgments as input: a structure whose pursuit is
abandoned is a deletion candidate; a structure whose pursuit is live
should be protected regardless of its bid. Currently eviction consults
neither, so it deletes live pursuits' structures (amputated MAPs) and
retains abandoned pursuits' shells (fossils). The fossil is what an
un-abandoned, un-forgotten, un-executable pursuit looks like from the
storage side: effort stopped (the graph was evicted), but no decision
ever marked the pursuit closed, so the header lingers at bid 2,
unrevisable and unreclaimed. Fossilization is abandonment-shaped: it is
what happens when stopping occurs by accident (eviction) instead of by
decision. A system with principled abandonment would still have storage
pressure, but its fossils would be decisions ("I stopped pursuing this;
reclaim it last") rather than accidents.

**The unifying frame.** The three analyses each found a missing "stop":
decline (stop answering), abandonment (stop trying), forgetting (stop
keeping). They are ordered by reversibility and by architectural depth:

```
query (reversible, per-event)  ->  DECLINE      (shallowest)
pursuit (resumable, cross-event) -> ABANDONMENT  (middle)
storage (irreversible, structural) -> FORGETTING (deepest)
```

Each deeper stop presupposes the shallower judgments: forgetting needs to
know what is abandoned; abandonment needs decline histories as failure
data; decline needs nothing from the deeper two but supplies data upward.
TNN-2 is missing all three, and the missing middle is load-bearing: you
cannot build principled forgetting on top of un-abandoned pursuits, and
you cannot close goal lifecycles without it. The "stop" column of the
architecture is empty at every level, and the emptiness is structural
(no decision points, no failure memory, no criteria), not a matter of
tuning constants.

---

## 5. Standing architectural metric (this analysis)

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 0 (analysis only) |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 |
| SOURCE-ENUMERABLE FORMS | n/a (analysis) |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 |
| REUSE EVENTS | 0 |
| REVISION EVENTS | 0 |
| ABANDON EVENTS | 0 (no abandonment decision exists) |
| COGNITION LINES | 0 added |
| MODES | 0 |
| BRIDGES | 0 |
| HANDLERS | 0 |
| SEMANTIC CASES | 0 |

## 6. Explicit non-claims

- This analysis does not design an abandonment mechanism and does not
  claim abandonment is sufficient for any L3, SUF, or C0 bar.
- It does not claim the A1-A5 criteria are the right ones; they are
  candidate criteria stated for analytical completeness.
- It does not predict that adding abandonment would improve any frozen
  battery score. Abandonment is infrastructure for the lifetime
  evaluation (bounded waste, directed effort), not a capability gain on
  the current bars.
- The "one-bit version" (section 3.2) is an observation about information
  already generated and discarded, not a proposal.
- DRAFT-NOT-FROZEN.

---

**Verdict: ABANDONMENT-COMPLETE.**
