#!/bin/sh
# c13_build.sh -- assemble and compile the cogops-percontext battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_percontext"
cd "$D"
head -n 1331 ../cogops_optimistic/c12_learn.zag > c13_learn.zag
cat c13_strat_additive.zag >> c13_learn.zag
cat c13_base.zag c13_world.zag c13_learn.zag c13_main.zag > c13_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c13_full.zag
"$ZNC" c13_full.zag -o c13_bin > c13_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c13_bin"; else echo "FAILED c13_bin"; tail -30 c13_compile.txt; exit 1; fi
echo "build-done"
