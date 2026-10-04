#!/bin/bash
# run_k4.sh - K4 no-regression self-check (ARENA lane, wave-20261001-2021pdt).
# Rebuilds world_gen + arena from COMMITTED sources, regenerates the
# deterministic sealed 68-item world (seed 71503461337030, inside
# world_gen.zag), runs the NEW contestant binary (tcn_p) over all turns,
# and scores with the arena scorer. Expected: per-capability scores
# byte-identical to the v6 refreeze baseline (54/68 = 0.794).
# Bash sequences process invocations ONLY. Pure Zag otherwise.
set -u
SRC="/home/hatch/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/competitive_arena"
LANE="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA"
B="/tmp/k4bin"
W="/tmp/k4world"
R="/tmp/k4run"
mkdir -p "$B" "$W" "$R/state"
echo "== building world_gen + arena from committed sources =="
znc "$SRC/world_gen.zag" -o "$B/world_gen" 2>/dev/null || { echo "world_gen build failed"; exit 1; }
znc "$SRC/arena.zag" -o "$B/arena" 2>/dev/null || { echo "arena build failed"; exit 1; }
echo "world_gen sha256: $(sha256sum "$B/world_gen" | cut -d' ' -f1)"
echo "arena sha256:     $(sha256sum "$B/arena" | cut -d' ' -f1)"
echo "expected:         c4c8340c818e6848c88e34f1989bf382ff097c69a71d6621c6bf28b58dc85211"
echo "expected:         3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076"
echo "== generating sealed world (deterministic seed) =="
"$B/world_gen" "$W" || { echo "world_gen run failed"; exit 1; }
echo "turns.jsonl sha256: $(sha256sum "$W/turns.jsonl" | cut -d' ' -f1)"
echo "expected:            0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469"
echo "== running new contestant binary =="
rm -rf "$R/state" && mkdir -p "$R/state"
> "$R/replies.jsonl"
> "$R/trace.log"
n=0
while IFS= read -r line; do
  echo "$line" > "$R/turn.json"
  "$LANE/bin/tcn_p" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" 2>> "$R/trace.log" || { echo "contestant failed at turn $n"; exit 1; }
  n=$((n+1))
  if tail -1 "$R/replies.jsonl" | grep -q '"done":true'; then break; fi
done < "$W/turns.jsonl"
echo "k4 run: $n turns completed"
echo "trace lines (should be empty; no pshow/ptest in this battery): $(wc -l < "$R/trace.log")"
echo "== scoring =="
"$B/arena" score "$W" "$R/replies.jsonl" "$R" || { echo "scoring failed"; exit 1; }
