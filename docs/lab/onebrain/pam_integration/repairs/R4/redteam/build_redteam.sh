#!/bin/bash
# build_redteam.sh — compile the ONE-BRAIN + SELF-PAM red-team battery.
# Pinned toolchain only. Fails loudly.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
SRC="$HERE/src"
OUT="$HERE/ob_redteam_bin"

[ -x "$ZNC" ] || { echo "FATAL: pinned znc not found at $ZNC" >&2; exit 1; }

# @import paths resolve relative to CWD in this znc build: compile from src/.
cd "$SRC"
"$ZNC" ob_test_redteam.zag -o "$OUT"

[ -x "$OUT" ] || { echo "FATAL: build produced no binary" >&2; exit 1; }
echo "BUILD_OK $OUT"
