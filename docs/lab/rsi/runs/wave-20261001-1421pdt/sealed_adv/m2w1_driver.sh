#!/bin/bash
# M2-W1 interactive driver (deterministic, fixed by prereg).
# Usage: m2w1_driver.sh <run#>
# Grows the world file from the template; runs the shim on incremental
# snippets with persistent state; logs ACTs to the driver log.
set -e
export PATH="$HOME/safebin"
DIR=~/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-1421pdt/sealed_adv
SHIM=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_shim/freeze_shim2_bin
RUN=$1

WORLD=$DIR/m2w1_world_run$RUN.txt
TRANS=$DIR/m2w1_trans_run$RUN.txt
LOG=$DIR/m2w1_log_run$RUN.txt
STATE=$DIR/m2_state_run$RUN.bin

cp $DIR/m2w1_template.txt $WORLD
> $TRANS
> $LOG
rm -f $STATE

step() {
  local lines="$1"
  printf "%s\n" "$lines" >> $WORLD
  printf "%s\n" "$lines" > /tmp/m2w1_step.txt
  $SHIM /tmp/m2w1_step.txt $STATE > /tmp/m2w1_out.txt
  cat /tmp/m2w1_out.txt >> $TRANS
  grep "^CHOICE " /tmp/m2w1_out.txt | tail -1 | awk '{print $2}'
}

for k in 45001 45002 45003 45004; do
  case $k in
    45001) T=45101; Bv=45101 ;;
    45002) T=45102; Bv=45998 ;;
    45003) T=45103; Bv=45103 ;;
    45004) T=45104; Bv=45997 ;;
  esac
  C=$(step "ACT")
  INF="NONE"; OBS=""
  if [ "$C" = "1" ]; then INF="A"; OBS="OBSERVE $k 45500 $T"; fi
  if [ "$C" = "2" ]; then INF="B"; OBS="OBSERVE $k 45500 $Bv"; fi
  if [ "$C" = "3" ]; then INF="C"; OBS="OBSERVE $k 45500 45999"; fi
  echo "ACT CAL $k $C $INF" >> $LOG
  if [ -n "$OBS" ]; then step "$OBS" > /dev/null; fi
  step "OBSERVE $k 45500 $T" > /dev/null
  step "QUERY $k 45500 $T" > /dev/null
done

for k in 45011 45012 45013 45014; do
  case $k in
    45011) T=45111; Bv=45996 ;;
    45012) T=45112; Bv=45995 ;;
    45013) T=45113; Bv=45994 ;;
    45014) T=45114; Bv=45993 ;;
  esac
  step "QUERY $k 45500 $T" > /dev/null
  for i in 1 2; do
    C=$(step "ACT")
    INF="NONE"; OBS=""
    if [ "$C" = "1" ]; then INF="A"; OBS="OBSERVE $k 45500 $T"; fi
    if [ "$C" = "2" ]; then INF="B"; OBS="OBSERVE $k 45500 $Bv"; fi
    if [ "$C" = "3" ]; then INF="C"; OBS="OBSERVE $k 45500 45999"; fi
    echo "ACT INQ $k $C $INF" >> $LOG
    if [ -n "$OBS" ]; then step "$OBS" > /dev/null; fi
  done
  step "QUERY $k 45500 $T" > /dev/null
done

echo "M2-W1 RUN $RUN DONE"
