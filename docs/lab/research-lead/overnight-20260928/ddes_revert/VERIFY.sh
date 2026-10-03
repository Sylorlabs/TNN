#!/bin/sh
# VERIFY.sh -- check every frozen prereg line against RUN1.txt.
# Usage: ./VERIFY.sh   (run from the ddes_revert/ directory)
set -e
F=RUN1.txt
if [ ! -f "$F" ]; then
  echo "VERIFY-FAIL: $F missing (run RUN.sh first)" >&2
  exit 1
fi
fail=0
need() {
  if grep -qF "$1" "$F"; then
    echo "PRESENT: $1"
  else
    echo "MISSING: $1" >&2
    fail=1
  fi
}
need "FEED e5 P0 passive=(1,2)=1 nc=3"
need "EP e5 P0 AMBIGUOUS survivors=[h0,h1,h2]"
need "ADAPT e5 P1 ROUND 1 survivors=[h0,h1,h2] TARGET V*=1 t*=1 schema=1"
need "ADAPT e5 P1 ROUND 1 PLAN [S,W,O(1)] built=1"
need "ADAPT e5 P1 ROUND 1 EXEC real=0"
need "ADAPT e5 P1 ROUND 1 PRED h0=1 h1=0 h2=0"
need "ADAPT e5 P1 ROUND 1 ELIM h0"
need "ADAPT e5 P1 ROUND 2 survivors=[h1,h2] TARGET V*=2 t*=1 schema=1"
need "ADAPT e5 P1 ROUND 2 PLAN [S,W,O(2)] built=1"
need "ADAPT e5 P1 ROUND 2 EXEC real=1"
need "ADAPT e5 P1 ROUND 2 PRED h1=1 h2=0"
need "ADAPT e5 P1 ROUND 2 ELIM h2"
need "ADAPT e5 P1 RESOLVED winner=h1 rounds=2"
need "ADAPT e5 P2 RESOLVED winner=h0 rounds=1"
need "ADAPT e5 P2 ROUND 1 EXEC real=1"
need "ONESHOT e5 P1 ONESHOT-RESOLVE-FAIL survivors=2"
need "STATIC e5 P1 SINGLE winner=h0 rounds=0"
need "ADAPT e6 P2 ROUND 2 survivors=[h1,h2] TARGET V*=2 t*=1 schema=1"
need "ADAPT e6 P2 ROUND 2 EXEC real=0"
need "ADAPT e6 P2 ROUND 2 PRED h1=1 h2=0"
need "ADAPT e6 P2 ROUND 2 ELIM h1"
need "ADAPT e6 P2 RESOLVED winner=h2 rounds=2"
need "DECLARE e7 P0 OUTSIDE-SET"
need "SUMMARY mode=BASE ok=13/13 resolved=0"
need "SUMMARY mode=ONESHOT ok=15/15 resolved=4"
need "SUMMARY mode=ADAPT ok=24/24 resolved=9"
need "SUMMARY mode=STATIC ok=19/19 resolved=9"
if [ "$fail" -ne 0 ]; then
  echo "VERIFY-FAIL: one or more frozen lines missing" >&2
  exit 1
fi
echo "VERIFY-OK: all frozen prereg lines present"
