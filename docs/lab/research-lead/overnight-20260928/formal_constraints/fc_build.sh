#!/bin/sh
# fc_build.sh -- compile the learner-built constraint channel experiment.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/formal_constraints"
cd "$D"
echo "dup check (expect 1):"
grep -c "^fn main(" "$D/fc_main.zag"
"$ZNC" "$D/fc_main.zag" -o "$D/fc_bin" > "$D/fc_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT fc_bin"; else echo "FAILED fc_bin"; tail -30 "$D/fc_compile.txt"; exit 1; fi
echo "build-done"
