#!/bin/bash
# run_battery.sh — B-3034COMP: run every mode 3x, SHA-256 compare stdout.
# Usage: run_battery.sh <bindir> <outdir>
# The binary must already be built from the committed sources.
set -u
BIN="$1"
OUT="$2"
mkdir -p "$OUT"
MODES="honest rf_full rc_full xr_fresh xr_reuse n_goal o_temporal o_numeric p_remint j_dump j_agg j_tag k_blind l_distal ge_gap"
# 16 modes (xr counts as two)
FAIL=0
> "$OUT/SHA256SUMS"
for m in $MODES; do
  for r in 1 2 3; do
    "$BIN" "$m" > "$OUT/drive3034_${m}_run${r}.out" 2>"$OUT/drive3034_${m}_run${r}.err"
    if [ ! -s "$OUT/drive3034_${m}_run${r}.out" ]; then echo "EMPTY: $m run $r"; FAIL=1; fi
    if [ -s "$OUT/drive3034_${m}_run${r}.err" ]; then echo "STDERR: $m run $r:"; cat "$OUT/drive3034_${m}_run${r}.err"; fi
  done
  s1=$(sha256sum "$OUT/drive3034_${m}_run1.out" | cut -d' ' -f1)
  s2=$(sha256sum "$OUT/drive3034_${m}_run2.out" | cut -d' ' -f1)
  s3=$(sha256sum "$OUT/drive3034_${m}_run3.out" | cut -d' ' -f1)
  if [ "$s1" = "$s2" ] && [ "$s2" = "$s3" ]; then
    echo "IDENTICAL $m $s1"
  else
    echo "DIVERGENT $m $s1 $s2 $s3"; FAIL=1
  fi
  echo "$s1  drive3034_${m}_run1.out" >> "$OUT/SHA256SUMS"
done
if [ "$FAIL" = "0" ]; then echo "BATTERY_OK 16/16 modes byte-identical across 3 runs"; else echo "BATTERY_FAIL"; fi
exit "$FAIL"
