#!/bin/sh
# gen_build.sh -- assemble and compile the integration-hook-generalize battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/integration_hook_gen"
cd "$D"
cat gen_base.zag gen_world.zag gen_module.zag gen_learn.zag gen_main.zag > gen_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" gen_full.zag
"$ZNC" gen_full.zag -o gen_bin > gen_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT gen_bin"; else echo "FAILED gen_bin"; tail -30 gen_compile.txt; exit 1; fi
echo "build-done"
