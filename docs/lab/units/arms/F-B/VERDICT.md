# F-B Verdict — 2026-09-21

## Verdict: BLOCKED

**Category**: `BLOCKED` (honest; `DISQUALIFIED` is invalid per tasking).

## Blockers

### 1. Performance (primary)
The validated 4-way set-associative mechanism suffers a 46x slowdown when
the candidate table fills:
- 4KB with empty table: 2.5s.
- 4KB with full table: 115s.
- 563KB (t1_prose): timeout at 180s.
- Full corpus (15MB): infeasible.

Root cause: random access to 208KB candidate table thrashes CPU cache
under VM memory pressure (191MB free, high steal, 2 CPUs oversubscribed).

The mechanism is CORRECT (Python and Zag match exactly on 2KB: 311 chunks,
checksum 3976909433127229168), but not FAST enough for the battery.

### 2. Comparators (secondary)
Kill criterion requires: "M3 < C-W's both corpora; OR within noise of F-S
on all metrics both corpora."

- Committed F-S scorecard is `partial`: M1 only, no M3.
- No committed C-W scorecard found.
- Local C-W VERDICT has combined M3 (100.0%) but no per-corpus breakdown.
- Exact adjudication unavailable. Status: `provisional-pending-comparators`.

## What was completed
- Validated segmentation mechanism (Python == Zag, byte-identical).
- Complete `cl/arm.zag` with M1 modes (builds, runs on small inputs).
- ARM_SPEC.md, BUILD_LOG.md, scorecard.
- Performance characterization.

## What was not completed
- M2-M9 battery (M1 only implemented).
- Full-corpus runs (infeasible).
- M8 determinism (requires 10 runs; each too slow).
- Content verification (hash-only matching).
- Global (not per-set) eviction.

## Recommendation
The mechanism is sound but needs a faster implementation strategy:
- Investigate why 208KB random access is so slow (may be VM-specific).
- Consider algorithmic alternatives that preserve semantics but improve
  locality (e.g., blocked table layout, software prefetching).
- Or: run battery on hardware with adequate cache/memory.

Do NOT silently change to clear-on-full or reduce LMAX to gain speed;
those bend the frozen prereg.
