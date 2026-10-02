#!/bin/bash
# Resume K1 battery from m2 onward (m1-prose and m1-code a/b already done).
# Usage: resume_battery.sh <outdir>
set -u
OUT="${1:?usage: resume_battery.sh <outdir>}"
CORPUS=~/workspace/tnn-lab/units/arms/harness/corpora/r1
BIN=./cl/k1test
LOG=work/runs/u7_battery_console.log
mkdir -p "$OUT"

run2() { # name, arg...
  local name="$1"; shift
  echo "=== $name ===" | tee -a "$LOG"
  "$BIN" "$@" > "$OUT/${name}_a.txt" 2>&1; echo "rc=$?" >> "$OUT/${name}_a.txt"
  "$BIN" "$@" > "$OUT/${name}_b.txt" 2>&1; echo "rc=$?" >> "$OUT/${name}_b.txt"
  if cmp -s "$OUT/${name}_a.txt" "$OUT/${name}_b.txt"; then
    echo "  PASS: byte-identical" | tee -a "$LOG"
  else
    echo "  FAIL: outputs differ" | tee -a "$LOG"
  fi
}

run2 m2-1x-prose m2-1x-prose "$CORPUS"
run2 m2-1x-code m2-1x-code "$CORPUS"
run2 m2-t2-prose m2-t2-prose "$CORPUS"
run2 m2-t2-code m2-t2-code "$CORPUS"
run2 m2-t3-prose m2-t3-prose "$CORPUS"
run2 m2-t3-code m2-t3-code "$CORPUS"
run2 m3-1x m3-1x "$CORPUS"
run2 m4-1x-bound m4-1x-bound "$CORPUS"
run2 m4-1x-content m4-1x-content "$CORPUS"
run2 m5-baseline m5-baseline
run2 m5-pressure m5-pressure
run2 m6-p2c-1x m6-p2c-1x "$CORPUS"
run2 m6-c2p-1x m6-c2p-1x "$CORPUS"
run2 m7-1x m7-1x "$CORPUS"
echo "=== m8-1x ===" | tee -a "$LOG"
mkdir -p "$OUT/m8_work"
"$BIN" m8-1x "$CORPUS" "$OUT/m8_work" none > "$OUT/m8-1x_a.txt" 2>&1; echo "rc=$?" >> "$OUT/m8-1x_a.txt"
"$BIN" m8-1x "$CORPUS" "$OUT/m8_work" none > "$OUT/m8-1x_b.txt" 2>&1; echo "rc=$?" >> "$OUT/m8-1x_b.txt"
if cmp -s "$OUT/m8-1x_a.txt" "$OUT/m8-1x_b.txt"; then echo "  PASS: byte-identical" | tee -a "$LOG"; else echo "  FAIL: outputs differ" | tee -a "$LOG"; fi
run2 k1-dedup-1x k1-dedup-1x "$CORPUS"
run2 k1-chain-1x k1-chain-1x "$CORPUS"
run2 k1-role-1x k1-role-1x "$CORPUS"
run2 k1-selftest k1-selftest
echo "RESUME BATTERY DONE" | tee -a "$LOG"
