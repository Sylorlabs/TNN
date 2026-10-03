#!/bin/sh
# c22_build.sh -- assemble and compile the cogops-transition-predict-2 battery.
# Builds on c20h: frozen base, world, learn prefix, strat additive.
# c22 adds new goal constructors (mk_goal2r/mk_goal8r) with fresh need1
# rels per arc; the (k, ledger) parameters are new. Pure shell + pinned
# znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
B="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928"
A="$B/cogops_alternation_world"
D="$B/cogops_leadership_transition"
C="$B/cogops_transition_predict2"
cd "$C"
# frozen learn prefix: same as c20h/c21 (c20h_learn.zag)
cat "$D/c20_base.zag" "$A/c18_world.zag" "$D/c20_world_add.zag" c22_world_add.zag "$D/c20h_learn.zag" c22_main.zag > c22h_full.zag
echo "main count c22h (expect 1):"
grep -c "^fn main(" c22h_full.zag
"$ZNC" c22h_full.zag -o c22h_bin > c22h_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c22h_bin"; else echo "FAILED c22h_bin"; tail -30 c22h_compile.txt; exit 1; fi
echo "build-done"
