#!/bin/bash
# Video COMBINATION experiment driver.
# Usage: run_combine.sh
# Ingests the pig clip with the existing repro machinery (verbatim, twice,
# byte-identical), then runs the combine attempt twice. The attempt is
# EXPECTED to refuse (rc=1, COMBINE_REFUSED): the clean negative.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPRO="$HOME/workspace/video-repro/src/repro_bin"
COMBINE="$HERE/src/combine_bin"
BUNNY_FRAMES="$HOME/workspace/video-repro/source/frames"
BUNNY_WORK="$HOME/workspace/video-repro/runs/work_verbatim"   # existing, read-only
PIG_FRAMES="$HERE/source/frames"
RUNS="$HERE/runs"

pass=0; fail=0
ls "$PIG_FRAMES"/frame_00.ppm >/dev/null || { echo "no pig frames"; exit 1; }
ls "$BUNNY_WORK"/store_verbatim.bin >/dev/null || { echo "no bunny store"; exit 1; }

for d in work_pig out_pig det_ia det_ib det_oa det_ob combine_a combine_b; do
  rm -rf "$RUNS/$d"; mkdir -p "$RUNS/$d"
done

echo "== ingest pig verbatim (run 1) =="
"$REPRO" ingest verbatim "$PIG_FRAMES" "$RUNS/det_ia"; echo "rc=$?"
echo "== ingest pig verbatim (run 2) =="
"$REPRO" ingest verbatim "$PIG_FRAMES" "$RUNS/det_ib"; echo "rc=$?"
if diff -r -q "$RUNS/det_ia" "$RUNS/det_ib" >/dev/null 2>&1; then
  echo "PASS pig-ingest-determinism (2 runs byte-identical)"; pass=$((pass+1))
else echo "FAIL pig-ingest-determinism"; fail=$((fail+1)); fi
rm -rf "$RUNS/work_pig"; cp -r "$RUNS/det_ia" "$RUNS/work_pig"

echo "== recall pig verbatim (2 runs) =="
"$REPRO" recall verbatim "$RUNS/work_pig" "$RUNS/det_oa" >/dev/null 2>&1
"$REPRO" recall verbatim "$RUNS/work_pig" "$RUNS/det_ob" >/dev/null 2>&1
if diff -r -q "$RUNS/det_oa" "$RUNS/det_ob" >/dev/null 2>&1; then
  echo "PASS pig-recall-determinism (2 runs byte-identical)"; pass=$((pass+1))
else echo "FAIL pig-recall-determinism"; fail=$((fail+1)); fi
rm -rf "$RUNS/out_pig"; cp -r "$RUNS/det_oa" "$RUNS/out_pig"
echo "== pig recall vs source frames =="
if diff -r -q "$PIG_FRAMES" "$RUNS/out_pig" >/dev/null 2>&1; then
  echo "PASS pig-recall-bit-identical-to-source"; pass=$((pass+1))
else echo "FAIL pig-recall-bit-identical-to-source"; fail=$((fail+1)); fi

echo "== combine attempt (run 1, expect rc=1 COMBINE_REFUSED) =="
"$COMBINE" combine "$BUNNY_WORK" "$RUNS/work_pig" "$RUNS/combine_a"; r1=$?; echo "rc=$r1"
echo "== combine attempt (run 2) =="
"$COMBINE" combine "$BUNNY_WORK" "$RUNS/work_pig" "$RUNS/combine_b"; r2=$?; echo "rc=$r2"
if [ $r1 -eq 1 ] && [ $r2 -eq 1 ]; then
  echo "PASS combine-refusal (rc=1 both runs)"; pass=$((pass+1))
else echo "FAIL combine-refusal (rc1=$r1 rc2=$r2, expected 1/1)"; fail=$((fail+1)); fi
if diff -q "$RUNS/combine_a/combine_refusal.txt" "$RUNS/combine_b/combine_refusal.txt" >/dev/null 2>&1; then
  echo "PASS combine-refusal-determinism (2 runs byte-identical)"; pass=$((pass+1))
else echo "FAIL combine-refusal-determinism"; fail=$((fail+1)); fi

echo "== summary: pass=$pass fail=$fail =="
[ $fail -eq 0 ]
