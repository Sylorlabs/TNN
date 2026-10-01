# TNN-2 Architectural Compression Audit

**Verdict: COMPRESSION-AUDIT-COMPLETE.** Audit only. No source edits proposed or made.
**Source audited:** `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag` (1591 lines, read-only).
**Date:** 2026-10-01.

## 1. Mechanism inventory

Every distinct cognitive mechanism in frozen TNN-2, its job, and what breaks if removed. Test-harness functions (t_c*, t_a*, t_p*, t_r_pact*, r_*) excluded. Thin infrastructure (getters, setters, constants) excluded.

### A. Execution substrate: ONE engine (already unified, not a candidate)

| Function | Lines | Job | If removed |
|---|---|---|---|
| `execute` | 24 | 4-op ISA interpreter (MOVE/BEQ/INC/DEC) over graph cells | Nothing executable runs; all constructed graphs inert |
| `exec_val` | 5 | execute + return root output slot | No value-returning execution |
| `t2_exec` | 7 | alloc frame, seed s0, call execute | Trial verification and MAP execution lose their entry point (thin adapter, could inline) |
| `res_op`, `seq_nx`, `fr_get`, `fr_set` | 4-6 each | operand resolution, sequence chaining, frame registers | execute cannot address operands |

Assessment: this is the protected-core ISA surface Micah froze. One engine, two thin adapters. No compression needed. `t2_exec` could be folded into callers (3 call sites) but the adapter documents the frame protocol, so keep.

### B. Construction: THREE assemblers + six cell builders

| Function | Lines | Job | If removed |
|---|---|---|---|
| `t2_asm_chain` | 14 | builds guard/set link-chain graph from value path | k-hop chain candidates disappear; FW1/FW2 class fails |
| `t2_asm_count` | 17 | chain template + per-link INC + MOVE epilogue | counting candidates disappear |
| `t2_asm_sum` | 14 | unrolled INC chain totaling a value subset | sum candidates disappear |
| `t2_lit`, `t2_cell`, `t2_guard`, `t2_set`, `t2_mov`, `t2_inc` | 4-5 each | single-cell constructors | assemblers cannot build anything |

`t2_asm_chain` and `t2_asm_count` share ~80 percent of their body (literal pair, guard, set, provenance edge, seq chaining differ only by the INC cell insertion and the epilogue MOVE). `t2_asm_sum` is a degenerate template (pure INC run). Three templates is exactly the enumerated schema the red teams attacked.

### C. Trial and search: ONE 81-line loop + gather helpers

| Function | Lines | Job | If removed |
|---|---|---|---|
| `t2_trial` | 81 | 4-phase candidate search: chains k=2..4, then sums (subset enumeration), then counts (per-relation), then single-hop fallback; each phase assembles, verifies, promotes | No constructive learning; only memory lookup and bootstrap remain |
| `t2_try_verify` | 14 | execute candidate, compare to expected (or accept any on masked), count tried/rejected | Trial loop loses its verification gate |
| `mp_run` | 5 | unpacks flags, calls t2_trial | Nothing (pure adapter; single call site in ev_query) |
| `t2_gather` | 31 | BFS path enumeration from s over FACTs (cycle-checked) | Chain phase has no candidate paths |
| `t2_gather_sum` | 13 | collects values + licensing facts of s direct facts | Sum phase has no candidates |
| `t2_rels` | 11 | lists relations of s via inc_fill | Count phase has no relations |
| `t2_chain` | 14 | per-relation value chain via t2_lu_first | Count phase has no value sequences |
| `t2_lu_first`, `inc_fill`, `comb_present`, `popcnt` | 5-13 each | single-use helpers | Their single caller breaks |

The search ORDER (chains before sums before counts before single-hops) is hardcoded researcher-owned control flow inside t2_trial. The `assemble -> t2_try_verify -> promote_graph` triple repeats 4 times verbatim.

### D. Promotion and standing

| Function | Lines | Job | If removed |
|---|---|---|---|
| `promote_graph` | 12 | allocates MAP node (type 20), writes root/s/r/answer, links provenance (ET_USE) and evidence (ET_DEP/ET_SUP) edges, then shadow-teaches the answer as a FACT | Verified graphs never persist; the C0-D shadow (promotion immediately memoizes a FACT that shadows the MAP) lives here |
| `map_standing` | 10 | counts DEP minus CON edges after promotion | No standing signal (currently unused by any decision; computed but not read) |
| `t2_sig` | 19 | structural signature walk for revision tests | K-H2 Q3 calibration and revision identity checks lose their function |
| `contradict_map` | 2 | links a CON self-edge on a MAP | Callers would inline one link_edge |

`map_standing` is computed nowhere-consumed: a mechanism with no reader. `contradict_map` is a 2-line wrapper around link_edge with 2 call sites.

### E. Inquiry and uncertainty

| Function | Lines | Job | If removed |
|---|---|---|---|
| `miss_inquire` | 18 | on true miss: creates UNCERTAINTY node (type 30), ensures POLICY_ROOT exists, creates guide FACT linked to both | No uncertainty reification; ev_act has nothing to select; inquiry learning disappears |
| `bootstrap_miss` | 26 | P-INV statistical bootstrap: if recent r-values are invariant and count >= k, creates a MAP node AND teaches the value as FACT, returns it | The statistical shortcut path disappears |
| `k_get` | 10 | threshold node (type 903), default 3 | bootstrap_miss loses its invariance threshold |
| `pol_get`/`pol_set` | 1-2 each | POLICY_ROOT pointer on node 0 field 20 | Inquiry policy root unreachable |
| `mp_get`/`mp_set` | 1-2 each | miss-policy pointer on node 1 field 20 | Trial miss policy unreachable |

`bootstrap_miss` does three jobs in one body: statistical test, MAP node creation, FACT teaching. Two parallel policy accessors (`pol_*` on node 0, `mp_*` on node 1) do the same job (named persistent pointer) for different decisions.

### F. Revision

| Function | Lines | Job | If removed |
|---|---|---|---|
| `revise_on_contradict` | 17 | dispatcher: scans MAPs for provenance links to the contradicted fact, calls t2_revise_graph on each hit | Contradictions never reach MAPs; stale graphs persist |
| `t2_revise_graph` | 46 | surgical revision: finds stale SET cell via provenance, tombstones it, inserts corrected SET cell, rewires, re-executes, reverts on verification failure, contradicts old answer fact, teaches new answer | No graph repair; the revision-corruption bug (frame-allocation aliasing, 8b58c4104) lives in the in-place revert path here |
| `t2_kill_edge` | 8 | deletes one edge by (a,type,to) scan | Revision cannot remove stale wiring |

`t2_revise_graph` is the largest single cognitive function and does five jobs: locate, build, verify, commit, revert. The revert path (~15 lines) exists only because mutation is in-place; Micah approved copy-and-commit as the replacement architecture.

### G. Action selection

| Function | Lines | Job | If removed |
|---|---|---|---|
| `ev_act` | 42 | scans POLICY_ROOT-adjacent guides (1-hop) then their neighbors (2-hop), picks max bid among context-matching non-superseded candidates | No learner-driven action; guides accumulate but are never selected |

The 1-hop scan and the 2-hop inner scan contain the same ~10-line block: supersession check, context match over 4 slots, bid computation, max tracking. The block is duplicated, not shared.

### H. Memory

| Function | Lines | Job | If removed |
|---|---|---|---|
| `activate` | 13 | max-bid FACT lookup by (s,r) among live non-superseded facts | ev_query and ev_observe lose exact recall |
| `decay` | 11 | decrements ET_PRO edge clocks, deletes expired | Protection edges never expire; retention policy frozen at leak |
| `evict_node` | 22 | 3-step eviction under the 1024-node budget | Memory grows unboundedly until alloc fails |
| `rec_evict` | 5 | recursive eviction helper | evict_node loses cascade |
| `ref_prot`/`is_prot` | 5-8 each | protection reference counting | Recently used nodes evicted immediately |
| `evcount`/`bid` | 8-12 each | evidence counting, directional bid | activate and ev_act lose their ranking signal |

`activate` (max-bid over FACTs) and `ev_act` (max-bid over guides) are the same selection job over different candidate sets.

### I. Teaching: TWO paths

| Function | Lines | Job | If removed |
|---|---|---|---|
| `ev_teach` | 13 | full teach: clock tick, decay, context push, alloc FACT, chain to previous fact (ET_REF), log event | External observations lose bookkeeping (decay/context/history) |
| `ev_teach_in` | 5 | minimal teach: alloc FACT, self-link, no decay/ctx/log | promote_graph, bootstrap_miss, t2_revise_graph, ev_observe lose their internal teach |

Same core job (create a FACT node), different bookkeeping. Four call sites use the minimal path, one the full path.

### J. Query and observe: the router

| Function | Lines | Job | If removed |
|---|---|---|---|
| `ev_query` | 23 | 4-stage fallback: activate (exact) -> mp_run/t2_trial (construct) -> bootstrap_miss (statistical) -> miss_inquire (uncertainty) | No unified query path; each stage is reachable only here |
| `ev_observe` | 22 | activate; if match, confirm edge; else contradict edge, revise_on_contradict, create T_HIST node, ev_teach_in new answer | Observations cannot confirm, contradict, or revise |

`ev_query` is a router across four subsystems (memory lookup, constructive trial, statistical bootstrap, inquiry). The stage order is researcher-owned. `ev_observe` does four jobs inline (confirm, contradict, history snapshot, teach).

### K. Node types: 3 dead, 1 single-use

| Type | Tag | Uses | Status |
|---|---|---|---|
| T_FACT | 1 | everywhere | live |
| T_GROUP | 2 | 0 (definition only) | DEAD |
| T_HIST | 3 | 1 (ev_observe inline) | single-use |
| T_REGRET | 4 | 0 (definition only) | DEAD |
| T_MAP | 20 | construction/promotion/revision | live |
| T_COEFF | 21 | 0 (definition only) | DEAD |
| T_UNCERT | 30 | inquiry | live |
| 900/901 | init nodes | init | live |
| 902 | frame | t2_exec | live |
| 903 | k-threshold | k_get | live |

## 2. One-System Rule check: bridges, routers, modes

- **Router found:** `ev_query` stages 4 subsystems in a hardcoded fallback chain. This is the clearest router pattern in TNN-2. Each stage has its own admission logic and none knows about the others.
- **No mode flags** in the cognitive path. The `flags` argument to ev_query carries test-harness ablation bits (masked/dc/di), not architecture modes. No CAUSAL_MODE/REVISION_MODE style smell.
- **FACT/MAP duality:** two node types for learned knowledge with different creation paths and, in frozen TNN-2, different query paths (facts via activate; MAPs via nothing, the C0-D finding). The reuse experiment added a MAP-first scan, which is a second lookup path rather than a unified one. This is a duality, not yet a bridge, but it is two representations where the architecture wants one.
- **Two policy stores** (`pol_*` vs `mp_*`): same pointer job, two instances. H3-lite formalizes three policy nodes; the auditor notes the accessor pattern is already duplicated at two.
- **No cross-subsystem bridges** beyond the ev_query router. The subsystems share the node/edge store directly (good: one substrate).

## 3. Compression candidates, ranked by compression ratio

Ranked by mechanisms-removed per capability-preserved. Hypotheses only; no source edits proposed.

### Rank 1: Trial 4-phase loop -> generic candidate-source iterator

- **Removes:** ~40 lines of repeated assemble/verify/promote; the `mp_run` adapter; the hardcoded phase order as control flow.
- **Preserves:** all four candidate families and their verification semantics.
- **Unification hypothesis:** one loop over candidate sources; each source is (gather, assemble) pair; the ORDER becomes data (a policy list) rather than code. This is exactly the policy node H3-lite Node 1 proposes to move into learner state, so compression and learner-authority point the same direction.
- **Risk:** medium. The order encodes the composition-preserving bias (longer chains before sums). Moving it to data is safe only if the default order is preserved and the learner can observe the cost of misordering. The dc/di ablation gates are entangled with the phases; they would need to become per-source attributes.

### Rank 2: FACT/MAP duality -> one knowledge node type with executability

- **Removes:** the type split (1 vs 20), the separate creation paths, the need for two query paths (activate for facts, MAP-scan for procedures). Promotion becomes "attach procedure to knowledge node" rather than "create parallel node plus shadow fact."
- **Preserves:** exact recall and procedure execution, if the executor checks for an attached graph.
- **Unification hypothesis:** a knowledge node holds (s, r, answer); an optional root pointer holds the executable graph. `ev_query` does one lookup, then executes if a graph is attached. The C0-D shadow disappears structurally: there is no separate FACT to shadow the MAP because they are one node.
- **Risk:** medium-high. Provenance and lifecycle edges currently distinguish the types (ET_USE/ET_DEP/ET_SUP on MAPs). Those would become edge patterns on one type, which is arguably cleaner but touches revision, eviction, and standing logic. This is the deepest candidate and the one most aligned with "procedures and causal rules converge on one executable graph type."

### Rank 3: ev_teach / ev_teach_in -> one teach with bookkeeping flags

- **Removes:** the 5-line duplicate; one of two teach paths.
- **Preserves:** both bookkeeping regimes (full vs minimal).
- **Unification hypothesis:** `ev_teach(W,s,r,o,flags)` where flags select decay, context push, chaining, and event logging. The four internal call sites pass minimal flags; the external path passes full.
- **Risk:** low-medium. The bookkeeping differences are load-bearing (decay-on-external-teach drives the retention economy). A flags parameter must not silently change which paths decay. The audit notes the current split is honest about the difference; unification must preserve it, not blur it.

### Rank 4: max-bid selection -> one generic pick-max

- **Removes:** ~20 lines: the duplicated 1-hop/2-hop blocks inside ev_act, and the parallel logic in activate.
- **Preserves:** FACT ranking and guide ranking with their different candidate predicates and context matching.
- **Unification hypothesis:** `pick_max(W, candidates, matches_ctx)` with the candidate enumeration and match predicate as parameters. activate, ev_act 1-hop, ev_act 2-hop become three call sites.
- **Risk:** low. Same job, different predicates. The 2-hop neighbor expansion in ev_act is the only semantic subtlety; it becomes a candidate-source choice, not a code duplicate.

### Rank 5: t2_asm_chain / t2_asm_count -> one parameterized assembler

- **Removes:** ~12 lines of duplicated guard/set/provenance/seq body.
- **Preserves:** both templates exactly.
- **Unification hypothesis:** `t2_asm_seq(W,v,plen,f,per_link_op)` where per_link_op selects none (chain) or INC (count). t2_asm_sum remains separate (it is a different shape: unrolled total, no guards).
- **Risk:** low. Pure code sharing; the templates stay enumerated (this compresses code, not the schema; it does not advance SUF).

### Rank 6: ev_query fallback chain -> staged policy, not hardcoded router

- **Removes:** the router as control flow; the stage order becomes inspectable data.
- **Preserves:** all four answer strategies and their admission conditions.
- **Unification hypothesis:** stages as a tried-in-order list with per-stage admission predicates, evaluated by one driver. True mechanism unification (one strategy subsuming lookup, trial, bootstrap, inquiry) is NOT proposed: the strategies are semantically different and premature fusion would destroy the causal attribution the freeze batteries depend on.
- **Risk:** high if pushed beyond staging-to-data; low if kept as stagelist refactor. Ranked below the code-level candidates because the honest version of this change is small and the ambitious version is dangerous.

### Rank 7: bootstrap_miss job separation

- **Removes:** nothing directly; clarifies three jobs (statistical test, MAP creation, FACT teaching) currently fused in one 26-line body.
- **Preserves:** the P-INV shortcut.
- **Unification hypothesis:** the statistical test returns a verdict; promotion and teaching are the shared paths (promote_graph / ev_teach_in). Note promote_graph currently ALSO teaches (the shadow), so this interacts with Rank 2 and the reuse fix.
- **Risk:** medium. The fusion is load-bearing for the shortcut's atomicity; separation must not introduce partial states.

### Rank 8: dead node types + trivial wrappers

- **Removes:** T_GROUP, T_REGRET, T_COEFF definitions (3 lines, zero uses); optionally folds contradict_map (2 lines, 2 call sites) and mp_run (5 lines, 1 call site) into callers.
- **Preserves:** everything (dead code) or readability (wrappers document intent).
- **Risk:** none for the dead types; low but negative readability value for the wrappers. Ranked last because it changes nothing architectural.

### Explicitly NOT candidates (already compressed or correctly separate)

- `execute` / `t2_exec` / `exec_val`: one engine, thin adapters. Fine.
- `revise_on_contradict` / `t2_revise_graph`: dispatcher/worker is a legitimate split. The compression opportunity inside revision is copy-and-commit (already approved), which replaces the ~15-line in-place revert path, not the split.
- Single-use helpers (`t2_lu_first`, `inc_fill`, `t2_kill_edge`, `seq_link`): no duplication to remove.
- `map_standing`: computed but never read. Not a compression candidate; it is a dead signal. Either a reader should exist (H3-lite Node 3 could use it) or it should go. Flagged, not ranked.

## 4. Standing architectural metric for this audit

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | inventory only; no changes proposed |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 (audit) |
| SOURCE-ENUMERABLE FORMS | 3 assemblers (unchanged by audit) |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 |
| REUSE EVENTS | 0 |
| REVISION EVENTS | 0 |
| COGNITION LINES | 0 added, 0 modified (read-only) |
| MODES | 0 |
| BRIDGES | 1 found (ev_query 4-stage router) |
| HANDLERS | 0 |
| SEMANTIC CASES | 0 |

## 5. Summary judgment

TNN-2 is not a dozens-of-subsystems tangle; it is one node/edge substrate with a small number of genuinely duplicated jobs. The audit finds **8 ranked candidates**, of which Ranks 1-5 are real compression with preserved capability:

1. Trial 4-phase loop -> candidate-source iterator (also the H3-lite Node 1 direction)
2. FACT/MAP duality -> one knowledge node with optional executable (deepest; resolves C0-D structurally)
3. Two teach paths -> one teach with flags
4. Three max-bid scans -> one generic pick-max
5. chain/count assemblers -> one parameterized assembler

The single router (ev_query fallback chain) should become staged data, not fused machinery. Three node types are dead. One computed signal (map_standing) has no reader. No mode flags exist in the cognitive path, which is to TNN-2's credit under the One-System Rule.

Total estimated removable duplication: ~90-110 lines of the ~700 cognitive lines (excluding tests), roughly a 13-16 percent code compression, plus the structural simplifications of Ranks 1-2 which are larger than their line counts suggest.
