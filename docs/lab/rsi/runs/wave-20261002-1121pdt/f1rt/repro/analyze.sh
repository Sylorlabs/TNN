#!/bin/sh
# analyze.sh - score sealed hidden preds and run the frozen analyzer.
# Pure shell + the pinned-znc-compiled f1_score and f1s_analyze.
# No Python.
set -u
LDIR="$(cd "$(dirname "$0")" && pwd)"
SCORE="$LDIR/dev/f1_score"
AN="$LDIR/dev/f1s_analyze"
S="$LDIR/sealed5"
RUNS="$LDIR/runs"
ANL="$LDIR/analysis"
mkdir -p "$ANL"

: > "$ANL/manifest.txt"
i=0
while [ $i -lt 40 ]; do
    acc=$("$SCORE" acc "$RUNS/1/s5_${i}_hidden.pred" "$S/s5_truth_$i.ep")
    set -- $acc
    echo "$i $2 $3 $RUNS/1/s5_${i}_train.trace" >> "$ANL/manifest.txt"
    i=$((i + 1))
done
"$AN" "$ANL/manifest.txt" > "$ANL/RESULTS.txt" 2>&1
cat "$ANL/RESULTS.txt" | tail -6
echo "wrote $ANL/RESULTS.txt $ANL/manifest.txt"
