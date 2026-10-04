#!/bin/bash
# CA-1 pilot driver. Bash sequences process invocations ONLY; all arena
# logic (world generation, contestant cognition, scoring) is pure Zag.
# Usage: run_arena.sh <competitive_arena dir>
set -u
A="$1"
W="$A/world"
R="$A/pilot_run"
ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
B=/tmp/ca1bin
mkdir -p "$B" "$W" "$R/state"
echo "== building =="
"$ZNC" "$A/world_gen.zag" -o "$B/world_gen" 2>/dev/null || { echo "world_gen build failed"; exit 1; }
"$ZNC" "$A/tnn_contestant.zag" -o "$B/tnn_contestant" 2>/dev/null || { echo "contestant build failed"; exit 1; }
"$ZNC" "$A/arena.zag" -o "$B/arena" 2>/dev/null || { echo "arena build failed"; exit 1; }
echo "== world generation + determinism check =="
"$B/world_gen" "$W" || { echo "world_gen run failed"; exit 1; }
mkdir -p "$B/wdet" && "$B/world_gen" "$B/wdet" >/dev/null || exit 1
for f in "$W"/*; do
  fn=$(basename "$f")
  cmp -s "$f" "$B/wdet/$fn" || { echo "NONDETERMINISM in $fn"; exit 1; }
done
echo "determinism: all world artifacts byte-identical across 2 runs"
echo "== TNN pilot =="
rm -rf "$R/state" && mkdir -p "$R/state"
> "$R/replies.jsonl"
n=0
while IFS= read -r line; do
  echo "$line" > "$R/turn.json"
  "$B/tnn_contestant" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" || { echo "contestant failed at turn $n"; exit 1; }
  n=$((n+1))
  if tail -1 "$R/replies.jsonl" | grep -q '"done":true'; then break; fi
done < "$W/turns.jsonl"
echo "pilot: $n turns completed"
echo "== scoring =="
"$B/arena" score "$W" "$R/replies.jsonl" "$R" || { echo "scoring failed"; exit 1; }
