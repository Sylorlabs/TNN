#!/usr/bin/env bash
# WS1C Track A full head-to-head: every battery x 4 arms x 3 reruns.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BIN="$HERE/src/skep_main"
OUT="$HERE/runs/main"
LAB="$HOME/workspace/tnn-lab"
mkdir -p "$OUT"
declare -A BATS
BATS[rtd1]="$LAB/deliberation_depth/depth1_discipline/batteries/rt_d1.jsonl"
BATS[poison2]="$HERE/batteries/poison2.jsonl"
BATS[baitflip2]="$HERE/batteries/baitflip2.jsonl"
BATS[refute2]="$HERE/batteries/refute2.jsonl"
BATS[refusal]="$LAB/consciousness_cost/refusal.jsonl"
BATS[ambig1]="$HERE/batteries/ambig1.jsonl"
BATS[admit]="$LAB/deliberation_depth/items_v2/admit.jsonl"
BATS[revoke]="$LAB/deliberation_depth/items_v2/revoke.jsonl"
BATS[logic]="$LAB/deliberation_depth/items_v2/logic.jsonl"
BATS[trap]="$LAB/deliberation_depth/items_v2/trap.jsonl"
BATS[cost]="$LAB/deliberation_depth/items_v2/cost.jsonl"
for b in rtd1 poison2 baitflip2 refute2 refusal ambig1 admit revoke logic trap cost; do
  for arm in 1 2 3 4; do
    for r in 0 1 2; do
      "$BIN" "${BATS[$b]}" "$arm" "$OUT/${b}_arm${arm}_r${r}.jsonl" "$OUT/${b}_arm${arm}_r${r}.met.jsonl" || echo "FAIL $b arm$arm r$r"
    done
  done
  echo "done $b"
done
echo ALLDONE
