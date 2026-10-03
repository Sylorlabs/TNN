#!/bin/bash
# drive_revert.sh - orchestration only. All experimental logic lives in the
# frozen Zag binaries (world_gen_revert_bin, contestant_bin, diag_bin, agg_bin).
# Steps: seeds (post-freeze /dev/urandom) -> gen x2 byte-identical -> race x3
# reps byte-identical -> diag per run -> per-family concat -> agg.
set -u
A=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/c1_revert_attack
cd "$A"
mkdir -p seeds worlds runs diag_out
GEN=./world_gen_revert_bin
BIN=./contestant_bin
DIAG=./diag_bin
: > seeds/hashes.txt
for FAM in A B C D; do
  for W in 0 1 2 3 4 5 6 7; do
    TAG=${FAM}${W}
    head -c 8 /dev/urandom > seeds/${TAG}.bin
    SH=$(sha256sum seeds/${TAG}.bin | cut -c1-16)
    echo "${TAG} ${SH}" >> seeds/hashes.txt
    for DUP in a b; do
      mkdir -p worlds/${TAG}_${DUP}
      $GEN seeds/${TAG}.bin $W worlds/${TAG}_${DUP} "$SH" $FAM || { echo "GEN-FAIL $TAG $DUP"; exit 1; }
    done
    cmp -s worlds/${TAG}_a/turns.jsonl worlds/${TAG}_b/turns.jsonl || { echo "GEN-NONDET-TURNS $TAG"; exit 1; }
    cmp -s worlds/${TAG}_a/key.json worlds/${TAG}_b/key.json || { echo "GEN-NONDET-KEY $TAG"; exit 1; }
    rm -rf worlds/${TAG}_b
    mv worlds/${TAG}_a worlds/${TAG}
    echo "GEN-OK $TAG"
  done
done
echo "ALL-GEN-OK"
for FAM in A B C D; do
  : > diag_out/fam${FAM}.txt
  for W in 0 1 2 3 4 5 6 7; do
    TAG=${FAM}${W}
    for REP in 1 2 3; do
      RDIR=runs/${TAG}_r${REP}
      bash run_race.sh worlds/${TAG} $BIN $RDIR > /dev/null 2>&1 || { echo "RACE-FAIL $TAG r$REP"; exit 1; }
    done
    for REP in 2 3; do
      cmp -s runs/${TAG}_r1/replies.jsonl runs/${TAG}_r${REP}/replies.jsonl || { echo "RACE-NONDET-REPLIES $TAG r$REP"; exit 1; }
      cmp -s runs/${TAG}_r1/scores.jsonl runs/${TAG}_r${REP}/scores.jsonl || { echo "RACE-NONDET-SCORES $TAG r$REP"; exit 1; }
      cmp -s runs/${TAG}_r1/state/state.txt runs/${TAG}_r${REP}/state/state.txt || { echo "RACE-NONDET-STATE $TAG r$REP"; exit 1; }
    done
    for REP in 1 2 3; do
      RDIR=runs/${TAG}_r${REP}
      $DIAG $RDIR/state/state.txt worlds/${TAG}/turns.jsonl $RDIR/scores.jsonl >> diag_out/fam${FAM}.txt 2>&1 || { echo "DIAG-FAIL $TAG r$REP"; exit 1; }
    done
    echo "RACE-OK $TAG"
  done
done
echo "ALL-RACE-OK"
./agg_bin diag_out/famA.txt diag_out/famB.txt diag_out/famC.txt diag_out/famD.txt | tee diag_out/agg.txt
echo "DONE"
