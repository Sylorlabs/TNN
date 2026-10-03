# NAMECHECK: L2-INTERFERENCE2 (pool saturation law + adversarial eviction attack)

## Step 0: Toolchain Guard

- Safebin activated at startup: `$HOME/safebin` (49 allowed tools,
  verified present).
- `export PATH="$HOME/safebin"` applied for all subsequent work.
- `which python3` returned NOTHING. `which python` returned NOTHING.
- `which znc` returns `/home/hatch/safebin/znc`, a symlink to the pinned
  compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev (edition 2026)`).
- No Python, C/C++, JavaScript, or Rust invoked at any point. Work so far:
  shell only (mkdir, ls, git status/log, file writes of prereg documents).
- Any forbidden-executable invocation in later steps = automatic
  PROCESS-FAIL for the current scientific wave.

## Scope

Lane directory (owned path only):
`docs/lab/research-lead/overnight-20260928/l2_interference2/`

Contents: PREREG.md (frozen first), NAMECHECK.md (this file),
l2_interference2.zag (implementation, after prereg commit), build
outputs, raw run logs (run1/2/3.txt), REPORT.md (after 3/3 runs).

## Environment notes

- Repo ~/workspace/tnn-rsi-gpi3; branch tnn-native-lab. Working directly
  in the checkout (no sparse worktree needed; the pinned znc is already
  present at src/tools/toolchain/).
- Commits local only, never pushed. Explicit pathspecs on every commit.
  No `git reset`. No amend of shared history. Per the 2026-10-03 shared
  workspace lesson, git writes go through /usr/bin/git directly (the
  safebin git symlink has failed with EPERM on object writes); on
  index.lock contention, retry with sleep backoff and never remove the
  lock while other workers are active.
- Builds on L2-INTERFERENCE (`../l2_interference/`): same A family,
  same benign FULL writer, same conflict-relocation mechanism. Only
  additions: parameterized POOLN and the churn adversary phase. No
  redesign of the mechanism.
- Sealed worlds: none used. No sealed-world contents inspected.
- Documentation style: no em or en dashes in lane documents (verified
  before commit).

## Design lineage

Follow-up to L2-INTERFERENCE clean restart (VERDICT=PASS, all 6 kill bars
green, 2026-10-02). Pushes the boundary along the two axes named in the
task: Option A (overflow pool exhaustion: sweep POOLN 0/4/8/16/32) and
Option C (adversarial interference: churn adversary flushing the FIFO
pool at POOLN 8 and 32). Option B (cross-structure analogical transfer)
is explicitly out of scope here and is noted as a recommended separate
follow-up.
