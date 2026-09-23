#!/usr/bin/env bash
# RESUME (2026-09-20, closer): the original run_trial_cells.sh was killed by a
# service restart during "n v0 run b". Completed cells (f0/f1/f2 a+b I-1 OK,
# n0_a FELT_DONE) are NOT touched. This script runs only the remaining cells
# with the identical binary and the runner's exact protocol, then runs the
# independent checker exactly as run_trial_cells.sh does.
set -euo pipefail
IMPL="$(cd "$(dirname "$0")" && pwd)"
cd "$IMPL"
OUT="$IMPL/trial_out"
LOG="$IMPL/logs/resume_2026-09-20.log"
exec >>"$LOG" 2>&1
echo "== resume $(date -u +%FT%TZ) =="
echo "binary: $(sha256sum felt_trial_v3_bin | cut -d' ' -f1)"
# remaining cells: n0_b, n1_a, n1_b, n2_a, n2_b
for spec in "n 0 b" "n 1 a" "n 1 b" "n 2 a" "n 2 b"; do
  set -- $spec; arm=$1; v=$2; r=$3
  f="$OUT/cell_${arm}${v}_${r}.txt"
  echo "  $arm v$v run $r -> $f"
  ./felt_trial_v3_bin "$arm" "$v" > "$f" 2>"$f.err" || { echo "RUN_FAILED $arm $v $r"; exit 1; }
  grep -q '^FELT_DONE$' "$f" || { echo "INCOMPLETE $f"; exit 1; }
done
for v in 0 1 2; do
  cmp -s "$OUT/cell_n${v}_a.txt" "$OUT/cell_n${v}_b.txt" || { echo "DETERMINISM_FAIL n v${v}"; exit 1; }
  echo "  I-1 OK: n v$v paired byte-identical"
done
echo "== independent checker =="
CELLS=()
for arm in F N; do
  la=$(echo "$arm" | tr 'A-Z' 'a-z')
  for v in 0 1 2; do
    CELLS+=(--cell "$arm,$v,$OUT/cell_${la}${v}_a.txt,$OUT/cell_${la}${v}_b.txt")
  done
done
python3 "$IMPL/check_felt_v3.py" --impl "$IMPL" "${CELLS[@]}" | tee "$OUT/check_report.txt"
grep -q '^CHECK_PASS$' "$OUT/check_report.txt" || { echo "CHECK_FAIL"; exit 1; }
echo "== sha256 of cell outputs =="
sha256sum "$OUT"/cell_*.txt | tee "$OUT/hashes.sha256"
echo "RESUME_COMPLETE"
