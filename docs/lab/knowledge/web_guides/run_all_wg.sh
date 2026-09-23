#!/bin/bash
# WG-1 full battery: 2 arms x 3 batteries x 3 reps = 18 runs. Deterministic; no randomness.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
RUNDIR="$HERE/results_wg1"
mkdir -p "$RUNDIR"
for arm in guided blind; do
  for bat in tasks_familiar.txt tasks_novel.txt tasks_adv.txt; do
    for rep in 1 2 3; do
      echo "=== $arm $bat rep $rep ==="
      python3 "$HERE/run_wg.py" "$arm" "$HERE/batteries/$bat" "$RUNDIR" "$rep"
    done
  done
done
echo "=== scoring ==="
python3 "$HERE/score_wg.py" "$RUNDIR"
