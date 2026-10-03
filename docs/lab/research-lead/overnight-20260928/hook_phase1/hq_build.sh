#!/bin/sh
# hq_build.sh -- assemble and compile the hook-phase1 battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/hook_phase1"
cd "$D"
cat hq_base.zag hq_world.zag hq_module.zag hq_learn.zag hq_main.zag > hq_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" hq_full.zag
"$ZNC" hq_full.zag -o hq_bin > hq_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT hq_bin"; else echo "FAILED hq_bin"; tail -30 hq_compile.txt; exit 1; fi
echo "build-done"
