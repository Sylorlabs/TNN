# Forgetting, Compression, and Retirement: Analysis

Date: 2026-10-01. Analyst: Forgetting Analyst (subagent).
Subject: frozen TNN-2, build commit `f4de7ff46`.
Mode: analysis only, read-only. No implementation, no design.

Question: what SHOULD forgetting look like in a continuous learner, and
what is the gap in TNN-2? Micah's continuous-learner message names
forgetting explicitly as a learner freedom: "forget/compress/retire
structures when useful" and "change retention priorities", under the
ideal of FROZEN RESEARCHER CODE plus CONTINUOUSLY CHANGING LEARNER STATE.

## 1. Inventory: TNN-2's current forgetting-adjacent machinery

### 1.1 The retention machinery (source audit, all researcher-authored)

| Mechanism | Source location | Behavior |
|---|---|---|
| Node budget | `alloc_node` (87) | 1024 nodes. Dead slots (slot36=0) reused first; when full, `evict_node` is called. |
| Eviction victim selection | `evict_node` (254) | Scans all 1024 nodes from cursor hg(W,8). Picks the lowest-bid UNPROTECTED live node. Ties broken oldest-first (strict `<` comparison). Advances cursor past victim. |
| Bid | `bid` (237) | Count of type-1 (DEP) + type-2 (SUP) + type-6 (USE) + type-7 (OBS) edges targeting the node, MINUS type-3 edges, plus the same sum for any node linked to it by a type-10 (policy) edge. |
| Protection | `is_prot` (221) | Node is protected iff it has a live type-9 (PRO) edge with clock > 0. |
| Protection refresh | `ref_prot` (276) | Sets the node's PRO edge clock to the current event clock: 12 events of protection from the last refresh. |
| Decay | `decay` (153) | Runs ONCE PER EVENT (teach, query, observe). Every type-9 PRO clock decrements by 1; at 0 the edge is deleted. |
| Fact lifecycle | `ev_teach_in`, `ev_query` (811), `ev_observe` (831) | Facts are created with a self PRO edge (clock 12). A query HIT adds a self USE edge (type 6) and refreshes protection. An observe MATCH adds a self OBS edge (type 7) and refreshes protection. An observe CONTRADICTION adds a self type-3 edge (which LOWERS the bid) and triggers revision. |
| MAP lifecycle | `promote_graph` (533) | MAP nodes get self SUP (type 2) + self USE (type 6) edges: a CONSTANT bid of 2. NO PRO edge. NO protection. NO decay-linked lifetime. |
| Graph cells and literals | assemblers | Tags 101-104 (ops) and 902 (literals): no self edges, bid 0, unprotected. |
| Trial garbage | `t2_trial` | Every rejected trial candidate leaves its cells allocated. Never linked, never freed, never deallocated. |
| Eviction log | `rec_evict` (249) | Each eviction writes a type-3 record node chained at slot 12, storing the evicted node's root, promotion index, answer, and clock. NOTHING reads these records. Under full budget, `alloc_raw` returns -1 and the record is silently dropped: the forgetting trace itself is not reliably kept. |

### 1.2 Who decides: six researcher-fixed forgetting criteria

Every retention decision in TNN-2 is made by fixed source constants. No
learner-state field is read by `alloc_node`, `evict_node`, `bid`,
`is_prot`, `ref_prot`, or `decay`.

1. Budget 1024. Fixed.
2. Protection window 12 events. Fixed.
3. Bid weight 1 per edge of each counted type. Fixed.
4. Scan from cursor, oldest-first ties. Fixed.
5. "Contradicted facts are cheaper to keep": the type-3 self edge on
   contradiction lowers the bid. This is a researcher-authored forgetting
   criterion baked into the bid function.
6. "Frequently queried facts are expensive to evict": each query hit adds
   a permanent USE edge (type 6 has no decay), so bid grows unboundedly
   with hits. This is a researcher-authored retention criterion, a crude
   fixed proxy for utility.

Plus two researcher-chosen constants with structural consequences:

7. "MAPs are worth exactly 2, forever": the SUP+USE self edges never
   decay, never refresh, never change.
8. "Graph cells are worth 0": the executable structure is always the
   cheapest thing to evict.

Learner-state input to any retention decision: ZERO.

### 1.3 Observed outcomes (transfer analysis P4: 1050 teaches past budget)

- The executable structure dies FIRST. All 101-104 cells (the winning
  8-cell graph AND the 10 rejected-trial garbage cells) evicted: bid 0,
  unprotected.
- The MAP outlives its graph and becomes a FOSSIL. Bid 2 beats the
  zero-bid sweep, so node 45 keeps tag 20, but its root cells are gone
  (re-execution returns -999999) and its licensing facts were evicted
  (provenance edges removed with them). It can never be revised or
  executed again. It is inert, unrevisable, and reclaimed last.
- The promoted FACT is also evicted. PRO clocks expire after 12 idle
  events, and the cursor sweep kills oldest zero-bid nodes first. The
  learned answer is catastrophically forgotten (requery = -2) and cannot
  be rebuilt because the licensing facts are gone too.
- Trial garbage is the dominant budget consumer under sustained trial
  activity and the first eviction victim: the system spends its eviction
  budget discarding its own scratch.
- Graceful at the interface: the forgotten query falls through trial and
  P-INV bootstrap into `miss_inquire`, re-creating UNCERTAINTY plus guide.
  The system reverts to inquiry rather than confabulating.

## 2. Definitions: forgetting vs compression vs retirement

These are three distinct cognitive functions. TNN-2 has none of them.
Eviction is workspace pressure management; it is not any of these.

- FORGETTING (deletion): permanent removal of a structure. Functional
  requirement: the decision must be justified by learner experience
  (utility estimates, usage history, dependency analysis), not by a
  fixed clock. Deletion should prefer structures whose removal least
  degrades future capability, and it must be revisable: re-learning a
  forgotten structure should be cheaper than first learning it.
- COMPRESSION: reduction of retention cost while preserving recoverable
  function. Operates on redundancy the learner identifies in its own
  state. Concrete redundancies in TNN-2 (from transfer analysis
  section 7): (a) trial garbage, compressible to zero cost, since it has
  no function; (b) MAP/FACT duplication, since the MAP's stored answer
  duplicates the promoted FACT for same-(s,r) queries (the MAP's unique
  roles are provenance-for-revision and the re-executable graph);
  (c) degenerate P-INV MAPs (root field 0), pure provenance records with
  no execution or revision use.
- RETIREMENT: a third state between live and deleted. Retired means
  excluded from active lookup and held at low retention cost, but
  recoverable on demand at bounded cost (re-derive, re-verify, re-link).
  A fossil is the ANTI-retirement: full retention cost, zero recoverable
  function, no path back to utility.

## 3. Functional requirements for learner-owned forgetting

Each requirement is stated as a decision the learner must be able to
make. Per Micah's K-H3 audit standard, a value in learner state with no
exercised production write path is theater: each requirement therefore
names the read path (what retention machinery must consult) and the
write path (what experience must set it).

- R1. RETENTION PRIORITY CONTROL. Learner state must contain fields that
  the eviction machinery READS (a protection override, a bid
  contribution, or a scheduling flag), and production write paths that
  SET them from experience (for example: "this structure licensed a
  later success" raises protection; "this structure never fires" lowers
  it). Today: no learner-state field is read by any retention function.
- R2. UTILITY-GROUNDED DELETION. The deletion criterion must reference
  experienced utility (reuse events, revision events, dependency degree),
  not elapsed events. Today: the only deletion criterion is bid plus
  clock, both researcher-fixed.
- R3. COMPRESSION OF IDENTIFIED REDUNDANCY. The learner must be able to
  recognize redundancy in its own state (duplicate answers, dead
  provenance, garbage cells) and collapse it. Today: zero compression;
  the MAP/FACT duplication is structural, not optional.
- R4. RETIREMENT AS A STATE. A retired structure must be
  distinguishable from a live one (excluded from lookup) and from a
  deleted one (recoverable). Today: two states only (live, dead), plus
  the accidental third state of fossil (dead but occupying).
- R5. REVISABLE FORGETTING. When a forgotten structure is needed again,
  re-learning must be cheaper than first learning. Candidate accelerants
  already exist but are unused: the `rec_evict` records (what was
  forgotten, when, with what answer) and surviving partial structures.
  Today: the eviction log is never read; forgotten answers are rebuilt
  from zero or not at all.
- R6. DEPENDENCY-AWARE EVICTION. Retention decisions should consider
  cross-structure dependencies (a fact that licenses a MAP, a MAP whose
  shape resembles another's). Today: eviction is per-node; killing a
  licensing fact silently amputates its MAP, which is exactly how
  fossils are manufactured.

## 4. The fossil problem

The fossil is the precise inversion of principled retirement:

- Retention cost: fossil HIGH (bid 2, reclaimed last); retired LOW
  (excluded from the active set).
- Executability: fossil NO (cells gone); retired RECOVERABLE at bounded
  cost.
- Revisability: fossil NO (provenance gone); retired PRESERVED or
  summarizable.
- Lookup: fossil INERT (never queried, but occupying); retired EXCLUDED
  by design.
- Path back to utility: fossil NONE; retired DEFINED.

Root cause: retention bids are per-node and fixed, while utility is
per-structure and experiential. The MAP's constant bid of 2 keeps the
header alive while the bid-0 policy kills its body and the clock-12
policy kills its dependencies. Fossilization is therefore not an
accident of the current policy; it is the guaranteed output of any
fixed per-node bid scheme under pressure whenever a structure's parts
carry heterogeneous fixed bids. Fixing fossils requires structure-level
retention reasoning, not better node-level constants.

## 5. Gap analysis

Missing, all six:

1. No learner-state field is read by any retention decision (R1).
2. No deletion criterion references experienced utility (R2).
3. No compression of any kind (R3).
4. No retirement state; the fossil is the accidental anti-state (R4).
5. No reuse of eviction records; forgetting is not revisable (R5).
6. No dependency-aware eviction (R6).

Minimal architectural delta (decision points, not implementation): the
eviction path would need to read at least one learner-writable field per
node or per structure (a protection override, a bid contribution, or a
retirement flag), and at least one production write path would need to
set that field from experience (reuse-driven protection, disuse-driven
demotion, dependency-driven grouping). This is the same class of move as
H3-lite's policy nodes: a researcher-fixed constant (a bid weight, a
clock, a protection rule) replaced by a learner-writable value with an
exercised write path. The six fixed quantities in section 1.2 are the
candidate decision points; the fossil analysis additionally requires
that retention reasoning operate at structure granularity, not node
granularity.

What this analysis does NOT claim: that any specific delta achieves SUF,
L3, C0-D, or any TNN-3 bar. Forgetting is infrastructure for the
lifetime evaluation; it is necessary for "memory under long
interference" but not sufficient for any invention claim.

## 6. Relation to the lifetime evaluation

Micah's lifetime stream requires measuring "memory under long
interference", including "whether learning itself improves" and "reuse
of old executable structures". Under the current fixed policy, the
predicted lifetime outcome is the P4 profile repeated at scale:
executable structures die first, MAPs fossilize, learned answers are
catastrophically forgotten after 12 idle events, and trial garbage
consumes the budget. The interference experimenter is measuring this
profile; this analysis states what would have to change for the
measurement to improve: learner-owned retention priorities (R1, R2),
compression of identified redundancy (R3), retirement instead of
fossilization (R4), revisable forgetting (R5), and dependency-aware
eviction (R6).

## 7. Standing architectural metric (this analysis)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 8 identified (budget, clock,
  bid weights, scan order, tie rule, contradiction penalty, hit bonus,
  MAP/graph constants), section 1.2
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: all retention behavior enumerable from source
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: n/a (analysis only)
- REVISION EVENTS: n/a (analysis only)
- COGNITION LINES: 0 added (analysis only)
- MODES: 0
- BRIDGES: 0
- HANDLERS: 0
- SEMANTIC CASES: 0
