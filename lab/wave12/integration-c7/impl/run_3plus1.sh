#!/usr/bin/env bash
# Head-on run driver for the C7 Direction 3+1 redesign
# (PREREG 2026-09-20-C7-DIRECTION-3PLUS1 §4).
# Builds the binary from a given source tree, runs the paired S10 stages,
# the controls, and the bite checks, collects instruments, verifies
# determinism. Adapted from the frozen analyze_s10.sh; SRC is a parameter.
# Usage: ./run_3plus1.sh <src_dir> <output_dir>
set -u
SRC="${1:?src_dir required}"
OUT="${2:-/tmp/c7_3plus1}"
BIN="$OUT/int1_c7_3plus1"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"

mkdir -p "$OUT"
echo "=== G0b: single o4_compose call site ==="
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
  exit 100
fi
echo "=== build ==="
sha256sum "$ZNC" > "$OUT/compiler.sha256"
"$ZNC" "$SRC/main.zag" -o "$BIN" 2> "$OUT/build.stderr"
echo "build_exit:$?" > "$OUT/build.exit"
sha256sum "$BIN" > "$OUT/binary.sha256"
(cd "$SRC" && sha256sum *.zag substrate/*.zag substrate/cl/*.zag) > "$OUT/sources.sha256" 2>/dev/null || \
  (cd "$SRC" && sha256sum *.zag substrate/*.zag) > "$OUT/sources.sha256"

cd "$SRC"

echo "=== paired stages s0..s5 ==="
for s in 0 1 2 3 4 5; do
  for rep in a b; do
    "$BIN" "s$s" > "$OUT/s${s}_${rep}.log" 2>&1
    echo "s${s}_${rep}:$?" >> "$OUT/stage.exits"
  done
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
  echo "--- C7 telemetry ---"
  grep -h "C7_TELEMETRY\|C7_COMP\|C7_NEW\|C7_LEGACY\|C7_POSCTRL\|C7_DUALISM" "$OUT"/controls.log
  echo "--- control verdicts ---"
  grep -h "CHECK,c[1-7]" "$OUT"/controls.log
} > "$OUT/instruments.txt"

echo "=== done ==="
cat "$OUT/determinism.txt"
