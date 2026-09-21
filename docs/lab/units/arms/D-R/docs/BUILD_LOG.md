# D-R Build Log

## 2026-09-21: v2 implementation (sub-quadratic, corrected semantics)

### Problem identified
The original D-R implementation had a critical semantic bug:
- `chunk_new(s,buf,bo,len,just)` always creates `ST_PROPOSED`; final arg is justification.
- Numeric collision: `ST_COMMITTED=1`, `JUST_RAW=1`.
- Old `pass1` called `chunk_new(..., ST_COMMITTED)`, which actually created a
  raw proposal (not a committed chunk).
- Result: repeated proposals never promoted; dumps showed `NCOMMITTED 0`.

### Corrected interpretation
1. Pass 1 discovers exact repeated spans at second occurrence → `JUST_SELF` proposal.
2. Walk references proposals through occurrences.
3. `d_add_occ` promotes only when `refs >= DR_REUSE_BAR` (2).
4. Unmatched walk chunks are `JUST_RAW`, remain proposed forever.
5. Tiling checks every length 64..3 (exact greedy).

### Algorithm: sub-quadratic proposal discovery
**Validated direction** (Python v5, 75/75 random trials):
- Group starts by exact 3-byte prefix.
- Sort each group lexicographically by suffix (capped 64B).
- Compute adjacent LCP (capped 64).
- Enumerate maximal LCP intervals via monotonic stack.
- For each interval, find two smallest source offsets; second is proposal position.
- Emit lengths `max(3,lcp[l]+1,lcp[r+1]+1)` .. `min(64,m)`.
- Order by (position, length).

**Boundary-LCP rule** fixes false positive where `(232,4)` was emitted for
`b' b '` with occurrences `[40,57,232]` (correct: only lengths where both
boundaries agree).

### Implementation (Zag)
- **Sorting**: Two 16-bit radix passes for 3-byte prefix; 61 MSB-first 8-bit
  passes for 61-byte suffix keys (bytes 3..63).
- **LCP**: Direct byte comparison, capped at 64.
- **Intervals**: Monotonic stack (O(G) per group).
- **2nd smallest**: Segment tree (G>=128) or linear scan (G<128).
- **Events**: Sharded arrays (4×4M = 16M capacity); 64-bit radix sort by
  (position, length).
- **Memory**: `[]u8` arenas with explicit LE accessors (avoids ZNC-007
  miscompile). No slice >33.5MB indexed (ZNC limit).

### Equivalence proof (100KB)
**Fixtures**:
- `syn100k.bin`: 102,400 bytes, SHA256 `f461fbd7d83dfd0407d943fe70756c720d962526d061bc7fa04f2659f452ccd8`
- `real100k.bin`: 102,400 bytes (r1 prose.bin head), SHA256 `c604ddca5a56905ff5e6eedc8468c0f5bbf69352e0705d239fb1e8bf1ab591cd`

**Results**:
- Synthetic: Zag 744 events, Python v5 744 events; full lists byte-identical.
- Real: Zag 99,471 events, Python v5 99,471 events; full lists byte-identical.
- Two Zag runs: byte-identical stdout (determinism verified).
- Mechanism: Synthetic NCOMMITTED=3, NOCC=1600; Real NCOMMITTED=3481, NOCC=18016.
  (Old buggy version: NCOMMITTED=0.)

### Scale testing
- 100KB: ~15-80s (synthetic vs real).
- 1MB: ~233s, 1,192,272 events. Works.
- 3MB: Panics (fast, <18s). Root cause: per-group allocation leaks (hfree is
  trace-only) + memory exhaustion. Not a correctness bug; a resource bug.
- 5.4MB (r1 prose): Cannot process. 1x battery BLOCKED.

### 1x battery status
**BLOCKED**. The implementation cannot process the 5.4MB prose or 9.5MB code
corpora required for the 1x battery. The core mechanism is proven correct on
100KB, but the scale limitation prevents full battery execution.

### D comparison
**BLOCKED**. As of 2026-09-21, `docs/lab/units/arms/D/` contains only
`BUILD_LOG.md` and `cl/`; no verdict, scorecard, or M3 evidence. Both the
binding D comparison and the additional cost/recall comparison cannot be
performed.

## 2026-09-21: Initial implementation and debugging (historical)

### Panic fix
- **Issue**: `panic: slice index out of bounds` in `trace_put` during init.
- **Root cause**: Direct assignment of `_zag_malloc` to a slice (`let b:[]u8=_zag_malloc(n)`)
  produces `len=0` in the frozen compiler. The trace buffer had len=0, causing
  OOB on first `trace_put`.
- **Fix**: Use `nio_alloc` (pointer-to-slice construction) for all allocations.

## Compiler notes
- Frozen toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- ZNC-007: Avoid `nio_alloc(...) as []i32/[]u32/[]u16`; use `[]u8` arenas.
- ZNC limit: No slice >33,554,432 bytes indexed.
- Build time: ~60-90s for 80KB source.
