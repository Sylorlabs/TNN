#!/bin/bash
# Crew L build: concatenate core + main (avoids @import path ambiguity), compile with pinned znc.
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
HERE=~/workspace/audio_principles/crew_l
mkdir -p "$HERE/build"
for m in organ render loop hf; do
  cat "$HERE/src/core.zag" "$HERE/src/main_${m}.zag" > "$HERE/build/${m}_full.zag"
  "$ZNC" "$HERE/build/${m}_full.zag" -o "$HERE/build/${m}" 2>&1 | grep -v "^znc: warning: zagd" || true
done
ls -la "$HERE/build"/organ "$HERE/build"/render "$HERE/build"/loop "$HERE/build"/hf
