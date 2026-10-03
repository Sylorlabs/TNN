# NAMECHECK.md - DEVINT-CLA2 Builder

## Step 0: Toolchain guard (mandatory, executed before any work)

- Guard check command: `which python3 python 2>/dev/null; echo "guard-check-done"`
- Result: `/usr/bin/python3` found (system binary, cannot be removed).
- Non-use documented: python3 is a system binary at /usr/bin/python3 alongside
  git/sha256sum/grep. Surgical PATH removal is not possible without breaking
  core utilities. The worker will never invoke python3, python, node, nodejs,
  or any other forbidden interpreter for any purpose.
- Computational research logic: Zag only, compiled with the pinned znc.
- Shell permitted only for: invoking znc, running binaries, git operations,
  file moves/copies.
- Forbidden executable invoked: none. Wave status: not PROCESS-FAIL.

## K1 ordering

- Prereg commit `f24063bcb` verified as ancestor of HEAD via
  `git merge-base --is-ancestor f24063bcb HEAD` before implementation.
- Implementation commit will be a strict descendant.

## Owned path

`docs/lab/research-lead/overnight-20260928/devint_cla2_build/`
