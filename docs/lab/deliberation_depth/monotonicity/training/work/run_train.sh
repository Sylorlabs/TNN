#!/bin/bash
# H-0 training: 10x and 100x, each run twice (A/B), byte-compare params.
set -u
T=~/workspace/tnn-lab/deliberation_depth/monotonicity/training
SRC=$T/src
W=$T/work
run_train() { # passes tag
  local passes=$1 tag=$2
  "$SRC/train_bin_a" "$W/features.tsv" "$passes" "$W/mt_params_${tag}_a.zag" "$W/log_${tag}_a.tsv"
  local rca=$?
  "$SRC/train_bin_b" "$W/features.tsv" "$passes" "$W/mt_params_${tag}_b.zag" "$W/log_${tag}_b.tsv"
  local rcb=$?
  echo "train $tag: rc a=$rca b=$rcb"
  if [ $rca -ne 0 ] || [ $rcb -ne 0 ]; then echo "TRAIN-FAIL $tag"; return 1; fi
  if cmp -s "$W/mt_params_${tag}_a.zag" "$W/mt_params_${tag}_b.zag"; then
    echo "PARAMS-BYTE-IDENTICAL $tag"
  else
    echo "PARAMS-MISMATCH $tag"; return 1
  fi
  if cmp -s "$W/log_${tag}_a.tsv" "$W/log_${tag}_b.tsv"; then
    echo "LOG-BYTE-IDENTICAL $tag"
  else
    echo "LOG-MISMATCH $tag (nonfatal)"; return 1
  fi
  cp "$W/mt_params_${tag}_a.zag" "$W/mt_params_${tag}.zag"
  cp "$W/log_${tag}_a.tsv" "$W/log_${tag}.tsv"
  return 0
}
run_train 10 10x
run_train 100 100x
echo "TRAIN-DONE"
