#!/bin/sh
# lc_build.sh -- assemble and compile the COMPOSE-LEARNCOMPOSE-1 battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/compose_learncompose_1"
cd "$D" || exit 1
BASE="lc_base.zag lc_thunk.zag lc_search.zag lc_mem.zag lc_rev.zag lc_world.zag lc_rep.zag"
cat $BASE lc_main.zag > lc_full.zag
echo "main count full (expect 1):"
grep -c "^fn main(" lc_full.zag
cat $BASE lc_fc1main.zag > lc_fc1.zag
echo "main count fc1 (expect 1):"
grep -c "^fn main(" lc_fc1.zag
cat $BASE lc_blindmain.zag > lc_blind.zag
echo "main count blind (expect 1):"
grep -c "^fn main(" lc_blind.zag
"$ZNC" lc_full.zag -o lc_bin > lc_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT lc_bin"; else echo "FAILED lc_bin"; tail -30 lc_compile.txt; exit 1; fi
"$ZNC" lc_fc1.zag -o lc_fc1_bin > lc_fc1_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT lc_fc1_bin"; else echo "FAILED lc_fc1_bin"; tail -30 lc_fc1_compile.txt; exit 1; fi
"$ZNC" lc_blind.zag -o lc_blind_bin > lc_blind_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT lc_blind_bin"; else echo "FAILED lc_blind_bin"; tail -30 lc_blind_compile.txt; exit 1; fi
echo "build-done"
