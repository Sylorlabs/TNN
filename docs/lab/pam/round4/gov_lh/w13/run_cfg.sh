#!/bin/bash
# run_cfg.sh — run one battery config twice, verify K2, store log.gz + hashes.
# usage: run_cfg.sh <variant f|a|b> <fam base|adv> <scale 10x|100x>
set -u
V=$1; FAM=$2; SCALE=$3
D=/home/hatch/workspace/pam_gov_lh/crew3_w13
BIN=$D/w13${V}_lease
STREAM=$D/w13_stream_${FAM}_${SCALE}.txt
R=$D/runs
mkdir -p "$R/scratch"
CFG=${V}_${FAM}_${SCALE}
for r in 1 2; do
  RAW=$R/scratch/${CFG}_r${r}.raw
  "$BIN" "$STREAM" > "$RAW"
  rc=$?
  if [ $rc -ne 0 ]; then echo "RUN FAILED rc=$rc $CFG r$r"; exit 1; fi
  sha256sum "$RAW" | cut -d' ' -f1 > "$R/${CFG}_r${r}.sha"
done
if ! cmp -s "$R/${CFG}_r1.sha" "$R/${CFG}_r2.sha"; then
  echo "K2 FAIL $CFG"; exit 1
fi
gzip -n -c "$R/scratch/${CFG}_r1.raw" > "$R/${CFG}.log.gz"
rm -f "$R"/scratch/${CFG}_r*.raw
echo "K2 OK $CFG sha=$(cat "$R/${CFG}_r1.sha") log=$R/${CFG}.log.gz"
