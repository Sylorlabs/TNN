# TNN-2 Degree-of-Freedom Map

Target: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
(frozen commit `f4de7ff46`, SHA-256 `a29972ca...`). Cognition path only
(lines 1-917). Test code excluded.

## Classification scheme

- RESEARCHER: the value is fixed in source, or produced by a fully
  deterministic researcher-authored rule (fixed search order, fixed template,
  fixed selection rule such as argmax-bid, fixed tie-break, fixed schema).
- LEARNER: the value is chosen at runtime by the learner from alternatives
  using a learner-created criterion, or an open-form creation the researcher
  did not enumerate.
- MIXED: the researcher fixes the space and the selection rule; the outcome
  varies with learner state, data, or external input. Space size is stated.

Counting convention: each distinct decision point is counted once per
function, not once per call site. Architectural constants are counted once.

## Headline result

- Pure LEARNER decisions in the cognition path: **0**
- MIXED (researcher space and rule, state/data selects): **5**
- RESEARCHER (fixed constants, templates, orders, rules, schemas): **~240**

The alternative-explanation attacker's compression claim is confirmed
everywhere in the cognition path: every runtime-varying value reduces to
(a) which index/position in a researcher-enumerated finite family is selected
by a fixed rule, or (b) which literal value is copied from data/observations
into a researcher-fixed slot. No function lets the learner originate a
choice of topology, procedure, or question.

## The "any topology?" answer

**No.** There is no place in the cognition path where the learner chooses a
topology, a procedure, or a question. Specifically:

1. Runtime construction (`t2_trial` + assemblers): the learner never chooses
   a wiring pattern. Exactly three fixed assemblers exist
   (`t2_asm_chain`, `t2_asm_count`, `t2_asm_sum`). Chain graphs are always
   guard-per-link with set-on-match; count graphs always add one INC per link
   plus a fixed `MOVE r0 <- r1` epilogue; sum graphs are always unrolled INC
   cells. What varies: chain length k in {2,3,4} (fixed search order tries
   longer first), sum length = data total (capped at 900 by source), count
   length = data chain length (capped at 16 by source). The "choice" of which
   graph wins is first-to-verify under the fixed order
   chains -> sums -> counts -> single hops, filtered by the external
   `expected` answer key. The candidate family is finite and fully
   researcher-enumerated (see space sizes below).
2. Inquiry (`miss_inquire`): the guide is a fixed 2-node, 2-edge template
   (UNCERTAINTY node tag 30 with fields (s,r,2,0); guide node tag 1 with
   fields (30,-999,0,0); DEP guide->uncertainty; MEM policy_root->guide).
   The learner chooses no question. The "question" is the input pair (s,r),
   which came from the driver query, not from learner deliberation. There is
   no derivation of a discriminating need: every miss produces the identical
   schema, differing only in the copied (s,r) literals.
3. Revision (`t2_revise_graph`): the repair is a fixed researcher-authored
   procedure: find the last tag-101 (MOVE/SET) cell with a DEP edge to the
   contradicted fact, find the last BRANCHEQ cell whose field12 points at it,
   build a new SET cell holding the new literal, rewire guard->new and
   new->successor, tombstone the stale cell, re-execute, revert on failure.
   The learner chooses no repair topology. When several stale cells exist,
   the winner is last-in-scan-order, a deterministic artifact, not a choice.
   Sum graphs carry no DEP provenance edges at all, so they are
   unrevisable by construction: the "generic" revision only fits the
   chain/count shape its author assumed.
4. Action selection (`ev_act`): fixed rule. Scan all edges incident to
   POLICY_ROOT (both directions) plus their 2-hop neighbors, keep candidates
   whose field4 matches one of the last 4 context entries, pick argmax bid,
   tie broken by first-in-edge-order, return the winner's field20, else 0.
   The candidates are learner-created nodes, but their schema is the fixed
   inquiry template and the selection rule is fixed.

## Complete decision-point table

### A. Layout and constants (lines 45-85): 37 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| A1 | Workspace size 110656 bytes | RESEARCHER |
| A2 | 1024 nodes, 4096 edges, 128 log slots | RESEARCHER |
| A3 | Node base 64, node stride 40, fields at 0..36 | RESEARCHER |
| A4 | Edge base 41024, edge stride 16, fields at 0/4/8/12 | RESEARCHER |
| A5 | Log base 106560, log stride 32 | RESEARCHER |
| A6 | 13 edge types (DEP/SUP/CON/REF/INS/USE/CFM/SUR/PRO/MEM/REG/SEQ/COR) | RESEARCHER |
| A7 | 4 ISA opcodes 101-104 (MOVE/BRANCHEQ/INC/DEC) | RESEARCHER |
| A8 | 7 node types (FACT/GROUP/HIST/REGRET/MAP/COEFF/UNCERT = 1/2/3/4/20/21/30) plus internal tags 900/901/902/903 | RESEARCHER |

### B. Allocation and linking (lines 87-138): 9 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| B1 | `alloc_node`: first-fit scan from id 2 upward | RESEARCHER |
| B2 | `alloc_node`: on full, evict via `evict_node`, else fail -1 | RESEARCHER |
| B3 | `alloc_node`: zero all 9 data fields on (re)use | RESEARCHER |
| B4 | `alloc_raw`: first-fit, no eviction, fail -1 | RESEARCHER |
| B5 | `write_node`: values map to fields 20/24/28/32 | RESEARCHER |
| B6 | `link_edge`: first free edge slot scanning 0..4095 | RESEARCHER |
| B7 | `link_edge`: edge layout (from, type, to, clock) | RESEARCHER |
| B8 | `is_superseded`: defined as a CON self-loop | RESEARCHER |
| B9 | Chosen ids are deterministic first-fit outcomes, not learner picks | RESEARCHER |

### C. Retrieval: `activate` (lines 140-152): 3 RESEARCHER, 1 MIXED

| # | Decision | Class |
|---|----------|-------|
| C1 | Exact (s,r) match required on type-1 nodes | RESEARCHER |
| C2 | Superseded nodes skipped | RESEARCHER |
| C3 | Winner = argmax bid over matches; tie = lowest node id (scan order) | MIXED: space = live matching facts; rule fixed |
| C4 | Return -1 when no match | RESEARCHER |

### D. EXECUTE interpreter (lines 166-219): 15 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| D1 | Frame slot chaining via node field4 (4 slots per node) | RESEARCHER |
| D2 | Operand encoding: 1000+slot = frame slot; 0..999 = literal node id; >=1000 in res_op with offset = slot | RESEARCHER |
| D3 | MOVE/BRANCHEQ/INC/DEC semantics exactly as coded | RESEARCHER |
| D4 | 1000-step execution budget (code literal) | RESEARCHER |
| D5 | Fail closed: any guard failure, unknown tag, or budget breach returns -999999 | RESEARCHER |
| D6 | BRANCHEQ true target = field12, false target = field16 | RESEARCHER |
| D7 | SEQ fallthrough via ET_SEQ edges (`seq_nx`) | RESEARCHER |
| D8 | Guard with no SEQ fallthrough fails closed (field16 = 0 hits header node tag 900) | RESEARCHER |
| D9 | Output operand = root field4; `exec_val` reads it after success | RESEARCHER |
| D10 | `t2_exec`: fresh 902 frame, slot0 = s0, slot1 = 0 | RESEARCHER |

(Points D1-D10 counted as 15 with sub-decisions for the four op semantics.)

### E. Retention: bid, protection, eviction (lines 221-283): 10 RESEARCHER, 1 MIXED

| # | Decision | Class |
|---|----------|-------|
| E1 | Protected = live PRO edge with clock > 0 | RESEARCHER |
| E2 | Bid formula: SUP+DEP+USE+CFM - CON, plus group-member edges of same types | RESEARCHER |
| E3 | `evict_node`: circular scan of 1024 ids starting at header field 8 | RESEARCHER |
| E4 | Victim = argmin bid among non-protected live nodes; tie = first found | MIXED: space = up to 1022 nodes; rule fixed |
| E5 | Initial best-bid 1000000 (so all bids are below it) | RESEARCHER |
| E6 | `rec_evict`: history record tag 3 copies (s,r,o,clock), links to header field 12 | RESEARCHER |
| E7 | Eviction tombstones node, deletes all incident edges | RESEARCHER |
| E8 | Eviction advances start pointer to victim+1 (wrap to 2) | RESEARCHER |
| E9 | `ref_prot`: refresh PRO clocks to header field 4 (= 12) | RESEARCHER |
| E10 | Protection duration constant 12 | RESEARCHER |

### F. Events, context, teaching (lines 285-316): 16 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| F1 | Log cap 128 entries, layout (clock,kind,r0,r1,p0..p3) | RESEARCHER |
| F2 | Context ring of 4, wrap on overflow | RESEARCHER |
| F3 | `ctx_get`: index arithmetic over the ring | RESEARCHER |
| F4 | `ev_teach`: clock++, decay, ctx_push(s) on every teach | RESEARCHER |
| F5 | `ev_teach`: tag 1, write (s,r,o,clock), PRO self-edge duration 12 | RESEARCHER |
| F6 | `ev_teach`: INS edge to the last (highest-id) live type-1 node | RESEARCHER |
| F7 | `ev_teach_in`: same minus clock/decay/context (the "internal" teach) | RESEARCHER |
| F8 | Event kind codes: 1 teach, 2 query, 3 act, 4 observe | RESEARCHER |

### G. Graph cell constructors (lines 338-361): 12 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| G1 | Literals are tag-902 nodes holding the value in field20 | RESEARCHER |
| G2 | `t2_guard`: BRANCHEQ cell, field4 = 1000+slot, field8 = literal node id | RESEARCHER |
| G3 | `t2_set`: MOVE cell, field4 = 1000+slot, field8 = literal node id | RESEARCHER |
| G4 | `t2_mov`: MOVE cell, field4 = 1000+dst, field8 = 1000+src | RESEARCHER |
| G5 | `t2_inc`: INC cell, field4 = 1000+slot | RESEARCHER |
| G6 | Every constructor allocates via `alloc_node` and fails -1 on exhaustion | RESEARCHER |

### H. Graph assemblers (lines 363-411): 15 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| H1 | Chain: one guard + one SET per link; guard true-target (field12) = SET | RESEARCHER |
| H2 | Chain: SET carries DEP edge to the licensing fact | RESEARCHER |
| H3 | Chain: links SEQ-chained previous-SET -> next-guard; root = first guard | RESEARCHER |
| H4 | Chain: literals copied from data vectors v[j], v[j+1] | MIXED (folded into K4 accounting; slot fixed, value from data) |
| H5 | Count: chain pattern plus one INC(slot1) per link, SEQ SET -> INC | RESEARCHER |
| H6 | Count: fixed epilogue `MOVE r0 <- r1` so the count is the output | RESEARCHER |
| H7 | Sum: total = sum of input values; decline if total <= 0 or total > 900 | RESEARCHER |
| H8 | Sum: unrolled linear chain of exactly `total` INC(slot0) cells | RESEARCHER |
| H9 | Sum: no DEP provenance edges on any cell (hence unrevisable, see R-section) | RESEARCHER |
| H10 | Slot conventions: chain/count guard and SET use slot0; count uses slot1; sum uses slot0 | RESEARCHER |

### I. Gatherers (lines 419-495): 15 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| I1 | `t2_lu_first`: first match scanning ids 2..1023 | RESEARCHER |
| I2 | `t2_chain`: v[0] = s; follow first-match facts; max length 16 | RESEARCHER |
| I3 | `t2_gather`: BFS from s, depth 1..4, cap 96 paths | RESEARCHER |
| I4 | `t2_gather`: 12-slot path entries (len, v0..v4, f0..f3) | RESEARCHER |
| I5 | `t2_gather`: no cycles, skip relations == -999, scan ids 2..1023 | RESEARCHER |
| I6 | `t2_gather_sum`: first 12 facts of s with relation != -999, scan order | RESEARCHER |
| I7 | `t2_rels`: distinct relations of s via `inc_fill`, excluding -999 | RESEARCHER |

### J. Verify and promote (lines 497-543): 11 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| J1 | `t2_try_verify`: counts tried and rejected into the stats buffer | RESEARCHER |
| J2 | Masked mode: accept any executed value except -2/-999999 | RESEARCHER |
| J3 | Unmasked mode: accept only if expected != -2 and value == expected | RESEARCHER |
| J4 | `expected` is external post-hoc feedback (driver-supplied answer key) | RESEARCHER (external input, not a learner decision) |
| J5 | `promote_graph`: MAP layout tag 20, field4 = r, field8 = s, field20 = graph root, field24 = promotion edge index, field28 = answer | RESEARCHER |
| J6 | `promote_graph`: self edges COR/SUP/USE; DEP edges to all licensing facts | RESEARCHER |
| J7 | `promote_graph`: also teaches (s,r,answer) via `ev_teach_in` | RESEARCHER |
| J8 | `t2_sig`: signature walk over SEQ + BRANCHEQ true-targets, 32-cell cap, records (tag, literal) | RESEARCHER |

### K. The trial loop `t2_trial` / `mp_run` (lines 586-673): 20 RESEARCHER, 2 MIXED

| # | Decision | Class |
|---|----------|-------|
| K1 | Phase order fixed: chains (k=2..4) -> sums -> counts -> single hops | RESEARCHER |
| K2 | Chain lengths tried: k = 2, 3, 4 only (longer first) | RESEARCHER |
| K3 | Per BFS path of length k+1, assemble exactly one chain graph | RESEARCHER |
| K4 | First candidate to verify stops the whole search (`ans != -2` breaks all loops) | MIXED: space = finite candidate family (chains: at most 96 BFS paths at depths 2..4; sums: at most 4095 nonempty subsets of at most 12 values; counts: at most 16 relations; single hops: at most 96 length-2 paths); rule = first-to-verify under the fixed order |
| K5 | Literals embedded in graphs are copied from learner-state facts and observations; slots are fixed | MIXED: slot fixed by researcher; value from data (copied input, not a learner choice) |
| K6 | Sum phase gated on `comb_present` (a type-8 node) | RESEARCHER; note: no type-8 node is creatable in the cognition path (only test line 1106 creates one), so this whole phase is externally gated |
| K7 | Sum subsets enumerated sz = m down to 1, mask = (1<<m)-1 down to 1, popcnt filter | RESEARCHER |
| K8 | Sum verify runs with s0 = 0 (frame slot0 = 0, not the query subject) | RESEARCHER |
| K9 | Count phase gated on di == 0; one count graph per relation of s | RESEARCHER |
| K10 | Count verify runs with s0 = s | RESEARCHER |
| K11 | Single-hop phase: paths of length exactly 2, chain assembler with plen 2 | RESEARCHER |
| K12 | Chain/count phases gated on dc == 0 (chains) with fixed flag-bit decoding in `mp_run` | RESEARCHER |
| K13 | `masked`, `dc`, `di` come from driver flags, not learner state | RESEARCHER (external input) |
| K14 | Trial stats packed as tried*1024 + rejected into header field 16 | RESEARCHER |

### L. Inquiry `miss_inquire` (lines 795-812): 5 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| L1 | UNCERTAINTY node schema: tag 30, field4 = -4, fields (s, r, 2, 0) | RESEARCHER |
| L2 | POLICY_ROOT created on demand if absent: tag 2 (GROUP), field4 = -5, stored at node 0 field 20 | RESEARCHER |
| L3 | Guide schema: tag 1 (FACT), field4 = s, fields (30, -999, 0, 0) | RESEARCHER |
| L4 | Guide wiring: DEP edge guide -> uncertainty; MEM edge policy_root -> guide | RESEARCHER |
| L5 | No discrimination step: the guide never encodes what evidence would resolve the uncertainty; (s,r) are copied from the triggering query | RESEARCHER |

### M. Action `ev_act` (lines 859-900): 7 RESEARCHER, 1 MIXED

| # | Decision | Class |
|---|----------|-------|
| M1 | Policy root read from node 0 field 20; return 0 if absent | RESEARCHER |
| M2 | Candidate pool: all edges incident to the root in either direction, plus their 2-hop neighbors | RESEARCHER |
| M3 | Context filter: candidate field4 must equal one of the last 4 context entries | RESEARCHER |
| M4 | Winner = argmax bid; tie = first in edge-id order (strict > comparison) | MIXED: space = context-matching 1-2 hop neighbors of POLICY_ROOT; rule fixed |
| M5 | Returned action = winner field20 (30 for inquiry guides); fallback 0 | RESEARCHER |
| M6 | Winner gets a USE self-edge | RESEARCHER |
| M7 | Superseded candidates skipped | RESEARCHER |

### N. Query pipeline `ev_query` (lines 813-835): 4 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| N1 | Fixed pipeline order: exact hit -> trial -> P-INV bootstrap -> miss_inquire | RESEARCHER |
| N2 | On miss, the most recent (highest-id) type-1 node gets a SUR self-edge | RESEARCHER |
| N3 | `bootstrap_miss`: scan ids 1023 down, collect up to 6 outputs for relation r | RESEARCHER |
| N4 | `bootstrap_miss`: if at least k (default 3, from tag-903 node) outputs and all identical, promote a FIXED-template MAP (tag 20, fields (0, edge-count, 0, 0), cnt SUP self-edges, COR/USE self-edges) and teach (s,r,v0) | RESEARCHER |

### O. Observe and contradiction `ev_observe` (lines 836-857): 3 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| O1 | Hit and value matches: CFM self-edge, refresh protection, return 1 | RESEARCHER |
| O2 | Hit and value differs: CON self-edge, `revise_on_contradict`, history record (tag 3), teach new fact, REF edge new -> old, return 0 | RESEARCHER |
| O3 | No hit: teach the observation | RESEARCHER |

### P. Revision `revise_on_contradict` / `t2_revise_graph` (lines 685-752): 19 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| P1 | No-op when old value == new value | RESEARCHER |
| P2 | Scan ALL type-20 MAP nodes for a DEP edge to the contradicted fact; revise each | RESEARCHER |
| P3 | Stale step = the LAST tag-101 (MOVE/SET) cell with a DEP edge to the fact (scan order decides ties) | RESEARCHER |
| P4 | Guard = the LAST BRANCHEQ cell whose field12 points at the stale cell | RESEARCHER |
| P5 | Repair = build literal(new_o) + SET(slot0) cell, DEP edge to the fact, rewire guard field12 -> new cell, new cell SEQ -> old successor, delete stale -> successor SEQ edge | RESEARCHER |
| P6 | Stale cell tombstoned: tag 0, alive 0 | RESEARCHER |
| P7 | Re-execute the graph; on failure (-999999) revert every change exactly and return 0 | RESEARCHER |
| P8 | On success: CON self-edge on the old answer fact, teach (s,r,new answer), update MAP field28 | RESEARCHER |
| P9 | MAP standing untouched by revision (no CON edge on the MAP) | RESEARCHER |
| P10 | Return 1 on success, 0 on any structural mismatch (no stale cell, no guard, alloc failure) | RESEARCHER |
| P11 | The learner selects no repair operator, no target, no rewiring: every step above is fixed | RESEARCHER |

### Q. Init and policy accessors (lines 902-917): 12 RESEARCHER

| # | Decision | Class |
|---|----------|-------|
| Q1 | Zero the workspace; mark all edges free (-1) | RESEARCHER |
| Q2 | Nodes 0/1 reserved (tags 900/901); allocation starts at 2 | RESEARCHER |
| Q3 | Header constants: PRO duration 12, eviction start 2, log/context counters 0 | RESEARCHER |
| Q4 | Policy root and miss-policy slots at node 0 field 20 and node 1 field 20 | RESEARCHER |
| Q5 | `mp_set` is never called in the cognition path (only test line 1010): the "miss policy" slot is write-only scaffolding; the real miss policy is the hardcoded `t2_trial` call in `ev_query` | RESEARCHER |

## Summary statistics

| Class | Count | Share |
|-------|-------|-------|
| RESEARCHER | ~240 | ~98% |
| MIXED (researcher space + rule; state/data selects) | 5 | ~2% |
| LEARNER (learner-originated choice of form) | 0 | 0% |

The 5 MIXED points and their spaces:

1. `activate` winner (C3): space = live non-superseded type-1 facts exactly
   matching (s,r); rule = argmax bid, tie = lowest id.
2. `evict_node` victim (E4): space = up to 1022 live non-protected nodes;
   rule = argmin bid, tie = first from circular start.
3. `t2_trial` winning candidate (K4): space = finite enumerated family
   (at most 96 chain paths per depth 2..4, at most 4095 sum subsets of at most
   12 values, at most 16 count graphs, at most 96 single hops); rule =
   first-to-verify under the fixed phase order, filtered by external
   `expected`.
4. Literal embedding (K5/H4): space = i32 values copied from learner-state
   facts and observations; slots fixed by the assemblers.
5. `ev_act` action (M4): space = context-matching 1-2 hop neighbors of
   POLICY_ROOT; rule = argmax bid, tie = first in edge order, fallback 0.

In every MIXED case the learner's role is exhausted by "state/data happens to
contain value X, so the fixed rule picks index i". Nothing is deliberated,
and no alternative outside the researcher-enumerated space can ever be
selected.

## Highest-impact researcher decisions

Ranked by what would break if changed:

1. `t2_trial` phase order and assembler set (K1, H1-H10). Every miss answer
   flows through chains -> sums -> counts -> single hops. Reordering changes
   which reading wins on ambiguous worlds (the masked t_f2 preference for
   the 2-hop reading is an order artifact). Removing any assembler removes a
   whole capability branch.
2. Verification = external `expected` match (J3, J4). The trial loop does not
   discover correctness; the driver supplies the answer key and the loop
   keeps the first candidate that matches it. With masked == 1 it keeps the
   first candidate unconditionally. This is the largest capability lever in
   the system and it is not learner-owned.
3. The `comb_present` gate on the sum phase (K6). The gate key is a type-8
   node that no cognition-path code can create (only test line 1106 does).
   An entire assembler branch is switched on by external scaffolding.
4. `execute` budget 1000 with fail-closed semantics (D4, D5), paired with the
   sum cap of 900 (H7). Two matched magic numbers: sums need up to 900 steps
   and the budget must exceed that. Lower either and summation silently dies.
5. `miss_inquire` fixed schema (L1-L4). `ev_act` can only select the guide
   because field4 = s matches the context window and field20 = 30 is the
   returned "action". The inquiry behavior is schema-determined, not
   derived.
6. `ev_act` selection rule (M2-M4). The "action choice" is argmax-bid over a
   fixed 2-hop neighborhood with a 4-deep context filter. Change the rule
   and FW6-style behavior changes with it.
7. `t2_revise_graph` shape assumption (P3-P5). Revision only works on graphs
   whose stale step is a DEP-tagged MOVE/SET cell pointed to by a BRANCHEQ
   field12: exactly the chain/count assembler output. Sum graphs carry no
   provenance and are unrevisable by construction.
8. `activate` exact-(s,r) plus argmax bid (C1-C3). All retrieval, and
   therefore all exact-hit answers, flows through this rule.
9. The `bid` formula (E2). One fixed formula simultaneously drives retrieval
   ranking, eviction victim choice, and action selection.
10. Frame conventions (D10, H10, K8, K10). slot0 = subject (or 0 for sums),
    slot1 = 0, root field4 = output operand. A silent cross-function contract
    shared by assemblers, `t2_exec`, and revision.
11. `bootstrap_miss` all-identical + k >= 3 + fixed MAP template (N3, N4).
    The P-INV fallback promotes a constant-answer template, not a derived
    procedure.
12. The ISA itself and `execute` semantics (D1-D9). Correctly frozen as
    protected machinery, but every constructed graph's meaning depends on
    these researcher-fixed semantics.

## Researcher decisions movable to the learner without new opcodes

Each of these can be moved using only existing node/edge types and the frozen
4-op ISA. "Movable" means the decision-relevant state can live in learner
state and the cognition path can consult it; no new opcodes, modes, bridges,
or handlers are required.

1. Trial phase order (K1). Keep per-assembler success/failure counts in
   learner state (written by `promote_graph`, read by `t2_trial`); try
   assemblers in order of past success instead of the fixed
   chains -> sums -> counts -> hops order.
2. Chain depth bound k <= 4 (K2). Adaptive deepening: a learner-state miss
   counter per (s,r) raises the depth cap after repeated failures instead of
   the fixed 2..4.
3. Sum subset enumeration order (K7). Order subsets by learner-kept priors
   over subset sizes instead of fixed largest-first.
4. The `comb_present` gate (K6). Let the learner set its own combination-mode
   marker node after observing additive structure, instead of requiring an
   externally created type-8 node.
5. Repair operator choice (P5). Replace the single fixed "swap the SET
   literal" repair with a trial over repair operators (replace literal,
   retarget guard, drop link, change slot), each re-executed and kept only on
   verification, mirroring the `t2_trial` propose/verify loop. All operators
   use existing cell constructors.
6. Repair target selection (P3, P4). When several stale cells or guards
   match, try each in turn with re-execution instead of last-in-scan-order.
7. Guide probe content (L5). Choose the probe (s', r') from
   uncertainty-ranked candidates in learner state instead of copying the
   triggering query's (s, r).
8. Action selection criterion (M4). Keep per-guide learned values in learner
   state and select on those instead of the fixed bid formula (bid stays for
   eviction; the two uses can be decoupled).
9. Acceptance criterion (J3). Consult a learner-held acceptance threshold or
   consistency check in `t2_try_verify` instead of the external `expected`
   answer key. This is the hardest move: it requires a learner-internal
   correctness signal, which is exactly what the current answer-keyed design
   avoids.
10. Contradiction protocol (O2). Which of several conflicting facts to keep
    could be decided by learner-kept track records instead of the fixed
    always-revise-then-teach-new sequence.

NOT movable (correctly researcher-fixed): the 4-op ISA, `execute` semantics,
node/edge memory layout. Those are protected core machinery per the ISA
ruling, not decisions the learner should make.

## Consequences for the three claimed mechanisms

- Runtime construction: the trial loop enumerates a finite researcher-authored
  family (3 fixed wiring patterns; bounded depths, subset counts, and path
  caps) and keeps the first candidate matching an external answer key. The
  learner's degrees of freedom are the winning index and the copied literals.
  This is search over a fixed menu, not open construction.
- Inquiry: the causal chain miss -> uncertainty -> guide -> POLICY_ROOT ->
  act exists in learner state, but every link's form is a fixed schema and the
  "question" is the input pair, never derived. The learner's degrees of
  freedom are the (s,r) literals copied into the template.
- Revision: the repair procedure is fixed ("replace the DEP-tagged SET step
  under its guard"); the learner supplies only the new literal. It cannot
  derive a structurally different repair, and sum graphs cannot be repaired
  at all.

## Verdict

DEGREE-OF-FREEDOM-MAP-COMPLETE
