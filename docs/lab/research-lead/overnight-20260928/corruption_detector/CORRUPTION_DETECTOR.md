# CORRUPTION Detector Specification

**Status:** SPECIFICATION-COMPLETE. No implementation exists.
**Date:** 2026-10-01.
**Scope:** Driver-side (researcher harness) detection of silent structural
destruction in frozen TNN-2 learner state, for the lifetime protocol.
**Verdict:** CORRUPTION-DETECTOR-COMPLETE.

## 1. Purpose

Frozen TNN-2 can silently corrupt its own procedural memory under budget
pressure: `evict_node` reclaims graph cells while surviving MAP shells keep
pointing at the freed slots, which `alloc_node` then reuses for unrelated
nodes. No production code checks MAP root validity, so the corruption is
invisible to the learner. The lifetime protocol (v2, Section 6.1) requires
the driver to detect it by snapshot comparison at world boundaries and log
CORRUPTION events. This document specifies exactly how.

Grounded in:

- `986c52fdc` (eviction corruption: DESIGN FLAW, field-based roots
  invisible to edge cleanup; MAP 45 and MAP 82 corrupted during FW9;
  policy anchor evicted).
- `2b81d0692` (zombie census: 3.8% zombies at 1022/1024 nodes, 0% at
  520/1024; two-pass detector; Z_WRONGTYPE and Z_SHARED observed;
  zero production detection or cleanup).
- Lifetime protocol v2, Sections 5 (step 4a), 6.1, 7.7, 11, 18.

## 2. What the detector watches

### 2.1 The core target: MAP field-20 root

`promote_graph` stores the executable graph root as a plain integer in
field 20 of the tag-20 MAP node (`write_node(W,m,root,...)`; frozen base
comment "field20=graph root"). `evict_node` deletes only edges touching
the victim; it never scans MAP root fields. Graph cells carry bid 0
(SEQ type-12 edges are not in the bid formula) while MAP shells carry
bid 2, so under pressure the cells a MAP depends on are evicted first
and the MAP shell survives, pointing at a reused slot.

A root is valid iff it names a live node whose tag the executor accepts.
`t2_exec` (frozen source, EXECUTE section) accepts tags 101 (SETREG),
102 (guard/BRANCHEQ), 103 (INC), 104 (DEC) and returns -999999 for any
other tag. The valid-root set is therefore {101,102,103,104}, grounded
in executor semantics, not convention.

### 2.2 Other field-based node references (same flaw class)

Read-only source inspection confirms three more integer node references
invisible to `evict_node`:

- Guard cell (tag 102) field 12: branch-true target cell. Set by the
  assemblers (`ns(W,g,12,st)` in `t2_asm_chain`, `t2_asm_count`) and by
  revision (`ns(W,g,12,nst)` in `t2_revise_graph`). Read by the executor
  (`nx=ng(W,cur,12)`). Field 16 (branch-false target) is never set.
- SETREG cell (tag 101) field 8: literal operand node id. `t2_set` and
  `t2_guard` store the tag-902 literal node id here; `res_op` resolves
  `0 <= op < 1000` via `ng(W,op,20)` (the literal's value). If the
  literal node is evicted and its slot reused, the SETREG silently reads
  a wrong value.
- Guard cell (tag 102) field 8: literal operand node id (same mechanism
  as SETREG).

These are REQUIRED to be documented and RECOMMENDED for detection
(Section 9). The REQUIRED core of this specification is the MAP root
check, which is what the protocol's CORRUPTION event names.

### 2.3 Out of scope

- SEQ successor links are type-12 edges (`seq_link` calls `link_edge`),
  so `evict_node` severs them correctly. A severed SEQ link truncates a
  graph (fossil-like); it does not create a wrong-type root.
- FACT field 20 holds the subject integer (a domain value, not a node
  id). Tag-903 node field 20 holds a return sentinel. Neither is a node
  reference.
- The tag-2 policy anchor eviction observed in FW9 (its MEM edges
  emanating from a reused slot) is a slot-reuse anomaly of the same
  family; a liveness check for the anchor is listed as a recommended
  extension, not core.

## 3. When detection runs

Per protocol v2 step 4a: at each world boundary, after the teach stream
completes and before the next world's stream begins, the driver takes a
white-box snapshot and runs the detector. It also runs at the final
retention sweep (which feeds the ZOMBIE-STATE classification).

CORRUPTION events are therefore emitted at boundary processing time.
Attribution caveat: the corruption occurred at some unknown point during
the preceding world's stream, not at the boundary. The `world` field
names the world whose stream just completed. This is world-granular
attribution, not event-granular. The protocol's measures must not treat
a CORRUPTION event as timestamped to the boundary tick.

## 4. Snapshot format

For every live (field 36 == 1) tag-20 node, one canonical line:

```
MAP <id> <root> <root_tag_or_dead> <promo_index>
```

- `<id>`: MAP node id.
- `<root>`: field 20 value.
- `<root_tag_or_dead>`: `ng(W,root,0)` if 2 <= root < 1024 and the node
  is live, else the literal token `dead` (covers dead slots and
  out-of-range roots; the classifier refines these).
- `<promo_index>`: field 24 (the `hg(W,24)` nonce at promotion). Used
  for MAP identity across snapshots: `alloc_node` reuses slots, so a
  node id alone does not identify a MAP over time. Identity key is
  `(id, promo_index)`.

Lines sorted by id, joined with `\n`, hashed with SHA-256. The hash is
committed to the run log at each boundary. The full snapshot text is
retained as run evidence (it is small: one line per MAP).

## 5. Detection algorithm

Two passes, driver-side, read-only. Deterministic: same workspace state
always yields the same classification.

### 5.1 Pass 1: per-MAP root validity

For each live tag-20 MAP node m with root = field20(m):

1. root == 0: BOOTSTRAP. Degenerate (a promoted MAP always has a real
   root). Not corruption. No event.
2. root < 2 or root >= 1024: Z_RANGE. The root was never a valid slot.
   Indicates an invariant break worse than eviction churn. Emit
   CORRUPTION.
3. node root dead (field 36 != 1): FOSSIL. The cell was evicted and its
   slot never reused (or reused then freed again and currently dead).
   The MAP shell survives with a dangling root: full budget cost, zero
   function. Emit CORRUPTION with status FOSSIL. (The zombie census
   called this Z_DEAD; the protocol's ZOMBIE-STATE taxonomy calls it
   FOSSIL. This spec uses FOSSIL.)
4. node root live and tag in {101,102,103,104}: VALID. Proceed to pass 2.
5. node root live and tag not in {101,102,103,104}: ZOMBIE. The cell
   was evicted and its slot reused by a wrong-typed node (observed:
   tag-30 UNCERTAINTY node, tag-902 literal cell). Emit CORRUPTION with
   status ZOMBIE.

### 5.2 Pass 2: shared and hijacked roots (VALID MAPs only)

Zombies cannot host a hijack claim: a pass-1-failed MAP is excluded as
a host and as a victim in this pass.

- Build the SEQ successor index in one edge pass: for each live
  type-12 edge, map source cell to target cell.
- For each VALID MAP, walk its graph: start at root; at a tag-102
  guard follow field 12 (matching the executor); otherwise follow the
  SEQ successor; bound the walk at 80 steps (same bound as the census).
- Z_SHARED: two live MAPs name the same root id. Emit CORRUPTION for
  each MAP involved (see Section 8 for why sharing is dangerous even
  though each root is individually valid).
- Z_HIJACKED: MAP B's root is visited during MAP A's graph walk
  (A != B). MAP B's graph has been absorbed into A's reachable
  structure. Emit CORRUPTION for B.

A MAP passing both passes is LIVE.

### 5.3 Transition and dedup rule

The driver keeps a table of last-known status keyed by MAP identity
`(id, promo_index)`. A CORRUPTION event is emitted only on transition:

- Previous status LIVE (or MAP newly seen) and current status in
  {FOSSIL, ZOMBIE, Z_SHARED, Z_HIJACKED}: emit once.
- A MAP that remains corrupt across consecutive boundaries is not
  re-emitted. Its ongoing presence is visible in the per-boundary
  ZOMBIE-STATE counts.
- If a node id is reused by a new MAP (promo_index differs), the old
  entry is retired and the new MAP is evaluated fresh.

This makes CORRUPTION events count corruption onsets, while
ZOMBIE-STATE counts (Section 7) report prevalence.

## 6. CORRUPTION event specification

Fixed field order, one event per line, matching the protocol v2
Section 6.1 signature:

```
CORRUPTION <world> <map> <field> <expected_type> <actual_type>
```

- `<world>`: id of the world whose stream just completed (Section 3
  caveat applies).
- `<map>`: MAP node id.
- `<field>`: 20 for the core check; 12 for the guard-target extension
  (Section 9).
- `<expected_type>`: for field 20, the literal string
  `graph-cell(101|102|103|104)`. For field 12, `setreg-cell(101)`.
- `<actual_type>`: one of `tag-<n>` (the occupying node's tag, e.g.
  `tag-30`, `tag-902`, `tag-102`), `dead` (FOSSIL: slot not live),
  `range` (Z_RANGE), `shared-root` (Z_SHARED), `hijacked` (Z_HIJACKED).

Examples:

```
CORRUPTION C 45 20 graph-cell(101|102|103|104) tag-902
CORRUPTION C 82 20 graph-cell(101|102|103|104) hijacked
CORRUPTION D 39 20 graph-cell(101|102|103|104) shared-root
```

The event is distinct from EVICT by construction: EVICT is the clean
removal of a node (its slot freed, its edges severed, budget recovered);
CORRUPTION is the silent invalidation of a surviving structure (the MAP
shell persists, occupies budget, and points at garbage or at another
structure's cells). A single eviction can cause zero EVICT-adjacent
harm to MAPs while causing one or more CORRUPTION events.

## 7. ZOMBIE-STATE classification mapping

At the final retention sweep the detector's per-MAP status maps
directly onto the protocol's four end-states:

- LIVE: passed both passes.
- ZOMBIE: ZOMBIE, Z_SHARED, or Z_HIJACKED.
- FOSSIL: FOSSIL (dangling root). Note the forgetting-analysis sense
  of fossil (shell outlives function) is exactly this: the MAP node
  survives at bid 2 while its graph is gone.
- DELETED: the MAP node itself was evicted (absent from the live
  tag-20 set; visible via EVICT lines, not via this detector).

The sweep reports counts per end-state per origin world, alongside
probe scores, per protocol Section 7.7.

## 8. The shared-root landmine

Z_SHARED deserves its own section because each involved MAP looks
healthy in isolation: both roots are live graph cells of valid tags.
The danger is operational, not classificatory.

If MAP A and MAP B share root cell R:

- `t2_revise_graph` on A rewires guard targets and SETREG steps
  through R (`ns(W,g,12,nst)`, `seq_link`). Those writes silently
  alter B's graph. B gets no REVISE event; its provenance is not
  consulted; its answer fact is not updated. B is collaterally
  modified with no log signature except the earlier Z_SHARED flag.
- Any future MAP-execution path (query-time execution, composition
  splicing) operating through A's root operates on B's cells and
  vice versa. The two MAPs are no longer independent structures.

In frozen TNN-2 the query path never executes MAPs, so the landmine
is inert today; revision is the live wire. Rule for future work:
any revision or execution machinery must consult the detector's
shared-root table before touching a MAP's graph, and a Z_SHARED flag
on a MAP must block unattributed in-place revision of its cells.

## 9. Recommended extensions (not core)

These use the same snapshot and emission machinery but are not
required for protocol compliance:

1. Guard branch-target check. During the pass-2 walk, for each
   tag-102 guard cell, verify field 12 names a live tag-101 cell.
   Dead target: truncated branch (fossil-like). Wrong-type target:
   guard corruption. Emit `CORRUPTION <world> <map> 12
   setreg-cell(101) <actual>`.
2. Literal-operand check. For each tag-101 SETREG and tag-102 guard,
   if field 8 names a node id (0 <= op < 1000 per `res_op`), verify
   it is a live tag-902 node. A reused slot means the cell silently
   reads a wrong literal value: semantic corruption with no
   structural signature at the MAP root.
3. Policy-anchor liveness. Exactly one tag-2 node should exist and be
   live (created lazily by `miss_inquire`). If it is missing or its
   slot was reused (the FW9 observation), emit a CORRUPTION-class
   driver alert. Field vocabulary does not apply; log as
   `CORRUPTION <world> <anchor_id> anchor policy-anchor(tag-2)
   <actual>`.

## 10. Driver cost

The detector is driver-side and runs O(boundaries), not O(events):

- Pass 1: one scan over up to 1024 nodes, filtering live tag-20.
- Pass 2: one edge pass (4096 slots) for the SEQ index, then at most
  one bounded 80-step walk per VALID MAP.
- Snapshot: one line per live MAP.

This is negligible next to the per-event scan costs measured in the
cost accounting (`3eeb0d78e`: a query hit costs ~38k scan steps; a
boundary snapshot costs on the order of 5k).

## 11. Explicit non-claims

- The detector does not prevent corruption and does not repair it.
  It makes silent destruction visible. Prevention is a TNN-3
  retention-design problem (structure-level bids, dependency-aware
  eviction).
- A zero CORRUPTION count at a boundary is evidence of no detected
  corruption, not proof of none: the core check covers MAP roots
  only. Interior guard-target and literal-operand corruption require
  the Section 9 extensions.
- CORRUPTION counts are workload- and pressure-dependent. The census
  measured 0% at 520/1024 nodes and 3.8% at 1022/1024 under
  chain-promotion churn, with 20% observed in the more diverse W
  cumulative state. Rates are diagnostics, not constants.
- The detector reads frozen-state layout (tags, field numbers). Any
  build that changes the MAP layout or graph cell tags must update
  this spec before its lifetime runs.

## 12. Standing metrics (this specification)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: the detector algorithm,
  snapshot format, event field order, classification taxonomy
  (researcher-owned measurement infrastructure; this is the
  legitimate role).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- CORRUPTION EVENTS: 0 (specification only; events will be counted
  when lifetime runs execute).
- COGNITION LINES: 0. MODES: 0. BRIDGES: 0. HANDLERS: 0.
- SEMANTIC CASES: 0.
