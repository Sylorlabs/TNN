#!/bin/sh
# ATTACK_BUILD.sh -- F3 REVISE step-6 alternative-explanation attack builds/runs.
# Prereg: revise_attack/PREREG_REVISE_ATTACK.md (frozen first, alone).
# Pure Zag + shell + znc only. No Python.
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
S=docs/lab/research-lead/overnight-20260928
D=$S/revise_attack
set -e
cd ~/workspace/tnn-rsi

build_run() {
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

case "$1" in
  setup)
    echo "=== setup validation: frozen learner + sealed S-NEG2 ==="
    build_run "valid_n" "$D/w_sneg2_ref.zag" "$D/f3_revise_frozen.zag"
    ;;
  srk)
    echo "=== Attack 1: B-REPLAY + S-RK ==="
    build_run "srk_replay" "$D/world_srk.zag" "$D/b_replay_frozen.zag"
    echo "=== Attack 1: REVISE + S-RK ==="
    build_run "srk_revise" "$D/world_srk.zag" "$D/f3_revise_frozen.zag"
    ;;
  nodrill)
    echo "=== Attack 2: drill-excised learner + sealed worlds ==="
    build_run "nodrill_c" "$D/w_sconj2_ref.zag" "$D/f3_revise_nodrill.zag"
    build_run "nodrill_n" "$D/w_sneg2_ref.zag" "$D/f3_revise_nodrill.zag"
    ;;
  *)
    echo "usage: $0 {setup|srk|nodrill}"; exit 1 ;;
esac

echo "=== md5 ==="
md5sum "$D"/raw_"$1"*_r*.txt 2>/dev/null | head -20
echo "=== stderr sizes (must all be 0) ==="
wc -c "$D"/raw_"$1"*_r*.err 2>/dev/null | head -20
