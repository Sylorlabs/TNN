# NAMECHECK.md: Utility Signal Builder

## Step 0: Toolchain Guard

**Date:** 2026-10-01 UTC
**Worker:** Utility Signal Builder (subagent)

### Guard activation

```bash
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

**Result:** `guard-check-done` with no output from `which python3 python`.
- `which python3` returns nothing (empty)
- `which python` returns nothing (empty)
- Safebin active at `$HOME/safebin`
- PATH restricted to safebin only

### Scope

**UNFROZEN VARIANT ONLY.** Frozen TNN-2 source is read-only.
- Base: `ub_base.zag` (verbatim frozen, SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`)
- Variant: `ub_full.zag` (base + utility mechanism + driver)
- Frozen source/binary never modified.

### Input provenance

- Design: `docs/lab/research-lead/overnight-20260928/utility_signal/UTILITY_SIGNAL.md` (commit `cd6a8a74a`)
- Frozen base: `../decline_gate/dg_base.zag` (SHA-256 verified identical)
- Parent task: Build learner-owned MAP utility signal per design

### Constraints honored

- Pure Zag via pinned znc (`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`)
- Shell only: znc invocation, binary execution, git ops, file moves
- Zero em/en dashes in all documentation (byte-verified before commit)
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` never modified
- No sealed worlds
- Nothing pushed (local commits only)
- Explicit pathspecs on all `git add` and `git commit`

### Forbidden executables

None invoked. Zero Python, zero other interpreters. All computation in Zag.
If any forbidden executable is invoked, this wave is PROCESS-FAIL per governance.
