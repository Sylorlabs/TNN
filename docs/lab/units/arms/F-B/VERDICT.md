# F-B VERDICT

## VERDICT: DISQUALIFIED

**Criterion:** Incomplete implementation — the arm cannot be fairly evaluated
against the preregistered M1–M9 battery.

### What exists
- Core F-B segmentation mechanism implemented in pure Zag (`cl/arm.zag`, 559 lines).
- Verified correct against C prototype on 30KB prose:
  - Zag: 11,243 chunks, mean 2.67, max 96
  - C (unbounded): 8,811 chunks, mean 3.40
  - Difference is due to bounded-table eviction (4096 candidates), which is
    part of the frozen specification.
- Zero RNG in decision paths. Deterministic.

### What is missing (cannot be tested)
- M1–M9 metric modes (only `segtest` diagnostic implemented)
- Chunk/content store with persistent IDs
- Audit ledger
- M8 determinism artifacts
- Content verification (currently hash-only)
- ID remapping, M7 cache rig

### Kill criterion status
**Cannot be adjudicated.** The binding criterion requires:
- "M3 < C-W's both corpora; OR within noise of F-S on all metrics both corpora"

No C-W or F-S scorecards were located as of 2026-09-21. Comparison results
cannot be invented.

### Performance blocker
Segmentation takes 39s wall (2.2s CPU) for 30KB. Projected 5+ hours for full
corpora. The 37s unexplained gap (not syscalls, not init) suggests VM-level
descheduling that cannot be fixed in arm code.

### 1x M1–M9 row
Not available — modes not implemented.

### 10x status
NOT ATTEMPTED.

### Commit hashes
None — no commits made (implementation incomplete; only source/docs exist).

### Ambiguities encountered
1. **REP_BAR unfrozen**: No numeric REP_BAR in frozen docs. Provisional choice: 2.
2. **P-FB1 vs binding kill rule**: P-FB1 says "either corpus"; binding rule says
   "both corpora". Binding rule governs; inconsistency documented.
3. **Online vs two-pass**: Frozen docs don't specify. Implemented online (query
   after observing current-ending spans). Provisional.
4. **W=256 semantics**: Not enforced as sliding window in current implementation.
5. **M8 reading (A17)**: Combined-instance vs separate M1/M3-instance remains open.
6. **Content verification**: Required but not implemented (hash-only currently).

### Recommendation
The F-B mechanism as literally specified over-cuts severely (mean 2-3 byte
chunks, ~60% one-byte chunks at 1MB scale). This is inherent to the rule, not
an implementation bug. A complete implementation would likely fail M3 (retention
under pressure) due to the sheer number of tiny units overwhelming the 4,000-slot
capacity. However, without a complete implementation and without C-W/F-S
comparison data, no KILLED verdict can be honestly issued.

**The arm is DISQUALIFIED from this evaluation round due to incomplete
implementation, not due to mechanism failure.**
