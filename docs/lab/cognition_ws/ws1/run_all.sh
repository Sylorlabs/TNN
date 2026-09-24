#!/usr/bin/env bash
# WS1-A battery runner: 18 cells x 3 arms x 3 reruns = 162 executions.
# Logs raw stdout per run; sha256 every log; appends to a TSV manifest.
# Binaries stay out of the repo; logs do not (evidence).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BLD="$HERE/build"
RAW="$HERE/runs/raw"
MAN="$HERE/runs/manifest.tsv"
mkdir -p "$RAW"
if [ ! -f "$MAN" ]; then
    printf 'cell\tarm\trerun\tlog\tsha256\twall_s\trc\n' > "$MAN"
fi
for cap in 32 128 512; do
for adv in 0 15 35; do
for rep in 1 3; do
  cell="cap${cap}a${adv}r${rep}"
  for arm in trained naive auto; do
    bin="$BLD/w1a_arm1"; [ "$arm" = naive ] && bin="$BLD/w1a_arm3"; [ "$arm" = auto ] && bin="$BLD/w1a_auto"
    for rr in 1 2 3; do
      log="$RAW/${cell}_${arm}_r${rr}.log"
      t0=$(date +%s.%N)
      "$bin" "$cap" "$adv" "$rep" > "$log" 2>&1; rc=$?
      t1=$(date +%s.%N)
      wall=$(awk "BEGIN{print $t1-$t0}")
      sha=$(sha256sum "$log" | cut -d' ' -f1)
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$cell" "$arm" "$rr" "$(basename "$log")" "$sha" "$wall" "$rc" >> "$MAN"
      echo "done $cell $arm r$rr rc=$rc sha=${sha:0:12}"
    done
  done
done; done; done
echo "BATTERY COMPLETE: $(($(wc -l < "$MAN")-1)) runs"
