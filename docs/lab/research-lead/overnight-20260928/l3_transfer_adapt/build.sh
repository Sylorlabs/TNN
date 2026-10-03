#!/bin/sh
# l3_transfer_adapt build. Pure Zag. Pinned compiler. Local only.
set -e
D=docs/lab/research-lead/overnight-20260928/l3_transfer_adapt
ZNC="$HOME/safebin/znc"
cd "$HOME/workspace/tnn-rsi"
cat "$D/learner.zag" "$D/driver.zag" > "$D/full.zag"
"$ZNC" "$D/full.zag" -o "$D/l3a_bin" 2> "$D/compile.log"
echo "build ok"
ls -l "$D/l3a_bin"
