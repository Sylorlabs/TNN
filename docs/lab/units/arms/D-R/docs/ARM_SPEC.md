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

## Design (as built)
- **Proposal**: Single-pass scan (pass1) over the corpus. For each position p
  and length len in [3, 64], compute rolling hash. Use a lossy first-seen
  table (1M slots, no probing on collision — overwrite). On 2nd occurrence
  with verified content match (memcmp), COMMIT the chunk immediately.
- **Commit**: `chunk_new` allocates from an 8MB blob, copies bytes (cached),
  assigns a stable chunk ID, inserts into the content index (65K slots,
  bounded probe at 32). State = ST_COMMITTED.
- **Walk** (pass 2): Greedy longest-match tiling against the content index.
  `match_at` checks lens [64,48,32,24,16,12,8,6,5,4,3] descending (not all
  64), inlined probe, returns on first hit. Unmatched maximal runs become
  raw chunks (JUST_RAW, content-indexed, never committed).
- **Reuse gate**: Enforced in `d_add_occ`. When an occurrence references a
  chunk, if the chunk is not yet committed and this is the 2nd distinct
  occurrence, the chunk transitions to ST_COMMITTED (ID minted, bytes cached).
  Raw chunks (JUST_RAW) never commit.
- **Occurrences**: Tiling entries (chunk_id, off) in `tile`/`offs` arrays.
  `d_recall` resolves occurrence → chunk.

## Arm-chosen parameters (unfrozen, documented here)
- `DR_MIN_LEN=3` (minimum proposal length).
- `DR_LMAX=64` (maximum proposal length).
- `DR_FS_SLOTS=1048576` (first-seen table, 1M slots, 16MB transient).
- `DR_CIDX_SLOTS=65536` (content index, 64K slots).
- First-seen table is LOSSY (overwrite on collision, no probing). This is an
  arm-chosen performance tradeoff; it may miss some repeats.
- `match_at` checks only 11 lens (not all 62), for speed. This finds a good
  match, not necessarily the longest.

## Deviations from frozen D
- D's exact proposal algorithm was not available in the frozen docs; D-R uses
  a single-pass 2nd-occurrence commit (which satisfies "second memory entry
  must reference the span before the ID is minted").
- The candidate table / context-diversity / REP_BAR=3 mechanism was removed
  during performance optimization. The current design commits on 2nd
  occurrence directly, which is a literal implementation of REUSE_BAR=2.

## Performance
- **Correctness**: Verified on 100KB synthetic (repetitive) and 100KB real
  corpus (t3.bin subset): 100% recall, etc=1 (criterion met in 1 episode).
- **Speed**: ~30s per 100KB per walk episode (after optimizations). For 1MB,
  ~5 min per episode. For 5.2MB prose (M1, 20 episodes), estimated >6 hours
  for a single mode. The full 1x battery (16 modes) is infeasible in
  reasonable time.
- **Bottleneck**: O(n × LMAX) with high constant factors in Zag (bounds
  checking, function calls). The `match_at` does up to 11 hash-table probes
  per position; each probe is bounds-checked.

## Status
- 1x battery: ATTEMPTED — FAILED (performance; see BUILD_LOG.md).
- No M1–M9 scorecard (1x did not complete).
- No 10x (requires 1x pass).
- Kill criterion: NOT EVALUATED (requires 10x evidence from D-R and D).
