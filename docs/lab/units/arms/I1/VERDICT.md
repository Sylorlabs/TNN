# ARM I1 — Verdict (1x)

**Date:** 2026-09-21
**Scale:** 1x
**Mechanism:** Strict tree hierarchy (STRUCT)
**Verdict:** **PROVISIONAL** — core mechanism validated; binding kills incomplete.

## Summary

The I1 strict tree hierarchy mechanism is implemented and the core formation dynamics are validated. L1 superchunks form at episode 7 (T_co=7) with zero formations at episodes 1-6, confirming the frozen threshold. However, not all binding kill criteria could be evaluated, and several modes require further work.

## Binding Kills

### Kill (i): L2+ superchunk recall <5% vs flat comparator
**Status:** NOT-IMPLEMENTED

Requires a genuine flat comparator with equal measured store cost. The comparator must be built and the 5% threshold measured. This is significant remaining work.

### Kill (ii): Maintenance + stale rebuild >20% of audit ops (per corpus)
**Status:** SURVIVE

Measured on corpus 9 (synthetic, 512 units, 20 formation episodes):
- Maintenance ops (form + dissolve + stale): 73
- Total audit ops: 585
- Ratio: 12.4% (124 tenths)
- Threshold: 20% (200 tenths)
- **Result:** 12.4% < 20% → SURVIVE

The hierarchy maintenance overhead is well below the kill threshold.

### Kill (iii): L1 boundary agreement <50% with natural breaks
**Status:** BLOCKED

"Natural breaks" remains undefined in the frozen prereg. This kill cannot be evaluated until the definition is frozen.

## Mode Results (1x)

| Mode | Status | Key Metrics |
|------|--------|-------------|
| m1-1x-prose | PASS | 84,731 units, 100% recall, 100% boundary, ID probe PASS |
| m1-1x-code | PASS | 148,678 units, 100% recall, 100% boundary, ID probe PASS |
| m2-t1-prose | OK | etc=3, ep0_recall=0%, not censored |
| m2-t1-code | OK | — |
| m2-t2-prose | OK | — |
| m2-t2-code | OK | — |
| m2-t3-1x | OK | — |
| m3-1x | PASS | 100% valuable survival, 50 weakens, FROZEN-UNDER-PRESSURE |
| m4-1x-prose | NEEDS-SPEC-VERIFICATION | 0% scores; Caesar transform not verified vs frozen spec |
| m4-1x-code | NEEDS-SPEC-VERIFICATION | — |
| m5-1x | METRICS-PRODUCED | 3.9 B/B (above 1.5 ranking bar; not a kill) |
| m6-p2c-1x | PASS | 100% recall, 100% boundary |
| m6-c2p-1x | NOT-RUN | — |
| m7-1x | BLOCKED | A7/A8 unresolved |
| m8-1x | TIMEOUT | Workload exceeds 120s |

## Formation Probe (Mechanism Validation)

The `probe-formation` mode validates the core STRUCT mechanism:
- **Episodes 1-6:** 0 L1 superchunks (no premature formation)
- **Episode 7:** 64 L1 superchunks form (512 L0 ÷ 8 per superchunk)
- **Run length:** 8 (within frozen 2..8 range)
- **T_co:** 7 (frozen threshold confirmed)
- **Single parentage:** Verified by construction (each L0 has exactly one parent)
- **Adjacency:** Verified (superchunks span contiguous L0 units)
- **ID uniqueness:** 23-bit serial space, no collisions

## Determinism

Byte-identical reruns verified for:
- `probe-formation` (two replicas)
- `kill-ii` (two replicas)

Zero randomness in the mechanism; all behavior is deterministic given state.

## Remaining Work

1. **Kill (i):** Build genuine flat comparator with equal measured store cost; measure L2+ recall ratio.
2. **M4:** Verify Caesar identifier transform against frozen prereg spec.
3. **M7:** Blocked pending A7/A8 freeze (edit bytes, lookup schedule).
4. **M8:** Optimize workload or extend timeout; implement full 5-perturbation battery with 6 artifacts each.
5. **M5:** Fix ledger-dump chunking (currently FATAL on large ledgers).
6. **10x:** Run only after all valid 1x binding bars survive (kill-i must be implemented first).

## Conclusion

I1's strict tree hierarchy forms correctly at the frozen threshold with acceptable maintenance overhead (12.4% < 20%). The mechanism is sound, but the evaluation is incomplete: kill-(i) requires the flat comparator, kill-(iii) awaits the natural-breaks definition, and several modes need spec verification or optimization. **No 10x run is authorized until kill-(i) is measured.**
