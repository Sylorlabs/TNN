#!/bin/sh
# fetch_corpora_prose.sh — EXPLORATORY (NOT EVIDENCE) corpus fetcher for the
# TNN representation program, wide-exploration track.
#
# Fetches 6 additional public-domain prose corpora from Project Gutenberg
# ON DEMAND. Corpora are NEVER committed to the repo (same rule as the frozen
# Shakespeare/sqlite3.c pipeline). Deterministic: each file is verified against
# its pinned SHA-256; any mismatch aborts.
#
# Usage: ./fetch_corpora_prose.sh <dest-dir>
# Exit 0 when all 6 files are present and hash-verified.
set -eu

DEST="${1:-/tmp/wide_prose}"
mkdir -p "$DEST"

# id | filename | sha256 (of the fetched bytes, recorded 2026-09-21)
fetch_one() {
  id="$1"; file="$2"; want="$3"
  url="https://www.gutenberg.org/cache/epub/${id}/${file}"
  out="${DEST}/${file}"
  if [ -f "$out" ]; then
    echo "exists: $out"
  else
    echo "fetch: $url"
    curl -fsSL --retry 3 --max-time 120 -o "$out" "$url"
  fi
  got="$(sha256sum "$out" | cut -d' ' -f1)"
  if [ "$got" != "$want" ]; then
    echo "HASH MISMATCH for $out: got $got want $want" >&2
    exit 1
  fi
  echo "ok: $out ($(wc -c < "$out") bytes, sha256 verified)"
}

fetch_one 3207 pg3207.txt  3de1e492641d939567a8b0de827fb13e1ad992324f9ac8b204f60475009b7294
fetch_one 84   pg84.txt    7810cd483cffcf2cc8a1d8f0d5807931e69d4f48cd14149b8c76f88af82fead3
fetch_one 98   pg98.txt    d54c2b80d40a40b982cd88852c6180bb944d95acdb028af3d0e01a1750681784
fetch_one 1661 pg1661.txt  922e2a12ccb43a4c9544c260b2166c6ad2097aeb5957faeee113f173bb857cd0
fetch_one 35   pg35.txt    2892e919000e17c83e1dac51b30f4675db50536b644d7579fe8a89bb399a9bdc
fetch_one 2010 pg2010.txt  7e2937e414d27ec2ee9bced09e1f9066191732aeaa15cc44ad9d85d687d8d00b

echo "ALL 6 EXPLORATORY PROSE CORPORA FETCHED AND VERIFIED -> $DEST"
