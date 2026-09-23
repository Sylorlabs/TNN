#!/usr/bin/env bash
# Frozen analysis driver for the INT-1 S10 battery-repair re-run.
# Repair 2026-09-20 (battery-repair amendment §11): this driver is FROZEN and
# committed. It builds the binary, runs the paired S10 stages, the controls,
# and the bite checks, collects the instruments, and verifies determinism.
# C5 redesign 2026-09-20 (amendment §7): G0b build-gate added — exactly one
# o4_compose call site in the source tree, inside seam4_compose; the build
# FAILS otherwise. Nothing else about the driver's behavior changes.
# Usage: ./analyze_s10.sh <output_dir>
# The binary is built deterministically; its SHA-256 is recorded.
set -u
OUT="${1:-/tmp/s10_repair}"
BIN="$OUT/int1_repair"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
SRC="$HOME/workspace/tnn-lab/wave9/integration/impl"

mkdir -p "$OUT"
echo "=== G0b: single o4_compose call site (C5-redesign amendment §7) ==="
# Comment-stripped static scan over the whole source tree (incl. substrate).
# Exactly one o4_compose( occurrence that is not the fn definition, and it
# must lie inside the fn seam4_compose body in seam.zag. Otherwise FAIL BUILD.
G0B_HITS="$(for f in "$SRC"/*.zag "$SRC"/substrate/*.zag "$SRC"/substrate/cl/*.zag; do
  [ -f "$f" ] || continue
  sed 's|//.*$||' "$f" | grep -n 'o4_compose(' | grep -v 'fn o4_compose(' | sed "s|^|$f:|"
done)"
G0B_N="$(printf '%s\n' "$G0B_HITS" | grep -c .)"
G0B_INFN="$(sed 's|//.*$||' "$SRC/seam.zag" | awk '
  /^fn seam4_compose\(/ {infn=1; next}
  infn && /^fn / {infn=0}
  infn && /o4_compose\(/ && !/fn o4_compose\(/ {c++}
  END {print c+0}')"
printf '%s\n' "$G0B_HITS" > "$OUT/g0b_hits.txt"
if [ "$G0B_N" -eq 1 ] && [ "$G0B_INFN" -eq 1 ]; then
  echo "G0b:PASS (exactly 1 o4_compose call site, inside seam4_compose)"
else
  echo "G0b:FAIL (total=$G0B_N, in_seam4_compose=$G0B_INFN) — failing the build"
  echo "build_exit:100" > "$OUT/build.exit"
  echo "G0b gate failed: expected exactly one o4_compose call site inside seam4_compose" > "$OUT/build.stderr"
  exit 100
fi
echo "=== build ==="
sha256sum "$ZNC" > "$OUT/compiler.sha256"
"$ZNC" "$SRC/main.zag" -o "$BIN" 2> "$OUT/build.stderr"
echo "build_exit:$?" > "$OUT/build.exit"
sha256sum "$BIN" > "$OUT/binary.sha256"
ls -l "$BIN" | awk '{print $5}' > "$OUT/binary.bytes"
# source hashes (all .zag files)
(cd "$SRC" && sha256sum *.zag substrate/*.zag) > "$OUT/sources.sha256"

# The binary's entry-gate static scans (G0/G0b/L5) read sources from the
# working directory: run everything from the source dir so the scans are
# deterministic regardless of where the driver was invoked.
cd "$SRC"

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
