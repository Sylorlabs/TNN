#!/bin/sh
# col_build.sh -- assemble and compile the cognitive-ops-learner battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cognitive_ops_learner"
cd "$D"
cat col_base.zag col_world.zag col_learn.zag col_main.zag > col_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" col_full.zag
"$ZNC" col_full.zag -o col_bin > col_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT col_bin"; else echo "FAILED col_bin"; tail -30 col_compile.txt; exit 1; fi
echo "build-done"
