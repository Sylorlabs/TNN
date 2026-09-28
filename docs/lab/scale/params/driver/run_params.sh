#!/bin/bash
# param sweep runner: 19 configs x reps, byte-identity diff per config.
cd ~/workspace/scale-params/driver
BIN=./param_learner
TEXTS=~/workspace/scale/corpus/texts
OUT=../runs
SUM=$OUT/summary.tsv
echo -e "cfg\tclean_num\tclean_den\tflaw\tabs_num\tabs_den\tops_pf_x1000\ttotal_bpf\tdigest\tdet" > $SUM

run_cfg() { # name slot_num slot_den evw vdepth an ad redun reps
  local name=$1; shift
  local sn=$1 sd=$2 evw=$3 vd=$4 an=$5 ad=$6 rd=$7 reps=$8
  local i=0 det=OK
  while [ $i -lt $reps ]; do
    $BIN eval 24000 24 1000 1 $i $TEXTS $sn $sd $evw $vd $an $ad $rd > $OUT/${name}_r${i}.log 2>&1
    if [ $i -gt 0 ]; then
      if ! diff -q $OUT/${name}_r0.log $OUT/${name}_r${i}.log > /dev/null; then det=FAIL; fi
    fi
    i=$((i+1))
  done
  local L=$OUT/${name}_r0.log
  local cn=$(grep "SCALE_MASTERY,clean_num=" $L | sed 's/.*clean_num=//;s/,.*//')
  local cd2=$(grep "SCALE_MASTERY,clean_num=" $L | sed 's/.*clean_den=//')
  local flaw=$(grep "SCALE_FLAW_TOTAL" $L | sed 's/.*pass=//;s/,.*//')
  local abn=$(grep "SCALE_ABSORPTION" $L | sed 's/.*absorbed=//;s/,.*//')
  local abd=$(grep "SCALE_ABSORPTION" $L | sed 's/.*den=//')
  local ops=$(grep "SCALE_OPS" $L | sed 's/.*ops_per_fact_x1000=//')
  local bpf=$(grep "SCALE_MEM" $L | sed 's/.*total_bpf=//;s/,.*//')
  local dg=$(grep "SCALE_DIGEST" $L | sed 's/.*fnv1a=//')
  echo -e "${name}\t${cn}\t${cd2}\t${flaw}\t${abn}\t${abd}\t${ops}\t${bpf}\t${dg}\t${det}" >> $SUM
  echo "$name det=$det digest=$dg"
}

run_cfg base    1 1 64  1 1 1 1 5
run_cfg slot025 1 4 64  1 1 1 1 3
run_cfg slot05  1 2 64  1 1 1 1 3
run_cfg slot2   2 1 64  1 1 1 1 3
run_cfg slot4   4 1 64  1 1 1 1 3
run_cfg slot8   8 1 64  1 1 1 1 3
run_cfg ev16    1 1 16  1 1 1 1 3
run_cfg ev32    1 1 32  1 1 1 1 3
run_cfg ev128   1 1 128 1 1 1 1 3
run_cfg ev256   1 1 256 1 1 1 1 3
run_cfg depth2  1 1 64  2 1 1 1 3
run_cfg depth4  1 1 64  4 1 1 1 3
run_cfg audit05 1 1 64  1 1 2 1 3
run_cfg audit2  1 1 64  1 2 1 1 3
run_cfg audit4  1 1 64  1 4 1 1 3
run_cfg red2    1 1 64  1 1 1 2 3
run_cfg red4    1 1 64  1 1 1 4 3
run_cfg jsmall  1 2 16  1 1 2 1 3
run_cfg jbig    4 1 256 4 4 1 4 3
echo "SWEEP_DONE"
