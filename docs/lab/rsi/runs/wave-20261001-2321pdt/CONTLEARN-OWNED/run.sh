#!/bin/sh
# run.sh -- CONTLEARN-OWNED discrimination harness (K1a/K1c/CO-3).
# 2 binaries (ow_treat = machinery-disabled variant, ow_control = frozen
# core) x 3 reps = 6 learner processes. Each run: mode token on stdin
# (driver-side label only, never reaches cognition), empty argv, empty
# environment (`bash -c 'exec -c'`; `env` is not linked in safebin).
# Stdout -> transcript_<bin>_<mode>_r<rep>.txt ; stderr -> stderr_*.txt
# (must stay 0 bytes). PIDs go only to harness.log, never to transcripts.
LANE="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED"
cd "$LANE" || exit 1
: > harness.log
nspawn=0
run_one() {
  bin="$1"; mode="$2"; rep="$3"
  out="transcript_${bin}_${mode}_r${rep}.txt"
  err="stderr_${bin}_${mode}_r${rep}.txt"
  printf '%s' "$mode" | PATH="$HOME/safebin" bash -c "exec -c ./$bin" > "$out" 2> "$err" &
  pid=$!
  nspawn=$((nspawn+1))
  echo "spawn bin=$bin mode=$mode rep=$rep pid=$pid count=$nspawn" >> harness.log
  wait "$pid"
  rc=$?
  echo "exit bin=$bin mode=$mode rep=$rep rc=$rc" >> harness.log
  if [ "$rc" -ne 0 ]; then echo "NONZERO_EXIT bin=$bin mode=$mode rep=$rep rc=$rc" >> harness.log; fi
  if [ -s "$err" ]; then echo "STDERR_NONEMPTY bin=$bin mode=$mode rep=$rep bytes=$(wc -c < "$err")" >> harness.log; fi
}
for rep in 1 2 3; do
  run_one ow_treat TREAT "$rep"
  run_one ow_control CONTROL "$rep"
done
echo "total_spawns=$nspawn want=6" >> harness.log
for b in ow_treat ow_control; do
  c=$(grep -c "spawn bin=$b " harness.log)
  echo "assert bin=$b spawns=$c want=3" >> harness.log
done
pids=$(grep "^spawn" harness.log | sed 's/.*pid=//;s/ .*//')
leak=0
for t in transcript_*.txt; do
  for p in $pids; do
    if grep -q "$p" "$t" 2>/dev/null; then echo "PID_LEAK file=$t pid=$p" >> harness.log; leak=1; fi
  done
done
echo "pid_leak_check=$leak" >> harness.log
echo "znc_invocations_during_runs=$(wc -l < znc_invocations.log)" >> harness.log
