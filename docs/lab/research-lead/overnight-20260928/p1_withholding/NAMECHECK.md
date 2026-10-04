# NAMECHECK.md - P1-Deep Withholding Worker

## Step 0: Toolchain Guard

**Date:** 2026-10-01
**Worker:** P1-Deep Withholding (learner-owned verification for withholding)

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

### Verification
- `which python3` returns nothing: CONFIRMED
- `which python` returns nothing: CONFIRMED
- Pinned znc: `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`: CONFIRMED
- Pure Zag for all computation: CONFIRMED
- Shell used only for: invoking znc, running binaries, git ops, file moves: CONFIRMED

**No forbidden executable invoked. Step 0 PASS.**

## Provenance
- Base cognition: `learner_verification/lv_cog.zag` (872 lines, from C181 `d52666a8b`)
- Prediction section: `learner_verification/lv_full_trt.zag` lines 873-1041 (ev_predict, pred_resolve, pred_record)
- This work: `wh_patch.zag` (withholding decision + learner-owned threshold) and `wh_driver.zag` (3 batteries)
- Unfrozen variant only. Frozen source never modified.
- Builds on commit `d52666a8b` (learner-verification, C181).

## Constraints
- Unfrozen variant only: YES
- Frozen read-only: YES
- Pure Zag: YES
- Zero em/en dashes in docs: YES (byte-verified before commit)
- Paper untouched: YES
- Nothing pushed: YES (local commits only)
- Explicit pathspecs on git add/commit: YES
