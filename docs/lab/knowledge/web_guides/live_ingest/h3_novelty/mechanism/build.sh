#!/bin/bash
# H3 novel.zag build — pinned znc toolchain, deterministic, zero RNG.
# Usage: build.sh [LESION] [OUT]
#   LESION=0 (default): the committed instrument.
#   LESION=1: recall-always-match calibration control.
#   LESION=2: recall-never-match calibration control.
# Requires R33_NATIVE_IO_V1.zag next to novel.zag (the @import target).
set -euo pipefail
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
HERE="$(cd "$(dirname "$0")" && pwd)"
LESION="${1:-0}"
OUT="${2:-$HERE/novel_bin}"
case "$LESION" in 0|1|2) ;; *) echo "LESION must be 0, 1, or 2" >&2; exit 2;; esac
TMP="$HERE/.build_lesion_$LESION.zag"
sed "s/const LESION:i32=0;/const LESION:i32=$LESION;/" "$HERE/novel.zag" > "$TMP"
"$ZNC" "$TMP" -o "$OUT"
rm -f "$TMP"
sha256sum "$OUT"
