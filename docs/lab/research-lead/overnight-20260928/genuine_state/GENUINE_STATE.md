# Genuine State Map: What Remains After Theater Removal

**Status:** ANALYSIS ONLY. Read-only white-box of frozen TNN-2
(`tnn2_build/tnn2.zag`, 1591 lines, SHA-256 `a29972ca...` verified).
No fixes proposed. No variant built.

**Verdict: GENUINE-STATE-COMPLETE.**

## 0. Correction to the theater audit

The theater audit (`e0423538a`, section 2) lists "GUIDE nodes (tag 2)".
This is imprecise. `miss_inquire` (line 807) creates the guide with
`ns(W,g,0,1)`: guides are **tag-1 nodes** carrying a field20=30 marker,
`write_node(W,g,30,-999,0,0)`, field4=s as context. The single **tag-2
node** is the policy anchor created lazily at line 803
(`ns(W,pr,0,2); ns(W,pr,4,-5)`), which `pol_set` points at. The audit's
substance holds (both production paths exercised for the guide/anchor
substrate), but the tag attribution is corrected here. Any downstream
document citing "tag-2 guide nodes" should read "tag-1 guide nodes with
field20=30, anchored by one tag-2 node."

## 1. Component inventory

### 1.1 FACT nodes (tag 1): the knowledge store

**Layout:** field0=1 (tag), field36=1 (live), field20=s, field24=r,
field28=o, field32=clock-at-write (via `write_node`: a to 20, b to 24,
c to 28, d to 32).

**Writers (5 internal sources, indistinguishable in state):**
- `ev_teach` (L297): full event. clock++, `decay`, `ctx_push(s)`,
  alloc, PRO self-edge (TTL=hdr4=12), INS edge to previous fact,
  `log_ev` kind 1.
- `ev_teach_in` (L310): bare insert. alloc, PRO self-edge. No clock,
  no decay, no log. Used by `promote_graph` (MAP shadow), 
  `bootstrap_miss` (own guess), `t2_revise_graph` (corrected answer),
  `ev_observe` (re-teach after contradiction).
- `promote_graph` (L543): shadow FACT via `ev_teach_in(W,s,r,ans)`.
  This shadow is what `activate` finds; the MAP itself is never
  executed on the query path.
- `bootstrap_miss` (L783): teaches its own inferred value.
- `t2_revise_graph` (L748): teaches the re-executed output.

**Readers:**
- `activate` (L139): max-bid exact (s,r) scan over live,
  non-superseded tag-1 nodes.
- `t2_gather` (L460): BFS paths over tag-1 facts (r != -999).
- `t2_lu_first` (L425), `t2_chain` (L434), `t2_gather_sum` (L473),
  `inc_fill` (L546): gather helpers.
- `bootstrap_miss` (L764): reverse scan of tag-1 nodes by r.
- `ev_observe` (L838): activate, then compare field28 to observation.

**Supersession:** ET_CON self-edge (type 3, source==target==n) marks a
fact superseded. `activate` and `ev_act` skip superseded nodes.
`ev_observe` adds CON on contradiction (L843); `t2_revise_graph` adds
CON to the old answer fact (L744). `is_superseded` (L131) scans for
the self-edge. CON count is subtracted in `bid`. Genuine.

**Limits:** 1024 node slots shared with all other node types; exact
(s,r) lookup only; no source provenance (5 writers, one tag); no
confidence or uncertainty attached to the fact itself.

### 1.2 Guide nodes (tag 1, field20=30): action-selection candidates

**Layout:** field0=1, field36=1, field4=s (context = the missed
subject), field20=30 (action), field24=-999, field28=0, field32=0.

**Writer:** `miss_inquire` (L806): one guide per miss. DEP edge
(type 1) guide to UNCERTAINTY node; MEM edge (type 10) from policy
anchor to guide.

**Reader:** `ev_act` (L859): traverses edges incident to POLICY_ROOT,
takes neighbors as candidates, keeps those whose field4 matches any
of the 4 context-stack slots and that are live and non-superseded,
ranks by `bid`, returns field20 of the winner.

**Semantics of the action value:** field20=30 is opaque. No production
code interprets it; `ev_act` returns it and the harness consumes it.
The value 30 coincides with T_UNCERT but nothing in production makes
that connection.

**Learning in ev_act:** near-zero. Winner gets a USE self-edge, so
`bid` rises by 1 and previously selected guides win later ties
(incumbency). No other adaptation: no new guides from success, no
guide removal, no context generalization (match is raw subject
equality against a 4-slot recency buffer).

**Second-order scan is inert:** `ev_act` also checks neighbors of each
candidate. A guide's neighbors are its UNCERTAINTY node (field4=-4)
and the anchor (field4=-5); neither can match a context slot (subjects
or -3). The loop fires on no structure the system actually builds.

**Collision note:** guides are tag-1 nodes, so `activate(W,30,-999)`
would retrieve one, and `t2_gather` can walk through field20=30 as a
value. No production query uses s=30, r=-999, so this is latent, not
active.

### 1.3 MAP nodes (tag 20): procedure shells

**Layout:** field0=20, field36=1, field4=r, field8=s, field12=-1,
field16=-1, field20=graph root, field24=promotion edge-count,
field28=answer.

**Writers:**
- `promote_graph` (L534): real trial promotion. SUP self-edge +
  USE self-edge (the "birth certificate", bid 2), COR self-edge
  (type 13, no readers), DEP edges to licensing facts, shadow FACT.
- `bootstrap_miss` (L777): bootstrap MAP. field20=0 (no graph),
  field24=edge count, cnt SUP self-edges + USE self-edge, COR
  self-edge, teaches its guess as FACT.

**Readers:**
- `revise_on_contradict` (L690): scans MAPs for a DEP edge to the
  contradicted fact, calls `t2_revise_graph`. This is the MAP's only
  genuine production read path.
- `t2_revise_graph` (L706): reads field20 (graph root), field8 (s),
  field4 (r), field28 (old answer); re-executes the graph after
  surgery; retargets field28 on success.
- Query path: NEVER. Confirmed by execute-vs-cache (`7186294cd`):
  no frozen query path executes a stored graph. MAPs are closed
  replays; re-execution cannot detect staleness.

**Genuine function, precisely:** revision targeting and nothing else.
The node is not theater (both paths exercised), but its primary
purpose (executable procedure reuse) is unexercised. The MAP's
executable body is genuine-for-revision, inert-for-query.

### 1.4 Executable graph cells (tags 101-104, 902): MAP bodies

**Layout:** cells carry tag 101 (MOVE), 102 (BRANCHEQ), 103 (INC),
104 (DEC). Operands in fields 4/8/12/16; literals are tag-902 nodes
with the value in field20. Cells chain via SEQ edges (type 12);
BRANCHEQ true-targets use field12 directly.

**Writers:** `t2_asm_chain`, `t2_asm_count`, `t2_asm_sum` (trial
assembly); `t2_revise_graph` (surgical insert of corrected SETREG).

**Readers:** `execute` (via `seq_nx`), `t2_exec`,
`t2_revise_graph` (re-execution after surgery). `t2_sig` reads them
but is never called in production.

**Status:** genuine for revision; unexercised for query. Subject to
the eviction-corruption design flaw (`986c52fdc`): roots are integer
fields, not edges, so `evict_node` cannot see the reference and graph
cells (bid 0) are freed first, leaving zombie MAPs.

**Dead sub-family:** the sum branch. `t2_trial` gates sums on
`comb_present(W)>=0` (L612), which requires a live tag-8 node; no
production code creates tag-8 nodes (only test line 1106 does). The
entire sum family (`t2_asm_sum`, `t2_gather_sum`) is unreachable in
production. Dead code, not a capability.

### 1.5 POLICY_ROOT (node 0, tag 900): the action pointer

**Layout:** field0=900, field36=1, field20=guide-anchor pointer
(`pol_get`/`pol_set`, L913-914), other fields -1/0.

**Readers:** `miss_inquire` (L800: `pol_get`), `ev_act` (L861:
direct `ng(W,0,20)`).

**Writer:** `miss_inquire` (L804): lazy init only. If the pointer is
< 2, allocate the tag-2 anchor and `pol_set` it. The pointer changes
exactly once per lifetime, at the first miss, and never from
experience after that.

**Status:** genuine by the letter (both paths exercised), but the
write is structural bootstrap, not learning. There is no
policy-update path: no success/failure signal ever reaches field20.

### 1.6 Context stack (hdr 32-48): 4-slot subject recency buffer

**Layout:** hdr 32,36,40,44 = 4 slots; hdr 48 = write pointer
(round-robin, wraps at 4).

**Writer:** `ctx_push` (L292), called on every event: `ev_teach`,
`ev_query`, `ev_observe` push s; `ev_act` pushes -3.

**Reader:** `ctx_get` (L294), used by `ev_act` for guide context
matching.

**Status:** genuine. Limits: 4 slots, raw subject integers, no
structure, overwritten round-robin, no salience weighting. A guide
matches iff its missed subject is among the last 4 event subjects
(or -3, which never equals a guide's field4=s... note `ev_act`
pushes -3 AFTER reading, so the -3 is for the next act call's
context; guides never have field4=-3, so the -3 slot never matches a
guide; it only dilutes the buffer).

### 1.7 Clock and counters

| Header | Written by | Read by | Decision use |
|--------|-----------|---------|--------------|
| 0 (clock) | ev_teach, ev_query, ev_observe, ev_act (+1) | write_node d-field, log_ev, rec_evict | none: timestamps are stored, never compared |
| 4 (PRO TTL=12) | init only | link_edge PRO creation, ref_prot | constant, not learner state |
| 8 (evict ptr) | evict_node (round-robin) | evict_node | genuine: eviction scan order |
| 20 (node count) | alloc_node, evict_node | alloc/evict bookkeeping only | none |
| 24 (edge count) | link_edge, evict_node, decay, t2_kill_edge | MAP field24 (promo index) | dead end: only consumer is map_standing, never called |

The clock is a timestamp source without temporal reasoning: nothing
compares two clocks, computes an age, or conditions a decision on
recency except implicitly through slot indices and the context
buffer. "Recency" effects in TNN-2 come from allocation order and
the context stack, not from the clock.

## 2. Edge-type census (13 types)

**Genuine (production read + exercised production write):**

| Type | Name | Writers | Readers | Role |
|------|------|---------|---------|------|
| 1 | DEP | promote, asm_chain/count, revise, miss_inquire | bid, t2_revise_graph | evidence; revision provenance walk |
| 2 | SUP | promote, bootstrap | bid | birth bid (MAP); evidence (facts) |
| 3 | CON | ev_observe, revise | bid (subtracted), is_superseded | contradiction / supersession |
| 6 | USE | ev_query hit, ev_act select, promote, bootstrap | bid | use evidence (facts); incumbency (guides); birth lie (MAPs) |
| 7 | CFM | ev_observe match | bid | confirmation evidence |
| 9 | PRO | ev_teach, ev_teach_in, k_get | is_prot, decay, ref_prot | eviction protection with TTL |
| 10 | MEM | miss_inquire (anchor to guide) | bid (inherited evidence) | guide linkage; inherits ~0 |
| 12 | SEQ | seq_link (graph cells) | seq_nx, execute | execution chaining |

**Write-only (no production readers):**

| Type | Name | Writers | Note |
|------|------|---------|------|
| 4 | REF | ev_observe L853 (new fact to contradicted fact) | orphan link; nothing traverses it |
| 5 | INS | ev_teach L307 (fact chain); ev_observe L850 (history link) | insertion order; unread |
| 8 | SUR | ev_query L825 (recent fact on miss) | "surprise" mark; unread |
| 13 | COR | promote_graph L537; bootstrap_miss L780 (MAP self) | corroboration self-edge; unread |

**Unused:** type 11 (REG): zero writers, zero readers. Vestigial.

5 of 13 edge types are dead weight: 4 write-only, 1 entirely unused.
The "one system" carries 8 live relation types.

**Additional write-only node site (not in the 6 theater instances):**
`ev_observe` L847-851 creates a T_HIST node via `alloc_raw` on every
contradiction and links it with INS to the contradicted fact. No
production reader. Same classification as T6 (write-only history),
second creation site. Noted here for completeness; the audit's T6
covered the `rec_evict` chain (hdr 12).

## 3. Interaction map (data flows per event)

**ev_teach(s,r,o):** clock++ ; decay (PRO countdown, may free edges)
; ctx_push(s) ; alloc FACT ; PRO self-edge (TTL 12) ; INS edge to
previous fact (write-only) ; log (theater). No retrieval, no
verification, no revision trigger.

**ev_query(s,r,expected,flags):** clock++ ; decay ; ctx_push(s) ;
`activate` = max-bid exact (s,r) FACT, skipping superseded. On hit:
USE self-edge on the fact, `ref_prot` (PRO refresh), return field28.
On miss: SUR self-edge on highest-index fact (write-only) ;
`mp_run` = `t2_trial`: `t2_gather` BFS over FACTs, assemble chain
graphs (k=2..4), then single-hop; `t2_try_verify` each against
expected (unmasked) or executability (masked); first verified answer
promotes (MAP + shadow FACT) and returns. Trial stats to hdr 16
(theater). On trial failure: `bootstrap_miss`: reverse scan FACTs by
r, unanimity check, k=3 gate (read-only), on pass create bootstrap
MAP + teach own guess as FACT. On bootstrap failure:
`miss_inquire`: UNCERT node (theater fields), guide node, MEM link
from anchor (lazy anchor creation on first miss); return -2.

**ev_observe(s,r,o):** clock++ ; decay ; ctx_push(s) ; `activate`.
No fact: `ev_teach_in`, return 1. Match (field28==o): CFM
self-edge, `ref_prot`, return 1. Contradiction: CON self-edge on the
fact ; `revise_on_contradict`: DEP-edge walk to licensing MAPs,
`t2_revise_graph` per MAP (find stale SETREG via provenance,
tombstone it, insert corrected SETREG with new_o literal, rewire,
re-execute; on `out==-999999` revert and return 0, discarding the
return at L699; on success CON the old answer fact, teach `out` as
FACT, retarget MAP field28 to `out`; note the V2 hole: `out==new_o`
never checked) ; T_HIST node (write-only) ; `ev_teach_in(W,s,r,o)` ;
REF edge new to old (write-only) ; return 0.

**ev_act():** clock++ ; decay ; ctx_push(-3) ; read POLICY_ROOT ;
traverse incident edges for candidates ; keep live, non-superseded
nodes whose field4 matches a context slot ; max-bid ; USE self-edge
on winner ; return field20. With no anchor (pr<2): return 0.

**Eviction (inside alloc_node when full):** round-robin scan from
hdr 8 for min-bid unprotected node ; `rec_evict` (T6 theater) ;
free node ; delete incident edges (field references like MAP roots
invisible: the corruption flaw) ; advance pointer.

## 4. Capability boundary of the genuine state

**Supported:**
- Store and retrieve (s,r,o) triples with evidence-weighted ranking.
- Protect recently used or confirmed facts from eviction (PRO/TTL +
  ref_prot on hit/match).
- Demote contradicted facts (CON self-edge; excluded from activate).
- Assemble executable graphs from FACTs on a miss (trial), promote
  the verified one (MAP + shadow FACT).
- Retain promoted procedures with provenance for later revision
  (MAP + DEP edges).
- Surgically revise a procedure after a counterexample
  (t2_revise_graph; subject to the confirmed V2 hole).
- Select among context-matching guides with weak incumbency
  (ev_act + USE self-edge).

**Not supported (no machinery in genuine state):**
- Learning from experience: no outcome of any event modifies a
  future decision except PRO refresh and guide USE incumbency. Trial
  order is source-fixed; k=3 is read-only; POLICY_ROOT is
  write-once; no failure counters exist.
- Source distinction: 5 writers, 1 tag; bootstrap counts its own
  guesses as observations (circular confidence loop candidate).
- Withholding, abandonment, principled forgetting: no decline gate,
  no attempt counters, no retirement path.
- Query-time procedure execution: MAP graphs never execute on the
  query path; the shadow FACT always answers first.
- Utility-reflecting bid for procedures: MAP bid is fixed at birth.
- Temporal reasoning: the clock is write-only as a decision input.

## 5. Gaps for one-system coherence

Ranked by how directly each blocks the "one continuing learner"
target. None is an implementation proposal; each names the missing
machinery.

1. **No consequence re-entry.** The three-stops synthesis
   (`48cb843e5`): outcomes of the system's activity do not re-enter
   its future decisions. The genuine state has exactly two
   consequence channels (PRO refresh on hit/match; USE incumbency on
   guide selection), both local and ungraded. Everything else flows
   forward and is discarded.
2. **No failure memory.** 7 signals inventoried (`d3e896c8c`), 5
   discard mechanisms, zero counters. Upstream of decline,
   abandonment, and forgetting.
3. **No source provenance.** Load-bearing conflation (`8744796fb`):
   `activate`, `bootstrap_miss`, and the shadow mechanism function
   because they do not distinguish taught from observed from
   self-generated facts. Separation needs provenance storage plus
   per-consumer source policies.
4. **No query-time execution.** The procedure half of learner state
   is inert when answering. Unification (duality analysis
   `6fa7dd2ec`) requires an execute-vs-cache decision with freshness
   and confidence signals that do not exist.
5. **No utility signal for structures.** Bid counts edges; MAP bid is
   a birth certificate (`1538eeefe`). Per-structure utility,
   execution feedback, and correctness-distinct-from-execution are
   all absent.
6. **Write-once policy substrate.** POLICY_ROOT field20 is set at the
   first miss and never revised. The guide/anchor/MEM/bid machinery
   exists but has no update rule driven by outcomes.
7. **Vestigial edge types and dead code.** Types 4, 5, 8, 13 are
   write-only; type 11 is unused; the sum family is unreachable;
   `map_standing`, `contradict_map`, `t2_sig` are never called in
   production. Roughly a third of the relation vocabulary and one
   trial family are dead weight in a system whose doctrine is
   architectural compression.
8. **Context is 4 raw integers.** Guide matching is subject equality
   against a 4-slot recency buffer. No abstraction, no salience, no
   structure; the -3 act-marker slot can never match a guide.
9. **Clock without comparison.** Timestamps are stored on every fact
   and never compared. All recency effects come from allocation
   order and the context buffer instead.

## 6. Standing architectural metrics (genuine-state basis)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: all of them (0 learner-owned;
  consistent with DOF map `d2af26581` and criterion mechanism
  `8a2ff4b77`).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (T1/T2/T5 excluded as
  theater; the remaining genuine writes are researcher-shaped:
  trial assembly order, revision topology, eviction rule).
- SOURCE-ENUMERABLE FORMS: all (node types, edge types, trial
  families, revision topology all fixed in source).
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0 (cross-domain transfer experiment `cbd7bc803`).
- REVISION EVENTS: supported mechanically (`880c87c4c`), always
  researcher-topology.
- COGNITION LINES: ~918 (lines 1-918); test battery excluded.
- MODES: 0. BRIDGES: 0. HANDLERS: 4 event handlers
  (ev_teach/ev_query/ev_observe/ev_act), all harness-called, zero
  internal callers (goal origination `3bf4d7bb4`).
- SEMANTIC CASES: 0 new (4-op ISA only).

## 7. Method

Systematic read of frozen `tnn2.zag` lines 1-918 (cognition region).
Every node-creation site, every `link_edge` call, every header
access, and every edge-type predicate enumerated; callers of each
accessor classified as production vs test (lines 920+). Cross-checked
against: theater audit `e0423538a`, bid semantics `1538eeefe`,
teach-observe `8744796fb`, execute-cache `7186294cd`, minus-two
`ede1060a5`, eviction corruption `986c52fdc`, white-box inventory
`b17fee225`, goal origination `3bf4d7bb4`. New findings beyond prior
work: guide tag correction (tag 1, not tag 2), sum-family
unreachability (no tag-8 nodes in production), COR/REF/SUR/INS
write-only classification, REG entirely unused, second
write-only history site in ev_observe, node/edge-count bookkeeping
dead-ends, clock never compared.

**Verdict: GENUINE-STATE-COMPLETE.**
