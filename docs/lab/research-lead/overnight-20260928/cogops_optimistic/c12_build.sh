#!/bin/sh
# c12_build.sh -- assemble and compile the cogops-optimistic battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_optimistic"
cd "$D"
head -n 1331 ../cogops_costaware/c11_learn.zag > c12_learn.zag
cat c12_strat_additive.zag >> c12_learn.zag
cat c12_base.zag c12_world.zag c12_learn.zag c12_main.zag > c12_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c12_full.zag
"$ZNC" c12_full.zag -o c12_bin > c12_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c12_bin"; else echo "FAILED c12_bin"; tail -30 c12_compile.txt; exit 1; fi
echo "build-done"
