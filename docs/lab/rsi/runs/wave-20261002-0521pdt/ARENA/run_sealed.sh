#!/bin/bash
# Sealed evaluation driver for the C9 causal contestant
# (wave-20261002-0521pdt, ARENA lane, frozen PREREG_CAUSAL).
# Bash sequences process invocations ONLY; all arena logic is pure Zag.
# Usage: run_sealed.sh <rundir> <contestant-binary> <worlddir>
set -u
R="$1"; INQ="$2"; W="$3"
for f in "$INQ"; do [ -x "$f" ] || { echo "missing binary: $f"; exit 1; }; done
[ -f "$W/turns.jsonl" ] || { echo "missing world: $W"; exit 1; }
mkdir -p "$R/state"
rm -rf "$R/state" && mkdir -p "$R/state"
> "$R/replies.jsonl"
> "$R/trace.txt"
n=0
while IFS= read -r line; do
  echo "$line" > "$R/turn.json"
  "$INQ" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" 2>> "$R/trace.txt" || { echo "contestant failed at turn $n"; exit 1; }
  n=$((n+1))
  if tail -1 "$R/replies.jsonl" | grep -q '"done":true'; then break; fi
done < "$W/turns.jsonl"
echo "run: $n turns completed"
echo "== scoring =="
"$(dirname "$0")/bin/arena_512" score "$W" "$R/replies.jsonl" "$R" || { echo "scoring failed"; exit 1; }
