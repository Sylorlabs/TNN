#!/usr/bin/env bash
# Frozen analysis driver for the INT-1 S10 battery-repair re-run.
# Repair 2026-09-20 (battery-repair amendment §11): this driver is FROZEN and
# committed. It builds the binary, runs the paired S10 stages, the controls,
# and the bite checks, collects the instruments, and verifies determinism.
# Usage: ./analyze_s10.sh <output_dir>
# The binary is built deterministically; its SHA-256 is recorded.
set -u
OUT="${1:-/tmp/s10_repair}"
BIN="$OUT/int1_repair"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
SRC="$HOME/workspace/tnn-lab/wave9/integration/impl"

mkdir -p "$OUT"
echo "=== build ==="
sha256sum "$ZNC" > "$OUT/compiler.sha256"
"$ZNC" "$SRC/main.zag" -o "$BIN" 2> "$OUT/build.stderr"
echo "build_exit:$?" > "$OUT/build.exit"
sha256sum "$BIN" > "$OUT/binary.sha256"
ls -l "$BIN" | awk '{print $5}' > "$OUT/binary.bytes"
# source hashes (all .zag files)
(cd "$SRC" && sha256sum *.zag substrate/*.zag) > "$OUT/sources.sha256"

echo "=== paired stages s0..s5 ==="
for s in 0 1 2 3 4 5; do
  for rep in a b; do
    "$BIN" "s$s" > "$OUT/s${s}_${rep}.log" 2>&1
    echo "s${s}_${rep}:$?" >> "$OUT/stage.exits"
  done
  # byte-identical paired reruns (determinism)
  if cmp -s "$OUT/s${s}_a.log" "$OUT/s${s}_b.log"; then
    echo "s$s:IDENTICAL" >> "$OUT/determinism.txt"
  else
    echo "s$s:DIFFER" >> "$OUT/determinism.txt"
  fi
done

echo "=== controls ==="
"$BIN" controls > "$OUT/controls.log" 2>&1
echo "controls:$?" >> "$OUT/stage.exits"

echo "=== bites ==="
"$BIN" pbite > "$OUT/pbite.log" 2>&1
echo "pbite:$?" >> "$OUT/stage.exits"
"$BIN" cbite > "$OUT/cbite.log" 2>&1
echo "cbite:$?" >> "$OUT/stage.exits"

echo "=== instrument summary ==="
{
  echo "--- stage gates ---"
  grep -h "CHECK,stage_gate" "$OUT"/s*_a.log
  echo "--- P2 drop ceiling ---"
  grep -h "DROPS" "$OUT"/s*_a.log
  grep -h "CHECK,p2_drop_ceiling" "$OUT"/s*_a.log
  echo "--- P1 retention ---"
  grep -h "P1RET" "$OUT"/s*_a.log
  echo "--- Q2 pin fraction ---"
  grep -h "PINFRAC" "$OUT"/s*_a.log
  echo "--- L1 coverage ---"
  grep -h "L1COVER" "$OUT"/s*_a.log
  echo "--- C7 telemetry ---"
  grep -h "C7_TELEMETRY\|C7_POSCTRL" "$OUT"/controls.log
  echo "--- control verdicts ---"
  grep -h "CHECK,c[1-7]" "$OUT"/controls.log
  echo "--- bites ---"
  grep -h "CHECK,bite" "$OUT"/pbite.log
  grep -h "CHECK,cbite" "$OUT"/cbite.log
} > "$OUT/instruments.txt"

echo "=== done ==="
cat "$OUT/determinism.txt"
echo "---"
grep -c "CHECK.*0,0" "$OUT"/s*_a.log | head -1
