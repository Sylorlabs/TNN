#!/bin/bash
# zr.sh -- compile + 3x watchdog-run + determinism assert for tcdefects probes.
# Shell is ORCHESTRATION ONLY (brief 10.x). All computation lives in the .zag file.
# EVERY run goes through tnnwatch.sh (brief 10.1). Nothing is left unattended.
#
# usage: ./zr.sh <name>        (name.zag in this directory)
set -u
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
D="$(cd "$(dirname "$0")" && pwd)"
N="$1"
SRC="$D/$N.zag"
[ -f "$SRC" ] || { echo "zr: no $SRC"; exit 2; }
OUT=$(znc "$SRC" 2>&1); RC=$?
if [ $RC -ne 0 ]; then echo "[$N] COMPILE-FAIL rc=$RC"; printf '%s\n' "$OUT"; exit 3; fi
case "$(file -b "$D/$N" 2>/dev/null)" in *ELF*) echo "[$N] INFRA-FAIL ELF"; exit 2;; esac
H=""
for i in 1 2 3; do
  $W reg "${N}_r$i" 120 "$D/$N" >/dev/null 2>&1
  R=$(cat /Users/Shared/micah/Documents/TNN/.runs/${N}_r$i.meta 2>/dev/null | sed -n 's/^status=//p')
  B=$(cat /Users/Shared/micah/Documents/TNN/.runs/${N}_r$i.log 2>/dev/null)
  S=$(printf '%s' "$B" | shasum -a 256 | cut -c1-12)
  BY=$(printf '%s' "$B" | wc -c | tr -d ' ')
  H="$H $S"
  echo "  [$N run$i] watch=$R bytes=$BY sha=$S"
  printf '%s\n' "$B" | sed 's/^/    | /'
done
U=$(printf '%s\n' $H | tr ' ' '\n' | sort -u | wc -l | tr -d ' ')
if [ "$U" = "1" ]; then echo "[$N] DETERMINISM PASS 3/3 ($H)"; else echo "[$N] DETERMINISM FAIL ($U distinct)"; exit 1; fi
