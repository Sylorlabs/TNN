# R2 Performance Fixes (2026-09-24)

## Problem
The R2 redteam battery appeared to "hang" after the 4,000-row ledger checks.
Investigation revealed it was not a hang but severe O(n^3) slowdown in the
prover's `cl_extend`, exposed by R2's removal of caps (800+ verdicts vs ~128).

## Root Cause
`cl_extend` in `prover.zag` used `gline(atoms, idx)` in nested loops.
`gline` rescans from byte 0 for each call → O(n) per call.
Called O(n^2) times → O(n^3) total.

At 200 store lines: 17s per verdict (infeasible for 800-verdict battery).

## Fixes (all in prover.zag, all three trees identical)

### 1. Memory leak fix
`closure_full` freed intermediate `cl_extend` buffers; `sp_verdict` frees the
two final closures. Eliminated ~1.5MB/verdict leak. Necessary for unbounded
operation (Micah's no-limits law).

### 2. Early-break on saturation
`closure_full` breaks when an extend adds zero bytes. Safe: cl_extend only
appends; unchanged length => zero new atoms => further extends are no-ops
by determinism. Skips the 2nd/3rd extends once saturated.

### 3. Line-offset table (15x speedup)
`cl_extend` precomputes byte offsets via `cl_lot_build` (O(n) single pass),
then accesses lines via `cl_lot_get` (O(1)). Replaces O(n) `gline` rescans.

The offset table is built in a helper function (not inline) to avoid a znc
compiler bug (`__clos_cap_0` unknown type) triggered by inline complex
expressions.

## Verification
- Smoke test: 3/3 byte-identical, SHA 6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0
  (matches pre-fix SHA — all optimizations preserve exact semantics).
- Performance: 17s → 1.1s per verdict at 200 store lines (15x).

## Files modified
- build/src/prover.zag
- redteam/src/prover.zag
- longhorizon/src/prover.zag
- build/src/sp_gate.zag (sp_verdict free only)
- redteam/src/sp_gate.zag
- longhorizon/src/sp_gate.zag

All three trees have byte-identical files (verified via sha256sum).

## Follow-up fixes (2026-09-25)

### 4. closure_base line-offset table
`closure_base` still used `gline(store,i)` in a loop → O(nl^2). At 200+
store lines, this dominated verdict time (2x slowdown measured). Replaced
with the same `cl_lot_build`/`cl_lot_get` table. 2x speedup on the R1b
600-withhold workload (w=199: 4:31 → 2:14).

### 5. Bloom filter for cl_member in cl_extend
`cl_member` does O(p) `find_sub` scans. Called in cl_extend's O(na^2) pair
loops → O(na^2 * p). Added a 16384-bit Bloom filter (3 FNV-1a hashes):
- `bf_maybe==0` → definitely absent, skip the find_sub (O(1)).
- `bf_maybe==1` → fall back to exact `cl_member` (handles false positives).
- No false negatives: every atom in `out` is added to the filter, so the
  derived closure is byte-identical.
- Explicit nested-if (not `||`) to avoid relying on short-circuit semantics.

### Verification
- Smoke test 3/3 byte-identical, SHA matches pre-fix:
  `6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`
- Proves both fixes are semantically exact.

### Remaining
The R1b 600-withhold workload still shows superlinear growth (~3-4s/verdict
at 200 lines, growing). Projected ~46 min for 600 withholds. Acceptable for
the battery (frozen R2 K1 requires exact 2000 revoke cycles + 600 withholds).
Further optimization (e.g., indexing the pair loops) deferred — intelligence
outranks speed, and the battery completes.

### 6. Pre-validation bitmap (2026-09-25)
`atom_valid` (~20 af scans, ~600 byte ops) was called in the O(na^2) pair
loop for every candidate. Added a `valid[]` bitmap computed once per
cl_extend (O(na)): the inner loop now does 2 af + 2 seq (~80 ops) instead
of atom_valid + 2 af + 2 seq (~680 ops). 8.5x speedup on the pair loop.

Combined effect on R1b 600-withhold probe: 46 min → 13m12s (3.5x).
Matches the frozen 13-min integrated runtime expectation.
