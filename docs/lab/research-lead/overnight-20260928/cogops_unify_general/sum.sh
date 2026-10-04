#!/bin/sh
# sum.sh -- one summary row per variant: capability score + efficiency metrics.
set -eu
cd "$(dirname "$0")"
for t in "$@"; do
  F="out/$t.txt"
  [ -f "$F" ] || { echo "$t MISSING"; continue; }
  CAP=$(grep '^SUMMARY-DET' "$F" | sed 's/SUMMARY-DET //')
  RT=$(grep '^RESCUE' "$F" | sed 's/RESCUE total=//;s/ count=/\//')
  U=$(awk '/^CTX[0-9]/{for(i=3;i<=NF;i++){split($i,a,"=");split(a[2],b,",");s+=b[1]}}END{print s+0}' "$F")
  C=$(awk '/^CTX[0-9]/{for(i=3;i<=NF;i++){split($i,a,"=");split(a[2],b,",");s+=b[3]}}END{print s+0}' "$F")
  W=$(awk '/^CTX[0-9]/{for(i=3;i<=NF;i++){split($i,a,"=");split(a[2],b,",");s+=b[2]}}END{print s+0}' "$F")
  printf '%-5s sha=%-12s | %s | rescueT/C=%-7s | learnerTurns=%-3s wins=%-3s cost=%-4s\n' \
    "$t" "$(shasum -a 256 "$F"|cut -c1-12)" "$CAP" "$RT" "$U" "$W" "$C"
done
