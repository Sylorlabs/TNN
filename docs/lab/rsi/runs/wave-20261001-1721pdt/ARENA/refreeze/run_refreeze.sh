#!/bin/bash
# Refreeze driver for Arena v6 (wave-20261001-1721pdt, ARENA lane).
# Runs the full frozen Arena battery against the hash-verified v6 binary
# exactly per PREREG_LANGUAGE.md + PREREG_LANGUAGE_AMEND1.md (1421pdt lane).
# Bash sequences process invocations ONLY; all arena logic is pure Zag.
# The committed competitive_arena sources are NEVER modified.
# Binaries in sealed/bin are hash-verified against the canonical 1421pdt
# sealed binaries (see REFREEZE_RECORD.md); they are NOT rebuilt here.
# Usage: run_refreeze.sh <run#>  (run# = 1, 2, 3)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
B="$HERE/sealed/bin"
W="$HERE/sealed/run$1/world"
R="$HERE/sealed/run$1/pilot"
V6="$B/v6_refreeze"
mkdir -p "$W" "$R/state"
for f in "$B/world_gen" "$B/arena" "$V6"; do
  [ -x "$f" ] || { echo "missing binary: $f"; exit 1; }
done
echo "== world generation (deterministic seed inside world_gen.zag) =="
"$B/world_gen" "$W" || { echo "world_gen run failed"; exit 1; }
echo "== contestant run $1 =="
rm -rf "$R/state" && mkdir -p "$R/state"
> "$R/replies.jsonl"
n=0
while IFS= read -r line; do
  echo "$line" > "$R/turn.json"
  "$V6" "$R/turn.json" "$R/state" "$W" >> "$R/replies.jsonl" || { echo "contestant failed at turn $n"; exit 1; }
  n=$((n+1))
  if tail -1 "$R/replies.jsonl" | grep -q '"done":true'; then break; fi
done < "$W/turns.jsonl"
echo "run $1: $n turns completed"
echo "== scoring =="
"$B/arena" score "$W" "$R/replies.jsonl" "$R" || { echo "scoring failed"; exit 1; }
