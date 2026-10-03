# C1 Harness Fix: REPORT

Verdict: C1-HARNESS-FIXED.

## The Bug

The Zag driver (`zag_driver.zag`) does `mkdir(state)` but never clears
pre-existing state. The resume script `refreeze_drive.sh` skipped
completed runs via `costs.txt` but did not clear partial `state/`
directories on resume. After an interruption, re-running on stale state
caused every turn to be ingested twice, doubling all weights and
flipping D1/D2/D3 abstention decisions.

Root cause documented in FLAKINESS_REPORT.md (commit e98a976a0).

## The Fix

File: `refreeze_drive_fixed.sh` (in this directory)

Change to `run_one()`, matching the pattern already correct in
`drive_remaining.sh`:

```bash
  # FIX: clear any partial state from an interrupted prior run.
  # The Zag driver never clears state/ itself; without this, resume
  # re-ingests turns on stale state and doubles all weights.
  rm -rf "$d"
  mkdir -p "$d"
```

The fix is harness-only. No contestant binary changes. No driver
Zag source changes.

## Verification

Test: `test_harness_fix.sh` (in this directory)

Three phases on w1 with the C1 contestant:
- Phase 1 (baseline, fresh dir): 63/63 correct, 32 facts
- Phase 2 (OLD: resume without clearing): 58/63 correct, 62 facts.
  BUG REPRODUCED. Facts exactly doubled. Score dropped.
- Phase 3 (NEW: resume with rm -rf): 63/63 correct, 32 facts.
  FIX VERIFIED. Identical to fresh run.

Result: HARNESS-FIX-PASS.

## Scope Notes

- `drive_remaining.sh` already had the correct `rm -rf` pattern.
- `drive_all.sh` has no skip logic (assumes fresh tree); it would hit
  the same bug if re-run on a populated tree. Recommend adding `rm -rf`
  there too for robustness, or documenting it as fresh-run-only.
- The original shell `run_race.sh` already clears state files explicitly
  (`rm -f "$STATE"/state.txt ...`). The bug was specific to the Zag
  driver harness scripts.

## Governance

- Toolchain guard: PASS. Zero Python invocations.
- No sealed FW1-FW9 files accessed.
- Contaminated paper: zero-diff.
- Harness scripts only. No source modifications.
