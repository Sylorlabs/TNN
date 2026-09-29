# Bridge B-A6b Fix: Result

**Date:** 2026-09-29
**Role:** Bridge Bug Fixer
**Prereg:** PREREG_BRIDGE_FIX.md (commit c22c29e4e, frozen before implementation)
**Status:** H-FIX SURVIVES. All kill bars PASS.

## The bug

From PI_BRIDGE_ADVERSARY_REPORT.md (B-A6b): when 15+ distractor values
exist, `bridge_learn` Step 3 called `pdiscover_direct` (which calls
`proc_store`) on every candidate (pos, val) split. Each failed split
attempt consumed a proc slot. With PROC_MAX=16, 15 failed attempts
exhausted all slots before the true split could store its second
procedure. `bridge_learn` returned -1 on a solvable task.

## The fix

Two changes to bridge_learn.zag (pure Zag, no Python):

1. **New function `pdiscover_dry(W, seqs, nseq, out_prog)`:**
   Identical search to `pdiscover_direct` (same 1055-program
   enumeration, same fit criteria). On success, copies winning program
   bytes to caller-provided `out_prog` and returns nnodes. On failure,
   returns -1. NEVER calls `proc_store`. Zero slot consumption.

2. **Modified `bridge_learn` Step 3:**
   Candidate (pos, val) splits now use `pdiscover_dry` for both
   subsets. Only after BOTH dry-runs succeed (winning split
   identified) does the code call `proc_store` twice to obtain s1, s2,
   then `br_store` for the rule. If `proc_store` fails at that point,
   returns -1 immediately (genuine exhaustion; no other split can
   succeed with 0 free slots).

Step 2 (direct discovery) unchanged: still uses `pdiscover_direct`
because a successful direct discovery IS the final result.

## Verification

### K-F1: B-A6b attack now succeeds -- PASS

Test: 16 pairs (15 broadcast-last distractors with distinct pos-0
values + trigger "xab"->"xxx"), PROC_MAX=16.

Before fix (adversary report): `bridge_learn` returned -1, 16/16
slots used, 0 bridge rules.

After fix (BRIDGE_FIX_BA6B_RAW.txt):
- `bridge_learn` returned 1000 (bridge rule 0)
- Rule: IF input[0]==120 THEN proc0 ELSE proc1
- Proc slots used: 2/16
- Bridge rules: 1
- Dispatch verified: "xqw"->"xxx", "abc"->"ccc"

### K-F2: Original 7/7 tests still pass -- PASS

Ran the existing `main` in bridge_learn.zag (Tasks C, A, B):
- Task C: direct proc slot 0, 0 bridge rules. K-B1(control) PASS
- Task A: bridge rule 0, (pos=0,val=120). K-B1(trigger), K-B2(part1),
  K-B3, K-B4(part1) PASS
- Task B: bridge rule 1, (pos=1,val=113). K-B2(part2), K-B4(part2) PASS
- Result: 7/7, H-BRIDGE SURVIVES

Raw output: BRIDGE_FIX_REGRESSION_RAW.txt (byte-identical to pre-fix
behavior on these tasks, except proc slot numbering is now dense).

Note: proc slot numbers changed (Task A now uses proc1/proc2 instead
of higher numbers) because failed attempts no longer consume slots.
This is the intended fix behavior, not a regression.

### K-F3: Slot usage bounded -- PASS

In the B-A6b scenario, failed split attempts consume 0 proc slots.
Measured: 2/16 slots used (only the winning split's two procedures).
Before fix: 16/16 slots used.

## Files

- bridge_learn.zag (modified: +pdiscover_dry, Step 3 dry-run)
- PREREG_BRIDGE_FIX.md (frozen prereg)
- BRIDGE_FIX_BA6B_RAW.txt (B-A6b test raw output)
- BRIDGE_FIX_REGRESSION_RAW.txt (7/7 regression raw output)
- This file: BRIDGE_FIX_RESULT.md

## Classification

B-A6b is REPAIRED. The bridge no longer denies learning on
distractor-heavy tasks. Slot waste (B-A6a) is fixed by the same
change. H-BRIDGE remains SURVIVES (bounded L2+ with functional
revision bridge, binary-conditional).
