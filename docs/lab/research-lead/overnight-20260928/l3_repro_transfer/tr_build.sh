#!/bin/sh
# L3-REPRO-TRANSFER build. Pure Zag. Pinned compiler. Local only.
set -e
D=docs/lab/research-lead/overnight-20260928/l3_repro_transfer
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
cd "$HOME/workspace/tnn-rsi"
cat "$D/tr_learner.zag" "$D/tr_h1.zag" > "$D/tr_h1_full.zag"
cat "$D/tr_learner.zag" "$D/tr_h2.zag" > "$D/tr_h2_full.zag"
"$ZNC" "$D/tr_h1_full.zag" -o "$D/tr_h1_bin" 2> "$D/tr_h1_compile.log"
"$ZNC" "$D/tr_h2_full.zag" -o "$D/tr_h2_bin" 2> "$D/tr_h2_compile.log"
ls -l "$D/tr_h1_bin" "$D/tr_h2_bin"
echo "build-done"
