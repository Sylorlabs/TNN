#!/bin/sh
# c20_build.sh -- assemble and compile the cogops-leadership-transition battery.
# One binary: c20h (hedge-bearing strat_sel + HGATE/HEDGE/TIE instrumentation).
# c20_base.zag is cmp-identical to c19_base.zag; the learn prefix is the
# frozen c12 head (1331 lines); the additive strat section is c19h's plus
# exactly the DET-TIE (kind 12) log-only instrumentation block.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
B="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928"
A="$B/cogops_alternation_world"
D="$B/cogops_leadership_transition"
cd "$D"
cmp c20_base.zag "$B/cogops_hedge_frequency/c19_base.zag" || { echo "BASE MISMATCH"; exit 1; }
echo "base cmp-identical"
head -n 1331 "$B/cogops_optimistic/c12_learn.zag" > c20h_learn.zag
cat c20h_strat_additive.zag >> c20h_learn.zag
cat c20_base.zag "$A/c18_world.zag" c20_world_add.zag c20h_learn.zag c20_main.zag > c20h_full.zag
echo "main count c20h (expect 1):"
grep -c "^fn main(" c20h_full.zag
"$ZNC" c20h_full.zag -o c20h_bin > c20h_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c20h_bin"; else echo "FAILED c20h_bin"; tail -30 c20h_compile.txt; exit 1; fi
echo "build-done"
