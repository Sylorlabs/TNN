#!/bin/sh
# es_build.sh -- assemble and compile the epoch-strong probe battery.
# Pure shell + pinned znc. No Python.
export PATH="$HOME/safebin"
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
D="$HOME/workspace/tnn-rsi-gpi3/docs/lab/research-lead/overnight-20260928/epoch_strong"
cd "$D"
cat es_base.zag es_world.zag es_module.zag es_learn.zag es_main.zag > es_full.zag
echo "main count (expect 1):"
grep -c "^fn main(" es_full.zag
"$ZNC" es_full.zag -o es_bin > es_compile.txt 2>&1
if [ $? -eq 0 ]; then echo "BUILT es_bin"; else echo "FAILED es_bin"; tail -30 es_compile.txt; exit 1; fi
echo "build-done"
