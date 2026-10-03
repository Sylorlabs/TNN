#!/bin/sh
# run_rj.sh -- frozen run procedure for the refusal exercise (a).
# 4 binaries x 3 reps = 12 runs. Empty argv and empty env per run via
# `bash -c 'exec -c'` (exec replaces the shell: exactly 1 process per run).
# Captures stdout, stderr (0-byte file each), and the rc per run.
# The znc invocation log must gain 0 entries during the runs (K1b).
set -u
export PATH="$HOME/safebin"
D="/home/hatch/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn"
cd "$D"
LOGCOUNT_BEFORE=$(wc -l < znc_invocations_rj.log)
for bin in rj_own_x rj_own_y rj_hard_x rj_hard_y; do
  r=1
  while [ $r -le 3 ]; do
    out="out_${bin}_r${r}.txt"
    err="err_${bin}_r${r}.txt"
    : > "$err"
    PATH="$HOME/safebin" bash -c "exec -c ./$bin" > "$out" 2>"$err"
    rc=$?
    echo "$bin rep $r rc=$rc out_bytes=$(wc -c < "$out") err_bytes=$(wc -c < "$err") sha=$(sha256sum < "$out" | cut -d' ' -f1)"
    r=$((r+1))
  done
done
LOGCOUNT_AFTER=$(wc -l < znc_invocations_rj.log)
echo "ZNCLLOG before=$LOGCOUNT_BEFORE after=$LOGCOUNT_AFTER"
