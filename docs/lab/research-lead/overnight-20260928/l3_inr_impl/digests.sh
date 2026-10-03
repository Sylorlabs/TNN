#!/bin/sh
# digests.sh -- 3/3 byte-identical verification for L3-INR DEV battery.
# Usage: digests.sh <runsdir>
# For each arm, compares sha256(summary+trace.log+proto.log) across run 1/2/3.
set -e
export PATH="$HOME/safebin"
RUNS="$1"
OUT="$RUNS/digests.txt"
: > "$OUT"
pass=1
# seq arms: T1 T2 T3 C5 T4 T3b live in seq_i/summary_<ARM>.txt, shared trace/proto
for arm in T1 T2 T3 C5 T4 T3b; do
  h1=$(cat "$RUNS/seq_1/summary_${arm}.txt" "$RUNS/seq_1/trace.log" "$RUNS/seq_1/proto.log" | sha256sum | cut -d' ' -f1)
  h2=$(cat "$RUNS/seq_2/summary_${arm}.txt" "$RUNS/seq_2/trace.log" "$RUNS/seq_2/proto.log" | sha256sum | cut -d' ' -f1)
  h3=$(cat "$RUNS/seq_3/summary_${arm}.txt" "$RUNS/seq_3/trace.log" "$RUNS/seq_3/proto.log" | sha256sum | cut -d' ' -f1)
  # note: trace/proto are shared across arms in seq_i, so per-arm digests
  # include the full seq logs; identical inputs => identical logs.
  if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then st="IDENTICAL"; else st="DIFFER"; pass=0; fi
  echo "$arm $st $h1" >> "$OUT"
done
# single arms
for spec in "t5a T5a" "t5b T5b" "c0 C0" "c1 C1" "c2 C2" "c3t C3" "c4 C4"; do
  set -- $spec
  dir="$1"; arm="$2"
  h1=$(cat "$RUNS/${dir}_1/summary_${arm}.txt" "$RUNS/${dir}_1/trace.log" "$RUNS/${dir}_1/proto.log" | sha256sum | cut -d' ' -f1)
  h2=$(cat "$RUNS/${dir}_2/summary_${arm}.txt" "$RUNS/${dir}_2/trace.log" "$RUNS/${dir}_2/proto.log" | sha256sum | cut -d' ' -f1)
  h3=$(cat "$RUNS/${dir}_3/summary_${arm}.txt" "$RUNS/${dir}_3/trace.log" "$RUNS/${dir}_3/proto.log" | sha256sum | cut -d' ' -f1)
  if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then st="IDENTICAL"; else st="DIFFER"; pass=0; fi
  echo "$arm $st $h1" >> "$OUT"
done
cat "$OUT"
if [ $pass -eq 1 ]; then echo "3/3 BYTE-IDENTICAL: ALL ARMS"; else echo "MISMATCH FOUND"; exit 1; fi
