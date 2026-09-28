#!/bin/bash
# Phase 4 style attribution battery runner.
# Runs every sealed script 3x (2 plain + 1 MALLOC_PERTURB_=165), verifies
# byte-identical stdout via sha256. K-D gates validity.
set -u
BIN=/home/hatch/workspace/phase4style/build/sa_bin
SEALED=/home/hatch/workspace/phase4style/sealed/scripts
OUT=/home/hatch/workspace/phase4style/results
mkdir -p "$OUT"
fail=0
for s in train asked watch profiles lesion_none lesion_LEN lesion_CASE lesion_PUNCT lesion_LEX lesion_STRUCT lesion_all redteam; do
  for r in 1 2 3; do
    if [ "$r" = "3" ]; then
      MALLOC_PERTURB_=165 "$BIN" "$SEALED/$s.txt" > "$OUT/$s.r$r" 2>"$OUT/$s.r$r.err"
    else
      "$BIN" "$SEALED/$s.txt" > "$OUT/$s.r$r" 2>"$OUT/$s.r$r.err"
    fi
  done
  h1=$(sha256sum "$OUT/$s.r1" | cut -d' ' -f1)
  h2=$(sha256sum "$OUT/$s.r2" | cut -d' ' -f1)
  h3=$(sha256sum "$OUT/$s.r3" | cut -d' ' -f1)
  if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then
    echo "OK   $s $h1"
  else
    echo "FAIL $s $h1 $h2 $h3"
    fail=1
  fi
  if [ -s "$OUT/$s.r1.err" ]; then echo "STDERR NONEMPTY $s"; fail=1; fi
done
echo "---"
(cd "$OUT" && sha256sum *.r1 > SHA256SUMS_RESULTS.txt)
if [ "$fail" = "0" ]; then echo "K-D DETERMINISM HOLDS"; else echo "K-D FAILED"; exit 1; fi
