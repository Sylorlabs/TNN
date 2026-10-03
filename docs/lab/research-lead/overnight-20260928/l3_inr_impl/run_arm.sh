#!/bin/sh
# run_arm.sh -- L3-INR arm driver. Pure shell: invokes binaries, relays files.
# Usage: run_arm.sh <statedir> <arm> <world> <seed>
# The LEARNER never receives the world path (information firewall); only this
# driver passes it to world_bin. All relay appends are logged to proto.log.
# Exit: 0 = arm complete (summary.txt), 1 = driver/learner failure.
set -e
export PATH="$HOME/safebin"
STATEDIR="$1"; ARM="$2"; WORLD="$3"; SEED="$4"
HERE=$(dirname "$0")
LEARNER="$HERE/build/learner_bin"
WORLDBIN="$HERE/build/world_bin"
mkdir -p "$STATEDIR"
touch "$STATEDIR/proto.log"
echo "=== ARM $ARM SEED $SEED ===" >> "$STATEDIR/proto.log"
# per-arm TEST budget mirror (prereg section 6)
case "$ARM" in
  T1|T5a|T5b) BUDGET=3000 ;;
  T2|C0|C1|C2) BUDGET=100 ;;
  T3) BUDGET=300 ;;
  T3b) BUDGET=50 ;;
  T4) BUDGET=2000 ;;
  C3) BUDGET=3000 ;;
  C4) BUDGET=600 ;;
  C5) BUDGET=10 ;;
  *) BUDGET=100 ;;
esac
START_LINES=$(wc -l < "$STATEDIR/proto.log")
iter=0
while [ $iter -lt 5000 ]; do
  iter=$((iter+1))
  set +e
  "$LEARNER" "$STATEDIR" "$ARM" "$SEED"
  rc=$?
  set -e
  if [ $rc -eq 1 ]; then
    echo "ARM $ARM complete after $iter iterations" >> "$STATEDIR/proto.log"
    cp "$STATEDIR/summary.txt" "$STATEDIR/summary_${ARM}.txt"
    exit 0
  fi
  if [ $rc -ne 0 ]; then
    echo "LEARNER FAILED rc=$rc arm=$ARM iter=$iter" >> "$STATEDIR/proto.log"
    exit 1
  fi
  # relay outbox -> world -> inbox (empty outbox = internal phase step; continue)
  if [ -s "$STATEDIR/outbox.txt" ]; then
    sed 's/^/> /' "$STATEDIR/outbox.txt" >> "$STATEDIR/proto.log"
    "$WORLDBIN" "$WORLD" < "$STATEDIR/outbox.txt" > "$STATEDIR/resp.tmp"
    cat "$STATEDIR/resp.tmp" >> "$STATEDIR/inbox.txt"
    sed 's/^/< /' "$STATEDIR/resp.tmp" >> "$STATEDIR/proto.log"
    rm -f "$STATEDIR/resp.tmp"
    : > "$STATEDIR/outbox.txt"
  fi
  # budget mirror: count TEST_PAIR / TEST_RANK requests since arm start
  NTEST=$(tail -n +"$START_LINES" "$STATEDIR/proto.log" | grep -c "^> TEST_" || true)
  if [ "$NTEST" -gt "$BUDGET" ]; then
    echo "BUDGET_HIT arm=$ARM ntest=$NTEST budget=$BUDGET" >> "$STATEDIR/proto.log"
    exit 1
  fi
done
echo "ITERATION CAP arm=$ARM" >> "$STATEDIR/proto.log"
exit 1
