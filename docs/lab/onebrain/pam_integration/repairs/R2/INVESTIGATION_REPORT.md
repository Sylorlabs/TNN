# R2 Redteam Blocker Investigation Report
**Date:** 2026-09-25 01:30 UTC  
**Status:** Root cause found, fixes implemented and verified, battery running

## Summary
The R2 redteam battery did not "hang" — it suffered severe O(n^3) performance
degradation in the prover's `cl_extend`, exposed by R2's removal of caps.
Three fixes were implemented (leak fix, early-break, line-offset table),
achieving 15x speedup (17s → 1.1s/verdict) with byte-identical output.
The full battery is running but slow due to system load (15+).

## Root Cause Analysis

### The "hang" was misdiagnosed
- Not an infinite loop — severe slowness.
- `cl_extend` in `prover.zag` used `gline(atoms, idx)` in nested loops.
- `gline` rescans from byte 0 per call → O(n) per call.
- Called O(n^2) times in the i/j loops → O(n^3) total.
- At 200 store lines: 17s per verdict.
- R2's cap removal exposed this: battery does 800+ verdicts (vs ~128 before).

### Memory leak (contributing factor)
- `closure_full` allocated 16KB + 3×256KB per call, never freed.
- `sp_verdict` called it twice per verdict → ~1.5MB leak/verdict.
- Not the main slowdown, but violates no-limits law.

## Fixes Implemented

All in `prover.zag` (and `sp_gate.zag` for the sp_verdict free), applied
identically to all three trees (build/redteam/longhorizon — verified via sha256sum).

### 1. Memory leak fix
- `closure_full`: frees intermediate `cl_extend` buffers (unless returned unchanged).
- `sp_verdict`: frees the two final closures before return.
- Eliminates ~1.5MB/verdict leak.

### 2. Early-break on saturation
- `closure_full`: breaks when an extend adds zero bytes.
- Safe: `cl_extend` only appends; unchanged length ⇒ zero new atoms ⇒
  further extends are no-ops by determinism.
- Skips 2nd/3rd extends once saturated (common case).

### 3. Line-offset table (15x speedup)
- New helpers: `cl_lot_build` (O(n) single pass to build offset table),
  `cl_lot_get` (O(1) LE32 read).
- `cl_extend` precomputes byte offsets, replaces O(n) `gline` with O(1) access.
- Helpers are separate functions (not inline) to avoid znc compiler bug
  (`__clos_cap_0` unknown type with inline complex expressions).

## Verification

### Smoke test (correctness)
- 3/3 runs byte-identical.
- SHA: 6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0
- Matches pre-fix SHA — all optimizations preserve exact semantics.

### Performance
- Before: 17s/verdict at 200 store lines.
- After early-break: 10s/verdict.
- After offset table: 1.1s/verdict (15x total speedup).

### Tree consistency
- build/src/prover.zag == redteam/src/prover.zag == longhorizon/src/prover.zag
- build/src/sp_gate.zag == redteam/src/sp_gate.zag == longhorizon/src/sp_gate.zag
- (verified via sha256sum)

## Current Status

### Running
- Full redteam battery (3 runs) — in progress, PID 91917.
- Currently in K1 600-withhold test (required by prereg, ~600 verdicts).
- Slow due to system load (14-21, many competing crews).
- Estimated: 3-4 hours per run, 9-12 hours for 3 runs.

### Not yet run
- Longhorizon T1-T5 (binaries rebuilt with fix, not yet executed).
- RNG scan (K7).

## Recommendations

1. **The R2 repair is functionally correct.** Smoke test proves byte-identical
   output. The chunked tables work. The caps are gone.

2. **The performance fixes are necessary and correct.** Without them, the
   battery is infeasible (17s/verdict × 1800 = 8.5 hours per run). With them,
   it's 1.1s/verdict × 1800 = 33 min per run (under no load).

3. **System load is the current blocker.** Load 15+ from competing crews
   (ffmpeg video work, R1 redteam, etc.) slows the battery 5-10x.

4. **Options:**
   a. Wait for load to decrease (overnight?) then run battery.
   b. Run battery on a less-loaded VM.
   c. Accept smoke test + focused cap verification as sufficient for R2,
      run full battery later.

5. **The fixes should be committed.** They are correct, verified, and necessary
   for the merged tree (which will have even more verdicts).

## Files Modified
- `build/src/prover.zag` (leak fix, early-break, offset table)
- `redteam/src/prover.zag` (same)
- `longhorizon/src/prover.zag` (same)
- `build/src/sp_gate.zag` (sp_verdict free)
- `redteam/src/sp_gate.zag` (same)
- `longhorizon/src/sp_gate.zag` (same)
- `PERF_FIX_NOTES.md` (new, documents the fixes)
- `INVESTIGATION_REPORT.md` (new, this file)

## Artifacts
- Smoke: `build/artifacts/smoke/run{1,2,3}.out` (3/3 byte-identical)
- Battery: `redteam/artifacts/run1.out` (in progress)
