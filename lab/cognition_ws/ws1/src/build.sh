#!/usr/bin/env bash
# Build WS1-A binaries with the pinned znc toolchain.
# Binaries are scratch artifacts and are NEVER committed.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
OUT="$HERE/../build"
mkdir -p "$OUT"
cd "$HERE"
for t in w1a_arm1 w1a_arm3 w1a_auto; do
    echo "== building $t"
    "$ZNC" "$t.zag" --no-zagd --no-analyze --no-foreground-cache -o "$OUT/$t" || exit 1
done
echo "BUILD OK"
