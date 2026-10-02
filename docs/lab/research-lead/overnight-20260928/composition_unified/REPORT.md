# REPORT: Unified Composition Mechanism

## Verdict: COMPOSITION-UNIFIED-COMPLETE

**Single operation replaces A/B/C's three engines. 51% fewer lines.
Capability retained. Generality extended (4 and 5 structures now work).
3/3 byte-identical.**

Date: 2026-10-02. Worker: Composition Collapse (unified builder).
Commit: (pending). Branch: tnn-native-lab, local only, nothing pushed.

## Architecture

C's iterative DFS is the single composition operation. A's plen-contracts
and B's co-use history are pluggable applicability predicates feeding the
DFS. A/B's pair-search machinery is deleted.

### What was kept

- **C's DFS** (`un_dfs`): iterative deepening over applicable MAPs.
  The 3-segment researcher cap is removed; max is now 8 segments.
- **C's assembly**: `t2_asm_chain` per segment, SEQ-linked, verified via
  `t2_try_verify`, promoted via `promote_graph` with LINK14 provenance.
- **C's structural extraction** (`cc_relseq`): relation sequence from
  executable graph structure, never MAP labels.
- **C's satisfiability** (`cc_satisfy`): relseq walk against fact store.

### What was ported

- **A's principle** (`cx_contract` + `un_satisfy` fallback): when relseq
  extraction fails, fall back to plen-contract via path gather. This is
  the OR in `un_satisfy`: C's walk first, A's gather second.
- **B's principle** (`cb_has_couse` + ordering + `cb_couse_link`):
  type-15 co-use edges order candidates (history-first), and successful
  compositions write type-15 edges between consecutive segments so
  history accumulates.

### What was deleted

- A's `compose_try` pair search (nested m1/m2 loops, ~120 lines).
- B's `compose_try` pair search (type-15 edge scan, ~60 lines).
- B's `cb_stage` (redundant with unified `un_satisfy`).
- C's `cc_candidates` (replaced by `un_candidates` with OR logic).
- C's `cc_dfs` 3-segment cap (`L+1>2`).

## Line Counts

| Engine | Lines |
|--------|-------|
| A (`cx_patch.zag`) | 183 |
| B (`cb_patch.zag`) | 298 |
| C (`cc_patch.zag`) | 308 |
| **Total A+B+C** | **789** |
| Unified (`un_patch.zag`) | **384** |
| **Deleted** | **405 (51%)** |

## Test Results (3/3 byte-identical, SHA 3e509438...)

### T3: 3-structure (capability retention)

- X (r1 plen-2), Y (r2 plen-2), W (r3 plen-2) trained independently.
- Z (r1x2, r2x2, r3x2, plen-6) solved: `COMP-SEGS n=3`, ans=107 (expected).
- ZMAP relseq=[1,1,2,2,3,3]. Correct assembly.
- **PASS**: matches C's capability.

### T4: 4-structure (cap removal)

- X, Y, W, V (r1-r4 plen-2 each) trained.
- Z (plen-8) solved: `COMP-SEGS n=4`, ans=119 (expected).
- **PASS**: C could not do this (3-segment cap). New capability.

### T5: 5-structure (cap removal)

- X, Y, W, V, U (r1-r5 plen-2 each) trained.
- Z (plen-10) solved: `COMP-SEGS n=5`, ans=131 (expected).
- **PASS**: beyond all three original engines. New capability.

### ABL-X: causal

- X MAP deleted. Z3 ans=-2. **PASS**: composition requires X.

### FRESH: causal

- No training. Z3 ans=-2. **PASS**: no spurious composition.

## Generality Assessment

| Test | A | B | C | Unified |
|------|---|---|---|---------|
| 3-struct | FAIL | FAIL | PASS | PASS |
| 4-struct | FAIL | FAIL | FAIL | PASS |
| 5-struct | FAIL | FAIL | FAIL | PASS |

The unified mechanism strictly dominates all three on arity. No test
where A/B/C succeed and unified fails.

## No Hidden Bridge

- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- Single `compose_try` in `ev_query`, same pipeline position as before.
- Applicability predicates are pure functions on learner state, not
  task-specific gates.
- The DFS does not branch on MAP identity or task type.

## Honest Boundaries

1. **T4 partial applicability**: still fails (all MAPs atomic). The
   unified mechanism does not address sub-MAP decomposition.
2. **T5 unsupervised**: still requires expected-answer. Learner-owned
   verification is future work.
3. **Signal arbitration**: when C's walk, A's contract, and B's history
   disagree, the current OR is permissive (any signal admits). A
   conflict-resolution policy is future work.
4. **B's episode history**: the unified mechanism writes type-15 edges
   from composition successes, but does not yet ingest B's `ev_cq`
   episode-style history. That integration is future work.
5. **Search cost**: 5-structure DFS explores more candidates. No
   pruning beyond the 8-segment cap. Scaling to very large MAP spaces
   needs the index work from the scaling lane.

## Files

- `un_patch.zag` (384 lines): the unified mechanism
- `un_driver.zag` (209 lines): T3/T4/T5/ABL-X/FRESH driver
- `un_full.zag` (2271 lines): base + patch + driver
- `un_bin`: pinned znc build
- `un_run1/2/3.txt`: 3/3 byte-identical
- `un_compile.txt`: clean (benign A0102 warnings only)
- `NAMECHECK.md`: toolchain guard

## Recommendation

The unified mechanism should replace A/B/C as the canonical composition
operation. The 405 deleted lines are pure win: less code, more capability,
no hidden complexity. The remaining work is T4 (decomposable MAPs) and
T5 (unsupervised verification), which are independent of the collapse.
