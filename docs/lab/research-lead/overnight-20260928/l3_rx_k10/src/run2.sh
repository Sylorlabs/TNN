#!/bin/sh
# run2.sh -- L3-RX-K10 battery harness. Shell ONLY for plumbing/sequencing;
# all decisions (worldgen, learning, answering, scoring, RK evaluation)
# are pure Zag. kb.txt persists across worlds within a run unless wiped.
# Usage: run2.sh <rundir> <sealeddir> <mode>
#   mode: main | poison | poisonctl
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
B=../build
RUNDIR=$1
SEALED=$2
MODE=$3
APPEND=$4
mkdir -p "$RUNDIR"
if [ "$APPEND" != "append" ]; then
  printf '0' > "$RUNDIR/seq.txt"
  : > "$RUNDIR/trace.txt"
  : > "$RUNDIR/kb.txt"
  : > "$RUNDIR/proto.log"
  : > "$RUNDIR/metrics.txt"
fi

run_world() {
  WID=$1    # learner-visible world id
  SRC=$2    # sealed source dir
  RK=$3     # rkmode for scorer
  WDIR="$RUNDIR/$WID"
  mkdir -p "$WDIR"
  cp "$SEALED/$SRC/train.txt" "$WDIR/train.txt"
  rm -f "$WDIR/commit.txt" "$WDIR/probe_req.txt" "$WDIR/probe_ans.txt"
  touch "$WDIR/probe_ans.txt"
  N=0
  while [ $N -lt 40 ]; do
    N=$((N+1))
    "$B/rx" "$RUNDIR" "$WDIR" "$WID" ""
    RC=$?
    if [ $RC -eq 7 ]; then
      "$B/answer2" "$SEALED/$SRC/oracle.txt" "$WDIR/probe_req.txt" "$WDIR/probe_ans.txt" "$RUNDIR/proto.log"
    else
      break
    fi
  done
  if [ $N -ge 40 ]; then
    echo "INVOCATION CAP EXCEEDED on $WID" >&2
    exit 1
  fi
  # stage sealed heldout AFTER the learner finished (learner never sees it)
  cp "$SEALED/$SRC/heldout.txt" "$WDIR/heldout.txt"
  "$B/score2" "$RUNDIR" "$WDIR" "$WID" "$RK" > /dev/null
}

run_world_wiped() {
  # same, but the "wiped" flag is passed to the learner (kb ignored)
  WID=$1
  SRC=$2
  RK=$3
  WDIR="$RUNDIR/$WID"
  mkdir -p "$WDIR"
  cp "$SEALED/$SRC/train.txt" "$WDIR/train.txt"
  rm -f "$WDIR/commit.txt" "$WDIR/probe_req.txt" "$WDIR/probe_ans.txt"
  touch "$WDIR/probe_ans.txt"
  N=0
  while [ $N -lt 40 ]; do
    N=$((N+1))
    "$B/rx" "$RUNDIR" "$WDIR" "$WID" "wiped"
    RC=$?
    if [ $RC -eq 7 ]; then
      "$B/answer2" "$SEALED/$SRC/oracle.txt" "$WDIR/probe_req.txt" "$WDIR/probe_ans.txt" "$RUNDIR/proto.log"
    else
      break
    fi
  done
  if [ $N -ge 40 ]; then
    echo "INVOCATION CAP EXCEEDED on $WID" >&2
    exit 1
  fi
  cp "$SEALED/$SRC/heldout.txt" "$WDIR/heldout.txt"
  "$B/score2" "$RUNDIR" "$WDIR" "$WID" "$RK" > /dev/null
}

wipe_kb() {
  : > "$RUNDIR/kb.txt"
}

if [ "$MODE" = "main" ]; then
  run_world w1 w1 0
  run_world w5 w5 4
  wipe_kb
  run_world w2 w2 1
  wipe_kb
  run_world w3 w3 2
  run_world w6 w6 4
  wipe_kb
  run_world_wiped w6w w6 4
  exit 0
fi
if [ "$MODE" = "poison" ]; then
  wipe_kb
  run_world w4a w4a 0
  run_world w4b w4b 3
  exit 0
fi
if [ "$MODE" = "poisonctl" ]; then
  wipe_kb
  run_world_wiped w4bw w4b 5
  exit 0
fi
echo "unknown mode $MODE" >&2
exit 1
