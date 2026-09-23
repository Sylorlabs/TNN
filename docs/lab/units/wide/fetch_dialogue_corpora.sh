#!/usr/bin/env bash
# fetch_dialogue_corpora.sh — fetch-on-demand for the EXTRA CORPORA: DIALOGUE track.
# Exploratory only. NOTHING here is program evidence. Corpora are NEVER committed:
# they live in /tmp/dialogue_corpora and are re-fetched on demand.
#
# URL scheme: Project Gutenberg canonical plain-text URLs
#   https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt
# (ebook IDs verified against gutenberg.org ebook pages, 2026-09-20)
# Eckermann/Oxenford is not on Project Gutenberg; fetched from the Internet
# Archive scan of the 1875 Bohn's Standard Library edition (OCR text).
# NOTE: use the /download/ URL (raw OCR text). The /stream/ URL serves an HTML
# viewer page with the OCR wrapped in a <pre> block -- NOT the raw text.
# Verified 2026-09-21: /download/ returns 743179 bytes of raw OCR, no HTML.
set -u
OUT="${1:-/tmp/dialogue_corpora}"
mkdir -p "$OUT"

fetch() { # name url outfile
  local name="$1" url="$2" out="$3"
  echo "--- $name"
  echo "    $url"
  if curl -sSL --fail --retry 2 --max-time 120 -o "$out" "$url"; then
    local bytes sha
    bytes=$(wc -c < "$out")
    sha=$(sha256sum "$out" | cut -d' ' -f1)
    echo "    OK bytes=$bytes sha256=$sha"
    echo "$name|$url|$bytes|$sha" >> "$OUT/MANIFEST.tsv"
  else
    echo "    FAILED (curl exit $?)"
    return 1
  fi
}

rm -f "$OUT/MANIFEST.tsv"
fail=0
fetch "wilde_earnest"   "https://www.gutenberg.org/cache/epub/844/pg844.txt"     "$OUT/wilde_earnest.txt"     || fail=1
fetch "ibsen_dollhouse" "https://www.gutenberg.org/cache/epub/2542/pg2542.txt"   "$OUT/ibsen_dollhouse.txt"   || fail=1
fetch "plato_republic"  "https://www.gutenberg.org/cache/epub/150/pg150.txt"     "$OUT/plato_republic.txt"     || fail=1
fetch "stoker_dracula"  "https://www.gutenberg.org/cache/epub/345/pg345.txt"     "$OUT/stoker_dracula.txt"     || fail=1
fetch "eckermann_goethe" "https://archive.org/download/conversationsgo01oxengoog/conversationsgo01oxengoog_djvu.txt" "$OUT/eckermann_goethe.txt" || fail=1

echo "=== manifest ==="
cat "$OUT/MANIFEST.tsv"
exit $fail
