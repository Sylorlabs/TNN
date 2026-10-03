#!/bin/sh
# c18_build.sh -- assemble and compile the cogops-alternation-world battery.
# Two binaries from one lane, differing ONLY in the additive strategy
# section: c18 (no hedge, c17 strat_sel) and c18h (with hedge, c16
# strat_sel). Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/cogops_alternation_world"
B="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928"
cd "$D"
head -n 1331 $B/cogops_optimistic/c12_learn.zag > c18_learn.zag
cat c18_strat_additive.zag >> c18_learn.zag
head -n 1331 $B/cogops_optimistic/c12_learn.zag > c18h_learn.zag
cat c18h_strat_additive.zag >> c18h_learn.zag
cat c18_base.zag c18_world.zag c18_learn.zag c18_main.zag > c18_full.zag
cat c18_base.zag c18_world.zag c18h_learn.zag c18_main.zag > c18h_full.zag
echo "main count c18 (expect 1):"
grep -c "^fn main(" c18_full.zag
echo "main count c18h (expect 1):"
grep -c "^fn main(" c18h_full.zag
"$ZNC" c18_full.zag -o c18_bin > c18_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c18_bin"; else echo "FAILED c18_bin"; tail -30 c18_compile.txt; exit 1; fi
"$ZNC" c18h_full.zag -o c18h_bin > c18h_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c18h_bin"; else echo "FAILED c18h_bin"; tail -30 c18h_compile.txt; exit 1; fi
echo "build-done"
