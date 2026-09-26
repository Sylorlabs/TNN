#!/bin/bash
# FORK B battery runner: PB1 (R3N) + PB4 (CHAIN-NL), 2x byte-identical reruns,
# clean cache snapshot per run, 180 s timeout per run (recovery protocol).
set -u
N5=~/workspace/n5_fork_b/n5b_bin
R4B=~/workspace/tnn-lab/math_logic/round4/batteries
R3B=~/workspace/tnn-lab/math_logic/round3/batteries
KNOW=$R4B/knowledge/KNOWLEDGE_STORE_NL.md
OUT=~/workspace/n5_fork_b/evidence/runs
LOG=$OUT/RUNLOG.txt
mkdir -p "$OUT/pb1" "$OUT/pb4"
cd ~/workspace/tnn-lab/math_logic/round4/engines/n5

echo -n "" > /tmp/forkb_cache_clean.txt
echo "=== FORK B run started $(date -u) ===" | tee "$LOG"
echo "binary: $(sha256sum $N5 | cut -d' ' -f1)" | tee -a "$LOG"
echo "source: $(sha256sum ~/workspace/n5_fork_b/n5b.zag | cut -d' ' -f1)" | tee -a "$LOG"
echo "knowledge: $(sha256sum $KNOW | cut -d' ' -f1)" | tee -a "$LOG"

NONDET=0
CRASH=0
run_one() { # battery, problem_file
  local bat=$1 f=$2 n rc
  n=$(basename "$f" .txt)
  for r in 1 2; do
    cp /tmp/forkb_cache_clean.txt /tmp/forkb_cache_run.txt
    timeout 180 "$N5" "$f" "$KNOW" /tmp/forkb_cache_run.txt /tmp/forkb_stage_run.txt > "$OUT/$bat/${n}_r${r}.out" 2>&1
    rc=$?
    if [ $rc -ne 0 ]; then echo "RC$rc $bat $n run$r" | tee -a "$LOG"; CRASH=1; fi
  done
  if ! cmp -s "$OUT/$bat/${n}_r1.out" "$OUT/$bat/${n}_r2.out"; then
    echo "NONDET $bat $n r1!=r2" | tee -a "$LOG"; NONDET=1
  fi
  grep -h "^VERDICT:" "$OUT/$bat/${n}_r1.out" | head -1 | sed "s/^/$bat $n /" | tee -a "$LOG"
}

echo "--- PB1 R3N ---" | tee -a "$LOG"
for f in $R3B/r3n/R3N_*.txt; do run_one pb1 "$f"; done
echo "--- PB4 CHAIN-NL ---" | tee -a "$LOG"
for f in $R4B/chain_nl/CHAIN_NL_*.txt; do run_one pb4 "$f"; done

echo "=== finished $(date -u); NONDET=$NONDET CRASH=$CRASH ===" | tee -a "$LOG"
