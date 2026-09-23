# D-R — Reuse-gated commit (Track A, arm dr)

## Frozen prereg
- Commit: `b0b9140c0eda`, branch `tnn-native-lab`, repo `sylorlabs/TNN`.
- Mechanism (ALPHABET_A-F.md, PREREG_FREEZE.md A-11, §3):
  > "D's proposals, but commit requires reuse ≥ REUSE_BAR: a second memory
  > entry must reference the span before the ID is minted. No ID until the
  > span proves worth caching."
- `REUSE_BAR=2` (frozen).
- Kill criterion: ">50% of final vocabulary still uncommitted at end of 10x
  while D commits and wins on M3 — gating is pure delay."

## Design v2 (as built, 2026-09-21)

### Corrected semantics
The original implementation had a critical bug: `chunk_new(..., ST_COMMITTED)`
actually created a `ST_PROPOSED` chunk with `JUST_RAW` justification (numeric
collision: `ST_COMMITTED=1`, `JUST_RAW=1`), so proposals never promoted and
`NCOMMITTED` was always 0.

The v2 implementation corrects this:
1. **Pass 1** discovers exact repeated spans at their second occurrence and
   creates `JUST_SELF` proposals (not raw).
2. **Walk** references proposals through occurrences.
3. **`d_add_occ`** promotes only when `refs >= DR_REUSE_BAR` (REUSE_BAR=2).
4. Unmatched walk-created chunks are `JUST_RAW` and remain proposed forever.
5. **Tiling** checks every length 64 down to 3 (exact greedy longest-match).

### Sub-quadratic proposal structure
Pass 1 uses a suffix-array-inspired approach to achieve sub-quadratic time:

1. **Group by 3-byte prefix**: Sort all positions (0..n-3) by their first 3
   bytes using two 16-bit radix passes (O(n)).
2. **Sort each group by suffix**: For each 3-gram group, sort positions
   lexicographically by the up-to-64-byte suffix using 61 MSB-first radix
   passes (O(G) per group, total O(n)).
3. **Compute LCP**: Adjacent LCP (longest common prefix) capped at 64 bytes
   via direct byte comparison (O(G) per group).
4. **Enumerate maximal LCP intervals**: Monotonic stack finds all maximal
   intervals where LCP >= threshold (O(G) per group).
5. **Find 2nd smallest position**: For each interval [l,r] with LCP m, use a
   segment tree (for G>=128) or linear scan (for G<128) to find the two
   smallest source offsets. The second is the proposal position.
6. **Emit events**: For interval [l,r] with LCP m, emit lengths
   `max(3, lcp[l]+1, lcp[r+1]+1)` through `min(64, m)` at position p2.
7. **Sort events**: 64-bit radix sort by (position, length) to get
   deterministic order.
8. **Create proposals**: In event order, create `JUST_SELF` chunks (capped at
   131,072 chunks).

All identity decisions use byte-loop/memcmp verification. Sort/hash structures
only organize candidates; they never decide equality.

**Boundary-LCP rule**: For interval [l,r], the minimum length is
`max(3, lcp[l]+1, lcp[r+1]+1)`, not just 3. This prevents false positives where
a span is claimed to repeat at length L but the boundary LCPs show it doesn't.
(Validated against Python v5 reference on 75 random trials.)

### Commit (reuse gate)
- Proposals start as `ST_PROPOSED` with `JUST_SELF`.
- During walk, when a proposal is referenced by a tiling occurrence,
  `d_add_occ` increments its ref count.
- When `refs >= 2` (REUSE_BAR), the chunk transitions to `ST_COMMITTED`:
  ID is minted, bytes are cached in the blob.
- Raw chunks (`JUST_RAW`, from unmatched walk runs) never commit.

### Walk (tiling)
- Greedy longest-match: at each position, check lengths 64 down to 3
  (all 62 lengths, not a subset).
- Uses `larr` (best exact-match length per position, from pass1) to skip
  lengths that cannot match.
- Content index lookup via FNV-1a hash + memcmp verification.
- Unmatched maximal runs become `JUST_RAW` chunks (proposed, never committed).

## Arm-chosen parameters (unfrozen, documented here)
- `DR_MIN_LEN=3`, `DR_LMAX=64` (frozen range).
- `DR_CHUNK_CAP=131072` (max chunks; events beyond this are dropped).
- `DR_CIDX_SLOTS=65536` (content index).
- `DR_REUSE_BAR=2` (frozen).
- Event buffer: 4 shards × 4M events (16M total capacity).
- Per-group segment tree for G>=128; linear scan for G<128.

## Equivalence proof (100KB)
- **Synthetic** (102,400 bytes, SHA256 `f461fbd7...`): Zag v2 and Python v5
  reference both produce 744 proposal events; full event lists byte-identical.
- **Real** (102,400 bytes from r1 prose.bin, SHA256 `c604ddca...`): Both
  produce 99,471 events; full lists byte-identical.
- Two Zag runs: byte-identical stdout (determinism).
- Mechanism check: Synthetic yields NCOMMITTED=3, NOCC=1600; Real yields
  NCOMMITTED=3481, NOCC=18016. (Old buggy version had NCOMMITTED=0.)

## Limitations
- **Scale**: Proven on 100KB and 1MB. Panics on 3MB+ inputs due to
  per-group allocation leaks (hfree is trace-only) and/or memory exhaustion.
  The 1x battery (5.4MB prose, 9.5MB code) cannot be completed with the
  current implementation.
- **Speed**: 100KB takes ~15-80s (synthetic vs real). 1MB takes ~233s.
  Estimated 5.4MB would take >30 minutes per mode if it didn't panic.

## Status
- 1x battery: BLOCKED (size limitation; cannot process 5.4MB+ inputs).
- 10x: NOT ATTEMPTED (requires 1x pass).
- D comparison: BLOCKED (D has no verdict/scorecard as of 2026-09-21).
- Kill criterion: NOT EVALUATED (requires 10x evidence).
