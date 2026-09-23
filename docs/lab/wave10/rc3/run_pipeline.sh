#!/usr/bin/env bash
# RC3 gated pipeline: wait for 1-min load < 2.5, then run equivalence proof,
# full trial, and negative control in sequence. Master log to logs/pipeline.log.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$BASE/logs"
LOG="$BASE/logs/pipeline.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== RC3 pipeline start $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
tries=0
while :; do
  load=$(awk '{print $1}' /proc/loadavg)
  echo "load_1min=$load (tries=$tries)"
  ok=$(awk "BEGIN{print ($load < 2.5) ? 1 : 0}")
  if [ "$ok" = "1" ]; then break; fi
  tries=$((tries+1))
  if [ "$tries" -gt 240 ]; then
    echo "LOAD STILL HIGH AFTER 4h: pipeline BLOCKED per compute discipline"
    exit 10
  fi
  sleep 60
done

echo "--- step 1: equivalence proof ---"
"$BASE/run_equiv_rc3.sh" || { echo "PIPELINE STOP: equivalence proof failed"; exit 1; }
echo "--- step 2: full RC3 trial ---"
"$BASE/run_rc3.sh"; rc=$?
if [ "$rc" -eq 3 ]; then
  echo "PIPELINE: prereg FALLBACK A triggered (projection > 8h) — full 100x run not started"
  exit 3
elif [ "$rc" -ne 0 ]; then
  echo "PIPELINE STOP: RC3 trial failed (rc=$rc)"
  exit 1
fi
echo "--- step 3: negative control ---"
"$BASE/run_neg_rc3.sh" || { echo "PIPELINE STOP: negative control failed"; exit 1; }
echo "=== RC3 pipeline complete $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
