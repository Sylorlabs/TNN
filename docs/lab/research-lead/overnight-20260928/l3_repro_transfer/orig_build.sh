#!/bin/sh
# XDOMAIN-GRAMMAR-L2M build. Pure Zag. Pinned compiler. Local only.
set -e
D=docs/lab/research-lead/overnight-20260928/xdomain_grammar_l2m
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
cd "$HOME/workspace/tnn-rsi"
cat "$D/glm_learner.zag" "$D/gl2m_h1.zag" > "$D/h1_full.zag"
cat "$D/glm_learner.zag" "$D/gl2m_h2.zag" > "$D/h2_full.zag"
"$ZNC" "$D/h1_full.zag" -o "$D/h1_bin" 2> "$D/h1_compile.log"
"$ZNC" "$D/h2_full.zag" -o "$D/h2_bin" 2> "$D/h2_compile.log"
ls -l "$D/h1_bin" "$D/h2_bin"
echo "build-done"
