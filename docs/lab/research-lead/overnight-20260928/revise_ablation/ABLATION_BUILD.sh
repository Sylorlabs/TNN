#!/bin/sh
# ABLATION_BUILD.sh -- F3 REVISE step-8 ablation builds/runs.
# Prereg: revise_ablation/PREREG_REVISE_ABLATION.md (frozen first, alone).
# Pure Zag + shell + znc only. No Python.
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
S=docs/lab/research-lead/overnight-20260928
D=$S/revise_ablation
A=$S/revise_attack
set -e
cd ~/workspace/tnn-rsi

FROZEN_SHA=354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392

case "$1" in
  derive)
    echo "=== verifying frozen learner sha256 ==="
    echo "$FROZEN_SHA  $A/f3_revise_frozen.zag" | sha256sum -c -
    echo "=== deriving A1 (no D1): line 1231 condition -> if(0==1) ==="
    sed '1231s/.*/      if(0==1){/' "$A/f3_revise_frozen.zag" > "$D/f3_revise_noD1.zag"
    echo "=== deriving A2 (no OP-GROW): line 994 condition -> if(0==1) ==="
    sed '994s/.*/        if(0==1){/' "$A/f3_revise_frozen.zag" > "$D/f3_revise_noGROW.zag"
    echo "=== diff check: exactly one changed line each ==="
    n1=$(diff "$A/f3_revise_frozen.zag" "$D/f3_revise_noD1.zag" | wc -l)
    n2=$(diff "$A/f3_revise_frozen.zag" "$D/f3_revise_noGROW.zag" | wc -l)
    echo "noD1 diff lines: $n1 (expect 3: 1231c1231, <, ---, > is 4 lines)"
    echo "noGROW diff lines: $n2"
    diff "$A/f3_revise_frozen.zag" "$D/f3_revise_noD1.zag" || true
    diff "$A/f3_revise_frozen.zag" "$D/f3_revise_noGROW.zag" || true
    if [ "$n1" -ne 4 ] || [ "$n2" -ne 4 ]; then
      echo "DERIVE-FAIL: expected exactly one changed line per learner"
      exit 1
    fi
    echo "derive complete"
    ;;
  run)
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
    echo "=== a1n: noD1 + S-NEG2 ==="
    build_run "a1n" "$A/w_sneg2_ref.zag" "$D/f3_revise_noD1.zag"
    echo "=== a1c: noD1 + S-CONJ2 (control) ==="
    build_run "a1c" "$A/w_sconj2_ref.zag" "$D/f3_revise_noD1.zag"
    echo "=== a2c: noGROW + S-CONJ2 ==="
    build_run "a2c" "$A/w_sconj2_ref.zag" "$D/f3_revise_noGROW.zag"
    echo "=== a2n: noGROW + S-NEG2 (control) ==="
    build_run "a2n" "$A/w_sneg2_ref.zag" "$D/f3_revise_noGROW.zag"
    echo "=== md5 of run outputs ==="
    md5sum "$D"/raw_a1n_r*.txt "$D"/raw_a1c_r*.txt "$D"/raw_a2c_r*.txt "$D"/raw_a2n_r*.txt
    echo "=== stderr sizes (must all be 0) ==="
    wc -c "$D"/raw_a1n_r*.err "$D"/raw_a1c_r*.err "$D"/raw_a2c_r*.err "$D"/raw_a2n_r*.err
    ;;
  *)
    echo "usage: $0 {derive|run}"; exit 1 ;;
esac
