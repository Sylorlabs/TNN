#!/bin/bash
# Sealed DAG-world driver for TRADES-DAG (dev).
# Bash sequences process invocations ONLY; all causal logic is pure Zag.
# Usage: run_dag.sh <worlddir> <binary> <outdir>
# The worlddir holds pre.jsonl, int_table.tsv, key.json (key.json is
# chmod 000 before the agent runs; the agent never opens it).
# int_table.tsv columns: t k o0 o1 o2 o3 (uniform 4 outcome columns).
set -u
W="$1"
BIN="$2"
R="$3"
[ -x "$BIN" ] || { echo "missing binary: $BIN"; exit 1; }
[ -f "$W/pre.jsonl" ] || { echo "missing pre.jsonl"; exit 1; }
[ -f "$W/int_table.tsv" ] || { echo "missing int_table.tsv"; exit 1; }
mkdir -p "$R/state"
rm -rf "$R/state" && mkdir -p "$R/state"
> "$R/replies.jsonl"
> "$R/trace.txt"
chmod 000 "$W/key.json"
n=0
# phase 1: pre turns (cbrief + 12 cobs)
while IFS= read -r line; do
  echo "$line" > "$R/turn.json"
  "$BIN" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" 2>> "$R/trace.txt" || { echo "agent failed at pre turn $n"; exit 1; }
  n=$((n+1))
done < "$W/pre.jsonl"
# read n_traces from the cbrief reply
NT=$(grep -o '"kind":"cbrief"[^}]*' "$R/replies.jsonl" | head -1 | grep -o '"n_traces":[0-9]*' | grep -o '[0-9]*')
[ -n "$NT" ] || { echo "no n_traces in cbrief reply"; exit 1; }
echo "n_traces=$NT"
# phase 2: 3 rounds x NT traces of choose_int / int_result
r=1
while [ $r -le 3 ]; do
  t=0
  while [ $t -lt "$NT" ]; do
    echo "{\"turn\":$n,\"kind\":\"choose_int\",\"trace\":$t,\"round\":$r}" > "$R/turn.json"
    "$BIN" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" 2>> "$R/trace.txt" || { echo "agent failed at choose r=$r t=$t"; exit 1; }
    K=$(tail -1 "$R/replies.jsonl" | grep -o '"k":[0-9]*' | grep -o '[0-9]*')
    [ -n "$K" ] || { echo "no k in choose_int reply r=$r t=$t"; exit 1; }
    read -r o0 o1 o2 o3 < <(awk -v t="$t" -v k="$K" '$1==t && $2==k {print $3, $4, $5, $6}' "$W/int_table.tsv")
    [ -n "$o0" ] || { echo "no outcome for t=$t k=$K"; exit 1; }
    echo "{\"turn\":$n,\"kind\":\"int_result\",\"trace\":$t,\"k\":$K,\"x\":$o0,\"y\":$o1,\"z\":$o2,\"w\":$o3}" > "$R/turn.json"
    n=$((n+1))
    "$BIN" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" 2>> "$R/trace.txt" || { echo "agent failed at result r=$r t=$t"; exit 1; }
    n=$((n+1))
    t=$((t+1))
  done
  r=$((r+1))
done
# phase 3: ctest + cdone
echo "{\"turn\":$n,\"kind\":\"ctest\"}" > "$R/turn.json"
"$BIN" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" 2>> "$R/trace.txt" || { echo "agent failed at ctest"; exit 1; }
n=$((n+1))
echo "{\"turn\":$n,\"kind\":\"cdone\"}" > "$R/turn.json"
"$BIN" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" 2>> "$R/trace.txt" || { echo "agent failed at cdone"; exit 1; }
n=$((n+1))
chmod 644 "$W/key.json"
echo "run complete: $n turns"
