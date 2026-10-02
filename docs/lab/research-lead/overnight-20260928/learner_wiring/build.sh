#!/bin/sh
# LW1 build + run + determinism check. Pure shell; safebin PATH only.
export PATH="$HOME/safebin"
set -u
D=docs/lab/research-lead/overnight-20260928/learner_wiring
cd "$HOME/workspace/tnn-rsi" || exit 1
znc "$D/lw1.zag" -o "$D/lw1_bin" --no-analyze > "$D/compile.log" 2>&1
rc=$?
if [ $rc -ne 0 ]; then cat "$D/compile.log"; exit 1; fi
mkdir -p "$D/runs"
: > "$D/sha256sums.txt"
for cond in base bridge selfwire noeval nowrite; do
  for r in 1 2 3; do
    "./$D/lw1_bin" "$cond" > "$D/runs/${cond}_run${r}.txt" || exit 1
  done
  sha256sum "$D/runs/${cond}_run1.txt" "$D/runs/${cond}_run2.txt" "$D/runs/${cond}_run3.txt" >> "$D/sha256sums.txt"
  cmp -s "$D/runs/${cond}_run1.txt" "$D/runs/${cond}_run2.txt" || { echo "NONDET $cond run1 vs run2"; exit 1; }
  cmp -s "$D/runs/${cond}_run2.txt" "$D/runs/${cond}_run3.txt" || { echo "NONDET $cond run2 vs run3"; exit 1; }
done
echo "BUILD-RUN-OK"
for cond in base bridge selfwire noeval nowrite; do
  echo "=== $cond ==="
  cat "$D/runs/${cond}_run1.txt"
done
