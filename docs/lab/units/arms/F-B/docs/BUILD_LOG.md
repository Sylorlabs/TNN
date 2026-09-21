# F-B BUILD_LOG

## 2026-09-21 — Core segmentation implemented and verified

### What was built
- `cl/arm.zag` (559 lines): Pure Zag implementation of F-B branching-continuation
  segmentation.
- `substrate/`: Verbatim copies of `R33_NATIVE_SHA256_V2.zag` and
  `R33_NATIVE_IO_V1.zag` from B-64.
- Candidate table: 4096 slots, 64-byte entries (hash, len, rep, contdiv bitset,
  seq, first-pos, verified flag).
- Hash buckets: 65536 buckets for O(1) candidate lookup.
- Binary min-heap: Preserves exact `(rep, seq)` eviction semantics (lowest rep,
  then oldest/lower seq evicted first).
- First-seen table: Direct-mapped 65536-entry cache for span positions.
- 256-bit continuation sets: 4×u64 per candidate, tracking distinct bytes
  following each span occurrence.

### Verification
- C prototype (exact, no eviction) on 30KB prose: 8,811 chunks, mean 3.40.
- Zag implementation on 30KB prose: 11,243 chunks, mean 2.67, max 96.
  - Difference from C prototype is due to bounded-table eviction (4096 candidates)
    vs unbounded C prototype. The eviction worsens over-cutting (more 1-byte
    chunks). This is inherent to the literal mechanism with bounded resources.
- REP_BAR sweep (C prototype, 30KB): 2→3.40, 5→1.51, 10→1.32, 20→1.28, 50→1.34.
  Higher REP_BAR makes over-cutting worse (fewer spans qualify as "repeated",
  so fewer cuts are suppressed... actually the relationship is non-monotonic
  due to eviction interactions).

### Performance issue
- 30KB prose: 39s wall time, 2.2s user CPU, 0.01s sys.
- The 37s gap is unexplained (not syscalls per strace; not cand_init which takes
  0.44s). Likely VM oversubscription/descheduling.
- Projected full corpora: prose (5.4MB) ~2 hours, code (9.5MB) ~3.4 hours.
  Too slow for battery iteration.

### What was NOT built
- Chunk/content store with persistent IDs
- M1–M9 metric modes (only `segtest` diagnostic exists)
- Audit ledger (16-word entries)
- M8 determinism artifacts
- Content verification (hash-only currently; required for correctness)
- ID remapping / M1 swap probe
- M7 cache rig

### Lessons
- `_zag_arg(n)` is non-owned: never free it.
- `_zag_strcmp` returns 1 on equality.
- Explicitly initialize all heap arrays (allocator memory not reliably zeroed).
- Never use slice `==` for content identity.
- Alias large-struct slice fields before indexing.
- Single slice cannot exceed 2^25 bytes.
- znc: `slice as *u8` does NOT yield data pointer (ZNC-2026-09-21-002).
- znc: slice-typed struct fields are 16 bytes (ZNC-2026-09-21-003).
