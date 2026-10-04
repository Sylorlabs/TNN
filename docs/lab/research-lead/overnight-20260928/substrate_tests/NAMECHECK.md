# NAMECHECK: Substrate Test Designer

**Date:** 2026-10-01
**Scope:** Design ONLY. No implementation, no variant built, no source edited.
**Parent task:** Design the 5 evaluation tests for the shared retention substrate.

## Step 0: Toolchain guard

- Safebin assembled at `$HOME/safebin` (36 allowed tools: git, znc, coreutils).
- `export PATH="$HOME/safebin"` active for all commands in this task.
- `which python3 python` returned nothing (verified at task start).
- Zero forbidden executables invoked. This task is analysis/design only;
  no computational research operation was required. Had one been needed,
  pure Zag via the pinned znc would have been used.

## Input provenance

- Shared substrate specification: commit `550fa268b`,
  `docs/lab/research-lead/overnight-20260928/shared_substrate/SHARED_SUBSTRATE.md`
  (sections 2 record format, 4 write paths, 5 read paths, 6 boundedness,
  7 source tagging, 8 non-specifications, 9 evaluation).
- Learning machinery falsifiability S1-S5: commit `3416ed218`,
  `learning_machinery/LEARNING_MACHINERY.md` section 5.
- H3-lite Node 1 build: commit `45c55ed83` (field-32 mechanism, the
  narrow-counter comparator for T3).
- Weak K-LT-5 prereg: `weak_klt5/WEAK_KLT5_PREREG.md` (bar R > 1.15).
- Frozen TNN-2: never read for modification; baseline reference only.

## Constraints honored

- Design ONLY. No variant built, no source modified, no binary produced.
- Frozen source, frozen preregs, and the paper untouched.
- No sealed worlds opened or created.
- Zero em dashes in all deliverables (byte-verified before commit).
- Nothing pushed.

## Verdict

SUBSTRATE-TESTS-COMPLETE (design).
