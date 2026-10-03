#!/bin/sh
# bc_build.sh -- assemble and compile the COMPOSE-BACKCHAIN-1 battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/compose_backchain_1"
cd "$D" || exit 1
BASE="bc_base.zag bc_thunk.zag bc_search.zag bc_world.zag"
cat $BASE bc_main.zag > bc_full.zag
echo "main count full (expect 1):"
grep -c "^fn main(" bc_full.zag
cat $BASE bc_blindmain.zag > bc_blind.zag
echo "main count blind (expect 1):"
grep -c "^fn main(" bc_blind.zag
"$ZNC" bc_full.zag -o bc_bin > bc_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT bc_bin"; else echo "FAILED bc_bin"; tail -30 bc_compile.txt; exit 1; fi
"$ZNC" bc_blind.zag -o bc_blind_bin > bc_blind_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT bc_blind_bin"; else echo "FAILED bc_blind_bin"; tail -30 bc_blind_compile.txt; exit 1; fi
echo "build-done"
