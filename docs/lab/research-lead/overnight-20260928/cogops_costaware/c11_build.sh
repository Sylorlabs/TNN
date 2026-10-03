#!/bin/sh
# c11_build.sh -- assemble and compile the cogops-costaware battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_costaware"
cd "$D"
head -n 1331 ../cogops_strategy/c10_learn.zag > c11_learn.zag
cat c11_strat_additive.zag >> c11_learn.zag
cat c11_base.zag c11_world.zag c11_learn.zag c11_main.zag > c11_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c11_full.zag
"$ZNC" c11_full.zag -o c11_bin > c11_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c11_bin"; else echo "FAILED c11_bin"; tail -30 c11_compile.txt; exit 1; fi
echo "build-done"
