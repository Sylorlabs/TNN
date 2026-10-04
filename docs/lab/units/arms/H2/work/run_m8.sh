#!/bin/bash
# H2 M8 five-regime adversarial-heap gate. Sequential (load constraint).
set -u
H2=~/workspace/tnn-lab/units/arms/H2
CORP=~/workspace/tnn-lab/corpora/r1
EV=$H2/evidence/r1
BIN=$H2/work/h2
mkdir -p "$EV"
for pert in clean frag aslr starve freelist-rev; do
  mode="m8-$pert"
  out="$EV/$mode"
  mkdir -p "$out"
  echo "[$(date -u +%H:%M:%S)] START $mode" | tee -a "$EV/m8.log"
  ( cd "$H2" && "$BIN" m8-1x "$CORP" "$out" "$pert" > "$out/stdout.txt" 2> "$out/stderr.txt" )
  ec=$?
  echo "$ec" > "$out/exitcode"
  echo "[$(date -u +%H:%M:%S)] END $mode exit=$ec" | tee -a "$EV/m8.log"
done
# Mechanical comparison: stdout + every artifact byte-identical to clean.
ref="$EV/m8-clean"
fail=0
for pert in frag aslr starve freelist-rev; do
  out="$EV/m8-$pert"
  for f in stdout.txt store_hashes.txt store_chain.txt ledger.bin ledger_chain.txt alloc_trace.txt; do
    if ! cmp -s "$ref/$f" "$out/$f"; then echo "M8-DIFF: $pert/$f differs"; fail=1; fi
  done
done
if [ $fail -eq 0 ]; then echo "M8-GATE: PASS (all 5 regimes byte-identical)"; else echo "M8-GATE: FAIL"; fi | tee -a "$EV/m8.log"
