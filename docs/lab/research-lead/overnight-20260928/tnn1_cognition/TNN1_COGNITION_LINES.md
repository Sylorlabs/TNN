# TNN-1 Cognition Line Remeasurement

Date: 2026-09-30. Worker: TNN-1 Cognition-Line Remeasurement Worker.
Method: MEASUREMENT_PROCEDURE.md (arch_accounting/), applied to frozen source.
Source: docs/lab/research-lead/overnight-20260928/tnn1_build/tnn1.zag
Build commit: 0323b97d5 (TNN-1 BUILD-COMPLETE).

## Headline

| Metric | Value |
|---|---|
| Total source lines (wc -l) | 1088 |
| Comment-only lines | 54 |
| Functions | 153 |
| Cognition source lines | 641 |
| Cognition functions | 53 |
| Semantic cases | 0 |
| Modes | 0 |
| Bridges | 0 |
| Handlers | 0 |

## Category breakdown

| Category | Lines | Functions | Notes |
|---|---|---|---|
| INFRA (io, alloc, string, byte helpers) | 23 | 6 | emit, i64s, e64, z_alloc, get32, set32 |
| ACCESSOR (workspace schema: offsets, constants, field helpers) | 55 | 55 | 40 type/opcode constants, 11 offset/get/set helpers, 4 policy/map accessors |
| COGNITION: generic substrate (workspace primitives + EXECUTE ISA) | 99 | 10 | alloc_node, alloc_raw, write_node, link_edge, fr_get, fr_set, res_op, seq_nx, execute, exec_val |
| COGNITION: retention/eviction (bid, protection, decay) | 102 | 10 | is_superseded, activate, decay, is_prot, evcount, bid, rec_evict, evict_node, ref_prot, log_ev |
| COGNITION: teach/query/act path | 144 | 9 | ctx_push, ctx_get, ev_teach, ev_teach_in, ev_query, ev_observe, ev_act, k_get, bootstrap_miss |
| COGNITION: plan synthesis/composition | 284 | 23 | plan_new through mp_run (COMP-1 port) |
| COGNITION: init | 12 | 1 | tnn1_init |
| DRIVER (test harness: 35 tests + runner + main) | 331 | 39 | t_c1..t_c15, t_a1..t_a6, t_p1..t_p7, t_f2, t_abl_*, t_dv, t_xcap, run_all, main |
| **Function lines subtotal** | **1050** | **153** | |
| Non-function lines (header/section comments, blanks) | 38 | - | |
| **Total** | **1088** | - | |

Cognition source lines: 99 + 102 + 144 + 284 + 12 = 641.

## Classification rationale

The generic substrate functions (alloc_node, alloc_raw, write_node,
link_edge, frame ops, execute) are classified as COGNITION rather than
INFRA because in TNN-1 they implement the learner's structural workspace,
not just raw memory allocation. They manage typed nodes, typed edges,
supersession, and the EXECUTE ISA. This follows the baseline precedent
where the associative store machinery (learn, query, evict) was
COGNITION while raw z_alloc was INFRA.

The 55 ACCESSOR functions are all single-line workspace schema helpers:
40 return type/opcode constants (node types, edge types, opcodes,
templates, step kinds), 11 compute offsets or read/write fields, and
4 access policy/map state. None implement cognitive operations.

## Comparison to frozen core baseline

| Generation | Cognition lines | Cognition functions | Capabilities |
|---|---|---|---|
| Frozen core (e129b2fbd) | 586 | 23 (8+6+9) | 1/9 freeze worlds |
| TNN-1 (0323b97d5) | 641 | 53 | 35/35 self-tests (sealed FW pending) |

TNN-1 carries 641 cognition lines vs the frozen core's 586, an increase
of 55 lines (9.4%). This buys: the unified structural workspace
(CLA-2 port), the ACT action-selection path, COMP-1 plan synthesis and
composition, CAM-1 verify/contradict, and the DEVINT curriculum driver.

The separate pre-integration implementations summed to 1255 cognition
lines (CLA-2 685 + CAM-1 408 + ACT 162). TNN-1's 641 represents a 49%
reduction from that sum, achieved by sharing one workspace substrate
instead of three separate stacks.

## Updated R_test (cognition-line basis)

The compression tracker reported R_test using total source lines:
TNN-1 3.22 per 100 lines (35 tests / 1088 lines).

On the cognition-line basis:
R_test = 35 / 641 = 5.46 tests per 100 cognition lines.

For reference, the frozen core: 1 world / 586 lines = 0.17 worlds per
100 cognition lines (not directly comparable; different test units).

## Semantic cases, modes, bridges, handlers

All zero, consistent with the TNN-1 red team finding (cbde38737):
no switch/match on domain content, no _MODE identifiers, no bridge
functions, no handle_ functions. The dispatch in exec_plan branches on
ISA opcodes, not domain templates.

## Learner-state bytes

110656 (z_alloc(110656) per WSZ(); 1024 nodes x 40 bytes + 4096 edges
x 16 bytes + log region). Up from the frozen core's 32768.

## New learned structures

Per the TNN-1 build: GROUP, MAP, and edge-standing conventions carried
forward from CLA-2/CAM-1, plus PROC nodes (from MUL-1, separate binary).
TNN-1 itself creates GROUP, MAP, PLAN, STEP, COMB, and COEFF node types
as learner-authored structures.

## Open items resolved

This remeasurement addresses compression tracker open items 6-8
(formal cognition-line classification for TNN-1).
