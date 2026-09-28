#!/bin/bash
# F1 AUTOPILOT runner: 3 timed runs, byte-identity determinism proof.
# Canonical artifacts (stdout RESULT lines, ledger) contain no timing data;
# wall-clock is measured by the shell and reported on separate TIMING lines.
set -u
AP=~/workspace/conscious_perception/forks/autopilot
FIX=~/workspace/conscious_perception/fixtures
OUT=$AP/results
BIN=$AP/f1
MAN=$AP/battery_all.txt
mkdir -p "$OUT"
export TMPDIR=~/workspace/tmp_commit

echo "F1RUN manifest=$MAN fixtures=$FIX runs=3"
for r in 1 2 3; do
  start=$(date +%s%N)
  "$BIN" "$MAN" "$FIX" "$OUT/ledger_run$r.txt" > "$OUT/stdout_run$r.txt" 2>"$OUT/stderr_run$r.txt"
  rc=$?
  end=$(date +%s%N)
  wall_ns=$((end - start))
  sha_out=$(sha256sum "$OUT/stdout_run$r.txt" | cut -d' ' -f1)
  sha_led=$(sha256sum "$OUT/ledger_run$r.txt" | cut -d' ' -f1)
  echo "TIMING run=$r rc=$rc wall_ns=$wall_ns wall_ms=$((wall_ns / 1000000)) stdout_sha256=$sha_out ledger_sha256=$sha_led"
  if [ $rc -ne 0 ]; then echo "F1RUN FAIL run=$r rc=$rc"; exit 1; fi
done

# byte-identity across the 3 runs (canonical stdout + ledger)
ok=1
for f in stdout_run1.txt stdout_run2.txt stdout_run3.txt; do :; done
cmp -s "$OUT/stdout_run1.txt" "$OUT/stdout_run2.txt" || { echo "DETERMINISM FAIL stdout run1 vs run2"; ok=0; }
cmp -s "$OUT/stdout_run2.txt" "$OUT/stdout_run3.txt" || { echo "DETERMINISM FAIL stdout run2 vs run3"; ok=0; }
cmp -s "$OUT/ledger_run1.txt" "$OUT/ledger_run2.txt" || { echo "DETERMINISM FAIL ledger run1 vs run2"; ok=0; }
cmp -s "$OUT/ledger_run2.txt" "$OUT/ledger_run3.txt" || { echo "DETERMINISM FAIL ledger run2 vs run3"; ok=0; }
if [ $ok -eq 1 ]; then
  echo "DETERMINISM PASS runs=3 stdout_bytes=$(wc -c < "$OUT/stdout_run1.txt") ledger_bytes=$(wc -c < "$OUT/ledger_run1.txt")"
else
  exit 1
fi

# aggregate line from run 1 summary
sum=$(grep "^SUMMARY" "$OUT/stdout_run1.txt")
n=$(echo "$sum" | sed 's/.*fixtures=\([0-9]*\).*/\1/')
c=$(echo "$sum" | sed 's/.*correct=\([0-9]*\).*/\1/')
o=$(echo "$sum" | sed 's/.*ops_total=\([0-9]*\).*/\1/')
head_hash=$(echo "$sum" | sed 's/.*chain_head=\([0-9a-f]*\).*/\1/')
echo "AGGREGATE fixtures=$n correct=$c wrong=$((n - c)) false_install_rate_x1000=$(( (n - c) * 1000 / n )) ops_total=$o ops_mean=$((o / n)) chain_head=$head_hash"
echo "F1RUN DONE"
