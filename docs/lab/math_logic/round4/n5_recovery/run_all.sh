#!/bin/bash
# N5 sealed-battery recovery run (independent recovery agent).
# Protocol per PREREG_MATH_R4.md (frozen, commit 84ed45077a554f9897ec55c2ca1430273c79eb69):
#   - pure Zag binary rebuilt from frozen n5.zag (pinned znc), byte-identical to crew build
#   - R4 knowledge store (prereg §2), NOT the corrupted R3 path the crew used
#   - 3x byte-identical reruns per problem, clean cache snapshot each run
#   - PARA-INV gate first (prereg §2 para 7: gate runs before bar scoring)
set -u
ONLY="${1:-all}"   # comma-separated battery subset: para,pb1,pb2,pb3,pb4,chain50 ; or "all"
want() { case ",$ONLY," in *,all,*|*,$1,*) return 0;; *) return 1;; esac }
CACHEPFX="${2:-n5rc}"  # /tmp file prefix so parallel runners don't share cache files
N5=~/workspace/n5_recovery/n5_bin
R4B=~/workspace/tnn-lab/math_logic/round4/batteries
R3B=~/workspace/tnn-lab/math_logic/round3/batteries
KNOW=$R4B/knowledge/KNOWLEDGE_STORE_NL.md
OUT=~/workspace/n5_recovery/runs
LOG=$OUT/RUNLOG.txt
mkdir -p $OUT
cd ~/workspace/tnn-lab/math_logic/round4/engines/n5

echo -n "" > /tmp/${CACHEPFX}_cache_clean.txt
echo "=== N5 recovery run started $(date -u) ===" | tee $LOG
echo "binary: $(sha256sum $N5 | cut -d' ' -f1)" | tee -a $LOG
echo "knowledge: $(sha256sum $KNOW | cut -d' ' -f1)" | tee -a $LOG

NONDET=0
run_one() { # battery, problem_file
  local bat=$1
  local f=$2
  local n
  n=$(basename "$f" .txt)
  mkdir -p "$OUT/$bat"
  if [ -f "$OUT/$bat/${n}_r1.out" ] && [ -f "$OUT/$bat/${n}_r2.out" ] && [ -f "$OUT/$bat/${n}_r3.out" ]; then
    cmp -s "$OUT/$bat/${n}_r1.out" "$OUT/$bat/${n}_r2.out" || { echo "NONDET $bat $n r1!=r2" | tee -a $LOG; NONDET=1; }
    cmp -s "$OUT/$bat/${n}_r1.out" "$OUT/$bat/${n}_r3.out" || { echo "NONDET $bat $n r1!=r3" | tee -a $LOG; NONDET=1; }
    grep -h "^VERDICT:" "$OUT/$bat/${n}_r1.out" | head -1 | sed "s/^/$bat $n /"
    return 0
  fi
  local rc ok=1
  for r in 1 2 3; do
    cp /tmp/${CACHEPFX}_cache_clean.txt /tmp/${CACHEPFX}_cache_run.txt
    timeout 180 "$N5" "$f" "$KNOW" /tmp/${CACHEPFX}_cache_run.txt /tmp/${CACHEPFX}_stage_run.txt > "$OUT/$bat/${n}_r${r}.out" 2>&1
    rc=$?
    if [ $rc -ne 0 ]; then echo "RC$rc $bat $n run$r" | tee -a $LOG; ok=0; fi
  done
  if ! cmp -s "$OUT/$bat/${n}_r1.out" "$OUT/$bat/${n}_r2.out"; then echo "NONDET $bat $n r1!=r2" | tee -a $LOG; NONDET=1; fi
  if ! cmp -s "$OUT/$bat/${n}_r1.out" "$OUT/$bat/${n}_r3.out"; then echo "NONDET $bat $n r1!=r3" | tee -a $LOG; NONDET=1; fi
  grep -h "^VERDICT:" "$OUT/$bat/${n}_r1.out" | head -1 | sed "s/^/$bat $n /"
}

if want para; then echo "--- PARA-INV gate ---" | tee -a $LOG
for i in 01 02 03 04 05 06 07 08 09 10 11 12; do
  BASE=$(python3 -c "import json; d=json.load(open('$R4B/para_inv/PARA_ENTAIL.json')); print(d['PARA_PAIR_$i']['base'])")
  run_one para "$R4B/chain_nl/${BASE}.txt" | tee -a $LOG
  run_one para "$R4B/para_inv/PARA_PAIR_$i.txt" | tee -a $LOG
  run_one para "$R4B/para_inv/PARA_NONCE_$i.txt" | tee -a $LOG
done
fi

if want pb1; then echo "--- PB1 R3N ---" | tee -a $LOG
for f in $R3B/r3n/R3N_*.txt; do run_one pb1 "$f" | tee -a $LOG; done
fi

if want pb2; then echo "--- PB2 twins ---" | tee -a $LOG
for f in $R3B/twins/T2_*.txt $R3B/twins/T3_*.txt $R3B/twins/T4_*.txt; do run_one pb2 "$f" | tee -a $LOG; done
fi

if want pb3; then echo "--- PB3 B5X-NL ---" | tee -a $LOG
for f in ${PB3PATTERN:-$R3B/b5x_nl/B5X_NL_*.txt}; do run_one pb3 "$f" | tee -a $LOG; done
fi

if want pb4; then echo "--- PB4 CHAIN-NL ---" | tee -a $LOG
for f in $R4B/chain_nl/CHAIN_NL_*.txt; do run_one pb4 "$f" | tee -a $LOG; done
fi

if want chain50; then echo "--- H-CHAIN CHAIN50-NL ---" | tee -a $LOG
for f in $R4B/chain50_nl/CHAIN50_NL_*.txt; do run_one chain50 "$f" | tee -a $LOG; done
fi

echo "=== finished $(date -u); NONDET=$NONDET ===" | tee -a $LOG
