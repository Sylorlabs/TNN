#!/bin/bash
cd ~/workspace/scratch-li-f4
n=0; fail=0
for d in runs/c1c2_pass1/work/*/; do
  c=$(basename $d)
  [ -f "$d/verdict.out" ] || continue
  q=$(grep -m1 "^QUERY|" $d/query.out 2>/dev/null | cut -d'|' -f2-)
  [ -n "$q" ] || continue
  ./webg_bf1 verdict fid/state3 "$d/need.txt" "$d/pages.txt" FACT "$q" > fid/cmp.out 2>&1
  n=$((n+1))
  cmp -s fid/cmp.out "$d/verdict.out" || { echo "DIFF: $c"; fail=$((fail+1)); }
done
echo "fidelity: compared=$n diffs=$fail"
