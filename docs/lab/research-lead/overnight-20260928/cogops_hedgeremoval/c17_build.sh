#!/bin/sh
# c17_build.sh -- assemble and compile the cogops-hedgeremoval battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_hedgeremoval"
B="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928"
cd "$D"
head -n 1331 $B/cogops_optimistic/c12_learn.zag > c17_learn.zag
cat c17_strat_additive.zag >> c17_learn.zag
cat c17_base.zag c17_world.zag c17_learn.zag c17_main.zag > c17_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" c17_full.zag
"$ZNC" c17_full.zag -o c17_bin > c17_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c17_bin"; else echo "FAILED c17_bin"; tail -30 c17_compile.txt; exit 1; fi
echo "build-done"
