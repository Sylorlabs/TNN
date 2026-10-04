#!/bin/bash
# sensrun.sh -- run binaries under the watchdog (brief 10.1), 600 s prereg limit.
#   sensrun.sh TAG BIN [BIN...]
# Writes R_<TAG>.txt. Reports EMPTY-LOG as a PROCESS FAILURE (brief 10.1):
# zero bytes is not a result.
set -u
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
TAG="$1"; shift
rc_all=0
for b in "$@"; do
  $W reg "$TAG" 600 "./$b" > "R_$TAG.txt" 2>&1
  rc=$?
  n=$(wc -c < "R_$TAG.txt" | tr -d ' ')
  if [ "$n" -lt 1 ]; then
    echo "[run] $TAG/$b EMPTY-LOG (rc=$rc) -- PROCESS-FAIL, not a result"; rc_all=1
  else
    echo "[run] $TAG/$b bytes=$n rc=$rc"
  fi
done
exit $rc_all
