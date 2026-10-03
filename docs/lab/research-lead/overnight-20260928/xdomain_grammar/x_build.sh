#!/bin/sh
# x_build.sh -- compile the cross-domain grammar->construction experiment.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/xdomain_grammar"
cd "$D"
echo "dup check (expect 1):"
grep -c "^fn main(" "$D/x_main.zag"
"$ZNC" "$D/x_main.zag" -o "$D/x_bin" > "$D/x_compile.txt" 2>&1
if [ $? -eq 0 ]; then echo "BUILT x_bin"; else echo "FAILED x_bin"; tail -30 "$D/x_compile.txt"; exit 1; fi
echo "build-done"
