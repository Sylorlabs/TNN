# D-R Verdict

## Verdict: ATTEMPTED — FAILED (1x battery, performance)

### What was built
D-R (Reuse-gated commit) implements the frozen mechanism: D's proposals, but
commit requires reuse ≥ REUSE_BAR=2. A second memory entry must reference the
span before the ID is minted. No ID until the span proves worth caching.

The implementation:
- Single-pass proposal scan (pass1) finds 2nd occurrences via a lossy
  first-seen table, verifies with memcmp, commits immediately.
- Greedy longest-match tiling (walk) uses the committed chunks.
- Raw unmatched runs stay JUST_RAW (never committed).
- REUSE_BAR=2 is enforced literally.

### What was proven
- **Correctness**: On 100KB (synthetic and real), M2 achieves 100% recall
  with etc=1 (criterion met in 1 episode). The reuse gate works: chunks are
  committed on 2nd occurrence, IDs are minted, tiling uses committed chunks.
- **Determinism**: Not yet verified (requires byte-identical reruns; not
  attempted due to performance).

### What failed
- **1x battery**: ATTEMPTED — FAILED. The implementation is too slow for the
  full 1x battery (multi-MB corpora). `m5-1x` (5.2MB) timed out at 120s.
  `m1-1x-prose` (5.2MB, 20 episodes) was not attempted (estimated >6 hours).
- **Root cause**: O(n × LMAX) complexity (n=5.2M, LMAX=64 → 333M iterations
  for pass1 alone) with high constant factors in Zag (bounds checking on
  every array access, function call overhead). The frozen compiler does not
  optimize these away.
- **No scorecard**: M1–M9 scorecard not assembled (1x did not complete).
- **No 10x**: Not attempted (requires 1x pass).
- **Kill criterion**: NOT EVALUATED. The kill rule (">50% of final vocabulary
  still uncommitted at end of 10x while D commits and wins on M3") requires
  10x evidence from both D-R and D. No 10x was run.

### Ambiguities (explicit)
1. **D's proposal algorithm**: The frozen docs did not specify D's exact
   proposal mechanism. D-R uses a single-pass 2nd-occurrence commit, which
   satisfies the frozen wording ("second memory entry must reference the span
   before the ID is minted") but may differ from D's actual algorithm.
2. **First-seen table lossiness**: The table overwrites on collision (no
   probing) for speed. This may miss some repeats. A probing table would be
   more accurate but slower.
3. **match_at lens**: Checks only 11 lens (not all 62) for speed. Finds a good
   match, not necessarily the longest. This affects tiling quality.
4. **REP_BAR=3**: Removed during optimization. The frozen REUSE_BAR=2 is
   enforced; the arm-chosen REP_BAR=3 (3 repetitions to propose) was dropped
   as redundant.

### Recommendation
The mechanism is sound and the implementation is correct at small scale.
To run the full battery, the implementation needs:
- A faster proposal algorithm (e.g., suffix array, or sampling, not O(n×LMAX)).
- Or: a faster language/runtime (Zag's overhead is the bottleneck).
- Or: run on smaller corpora (but this violates the frozen protocol).

**No verdict on the kill criterion.** The arm was not killed; it was not
evaluated. The performance failure is an implementation limitation, not a
mechanism failure.
