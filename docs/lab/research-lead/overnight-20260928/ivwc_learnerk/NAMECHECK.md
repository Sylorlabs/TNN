# NAMECHECK.md -- IVWC-LEARNERK

## Step 0: toolchain guard (worker startup)

- Date: 2026-10-03. Worker: IVWC-LEARNERK.
- Safebin is the entire PATH for this lane: `export PATH="$HOME/safebin"`.
- Verification at startup: `which python3` returns nothing; `which python`
  returns nothing. (Confirmed 2026-10-03: both empty under the safebin PATH.)
- Builder: pinned znc at `$HOME/safebin/znc`. All computation in pure Zag.
- All research logic (world, learner, verdicts, diagnostics, prediction
  arithmetic) is implemented in Zag. Shell is used only to invoke znc, run
  the binary, and for git/file operations.
- If a forbidden executable is invoked at any point, this wave is
  PROCESS-FAIL per the worker toolchain guard; the result stays exploratory
  until a clean safebin reproduction. No such invocation has occurred.
- Lane continues the clean streak from IVWC-BATCHAWARE, IVWC-PERBUCKET, and
  IVWC-MARGINAL (zero python3/python invocations).

## Step 0b: git discipline (shared worktree)

- Current checkout branch is `lane-beliefaudit-20261003` (another worker's
  branch); this lane commits on `tnn-native-lab` per the task.
- All commits use a separate `GIT_INDEX_FILE` (plumbing), leaving the shared
  index untouched, with explicit pathspecs confined to `ivwc_learnerk/`.
- Commit sequence: prereg commit (NAMECHECK.md + PREREG.md) strictly before
  any implementation source; implementation commit (src + runs + REPORT.md)
  after.
- Git invoked via `/usr/bin/git` directly (the `$HOME/safebin/git` symlink
  has a known EPERM failure mode on writes; see AGENTS.md).
- `bin/` (reproducible via the pinned znc) is excluded from commits per
  Micah's 2026-10-03 guidance.
