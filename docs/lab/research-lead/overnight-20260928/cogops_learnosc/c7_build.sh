#!/bin/sh
# c7_build.sh -- assemble and compile the cogops-learnosc battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_learnosc"
cd "$D"
cat c7_base.zag c7_world.zag c7_learn.zag c7_main.zag > c7_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c7_full.zag
"$ZNC" c7_full.zag -o c7_bin > c7_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c7_bin"; else echo "FAILED c7_bin"; tail -30 c7_compile.txt; exit 1; fi
echo "build-done"
