#!/bin/bash
# Sealed arena evaluation for the language lane (v6 contestant).
# Bash sequences process invocations ONLY; all arena logic (world generation,
# contestant cognition, scoring) is pure Zag via the pinned znc.
# The committed competitive_arena sources are NEVER modified.
# Usage: run_sealed.sh <run#>   (run# = 1, 2, 3 for the determinism bar)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ARENA=/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/competitive_arena
ZNC=/home/hatch/safebin/znc
RUN="${1:-1}"
B="$HERE/sealed/bin"
W="$HERE/sealed/run$RUN/world"
R="$HERE/sealed/run$RUN/pilot"
mkdir -p "$B" "$W" "$R/state"
echo "== building (pinned znc, unmodified arena sources) =="
"$ZNC" "$ARENA/world_gen.zag" -o "$B/world_gen" 2>/dev/null || { echo "world_gen build failed"; exit 1; }
"$ZNC" "$ARENA/arena.zag" -o "$B/arena" 2>/dev/null || { echo "arena build failed"; exit 1; }
"$ZNC" "$HERE/devint1_contestant_v6.zag" -o "$B/v6" 2>/dev/null || { echo "v6 build failed"; exit 1; }
echo "== world generation (deterministic seed inside world_gen.zag) =="
"$B/world_gen" "$W" || { echo "world_gen run failed"; exit 1; }
echo "== contestant run $RUN =="
rm -rf "$R/state" && mkdir -p "$R/state"
> "$R/replies.jsonl"
n=0
while IFS= read -r line; do
  echo "$line" > "$R/turn.json"
  "$B/v6" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" || { echo "contestant failed at turn $n"; exit 1; }
  n=$((n+1))
  if tail -1 "$R/replies.jsonl" | grep -q '"done":true'; then break; fi
done < "$W/turns.jsonl"
echo "run $RUN: $n turns completed"
echo "== scoring =="
"$B/arena" score "$W" "$R/replies.jsonl" "$R" || { echo "scoring failed"; exit 1; }
