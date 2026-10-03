#!/bin/sh
# REVISE_BUILD.sh -- build the REVISE learner against the sealed worlds.
# Pure Zag + shell only. No Python.
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
D=docs/lab/research-lead/overnight-20260928/f3_revise_impl
S=docs/lab/research-lead/overnight-20260928
set -e

build_one() {
  name="$1"; world="$2"; learner="$3"
  cat "$learner" "$world" > "$D/run_$name.zag"
  "$ZNC" "$D/run_$name.zag" -o "$D/bin_$name" 2> "$D/build_$name.err" || (cat "$D/build_$name.err"; exit 1)
  i=1
  while [ $i -le 3 ]; do
    "$D/bin_$name" > "$D/raw_${name}_r$i.txt" 2> "$D/raw_${name}_r$i.err"
    i=$((i+1))
  done
  echo "$name built and run 3x"
}

echo "=== T-CONJ (ADV1) ==="
build_one "revise_c" "$S/f2_ablation/world_adv1.zag" "$D/f3_revise.zag"
echo "=== T-NEG (sealed) ==="
build_one "revise_n" "$S/f3_phase3/world_tneg_a.zag" "$D/f3_revise.zag"
echo "=== T-NEG renamed (F-RNAME) ==="
build_one "revise_rn" "$S/f3_attack/world_tneg_renamed.zag" "$D/f3_revise.zag"

echo "=== md5 ==="
md5sum "$D"/raw_revise_c_r*.txt "$D"/raw_revise_n_r*.txt "$D"/raw_revise_rn_r*.txt
echo "=== verdicts ==="
grep "F3P3 RESULT" "$D"/raw_revise_c_r1.txt "$D"/raw_revise_n_r1.txt "$D"/raw_revise_rn_r1.txt
