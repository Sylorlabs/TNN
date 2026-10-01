#!/bin/bash
# Build script for adaptive threshold experiments. Pure shell + znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
DIR="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/adaptive_threshold"
cd "$DIR"

cat at_core_adaptive.zag at_tests.zag at_drv_adaptive.zag > /tmp/at_adaptive_full.zag
"$ZNC" /tmp/at_adaptive_full.zag -o "$DIR/at_bin_adaptive"
if [ $? -eq 0 ]; then echo "BUILT at_bin_adaptive"; else echo "FAILED at_bin_adaptive"; exit 1; fi

cat at_core_fixed.zag at_tests.zag at_drv_fixed.zag > /tmp/at_fixed_full.zag
"$ZNC" /tmp/at_fixed_full.zag -o "$DIR/at_bin_fixed"
if [ $? -eq 0 ]; then echo "BUILT at_bin_fixed"; else echo "FAILED at_bin_fixed"; exit 1; fi

echo "build-done"
