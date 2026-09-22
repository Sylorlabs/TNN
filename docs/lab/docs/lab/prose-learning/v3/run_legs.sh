#!/bin/sh
# v3 ablation run harness. Prereg: v3/PREREG3.md (FROZEN).
# Legs: A0=v2 on v2 inputs | A1=v2 on dense inputs | A2=learn3 m1 on dense | A3=learn3 m2 on dense
# Each leg: 4 championship sources x 5 reps + 7 sub-batteries x 3 reps.
# Determinism: rep2..5 cmp 0-diff vs rep1, hard fail otherwise.
# Usage: run_legs.sh <leg>   (leg in A0 A1 A2 A3)
set -e
LEG="$1"
case "$LEG" in
  A0) BIN=../v2/src/prose_learn2; INP=inputs3_v2single; MODE="" ;;
  A1) BIN=../v2/src/prose_learn2; INP=inputs3;       MODE="" ;;
  A2) BIN=src/prose_learn3;      INP=inputs3;       MODE="m1" ;;
  A3) BIN=src/prose_learn3;      INP=inputs3;       MODE="m2" ;;
  *) echo "usage: run_legs.sh A0|A1|A2|A3"; exit 1 ;;
esac
cd "$(dirname "$0")"
V3D="$(pwd)"
[ -x "$V3D/$BIN" ] || { echo "missing binary $BIN"; exit 1; }
WORK="$V3D/runs/$LEG"
mkdir -p "$WORK/scratch"
echo "== leg $LEG bin=$BIN inputs=$INP mode=$MODE =="
# championship: 4 sources x 5 reps
for s in grok sol step muse-native; do
  SD="$WORK/scratch/champ_$s"; mkdir -p "$SD/inputs"
  for f in train_${s}.txt test_${s}.txt false_ids_${s}.txt; do
    ln -sf "$V3D/$INP/$f" "$SD/inputs/$f"
  done
  for rep in 1 2 3 4 5; do
    (cd "$SD" && "$V3D/$BIN" "$s" $MODE > "$WORK/champ_${s}_rep${rep}.log" 2>&1)
  done
  for rep in 2 3 4 5; do
    cmp -s "$WORK/champ_${s}_rep1.log" "$WORK/champ_${s}_rep${rep}.log" || {
      echo "NONDET champ $s rep$rep"; exit 1; }
  done
  echo "DET-OK champ_$s 5/5 :: $(grep '^SUMMARY' "$WORK/champ_${s}_rep1.log")"
done
# sub-batteries: 7 x 3 reps. All legs use v3/inputs3 sub-battery txt files
# (converted verbatim from v2's frozen inputs2, except NEG which is the
# preregistered rebuild per PREREG3 section 5).
for s in para contr hedge neg multi core distr; do
  SD="$WORK/scratch/sub_$s"; mkdir -p "$SD/inputs"
  ln -sf "$V3D/inputs3/sub_${s}_train.txt" "$SD/inputs/train_${s}.txt"
  ln -sf "$V3D/inputs3/sub_${s}_test.txt"  "$SD/inputs/test_${s}.txt"
  : > "$SD/inputs/false_ids_${s}.txt"
  for rep in 1 2 3; do
    (cd "$SD" && "$V3D/$BIN" "$s" $MODE > "$WORK/sub_${s}_rep${rep}.log" 2>&1)
  done
  for rep in 2 3; do
    cmp -s "$WORK/sub_${s}_rep1.log" "$WORK/sub_${s}_rep${rep}.log" || {
      echo "NONDET sub $s rep$rep"; exit 1; }
  done
  echo "DET-OK sub_$s 3/3 :: $(grep '^SUMMARY' "$WORK/sub_${s}_rep1.log")"
done
echo "LEG $LEG DONE"
