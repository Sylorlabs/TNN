#!/bin/sh
# hp_build.sh -- assemble and compile the hook-phase0 battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/hook_phase0"
cd "$D"
cat hp_base.zag hp_world.zag hp_module.zag hp_learn.zag hp_main.zag > hp_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" hp_full.zag
"$ZNC" hp_full.zag -o hp_bin > hp_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT hp_bin"; else echo "FAILED hp_bin"; tail -30 hp_compile.txt; exit 1; fi
echo "build-done"
