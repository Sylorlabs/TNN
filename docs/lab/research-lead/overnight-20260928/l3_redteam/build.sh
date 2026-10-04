#!/bin/sh
# L3-REDTEAM attack battery build. Pure Zag. Pinned compiler. Local only.
set -e
D=docs/lab/research-lead/overnight-20260928/l3_redteam
ZNC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
cd "$HOME/workspace/tnn-rsi"
for v in v0 v1 v2 v2s v3 v4 v5 v6; do
  cat "$D/$v/learner.zag" "$D/$v/driver.zag" > "$D/$v/full.zag"
  "$ZNC" "$D/$v/full.zag" -o "$D/$v/bin" 2> "$D/$v/compile.log"
  echo "$v build ok"
done
ls -l "$D"/v*/bin
echo "build-done"
