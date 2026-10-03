#!/bin/sh
# sus_build.sh -- assemble and compile the COMPOSE-SUSPEND-1 battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/compose_suspend_1"
cd "$D" || exit 1
BASE="sus_base.zag sus_thunk.zag sus_asm.zag sus_rev.zag sus_world.zag"
cat $BASE sus_main.zag > sus_full.zag
echo "main count full (expect 1):"
grep -c "^fn main(" sus_full.zag
cat $BASE sus_blindmain.zag > sus_blind.zag
echo "main count blind (expect 1):"
grep -c "^fn main(" sus_blind.zag
"$ZNC" sus_full.zag -o sus_bin > sus_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT sus_bin"; else echo "FAILED sus_bin"; tail -30 sus_compile.txt; exit 1; fi
"$ZNC" sus_blind.zag -o sus_blind_bin > sus_blind_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT sus_blind_bin"; else echo "FAILED sus_blind_bin"; tail -30 sus_blind_compile.txt; exit 1; fi
echo "build-done"
