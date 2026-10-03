#!/bin/sh
# integ2_build.sh -- H-COMPINTEG-2 build. Pure Zag via safebin PATH.
# Guard: python3/python must not resolve under this PATH.
export PATH="$HOME/safebin"
if which python3 python 2>/dev/null; then
  echo "GUARD-FAIL: forbidden interpreter resolvable"; exit 1
fi
echo "GUARD-OK: no python3/python in PATH"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D=$(dirname "$0")
cd "$D" || exit 1
cat cc_base_g.zag un_patch.zag adapt_patch.zag revise_patch.zag ts_patch_g.zag lvcomp_patch_g.zag integ_patch.zag integ2_patch.zag integ2_driver.zag > integ2_full.zag
"$ZNC" integ2_full.zag -o integ2_bin > integ2_compile.txt 2>&1
echo "compile exit: $?"
wc -l integ2_patch.zag
grep -c "expected" integ2_patch.zag || true
grep -n 'while.*!(' integ2_patch.zag integ2_driver.zag || echo "no negated-conjunction while loops"
