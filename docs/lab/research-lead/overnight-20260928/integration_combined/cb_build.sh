#!/bin/sh
# cb_build.sh -- assemble and compile the integration-combined battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/integration_combined"
cd "$D"
cat cb_base.zag cb_world.zag cb_module.zag cb_learn.zag cb_main.zag > cb_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" cb_full.zag
"$ZNC" cb_full.zag -o cb_bin > cb_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT cb_bin"; else echo "FAILED cb_bin"; tail -30 cb_compile.txt; exit 1; fi
echo "build-done"
