# Preregistration: Bridge B-A6b Denial-of-Learning Fix

**Date:** 2026-09-29
**Role:** Bridge Bug Fixer
**Target:** B-A6b bug from PI_BRIDGE_ADVERSARY_REPORT.md
**Status:** FROZEN before implementation

## Hypothesis H-FIX

The B-A6b denial-of-learning bug is caused by `bridge_learn` Step 3
calling `pdiscover_direct` (which calls `proc_store`) on every
candidate (pos, val) split. Failed split attempts consume proc slots
that are never reclaimed. With 15+ distractors, all 16 slots are
exhausted before the true split is attempted.

**Fix:** Subset discovery must dry-run without storing. Reserve proc
slots only for the winning split. Do not consume proc slots until the
final (pos, val) is selected.

## Specific changes (committed before running)

1. Add `pdiscover_dry(W, seqs, nseq, out_prog)` function:
   - Identical search to `pdiscover_direct` (same enumeration order,
     same fit criteria)
   - On success: copies winning program bytes to `out_prog`,
     returns nnodes (>=0)
   - On failure: returns -1
   - NEVER calls `proc_store`. Zero slot consumption.

2. Modify `bridge_learn` Step 3 (the (pos, val) search loop):
   - Replace `pdiscover_direct(W, pbase, d1, n1)` with
     `pdiscover_dry(W, d1, n1, prog1)`
   - Replace `pdiscover_direct(W, pbase, d2, n2)` with
     `pdiscover_dry(W, d2, n2, prog2)`
   - Only AFTER both dry-runs succeed (winning split found):
     call `proc_store(W, pbase, prog1, nn1)` and
     `proc_store(W, pbase, prog2, nn2)` to obtain s1, s2
   - Then `br_store` as before

3. Step 2 (direct discovery) UNCHANGED: still uses `pdiscover_direct`
   because a successful direct discovery IS the final result and
   should consume exactly one slot.

## What is NOT changed

- The (pos, val) search order (positions 0..maxlen-1, values in
  first-seen order)
- The program enumeration (1055 programs, same order)
- The fit criteria (`pfits` on all subset sequences)
- The bridge rule semantics (IF input[pos]==val THEN proc_true
  ELSE proc_false)
- PROC_MAX=16, BR_MAX=4
- No new primitives, no new search heuristics

## Kill bars (frozen)

- **K-F1:** B-A6b attack (16 pairs: 15 distractors + trigger) now
  succeeds. `bridge_learn` returns 1000+bslot (not -1). Bridge rule
  learned: IF input[0]==120 THEN procX ELSE procY. At most 2 proc
  slots consumed for the winning split (plus any from prior tasks
  in the same W, which the test controls).

- **K-F2:** Original 7/7 bridge tests still pass. The existing
  `main` in bridge_learn.zag (Tasks C, A, B with K-B1..K-B4 checks)
  must output 7/7 PASS and H-BRIDGE SURVIVES. No regression.

- **K-F3:** Slot usage is bounded. In the B-A6b scenario, failed
  split attempts consume 0 proc slots. Verifiable by inspecting
  proc_used counts: after the fix, only the 2 winning-split slots
  are marked used (within a fresh W).

## Test plan

1. Implement fix in bridge_learn.zag (pure Zag, no Python).
2. Compile with znc. Must compile clean.
3. Run existing main: expect 7/7 PASS (K-F2).
4. Write B-A6b reproduction test (bridge_fix_test.zag or extend
   main): 15 distractors + trigger, expect bridge rule learned
   (K-F1), verify slot count <= 2 for the bridge task (K-F3).
5. Commit fix, test, results.

## Failure modes (what would kill H-FIX)

- B-A6b still returns -1 after fix: H-FIX KILLED
- Original 7/7 regresses: H-FIX KILLED (or needs narrower fix)
- Fix requires changing search order or enumeration: out of scope,
  H-FIX as specified KILLED

## Provenance

- Bug report: PI_BRIDGE_ADVERSARY_REPORT.md (B-A6b)
- Adversary recommendation: dry-run discovery, reserve slots for
  winning split only
- Implementation target: bridge_learn.zag, function `bridge_learn`
  Step 3, plus new `pdiscover_dry` function
