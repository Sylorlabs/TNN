#!/bin/sh
# fetch_sqlite_amalgamation.sh — on-demand fetch of the SQLite 3.53.4
# amalgamation (sqlite3.c) for TNN Track B curriculum.
#
# PROVENANCE: public domain. SQLite is dedicated to the public domain by its
# authors (see PROVENANCE.md; https://www.sqlite.org/copyright.html).
#
# The corpus is NEVER committed to the repo. It is fetched on demand into
# $CORPUS_DIR (default /tmp/tnn-corpora); only sqlite3.c is extracted. The
# builder verifies byte length + SHA-256 of sqlite3.c against the pinned values
# in PROVENANCE.md before any slice is built. A hash mismatch aborts the build.
#
# Determinism: sqlite3.c is used byte-for-byte as shipped in the zip; the zip
# itself is not retained (timestamps inside zips are not byte-stable inputs).
set -eu
CORPUS_DIR="${CORPUS_DIR:-/tmp/tnn-corpora}"
VER="${SQLITE_VER:-3530400}"
URL="${SQLITE_URL:-https://www.sqlite.org/2026/sqlite-amalgamation-$VER.zip}"
OUT="$CORPUS_DIR/sqlite3.c"
mkdir -p "$CORPUS_DIR"
if [ -f "$OUT" ]; then
  echo "exists: $OUT (delete to re-fetch)"
else
  TMPZIP="$CORPUS_DIR/.amalgamation-$VER.zip"
  echo "fetching $URL"
  curl -sSL --retry 3 --max-time 600 -o "$TMPZIP" "$URL"
  python3 -c "
import zipfile,sys
z=zipfile.ZipFile('$TMPZIP')
names=z.namelist()
c=[n for n in names if n.endswith('/sqlite3.c') or n=='sqlite3.c']
assert len(c)==1, names[:10]
data=z.read(c[0])
open('$OUT','wb').write(data)
print('extracted', c[0], len(data), 'bytes')
"
  rm -f "$TMPZIP"
fi
wc -c "$OUT"
sha256sum "$OUT"
