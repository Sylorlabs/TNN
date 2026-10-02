# REPORT.md -- Scaling 5000 Worker (s5_* workstream)

## Verdict: SCALING-5000-PARTIAL

The hardened MAP index holds its 5-visit flat at 5000 MAPs (13,107x
reduction measured). However, a build-order-dependent correctness bug
in the FACT index (used during build) causes query failures when
~5000 decoys are built BEFORE the real MAPs. The index mechanism
itself is sound; the bug is in build-time fact lookup at large scale.

## 1. What was built (s5_* workstream)

- **Base** (`s5_base.zag`): 65536 nodes / 131072 edges via sed from
  scaling_clean/sc_base_expanded.zag (8192/16384). Workspace 4,722,752
  bytes. Two build-performance optimizations (unfrozen, semantically
  equivalent):
  - `alloc_node`/`alloc_raw`: high-water start (`hg(W,20)+2`) instead
    of linear scan from 2. Equivalent when no eviction occurs.
  - `ev_teach` prev-scan: down-scan from `n-1` instead of up-scan
    from 2. Finds max live FACT id < n; identical to original.
- **Patch** (`s5_patch.zag`): sc_patch mechanisms (MAP plen-bucket
  index + FACT subject index) with hardened `idx_walk_bucket`
  (I1 bounds, I2 cycle via seen bitmap, I3 liveness, I4 type check,
  I5 buffer nc<8192 for 65536-byte/8192-entry candidate buffer).
- **Driver** (`s5_driver.zag`): T1 scale (4990 broken plen-2 + 5 real
  plen-5, modes 0/1), T2 corruption (cycle in plen-5 bucket), T3 churn
  (evict/re-promote), T4 collision (2000 plen-5 in one bucket).
- **Binary** (`s5_bin`): compiled with pinned znc, exit 0.

Note: A parallel s5000_* workstream exists in this directory from
another worker (base_64k.zag, s5000_*.zag, REPORT.md sections
describing it). That workstream is separate; this report covers only
the s5_* files.

## 2. Scale law (T1) -- MEASURED

| MAPs | mode | scan visits | tried | ok |
|------|------|-------------|-------|----|
| 5000 | linear | 65534 | 5 | 0 (FAIL) |
| 5000 | indexed (hardened) | 5 | 5 | 0 (FAIL) |

- The 5-visit flat HOLDS at 5000 MAPs. Indexed scan visits do not
  grow with MAP count.
- Linear visits all 65534 slots (65536-2).
- Reduction: 65534/5 = **13,107x**.
- **BUT**: queries failed (ans=-2). All 5 real plen-5 MAPs were found
  by the index (scan=5 proves it) but all 5 failed verification
  (tried=5, rejected=5).

## 3. Correctness bug: build-order dependent

### 3a. Threshold investigation

| Broken decoys (built BEFORE 5 real) | Query result |
|-------------------------------------|--------------|
| 0 | ok=1, tried=1 |
| 10 | ok=1, tried=1 |
| 100 | ok=1, tried=1 |
| 500 | ok=1, tried=1 |
| 1000 | ok=1, tried=1 |
| 4990 | ok=0, tried=5 rejected=5 |

The mechanism works up to at least 1000 decoys. Failure threshold
is between 1000 and 4990.

### 3b. Build-order test (dbg5)

- Build 5 real MAPs FIRST, query: **ok=1, tried=1** (works).
- Build 2000 decoys, query AGAIN: **ok=1, tried=0** (works via
  activate; the first query taught the answer fact).
- Conclusion: Decoys built AFTER real MAPs do NOT break queries.
  The bug is **build-time interference**: building ~5000 decoys
  BEFORE the real MAPs corrupts the real MAP builds.

### 3c. Root cause hypothesis

The real MAPs are built via `s5_mkchain` -> `t2_chain` ->
`t2_lu_first`. During build, mode=5 (FACT index enabled), so
`t2_lu_first_idx` is used. With ~5000 decoy FACTs already in the
24-bucket FACT index (~208 per bucket), the indexed lookup likely
returns a wrong fact (or the bucket list is corrupted), causing
`t2_chain` to follow a wrong path. The resulting MAP has plen=5
(correct shape, so it gets indexed) but wrong literals/values, so
verification fails at query time.

The MAP index (`idx_walk_bucket`) is NOT the culprit: it correctly
finds all 5 candidates (scan=5). The bug is in the FACT index used
during `t2_chain` at build time.

This is a **new finding**: the FACT subject index has a
scale-dependent correctness bug not caught by the 1000-MAP tests.
It needs a dedicated red-team/fix cycle like the MAP index got.

## 4. Stress tests (T2-T4) -- NOT COMPLETED

T2 (corruption at scale), T3 (churn), T4 (collision) were not run
because:
1. The 5000-MAP run timed out after 30 minutes (build is slow).
2. The correctness bug blocks meaningful stress measurements
   (queries must work to stress the index).

These remain open for a follow-up worker once the FACT index bug
is fixed.

## 5. Key results

1. **Index scales**: 5-visit flat holds at 5000 MAPs. 13,107x
   reduction over linear (65534 visits).
2. **Hardened walk is safe**: No crashes, no panics at 5000 MAPs.
   The I1-I5 invariants hold.
3. **New bug found**: FACT index has build-time scale-dependent
   correctness bug (threshold 1000-4990 decoys). The MAP index is
   fine; the FACT index needs hardening.
4. **Build optimizations work**: High-water alloc and down-scan
   prev-scan enabled the 5000-MAP build to complete (fails=0).

## 6. Files (s5_* workstream)

- NAMECHECK.md (Step 0 toolchain guard)
- REPORT.md (this file)
- s5_base.zag, s5_base_raw.zag (65536-node base)
- s5_patch.zag (mechanisms + hardened walk)
- s5_driver.zag (T1-T4 driver)
- s5_full.zag (assembled, 2217 lines)
- s5_bin, s5_compile.txt
- s5_run1.txt (partial: T1 completed, T2-T4 timed out)
- dbg_*.zag, dbg*_bin (diagnostics: dbg, dbg2, dbg3, dbg5)
- s5k_hardwalk.zag (extracted hardened walk, unused)

## 7. Toolchain

Safebin active throughout. `which python3 python` returns nothing.
Pure Zag for all computation. Zero em/en dashes. Paper untouched.
Nothing pushed.

## 8. Recommended follow-ups

1. **Fix FACT index bug**: Red-team the FACT subject index at
   2000-5000 FACTs. Likely culprits: `fidx_add` list corruption,
   `t2_lu_first_idx` bucket walk, hash collision handling.
2. **Re-run T2-T4**: Once FACT index is fixed, run corruption,
   churn, and collision stress tests at 5000 MAPs.
3. **3/3 determinism**: Full 3-run validation (blocked by timeout;
   need faster build or longer timeout).
4. **10000 MAPs**: If 5000 stabilizes, push to 10000.
