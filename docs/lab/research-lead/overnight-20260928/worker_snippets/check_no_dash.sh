#!/bin/sh
# check_no_dash.sh -- shell-only byte check for em dash / en dash.
# No Python. Uses LC_ALL=C grep on byte sequences built via printf.
# Usage: sh check_no_dash.sh <file> [<file> ...]
# Exit 0 when every file is clean; exit 1 when any forbidden byte is found
# or when a file cannot be read.
EMDASH=$(printf '\342\200\224')
ENDASH=$(printf '\342\200\223')
fail=0
if [ "$#" -eq 0 ]; then
  printf 'usage: sh check_no_dash.sh <file> [file...]\n' >&2
  exit 2
fi
for f in "$@"; do
  if [ ! -r "$f" ]; then
    printf 'UNREADABLE: %s\n' "$f"
    fail=1
    continue
  fi
  if LC_ALL=C grep -q "$EMDASH" -- "$f" 2>/dev/null; then
    printf 'EMDASH-FOUND: %s\n' "$f"
    fail=1
  fi
  if LC_ALL=C grep -q "$ENDASH" -- "$f" 2>/dev/null; then
    printf 'ENDASH-FOUND: %s\n' "$f"
    fail=1
  fi
done
exit $fail
