#!/bin/sh
# is_build.sh -- assemble and compile the integration-stress battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/integration_stress"
cd "$D"
cat is_base.zag is_world.zag is_module.zag is_learn.zag is_main.zag > is_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" is_full.zag
"$ZNC" is_full.zag -o is_bin > is_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT is_bin"; else echo "FAILED is_bin"; tail -30 is_compile.txt; exit 1; fi
echo "build-done"
