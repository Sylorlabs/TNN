#!/bin/sh
# Core Freeze Challenge run harness (Stage 2).
# POSIX shell only. No Python. Uses sha256sum, cmp, grep, awk, sed.
# Usage: run_world.sh <world.txt> <state_in.bin> <state_out.bin> <out.txt>
# Runs the frozen binary on one world file, capturing stdout and the new state.
# The state_in is copied to state_out first (so the binary's load-modify-write
# is contained), then the binary runs as: bin <world.txt> <state_out.bin>.

set -u
BIN="$1"; WORLD="$2"; SIN="$3"; SOUT="$4"; OUT="$5"
FROZEN_BIN_HASH="8733af3d28148263f9ce41d979043379b9e6d637f09dcab42eff2374f3a59960"

# K1: verify binary hash before every world.
H=$(sha256sum "$BIN" | awk '{print $1}')
if [ "$H" != "$FROZEN_BIN_HASH" ]; then
  echo "VOID: binary hash mismatch before world $WORLD" >&2
  echo "  got      $H" >&2
  echo "  expected $FROZEN_BIN_HASH" >&2
  exit 10
fi

# Copy state in -> out (binary loads, processes, writes back).
cp "$SIN" "$SOUT" || exit 11

# Run with wall-clock timing.
START=$(date +%s%N)
"$BIN" "$WORLD" "$SOUT" > "$OUT" 2> "$OUT.stderr"
RC=$?
END=$(date +%s%N)
echo "$RC" > "$OUT.rc"
echo $(( (END - START) / 1000000 )) > "$OUT.ms"

# Report state hash after.
sha256sum "$SOUT" | awk '{print $1}' > "$OUT.statehash"
exit 0
