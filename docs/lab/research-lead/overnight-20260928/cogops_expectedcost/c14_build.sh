#!/bin/sh
# c14_build.sh -- assemble and compile the cogops-expectedcost battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_expectedcost"
cd "$D"
head -n 1331 ../cogops_optimistic/c12_learn.zag > c14_learn.zag
cat c14_strat_additive.zag >> c14_learn.zag
cat c14_base.zag c14_world.zag c14_learn.zag c14_main.zag > c14_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c14_full.zag
"$ZNC" c14_full.zag -o c14_bin > c14_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c14_bin"; else echo "FAILED c14_bin"; tail -30 c14_compile.txt; exit 1; fi
echo "build-done"
