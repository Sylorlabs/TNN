#!/bin/bash
# Full native-reproduction pipeline driver.
# Usage: run_all.sh <srcdir>   (srcdir holds frame_00.ppm .. frame_23.ppm)
# Every Zag binary runs TWICE; outputs must be byte-identical or the run FAILS.
set -u
SRC="${1:?srcdir required}"
HERE="$(cd "$(dirname "$0")" && pwd)"
BIN="$HERE/src/repro_bin"
RUNS="$HERE/runs"

pass=0; fail=0
chk() { # chk <desc> <outdir-is-last-arg> <cmd...>: run twice into det_a/det_b, byte-compare
  local desc="$1"; shift
  local d1="$RUNS/det_a" d2="$RUNS/det_b"
  rm -rf "$d1" "$d2"; mkdir -p "$d1" "$d2"
  local args1=() args2=()
  for a in "$@"; do
    args1+=("$a")
    if [ "$a" = "__OUT__" ]; then args2+=("$d2"); else args2+=("$a"); fi
  done
  # replace __OUT__ with d1 in args1
  local fixed1=()
  for a in "${args1[@]}"; do
    if [ "$a" = "__OUT__" ]; then fixed1+=("$d1"); else fixed1+=("$a"); fi
  done
  "${fixed1[@]}" >/dev/null 2>&1; local r1=$?
  "${args2[@]}" >/dev/null 2>&1; local r2=$?
  if [ $r1 -ne 0 ] || [ $r2 -ne 0 ]; then
    echo "FAIL $desc (rc1=$r1 rc2=$r2)"; fail=$((fail+1)); return 1
  fi
  if ! diff -r -q "$d1" "$d2" >/dev/null 2>&1; then
    echo "FAIL $desc (outputs differ between runs)"; fail=$((fail+1)); return 1
  fi
  echo "PASS $desc (2 runs byte-identical)"
  pass=$((pass+1))
}

echo "== source: $SRC =="
ls "$SRC"/frame_00.ppm >/dev/null || { echo "no frames in $SRC"; exit 1; }

# fresh output dirs (O_EXCL writers fail on existing files)
for d in work_verbatim out_verbatim work_encoded out_encoded bytecopy; do
  rm -rf "$RUNS/$d"; mkdir -p "$RUNS/$d"
done

echo "== ingest verbatim =="
"$BIN" ingest verbatim "$SRC" "$RUNS/work_verbatim"; echo "rc=$?"
echo "== recall verbatim =="
"$BIN" recall verbatim "$RUNS/work_verbatim" "$RUNS/out_verbatim"; echo "rc=$?"
echo "== ingest encoded =="
"$BIN" ingest encoded "$SRC" "$RUNS/work_encoded"; echo "rc=$?"
echo "== recall encoded =="
"$BIN" recall encoded "$RUNS/work_encoded" "$RUNS/out_encoded"; echo "rc=$?"

echo "== determinism: ingest verbatim =="
chk "ingest-verbatim-determinism" "$BIN" ingest verbatim "$SRC" __OUT__
echo "== determinism: recall verbatim =="
# recall needs a workdir input; use a stable one
rm -rf "$RUNS/det_ra" "$RUNS/det_rb"; mkdir -p "$RUNS/det_ra" "$RUNS/det_rb"
"$BIN" recall verbatim "$RUNS/work_verbatim" "$RUNS/det_ra" >/dev/null 2>&1
"$BIN" recall verbatim "$RUNS/work_verbatim" "$RUNS/det_rb" >/dev/null 2>&1
if diff -r -q "$RUNS/det_ra" "$RUNS/det_rb" >/dev/null 2>&1; then
  echo "PASS recall-verbatim-determinism (2 runs byte-identical)"; pass=$((pass+1))
else echo "FAIL recall-verbatim-determinism"; fail=$((fail+1)); fi

echo "== byte-copy control =="
cp "$SRC"/frame_*.ppm "$RUNS/bytecopy/"

echo "== floor control (240x240 shape renderer, 2 runs) =="
rm -rf "$RUNS/floor240"; mkdir -p "$RUNS/floor240"
"$HERE/src/floor_bin" "$RUNS/floor240"; echo "rc=$?"
rm -rf "$RUNS/det_fa" "$RUNS/det_fb"; mkdir -p "$RUNS/det_fa" "$RUNS/det_fb"
"$HERE/src/floor_bin" "$RUNS/det_fa" >/dev/null 2>&1
"$HERE/src/floor_bin" "$RUNS/det_fb" >/dev/null 2>&1
if diff -r -q "$RUNS/det_fa" "$RUNS/det_fb" >/dev/null 2>&1; then
  echo "PASS floor-determinism (2 runs byte-identical)"; pass=$((pass+1))
else echo "FAIL floor-determinism"; fail=$((fail+1)); fi

echo "== summary: pass=$pass fail=$fail =="
[ $fail -eq 0 ]
