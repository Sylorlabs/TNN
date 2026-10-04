#!/bin/sh
# BASELINE_BUILD.sh -- build simple baselines against sealed worlds.
# Pure Zag + shell only. No Python.
# Prereg: revise_baseline/PREREG_REVISE_BASELINE.md (4786633c5) +
# Amendment 1 (db585360a), both frozen before any implementation.
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
S=docs/lab/research-lead/overnight-20260928
D=$S/revise_baseline
W=$S/revise_sealed
set -e

echo "$D: verifying sealed world bytes..."
echo "64ba1097cb601a060c67e5857914d00ba8791623ea31ea20222e894b4327534c  $W/world_sconj2.zag" | sha256sum -c -
echo "545118a1fe9d30186930d16539c305bdf5197ee804c13f4c948ae4cecfb7735f  $W/world_sneg2.zag" | sha256sum -c -

build_one() {
  name="$1"; world="$2"; base="$3"
  cat "$D/$base" "$W/$world" > "$D/run_$name.zag"
  "$ZNC" "$D/run_$name.zag" -o "$D/bin_$name" 2> "$D/build_$name.err" || (cat "$D/build_$name.err"; exit 1)
  i=1
  while [ $i -le 3 ]; do
    "$D/bin_$name" > "$D/raw_${name}_r$i.txt" 2> "$D/raw_${name}_r$i.err"
    i=$((i+1))
  done
  echo "$name built and run 3x"
}

echo "=== B-REPLAY + S-CONJ2 ==="
build_one "replay_c" "world_sconj2.zag" "b_replay.zag"
echo "=== B-REPLAY + S-NEG2 ==="
build_one "replay_n" "world_sneg2.zag" "b_replay.zag"
echo "=== B-SINGLETON + S-CONJ2 ==="
build_one "single_c" "world_sconj2.zag" "b_singleton.zag"
echo "=== B-SINGLETON + S-NEG2 ==="
build_one "single_n" "world_sneg2.zag" "b_singleton.zag"

echo "=== md5 ==="
md5sum "$D"/raw_replay_c_r*.txt "$D"/raw_replay_n_r*.txt "$D"/raw_single_c_r*.txt "$D"/raw_single_n_r*.txt
echo "=== stderr sizes (must all be 0) ==="
wc -c "$D"/raw_replay_*_r*.err "$D"/raw_single_*_r*.err
echo "=== GOAL_REAL lines ==="
grep -H "GOAL_REAL" "$D"/raw_replay_c_r1.txt "$D"/raw_replay_n_r1.txt "$D"/raw_single_c_r1.txt "$D"/raw_single_n_r1.txt
