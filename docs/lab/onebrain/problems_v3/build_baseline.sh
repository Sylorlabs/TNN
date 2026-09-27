#!/bin/sh
# Build the onebrain Experiment 2 single-deliberation baseline.
# Pinned toolchain per lab convention.
set -e
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
cd "$(dirname "$0")"
"$ZNC" baseline.zag -o baseline_bin
echo "built baseline_bin"
