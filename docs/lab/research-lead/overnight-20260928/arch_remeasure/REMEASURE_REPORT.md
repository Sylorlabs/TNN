# Architecture Accounting: Re-measurement (2026-09-30)

Worker: Architecture Accounting Re-measurement Worker.
Status: ARCH-REMEASURE-COMPLETE.
Method: MEASUREMENT_PROCEDURE.md, applied to frozen builder sources.

## Headline

| Generation | Capabilities passed | Cognition lines | Sem | Modes | Bridges | Handlers | State bytes | Learned structures |
|---|---|---|---|---|---|---|---|---|
| Frozen core (87ac95d08) | 1/9 freeze worlds | 586 | 0 | 0 | 0 | 0 | 32768 | 0 |
| contlearn2 (179b4a950) | LEARNER-EXTENDED | 136 | 0 | 0 | 0 | 0 | 1024 | 0 |
| CLA-2 (e639904f2) | 15/15 self-tests (sealed FW pending) | 685 | 0 | 0 | 0 | 0 | 16384 | 3 |
| CAM-1 (371d20743) | 6/6 synthetic (sealed FW pending) | 408 | 0 | 0 | 0 | 0 | 344080 | 1 |
| ACT (f7d87938f) | 24/24 tests (sealed FW pending) | 162 | 0 | 0 | 0 | 0 | 33816 | 2 |

## The honest sum

CLA-2 + CAM-1 + ACT cognition lines = 685 + 408 + 162 = **1255**.

Frozen core = 586.

The sum is 2.1x the frozen core. The prereg projection of
"net-negative vs mechanism sum" does NOT hold for the three separate
implementations.

## Why the sum exceeds the projection

The three implementations are separate. Each reimplements the workspace
machinery independently:

- Three copies of z_alloc/get32/set32 and byte helpers (INFRA).
- Three copies of node/edge accessor functions (ACCESSOR).
- Three separate node layouts (CLA-2: 40-byte nodes at noff;
  CAM-1: 36-byte nodes; ACT: 36-byte nodes).

An integrated one-system implementation would share one workspace,
one allocator, one accessor set, and one edge store. The duplication
is an artifact of parallel development, not architectural necessity.

The real test, per the baseline document, is the integrated system
measured on fresh adversarial worlds. That measurement is pending
integration.

## Trajectory assessment

**Lines:** Currently negative. 1255 > 586. The consolidation has not
yet reduced researcher-written cognitive machinery. The three builders
each wrote a full stack.

**Modes/bridges/handlers:** Holding at zero across all three. The
One-System Rule is honored in the negative (no new subsystems), even
as the positive (shared substrate) is not yet realized.

**Semantic cases:** Zero across all three. Verified by source inspection:
no switch/match, no hardcoded domain-id branches in cognition paths.
Test assertions with synthetic ids (e.g. CLA-2:1027, CAM-1:622) are
not cognition-path branches.

**Learner-state bytes:** CLA-2 uses 16384 (single workspace, half the
frozen core's 32768). CAM-1 uses 344080 (larger: 4096 nodes x 36 bytes
+ 16384 edges x 12 bytes). ACT uses 33816. These are separate stores;
integration would unify them.

**Learned structures:** This is where the trajectory is positive.
- Frozen core: 0 (fixed slots).
- contlearn2: 0 (fixed slots).
- CLA-2: 3 (learner-created GROUP nodes, learner-created MAP nodes,
  edge-derived standing convention).
- CAM-1: 1 (learner-created MAP nodes with trial-discovered bodies).
- ACT: 2 (POLICY_ROOT as learner-writable policy register,
  ACTION-GUIDE structures).

The learner now creates structure. The researcher still writes too much
machinery to support it.

## What would change the trajectory

1. Integrate CLA-2 + CAM-1 + ACT into one workspace implementation.
   Eliminate the duplicated INFRA/ACCESSOR (roughly 107+84 + 62+57 +
   64+30 = 404 lines of duplication).
2. Measure the integrated system on sealed FW1-FW9.
3. Compare integrated cognition lines against 586 with capabilities
   measured on the same sealed worlds.

Until then, the honest reading is: more machinery, but the machinery
now supports learner-created structure where the frozen core supported
none.

## Re-measurement log entry

| Date | Generation | Trigger | Result |
|---|---|---|---|
| 2026-09-30 | CLA-2, CAM-1, ACT | builder landings (e639904f2, 371d20743, f7d87938f) | this document; sum 1255 vs 586 |

## Detail: CLA-2 (e639904f2)

Source: docs/lab/research-lead/overnight-20260928/cla2_build/cla2.zag
Total lines: 1419. Comment-only: 235. Functions: 101.

| Category | Lines |
|---|---|
| INFRA (emit, i64s, e64, z_alloc, get32, set32, ET_*/OP_*/T_* constants, alloc_node, alloc_node_raw) | 107 |
| ACCESSOR (hg/hs, noff/ng/ns, eoff/eg/es, loff/lg/ls, write_node, frame_get/set, k_get, policy/miss_policy get/set, ctx_push/get) | 84 |
| COGNITION (link_edge, is_superseded, activate, decay, resolve_op, seq_next, execute, execute_value, is_protected, evcount, bid, record_eviction, evict_node, refresh_protection, log_event, ev_teach, ev_query, ev_observe, ev_teach_inner, ev_act, make_group, group_add, group_evidence, make_map, map_add_coeff, map_standing, k_node, bootstrap_miss) | 685 |
| DRIVER (cla2_init, state_copy/equal, 16 test functions, main) | 525 |

Semantic cases: 0. Modes: 0. Bridges: 0 (one comment mentions "Zero bridges").
Handlers: 0. State: 16384 bytes (single workspace).
Learned structures: 3 (GROUP nodes, MAP nodes, edge-derived standing).

## Detail: CAM-1 (371d20743)

Source: docs/lab/research-lead/overnight-20260928/cam1_build/cam1.zag
Total lines: 818. Comment-only: 124. Functions: 63.

| Category | Lines |
|---|---|
| INFRA (z_alloc, emit, i32s, get32, set32, T_*/E_*/B_* constants, ws_alloc, m_init) | 62 |
| ACCESSOR (n_tag/ref/pay get/set, e_from/to/type/set, m_nn/ne/maxn/maxe get/set, fact_obj, subj_obj, ws_init, es_init) | 57 |
| COGNITION (es_add, standing, count_edges_to, teach, lookup, align, materialize_group, propose, eval_body, verify, promote, query, contradict) | 408 |
| DRIVER (rep, run_loop, 6 test functions, main) | 266 |

Semantic cases: 0. Modes: 0. Bridges: 0. Handlers: 0.
State: 344080 bytes (ws 147456 + es 196608 + m 16).
Learned structures: 1 (MAP nodes with trial-discovered bodies).

## Detail: ACT (f7d87938f)

Source: docs/lab/research-lead/overnight-20260928/act_build/act.zag
Total lines: 615. Comment-only: 120. Functions: 68.

| Category | Lines |
|---|---|
| INFRA (z_alloc, emit, i32s, get32, set32, beq, pl, MAX*/E_*/T_* constants, nalloc) | 64 |
| ACCESSOR (nget/nset/ntag, eget/eset, st_* counters, polset/polget, ctxpush/ctxget) | 30 |
| COGNITION (elink, bid, nbr, seen, activate, act_event, learn_confirm, learn_contra, live_count, evict_to_cap) | 162 |
| FIXTURE (mk_fact, mk_goal, mk_guide, mk_uncert, derive_d1) | 69 |
| DRIVER (ptest, new_world, setup_stores, 6 test functions, usage, main) | 268 |

Semantic cases: 0. Modes: 0. Bridges: 0. Handlers: 0.
State: 33816 bytes (nd 9216 + ed 24576 + st 8 + cx 16).
Learned structures: 2 (POLICY_ROOT convention, ACTION-GUIDE structures).
