#!/bin/sh
# fetch_gutenberg_100.sh — on-demand fetch of Project Gutenberg #100
# (The Complete Works of William Shakespeare) for TNN Track B curriculum.
#
# PROVENANCE: public domain. Shakespeare died 1616; the Project Gutenberg
# edition is public domain in the United States (see PROVENANCE.md).
#
# The corpus is NEVER committed to the repo (prereg §1.12 / C-T freeze note).
# It is fetched on demand into $CORPUS_DIR (default /tmp/tnn-corpora) and the
# builder verifies byte length + SHA-256 against the pinned values in
# PROVENANCE.md before any slice is built. A hash mismatch aborts the build.
#
# Determinism: the file is used byte-for-byte as served; no normalization.
set -eu
CORPUS_DIR="${CORPUS_DIR:-/tmp/tnn-corpora}"
URL="${GUTENBERG_100_URL:-https://www.gutenberg.org/cache/epub/100/pg100.txt}"
OUT="$CORPUS_DIR/pg100.txt"
mkdir -p "$CORPUS_DIR"
if [ -f "$OUT" ]; then
  echo "exists: $OUT (delete to re-fetch)"
else
  echo "fetching $URL"
  curl -sSL --retry 3 --max-time 300 -o "$OUT" "$URL"
fi
wc -c "$OUT"
sha256sum "$OUT"
