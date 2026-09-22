#!/bin/sh
# v2 sub-battery runs: 7 sub-batteries x 3 reps, byte-identical within
# sub-battery. Run from the v2 workdir root. Logs -> runs/sub_<s>_rep<N>.log
#
# The learner reads inputs/train_<s>.txt etc. relative to CWD, so each
# sub-battery runs in its own scratch dir (subruns/<s>/). Conversion is
# input plumbing only (NOT part of the frozen mechanism, PREREG2).
set -e
cd "$(dirname "$0")/.."
BIN=src/prose_learn2
for s in para contr hedge neg multi core distr; do
  mkdir -p subruns/$s/inputs
  python3 runs/convert_jsonl2.py inputs2/sub_${s}_train.jsonl \
    inputs2/sub_${s}_test.jsonl subruns/$s/inputs $s
  for rep in 1 2 3; do
    (cd subruns/$s && ../../$BIN $s > ../../runs/sub_${s}_rep${rep}.log 2>&1)
  done
  for rep in 2 3; do
    cmp -s runs/sub_${s}_rep1.log runs/sub_${s}_rep${rep}.log || {
      echo "NONDET $s rep$rep"; exit 1; }
  done
  echo "DET-OK $s 3/3 :: $(grep '^SUMMARY' runs/sub_${s}_rep1.log)"
done
echo "ALL SUB-BATTERY RUNS DONE"
