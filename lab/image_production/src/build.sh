#!/bin/bash
# Build the adaptive-layers + adaptive-magnification fork.
# Pinned toolchain (same as all parents).
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
"$ZNC" azingest.zag -o azingest_bin
"$ZNC" azemit.zag -o azemit_bin
echo "build ok"
