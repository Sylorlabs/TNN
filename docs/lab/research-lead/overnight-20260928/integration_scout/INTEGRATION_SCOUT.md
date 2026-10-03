# Integration Architecture Spec: One Continuing Learner

Status: SCOUT SPECIFICATION. Analysis only, no implementation.
Verdict target: INTEGRATION-SCOUT-COMPLETE.

## 1. The duplication inventory

Four implementations, four workspace stacks. Measured cognition lines:
CLA-2 685, CAM-1 408, ACT 162, COMP-1 (not yet measured, ~879 total lines).
The re-measurement report found ~404 lines of duplicated workspace machinery
per builder. Source inspection confirms the duplication is real and
mechanical:

### 1.1 Byte-level primitives (all four)

Every implementation defines its own `z_alloc`, `get32`, `set32`, `emit`,
and integer-to-string. These are byte-identical in function, differing only
in names (`i64s` vs `i32s`). Cost: ~20 lines x 4 = 80 lines, of which 60 are
pure duplication.

### 1.2 Node accessors (all four)

- CLA-2: 40-byte nodes, `ng`/`ns` with header offset (`noff(n) = 64+n*40`).
- CAM-1: 36-byte nodes, `n_tag`/`n_ref`/`n_pay` with `n*36`.
- ACT: 36-byte nodes, `nget`/`nset` with `a*36+f*4`.
- COMP-1: 40-byte nodes plus valid flag, `n_tag`/`n_ref`/`n_pay`/`n_valid`
  with `n*40`.

Same operations, four spellings. Cost: ~30 lines x 4 = 120 lines, of which
~90 are duplication.

### 1.3 Edge accessors (all four)

- CLA-2: 16-byte edges (`eoff(e) = 2624+e*16`), `eg`/`es`.
- CAM-1: 12-byte edges (`e*12`), `e_from`/`e_to`/`e_type`/`e_set`.
- ACT: 12-byte edges (`e*12+f*4`), `eget`/`eset`.
- COMP-1: 16-byte edges (`e*16`), `e_from`/`e_to`/`e_type`.

Cost: ~20 lines x 4 = 80 lines, of which ~60 are duplication.

### 1.4 Allocators and linkers (all four)

`alloc_node`/`ws_alloc`/`nalloc`/`node_alloc` and
`link_edge`/`es_add`/`elink`/`edge_add`. Same logic, four spellings.
Cost: ~25 lines x 4 = 100 lines, of which ~75 are duplication.

### 1.5 Teach and query (all four)

`ev_teach`/`ev_query` (CLA-2), `teach`/`lookup`/`query` (CAM-1),
`mk_fact` plus test setup (ACT), `teach`/`exact_lookup`/`query` (COMP-1).
The teach path (allocate node, set tag/refs/payload, link edges) and the
exact-key query path are the same algorithm four times.
Cost: ~40 lines x 4 = 160 lines, of which ~120 are duplication.

### 1.6 Activation (CLA-2 and ACT)

Both implement graph activation from a root over edges. CLA-2 `activate`
filters tag=1; ACT `activate` does 2-hop traversal with visited-set.
Overlapping logic, different signatures.
Cost: ~30 lines x 2 = 60 lines, of which ~30 are duplication.

### 1.7 Evidence bid (CLA-2, CAM-1, ACT)

`bid`/`evcount` (CLA-2), `standing`/`count_edges_to` (CAM-1), `bid` (ACT).
All count typed edges to compute a signed score. The ACT red team found a
real divergence: ACT counts both directions, CLA-2 counts incoming only.
Cost: ~20 lines x 3 = 60 lines, of which ~40 are duplication, plus one
spec bug to resolve.

### 1.8 Test harnesses (all four)

Each has its own `main`, test functions, and assertion helpers. These are
driver code, not cognition, but they still duplicate the world-setup logic.
Cost: ~100 lines x 4 = 400 lines (driver, excluded from cognition counts
but real maintenance burden).

### Total duplication

Cognition duplication: ~60 + 90 + 60 + 75 + 120 + 30 + 40 = ~475 lines.
This matches the re-measurement estimate of ~404 lines per builder within
inspection tolerance. The four implementations contain roughly 475 lines
that are the same workspace machinery written four times.

## 2. The unified workspace

### 2.1 Format decision: CLA-2 wins

The unified workspace uses CLA-2's format as the base, for four reasons:

1. It is the most complete: 12 edge types covering every relation the other
   three use (CAM-1's 5 and ACT's 9 and COMP-1's 3 are all subsets).
2. It has the EXECUTE primitive with the closed 4-op ISA (MOVE, BRANCHEQ,
   INC, DEC), which COMP-1's `exec_plan` needs and CAM-1's trial bodies
   can target.
3. It has POLICY_ROOT and MISS_POLICY as ordinary nodes (A12), which is
   the dispatch mechanism COMP-1's `mp_run` and CAM-1's `propose` both
   need.
4. It already contains the 5-step ACT protocol (`ev_act`, line 660) and
   MAP nodes (T_MAP=20, T_COEFF=21), so ACT and CAM-1 are already
   partially integrated at the source level.

### 2.2 Additions to the CLA-2 base

The base needs four additions, all as new node types and edge uses, zero
new core operations:

1. **Plan nodes** (from COMP-1): T_PLAN, T_STEP, T_COMBINE, and the template
   markers TM_CHAIN2, TM_GATHER, TM_ITER, TM_COMPOSED. Plans are executable
   graphs linked with ET_SEQ edges, invoked through the existing EXECUTE
   primitive. COMP-1's `mp_build`, `mp_build_compose`, and `exec_plan`
   port directly; `exec_plan`'s SK_* step kinds map onto the 4-op ISA.

2. **Uncertainty nodes** (from ACT): T_UNCERT and the guide mechanism
   (`mk_guide`, `mk_uncert`). CLA-2's `ev_act` already does address-equality
   matching over the context ring; uncertainty-anchored guides become
   nodes that `ev_act` can select when their anchor is live. ACT's
   `learn_confirm` and `learn_contra` port as edge operations (USE,
   CONFIRMS, CONTRADICTS), which already exist.

3. **Trial bodies** (from CAM-1, minus the menu): CAM-1's `propose` is a
   4-item researcher menu (red-team finding: bounded L2, not discovery).
   The integration replaces the menu with COMP-1's plan construction:
   on query miss, MISS_POLICY fires plan construction over the three
   frozen templates, and the surviving plan is promoted as a MAP node.
   CAM-1's `verify` (train/test split) and `promote` survive; the
   `eval_body` 4-way dispatch is deleted.

4. **Bid directionality fix** (ACT red-team finding): resolve whether `bid`
   counts incoming-only (CLA-2 `evcount`) or bidirectional (ACT `bid`).
   Recommendation: incoming-only, matching CLA-2, because outgoing edges
   represent consequences the node asserts rather than evidence it has
   received. This is a one-line change in the ported ACT code and a spec
   amendment, not new machinery.

### 2.3 What gets deleted

- CAM-1's `eval_body` 4-way dispatch (the menu). Deleted, not ported.
- CAM-1's `B_COPY_B` and `B_DBL_B` dead code. Deleted.
- Three of the four byte-accessor sets. Deleted.
- Three of the four node/edge accessor sets. Deleted.
- Three of the four allocators, linkers, teach paths, query paths. Deleted.
- One of the two activation functions (keep CLA-2's, extend with ACT's
   visited-set logic if needed).
- Two of the three bid functions (keep CLA-2's incoming-only).
- Three of the four test harnesses (keep one unified driver).

### 2.4 The unified event flow

One teach path, one query path, one action path:

```
TEACH(subj, rel, obj):
  allocate fact node, link edges, log event, decay, done.
  (CLA-2 ev_teach; the only teach.)

QUERY(subj, rel):
  exact-key lookup -> hit? return.
  miss -> MISS_POLICY dispatch:
    null -> bootstrap (CLA-2 bootstrap_miss: P-INV trial)
    learner-set -> plan construction (COMP-1 mp_build over 3 templates)
    constructed plan -> verify (CAM-1 train/test split)
    verified -> promote as MAP node, execute via EXECUTE
    failed -> return -2 (S_MISS).
  (One miss path replacing three.)

ACT():
  5-step protocol (CLA-2 ev_act):
    context assembly -> POLICY_ROOT check -> 2-hop activation ->
    address-equality match -> highest-bid selection.
  Uncertainty nodes participate as ordinary candidates; no special case.
```

CAM-1's PROPOSE/VERIFY/PROMOTE/APPLY becomes: plan construction is the
propose step, the train/test split is the verify step, MAP promotion is
the promote step, EXECUTE is the apply step. Four named phases, one
code path, zero new operations.

## 3. Coexistence of the three mechanisms

### 3.1 CAM-1's trial-based P-DEP

Survives as the verify/promote half. The propose half is replaced by
COMP-1's plan construction (see 2.2.3). The red team showed the menu is
bounded L2; the integration does not port the menu. What ports:
`verify` (spurious-regularity rejection, demonstrated by P6),
`promote` (SUPPORTS-edge writing, with the circularity noted by the red
team fixed by requiring post-promotion corroboration before standing
counts), `contradict` (CONTRADICTS-edge demotion).

### 3.2 ACT's 5-step protocol

Already in CLA-2 as `ev_act`. Ports unchanged except the bid
directionality fix. The uncertainty mechanism ports as node types plus
the `learn_confirm`/`learn_contra` edge operations. No separate ACT
module survives; it is a usage pattern of the unified workspace.

### 3.3 COMP-1's plan construction

Ports as the miss-policy implementation. The three frozen templates and
the e-ruling (expected as post-hoc feedback only, e-ablation mandatory)
are preserved exactly. `mp_trigger`, `mp_build`, `mp_build_compose`,
`exec_plan` port with accessor renaming only. The 150-line bootstrap
bound from the COMP-1 prereg becomes the budget for the ported miss
policy.

### 3.4 The composition that matters

The integration's thesis: a query miss triggers plan construction
(COMP-1), the constructed plan is verified (CAM-1's split), the verified
plan is promoted as a MAP node (CLA-2's standing), and future queries
hit the MAP node via exact-key lookup. Action selection (ACT) runs on
the same workspace, selecting among ACTION-GUIDEs by the same bid
function. One workspace, one bid, one miss path, three capabilities.

## 4. Projected line count

### 4.1 The honest arithmetic

Starting point: 1255 cognition lines (685 + 408 + 162; COMP-1 not yet
measured but ~300 estimated cognition lines, for ~1555 total across four).

Deletions (duplication removed):
- Byte accessors: -60
- Node accessors: -90
- Edge accessors: -60
- Allocators/linkers: -75
- Teach/query paths: -120
- Activation (one of two): -30
- Bid (two of three): -40
- CAM-1 menu (`eval_body` dispatch, dead code): -80
- Redundant test drivers: -300 (driver, not cognition, but counted
  for completeness)

Cognition deletions: ~555 lines.
Additions (integration glue):
- Plan node types and template markers: +20
- Uncertainty node types: +10
- Miss-policy wiring (COMP-1 as MISS_POLICY impl): +40
- Post-promotion corroboration (red-team fix): +30

Cognition additions: ~100 lines.

Projected cognition lines: 1555 - 555 + 100 = ~1100.
Projected total lines (with one driver): ~1400.

### 4.2 Against the targets

- Below 1255 (three-system sum): YES, ~1100 < 1255.
- Below 1555 (four-system sum): YES, by ~455 lines.
- Approaching 586 (frozen core): NO. The frozen core does far less
  (1/9 worlds, no composition, no uncertainty, no trial discovery).
  The honest comparison is capability-adjusted: the integrated system
  should demonstrate CLA-2's 15/15 plus COMP-1's 10/10 plus ACT's 24/24
  in one binary, which no 586-line system does.

### 4.3 The trajectory verdict

The re-measurement report was correct: separate implementations do not
compress. Integration recovers ~455 lines of duplication and, more
importantly, produces one testable system instead of four. The line
count will still exceed the frozen core because the capability exceeds
the frozen core. The metric that matters is capability per line:
- Frozen core: 1/9 worlds / 586 lines = 0.0017 worlds/line.
- Integrated (projected): (15 + 10 + 24 tests) / 1100 lines.
The test suites are not commensurable, so the honest claim is narrower:
one binary passes all three suites, which no single existing binary does.

## 5. Integration prereg shape

### 5.1 What the builder implements

A single Zag source file, `tnn.zag`, containing:

1. The unified workspace (CLA-2 format: 40-byte nodes, 16-byte edges,
   64-byte header, 12 edge types, node/edge accessors, allocator,
   linker, teach, exact-key query, activation, incoming-only bid,
   decay, retention, event log).
2. The 7 core primitives (ALLOC, READ, WRITE, LINK, ACTIVATE, DECAY,
   EXECUTE) with the closed 4-op ISA.
3. POLICY_ROOT and MISS_POLICY as ordinary nodes (A12).
4. The unified miss path: exact-key -> MISS_POLICY -> plan construction
   (3 templates) -> verify (train/test) -> promote (MAP node) -> -2.
5. The 5-step ACT protocol over the same workspace.
6. Plan node types (T_PLAN, T_STEP, T_COMBINE) and template markers.
7. Uncertainty node types (T_UNCERT) and guide edge operations.
8. The bootstrap miss policy (P-INV trial, learner-supersedable).
9. Post-promotion corroboration (red-team fix for circular standing).
10. One test driver running all ported tests.

### 5.2 Kill bars

- K1 (commit order): integration prereg committed alone before any
  implementation; implementation commit must be a strict descendant.
- K2 (architecture): zero new core operations beyond the 7; zero
  semantic cases; zero modes; zero bridges; zero task-specific handlers;
  cognition lines < 1200 (hard ceiling); the CAM-1 menu must not reappear
  in any form (source scan for template-count > 3 in the propose path
  fails the build).
- K3 (purity): pure Zag; shell only for znc, binaries, git, moves.
- K4 (functional): the integrated binary passes CLA-2's 15/15, ACT's
  24/24, and COMP-1's 10/10, all in one process, byte-identical across
  3 runs. CAM-1's P6 (spurious-regularity rejection) and P7
  (contradiction demotion) port as integration tests.
- K5 (no regression): the e-ablation (F2) still passes; the bid
  directionality fix is verified by a test with outgoing-only evidence.

### 5.3 Falsification

- F-INT1: if the integrated line count exceeds 1200, the integration
  has failed to compress and the One-System claim is weakened.
- F-INT2: if any test from the three suites fails in the integrated
  binary but passed standalone, the port introduced a regression.
- F-INT3: if source scan finds a fourth template in the propose path or
  a domain-conditional in the miss path, the integration smuggled in
  researcher knowledge.
- F-INT4: if the integrated system cannot pass a cross-capability test
  (e.g., a plan constructed for a query miss later selected by ACT as
  an action guide), the mechanisms coexist but do not integrate.

### 5.4 What success looks like

One binary, ~1100 cognition lines, zero architectural smells, passing
49 tests across three suites plus cross-capability integration tests.
The four mechanisms (continuing memory, trial verification, action
selection, plan construction) share one workspace, one bid function,
one miss path, and one event log. A plan built for a query can later
guide an action; a contradiction against a MAP node demotes both its
query standing and its action candidacy through the same edges.

That is the One-System Rule made executable: not four systems with a
router, but one workspace with four usage patterns.

## 6. Open questions for the prereg author

1. **Bid directionality**: incoming-only (recommended) vs bidirectional.
   The ACT red team flagged this; the integration prereg must decide.
2. **COMP-1's `expected` parameter**: the miss path signature needs
   `expected` for the e-ruling (post-hoc feedback). Where does `expected`
   come from in a unified query that has no test harness? Frozen answer:
   the query path takes an optional expected only in test mode; in live
   mode it is absent and selection falls back to first non-sentinel.
3. **Retention unification**: CLA-2 has the three-step routine, ACT has
   `evict_to_cap`, CAM-1 has none. The integration needs one retention
   policy. Recommendation: CLA-2's three-step routine, with ACT's
   signed-bid eviction as the step-1 ordering.
4. **Node budget**: CLA-2 uses 64 nodes, ACT 256, COMP-1 256, CAM-1 4096.
   The unified budget must be set deliberately. Recommendation: 1024
   nodes, 4096 edges, justified as 4x headroom over the largest current
   test (COMP-1's 256-node tests).

## Governance

- Analysis only. No implementation, no computational research logic.
- Zero Python invocations (guard recorded in NAMECHECK.md).
- Contaminated paper verified zero-diff.
- Sealed FW1-FW9 files not accessed.
- Dash-clean via byte check.
