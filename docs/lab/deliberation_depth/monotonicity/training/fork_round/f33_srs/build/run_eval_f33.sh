#!/bin/bash
# F33 eval wrapper: wipe deterministic per-item state, then the frozen 37-leg matrix.
set -u
FR=~/workspace/tnn-lab/deliberation_depth/monotonicity/training/fork_round/f33_srs
TR=~/workspace/tnn-lab/deliberation_depth/monotonicity/training
OUT=$TR/results_f33full
mkdir -p "$OUT"
rm -f "$OUT"/.f33state_A.tsv "$OUT"/.f33state_B.tsv
echo "state wiped: $(ls "$OUT"/.f33state_*.tsv 2>/dev/null | wc -l) state files remain"
"$TR/run_eval.sh" f33full "$FR/build/policy_bin" 33 0
