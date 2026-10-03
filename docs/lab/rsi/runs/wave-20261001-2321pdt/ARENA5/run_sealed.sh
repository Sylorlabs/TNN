#!/bin/bash
# Sealed evaluation driver for ARENA5 DEFRECALL (wave-20261001-2321pdt).
# Bash sequences process invocations ONLY; all arena logic is pure Zag.
# Usage: run_sealed.sh <runname> <binary>
set -u
HERE="/tmp/arena5_work"
B="$HERE/sealed/bin"
W="$HERE/sealed/world"
R="$HERE/sealed/$1"
BIN="$2"
mkdir -p "$B" "$R/state"
cp "$HERE/arena_fresh" "$B/arena" 2>/dev/null; chmod +x "$B/arena"
[ -x "$B/arena" ] || { echo "missing arena"; exit 1; }
[ -x "$BIN" ] || { echo "missing binary: $BIN"; exit 1; }
rm -rf "$R/state" && mkdir -p "$R/state"
> "$R/replies.jsonl"
n=0
while IFS= read -r line; do
  echo "$line" > "$R/turn.json"
  "$BIN" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" 2>/dev/null || { echo "contestant failed at turn $n"; exit 1; }
  n=$((n+1))
  if tail -1 "$R/replies.jsonl" | grep -q '"done":true'; then break; fi
done < "$W/turns.jsonl"
echo "run $1: $n turns completed"
echo "== scoring =="
"$B/arena" score "$W" "$R/replies.jsonl" "$R" || { echo "scoring failed"; exit 1; }
