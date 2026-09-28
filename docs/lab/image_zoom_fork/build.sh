#!/bin/bash
# build.sh — build ingest + emit for the zoom fork
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd "$(dirname "$0")"
$ZNC ingest.zag -o ingest_bin 2>ingest_build.log || { echo "INGEST BUILD FAILED"; tail -30 ingest_build.log; exit 1; }
$ZNC emit.zag -o emit_bin 2>emit_build.log || { echo "EMIT BUILD FAILED"; tail -30 emit_build.log; exit 1; }
echo "build ok"
