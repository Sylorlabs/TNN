#!/bin/sh
# REDTEAM_BUILD.sh -- F3 REVISE step-10 independent red-team builds/runs.
# Prereg: revise_redteam/PREREG_REVISE_REDTEAM.md (frozen alone first).
# Pure Zag + shell + znc only. No Python.
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
S=docs/lab/research-lead/overnight-20260928
D=$S/revise_redteam
FROZEN=$S/revise_attack/f3_revise_frozen.zag
FROZEN_SHA=354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392
set -e
cd ~/workspace/tnn-rsi

echo "=== frozen learner sha256 ==="
H=$(sha256sum "$FROZEN" | cut -d' ' -f1)
echo "$H"
if [ "$H" != "$FROZEN_SHA" ]; then
  echo "FROZEN LEARNER HASH MISMATCH"; exit 1
fi
cp "$FROZEN" "$D/f3_revise_frozen.zag"

build_run() {
  name="$1"; world="$2"
  cat "$D/f3_revise_frozen.zag" "$D/$world" > "$D/run_$name.zag"
  "$ZNC" "$D/run_$name.zag" -o "$D/bin_$name" 2> "$D/build_$name.err" || (cat "$D/build_$name.err"; exit 1)
  i=1
  while [ $i -le 3 ]; do
    "$D/bin_$name" > "$D/raw_${name}_r$i.txt" 2> "$D/raw_${name}_r$i.err"
    i=$((i+1))
  done
  echo "$name built and run 3x"
}

case "$1" in
  ctrl)  echo "=== W-CTRL: harness validity control ==="; build_run "ctrl" "world_rt_ctrl.zag" ;;
  conf1) echo "=== W-CONF1: one confounder ==="; build_run "conf1" "world_rt_conf1.zag" ;;
  conf2) echo "=== W-CONF2: two confounders ==="; build_run "conf2" "world_rt_conf2.zag" ;;
  inh2)  echo "=== W-2INH: two true inhibitors ==="; build_run "inh2" "world_rt_2inh.zag" ;;
  all)   "$0" ctrl; "$0" conf1; "$0" conf2; "$0" inh2 ;;
  *)     echo "usage: $0 {ctrl|conf1|conf2|inh2|all}"; exit 1 ;;
esac

echo "=== md5 of raw outputs ==="
md5sum "$D"/raw_"$1"*_r*.txt 2>/dev/null
echo "=== stderr sizes (must all be 0) ==="
wc -c "$D"/raw_"$1"*_r*.err 2>/dev/null
