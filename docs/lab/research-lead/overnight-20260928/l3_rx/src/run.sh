#!/bin/sh
# run.sh -- L3-RX sealed battery harness. Shell ONLY for plumbing/sequencing;
# all decisions (learning, answering, scoring, auditing, verdict) are Zag.
# Usage: run.sh <rundir> <sealeddir> [flags]
#   flags: "" (main battery) | "noops" (C-NOOP on F1) | "wiped" (C-SCRATCH on F3)
# Worlds run in frozen order; kb.txt persists across worlds within a run.
# Learner sees ONLY train.txt (+ its own kb/trace/commit/protocol files).
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
B=../build
RUNDIR=$1
SEALED=$2
FLAGS=$3
mkdir -p "$RUNDIR"
printf '0' > "$RUNDIR/seq.txt"
: > "$RUNDIR/trace.txt"
: > "$RUNDIR/kb.txt"
: > "$RUNDIR/proto.log"
: > "$RUNDIR/metrics.txt"

run_world() {
  WID=$1
  FAM=$2
  SRC=$3
  WDIR="$RUNDIR/$WID"
  mkdir -p "$WDIR"
  cp "$SEALED/$SRC/train.txt" "$WDIR/train.txt"
  rm -f "$WDIR/commit.txt" "$WDIR/probe_req.txt" "$WDIR/probe_ans.txt"
  touch "$WDIR/probe_ans.txt"
  N=0
  while [ $N -lt 40 ]; do
    N=$((N+1))
    "$B/rx" "$RUNDIR" "$WDIR" "$WID" "$FLAGS"
    RC=$?
    if [ $RC -eq 7 ]; then
      "$B/answer" "$SEALED/$SRC/oracle.txt" "$WDIR/probe_req.txt" "$WDIR/probe_ans.txt" "$RUNDIR/proto.log"
    else
      break
    fi
  done
  if [ $N -ge 40 ]; then
    echo "INVOCATION CAP EXCEEDED on $WID" >&2
    exit 1
  fi
  # stage sealed heldout for the scorer AFTER the learner finished
  # (learner never sees it; scorer is trusted)
  cp "$SEALED/$SRC/heldout.txt" "$WDIR/heldout.txt"
  "$B/score" "$WDIR" "$FAM" "$WID" >> "$RUNDIR/metrics.txt"
}

if [ "$FLAGS" = "noops" ]; then
  for W in w_f1_1 w_f1_2 w_f1_3 w_f1_4; do
    run_world "noop_$W" gated "$W"
  done
  exit 0
fi
if [ "$FLAGS" = "wiped" ]; then
  run_world w_f3_1 gated w_f3_1
  run_world w_f3_2 gated w_f3_2
  exit 0
fi

# main battery (frozen order)
run_world w_f1_1 gated w_f1_1
run_world w_f1_2 gated w_f1_2
run_world w_f1_3 gated w_f1_3
run_world w_f1_4 gated w_f1_4
run_world w_f2_1 f2 w_f2_1
run_world w_f2_2 f2 w_f2_2
run_world w_f3_1 gated w_f3_1
run_world w_f3_2 gated w_f3_2
run_world w_f4 gated w_f4
run_world w_f5 gated w_f5
run_world w_f6 plain w_f6
echo "battery done: $RUNDIR"
