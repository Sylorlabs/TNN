# D-R Verdict

## Verdict: BLOCKED

### Summary
D-R implements a genuinely sub-quadratic proposal structure with corrected
reuse-gate semantics. The core mechanism is proven correct on 100KB synthetic
and real samples (proposal events byte-identical to a validated Python
reference). However, the 1x battery cannot be completed due to a scale
limitation: the implementation panics on inputs ≥3MB. The D comparison is
also blocked (D has published no verdict). Per the frozen kill criterion,
which requires 10x evidence, no kill evaluation is possible.

### What was proven
1. **Corrected semantics**: The v2 implementation fixes a critical bug where
   proposals never promoted (NCOMMITTED was always 0). Now:
   - Pass 1 creates `JUST_SELF` proposals at second occurrence.
   - Walk references proposals; `d_add_occ` promotes at refs>=2.
   - Raw unmatched runs stay proposed forever (never commit).
   - Tiling is exact greedy longest-match (all lengths 64..3).

2. **Sub-quadratic structure**: Suffix-array-inspired approach:
   - Group by 3-byte prefix (radix sort, O(n)).
   - Sort each group by 64B suffix (radix sort, O(n) total).
   - LCP via byte compare; maximal intervals via monotonic stack.
   - 2nd smallest via segment tree (G>=128) or scan (G<128).
   - All identity decisions are memcmp-verified; sort only organizes candidates.

3. **Equivalence on 100KB** (binding requirement):
   - Synthetic (102,400B): 744 events, byte-identical to Python v5.
   - Real (102,400B): 99,471 events, byte-identical to Python v5.
   - Determinism: two runs byte-identical.
   - Mechanism: NCOMMITTED=3 (syn) / 3481 (real); NOCC=1600 / 18016.

4. **Determinism**: Zero RNG in AI paths. Two runs produce byte-identical stdout.

### What is blocked
1. **1x battery**: BLOCKED. Implementation panics on 3MB+ inputs due to
   per-group allocation leaks (hfree is trace-only; 19K groups × per-group
   buffers exhaust memory). The 5.4MB prose and 9.5MB code corpora cannot be
   processed. This is a resource bug, not a correctness bug—the algorithm is
   sound, but the implementation needs buffer reuse or real freeing.

2. **10x**: NOT ATTEMPTED (requires 1x pass).

3. **D comparison**: BLOCKED. As of 2026-09-21, D has published no verdict,
   scorecard, or M3 evidence (`docs/lab/units/arms/D/` contains only
   BUILD_LOG.md and cl/). Both the binding comparison and the additional
   cost/recall comparison cannot be performed honestly.

4. **Kill criterion**: NOT EVALUATED. Requires 10x evidence from D-R and D.
   The frozen criterion (">50% uncommitted at 10x while D commits and wins
   on M3") cannot be assessed.

### Honest assessment
The v2 implementation is a genuine advance: it fixes the zero-commit bug,
achieves sub-quadratic proposal discovery, and proves equivalence on 100KB.
However, it does not meet the scale bar. The 1x battery is a hard requirement,
and the current implementation cannot complete it.

**This is not a PASS.** It is a BLOCKED with proven 100KB correctness.

### What would unblock
1. Fix per-group allocation leaks: reuse buffers sized for max G (73K observed),
   or implement real nio_free in hfree.
2. Re-run 100KB equivalence to confirm no regression.
3. Run 1x battery on 5.4MB/9.5MB inputs.
4. If 1x passes, attempt 10x (requires streaming for 54MB/95MB inputs, as
   read_file caps at 33.5MB).
5. Re-check D for verdict before final comparison.

### Files
- Source: `cl/arm.zag` (v2, ~80KB)
- Spec: `docs/ARM_SPEC.md`
- Build log: `docs/BUILD_LOG.md`
- This verdict: `docs/VERDICT.md`
