#!/bin/bash
# Build onebrain (Experiment 2 implementer). Pure Zag, zero RNG.
# Toolchain pinned per AGENTS.md.
set -e
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
DIR="$(cd "$(dirname "$0")" && pwd)"
"$ZNC" "$DIR/onebrain.zag" -o "$DIR/onebrain"
echo "BUILD OK: $DIR/onebrain"
