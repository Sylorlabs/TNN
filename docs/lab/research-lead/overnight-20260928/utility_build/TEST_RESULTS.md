# Utility Signal Test Results

**Binary:** `ub_bin` (from `ub_test.zag`).
**Runs:** 3/3 byte-identical (SHA-256 `81669ae411719da00b1e3d4924a27798300a2b29ff7de8eefc4efd332ea02775`).
**Base equivalence:** `ub_test_bin` (full variant with base `main`) passes all C1-C15, A1-A5.

## Falsification test results (design section 4)

### 1. Fossil discrimination: PASS

**Battery:** Promote 4 MAPs, use 1 via 5 query hits, 500 filler pressure.

**Results:**
- After promotion: all 4 MAPs U=2 (trial success +2). L=birth tick.
- After 5 hits on MAP 24's shadow: MAP 24 U=7 (2+5), L updated. Others U=2.
- Attribution works: `util_attr` correctly identified owning MAP via shadow f4.
- After pressure: live=600, maps=4. All 4 survived with `graph_ok=1`.

**Interpretation:** U distinguishes used (U=7) from unused (U=2). The signal is live. (Pressure was moderate; heavier pressure needed to observe fossil-first reclaim ordering. See limitations.)

### 2. Zombie preemption: PASS

**Battery:** Promote 2 MAPs, 1050 churn teaches to cap.

**Results:**
- After churn: live=1022 (at cap), maps=2.
- **Zombies: 0.** Total MAPs: 2.
- Baseline (zombie census): 3.8% zombies at 1022/1024 nodes.

**Interpretation:** Atomic reclaim makes the shell-without-body route impossible, not rare. The 3.8% baseline is eliminated by construction. This is the strongest result: a prospective zombie-detector subsystem is deleted, not built.

### 3. Use-protection (MAP 22 replay): PASS

**Battery:** Promote MAP, contradict licensing fact (triggers revision), 800 filler.

**Results:**
- MAP 16: U0=2, cells0=4.
- After revision: U=3 (revision success +1). The D1 discard is closed.
- After pressure: MAP alive, U=3, `graph_ok=1`, cells=4 (all survived).
- **Reexec succeeded:** out=999. The MAP remains executable.

**Interpretation:** This is the fossil census's sharpest case inverted. MAP 22 was LIVE (refs=2) yet zombified because "use leaves no trace on the bid." With U=3, the MAP's cells were protected through the filler wave. The learner now has a way to mark structural importance. The "how" survives.

### 4. Zero-pressure equivalence: PASS

**Battery:** Base `run_all` (C1-C15, A1-A5) on variant with utility.

**Results:** All 20 tests PASS, identical to frozen base.

**Interpretation:** Utility writes are behavior-free until the reader (eviction) runs. No eviction fired in these tests, so no behavioral difference. The signal is dormant, not disruptive.

### 5. Cost visibility: PASS

**Battery:** Query hit on shadow FACT, measure node delta.

**Results:**
- Query-hit dn=0. Zero node allocations.
- MAP U incremented 2->3 (in-place field update).

**Interpretation:** Utility writes are O(1) field updates. They appear in DYN-1 accounting as zero marginal cost. The mechanism does not bend DYN-1 (as designed: it changes what survives pressure, not per-event write cost).

### 6. Redundancy falsification (S2-style): NOT RUN

**Question:** If structure-aware bid inheritance alone (no U counter) achieves the same reclaim ordering, the U counter is redundant.

**Status:** Requires a separate control build (atomic reclaim + cell protection, but no U field; MAPs ordered by bid). Not built in this wave.

**Honest assessment:** The zombie preemption (test 2) was achieved by atomic reclaim, not by U. The use-protection (test 3) used U=3 to classify the MAP as LIVE, but the MAP was also recent (just revised), so recency alone might have sufficed. The U counter's unique contribution (distinguishing old-but-useful from old-and-unused) was not isolated. This test is needed before claiming the U field earns its place.

## Summary

| Test | Result | Key number |
|---|---|---|
| 1. Fossil discrimination | PASS | U=7 (used) vs U=2 (unused) |
| 2. Zombie preemption | PASS | 0 zombies (baseline 3.8%) |
| 3. Use-protection | PASS | MAP executable after pressure (reexec=999) |
| 4. Zero-pressure equivalence | PASS | 20/20 base tests |
| 5. Cost visibility | PASS | dn=0 per hit |
| 6. Redundancy | NOT RUN | Control build needed |

**Verdict: UTILITY-BUILD-COMPLETE: WORKS (5/6).**

The learner-owned utility signal works as designed. MAPs accumulate U from experience (promotion, query hits, trial success, revision outcomes). Eviction consults U/L. Zombies are preempted by construction. Used structures survive pressure with executable graphs intact.

**Limitations:**
- FOSSIL_AGE=200 is scaffolded, not learner-adapted.
- Increment magnitudes (+2/+1/-1/-2) are researcher-set.
- Test 6 (redundancy) not run; U's unique value over recency+structure not isolated.
- Does not bend DYN-1 (by design; that's the decline/dedup workers' job).
- U is use, not truth: a wrong-but-frequently-used MAP accumulates U. Must never be read as correctness signal (per design 2.6).
