#!/bin/bash
# r10 build helper: @import("../../toolchain/...") resolves relative to the
# SOURCE FILE's directory, so stage the .zag in img/ for the build.
# Usage: build_r10.sh <srcname> <outbin>
#   srcname: file in r10/src (no .zag suffix)
set -e
IMG=~/workspace/tnn-lab/imagination_discovery/img
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cp "$IMG/r10/src/$1.zag" "$IMG/__r10build_$1.zag"
( cd "$IMG" && "$ZNC" "__r10build_$1.zag" --no-zagd --no-analyze -o "$2" )
rm -f "$IMG/__r10build_$1.zag"
echo "built $2"
