#!/bin/sh
# run.sh -- CONTLEARN learner-ownership probe harness (K1a/K1c/K6).
# 2 modes x 3 reps = 6 learner processes. Each run: mode token on stdin
# (driver-side only, never reaches cognition), empty argv, empty environment
# (phase-free; `env` is not linked in safebin, so `bash -c 'exec -c'` is used
# to launch with a fully empty env).
# Stdout -> transcript_<mode>_r<rep>.txt ; stderr -> stderr_<mode>_r<rep>.txt
# (must stay 0 bytes). PIDs go only to harness.log, never to transcripts.
LANE="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN"
cd "$LANE" || exit 1
: > harness.log
nspawn=0
run_one() {
  mode="$1"; rep="$2"
  out="transcript_${mode}_r${rep}.txt"
  err="stderr_${mode}_r${rep}.txt"
  printf '%s' "$mode" | PATH="$HOME/safebin" bash -c 'exec -c ./lo_driver' > "$out" 2> "$err" &
  pid=$!
  nspawn=$((nspawn+1))
  echo "spawn mode=$mode rep=$rep pid=$pid count=$nspawn" >> harness.log
  wait "$pid"
  rc=$?
  echo "exit mode=$mode rep=$rep rc=$rc" >> harness.log
  if [ "$rc" -ne 0 ]; then echo "NONZERO_EXIT mode=$mode rep=$rep rc=$rc" >> harness.log; fi
  if [ -s "$err" ]; then echo "STDERR_NONEMPTY mode=$mode rep=$rep bytes=$(wc -c < "$err")" >> harness.log; fi
}
for rep in 1 2 3; do
  for mode in TREAT NOSTORE; do
    run_one "$mode" "$rep"
  done
done
echo "total_spawns=$nspawn want=6" >> harness.log
for mode in TREAT NOSTORE; do
  c=$(grep -c "spawn mode=$mode " harness.log)
  echo "assert mode=$mode spawns=$c want=3" >> harness.log
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
