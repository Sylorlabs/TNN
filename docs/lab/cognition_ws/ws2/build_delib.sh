#!/bin/bash
# Build the WS2-C deliberative engine (pure Zag, pinned znc).
set -e
ZNC=${ZNC:-~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}
SRC=${SRC:-~/workspace/cognition_ws/ws2/delib.zag}
OUTDIR=${OUTDIR:-~/workspace/cognition_ws/ws2/build}
mkdir -p "$OUTDIR"
cp "$SRC" "$OUTDIR/delib.zag"
cp ~/workspace/tnn-lab/toolchain/R33_NATIVE_SHA256_V2.zag "$OUTDIR/"
cp ~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag "$OUTDIR/"
cd "$OUTDIR"
"$ZNC" delib.zag -o delib
echo "built $OUTDIR/delib"
