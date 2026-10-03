#!/bin/sh
# run_xk.sh -- frozen run procedure for the cross-kind rebind (c).
# 2 binaries x 3 reps = 6 runs. Empty argv/env via `bash -c 'exec -c'`.
set -u
export PATH="$HOME/safebin"
D="/home/hatch/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn"
cd "$D"
LOGCOUNT_BEFORE=$(wc -l < znc_invocations_xk.log)
for bin in xk_full xk_nophase; do
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
LOGCOUNT_AFTER=$(wc -l < znc_invocations_xk.log)
echo "ZNCLLOG before=$LOGCOUNT_BEFORE after=$LOGCOUNT_AFTER"
