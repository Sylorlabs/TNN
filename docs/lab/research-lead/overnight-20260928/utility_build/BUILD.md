# Utility Signal Build

**Verdict:** UTILITY-BUILD-COMPLETE (pending falsification test 6).
**Date:** 2026-10-01 UTC.
**Design:** `docs/lab/research-lead/overnight-20260928/utility_signal/UTILITY_SIGNAL.md` (commit `cd6a8a74a`).
**Base:** Frozen TNN-2 `ub_base.zag` (SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`).

## Implementation

### Files

- `ub_base.zag`: Verbatim frozen TNN-2 (1591 lines). SHA-256 verified.
- `ub_util.zag`: Utility helpers (new, 8 functions).
- `ub_patch.zag`: Five modified functions (replacements).
- `ub_core.zag`: Base minus 5 replaced functions (1505 lines).
- `ub_full.zag`: Core + util + patch (1922 lines). Compiles clean.
- `ub_driver.zag`: Test driver (4 tests).
- `ub_test.zag`: Core + util + patch + driver (2168 lines).
- `ub_bin`: Compiled test binary.
- `ub_run1/2/3.txt`: 3/3 byte-identical runs (SHA-256 `81669ae4...`).

### Field layout (per design 2.1)

Collision audit confirmed (frozen source, read-only):
- MAP (tag-20) f12: U (utility). Base sets -1, never read on tag-20. Repurposed.
- MAP (tag-20) f16: L (last-active tick). Base sets -1, never read on tag-20. Repurposed.
- FACT (tag-1) f4: O (owning MAP id). Base never reads f4 on tag-1. Safe.
- FACT (tag-1) f12: Untouched (discount-reserved per discount spec).

### Write paths (per design 2.2)

| Event | Location | Update |
|---|---|---|
| Promotion | `promote_graph` (patched) | U=0, L=birth tick via `util_init`; shadow f4=m |
| Trial verify success | `promote_graph` (patched) | U+=2 via `util_add` (promote only called on success) |
| Query via shadow | `ev_query` (patched) | `util_attr` checks f4, U+=1 if valid MAP |
| Revision success | `revise_on_contradict` (patched) | Captures `t2_revise_graph` return 1, U+=1 |
| Revision failure | `revise_on_contradict` (patched) | Return 0, U-=1 (floor -8) |
| Contradiction | `contradict_map` (patched) | U-=2 (floor -8), L=now |

`util_add` enforces floor -8, ceiling +127, updates L=now on every write.
"Ran" alone never increments (V2-hole guard): only verified outcomes write.

### Read path: `evict_node` (patched, per design 2.4)

Priority (first match wins):
1. **ZOMBIE**: `map_is_zombie` (invalid root: dead/out-of-range/wrong-tag, or shared). Immediate `reclaim_map_atomic`. U irrelevant.
2. **FOSSIL**: `map_is_fossil` (valid root, U<=0, age > FOSSIL_AGE=200). Oldest first, atomic reclaim.
3. **LIVE low-U**: Unified scan. MAPs ordered by U ascending; non-MAPs by bid (fallback). Cells of LIVE MAPs skipped via `cell_of_live_map`.
4. **Bid fallback**: Integrated in pass 3 for non-utility nodes.

### Structure-atomic reclaim

`reclaim_map_atomic(W,m)`: Walks SEQ edges from MAP root (80-step bound, same as zombie detector), reclaims each cell, then reclaims MAP shell, then sweeps edges touching dead nodes. Single pass. Makes the "shell survives, body rots" zombie route impossible by construction.

### Structure-aware cell protection

`cell_of_live_map(W,c,now)`: For cell c (tag 101-104), checks if reachable from any LIVE MAP's root via bounded SEQ walk. Live MAPs' cells are skipped in victim scan. Cost: O(live MAPs x chain length) per eviction, bounded by 80-step walk.

### FOSSIL_AGE

Scaffolded at 200 ticks (design 2.5: twice the observed fossilization window; interference battery shows degradation at V=1000). Honestly labeled as researcher-set. Retirement condition: learner adapts threshold from reclaim-regret (downstream).

## One-System Rule audit

- **Modes:** 0. No utility mode. Writes inline in existing event paths.
- **Bridges:** 0. Native i32 fields on existing nodes.
- **Task-specific handlers:** 0. All write sites are generic event paths.
- **New edge types:** 0. Attribution via MAP-id field, not new edge.
- **New node kinds:** 0. No utility nodes or sidecar structures.
- **Semantic cases:** 0. Live/fossil/zombie is predicate over fields, not content-based.
- **Net mechanism count:** Negative. Atomic reclaim removes future zombie-detector need.

## Cognition diff

Modified functions: `promote_graph`, `contradict_map`, `ev_query`, `revise_on_contradict`, `evict_node` (5).
New helpers: `util_add`, `util_init`, `util_attr`, `util_clamp`, `map_root`, `map_root_valid`, `map_root_shared`, `map_is_zombie`, `map_is_fossil`, `map_is_live`, `cell_of_live_map`, `reclaim_map_atomic`, `FOSSIL_AGE` (13).
All other functions byte-identical to frozen base.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 5 (magnitudes +2/+1/-1/-2, floor -8, ceiling +127, FOSSIL_AGE=200, priority order)
- LEARNER-OWNED STRUCTURAL DECISIONS: Per-MAP U/L values (accumulated from experience)
- SOURCE-ENUMERABLE FORMS: 0 (no new node kinds, edge types, modes)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0 (magnitudes scaffolded, retirement stated)
- REUSE EVENTS: 0
- REVISION EVENTS: Measured in tests
- COGNITION LINES: ~180 added (helpers + patches)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
