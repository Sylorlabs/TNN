#!/bin/bash
# Wiring build: concatenate library + mains (avoids @import cwd ambiguity),
# compile with the pinned znc toolchain. Pure Zag, zero RNG.
set -e
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
W=~/workspace/audio_longhorizon/wiring
mkdir -p "$W/build"
cat "$W/src/organ_lib.zag" "$W/src/f0low.zag" "$W/src/emit_main.zag" > "$W/build/emit_full.zag"
cat "$W/src/organ_lib.zag" "$W/src/delib_main.zag" > "$W/build/delib_full.zag"
cat "$W/src/organ_lib.zag" "$W/src/render_act.zag" > "$W/build/render_full.zag"
cat "$W/src/organ_lib.zag" "$W/src/f0low.zag" "$W/src/session_main.zag" > "$W/build/session_full.zag"
cp ~/workspace/audio_principles/crew_p/organ.zag "$W/build/organ_frozen.zag"
"$ZNC" "$W/build/emit_full.zag" -o "$W/build/emit_desc" 2>&1 | grep -E "error|wrote native" || true
"$ZNC" "$W/build/delib_full.zag" -o "$W/build/deliberate" 2>&1 | grep -E "error|wrote native" || true
"$ZNC" "$W/build/render_full.zag" -o "$W/build/render_act" 2>&1 | grep -E "error|wrote native" || true
"$ZNC" "$W/build/session_full.zag" -o "$W/build/session_run" 2>&1 | grep -E "error|wrote native" || true
"$ZNC" "$W/build/organ_frozen.zag" -o "$W/build/organ_frozen" 2>&1 | grep -E "error|wrote native" || true
ls -la "$W/build/emit_desc" "$W/build/deliberate" "$W/build/render_act" "$W/build/session_run" "$W/build/organ_frozen"
sha256sum "$W/build/emit_desc" "$W/build/deliberate" "$W/build/render_act" "$W/build/session_run" "$W/build/organ_frozen"
