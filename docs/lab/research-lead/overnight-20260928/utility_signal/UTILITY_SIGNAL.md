# Learner-Owned Utility Signal: Design

**Status:** DESIGN ONLY. No implementation, no variant built, no experiment run.
**Verdict:** UTILITY-DESIGN-COMPLETE.
**Date:** 2026-10-01 UTC.
**Parents:** fossil census (`7a3ba6137`), zombie census (`2b81d0692`),
bid semantics (`1538eeefe`), shared substrate (`550fa268b`),
discount spec (`62fa77192`), learning machinery (`3416ed218`),
consequence re-entry (`7eab34ff2`), eviction-corruption (`986c52fdc`).

---

## 1. The bid failure, analyzed

### 1.1 What the bid is supposed to do

The bid serves three production consumers in frozen TNN-2:

1. `activate` (line 145): retrieval ranking. Max-bid among FACTs matching
   (s, r). Hardcoded tag check excludes MAPs.
2. `evict_node` (line 259): retention priority. Min-bid among live
   unprotected nodes is evicted. MAPs are included here.
3. `ev_act` (lines 872, 884): guide selection. Max-bid among
   context-matching guides.

One number is asked to do two different jobs: rank answers for retrieval
and order victims for retention. The bid semantics analysis already
flagged this conflation. For FACTs the dual use mostly works, because a
fact's truth-evidence correlates with its keep-worthiness. For MAPs it
fails completely, because a procedure's value is in its execution
behavior, and no execution behavior is ever recorded.

### 1.2 Why the MAP bid stays at 2

The formula (`bid`, line 237):

```
bid(n) = evcount(n,1) + evcount(n,2) + evcount(n,6) + evcount(n,7)
         - evcount(n,3)
       + sum over g with type-10 edge to n of [same sum for g]
```

`promote_graph` (line 533) gives a fresh MAP: one type-2 (SUP) self-edge
(+1) and one type-6 (USE) self-edge (+1). Fresh MAP bid = 2. The USE
self-edge is semantically false: it is written once at creation and
records "promoted," not "used."

Post-creation, an exhaustive `link_edge` scan (bid semantics analysis,
section 2.2) shows exactly ONE production path that changes a MAP's bid:
`contradict_map` (line 579) adds a type-3 (CON) self-edge, -1 per
contradiction. Nothing else writes a bid-relevant edge targeting a MAP,
because:

- Query hits add USE edges to the node `activate` returns. `activate`
  returns FACTs only. The shadow FACT created inside `promote_graph` by
  `ev_teach_in` absorbs every query hit. The MAP gets nothing.
- `ev_observe` confirmations add CFM to the activated FACT, not the MAP.
- Trial and harness executions of MAPs write no edges.
- No guide ever links type-10 (MEM) to a MAP.

So MAP bid = 2 - (contradictions). It is a birth certificate minus a
contradiction count. The fossil census confirmed the consequence: all 4
MAPs at bid 2 pre-filler and post-filler, pre/post revision, live or
zombie. "The bid never reflected utility at any point in any MAP's
lifetime." Worse, MAP 22 was LIVE (referenced by revision, refs=2) and
still zombified: "Being used does not protect a MAP, because use leaves
no trace on the bid."

### 1.3 What a real utility signal needs

Six information requirements, each currently missing for MAPs:

1. **Execution attribution.** A use event must name the structure used.
   Today the shadow FACT answers and the owning MAP is invisible to the
   accounting. The refs counter from the fossil census instrumentation
   proved the information exists at the event site; it is just discarded.
2. **Success distinct from running.** The V2-hole finding: "ran without
   error" is a vacuous success signal. Utility must count correct
   outcomes, not executions. The minimum sound criterion already exists
   in the substrate spec: `out == new_o` for repairs; verification
   acceptance for trials.
3. **Negative events.** Contradiction, failed repair, failed verification
   must subtract. Currently only contradiction moves anything (-1 to bid),
   and revision outcomes are discarded (D1 in the failure-retention
   inventory).
4. **Structural validity.** A MAP whose graph root is dead, out of range,
   wrong-tagged, or shared has zero utility regardless of its history.
   The zombie census: 3.8% zombies at 1022/1024 nodes, "no machinery
   checks root integrity before use."
5. **Freshness.** Birth tick versus last-use tick. Permanent counters let
   ancient history outvote recent experience (bid semantics, gap 3).
6. **A production reader.** Per the read-path-first rule, a signal no
   decision consults is theater. The reader is eviction, plus the
   substrate's retention input.

---

## 2. Design: MAP-local utility counters

### 2.1 Storage

Two fields on the MAP node (tag-20), one field on the shadow FACT (tag-1):

- **MAP f12: signed utility U.** Initialized 0 at promotion. Incremented
  on use/success events, decremented on contradiction/failure events,
  floored at -8, saturating ceiling +127.
- **MAP f16: last-active event tick L.** Initialized to the birth tick
  `hg(W,0)`. Updated on every utility write.
- **Shadow FACT f4: owning MAP id O.** Written by `promote_graph` after
  `ev_teach_in` returns the shadow node. Lets the query-answer path
  attribute a hit to the MAP whose procedure produced the answer.

Collision audit (frozen source, read-only):

- f12/f16 on tag-20: set to -1 at promotion, never read by any production
  function on tag-20. All `ng(...,12)` / `ng(...,16)` reads in frozen
  source are on tag-101/102 graph cells (executor branch targets) or on
  FACT nodes (discount). The -1 initial value has no production meaning;
  it is safe to repurpose.
- FACT f4 on tag-1: no production cognition function reads f4 on a tag-1
  node. The one `ng(W,n,4)==9002` scan is harness-side marker detection;
  a node id in [2,1024) cannot collide with the 9002 marker.
- FACT f12 stays discount-reserved per the discount spec. Different tag,
  different semantics, documented side by side to prevent confusion.

Why MAP-local rather than a new substrate namespace: `evict_node`
already visits every node per victim selection; reading two fields is
zero marginal cost. A keyed substrate lookup per candidate per eviction
would put an O(records) lookup inside an already O(1024) scan. The
substrate keeps pursuit/strategy aggregates for the gates; utility lives
on the structure it describes. One event produces two projections: the
same event handler writes the substrate record (for decline/abandonment
gates) and the local utility (for eviction), using one shared write
vocabulary. This is not two engines; it is one event vocabulary with two
readers.

### 2.2 Write events

All writes happen inline in existing generic event paths. No new modes,
no new functions owning the decision, no task-specific sites.

| Event | Writer (existing function) | Update | Source class |
|---|---|---|---|
| Promotion | `promote_graph` | U=0, L=birth tick, shadow f4=m | taught |
| Query answered via shadow FACT | query-answer path, after `activate` returns a FACT with valid O | U+=1, L=now | self (see 2.5) |
| Trial verification success | `t2_trial` success path | U+=2, L=now | per criterion |
| Revision success | `t2_revise_graph` return 1 | U+=1, L=now | observed/self |
| Contradiction of licensing fact | `contradict_map` | U-=2, floor -8, L=now | observed |
| Revision failure | `t2_revise_graph` return 0 | U-=1, floor -8, L=now | observed |
| Trial verified-correct under audited criterion | `t2_trial` verify path | counts as success | per criterion |
| Trial ran but correctness unchecked | (no write) | "ran" alone never increments (V2-hole guard) | n/a |

Notes:

- The revision success/failure writes close the D1 discard: `t2_revise_graph`
  currently returns 0/1 and the outcome is dropped. The substrate spec
  already requires the PURSUIT (MAP id) record write at the same site;
  the U update rides the same handler.
- Bootstrap MAPs (line 780): same initialization. Their birth bid of
  cnt+1 is frozen evidence; U starts at 0 and only experience moves it.
  This separates stale birth evidence from live utility by construction.
- The query-answer writer must guard the attribution: only write when
  `2 <= O < 1024`, `ng(W,O,36)==1`, and `ng(W,O,0)==20`. An unattributed
  hit (ordinary FACT) writes nothing.

### 2.3 Learner-owned check

What the learner owns: the accumulated values. No researcher sets any
MAP's utility; U moves only in response to the learner's own experience
stream (queries it receives, trials it runs, contradictions it observes,
revisions it attempts). Two learners with different histories have
different utility landscapes over identical code. That is the
counterfactual the learning machinery spec requires: same probe,
different history, different state, via a production write path.

What is honestly scaffolded (researcher-set, labeled as such per the
three-stops rule): the increment/decrement magnitudes, the -8 floor and
+127 ceiling, the fossil-age threshold, and the eviction priority order
itself.

What would make the scaffolding learner-owned: second-order adaptation
of magnitudes and thresholds from gate outcomes (did reclaiming this
fossil free useful budget? did protecting this MAP pay off?). That is
explicitly downstream work (substrate spec, section 8). The design
requires the prereg to state the retirement condition for the
scaffolding; it does not claim to meet it now.

### 2.4 Read paths

**Primary: `evict_node` victim selection.** This satisfies the
read-path-first rule: the signal is consulted on transcript in normal
production operation under pressure, and the victim identifiably changes.

Victim priority order (first match wins):

1. **ZOMBIE.** MAP with invalid root (dead slot, out of [2,1024), live
   but wrong tag, or root shared with another live MAP) or any dead
   structure. Reclaim immediately. Structural invalidity dominates all
   history: a dead structure has zero utility regardless of U.
2. **FOSSIL.** Live MAP, root valid, U <= 0, age (now - L) > FOSSIL_AGE.
   Oldest first. This is the fossil-census population: intact,
   never referenced, bid frozen at birth.
3. **LIVE low-utility.** Remaining candidates in ascending U, ties broken
   oldest-first (the existing tiebreak).
4. **Bid fallback.** The current min-bid rule is kept as the final
   tiebreak and for node kinds without utility (per substrate spec 5.3:
   bid sweep kept as fallback, not removed).

**Structure-atomic reclaim (zombie elimination by construction).** When a
MAP is selected as victim, its SEQ-walked graph cells are reclaimed in
the same pass, using the same bounded walk the zombie detector uses
(80-step bound). The fossil census showed the observed zombie route is
"shell survives (bid 2), body rots (bid 0)"; atomic reclaim makes that
route impossible rather than detecting it afterward. This removes the
need for a zombie detector/cleaner subsystem: one mechanism fewer, not
one more.

**Structure-aware cell protection.** Graph cells (tags 101-104) reachable
from a LIVE MAP's root inherit the MAP's protection during the victim
scan: cells marked by the current pass's membership walk are skipped.
This addresses the bid-semantics gap analysis item 5 (per-node bid
cannot see structural membership; "a retention priority that cannot see
structural membership will always fossilize composite structures").
Without this, U on the MAP shell repeats the exact fossil/zombie split
the census measured: the shell would be protected while its cells rot.
Cost is O(live MAPs x chain length) per eviction pass, bounded by the
existing walk bound.

**Secondary: substrate retention input.** The substrate spec (section 5.3)
specifies that eviction consults PURSUIT records keyed by MAP id for
repair campaigns. Those records read U and L as the per-structure
utility C7 they were waiting on. This design fills the deferred C7.

### 2.5 Live / fossil / zombie classification

| State | Condition | Action |
|---|---|---|
| ZOMBIE | root invalid (dead, out of range, wrong tag, shared) | immediate atomic reclaim; U irrelevant |
| FOSSIL | root valid, U <= 0, now - L > FOSSIL_AGE | reclaim after zombies, oldest first |
| LIVE | root valid, U > 0 or now - L <= FOSSIL_AGE | protect; order by U then recency |

- FOSSIL_AGE: researcher-scaffolded initial value, honestly labeled.
  Suggested starting point: twice the observed fossilization window from
  the census battery. Retirement condition: learner adjusts it from
  reclaim-regret outcomes (downstream).
- The U ceiling (+127) plus the L recency tick together give freshness:
  an ancient heavily-used MAP cannot outrank a recently useful one
  forever, because ties and ordering consult L.
- Source-provenance rule: U increments from shadow-FACT query answers
  are src_self (the MAP's own shadow answering is self-generated
  evidence). They count for retention utility but MUST be excluded from
  any epistemic gate tally, per the substrate bootstrap-exclusion rule.
  Utility is "how much is this structure used," not "how true is it."
  Truth evidence stays in the bid/edge system; use evidence lives in U.
  The separation is deliberate and answers the bid-semantics conflation
  (section 2.3) by splitting the two jobs into two signals instead of
  overloading one.

### 2.6 Honest scope: what this does not claim

- Does not fix truth-evidence semantics. The bid still measures
  evidence-for-node for FACTs. U is retention utility, not epistemic
  confidence.
- Does not bend DYN-1. Utility changes what survives pressure, not the
  per-event write cost. DYN-1 still needs dedup, decline, and reuse
  (the decline-gate and dedup workers own that).
- Does not make reclaim non-destructive in the archival sense. Reclaimed
  structures are gone. What it makes non-corrupting: atomic reclaim
  cannot leave orphaned shells, and validity-gated reclaim cannot kill a
  live structure's body while keeping its header.
- Does not invent similarity, retrieval, or transfer. Cross-domain reuse
  remains the five-deep dependency chain (verification, usable
  structure, reusable structure, rebinding, learned retrieval).
- Does not protect against the majority-wrong adversary pattern: a
  wrong-but-frequently-used MAP accumulates U. Utility is use, not
  truth. The discount mechanism and revision criteria own correctness;
  U must never be read as a correctness signal.

---

## 3. Integration and One-System Rule check

### 3.1 Substrate relation

- This design fills the deferred C7 (per-structure utility) that the
  substrate's retention read path (5.3) depends on. No new namespace is
  needed: utility is keyed by node id implicitly because it lives on the
  node. PURSUIT records keyed by MAP id reference it; there is no
  duplicate storage.
- The write vocabulary is shared with the substrate (section 4):
  attempt / success / failure with source tags. The query-answer handler
  writes the substrate PURSUIT (s, r) success AND the MAP U increment in
  one place. The revision handler writes the PURSUIT (MAP id) outcome
  AND the U update in one place. One event, two projections, one
  vocabulary.

### 3.2 One-System Rule audit

- **Modes: 0.** No utility mode. Writes happen inline in existing event
  paths (query answer, trial verify, revision, contradiction, eviction
  scan).
- **Bridges: 0.** Native i32 fields on existing nodes. No translation
  layer between a utility subsystem and cognition; there is no utility
  subsystem.
- **Task-specific handlers: 0.** Every write site is a generic event
  path, not a per-task or per-world handler.
- **New edge types: 0.** Attribution uses the MAP-id field on the shadow
  FACT, not a new edge type. This avoids the ET inflation the
  composition design is already spending (ET_FRAGUSE=14 and siblings)
  and avoids the bid-inheritance side effect a type-10 MEM edge would
  cause (the MAP would inherit the shadow FACT's bid sum).
- **New node kinds: 0.** No utility nodes, no counters table, no sidecar
  structures.
- **Semantic cases: 0.** Live/fossil/zombie is a predicate over existing
  fields (root validity, U, L), not a content-based case split on what
  the procedure computes.
- **Net mechanism count: negative.** Structure-atomic reclaim removes the
  future need for a zombie detector/cleaner. The design deletes a
  prospective subsystem rather than adding one.

### 3.3 Consolidation with neighboring designs

- **H3-lite Node 1 field-32 migration:** unaffected. That counter moves
  to STRATEGY records (per-family selection). Utility is per-structure
  retention. The two do not overlap; neither is duplicated.
- **Fragment F-utility:** if fragment composition proceeds, fragment
  invocation/success counters should use this same U/L vocabulary on the
  fragment-bearing node rather than a parallel private counter. Flagged
  here as a convergence requirement for the composition builder.
- **Discount:** FACT f12 is discount (epistemic suspicion, consumer:
  bootstrap scan). MAP f12 is utility (retention use, consumer:
  eviction). Different tags, different semantics, different readers.
  Documented together so a future reader does not conflate them.

---

## 4. Falsification and evaluation (for the builder's prereg)

1. **Fossil discrimination.** Mixed battery (promote N MAPs, use K of
   them), then eviction pressure. Prediction: fossils (U<=0, old L)
   are reclaimed before live MAPs; the reclaim-order trace shows the
   U/L ordering, not the bid ordering. Fails if bid order dominates the
   victim sequence.
2. **Zombie preemption.** Heavy churn to 1022/1024 nodes, then census.
   Baseline: 3.8% zombies. Prediction: 0 zombie MAPs survive an eviction
   pass, because atomic reclaim makes the shell-without-body route
   impossible, not rare.
3. **Use-protection (MAP 22 replay).** The fossil census's sharpest case:
   a MAP referenced by revision (refs=2) still zombified. Prediction:
   with U>0 the MAP's cells are protected through the filler wave; the
   MAP survives intact. Fails if the MAP still zombifies (would show the
   cell-protection walk is not firing).
4. **Zero-pressure equivalence.** Battery output byte-identical with and
   without utility writes when no eviction fires (the fossil census's
   own base-vs-full equivalence method). Utility must be behavior-free
   until the reader runs.
5. **Cost visibility.** Utility writes are in-place field updates: zero
   node allocations per event. Overhead must appear in the DYN-1
   accounting and stay a small constant fraction of per-event cost.
6. **Redundancy falsification (S2-style).** If structure-aware bid
   inheritance alone (no U counter) achieves the same reclaim ordering
   on the test batteries, the U counter is redundant and this design is
   overstated. The design must earn the extra field against that
   simpler alternative.

---

## 5. Open questions for future work (not decided here)

1. Should U increments from trial verification (+2) outweigh query hits
   (+1)? The 2:1 ratio is scaffolding with no evidence behind it.
2. Is the -8 floor deep enough to let a contradicted-but-useful MAP
   recover, or does it create a poverty trap? Needs the rehabilitation
   measurement the discount adversary is running.
3. Should abandonment (substrate `state`=ABANDONED) force U to the floor,
   or should U and pursuit-state stay independent signals? Kept
   independent in this design; the interaction is untested.
4. Does the membership walk cost stay acceptable at 1024 nodes with many
   live MAPs, or does eviction need the walk amortized across passes?
   Measurement required, not assumed.

---

## 6. Standing metrics (this design)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 added (design only; no code)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0 (no new node kinds, edge types, or modes)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0 built (magnitudes and thresholds
  scaffolded with a stated retirement condition)
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

**Verdict: UTILITY-DESIGN-COMPLETE.**
