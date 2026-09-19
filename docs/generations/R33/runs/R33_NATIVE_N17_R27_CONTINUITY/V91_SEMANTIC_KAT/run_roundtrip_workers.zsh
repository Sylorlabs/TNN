#!/bin/zsh
set -u
setopt PIPE_FAIL

EMIT=${1:?emit binary}
ROOT=${2:?input root}
CF=${3:?condition frame}
OUT=${4:?fresh output directory}

[[ ! -e "$OUT" ]] || exit 60
mkdir -p "$OUT" || exit 61

typeset -a pids
for i in {0..15}; do
  "$EMIT" "$ROOT" "$CF" "$i" "$OUT/row_$i.bin" >"$OUT/row_$i.stdout" 2>"$OUT/row_$i.stderr" &
  pids+=($!)
done

rc=0
for p in $pids; do
  wait $p || rc=1
done

for i in {0..15}; do
  [[ -s "$OUT/row_$i.bin" ]] || rc=1
  [[ -s "$OUT/row_$i.stderr" ]] && rc=1
  cat "$OUT/row_$i.stdout"
done
exit $rc
