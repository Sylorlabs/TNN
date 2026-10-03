# ARCH_ACCOUNTING_1421.md

Wave: wave-20260930-1421pdt. Tip measured: d5984f313.
Method: MEASUREMENT_PROCEDURE.md from docs/lab/research-lead/overnight-20260928/arch_accounting/
(the baseline document; historical rows never edited).

## Counting method (reproducible)

For each generation source file: total lines via `wc -l`; comment-only
lines via `grep -cE "^[[:space:]]*//"`; function spans via awk on
`^fn ` definitions (span = lines from the fn line to the next fn line).
Each function classified into exactly one bucket: INFRA (io, alloc,
string, byte helpers), ACCESSOR (slot/field read/write helpers),
VOCAB (researcher-authored structural vocabulary constants: node tags,
edge types, opcodes, capacities; reported separately, not in the
cognition headline), COGNITION (learn, retrieve, infer, retain/evict,
plan, causal derivation, discovery, revision, execute), DIAG (test
reporting, state comparison helpers), FIXTURE (init and test setup),
TEST (self-test functions), DRIVER (main, test runners). Cognition
source lines = sum of COGNITION spans. Modes via `grep -c "_MODE"`;
bridges via `grep -ci "bridge"` with manual review of each hit;
handlers via `grep -c "^fn handle_"`; semantic cases via
`grep -cE "^[[:space:]]*(switch|match)[[:space:]]"` plus manual review
of `grep -nE "== *[0-9]{3,}"` hits. State bytes from the main-driver
z_alloc(N) sizes. Classification reviewed function by function; totals
reconcile to file line counts within header-comment lines.

## Headline table (tip d5984f313)

| Generation | Source file | Total lines | Cognition lines (functions) | Modes | Bridges | Handlers | Semantic cases | Learner-state bytes |
|---|---|---|---|---|---|---|---|---|
| Frozen core [RE-CERT] | core_freeze/stage0/world_learn.zag | 1424 | 586 (75) | 0 | 0 | 0 | 0 | 32768 |
| CLA-2 [NEW] | cla2_build/cla2.zag | 1419 | 739 (31) | 0 | 0 | 0 | 0 | 16384 |
| CAM-1 [NEW] | cam1_build/cam1.zag | 818 | 448 (16) | 0 | 0 | 0 | 0 | 344064 |
| ACT [NEW] | act_build/act.zag | 615 | 222 (14) | 0 | 0 | 0 | 0 | 33816 |

## Per-generation breakdowns

CLA-2 (cla2.zag, 1419 lines, 101 functions, 235 comment-only lines):
COGNITION 739 (31 fns: alloc_node, write_node, link_edge,
is_superseded, activate, decay, seq_next, execute, execute_value,
is_protected, evcount, bid, record_eviction, alloc_node_raw,
evict_node, refresh_protection, log_event, ev_teach, ev_query,
ev_observe, ev_teach_inner, ev_act, make_group, group_add,
group_evidence, make_map, map_add_coeff, map_standing, k_node,
k_get, bootstrap_miss). ACCESSOR 75 (20 fns). VOCAB 31 (21 fns:
ET_* edge types, T_* node tags, OP_MOVE/OP_BRANCHEQ/OP_INC/OP_DEC,
OSLOT, EBUDGET). INFRA 27 (6). DIAG 17 (state_copy, state_equal).
FIXTURE 21 (cla2_init). TEST 466 (16 self-test fns). DRIVER 20
(main). State: W = z_alloc(16384) in test mains.

CAM-1 (cam1.zag, 818 lines, 63 functions, 124 comment-only lines):
COGNITION 448 (16 fns: ws_alloc, es_add, standing, count_edges_to,
teach, lookup, fact_obj, align, materialize_group, subj_obj,
propose, eval_body, verify, promote, query, contradict). ACCESSOR 24
(16). VOCAB 23 (14 fns: T_FACT/T_MAP/T_GROUP, E_* edge types, B_*
body kinds). INFRA 24 (5). FIXTURE 7 (ws_init, es_init, m_init).
DIAG 7 (rep). TEST 209 (6 self-test fns). DRIVER 49 (run_loop,
main). State: ws = z_alloc(4096*36) = 147456, es =
z_alloc(16384*12) = 196608; persistent total 344064 bytes.

ACT (act.zag, 615 lines, 68 functions, 120 comment-only lines):
COGNITION 222 (14 fns: bid, nbr, seen, activate, act_event, mk_fact,
mk_goal, mk_guide, mk_uncert, learn_confirm, learn_contra,
derive_d1, live_count, evict_to_cap). ACCESSOR 46 (15). VOCAB 29 (21
fns: MAXN/NODESZ/MAXE/EDGESZ capacities, E_* edge types, T_* tags).
INFRA 28 (6). DIAG 7. FIXTURE/test setup 229 (new_world,
setup_stores, t_pact1..6). DRIVER 33 (usage, main). State: nd =
256*36 = 9216, ed = 2048*12 = 24576, st = 8, cx = 16; total 33816
bytes.

## Delta against baseline

Baseline (2026-09-30, 4d38aac91): frozen core 586 cognition lines
across 75 functions, 1/9 worlds, zero modes/bridges/handlers, 32768
state bytes; contlearn2 136 lines, 1024 bytes.

- Frozen core at tip: byte-unchanged (git diff e129b2fbd..d5984f313
  on world_learn.zag is empty). Row stands: 586 lines, 1/9 worlds,
  32768 bytes. [RE-CERT].
- CLA-2 alone (the consolidated continuing learner): 739 cognition
  lines vs 586, a +153 delta. The baseline projection of "40-60
  retention lines" for CLA-2 was about mechanism-line retention
  versus the sum of superseded mechanisms, not about the full
  consolidated file; the landed full generation file is 739.
- CLA-2 + CAM-1 + ACT (the baseline's stated honest comparison):
  739 + 448 + 222 = 1409 cognition lines vs the frozen core's 586
  (+823). Heavy caveat: the three are standalone prototype builds,
  not one merged generation; infra, accessor, and vocabulary
  machinery is duplicated across the three files; the integration
  lane this wave is explicitly converging them toward one
  executable graph type. A summed comparison is therefore
  pessimistic; the meaningful re-measure is after integration.
- New learned structures: 0 evidenced in all generations. All three
  use fixed-capacity arenas with researcher-authored vocabulary;
  CLA-2's edge/node conventions are projected, not yet evidenced on
  sealed worlds.

## One-System Rule smells

- _MODE identifiers: 0 in all three files (no CAUSAL_MODE,
  REVISION_MODE, LANGUAGE_MODE, MEMORY_MODE, PROCEDURE_MODE, or
  equivalents).
- Bridges: 0. The single `bridge` grep hit in cla2.zag is a comment
  asserting "Zero bridges" (line 14); not a mechanism.
- Handlers: 0 (`^fn handle_` count is 0 in all three files). Generic
  event dispatch (TEACH/QUERY/ACT/OBSERVE) is the single entry path.
- switch/match in cognition sources: 0. CLA-2's execute() dispatches
  over the closed 4-op ISA {MOVE, BRANCHEQ, INC, DEC} via if-chains:
  generic computational basis under the ISA ruling, not a semantic
  case.
- Hardcoded-id review: tag constants 101-104 (T_FACT/T_GROUP/
  T_HISTORY/T_REGRET) are the researcher-authored structural
  vocabulary (domain-neutral, not freeze-world ids); 903/3001 in
  k_node and test persistence are bootstrap/test constants; 6100+i
  style constants are test data. No freeze-world domain branches
  (no world ids, no sealed-world relation ids) in the cognition
  path.
- Governance flag for any future L3 claim: the T_*/E_*/OP_*/B_*
  vocabulary constants are researcher-authored structural
  vocabulary. Under L3 criterion C0-A, semantics must reside in
  learner-created persistent state; these constants are the
  enumerate-what-the-learner-may-build, so they bound how far any
  representational-invention claim can reach without revision.

Capabilities for the three new generations remain pending (builds
landed as BUILD-COMPLETE per commit messages; self-tests pass;
verdicts await evaluation and red team). Re-measurement triggers
after the integration lane lands.

No em-dashes in this documentation.
