#!/bin/sh
# build.sh -- H-COMPINTEG-1 build. Pure Zag via safebin PATH.
# Guard: python3/python must not resolve under this PATH.
export PATH="$HOME/safebin"
if which python3 python 2>/dev/null; then
  echo "GUARD-FAIL: forbidden interpreter resolvable"; exit 1
fi
echo "GUARD-OK: no python3/python in PATH"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
cat cc_base.zag un_patch.zag adapt_patch.zag revise_patch.zag ts_patch.zag lvcomp_patch.zag integ_patch.zag integ_driver.zag > integ_full.zag
"$ZNC" integ_full.zag -o integ_bin > compile.txt 2>&1
echo "compile exit: $?"
