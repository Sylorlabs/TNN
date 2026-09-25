#!/bin/bash
# run_lh.sh — T1/T2: run both long-horizon binaries 3x each, assert
# OB_FAILURES,0 and byte-identical outputs (SHA-256). Fails loudly.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ART="$HERE/artifacts"

for bin in ob_lh_bal_bin ob_lh_int_bin; do
  [ -x "$HERE/$bin" ] || { echo "FATAL: $bin missing" >&2; exit 1; }
  tag="${bin%_bin}"
  for i in 1 2 3; do
    "$HERE/$bin" > "$ART/${tag}_run$i.out" 2> "$ART/${tag}_run$i.err"
    rc=$?
    [ $rc -eq 0 ] || { echo "FATAL: $tag run$i rc=$rc" >&2; tail -5 "$ART/${tag}_run$i.out" >&2; exit 1; }
    [ "$(tail -1 "$ART/${tag}_run$i.out")" = "OB_FAILURES,0" ] || {
      echo "FATAL: $tag run$i not OB_FAILURES,0:" >&2
      grep "^OB_CHECK" "$ART/${tag}_run$i.out" | awk -F, '$3!=$4' >&2
      exit 1
    }
    sha256sum "$ART/${tag}_run$i.out" | awk '{print $1}' > "$ART/${tag}_run$i.sha256"
    echo "RUN_OK $tag run$i $(cat "$ART/${tag}_run$i.sha256")"
  done
  cmp -s "$ART/${tag}_run1.out" "$ART/${tag}_run2.out" || { echo "FATAL: $tag run1 vs run2 differ" >&2; exit 1; }
  cmp -s "$ART/${tag}_run1.out" "$ART/${tag}_run3.out" || { echo "FATAL: $tag run1 vs run3 differ" >&2; exit 1; }
  echo "DETERMINISM_OK $tag 3/3 byte-identical"
done
echo "ALL_OK"
