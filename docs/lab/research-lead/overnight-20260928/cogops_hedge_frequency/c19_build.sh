#!/bin/sh
# c19_build.sh -- assemble and compile the cogops-hedge-frequency battery.
# Two binaries from one lane, differing ONLY in the additive strategy
# section: c19 (no hedge, c18 strat_sel verbatim) and c19h (with hedge,
# c18h strat_sel + 2 log-only det_ev instrumentation lines).
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
B="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928"
A="$B/cogops_alternation_world"
D="$B/cogops_hedge_frequency"
cd "$D"
cp "$A/c18_base.zag" c19_base.zag
head -n 1331 "$B/cogops_optimistic/c12_learn.zag" > c19_learn.zag
cat c19_strat_additive.zag >> c19_learn.zag
head -n 1331 "$B/cogops_optimistic/c12_learn.zag" > c19h_learn.zag
cat c19h_strat_additive.zag >> c19h_learn.zag
cat c19_base.zag "$A/c18_world.zag" c19_world_add.zag c19_learn.zag c19_main.zag > c19_full.zag
cat c19_base.zag "$A/c18_world.zag" c19_world_add.zag c19h_learn.zag c19_main.zag > c19h_full.zag
echo "main count c19 (expect 1):"
grep -c "^fn main(" c19_full.zag
echo "main count c19h (expect 1):"
grep -c "^fn main(" c19h_full.zag
"$ZNC" c19_full.zag -o c19_bin > c19_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c19_bin"; else echo "FAILED c19_bin"; tail -30 c19_compile.txt; exit 1; fi
"$ZNC" c19h_full.zag -o c19h_bin > c19h_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c19h_bin"; else echo "FAILED c19h_bin"; tail -30 c19h_compile.txt; exit 1; fi
echo "build-done"
