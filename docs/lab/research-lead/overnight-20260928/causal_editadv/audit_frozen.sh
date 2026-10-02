#!/bin/sh
# audit_frozen.sh -- verify attack drivers keep the frozen mechanism byte-identical.
# The mechanism region is everything before the main marker line in the
# 4c233f82a blob of causal_editinvent/editinvent.zag. Each attack driver must
# match the blob byte-for-byte over that region; only the driver main (at and
# after the marker) may differ. Shell only.
# Usage: sh audit_frozen.sh <driver.zag> [...]
# Exit 0 iff every driver's mechanism region is byte-identical to the frozen blob.
set -u
BLOB_TMP=/tmp/editadv_frozen_blob.zag
P1_TMP=/tmp/editadv_p1.zag
P2_TMP=/tmp/editadv_p2.zag
REPO=$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)
BLOB_PATH="docs/lab/research-lead/overnight-20260928/causal_editinvent/editinvent.zag"
if ! git -C "$REPO" show "4c233f82a:$BLOB_PATH" > "$BLOB_TMP" 2>/dev/null; then
  printf 'BLOB-FAIL: cannot extract 4c233f82a blob\n'
  exit 1
fi
MARK=$(LC_ALL=C grep -n "============ main:" "$BLOB_TMP" | cut -d: -f1 | head -1)
if [ -z "$MARK" ]; then
  printf 'MARK-FAIL: main marker not found in frozen blob\n'
  exit 1
fi
OFF=$(head -n $((MARK-1)) "$BLOB_TMP" | wc -c)
printf 'frozen blob: 4c233f82a main marker at line %s, mechanism region %s bytes\n' "$MARK" "$OFF"
head -c "$OFF" "$BLOB_TMP" > "$P2_TMP"
fail=0
if [ "$#" -eq 0 ]; then
  printf 'usage: sh audit_frozen.sh <driver.zag> [...]\n' >&2
  exit 2
fi
for d in "$@"; do
  if [ ! -r "$d" ]; then
    printf 'UNREADABLE: %s\n' "$d"
    fail=1
    continue
  fi
  head -c "$OFF" "$d" > "$P1_TMP"
  if cmp -s "$P1_TMP" "$P2_TMP"; then
    printf 'FROZEN-OK: %s (first %s bytes identical to 4c233f82a)\n' "$d" "$OFF"
  else
    printf 'FROZEN-FAIL: %s differs inside the mechanism region\n' "$d"
    fail=1
  fi
done
exit $fail
