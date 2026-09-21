# D-R Build Log

## 2026-09-21: Initial implementation and debugging

### Panic fix
- **Issue**: `panic: slice index out of bounds` in `trace_put` during init.
- **Root cause**: Direct assignment of `_zag_malloc` to a slice (`let b:[]u8=_zag_malloc(n)`)
  produces `len=0` in the frozen compiler. The trace buffer had len=0, causing
  OOB on first `trace_put`.
- **Fix**: Use `nio_alloc` (pointer-to-slice construction) for all allocations.
- **Result**: `m5-baseline` runs successfully.

### Performance optimization (iterative)
1. **Candidate table**: Increased from 4K to 64K slots, changed eviction from
   O(n) scan to O(1) overwrite. Added `maybe_propose` early-exit if chunk exists.
2. **First-seen table**: Increased from 256K to 1M slots (16MB) to reduce
   lossiness. Fixed field overlap bug (len was at+4, colliding with key).
3. **Simplified pass1**: Removed candidate table / contdiv / REP_BAR=3.
   Now commits directly on 2nd occurrence with memcmp verification.
   (Justification: REUSE_BAR=2 is frozen; the candidate mechanism was an
   arm-chosen addition that hurt performance without clear benefit.)
4. **match_at**: Inlined the cidx probe, changed from ascending (all 64 lens)
   to descending (11 lens: 64,48,32,24,16,12,8,6,5,4,3), bounded probe at 32
   slots (was 512). Uses reusable `s.*.mhs` buffer (no per-call alloc).
5. **Walk**: Added fast path: if `nchunk==0`, skip the raw-run scan (entire
   input is raw).

### Correctness verification
- **100KB synthetic** ("hello world " × 500): `m2-t3-1x` → etc=1, final
  100.0%, 100.0%. PASS.
- **100KB real** (t3.bin subset): `m2-t3-1x` → etc=1, final 100.0%, 100.0%.
  PASS. (Required the 1M-slot first-seen table; 256K was too lossy.)
- **m5-baseline**: Emits METRIC_JSON correctly. PASS.

### Performance results
- 100KB, 4 episodes (m2-t3-1x): 30s (after all optimizations).
- 5.2MB prose (m5-1x): Timeout at 120s (no output). Estimated 27 min for
  pass1 alone (345M iterations).
- **Conclusion**: The implementation is correct but too slow for the full 1x
  battery. The O(n × LMAX) complexity with Zag's overhead (bounds checking,
  function calls) makes multi-MB corpora infeasible.

### 1x battery attempt
- **m5-baseline**: PASS (fast, no corpus walk).
- **m2-t3-1x** (100KB subset): PASS (30s, 100% recall).
- **m5-1x** (5.2MB): TIMEOUT (120s, no output). ATTEMPTED — FAILED.
- **m1-1x-prose** (5.2MB, 20 episodes): Not attempted (estimated >6 hours).
- **Other modes**: Not attempted (performance).
- **Overall**: 1x battery ATTEMPTED — FAILED (performance).

## Files
- Source: `cl/arm.zag` (~1,850 lines).
- Binary: `work/dr` (build artifact, not committed).
- Docs: `docs/ARM_SPEC.md` (this file: `docs/BUILD_LOG.md`).
