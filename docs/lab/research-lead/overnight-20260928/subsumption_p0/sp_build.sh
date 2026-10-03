#!/bin/sh
# sp_build.sh -- assemble and compile the SUBSUMPTION-P0 battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/subsumption_p0"
cd "$D"
cat sp_base.zag sp_module.zag sp_world.zag sp_harness.zag > sp_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" sp_full.zag
"$ZNC" sp_full.zag -o sp_bin > sp_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT sp_bin"; else echo "FAILED sp_bin"; tail -30 sp_compile.txt; exit 1; fi
echo "build-done"
