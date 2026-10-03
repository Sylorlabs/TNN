#!/bin/sh
# c4_build.sh -- assemble and compile the cogops-diamond battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_diamond"
cd "$D"
cat c4_base.zag c4_world.zag c4_learn.zag c4_main.zag > c4_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c4_full.zag
"$ZNC" c4_full.zag -o c4_bin > c4_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c4_bin"; else echo "FAILED c4_bin"; tail -30 c4_compile.txt; exit 1; fi
echo "build-done"
