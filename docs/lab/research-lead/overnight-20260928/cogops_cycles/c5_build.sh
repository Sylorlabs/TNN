#!/bin/sh
# c5_build.sh -- assemble and compile the cogops-cycles battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_cycles"
cd "$D"
cat c5_base.zag c5_world.zag c5_learn.zag c5_main.zag > c5_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c5_full.zag
"$ZNC" c5_full.zag -o c5_bin > c5_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c5_bin"; else echo "FAILED c5_bin"; tail -30 c5_compile.txt; exit 1; fi
echo "build-done"
