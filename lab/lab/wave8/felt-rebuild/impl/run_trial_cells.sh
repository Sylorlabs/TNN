#!/usr/bin/env bash
# FELT-INTENSITY V3 trial cell runner.
# Runs the 12 preregistered trial cells (F/N x variants 0/1/2 x 2 runs),
# verifies paired byte-identical determinism, then runs the independent checker.
#
# DO NOT RUN without Micah's explicit authorization for the trial cells.
# Calibration (cal7/cal8) was authorized 2026-09-20 and is NOT re-run here;
# the trial constants are frozen in calib_consts.zag per CALIBRATION_RECORD.md.
set -euo pipefail
IMPL="$(cd "$(dirname "$0")" && pwd)"
cd "$IMPL"

echo "== build =="
./build.sh || { echo "BUILD_FAILED"; exit 1; }

OUT="$IMPL/trial_out"
mkdir -p "$OUT"

echo "== trial cells (12 runs) =="
for arm in f n; do
  for v in 0 1 2; do
    for r in a b; do
      f="$OUT/cell_${arm}${v}_${r}.txt"
      echo "  $arm v$v run $r -> $f"
      ./felt_trial_v3_bin "$arm" "$v" > "$f" 2>"$f.err" || {
        echo "RUN_FAILED $arm $v $r"; exit 1; }
      # FELT_DONE must be present (complete run)
      grep -q '^FELT_DONE$' "$f" || { echo "INCOMPLETE $f"; exit 1; }
    done
    # I-1: paired runs byte-identical
    cmp -s "$OUT/cell_${arm}${v}_a.txt" "$OUT/cell_${arm}${v}_b.txt" || {
      echo "DETERMINISM_FAIL ${arm} v${v}"; exit 1; }
    echo "  I-1 OK: ${arm} v${v} paired byte-identical"
  done
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
echo "TRIAL_RUN_COMPLETE"
