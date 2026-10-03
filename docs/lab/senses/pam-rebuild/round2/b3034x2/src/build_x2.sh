#!/bin/bash
# build_x2.sh — build the B-3034X2 binaries with the PINNED toolchain.
# Usage: ./build_x2.sh <outdir>
# The pinned znc lives at ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
set -euo pipefail
OUTDIR="${1:?outdir required}"
SRC="$(dirname "$0")"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
cd "$SRC"
"$ZNC" x2_battery.zag -o "$OUTDIR/x2_full"
"$ZNC" x2_nopmain.zag -o "$OUTDIR/x2_nop"
echo "built: $OUTDIR/x2_full $OUTDIR/x2_nop"
