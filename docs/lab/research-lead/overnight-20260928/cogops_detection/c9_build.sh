#!/bin/sh
# c9_build.sh -- assemble and compile the cogops-detection battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_detection"
cd "$D"
cat c9_base.zag c9_world.zag c9_learn.zag c9_main.zag > c9_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c9_full.zag
"$ZNC" c9_full.zag -o c9_bin > c9_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c9_bin"; else echo "FAILED c9_bin"; tail -30 c9_compile.txt; exit 1; fi
echo "build-done"
