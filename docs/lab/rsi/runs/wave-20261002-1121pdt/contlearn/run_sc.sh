#!/bin/sh
# run_sc.sh -- frozen run procedure for the scheduling exercise (b).
# 4 binaries x 3 reps = 12 runs. Empty argv/env via `bash -c 'exec -c'`.
set -u
export PATH="$HOME/safebin"
D="/home/hatch/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn"
cd "$D"
LOGCOUNT_BEFORE=$(wc -l < znc_invocations_sc.log)
for bin in sc_treat_a sc_treat_b sc_costume_a sc_costume_b; do
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
LOGCOUNT_AFTER=$(wc -l < znc_invocations_sc.log)
echo "ZNCLLOG before=$LOGCOUNT_BEFORE after=$LOGCOUNT_AFTER"
