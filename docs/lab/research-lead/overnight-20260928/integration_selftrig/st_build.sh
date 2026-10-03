#!/bin/sh
# st_build.sh -- assemble and compile the integration-selftrig battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/integration_selftrig"
cd "$D"
cat st_base.zag st_world.zag st_module.zag st_learn.zag st_main.zag > st_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" st_full.zag
"$ZNC" st_full.zag -o st_bin > st_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT st_bin"; else echo "FAILED st_bin"; tail -30 st_compile.txt; exit 1; fi
echo "build-done"
