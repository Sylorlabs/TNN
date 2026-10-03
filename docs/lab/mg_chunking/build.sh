#!/bin/bash
# build.sh — build the magnifying-glass chunking fork
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
$ZNC mg_chunk.zag -o mg_chunk_bin 2>build.log || { echo "BUILD FAILED"; tail -30 build.log; exit 1; }
echo "build ok"
