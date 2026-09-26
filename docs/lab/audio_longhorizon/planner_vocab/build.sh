#!/bin/bash
# Planner/vocabulary build: one binary holding frozen hearing + deliberation +
# vocabulary growth + correction + rendering. Pure Zag, zero RNG.
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
P=~/workspace/audio_longhorizon/planner_vocab
mkdir -p "$P/build"
# frozen organ with its standalone main renamed away (single main in plan_main)
sed 's/^fn main() i32 {/fn organ_standalone_main_unused() i32 {/' \
  ~/workspace/audio_principles/crew_p/organ.zag > "$P/build/organ_lib.zag"
cat "$P/build/organ_lib.zag" \
    ~/workspace/audio_longhorizon/wiring/src/f0low.zag \
    "$P/src/plan_main.zag" > "$P/build/plan_full.zag"
"$ZNC" "$P/build/plan_full.zag" -o "$P/build/plan" 2>&1 | grep -E "error|wrote native" || true
ls -la "$P/build/plan"
sha256sum "$P/build/plan"
