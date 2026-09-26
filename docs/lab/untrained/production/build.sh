#!/bin/bash
# Build the production abstention-capable analyzer.
# Usage: ./build.sh [output-binary]
# Requires the pinned toolchain at ../../toolchain/bin/znc_linux_x86_64_abed8aa1
# (relative to the production directory in the repo).
set -e
ZNC="${ZNC:-$(dirname "$0")/../../../toolchain/bin/znc_linux_x86_64_abed8aa1}"
OUT="${1:-uanalyze}"
"$ZNC" build "$(dirname "$0")/uanalyze.zag" -o "$OUT"
echo "Built $OUT"
sha256sum "$OUT"
