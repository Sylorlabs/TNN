#!/bin/sh
# det.sh -- determinism check for the file-sink build (B1).
# zbuild.sh --rep 3 asserts 3x byte-identical STDOUT; this lane's builds
# flush to a file (PROBE_RAW_SYSCALL_INERT.md), so the same assertion is
# made on the flushed bytes instead. Usage: det.sh <tag>
set -eu
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
D="$(cd "$(dirname "$0")" && pwd)"
TAG="$1"
BIN="$D/probe/U_$TAG"
H=""
i=0
while [ "$i" -lt 3 ]; do
  i=$((i+1))
  rm -f /tmp/cogops_unify_out.txt
  "$BIN" > /dev/null 2>&1
  RC=$?
  H="$H $(shasum -a 256 /tmp/cogops_unify_out.txt | cut -d' ' -f1)"
done
U=$(printf '%s\n' $H | sort -u | wc -l | tr -d ' ')
if [ "$U" = 1 ]; then
  echo "DETERMINISM $TAG: PASS 3/3 byte-identical  $H"
else
  echo "DETERMINISM $TAG: FAIL ($U distinct)"
fi
