#!/bin/sh
# c3_build.sh -- assemble and compile the cogops-3way battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_3way"
cd "$D"
cat c3_base.zag c3_world.zag c3_learn.zag c3_main.zag > c3_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c3_full.zag
"$ZNC" c3_full.zag -o c3_bin > c3_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c3_bin"; else echo "FAILED c3_bin"; tail -30 c3_compile.txt; exit 1; fi
echo "build-done"
