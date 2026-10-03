#!/bin/sh
# ib_build.sh -- assemble and compile the integration-b1b2 battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/integration_b1b2"
cd "$D"
cat ib_base.zag ib_world.zag ib_module.zag ib_learn.zag ib_main.zag > ib_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" ib_full.zag
"$ZNC" ib_full.zag -o ib_bin > ib_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT ib_bin"; else echo "FAILED ib_bin"; tail -30 ib_compile.txt; exit 1; fi
echo "build-done"
