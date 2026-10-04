# NAMECHECK: Mini-Lifetime Builder

## Step 0: Toolchain Guard

Date: 2026-10-01. Operator: Mini-Lifetime Builder (subagent).

```sh
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no paths printed. `which python3` and
`which python` return nothing. Safebin active.

## Scope

Build and run the mini-lifetime causal experiment per parent task.

- Build A: frozen TNN-2 (f4de7ff46), cognition untouched. Read-only
  reference: `tnn2_build/tnn2.zag`, SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
- Build B: reuse-path variant, exactly the 5 minimal items from
  `tnn2_reusepath/REUSE_PATH_DESIGN.md` Section 6.1. `t2_revise_graph`
  UNCHANGED except the shadow-teach deletion specified by the design.
- Worlds: A-mini, B-mini, C-mini per `mini_lifetime/MINI_LIFETIME.md`.
  Fresh, independently sealed, hashes recorded. Trial-must-run
  validated per build.
- Runs: 3/3 deterministic per build, byte-identical.

## Provenance

- Design: `mini_lifetime/MINI_LIFETIME.md` (commit 0bab6db08).
- Reuse design: `tnn2_reusepath/REUSE_PATH_DESIGN.md` Section 6.1.
- Frozen source: `tnn2_build/tnn2.zag` at f4de7ff46.
- No sealed world contents inspected beyond hashes until evaluation.

## Constraints

- Pure Zag via pinned znc. Shell only for builds, runs, git, file ops.
- Zero em/en dashes in docs (byte-verified before commit).
- Paper untouched. Nothing pushed. Frozen cognition untouched.
- Any forbidden executable invocation = PROCESS-FAIL for this wave.
