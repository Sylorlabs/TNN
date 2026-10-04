#!/bin/bash
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
DRIVER="$HERE/../zag_driver_bin"
WORLDS="/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/c1_clean/worlds"
C1BIN="/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/c1_clean/contestant_bin"
BASE="/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/c1_baseline"
OUT="$HERE/runs"

run_one() {
  local name=$1 bin=$2 world=$3 rep=$4
  local d="$OUT/${name}_${world}_r${rep}"
  if [ -f "$d/costs.txt" ]; then echo "skip $name $world r$rep (done)"; return; fi
  rm -rf "$d"; mkdir -p "$d"
  "$DRIVER" "$WORLDS/$world" "$bin" "$d" > "$d/driver.log" 2>&1
  echo "done $name $world r$rep: $(grep 'queries=' "$d/costs.txt" | head -1)"
}
export -f run_one
export HERE DRIVER WORLDS C1BIN BASE OUT

JOBS=""
for w in h0 h1; do
  for r in 1 2 3; do
    JOBS="$JOBS c1:$C1BIN:$w:$r mem:$BASE/mem_bin:$w:$r freq:$BASE/freq_bin:$w:$r rand:$BASE/rand_bin:$w:$r"
  done
done
echo "$JOBS" | tr ' ' '\n' | grep -v '^$' | xargs -P 4 -I {} bash -c '
  IFS=":" read -r name bin world rep <<< "{}"
  run_one "$name" "$bin" "$world" "$rep"
'
echo ALL-DONE
