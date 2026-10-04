#!/bin/bash
# Sealed evaluation driver for Arena ROSTER (wave-20261001-2321pdt, ARENA4 lane).
# Runs the frozen ROSTER contestant over the sealed 68-item battery.
# Bash sequences process invocations ONLY; all arena logic is pure Zag.
# Usage: run_sealed.sh <run#> <binary>
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
B="$HERE/sealed/bin"
W="$HERE/sealed/world"
R="$HERE/sealed/run$1"
ROSTER="$2"
for f in "$B/arena" "$ROSTER"; do
  [ -x "$f" ] || { echo "missing binary: $f"; exit 1; }
done
rm -rf "$R/state" && mkdir -p "$R/state"
> "$R/replies.jsonl"
n=0
while IFS= read -r line; do
  echo "$line" > "$R/turn.json"
  "$ROSTER" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" 2>/dev/null || { echo "contestant failed at turn $n"; exit 1; }
  n=$((n+1))
  if tail -1 "$R/replies.jsonl" | grep -q '"done":true'; then break; fi
done < "$W/turns.jsonl"
echo "run $1: $n turns completed"
echo "== scoring =="
"$B/arena" score "$W" "$R/replies.jsonl" "$R" || { echo "scoring failed"; exit 1; }
