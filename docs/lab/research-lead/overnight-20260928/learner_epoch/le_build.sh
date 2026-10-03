#!/bin/sh
# le_build.sh -- assemble and compile the learner-epoch battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/learner_epoch"
cd "$D"
cat le_base.zag le_world.zag le_module.zag le_learn.zag le_main.zag > le_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" le_full.zag
"$ZNC" le_full.zag -o le_bin > le_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT le_bin"; else echo "FAILED le_bin"; tail -30 le_compile.txt; exit 1; fi
echo "build-done"
