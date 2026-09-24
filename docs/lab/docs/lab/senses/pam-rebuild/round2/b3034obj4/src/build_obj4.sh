#!/bin/bash
# build_obj4.sh — build the B-OBJ4 battery binary with the PINNED toolchain.
# Usage: ./build_obj4.sh <outdir>
# The pinned znc lives at ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
# The driver files in this dir are byte-identical to fec41193 (verified by
# script; SHAs in PREREG_RT_OBJ4.md §0). Only obj4_battery.zag is new code.
set -euo pipefail
OUTDIR="${1:?outdir required}"
SRC="$(dirname "$0")"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
cd "$SRC"
"$ZNC" obj4_battery.zag -o "$OUTDIR/obj4_bin"
echo "built: $OUTDIR/obj4_bin"
