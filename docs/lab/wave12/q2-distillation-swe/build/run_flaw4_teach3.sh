#!/usr/bin/env bash
# Q2-SWE flaw4 + teach3 legs: N=5 runs each, byte-identical.
# Run AFTER the corpus is frozen and committed.
set -euo pipefail
D=~/workspace/tnn-lab/wave12/q2-distillation-swe
cd "$D/build"
for i in 1 2 3 4 5; do
  ./swe_bin flaw4 > "$D/evidence/logs/flaw4_run${i}.log" 2>&1
  ./swe_bin teach3 > "$D/evidence/logs/teach3_run${i}.log" 2>&1
done
# byte-identity across all 5 runs
for mode in flaw4 teach3; do
  ref=$(sha256sum "$D/evidence/logs/${mode}_run1.log" | cut -d' ' -f1)
  for i in 2 3 4 5; do
    h=$(sha256sum "$D/evidence/logs/${mode}_run${i}.log" | cut -d' ' -f1)
    if [ "$h" != "$ref" ]; then echo "MISMATCH $mode run $i"; exit 1; fi
  done
  echo "$mode: 5/5 byte-identical ($ref)"
done
