#!/bin/sh
# hc_build.sh -- assemble and compile the hook-composition battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/hook_composition"
cd "$D"
cat hc_base.zag hc_world.zag hc_module.zag hc_learn.zag hc_main.zag > hc_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" hc_full.zag
"$ZNC" hc_full.zag -o hc_bin > hc_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT hc_bin"; else echo "FAILED hc_bin"; tail -30 hc_compile.txt; exit 1; fi
echo "build-done"
