#!/bin/bash
# teach_store.sh — teach facts_run1.dat twice (pure-Zag gate_bin), compare stores
set -u
W=/home/hatch/workspace/scratch_10gb_work
T=/home/hatch/workspace/tnn-lab/knowledge/ingest_10gb/teach
FACTS=$W/facts_run1.dat
BAD=/home/hatch/workspace/tmp10/bad.bin
# count records to size ncap
NRECS=$(python3 -c "
import struct
n=0
with open('$FACTS','rb') as f:
    while True:
        h=f.read(7)
        if len(h)<7: break
        k,t=struct.unpack('>HI',h[1:7])
        f.seek(k+t,1); n+=1
print(n)")
echo "[teach] facts records: $NRECS"
NCAP=$((NRECS + NRECS/5 + 100000))
echo "[teach] ncap: $NCAP"
for S in 1 2; do
  echo "[teach] store$S starting"
  $T/gate_bin ingest "$FACTS" "$BAD" "$W/store$S/" $NCAP > $W/logs/teach_store$S.log 2>&1
  echo "[teach] store$S rc=$?"
done
echo "[teach] comparing stores"
diff -r $W/store1/ $W/store2/ && echo "[teach] STORES BYTE-IDENTICAL" || echo "[teach] STORES DIFFER"
sha256sum $W/store1/manifest.txt $W/store2/manifest.txt
