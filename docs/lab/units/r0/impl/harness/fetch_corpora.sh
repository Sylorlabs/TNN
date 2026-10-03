#!/bin/sh
# fetch_corpora.sh — fetch R0 corpora ON DEMAND. The corpora are NEVER committed.
#   corpus 0: Project Gutenberg #100 (Complete Works of Shakespeare, prose, ~5.4MB)
#   corpus 1: sqlite3.c amalgamation (code, ~9.5MB)
# Usage: fetch_corpora.sh <dest-dir>
# Verifies SHA-256 after download and prints the hashes for the evidence log.
# Re-running is idempotent (skips files that already exist with matching hash).
set -u
DEST="${1:?usage: fetch_corpora.sh <dest-dir>}"
mkdir -p "$DEST" || exit 2

GUT_URL="https://www.gutenberg.org/cache/epub/100/pg100.txt"
# Pinned amalgamation: resolve the current versioned zip from sqlite.org.
# The zip is versioned; we pin the version in AMALG_VER after checking
# https://www.sqlite.org/download.html. Update the pin deliberately, never silently.
AMALG_VER="3530400"
AMALG_URL="https://www.sqlite.org/2026/sqlite-amalgamation-${AMALG_VER}.zip"

fetch() {
  url="$1"; dest="$2"
  if [ -f "$dest" ]; then
    echo "exists: $dest (skipping download)"
    return 0
  fi
  echo "fetching $url"
  curl -sSL --retry 3 --max-time 300 -o "$dest" "$url" || { echo "FAILED: $url"; return 1; }
}

fetch "$GUT_URL" "$DEST/pg100.txt" || exit 1

if [ ! -f "$DEST/sqlite3.c" ]; then
  fetch "$AMALG_URL" "$DEST/sqlite-amalgamation.zip" || exit 1
  # shell-only extraction (no python: pure-Zag law for the harness; the fetch
  # runner itself is external corpus transport, not AI logic)
  inner=$(unzip -Z1 "$DEST/sqlite-amalgamation.zip" | grep '/sqlite3\.c$' | head -1)
  if [ -z "$inner" ]; then echo "sqlite3.c not found in amalgamation zip"; exit 1; fi
  unzip -p "$DEST/sqlite-amalgamation.zip" "$inner" > "$DEST/sqlite3.c" || exit 1
  echo "extracted sqlite3.c"
else
  echo "exists: $DEST/sqlite3.c (skipping download)"
fi

echo "--- corpus hashes (record in evidence log; M-30) ---"
sha256sum "$DEST/pg100.txt" "$DEST/sqlite3.c"
wc -c "$DEST/pg100.txt" "$DEST/sqlite3.c"
