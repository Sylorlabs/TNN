#!/usr/bin/env bash
# Build the H5 deliberation harness with the pinned znc toolchain.
# Usage: ./build.sh [output-binary]
# The binary is a scratch artifact and is never committed.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
OUT="${1:-$HERE/delib_harness}"
cd "$HERE"
exec "$ZNC" delib_harness.zag --no-zagd --no-analyze --no-foreground-cache -o "$OUT"
