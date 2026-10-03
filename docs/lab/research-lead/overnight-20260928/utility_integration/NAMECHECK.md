# NAMECHECK: Utility Integration Worker

## Step 0: Toolchain Guard

**Date:** 2026-10-01 UTC.
**Action:** Safebin activated per mandate.

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

**Result:** `guard-check-done` with no python3/python paths printed.
`which python3 python` returns nothing. Safebin PATH active.

**Contamination status:** CLEAN. No forbidden executable invoked.
If a forbidden executable is invoked, this wave is PROCESS-FAIL.

## Mission

Micah Priority 6: Finish utility Test 6 (redundancy control) and connect
utility to learner-owned predictive success rather than fixed +2/-2.
Attack the "wrong but frequently used" case.

## Prior work (read-only reference)

- Utility build: commit `c912b9b19` (WORKS 5/6, Test 6 NOT RUN).
  Dir: `docs/lab/research-lead/overnight-20260928/utility_build/`.
- Learner-success: commit `b320213f2` (prediction reliability scores work).
  Dir: `docs/lab/research-lead/overnight-20260928/learner_success/`.
- Base: frozen TNN-2, SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
  Verified identical in both prior builds. Never modified.

## Constraints

- Unfrozen variant only. Frozen source read-only.
- Pure Zag via pinned znc. Shell only for znc, binaries, git, file ops.
- Zero em/en dashes in docs (byte-verified before commit).
- Research paper untouched. Nothing pushed. Explicit pathspecs on git add/commit.
