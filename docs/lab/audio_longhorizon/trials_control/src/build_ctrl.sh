#!/bin/bash
# build_ctrl.sh — reproduce build/ctrl_full.zag + build/ctrl deterministically.
# Assembly (frozen):
#   1. ~/workspace/audio_principles/crew_p/organ.zag, with `fn main()` renamed to
#      `fn organ_standalone_main_unused()` (single main rule)
#   2. ~/workspace/audio_longhorizon/wiring/src/f0low.zag (byte-identical)
#   3. src/ctrl_main.zag (byte-identical)
# Compile with the pinned toolchain; run from this directory.
set -e
cd "$(dirname "$0")/.."
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
ORG=~/workspace/audio_principles/crew_p/organ.zag
F0L=~/workspace/audio_longhorizon/wiring/src/f0low.zag
sed 's/^fn main() i32 {/fn organ_standalone_main_unused() i32 {/' "$ORG" > build/_org.tmp
cat build/_org.tmp "$F0L" src/ctrl_main.zag > build/ctrl_full.zag
rm build/_org.tmp
rm -rf build/.zag-cache
"$ZNC" build build/ctrl_full.zag -o build/ctrl
sha256sum build/ctrl_full.zag build/ctrl
