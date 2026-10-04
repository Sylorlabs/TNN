#!/bin/bash
# build.sh — build the three traced intake drivers with the pinned toolchain.
# Run from this directory (@import paths resolve relative to cwd).
set -e
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
if [ ! -x "$ZNC" ]; then echo "pinned toolchain not found: $ZNC"; exit 1; fi
"$ZNC" audio_intake_trace.zag -o audio_intake_trace
"$ZNC" image_intake_trace.zag -o image_intake_trace
"$ZNC" video_intake_trace.zag -o video_intake_trace
echo "built: audio_intake_trace image_intake_trace video_intake_trace"
