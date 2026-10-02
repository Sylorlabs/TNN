# NAMECHECK.md: DEVINT-CLA2 E6 Builder

Date: 2026-09-30. Worker: DEVINT-CLA2 E6 Builder.
Owned path: docs/lab/research-lead/overnight-20260928/devint_e6_build/

## Step 0: Toolchain Guard

Restricted PATH set up at startup:
- Created $HOME/safebin with symlinks to: git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack, plus coreutils (basename, chmod, cut, date, diff, dirname, echo, find, head, od, printf, sleep, sort, stat, tail, tr, uniq, etc.)
- Exported PATH="$HOME/safebin" (ONLY safebin, no /usr/bin, no /bin)
- Verified via `command -v` (bash builtin):
  - `command -v python3` returns NOTHING (not accessible)
  - `command -v python` returns NOTHING (not accessible)
  - `command -v git` returns /home/hatch/safebin/git (accessible)
  - `command -v znc` returns /home/hatch/safebin/znc (accessible)
- Guard check: PASS. python3 and python are ABSENT from the restricted PATH.

All subsequent commands in this session use PATH=$HOME/safebin.
If a forbidden executable is invoked, this wave is PROCESS-FAIL.

## Rules acknowledged

- Pure Zag for all computational research. Shell only for znc, binary execution, git, file moves.
- No em dashes in documentation (hyphens only).
- Contaminated paper never touched.
- No sealed FW1-FW9 access.
- K1: implementation commit strictly follows 8ab5abbdb (E6-PREREG-FROZEN).
- Owned path only. Explicit pathspecs. Commits stay local.
