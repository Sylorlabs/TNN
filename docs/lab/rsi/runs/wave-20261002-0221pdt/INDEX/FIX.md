# FIX.md - INDEX lane, wave-20261002-0221pdt (Part B, fix)

Governing bar: PREREG_INDEX_REPRO.md B2 + B4 (frozen).

## What was changed

File: `work/sc_patch_fixed.zag` (delta against the canonical
`scaling_cont/sc_patch.zag`; 159 diff lines, pure Zag, no new modes,
bridges, handlers, or semantic cases). The fixed patch is a drop-in
replacement for sc_patch.zag in the frozen build assembly.

1. `idx_bnext` (new): OOB-safe bucket-list step. Any negative or
   out-of-range id, or any out-of-range next pointer, yields -1
   (list end) instead of panicking inside `ng`.

2. `idx_collect` (new): replaces the raw candidate-collection loop
   in `rebind_try_idx`. Floyd tortoise-and-hare cycle detection,
   writes bounded by the true buffer capacity (capc=8192 for the
   65536-byte buffer), only live tag-20 MAP members collected, scan-
   visit counter incremented per visited node exactly as before.
   Cannot panic on any list shape.

3. `mtf_win`: the predecessor search loop gets an OOB guard on the
   head, a step cap (NN), OOB-safe stepping, and a post-loop equality
   check so a guard trip never splices. (Defense in depth; the gate
   below already excludes corrupt buckets from this path.)

4. `rebind_try_idx`: calls `idx_validate` first; on REJECT it returns
   `rebind_try_lin(...)` instead of touching the index. The corrupt
   index is never used in production; the query still gets an answer
   via the linear path.

5. `t2_gather` / `t2_lu_first`: the bit2 dispatch consults
   `fidx_validate`; on REJECT they use the linear variants.

6. Gate functions `idx_validate`, `idx_bucket_ok`, `fidx_validate`,
   `fidx_chain_ok` (documented in VALIDATION_GATE.md): pure reads,
   no counters touched.

## Why this shape

Two layers, because they answer different threats:

- The hardened walk (`idx_collect`, `idx_bnext`, `mtf_win` guard)
  answers "no input shape may panic the consumer". It is lenient:
  OOB next = list end, dead members skipped, cycles stop after one
  pass. Leniency here is safe because every id it emits is range-
  checked and downstream use of candidate ids is already guarded
  (the MTF fast path checks liveness and tag; `rb_attempt` verifies
  structurally).
- The validation gate answers "corrupt index state must not drive
  production behavior". It is strict: any cycle, OOB id, dead node,
  wrong tag, plen mismatch, or garbage next pointer anywhere in the
  index rejects the whole index for that query and the linear path
  serves instead. Strictness here is cheap because the gate only
  runs when the index would be used, and correctness (never a wrong
  answer from a corrupt index) dominates the extra walk.

The strict/lenient split is deliberate: the gate decides TRUST, the
walk guarantees SAFETY. A bypassed gate still cannot panic; a
paranoid gate never lets a corrupt index steer answers.

## Verification

- Minimal fixed-pattern tests: 6/6 shapes pass, exit 0
  (CRASH_REPRO.md).
- Gate matrix on the real structures: 8/8 expectations hold, 3/3
  byte-identical (VALIDATION_GATE.md).
- Full-scale fixed rebuild (`work/sc_full_fixed.zag`, 2287 lines,
  pinned znc, exit 0): 3/3 runs must equal the canonical output
  hash eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d
  (frozen B4). This proves the fix+gate are exact no-ops on healthy
  state: same candidates, same counters, same answers.

## Cost accounting (honest)

- The gate walks all buckets per indexed query: O(index size) extra
  reads per query, touching no measured counters. On the 1000-MAP
  benchmark this roughly doubled wall time (about 30 s to about
  70 s per run) without changing any measured number. A production
  refinement would cache a validity epoch bumped on index mutation
  instead of revalidating per query; that epoch machinery is out of
  scope for this fix.
- New cognition lines: about 125 (helpers + gate). New modes/
  bridges/handlers/semantic cases: 0. The mode bits are unchanged
  (learner-state flags, not cognitive modes).

## Red-team self-review (fix)

- The gate runs per query, but corruption could in principle land
  BETWEEN the gate and the index use. Single-threaded Zag: no
  interleaving exists, so the window is empty. A concurrent future
  would need the check re-placed or a lock; noted, not built.
- `idx_bucket_ok` calls `rb_chain_plen` per member (up to 64 steps
  each). A deeply adversarial chain cannot make it panic (the
  64-step cap and the root range check precede it), but it does make
  the gate O(members x chain). Same complexity class as the walk
  it guards; acceptable.
- The plen-match check (`rb_chain_plen(root)==plen`) assumes the
  bucket invariant "member filed under its promotion plen" holds
  for healthy state. If a future mechanism legitimately re-files
  MAPs across buckets, the gate becomes over-strict and must be
  revised with it. The B4 byte-identical result is the evidence
  that the invariant holds for the current mechanisms.
- Fallback-on-reject changes the performance profile under
  corruption (linear scan) but never the answer: `rebind_try_lin`
  is the verified baseline path. Availability is preserved;
  degraded performance under corruption is the correct tradeoff.
- What would falsify this fix: a corrupt index shape that (a)
  panics the fixed walk, (b) passes the gate yet steers a wrong
  answer, or (c) changes healthy-state output. B2, B3, B4 test
  exactly these three; all hold.
- Not fixed here (out of scope, recorded): the eviction path that
  CREATES stale bucket entries is untouched; the gate treats its
  output as corrupt and routes around it. Eliminating the staleness
  at the source (index-coherent eviction) is a separate work item.
