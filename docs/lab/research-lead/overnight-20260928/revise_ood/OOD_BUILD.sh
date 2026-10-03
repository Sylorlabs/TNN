#!/bin/sh
# OOD_BUILD.sh -- F3 REVISE step-7 OOD test builds/runs.
# Prereg: revise_ood/PREREG_REVISE_OOD.md (frozen first, alone, 7bf467d35).
# Pure Zag + shell + znc only. No Python.
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
S=docs/lab/research-lead/overnight-20260928
D=$S/revise_ood
A=$S/revise_attack
set -e
cd ~/workspace/tnn-rsi

FROZEN_SHA=354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392

# Verify the frozen learner hash before any build.
echo "$FROZEN_SHA  $A/f3_revise_frozen.zag" | sha256sum -c - || exit 1

build_run() {
  name="$1"; world="$2"
  cat "$A/f3_revise_frozen.zag" "$world" > "$D/run_$name.zag"
  "$ZNC" "$D/run_$name.zag" -o "$D/bin_$name" 2> "$D/build_$name.err" || (cat "$D/build_$name.err"; exit 1)
  i=1
  while [ $i -le 3 ]; do
    "$D/bin_$name" > "$D/raw_${name}_r$i.txt" 2> "$D/raw_${name}_r$i.err"
    i=$((i+1))
  done
  echo "$name built and run 3x"
}

FROZEN_SHA=354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392

case "$1" in
  d3)
    echo "=== OOD-D3: delay shift within currency ==="
    build_run "ood_d3" "$D/world_ood_d3.zag"
    ;;
  d6)
    echo "=== OOD-D6: delay beyond currency ==="
    build_run "ood_d6" "$D/world_ood_d6.zag"
    ;;
  all)
    "$0" d3
    "$0" d6
    ;;
  *)
    echo "usage: $0 {d3|d6|all}"; exit 1 ;;
esac
