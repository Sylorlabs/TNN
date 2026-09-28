#!/bin/bash
# Build the three MORG arm binaries with the pinned znc toolchain.
# @import is cwd-relative: copy lib + pinned substrate files into build/ first.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
rm -rf "$HERE/build"
mkdir -p "$HERE/build"
cp "$HERE/lib.zag" "$HERE/arm_self.zag" "$HERE/arm_imposed.zag" "$HERE/arm_flat.zag" "$HERE/build/"
cp ~/workspace/tnn-lab/toolchain/R33_NATIVE_SHA256_V2.zag ~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag "$HERE/build/"
cd "$HERE/build"
for a in self imposed flat; do
  "$ZNC" "arm_$a.zag" -o "arm_$a" 2>&1 | grep -v "zagd unavailable" || true
done
ls -la arm_self arm_imposed arm_flat
