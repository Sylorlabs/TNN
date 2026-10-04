#!/bin/bash
# sensbuild.sh -- concatenate parts and compile through zbuild.sh.
#   sensbuild.sh OUT.zag PART1 PART2 ...
# Note: zbuild.sh invokes the binary by BARE name, so it cannot execute
# without "." on PATH. This script therefore only BUILDS; use sensrun.sh to
# execute under the watchdog (brief 10.1).
set -eu
OUT="$1"; shift
rm -f "$OUT" "$(basename "$OUT" .zag)" 2>/dev/null || true
cat "$@" > "$OUT"
echo "[sensbuild] $OUT  ($(wc -l < "$OUT" | tr -d ' ') lines)  <- $*"
/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh "$OUT" 2>&1 | grep -E '^\[znc\]|^\[zbuild\]' || true
B="$(basename "$OUT" .zag)"
[ -x "./$B" ] || { echo "[sensbuild] COMPILE-FAIL $OUT"; exit 1; }
echo "[sensbuild] OK $OUT -> ./$B"
