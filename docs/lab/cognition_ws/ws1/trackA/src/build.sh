#!/usr/bin/env bash
# Build the WS1C Track A skepticism harness with the pinned znc toolchain.
# Usage: ./build.sh [output-binary]
# The binary is a scratch artifact and is never committed.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
OUT="${1:-$HERE/skep_main}"
cd "$HERE"
exec "$ZNC" skep_main.zag --no-zagd --no-analyze --no-foreground-cache -o "$OUT"
