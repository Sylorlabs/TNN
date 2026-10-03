#!/bin/bash
# R2-15 battery: 2 passes x 2 modes x 5 family batch files.
set -u
BIN=work/fsc
FIX=../../fixtures/fsc
EV=evidence
for pass in 1 2; do
  for mode in 0 1; do
    for f in "$FIX"/fsc_*.fsc; do
      base=$(basename "$f" .fsc)
      "$BIN" "$mode" "$f" "$EV/report_m${mode}_${base}_p${pass}.txt" "$EV/ledger_m${mode}_${base}_p${pass}.txt" || echo "RUN FAILED: $mode $base p$pass"
    done
  done
done
echo done
