#!/bin/bash
# run_battery.sh — run the F2 deliberative battery. Args: <outdir> [opcap]
# One process per fixture (deterministic; no shared state).
set -u
OUTDIR="$1"
CAP="${2:-100000}"
BIN=~/workspace/conscious_perception/forks/deliberative/src/f2_bin
FX=~/workspace/conscious_perception/fixtures
mkdir -p "$OUTDIR"
run_one() {
  local f="$1"
  local n
  n=$(basename "$f")
  "$BIN" "$f" "$OUTDIR/$n" "$CAP"
}
for f in "$FX"/test/omission/*.pcm "$FX"/test/ambiguity/am_p1.pcm "$FX"/test/ambiguity/am_c1.img \
         "$FX"/test/redteam/rt_p1.pcm "$FX"/test/redteam/rt_c1.img \
         "$FX"/test/illusion/il_c1.img "$FX"/test/illusion/il_c2.img \
         "$FX"/test/inattentional/ib_m1.vid "$FX"/test/inattentional/ib_m2.vid \
         "$FX"/train/omission/tr_om_p1.pcm "$FX"/train/omission/tr_om_p2.pcm \
         "$FX"/train/omission/tr_om_p3.pcm "$FX"/train/omission/tr_om_t1.pcm \
         "$FX"/train/ambiguity/tr_am_p1.pcm "$FX"/train/ambiguity/tr_am_c1.img \
         "$FX"/train/redteam/tr_rt_p1.pcm "$FX"/train/redteam/tr_rt_c1.img \
         "$FX"/train/inattentional/tr_ib_m1.vid "$FX"/train/inattentional/tr_ib_m2.vid \
         "$FX"/train/illusion/tr_il_c1.img "$FX"/train/illusion/tr_il_c2.img; do
  [ -e "$f" ] || continue
  run_one "$f"
done
echo "battery done -> $OUTDIR (opcap=$CAP)"
