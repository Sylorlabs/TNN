#!/bin/bash
# merge_run1_zag.sh — merge 8 run-1 sources with the PROVEN pure-Zag k-way merger.
# Runbook shard order: ostx, gb_A, gb_B, se_bio, se_chem, se_phys, se_math, wiki.
# All shards must exist; exits 1 otherwise. Writes facts_run1.dat + .sha256.
set -u
W=~/workspace/scratch_10gb_work
MERGE=$W/merge_zag_bin
OUT=$W/facts_run1.dat
LOG=$W/logs/merge_run1.log
cd "$W" || exit 1
SHARDS="stage/ostx_run2/facts.dat stage/gb_A_run1/facts.dat stage/gb_B_run1/facts.dat stage/se_bio_run2/facts.dat stage/se_chem_run1/facts.dat stage/phys_run1/facts.dat stage/se_math_run1/facts.dat stage/wiki_run1/facts.dat"
for s in $SHARDS; do
  if [ ! -f "$s" ]; then echo "[merge] MISSING shard: $s"; exit 1; fi
done
echo "[merge] run-1 shards ok, starting $(date -u)" | tee "$LOG"
time $MERGE "$OUT" $SHARDS >> "$LOG" 2>&1
rc=$?
echo "[merge] merge_zag_bin rc=$rc" | tee -a "$LOG"
[ $rc -ne 0 ] && exit $rc
sha256sum "$OUT" | tee "$W/facts_run1.dat.sha256"
echo "[merge] done $(date -u)" | tee -a "$LOG"
# record count
python3 -c "
import struct
n=0
with open('$OUT','rb') as f:
    while True:
        h=f.read(7)
        if len(h)<7: break
        k,t=struct.unpack('>HI',h[1:7])
        f.seek(k+t,1); n+=1
print('records:',n)" | tee -a "$LOG"
