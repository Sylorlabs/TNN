#!/bin/bash
# run_dev.sh - dev-run driver for TCNP (ARENA lane, wave-20261001-2021pdt).
# Dev-only: practice worlds in /tmp (contaminated by construction), never
# sealed, never counted toward any bar. Bash sequences process invocations
# ONLY; all logic is in the pinned-znc-built Zag binaries.
# Usage: run_dev.sh <binary> <rundir>
#   <binary>: tcn_p | tcn_p_ablated | tcn_p_memctrl
#   <rundir>: fresh output dir (created)
set -u
LANE="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA"
BIN="$LANE/bin/$1"
R="$2"
DEV="/tmp/tcn_p_dev"
[ -x "$BIN" ] || { echo "missing binary: $BIN"; exit 1; }
[ -f "$DEV/turns.jsonl" ] || { echo "missing dev worlds; run gen_devworlds first"; exit 1; }
mkdir -p "$R/state"
> "$R/replies.jsonl"
> "$R/trace.log"
n=0
while IFS= read -r line; do
  echo "$line" > "$R/turn.json"
  "$BIN" "$R/turn.json" "$R/state" "$DEV" >> "$R/replies.jsonl" 2>> "$R/trace.log" || { echo "binary failed at turn $n"; exit 1; }
  n=$((n+1))
  if tail -1 "$R/replies.jsonl" | grep -q '"done":true'; then break; fi
done < "$DEV/turns.jsonl"
echo "run done: $n turns -> $R"
