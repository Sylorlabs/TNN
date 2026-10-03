#!/bin/sh
# cc_build.sh -- assemble and compile the cogops-compose battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_compose"
cd "$D"
cat cc_base.zag cc_world.zag cc_learn.zag cc_main.zag > cc_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" cc_full.zag
"$ZNC" cc_full.zag -o cc_bin > cc_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT cc_bin"; else echo "FAILED cc_bin"; tail -30 cc_compile.txt; exit 1; fi
echo "build-done"
