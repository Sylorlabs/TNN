#!/bin/sh
# COGOPSLESION build+run harness. Orchestration only; all computation in Zag.
#
# Usage: mk.sh <additive.zag> <tag> [main.zag]
# Assembles base + world + frozen_prefix + <additive> + <main> and runs.
# Only the additive varies between grid cells.
# VERIFIED: additive=inc_c15, main=main.zag reproduces
# cogops_rescueaware/c15_run1.txt byte-for-byte on this host.
set -eu
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D="$(cd "$(dirname "$0")" && pwd)"
INC="$1"; TAG="$2"; MAIN="${3:-$D/ref/main.zag}"
SRC="$D/tu/U_$TAG.zag"
mkdir -p "$D/tu" "$D/out"
cat "$D/ref/base.zag" "$D/ref/world.zag" "$D/ref/frozen_prefix.zag" \
    "$INC" "$MAIN" > "$SRC"
/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh "$SRC" > "$D/out/$TAG.buildlog" 2>&1 \
  || { echo "$TAG BUILD-FAIL"; tail -5 "$D/out/$TAG.buildlog"; exit 1; }
./tu/U_$TAG > "$D/out/$TAG.txt" 2>"$D/out/$TAG.err"
echo "$TAG: $(wc -l < "$D/out/$TAG.txt" | tr -d ' ') lines $(wc -c < "$D/out/$TAG.txt" | tr -d ' ') bytes $(shasum -a 256 "$D/out/$TAG.txt" | cut -c1-16)"