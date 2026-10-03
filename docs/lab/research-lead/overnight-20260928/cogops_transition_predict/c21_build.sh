#!/bin/sh
# c21_build.sh -- assemble and compile the cogops-transition-predict battery.
# Builds on c20h: frozen base, world, learn prefix, strat additive.
# c21 adds NO new kinds (proven kinds 2,4,8,9 reused); the new worlds
# are new (k, ledger) parameters. Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
B="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928"
A="$B/cogops_alternation_world"
D="$B/cogops_leadership_transition"
C="$B/cogops_transition_predict"
cd "$C"
# frozen learn prefix: same as c20h (1331-line c12 head + strat additive)
cp "$D/c20h_learn.zag" c21h_learn.zag
cmp c21h_learn.zag "$D/c20h_learn.zag" || { echo "LEARN MISMATCH"; exit 1; }
echo "learn cmp-identical to c20h"
cat "$D/c20_base.zag" "$A/c18_world.zag" "$D/c20_world_add.zag" c21h_learn.zag c21_main.zag > c21h_full.zag
echo "main count c21h (expect 1):"
grep -c "^fn main(" c21h_full.zag
"$ZNC" c21h_full.zag -o c21h_bin > c21h_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT c21h_bin"; else echo "FAILED c21h_bin"; tail -30 c21h_compile.txt; exit 1; fi
echo "build-done"
