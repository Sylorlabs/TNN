# The Three Stops: Unified Architecture Synthesis

**Status:** SYNTHESIS ONLY. No implementation designed or proposed. DRAFT-NOT-FROZEN.
**Date:** 2026-10-01
**Verdict:** THREE-STOPS-COMPLETE

Synthesizes four completed analyses:
- Decline signal (`9e0ae81d1`): no "should I answer?" gate; -2 is pipeline exhaust.
- Abandonment (`ae76a60a7`): zero attempt counters; decline -> abandonment -> forgetting ordered by reversibility.
- Forgetting (`2726baf74`): 8 researcher-fixed retention decisions; fossils are the anti-retirement.
- Failure retention (`d3e896c8c`): 7 failure signals, 5 discard mechanisms; retention is upstream of all three stops.

---

## 0. The single underlying incapacity

"Cannot stop" is the symptom. The incapacity is more specific:

**TNN-2 has no machinery by which the consequences of its own activity re-enter its future decisions.**

Trace any activity through frozen cognition and the pattern is uniform: information flows forward (teach, query, trial, miss, write) and never flows back. The system generates failure experience constantly (trial exhaustions, revision 0-returns, bootstrap disagreements, activation misses) and discards all of it at five discard points (D1-D5: return-value discard, reason collapse, write-only instrumentation, no counters, silent propagation). It writes records of its ignorance (T30), its trial statistics (hdr+16), its evictions (rec_evict), and its events (log_ev); no production decision reads any of them. This is the write-mostly disease diagnosed in state dynamics (`ee238d8d4`), now located precisely: the disease is not that nothing is written, but that writing is never connected to deciding.

Stopping is the canonical case of consequence-driven behavior: you stop doing X *because* doing X has repeatedly failed, *because* the pursuit shows no progress, *because* the structure serves no live purpose. Every "because" in those sentences requires retained experience consulted at a decision point. TNN-2 lacks the retention, the consultation, and the decision points. So it cannot stop -- not as a policy choice, but as a structural incapacity. There is nowhere in the architecture for a stop decision to live.

This is why the four analyses are facets of one problem rather than four problems. They each found the same absence at a different depth: the absence of a feedback path from outcome to decision.

---

## 1. Dependency graph

```
                        FAILURE RETENTION (G1-G5)
                        [per-pursuit counters, failure memory]
                                   |
                    +--------------+--------------+
                    |              |              |
              DECLINE GATE   ABANDONMENT GATE   EVICTION INPUT
           (stop answering)  (stop trying)    (abandoned-pursuit list)
           per-query          per-pursuit       per-structure
           reversible         resumable         irreversible
                    |              |              |
                    +------>-------+<-------------+
                    |   ABANDONMENT JUDGMENTS     |
                    |   (what is closed)          |
                    +--------------+--------------+
                                   |
                         PRINCIPLED FORGETTING
                    (R1-R6: retention priorities,
                     retirement, compression, revisability)
```

Reading the graph:

- **Failure retention is the shared base.** All three stops consume failure experience. Decline needs failure history as gate input (U3: "this pursuit keeps failing; withhold"). Abandonment needs the consecutive-failure count as the A1 criterion input. Forgetting needs the abandoned-pursuit list as its safe-reclaim set (U5). Without retention, none of the three stops can be stated; the abandonment analysis's one-bit version holds: the gap is retention, not experience.
- **The stops are ordered by reversibility and by depth** (abandonment section 4): decline (per-query, shallowest) -> abandonment (per-pursuit, middle) -> forgetting (per-structure, deepest). Each deeper stop presupposes the shallower judgments: forgetting needs to know what is abandoned; abandonment needs decline histories as failure data. The missing middle is load-bearing.
- **Verification is an upstream neighbor, not a stop.** Graded failure (G4) and the decline criterion both require a correctness-substitute computation that does not exist (verification criterion `c2a48bee6`). The stopping subsystem can be built with binary failure signals first; grading is a later refinement. But any claim that the system "knows it is failing usefully" (A2, no-progress) depends on verification machinery outside this synthesis.

What the graph rules out: building principled forgetting without abandonment judgments (the current eviction does exactly this and manufactures fossils); building abandonment without failure retention (A1 cannot be stated without a count); building decline without a criterion read path (a gate with a source-fixed threshold is a researcher decision, not a cognitive choice).

---

## 2. The unified stopping subsystem

One substrate, three gates. The analyses converge on a single shared retention layer with three consumers at three depths.

### 2.1 Inputs

- **Failure signals F1-F7** (failure retention section 1): trial candidate rejection, trial exhaustion, revision failure (five modes), bootstrap disagreement (two modes), resource exhaustion, activation miss, event-log failure marks. These already fire; the subsystem's first job is to stop discarding them.
- **Pursuit state**: which (s, r) inquiry, which MAP repair campaign, which goal thread is currently active. Requires the pursuit representation (abandonment P1) that does not exist.
- **Resource pressure**: budget fullness, eviction rate, allocation failures (F5). The deepest stop (forgetting) is the one that answers pressure; the shallower stops reduce the pressure that forgetting must absorb.
- **Success signals**: the reset half of every counter. Retention of failure without retention of success produces a system that only ever becomes more pessimistic; the write path must reset on success (failure retention 4.1).

### 2.2 Outputs

- **Decline decisions**: per-query withhold/do-not-withhold, with the withheld candidate, the criterion value, and the evidence consulted recorded in a WITHHOLD-class trace (decline section 4c). Distinguishable in white-box state from both "answered" and "missed by exhaust."
- **Abandonment judgments**: per-pursuit continue/stop with re-engagement conditions (abandonment 2.3 item 5: "resume if new evidence of type E arrives; a new repair strategy becomes available; N events pass"). Without re-engagement, abandonment is deletion with extra steps.
- **Eviction priorities**: the abandoned-pursuit list as the safe-reclaim set; live pursuits' structures protected regardless of bid. This is the input that converts eviction from blind per-node sweep into pursuit-aware reclamation (forgetting R6, U5).

### 2.3 State maintained

- **Per-pursuit failure counter**: consecutive failures, incremented on F1-F6 for that pursuit's key, reset on success. Keyed by (s, r) for inquiries or MAP id for repair campaigns. This is failure retention G1, the minimal substrate.
- **Last failure mode**: which of F1-F7 (and which sub-mode) the pursuit last hit. Enables U2 (repeat-avoidance) and U4 (repair triage) later; not required for A1.
- **Pursuit lifecycle state**: active / abandoned / re-engaged, with the abandonment timestamp and the re-engagement conditions. This is abandonment item 4-5.
- **Abandoned-pursuit list**: the set eviction consults. Replaces the current blind bid sweep as the primary deletion ordering (kept as fallback, not removed).

Explicitly NOT maintained at the minimal stage: full temporal histories (G3), graded failure (G4), learner-derived failure categories (G5). Those are extensions with their own treadmill risks (section 3).

### 2.4 The theater guard

Every element above must satisfy the read-path-first rule (failure retention 4.3, abandonment 2.3, decline section 7): a record no production decision consults is T3/T4/T5 again. The subsystem's unit of progress is not "a place where failures are recorded" but "a record that a production decision consults." Concretely:

- A per-pursuit counter with no read path on the retry decision is trial-stats theater (T3).
- An abandonment judgment with no effect on re-repair eligibility is supersede theater (a flag without consequence).
- A WITHHOLD trace with no consumer is event-log theater (T4).
- A source-fixed abandonment threshold N is a researcher decision (abandonment A1 honest note), not learner-owned stopping. The threshold itself must satisfy the K-H3 six-element standard to count as cognitive.

---

## 3. Implementation order (ranked)

### Must come first

**R0. Failure retention G1: per-pursuit failure counters.** Generic (any pursuit, any failure), one counter and one mode per pursuit, production read path before re-attempt. Treadmill risk LOW if generic. This is upstream of everything: A1 cannot be stated without a count, decline has no gate input without history, forgetting has no safe-reclaim set without the abandoned list. The failure retention analysis ranks it least-hard; this synthesis ranks it first-required.

**R1. Pursuit representation (abandonment P1).** The counter needs a key. For TNN-2's query-driven architecture the natural keys are (s, r) for inquiries and MAP id for repair campaigns. No keyed lookup by (s, r) for non-FACT nodes currently exists; building one is new machinery (a small index or scan convention), and it must survive eviction without corrupting (the eviction-corruption hazard: integer field references are invisible to the evictor, `986c52fdc`).

**R2. Decline gate.** Decision point in the query path no later than Stage 1 return, consulting failure history and a criterion. The criterion with a source-fixed threshold is a researcher decision; learner-owned thresholds are the further gap (same standard as K-H2-3). The gate must produce the WITHHOLD-class trace.

### Then

**R3. Abandonment gate (A1 class).** Continue/stop per pursuit on consecutive-failure count, with abandonment action semantics (freeze records, exclude from re-repair eligibility) and re-engagement conditions. A1 first; A2 (no progress) needs the progress measure P3 which needs goal representation with a satisfaction gradient; A3 (premise undermined) needs premise-liveness checks; A4 (approach exhaustion) needs a strategy inventory; A5 (opportunity cost) needs a scheduler. A2-A5 are ordered by their own prerequisites, not by importance.

**R4. Forgetting on abandonment judgments.** Eviction consults the abandoned-pursuit list; live pursuits' structures protected regardless of bid (forgetting R1, R2, R6). Retirement as a third state (R4): excluded from lookup, recoverable at bounded cost. Compression of identified redundancy (R3): trial garbage to zero, MAP/FACT duplication, degenerate P-INV MAPs. Revisable forgetting (R5): the rec_evict records become the re-learning accelerant.

### Can be deferred

- **Failure-mode vocabulary (G2).** Needed for repeat-avoidance (U2) and repair triage (U4), not for abandonment itself. Treadmill risk HIGH: a researcher-enumerated failure taxonomy is one step from a researcher-enumerated repair dispatch. Build G1 first; treat any fixed vocabulary as provisional scaffolding with an explicit retirement condition.
- **Temporal history (G3).** Needed for A2 (is it getting worse). Blocked on the absence of a temporal index and the 1024-node budget; compression of history is itself a cognitive decision.
- **Graded failure (G4).** Downstream of the verification gap: no correctness-substitute, no grading. Binary failure supports all three stops at minimal form.
- **Learner-owned failure categories (G5).** L3 asymptote; the representational-invention frontier reflected in the failure domain. Not a near-term target.

### Treadmill risks at each step

- R0: LOW if the counter is generic. Rises to MEDIUM if per-failure-type counters proliferate into a taxonomy (that is G2 wearing a G1 costume).
- R1: LOW. A keyed index is infrastructure, not a cognitive claim. Risk is corruption (eviction hazard), not treadmill.
- R2: MEDIUM. A gate with a source-fixed threshold is a researcher decision that looks like a cognitive one. The honest version names the threshold as scaffolding.
- R3: MEDIUM at A1, HIGH at A2-A5. Each higher criterion presupposes machinery (progress measure, premise tracking, strategy inventory, scheduler) that is itself a research program. The temptation is to simulate the higher criteria with researcher heuristics; each such simulation is a treadmill step.
- R4: MEDIUM. Retirement and compression are the most likely places for "one more node type" to become a subsystem. The One-System Rule applies: retirement must be a state of the unified node, not a second storage system.

---

## 4. Relation to H3-lite

H3-lite (frozen prereg `9084a7760`) moves three researcher-fixed decision criteria into learner-writable policy nodes: trial search order (Node 1), inquiry guide defaults (Node 2), repair topology dispatch (Node 3). Each has a production read path and one production write path from experience. The procedures stay researcher-authored; the locus of control moves.

**Does H3-lite touch the stopping problem? Largely no. The three nodes are:**

- Node 1 (trial order): revises *which family to try first*. It does not decide *whether to try at all*, *when to stop trying*, or *whether to answer*. A counts-first order that still exhausts all families on every miss is revisability without stopping.
- Node 2 (guide template): revises *what the guide says*. It does not decide *whether to inquire*, *when the inquiry is satisfied*, or *when to abandon it*. The known limit is stated in the prereg: "a revisable constant action is still a constant action until experience changes it."
- Node 3 (repair dispatcher): revises *which repair topology to attempt*. It does not decide *whether to repair*, *when the repair campaign has failed*, or *when to stop re-firing*. The discarded 0-return (D1) remains discarded under every topology.

**Partial overlaps (real but narrow):**

- Node 1's field 32 (first-choice rejection count; demote after 8) is a per-*family* failure counter with a write path. This is a narrow, family-level instance of the failure-accounting pattern (G1), keyed by assembler family rather than by pursuit, driving reordering rather than stopping. It is the closest thing in H3-lite to the stopping substrate, and it demonstrates the pattern without supplying the stop.
- Node 2's `resolve_uncertainty` (supersede on observation match, increment resolution count) is a satisfaction-detection write path. Satisfaction is the success half of the pursuit lifecycle; abandonment is the failure half. Node 2 builds the easier half.

**Composition, not dependence, in both directions:**

- H3-lite does not need the stopping subsystem. Its discrimination tests (order flips to counts-first; template default shifts; topology dispatch changes) are about revisability of choices, and all three are testable without any stop decision existing.
- The stopping subsystem does not need H3-lite. It needs failure retention (R0), pursuit keys (R1), and gates (R2/R3) -- all new machinery, none of which is a policy node over an existing constant. A stop gate is a new decision point, not a parameterized old one.
- They compose cleanly: H3-lite's Node 1 rejection counter is a prototype of per-family failure accounting that a full retention system would generalize to per-pursuit; the stopping subsystem's abandonment judgments would give H3-lite's Node 3 a "stop re-firing" input its dispatcher currently lacks. If both existed, each would be more useful. Neither is a prerequisite for the other.

**What H3-lite cannot tell us about stopping:** the prereg's diagnostic question is "does moving criteria into learner state produce causal improvement in revisability." A positive result would show that criteria ownership matters for *choice* revisability. It would not show that criteria ownership suffices for *stopping*, because stopping requires the retention substrate (R0/R1) that H3-lite does not build. The honest reading of an H3-lite PASS: the disease is partly criteria ownership; the stopping column remains empty.

---

## 5. What the synthesis adds beyond the four analyses

1. **The incapacity stated once**: no feedback path from outcome to decision (section 0). The four analyses each located it at their depth; it is one absence, not four.
2. **The dependency graph** (section 1): failure retention at the base, three gates at three depths, verification as an upstream neighbor. This rules out specific build orders (forgetting before abandonment; abandonment before retention).
3. **One substrate, three gates** (section 2): the analyses each specified their stop's requirements; the synthesis shows they share one retention layer and differ only in key (query/pursuit/structure) and reversibility.
4. **The ranked order with treadmill annotations** (section 3): R0 first-required (not merely least-hard), A2-A5 ordered by prerequisite, G2/G3/G4/G5 explicitly deferred with the risk of each named.
5. **The H3-lite composition result** (section 4): orthogonal with narrow overlaps; neither is a prerequisite; an H3-lite PASS would not fill the stopping column.

## 6. Explicit non-claims

- This synthesis does not design the stopping subsystem; sections 2-3 state requirements and order, not mechanisms.
- It does not claim the R0-R4 order is the only viable order; it claims the dependency constraints (retention before stops; abandonment judgments before principled forgetting) are non-negotiable.
- It does not claim stopping is sufficient for any L3, SUF, or C0 bar. Stopping is infrastructure for the lifetime evaluation (bounded waste, directed effort, revisable memory), not an invention claim.
- It does not predict H3-lite outcomes or alter the frozen prereg in any way.
- DRAFT-NOT-FROZEN.

---

## Standing architectural metric (this synthesis)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (synthesis only; nothing built)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0 added
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- WITHHOLD / ABANDON / FORGET EVENTS: 0 / 0 / 0
- COGNITION LINES: 0 added
- MODES: 0
- BRIDGES: 0
- HANDLERS: 0
- SEMANTIC CASES: 0

Analyses unified: 4. Dependency constraints stated: 3 (retention-before-stops, abandonment-before-forgetting, read-path-first). Build steps ranked: R0-R4 + 4 deferred. H3-lite relation: orthogonal with narrow overlaps, composition not dependence.
