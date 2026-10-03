#!/bin/sh
# si_build.sh -- assemble and compile the stale-index-recovery battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/stale_index"
cd "$D"
cat si_base.zag si_world.zag si_module.zag si_learn.zag si_main.zag > si_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" si_full.zag
"$ZNC" si_full.zag -o si_bin > si_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT si_bin"; else echo "FAILED si_bin"; tail -30 si_compile.txt; exit 1; fi
echo "build-done"
