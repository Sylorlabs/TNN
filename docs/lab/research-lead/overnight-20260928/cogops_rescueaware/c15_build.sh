#!/bin/sh
# c15_build.sh -- assemble and compile the cogops-rescueaware battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_rescueaware"
cd "$D"
head -n 1331 ../cogops_optimistic/c12_learn.zag > c15_learn.zag
cat c15_strat_additive.zag >> c15_learn.zag
cat c15_base.zag c15_world.zag c15_learn.zag c15_main.zag > c15_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c15_full.zag
"$ZNC" c15_full.zag -o c15_bin > c15_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c15_bin"; else echo "FAILED c15_bin"; tail -30 c15_compile.txt; exit 1; fi
echo "build-done"
