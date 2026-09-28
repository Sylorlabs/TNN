#!/bin/bash
# Fork D build script - deterministic, no RNG.
set -e
cd "$(dirname "$0")/src"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
echo "Compiling forkD..."
$ZNC main.zag -o forkD 2>&1 | head -5
echo "Build complete: src/forkD"
# Verify no RNG in sources.
echo "Checking for RNG..."
if grep -rni "rand\|rng\|seed\|clock\|getrandom" *.zag | grep -v "^.*://"; then
    echo "ERROR: RNG found!"
    exit 1
fi
echo "No RNG found. OK."
