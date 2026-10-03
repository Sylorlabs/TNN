#!/bin/sh
# run_dev.sh -- frozen dev validation driver for C9GEN.
# Implements PREREG_C9GEN.md section 8 exactly. Shell only, no Python.
# Assumes: safebin PATH exported (Step 0). Run from the C9BAT lane dir.
# Usage: sh run_dev.sh
set -e
SEED=777001337
NITEMS=24
echo "=== C9GEN dev validation (seed $SEED) ==="
echo "--- 8.1 build from committed sources ---"
for f in c9gen c9gamer c9exp c9score; do
  znc $f.zag -o bin/$f 2>/dev/null
  echo "built bin/$f"
done
sha256sum bin/c9gen bin/c9gamer bin/c9exp bin/c9score | tee dev/BIN_HASHES.txt
echo "--- 8.2 three seeded generations ---"
for d in dev dev2 dev3; do
  mkdir -p $d
  bin/c9gen $SEED $d
done
for f in turns.jsonl key.txt worlds.txt manifest.txt; do
  sha256sum dev/$f dev2/$f dev3/$f
done
DET_OK=1
for f in turns.jsonl key.txt worlds.txt manifest.txt; do
  cmp -s dev/$f dev2/$f || DET_OK=0
  cmp -s dev/$f dev3/$f || DET_OK=0
done
if [ "$DET_OK" = "1" ]; then echo "DETERMINISM: 3/3 byte-identical"; else echo "DETERMINISM: FAIL"; fi
echo "--- 8.3 gamer negative controls ---"
bin/c9gamer dev/turns.jsonl old > dev/rep_old.txt
bin/c9gamer dev/turns.jsonl first > dev/rep_first.txt
bin/c9gamer dev/turns.jsonl second > dev/rep_second.txt
printf "gamer old:    "; bin/c9score dev/key.txt dev/rep_old.txt 2>/dev/null
printf "gamer first:  "; bin/c9score dev/key.txt dev/rep_first.txt 2>/dev/null
printf "gamer second: "; bin/c9score dev/key.txt dev/rep_second.txt 2>/dev/null
echo "--- 8.4 reference experimenter ---"
bin/c9exp dev/turns.jsonl > dev/rep_exp.txt
printf "experimenter: "; bin/c9score dev/key.txt dev/rep_exp.txt 2>/dev/null
echo "--- 8.5 honest UNKNOWN ---"
i=0
while [ "$i" -lt "$NITEMS" ]; do echo "UNKNOWN"; i=$((i+1)); done > dev/rep_unknown.txt
printf "all-UNKNOWN:  "; bin/c9score dev/key.txt dev/rep_unknown.txt 2>/dev/null
echo "--- 8.6 audits ---"
echo "chain-literal hits in c9gen.zag (want 0):"
grep -c 'X->Y->Z\|X->Z->Y\|Y->X->Z\|Y->Z->X\|Z->X->Y\|Z->Y->X' c9gen.zag || true
echo "which python3 at lane end (want empty):"
which python3 || true
echo "=== done ==="
