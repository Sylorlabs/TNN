# REPORT: Unified Composition Mechanism

## Verdict: COMPOSITION-UNIFIED-COMPLETE

**One operation replaces A/B/C's three engines. 369 fewer lines (47%).
Capability retained on T1/T3. Generality extended: 4 and 5 structure
composition now work (the 3-segment cap was the only blocker).
3/3 byte-identical. Zero modes/bridges/handlers.**

Date: 2026-10-02. Worker: Composition Collapse Builder.
Prereg: PREREG.md, commit 06ea103bd (frozen before implementation).
Branch: tnn-native-lab, local only, nothing pushed.

## Architecture

C's iterative DFS is the single composition operation. A's plen-contracts
and B's co-use history are pluggable applicability predicates feeding the
DFS. A/B's pair-search machinery is deleted, not ported.

### Kept (from C)

- `un_dfs`: iterative deepening over applicable MAPs. The researcher
  3-segment cap is removed; the practical search bound is now 8 segments
  (documented; the battery needs 5).
- Assembly: `t2_asm_chain` per segment, SEQ-linked, verified via
  `t2_try_verify`, promoted via `promote_graph` with LINK14 provenance
  to each segment MAP.
- `cc_relseq`: relation sequence extracted from executable graph
  structure, never MAP labels.
- `cc_satisfy`: relseq walk against the fact store.

### Ported

- **A's principle** (`cx_contract`, verbatim): plen contract of a chain
  MAP. Consulted as a fallback in `un_satisfy` when relseq extraction
  fails (OR admission: C's walk first, A's gather second). Not a gate.
- **B's principle** (`cb_couse_link` verbatim; `cb_has_couse` new):
  type-15 co-use edges order candidates (history-first, stable ties),
  and every successful composition writes type-15 edges between
  consecutive segments so history accumulates from composition itself.
  B's `ev_cq` episode facility is retained verbatim as the
  history-writing event.

### Deleted

- A's `compose_try` pair search (nested m1/m2 loops).
- B's `compose_try` pair search (type-15 edge scan over pairs).
- B's `cb_stage` (redundant with `un_satisfy`).
- C's `cc_candidates` (replaced by `un_candidates` with OR admission).
- C's 3-segment cap (`L+1>2`).

### Pipeline position

`ev_query`: activate -> rebind_try -> compose_try -> trial ->
bootstrap. Same position as all three predecessors. One `compose_try`
definition, one call site. No COMPOSE_MODE.

## Line Counts (kill bar K5)

| Engine | Lines |
|--------|-------|
| A (cx_patch.zag) | 183 |
| B (cb_patch.zag) | 298 |
| C (cc_patch.zag) | 308 |
| Sum A+B+C | 789 |
| Unified (un_patch.zag) | 420 |
| **Delta** | **369 fewer (47%)** |

## Test Results

Battery: the 6 comparative-battery tests (frozen protocol, including
B-style co-use episodes). SHA-256
96ffabf454070de47590e60f1d57e288b9ec47f6107967e8a95d8406842032d8,
3/3 byte-identical.

| Test | Expect | Result | Detail |
|------|--------|--------|--------|
| T1 3-struct | PASS | PASS | COMP-SEGS n=3 (MAPs 13 26 39, same as C), ans=107. couse15 2->4: composition wrote history. |
| T2A 4-struct | PASS | PASS | COMP-SEGS n=4 (13 26 39 52), ans=109. couse15 3->6. |
| T2B 5-struct | PASS | PASS | COMP-SEGS n=5 (13 26 39 52 65), ans=111. couse15 4->8. |
| T3 cross-domain | PASS | PASS | COMP-SEGS n=2 (27 42, same as C), ans=105. |
| T4 partial | FAIL, no false positive | FAIL | ans=-2, terminates. No regression vs C. |
| T5 no-expected | decline -2 | decline | compose declines cleanly (-2), ans=-2. No regression vs C. |

Kill bars: K1 PASS, K2 PASS, K3 PASS, K4 PASS, K5 PASS (420 < 789),
K6 PASS (3/3 identical), K7 PASS (audit below), K8 PASS (T4/T5 no
regression). All 8 pass.

## Generality Comparison

| Test | A | B | C | Unified |
|------|---|---|---|---------|
| T1 3-struct | FAIL | FAIL | PASS | PASS |
| T2A 4-struct | FAIL | FAIL | FAIL | PASS |
| T2B 5-struct | FAIL | FAIL | FAIL | PASS |
| T3 cross-domain | PASS | PASS | PASS | PASS |
| T4 partial | FAIL | FAIL | FAIL | FAIL |
| T5 no-expected | FAIL | FAIL | FAIL | FAIL |

The unified mechanism strictly dominates all three on arity. There is no
test where A/B/C succeed and unified fails. The 4/5-structure failures
were purely the researcher cap: same DFS, bound raised, both pass.

## Predicate Evidence

- **C's walk** did the selection work in all passing tests (segment MAPs
  13 26 39 match C's run exactly; T3 segments 27 42 match C exactly).
- **A's contract** is live as the OR fallback in `un_satisfy` (fires
  when relseq extraction fails); it did not need to fire on this
  battery, which is expected since all MAPs here are pure chains.
- **B's history** is live in both directions: episodes wrote type-15
  edges (couse15=2/3/4/1 before Z), candidate ordering consults them,
  and composition successes wrote new edges (post counts 4/6/8/2).
  History accumulates from composition itself, not only from episodes.

## No Hidden Bridge (kill bar K7)

- Exactly 1 `compose_try` definition, exactly 1 call site in ev_query.
- 0 COMPOSE_MODE, 0 MODE identifiers, 0 task-specific relation numbers
  in un_patch.zag.
- Predicates are pure functions over learner state (MAP graphs, edge
  store), not task-specific gates. The DFS never branches on MAP
  identity or task type.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.

## Honest Boundaries

1. **T4 partial applicability**: still fails (atomic MAP assumption).
   Unification does not address sub-MAP decomposition. Open question
   stands.
2. **T5 unsupervised**: still requires expected-answer. compose_try
   declines cleanly on expected<0. Learner-owned verification is future
   work.
3. **Signal arbitration**: admission is permissive OR (any predicate
   admits). Conflict resolution between predicates is future work.
4. **Search cost**: 8-segment bound is a practical DFS limit, stated in
   the prereg. Scaling to large MAP spaces needs the indexing work from
   the scaling lane.
5. A/B's original pair-search code is deleted from the unified build;
   the old engines remain in their own directories, untouched.

## Files

- `PREREG.md`: frozen preregistration (commit 06ea103bd, committed
  before implementation)
- `NAMECHECK.md`: toolchain guard, build records, audits
- `REPORT.md`: this file
- `un_patch.zag` (420 lines): the unified mechanism
- `un_driver.zag` (289 lines): the 6-test battery driver
- `un_full.zag` (2386 lines): base + patch + driver
- `un_bin`: pinned znc build
- `un_run1/2/3.txt`: 3/3 byte-identical runs
- `un_compile.txt`: compile log

## Recommendation

Adopt the unified mechanism as the canonical composition operation and
retire A/B's pair-search engines (their directories stay as evidence;
nothing is deleted from history). The 369 deleted lines are pure win:
less code, more capability, no hidden complexity. Next composition work
is T4 (decomposable MAPs) and T5 (unsupervised verification), both
independent of the collapse.
