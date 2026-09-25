#!/bin/bash
# run_smoke.sh — run the integration smoke battery 3x and prove the outputs
# byte-identical. Fails loudly on any check failure or any output drift.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$HERE/ob_integration_bin"
ART="$HERE/artifacts/smoke"

[ -x "$BIN" ] || { echo "FATAL: binary missing; run build.sh first" >&2; exit 1; }
mkdir -p "$ART"

for i in 1 2 3; do
  "$BIN" > "$ART/run$i.out" 2> "$ART/run$i.err"
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "FATAL: run$i exited rc=$rc" >&2
    tail -20 "$ART/run$i.out" "$ART/run$i.err" >&2
    exit 1
  fi
  if [ "$(tail -1 "$ART/run$i.out")" != "OB_FAILURES,0" ]; then
    echo "FATAL: run$i did not report OB_FAILURES,0:" >&2
    tail -3 "$ART/run$i.out" >&2
    awk -F, '$1=="OB_CHECK" && $3!=$4' "$ART/run$i.out" >&2
    exit 1
  fi
  sha256sum "$ART/run$i.out" | awk '{print $1}' > "$ART/run$i.sha256"
  echo "RUN${i}_OK $(cat "$ART/run$i.sha256")"
done

if ! cmp -s "$ART/run1.out" "$ART/run2.out"; then
  echo "FATAL: run1 vs run2 differ" >&2; exit 1
fi
if ! cmp -s "$ART/run1.out" "$ART/run3.out"; then
  echo "FATAL: run1 vs run3 differ" >&2; exit 1
fi
echo "DETERMINISM_OK 3/3 byte-identical"
