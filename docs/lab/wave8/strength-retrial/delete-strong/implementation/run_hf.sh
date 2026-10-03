#!/bin/bash
# HOLEFIX re-verification runner (2026-09-26).
# Re-runs every battery 2x into logs/hf/ (old baseline logs untouched).
# Foreground sequential: background & jobs + relative redirects yield
# empty logs in this sandbox (RUNLOG 2026-09-26).
set -u
cd ~/workspace/strength-delete
OUT=logs/hf
mkdir -p $OUT/s1 $OUT/s10s100

echo "== attack batteries (2x) =="
cd r4val
for d in del_attack f1_attack f2_attack f4_attacks rt_redteam; do
  ./$d\_bin > ../$OUT/${d}_r1.log 2>&1
  ./$d\_bin > ../$OUT/${d}_r2.log 2>&1
  echo "$d done"
done
for p in a b c; do
  ./r4_overwrite_bin $p > ../$OUT/r4_attack_${p}_r1.log 2>&1
  ./r4_overwrite_bin $p > ../$OUT/r4_attack_${p}_r2.log 2>&1
  echo "r4_overwrite $p done"
done
cd ..

echo "== gates (2x) =="
for arm in B C C-P3 B2; do
  ./trial_bin $arm GATE 0 S1 > $OUT/gate_${arm}_r1.log 2>&1
  ./trial_bin $arm GATE 0 S1 > $OUT/gate_${arm}_r2.log 2>&1
  echo "gate $arm done"
done

echo "== S1 matrix 36 cells (2x) =="
for arm in B C C-P3 B2; do
  for cur in VUP WBS JI; do
    for v in 0 1 2; do
      ./trial_bin $arm $cur $v S1 > $OUT/s1/cell_${arm}_${cur}_${v}_r1.log 2>&1
      ./trial_bin $arm $cur $v S1 > $OUT/s1/cell_${arm}_${cur}_${v}_r2.log 2>&1
    done
  done
  echo "S1 $arm done"
done

echo "== S10/S100 spots (2x) =="
for spec in "B JI 0 S10" "B JI 0 S100" "B VUP 2 S10" "B VUP 2 S100"; do
  set -- $spec
  ./trial_bin $1 $2 $3 $4 > $OUT/s10s100/cell_${1}_${2}_${3}_${4}_r1.log 2>&1
  ./trial_bin $1 $2 $3 $4 > $OUT/s10s100/cell_${1}_${2}_${3}_${4}_r2.log 2>&1
  echo "spot $spec done"
done
echo "ALL DONE"
