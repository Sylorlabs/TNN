#!/usr/bin/env bash
# Final PB4 tail: exact main-runner protocol (absolute KNOW, cache files).
set -u
N5=~/workspace/n5_fork_b/n5b_bin
R4B=~/workspace/tnn-lab/math_logic/round4/batteries
KNOW=$R4B/knowledge/KNOWLEDGE_STORE_NL.md
OUT=~/workspace/n5_fork_b/evidence/runs
LOG=$OUT/RUNLOG.txt
cd ~/workspace/tnn-lab/math_logic/round4/engines/n5 || exit 1
echo -n "" > /tmp/forkb_cache_clean.txt
run_one() { # $1=name
  local n="$1" f="$R4B/chain_nl/$n.txt" rc
  for r in 1 2; do
    [ "$n" = "CHAIN_NL_18" ] && [ "$r" = "1" ] && continue  # r1 kept from main run
    cp /tmp/forkb_cache_clean.txt /tmp/forkb_cache_run.txt
    timeout 180 "$N5" "$f" "$KNOW" /tmp/forkb_cache_run.txt /tmp/forkb_stage_run.txt > "$OUT/pb4/${n}_r${r}.out" 2>&1
    rc=$?
    if [ $rc -ne 0 ]; then echo "RC$rc pb4 $n run$r" >> "$LOG"; fi
  done
  if ! cmp -s "$OUT/pb4/${n}_r1.out" "$OUT/pb4/${n}_r2.out"; then
    echo "NONDET pb4 $n r1!=r2" >> "$LOG"
  else
    echo "pb4 $n DETERMINISTIC" >> "$LOG"
  fi
  grep -h "^VERDICT:" "$OUT/pb4/${n}_r1.out" | head -1 | sed "s/^/pb4 $n /" >> "$LOG"
}
for n in CHAIN_NL_18 CHAIN_NL_19 CHAIN_NL_20; do run_one "$n"; done
echo "=== FORK B run complete ===" >> "$LOG"
