#!/bin/sh
# rt_build.sh -- INTEG-BREAK redteam build. Pure Zag via safebin PATH.
# Guard: python3/python must not resolve under this PATH.
export PATH="$HOME/safebin"
if which python3 python 2>/dev/null; then
  echo "GUARD-FAIL: forbidden interpreter resolvable"; exit 1
fi
echo "GUARD-OK: no python3/python in PATH"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D=$(dirname "$0")
cd "$D" || exit 1
# Attack binary: pristine frozen sources + attack driver.
cat cc_base.zag un_patch.zag adapt_patch.zag revise_patch.zag ts_patch.zag lvcomp_patch.zag integ_patch.zag rt_attack.zag > rt_full.zag
"$ZNC" rt_full.zag -o rt_bin > rt_compile.txt 2>&1
echo "attack compile exit: $?"
# Guard binary: guarded copies + guard-test driver.
cat cc_base_g.zag un_patch.zag adapt_patch.zag revise_patch.zag ts_patch_g.zag lvcomp_patch_g.zag integ_patch.zag rt_guardtest.zag > rt_guard_full.zag
"$ZNC" rt_guard_full.zag -o rt_guard_bin > rtg_compile.txt 2>&1
echo "guard compile exit: $?"
# T3 call-site census (static): every t2_exec site replays by construction
# (it executes the assembled graph); recorded for the report.
echo "--- t2_exec call sites (replay) ---"
grep -n "t2_exec(W" rt_full.zag | grep -v "^412:fn t2_exec"
echo "--- live-fact re-derive sites ---"
grep -c "t2_lu_first(W" rt_full.zag
