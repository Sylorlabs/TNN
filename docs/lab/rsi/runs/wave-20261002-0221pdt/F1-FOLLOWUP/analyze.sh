#!/bin/sh
# Sealed analysis driver (F1-FOLLOWUP, wave-20261002-0221pdt).
# Scores every hidden pred with the pure-Zag scorer, builds the analyzer
# manifest, and runs f1f_analyze (pure Zag). Writes analysis/RESULTS.txt.
# Pure shell + frozen binaries. No Python.
set -u
LDIR="$(cd "$(dirname "$0")" && pwd)"
SCORE="$LDIR/dev/f1_score"
AN="$LDIR/dev/f1f_analyze"
S="$LDIR/sealed"
RUNS="$LDIR/runs/1"
A="$LDIR/analysis"
mkdir -p "$A"

: > "$A/manifest.txt"
i=0
while [ $i -lt 40 ]; do
    acc="$("$SCORE" acc "$RUNS/s3_${i}_hidden.pred" "$S/s3_truth_$i.ep")"
    set -- $acc
    # acc format: ACC <num> <den> <pct>
    echo "$i $2 $3 $RUNS/s3_${i}_train.trace" >> "$A/manifest.txt"
    i=$((i + 1))
done
"$AN" "$A/manifest.txt" > "$A/RESULTS.txt" 2> "$A/analyze.stderr"
echo "rc=$?" > "$A/analyze.rc"
cat "$A/RESULTS.txt"
