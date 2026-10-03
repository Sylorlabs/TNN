# NAMECHECK.md - MUL Rung B Builder

## Step 0: Toolchain Guard

Date: 2026-09-30. Worker: MUL Rung B Builder.

**Restricted PATH setup:**
- Created `$HOME/safebin` with symlinks to allowed tools only: git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, and standard coreutils.
- `export PATH="$HOME/safebin"` applied to all shell sessions.
- `which python3 python` returns nothing (verified). No python3 or python in PATH.
- All computational work will use Zag via the pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Shell only for: invoking znc, running binaries, git operations, file moves/copies.

**K1 anchor:** Frozen prereg commit `3ce154801` (MUL-RUNGB-PREREG-FROZEN). Implementation commit must strictly follow it (verified by `git merge-base --is-ancestor 3ce154801 HEAD` before committing results).

**Forbidden executables:** python3, python, or any other interpreter. If invoked, this wave is automatically PROCESS-FAIL.

**Status:** Guard active. Zero invocations at Step 0.
