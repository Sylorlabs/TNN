#!/bin/bash
# dump_chunked.sh — wrapper for dump.zag that handles large inputs via chunking.
# The dump's single read() doesn't guarantee full file read; split into
# 2000-line chunks to avoid the issue.
# Usage: dump_chunked.sh <input.tsv> <base_dir> <output.tsv>
set -e
INPUT="$1"
BASE="$2"
OUTPUT="$3"
DUMP_BIN="$(dirname "$0")/../src/dump"
TMPDIR="${TMPDIR:-/tmp}/dump_chunks_$$"
mkdir -p "$TMPDIR"
split -l 2000 "$INPUT" "$TMPDIR/chunk_"
for c in "$TMPDIR"/chunk_*; do
    bn=$(basename "$c")
    "$DUMP_BIN" "$c" "$BASE" "$TMPDIR/out_${bn}.tsv" 2>&1 | tail -1 >&2
done
cat "$TMPDIR"/out_*.tsv > "$OUTPUT"
rm -rf "$TMPDIR"
echo "wrote $OUTPUT" >&2
