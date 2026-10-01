# NAMECHECK: Shared Consequence Substrate Builder

## Step 0: Toolchain Guard

Date: 2026-10-01
Worker: Shared Consequence Substrate Builder (subagent)

Activation:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned empty. `guard-check-done` printed.
Zero forbidden executables in PATH. Pure Zag via pinned znc only.

## Scope

UNFROZEN variant only. Frozen TNN-2 source is read-only reference
(SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
re-verified before use).

Mission: build the shared consequence substrate (Micah Q4, increased
priority). One persistent PURSUIT/UNCERTAINTY store driving two
behaviors: action-policy learning (Node2-v2 convergence) and
withholding (substrate consumer, not a separate decline gate).

## Constraints Honored

- Unfrozen variant only; frozen source never modified.
- Pure Zag via pinned znc; safebin PATH; no python.
- Zero em/en dashes in documentation (byte-verified before commit).
- Research paper untouched.
- Nothing pushed (local commits only, explicit pathspecs).
- Sealed worlds: none used in this wave (builder-run experiments).
