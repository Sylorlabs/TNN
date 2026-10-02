#!/bin/bash
# verify_copies.sh — prove the drivers' mechanism functions are byte-identical
# to the committed H-PAM-35/36 probe source (8d16d9f3). Re-extracts and diffs.
# Usage: ./verify_copies.sh <path-to-hpam3536_probe.zag> <dir-with-copy35.zag-copy36.zag>
set -e
SRC="$1"
DIR="$2"
for W in 35 36; do
  python3 "$(dirname "$0")/extract_copies.py" "$SRC" "$W" "$DIR/copy$W.check.zag"
  if cmp -s "$DIR/copy$W.check.zag" "$DIR/copy$W.zag"; then
    echo "copy$W.zag: BYTE-IDENTICAL to committed probe functions"
  else
    echo "copy$W.zag: MISMATCH — FAIL"
    exit 1
  fi
  rm "$DIR/copy$W.check.zag"
done
