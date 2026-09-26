#!/bin/bash
# Red-team full matrix for arm B: 3 cur x 3 var x 3 scales x 2 runs = 54 runs.
# Each run's stdout saved; byte-identity of pairs checked at the end.
cd ~/workspace/strength-round4 || exit 1
OUT=redteam_B/matrix_logs
mkdir -p "$OUT"
for cur in VUP WBS JI; do
  for var in 0 1 2; do
    for scale in S1 S10 S100; do
      for r in 1 2; do
        f="$OUT/cell_B_${cur}_${var}_${scale}_r${r}.log"
        ./trial_bin_r4 B "$cur" "$var" "$scale" > "$f" 2>&1
        echo "done $f rc=$? invalid=$(grep -c 'ST_INVALID 1' "$f")"
      done
    done
  done
done
echo "MATRIX_DONE"
