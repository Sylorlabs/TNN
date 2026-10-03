# NAMECHECK: L2-INTERFERENCE clean restart

## Step 0: Toolchain Guard

- Safebin activated at startup: `$HOME/safebin` created and populated via
  symlink loop over allowed tools (git, znc, sh, bash, ls, cp, mv, rm,
  mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack,
  git-upload-pack).
- `export PATH="$HOME/safebin"` applied for all subsequent work.
- `which python3` returned NOTHING. `which python` returned NOTHING.
- `which znc` returns `/home/hatch/safebin/znc`, a symlink to the pinned
  compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev (edition 2026)`).
- No Python, C/C++, JavaScript, or Rust invoked at any point. Work so far:
  shell only (mkdir, ls, git worktree, git log, file writes of prereg
  documents). No computation, no binaries executed beyond `znc --version`.
- Any forbidden-executable invocation in later steps = automatic
  PROCESS-FAIL for the current scientific wave.

## Scope

Lane directory (owned path only):
`docs/lab/research-lead/overnight-20260928/l2_interference_clean/`

Contents: PREREG.md (frozen first), NAMECHECK.md (this file),
l2_interference.zag (implementation, after prereg commit), build outputs,
raw run logs, REPORT.md (after 3/3 runs).

## Environment notes

- Repo ~/workspace/tnn-rsi; branch tnn-native-lab is checked out by
  another worker's locked worktree (~/workspace/tnn-rsi-gpi3), so this
  lane uses a sparse worktree at ~/workspace/lane-l2-interference,
  detached at tnn-native-lab tip 533706483
  ("HPIREV2 clean reproduction: frozen narrowed step-7 prereg
  (wave-20261002-1421pdt)"). Sparse profile: src/tools/toolchain only
  (~21M); lane docs are new untracked files under the owned path.
- A full worktree checkout was attempted first and removed after the
  disk hit 100 percent; the sparse worktree keeps this lane's footprint
  small. No other worker's files were touched.
- Commits local only, never pushed. Explicit pathspecs on every commit.
  No `git reset`. No amend of shared history.
- Sealed worlds: none used in this lane. No sealed-world contents
  inspected (the experiment is self-contained; the evaluator is not
  needed).
- Documentation style: no em or en dashes in lane documents (verified
  before commit).
