# NAMECHECK.md -- Governance/Frontier Worker (Wave 2)

## Step 0: Toolchain Guard (MANDATORY, recorded 2026-10-01)

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty). Only
`guard-check-done` printed. Safebin active with 42 tools. Pinned znc
available at `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Zero forbidden executables invoked. Verified before any git operations.

## Scope

Governance only. Ledger updates (C181+), SUF tracking table update,
frontier gap analysis against Micah's 10 priorities. Do not modify
experiment files. Pure shell/git operations. Zero em/en dashes in docs.
Paper untouched. Nothing pushed.

## Mission

1. Wait for 8 new priority workers + protect-how retry to complete.
2. Append new claims C181+ to canonical ledger (verify commit hashes).
3. Update SUF tracking (researcher-owned vs learner-owned).
4. Identify frontier gaps.
5. Commit with explicit pathspecs.
