#!/bin/sh
# c6_build.sh -- assemble and compile the cogops-oscillatory battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_oscillatory"
cd "$D"
cat c6_base.zag c6_world.zag c6_learn.zag c6_main.zag > c6_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c6_full.zag
"$ZNC" c6_full.zag -o c6_bin > c6_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c6_bin"; else echo "FAILED c6_bin"; tail -30 c6_compile.txt; exit 1; fi
echo "build-done"
