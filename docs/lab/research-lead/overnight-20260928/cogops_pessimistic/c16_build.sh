#!/bin/sh
# c16_build.sh -- assemble and compile the cogops-pessimistic battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_pessimistic"
cd "$D"
head -n 1331 ../cogops_optimistic/c12_learn.zag > c16_learn.zag
cat c16_strat_additive.zag >> c16_learn.zag
cat c16_base.zag c16_world.zag c16_learn.zag c16_main.zag > c16_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c16_full.zag
"$ZNC" c16_full.zag -o c16_bin > c16_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c16_bin"; else echo "FAILED c16_bin"; tail -30 c16_compile.txt; exit 1; fi
echo "build-done"
