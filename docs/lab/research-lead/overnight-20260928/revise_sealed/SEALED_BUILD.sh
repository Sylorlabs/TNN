#!/bin/sh
# SEALED_BUILD.sh -- build the FROZEN REVISE learner against the sealed worlds.
# Pure Zag + shell only. No Python.
# Prereg: revise_sealed/PREREG_REVISE_SEALED.md (8cdf0992a, frozen first).
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
S=docs/lab/research-lead/overnight-20260928
D=$S/revise_sealed
IMPL=$S/f3_revise_impl
set -e

# Frozen-learner integrity gate: abort if bytes differ from the
# builder's committed artifacts.
echo "$D: verifying frozen learner bytes..."
echo "354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392  $IMPL/f3_revise.zag" | sha256sum -c -
echo "4e3bdf0680f11778d9226ac127d20588b40a42295e85af2efaf3a1b77ea786b2  $IMPL/f3_revise_abl.zag" | sha256sum -c -

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

echo "=== S-CONJ2 (sealed) ==="
build_one "sealed_c" "$D/world_sconj2.zag" "$IMPL/f3_revise.zag"
echo "=== S-CONJ2 renamed (F-RNAME) ==="
build_one "sealed_cr" "$D/world_sconj2r.zag" "$IMPL/f3_revise.zag"
echo "=== S-NEG2 (sealed) ==="
build_one "sealed_n" "$D/world_sneg2.zag" "$IMPL/f3_revise.zag"
echo "=== S-NEG2 renamed (F-RNAME) ==="
build_one "sealed_nr" "$D/world_sneg2r.zag" "$IMPL/f3_revise.zag"
echo "=== S-CONJ2 ablation (F-RABLN) ==="
build_one "sealed_abl_c" "$D/world_sconj2.zag" "$IMPL/f3_revise_abl.zag"
echo "=== S-NEG2 ablation (F-RABLN) ==="
build_one "sealed_abl_n" "$D/world_sneg2.zag" "$IMPL/f3_revise_abl.zag"

echo "=== md5 ==="
md5sum "$D"/raw_sealed_c_r*.txt "$D"/raw_sealed_cr_r*.txt "$D"/raw_sealed_n_r*.txt "$D"/raw_sealed_nr_r*.txt "$D"/raw_sealed_abl_c_r*.txt "$D"/raw_sealed_abl_n_r*.txt
echo "=== stderr sizes (must all be 0) ==="
wc -c "$D"/raw_sealed_*_r*.err
echo "=== verdicts ==="
grep -H "F3P3 RESULT" "$D"/raw_sealed_c_r1.txt "$D"/raw_sealed_n_r1.txt "$D"/raw_sealed_abl_c_r1.txt "$D"/raw_sealed_abl_n_r1.txt
