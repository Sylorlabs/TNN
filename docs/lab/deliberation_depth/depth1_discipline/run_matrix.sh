#!/bin/bash
# Full D1 discipline matrix: forks x batteries x 2 runs, byte-identical rerun check.
D=/home/hatch/workspace/tnn-lab/deliberation_depth/depth1_discipline
BIN=$D/harness/d1_harness
OUT=$D/results/matrix
mkdir -p $OUT
declare -A CFGS=( [d1a]=d1a.cfg [d1b]=d1b.cfg [d1c]=d1c.cfg [d1d]=d1d.cfg [d1e]=d1e.cfg [depth2]=depth2.cfg )
BATS=(trap admit revoke logic rt_d1)
fail=0
for fork in d1a d1b d1c d1d d1e depth2; do
  for b in "${BATS[@]}"; do
    if [ "$b" = "rt_d1" ]; then items=$D/batteries/rt_d1.jsonl; else items=$D/../items_v2/$b.jsonl; fi
    for run in 1 2; do
      $BIN "$items" "$D/configs/${CFGS[$fork]}" "$OUT/${fork}_${b}_r${run}.jsonl" "$OUT/${fork}_${b}_r${run}.ledger" > /tmp/mat.log 2>&1
      if [ $? -ne 0 ]; then echo "RUN FAIL: $fork $b r$run"; cat /tmp/mat.log; fail=1; fi
    done
    if cmp -s "$OUT/${fork}_${b}_r1.jsonl" "$OUT/${fork}_${b}_r2.jsonl" && cmp -s "$OUT/${fork}_${b}_r1.ledger" "$OUT/${fork}_${b}_r2.ledger"; then
      echo "$fork/$b: reruns identical"
    else
      echo "RERUN MISMATCH: $fork $b"; fail=1
    fi
  done
done
echo "fail=$fail"
