#!/bin/bash
# hyptest native build (Crew M).
# Assembles the substrate (IO, SHA256, common, st_memory_core) with hyptest.zag
# into one translation unit and compiles it with the pinned znc.
# Paths are resolved relative to this script's location (relocation-safe).
# The assembled unit and the binary live in the scratch dir (never committed).
#
# usage: build.sh <delib:1|0> <scratch_dir> <binary_path>
#   delib=1 -> full hypothesis-testing loop
#   delib=0 -> deliberation-disabled variant (hypothesize/adjudicate no-ops)
set -e
DELIB="$1"; SCRATCH="$2"; BIN="$3"
if [ "$DELIB" != "1" ] && [ "$DELIB" != "0" ]; then echo "delib must be 1 or 0"; exit 2; fi
if [ -z "$SCRATCH" ] || [ -z "$BIN" ]; then echo "usage: build.sh <delib> <scratch_dir> <binary_path>"; exit 2; fi
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# substrate lives under docs/lab/continual_learning/build/substrate in the worktree
SUB="$SCRIPT_DIR/../../continual_learning/build/substrate"
BODY="$SCRIPT_DIR/hyptest.zag"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
if [ ! -f "$SUB/st_memory_core.zag" ]; then echo "substrate not found at $SUB"; exit 2; fi
if [ ! -f "$BODY" ]; then echo "body not found at $BODY"; exit 2; fi
if [ ! -x "$ZNC" ]; then echo "znc not found at $ZNC"; exit 2; fi
mkdir -p "$SCRATCH"
ALL="$SCRATCH/hyptest_all.zag"
cat "$SUB/R33_NATIVE_IO_V1.zag" > "$ALL"
grep -v '^@import(' "$SUB/R33_NATIVE_SHA256_V2.zag" >> "$ALL"
grep -v '^@import(' "$SUB/cl/common.zag" >> "$ALL"
grep -v '^@import(' "$SUB/st_memory_core.zag" >> "$ALL"
sed "s/^const HT_DELIB:i32=1;/const HT_DELIB:i32=$DELIB;/" "$BODY" >> "$ALL"
"$ZNC" "$ALL" -o "$BIN"
echo "built $BIN (delib=$DELIB)"
sha256sum "$BIN"
