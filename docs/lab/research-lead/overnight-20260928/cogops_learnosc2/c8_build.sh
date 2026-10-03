#!/bin/sh
# c8_build.sh -- assemble and compile the cogops-learnosc2 ablation battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_learnosc2"
cd "$D"
cat c8_base.zag c8_world.zag c8_learn.zag c8_main.zag > c8_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c8_full.zag
"$ZNC" c8_full.zag -o c8_bin > c8_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c8_bin"; else echo "FAILED c8_bin"; tail -30 c8_compile.txt; exit 1; fi
echo "build-done"
