# NAMECHECK.md: Learner-Owned Success Criteria Worker

## Step 0: Toolchain Guard (mandatory)

Executed at startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with NO python3/python paths printed.
`which python3` returns nothing. `which python` returns nothing.
Zero forbidden executables invoked. Safebin active for all work.

## Provenance

- Worker: Learner-Owned Success Criteria Worker (Micah Q8).
- Task: test if TNN can generate predictions BEFORE outcomes and use
  prediction error to judge structures.
- Base: `provenance_exp/pv_base.zag` verbatim copy, SHA-256 verified
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  (frozen TNN-2 hash).
- Variant: UNFROZEN only. Frozen source never modified.
- Pure Zag via pinned `znc`. Shell only for znc invocation, git, file ops.

## Constraints honored

- Unfrozen variant only; frozen source read-only reference.
- Pure Zag for all computation. Zero Python.
- Zero em/en dashes in docs (byte-verified before commit).
- Research paper untouched. Nothing pushed (local commits only).
- Explicit pathspecs on git add and git commit.
