#!/bin/sh
# digests_k10.sh -- 3/3 byte-identical verification for L3-INR-K10.
# Usage: digests_k10.sh <runsdir>
# Per sequence, sha256(summary_*.txt + trace.log + proto.log) across runs 1/2/3.
set -e
export PATH="$HOME/safebin"
RUNS="$1"
OUT="$RUNS/digests.txt"
: > "$OUT"
pass=1
# seq_pc: single arm T5a per run dir
for i in 1 2 3; do
  eval h$i='$(cat "$RUNS/seq_pc_$i/summary_T5a.txt" "$RUNS/seq_pc_$i/trace.log" "$RUNS/seq_pc_$i/proto.log" | sha256sum | cut -d" " -f1)'
done
if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then st="IDENTICAL"; else st="DIFFER"; pass=0; fi
echo "seq_pc_T5a $st $h1" >> "$OUT"
# seq_pd / seq_pe: T1+T4 share trace/proto per run dir; digest per arm summary + shared logs
for seq in seq_pd seq_pe; do
  for arm in T1 T4; do
    for i in 1 2 3; do
      eval h$i='$(cat "$RUNS/'$seq'_$i/summary_'$arm'.txt" "$RUNS/'$seq'_$i/trace.log" "$RUNS/'$seq'_$i/proto.log" | sha256sum | cut -d" " -f1)'
    done
    if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then st="IDENTICAL"; else st="DIFFER"; pass=0; fi
    echo "${seq}_${arm} $st $h1" >> "$OUT"
  done
done
cat "$OUT"
if [ $pass -eq 1 ]; then echo "3/3 BYTE-IDENTICAL: ALL SEQUENCES"; else echo "MISMATCH FOUND"; exit 1; fi
