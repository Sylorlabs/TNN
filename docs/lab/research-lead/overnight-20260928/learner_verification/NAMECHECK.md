# NAMECHECK.md - Learner-Owned Verification Worker

## Step 0: Toolchain Guard

**Date:** 2026-10-01
**Worker:** Learner-Owned Verification (Priority 1)

### Safebin Setup
```bash
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

**Result:** `guard-check-done` with no python3/python output. Safebin active.
**PATH:** `$HOME/safebin` only.

### Verification
- `which python3` returns nothing: CONFIRMED
- `which python` returns nothing: CONFIRMED
- Pinned znc: `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1` : CONFIRMED
- Pure Zag for all computation: CONFIRMED
- Shell used only for: invoking znc, running binaries, git ops, file moves: CONFIRMED

**No forbidden executable invoked. Step 0 PASS.**

## Provenance
- Base: `learner_success/ls_base.zag` lines 1-917 (cognition, minus overridden fns)
- Prediction patch: `learner_success/ls_patch.zag` (treatment, score_on=1)
- This work: unfrozen variant only. Frozen source never modified.
- Build on commit `b320213f2` (learner-success).

## Constraints
- Unfrozen variant only: YES
- Frozen read-only: YES (hash verified)
- Pure Zag: YES
- Zero em/en dashes in docs: YES (byte-verified before commit)
- Paper untouched: YES
- Nothing pushed: YES (local commits only)
- Explicit pathspecs on git add/commit: YES
