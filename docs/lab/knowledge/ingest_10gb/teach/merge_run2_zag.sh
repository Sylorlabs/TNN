#!/bin/bash
# merge_run2_zag.sh — merge 8 run-2 sources with merge_zag_bin (runbook order).
# Run-2 outputs live in stage/*_r2 (independent re-cleanings, same staged inputs).
# Exits 1 if any shard missing. Writes facts_run2.dat + .sha256.
set -u
W=~/workspace/scratch_10gb_work
MERGE=$W/merge_zag_bin
OUT=$W/facts_run2.dat
LOG=$W/logs/merge_run2.log
cd "$W" || exit 1
SHARDS="stage/ostx_r2/facts.dat stage/gb_A_r2/facts.dat stage/gb_B_r2/facts.dat stage/se_bio_r2/facts.dat stage/se_chem_r2/facts.dat stage/se_phys_r2/facts.dat stage/se_math_r2/facts.dat stage/wiki_r2/facts.dat"
for s in $SHARDS; do
  if [ ! -f "$s" ]; then echo "[merge] MISSING shard: $s"; exit 1; fi
done
echo "[merge] run-2 shards ok, starting $(date -u)" | tee "$LOG"
time $MERGE "$OUT" $SHARDS >> "$LOG" 2>&1
rc=$?
echo "[merge] merge_zag_bin rc=$rc" | tee -a "$LOG"
[ $rc -ne 0 ] && exit $rc
sha256sum "$OUT" | tee "$W/facts_run2.dat.sha256"
echo "[merge] done $(date -u)" | tee -a "$LOG"
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
echo "=== determinism gate ==="
S1=$(cat $W/facts_run1.dat.sha256 | cut -d' ' -f1)
S2=$(cat $W/facts_run2.dat.sha256 | cut -d' ' -f1)
if [ "$S1" = "$S2" ]; then echo "PASS: facts_run1 == facts_run2 ($S1)"; else echo "FAIL: $S1 != $S2"; exit 1; fi
