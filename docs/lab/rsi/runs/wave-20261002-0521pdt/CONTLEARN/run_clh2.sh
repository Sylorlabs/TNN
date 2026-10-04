#!/bin/sh
# run_clh2.sh -- CLH2 sealed harness (K1a/K1c/CP-R6).
# 3 binaries x 3 reps = 9 learner processes. Each run: one process for the
# full script, empty argv, empty environment
# (`bash -c 'exec -c'`, since `env` is not linked in safebin).
# Stdout -> transcript_<mode>_r<rep>.txt ; stderr -> stderr_<mode>_r<rep>.txt
# (must stay 0 bytes). PIDs go only to harness_clh2.log, never to transcripts.
LANE="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN"
cd "$LANE" || exit 1
: > harness_clh2.log
nspawn=0
run_one() {
  mode="$1"; rep="$2"; bin="$3"
  out="transcript_${mode}_r${rep}.txt"
  err="stderr_${mode}_r${rep}.txt"
  PATH="$HOME/safebin" bash -c "exec -c ./$bin" > "$out" 2> "$err" &
  pid=$!
  nspawn=$((nspawn+1))
  echo "spawn mode=$mode rep=$rep pid=$pid count=$nspawn" >> harness_clh2.log
  wait "$pid"
  rc=$?
  echo "exit mode=$mode rep=$rep rc=$rc" >> harness_clh2.log
  if [ "$rc" -ne 0 ]; then echo "NONZERO_EXIT mode=$mode rep=$rep rc=$rc" >> harness_clh2.log; fi
  if [ -s "$err" ]; then echo "STDERR_NONEMPTY mode=$mode rep=$rep bytes=$(wc -c < "$err")" >> harness_clh2.log; fi
}
for rep in 1 2 3; do
  run_one "TREAT" "$rep" "clh2_treat"
  run_one "CONTROL" "$rep" "clh2_control"
  run_one "NOPHASE" "$rep" "clh2_nophase"
done
echo "total_spawns=$nspawn want=9" >> harness_clh2.log
