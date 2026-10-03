#!/bin/sh
# run_ow.sh -- CONTLEARN-OWNED2 discrimination harness (K1a/K1c/K6).
# 2 binaries x 3 reps = 6 learner processes. Each run: one process for the
# full 104-event script, empty argv, empty environment
# (`bash -c 'exec -c'`, since `env` is not linked in safebin).
# Stdout -> transcript_<mode>_r<rep>.txt ; stderr -> stderr_<mode>_r<rep>.txt
# (must stay 0 bytes). PIDs go only to harness_ow.log, never to transcripts.
LANE="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED2"
cd "$LANE" || exit 1
: > harness_ow.log
nspawn=0
run_one() {
  mode="$1"; rep="$2"; bin="$3"
  out="transcript_${mode}_r${rep}.txt"
  err="stderr_${mode}_r${rep}.txt"
  PATH="$HOME/safebin" bash -c "exec -c ./$bin" > "$out" 2> "$err" &
  pid=$!
  nspawn=$((nspawn+1))
  echo "spawn mode=$mode rep=$rep pid=$pid count=$nspawn" >> harness_ow.log
  wait "$pid"
  rc=$?
  echo "exit mode=$mode rep=$rep rc=$rc" >> harness_ow.log
  if [ "$rc" -ne 0 ]; then echo "NONZERO_EXIT mode=$mode rep=$rep rc=$rc" >> harness_ow.log; fi
  if [ -s "$err" ]; then echo "STDERR_NONEMPTY mode=$mode rep=$rep bytes=$(wc -c < "$err")" >> harness_ow.log; fi
}
for rep in 1 2 3; do
  run_one "TREAT" "$rep" "ow_driver_treat"
  run_one "CONTROL" "$rep" "ow_driver_control"
done
echo "total_spawns=$nspawn want=6" >> harness_ow.log
for mode in TREAT CONTROL; do
  c=$(grep -c "spawn mode=$mode " harness_ow.log)
  echo "assert mode=$mode spawns=$c want=3" >> harness_ow.log
done
pids=$(grep "^spawn" harness_ow.log | sed 's/.*pid=//;s/ .*//')
leak=0
for t in transcript_*.txt; do
  for p in $pids; do
    if grep -q "$p" "$t" 2>/dev/null; then echo "PID_LEAK file=$t pid=$p" >> harness_ow.log; leak=1; fi
  done
done
echo "pid_leak_check=$leak" >> harness_ow.log
echo "znc_invocations_during_runs=$(wc -l < znc_invocations_ow.log)" >> harness_ow.log
