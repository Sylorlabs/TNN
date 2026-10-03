#!/bin/sh
# c10_build.sh -- assemble and compile the cogops-strategy battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_strategy"
cd "$D"
head -n 1331 ../cogops_detection/c9_learn.zag > c10_learn.zag
cat c10_strat_additive.zag >> c10_learn.zag
cat c10_base.zag c10_world.zag c10_learn.zag c10_main.zag > c10_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c10_full.zag
"$ZNC" c10_full.zag -o c10_bin > c10_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c10_bin"; else echo "FAILED c10_bin"; tail -30 c10_compile.txt; exit 1; fi
echo "build-done"
