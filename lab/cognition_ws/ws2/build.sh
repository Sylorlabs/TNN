#!/bin/bash
# WS2-A: build MORG arm binaries + instrumented probe driver with pinned znc.
# @import is cwd-relative: copy sources + pinned substrate files into build/ first.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
rm -rf "$HERE/build"
mkdir -p "$HERE/build"
cp "$HERE/probe.zag" ~/workspace/tnn-lab/memory_org/arms/lib.zag \
   ~/workspace/tnn-lab/memory_org/arms/arm_self.zag \
   ~/workspace/tnn-lab/memory_org/arms/arm_imposed.zag \
   ~/workspace/tnn-lab/memory_org/arms/arm_flat.zag "$HERE/build/"
cp ~/workspace/tnn-lab/toolchain/R33_NATIVE_SHA256_V2.zag \
   ~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag "$HERE/build/"
cd "$HERE/build"
for a in probe arm_self arm_imposed arm_flat; do
  "$ZNC" "$a.zag" -o "$a" 2>&1 | grep -v "zagd unavailable" || true
done
ls -la probe arm_self arm_imposed arm_flat
