#!/bin/bash
# drive_smallk.sh - run the sealed F-E worlds with the smallk contestant variant.
# Shell only. All experimental logic lives in frozen Zag binaries.
set -u
FE=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/c1_fe_family
SK=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/c1_smallk
cd "$SK"
mkdir -p runs diag_out
BIN=./contestant_smallk_bin
DIAG=$FE/diag_bin
RACE=$FE/run_race.sh
: > diag_out/famE_smallk.txt
for W in 0 1 2 3 4 5 6 7; do
  TAG=E${W}
  for REP in 1 2 3; do
    RDIR=runs/${TAG}_r${REP}
    bash "$RACE" $FE/worlds/${TAG} "$BIN" "$RDIR" > /dev/null 2>&1 || { echo "RACE-FAIL $TAG r$REP"; exit 1; }
  done
  for REP in 2 3; do
    cmp -s runs/${TAG}_r1/replies.jsonl runs/${TAG}_r${REP}/replies.jsonl || { echo "RACE-NONDET-REPLIES $TAG r$REP"; exit 1; }
    cmp -s runs/${TAG}_r1/scores.jsonl runs/${TAG}_r${REP}/scores.jsonl || { echo "RACE-NONDET-SCORES $TAG r$REP"; exit 1; }
    cmp -s runs/${TAG}_r1/state/state.txt runs/${TAG}_r${REP}/state/state.txt || { echo "RACE-NONDET-STATE $TAG r$REP"; exit 1; }
  done
  for REP in 1 2 3; do
    RDIR=runs/${TAG}_r${REP}
    "$DIAG" $RDIR/state/state.txt $FE/worlds/${TAG}/turns.jsonl $RDIR/scores.jsonl >> diag_out/famE_smallk.txt 2>&1 || { echo "DIAG-FAIL $TAG r$REP"; exit 1; }
  done
  echo "RACE-OK $TAG"
done
echo "ALL-RACE-OK"
echo "=== SMALLK SUMMARY (from diag_out/famE_smallk.txt) ==="
echo "R1 total: $(grep -c '^R1' diag_out/famE_smallk.txt)"
echo "R1 HIT-OK: $(grep '^R1' diag_out/famE_smallk.txt | grep -c 'loc=HIT-OK')"
echo "R1 APPLICATION: $(grep '^R1' diag_out/famE_smallk.txt | grep -c 'loc=APPLICATION')"
echo "R1 UNCLASSIFIED: $(grep '^R1' diag_out/famE_smallk.txt | grep -c 'loc=UNCLASSIFIED')"
echo "R2 HIT-OK: $(grep '^R2' diag_out/famE_smallk.txt | grep -c 'loc=HIT-OK')"
echo "R3 HIT-OK: $(grep '^R3' diag_out/famE_smallk.txt | grep -c 'loc=HIT-OK')"
echo "det_fail total: $(grep -o 'det_fail=[0-9]*' diag_out/famE_smallk.txt | grep -v 'det_fail=0' | wc -l)"
echo "DONE"
