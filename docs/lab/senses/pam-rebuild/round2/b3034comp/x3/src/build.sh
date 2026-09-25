#!/bin/bash
# build.sh — compile the B-3034X3 battery from src/ (imports are cwd-relative).
# Usage: ./build.sh [outdir]   (default outdir: .)
set -e
cd "$(dirname "$0")"
OUT="${1:-.}"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
"$ZNC" x3_main.zag -o "$OUT/x3_battery"
echo "built $OUT/x3_battery"
