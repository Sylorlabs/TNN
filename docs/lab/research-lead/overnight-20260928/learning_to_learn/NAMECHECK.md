# NAMECHECK: Learning-to-Learn Worker

## Step 0: Toolchain Guard (mandatory)

Executed at worker startup, before any research computation:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING. Only `guard-check-done` printed.
Safebin active for all subsequent commands. PATH contains only the 36
allowed tools (coreutils, git, pinned znc, shell).

## Step 1: Identity

Worker: Learning-to-Learn Worker (Constitution Section 16).
Task: Test if TNN gets better at learning with age. Family 1 (5 chain
problems) then Family 2 (5 new problems). Measure examples-to-criterion,
search cost, compute. Controls: fresh (no Family 1), ablated (Family 1
experience, LINK strategy removed, MAP facts retained).

## Step 2: Base provenance

- Cognition base: `../persistent_connections/pc_base.zag`, SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  (verified byte-identical to frozen TNN-2 base per persistent_connections
  REPORT.md).
- Mechanism patch: `../persistent_connections/pc_patch.zag` verbatim
  (LINK edge write on verified rebind + two-pass rebind_try + pc_del_links),
  plus 2 lines of behavior-neutral measurement instrumentation (stash
  rebind tried/rejected into unused header fields 56/60; nothing reads
  them; search/execution behavior unchanged).
- Frozen source: read-only. No modifications to frozen files.
- Unfrozen variant only.

## Step 3: Build method

- Trim base: remove base `ev_query` (lines 813-835) and base `fn main`
  (line 1357), reproducing the exact trim used by the
  persistent_connections worker (verified by diff against
  `pc_full_treat.zag` lines 1-1567).
- Assemble: trimmed base + patch + driver, compiled with pinned
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Three drivers (treatment / fresh / ablation), three binaries.
- 3/3 deterministic runs per arm, SHA-256 verified.

## Step 4: Constraints honored

- Pure Zag. Shell only for znc invocation, binary runs, git, file moves.
- Zero em/en dashes in docs (byte-verified before commit).
- TNN_RESEARCH_PAPER_20260929.md untouched.
- Nothing pushed. Commits local only on `tnn-native-lab`.
