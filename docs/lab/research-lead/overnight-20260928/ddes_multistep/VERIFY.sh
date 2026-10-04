#!/bin/sh
# VERIFY.sh -- check every frozen prereg line against a run transcript.
# Usage: VERIFY.sh RUN.txt ; exits nonzero on any mismatch. Pure shell.
set -e
R="$1"
fail=0
chk() {
  n=$(grep -c -F "$1" "$R" || true)
  if [ "$n" != "1" ]; then
    echo "MISMATCH (count=$n): $1"
    fail=1
  fi
}
# M1 adaptive trace
chk "ADAPT e2 ROUND 1 survivors=[h0,h1,h2] TARGET V*=1 t*=1 schema=1"
chk "ADAPT e2 ROUND 1 PLAN [S,W,O(1)] built=1"
chk "ADAPT e2 ROUND 1 EXEC real=0"
chk "ADAPT e2 ROUND 1 PRED h0=1 h1=0 h2=0"
chk "ADAPT e2 ROUND 1 ELIM h0"
chk "ADAPT e2 ROUND 2 survivors=[h1,h2] TARGET V*=2 t*=2 schema=1"
chk "ADAPT e2 ROUND 2 PLAN [S,W,W,O(2)] built=1"
chk "ADAPT e2 ROUND 2 EXEC real=1"
chk "ADAPT e2 ROUND 2 PRED h1=0 h2=1"
chk "ADAPT e2 ROUND 2 ELIM h1"
chk "ADAPT e2 RESOLVED winner=h2 rounds=2"
# M2 adaptive trace
chk "ADAPT e3 ROUND 1 survivors=[h0,h1,h2] TARGET V*=1 t*=1 schema=1"
chk "ADAPT e3 ROUND 1 PLAN [S,W,O(1)] built=1"
chk "ADAPT e3 ROUND 1 EXEC real=0"
chk "ADAPT e3 ROUND 2 survivors=[h1,h2] TARGET V*=2 t*=1 schema=1"
chk "ADAPT e3 ROUND 2 PLAN [S,W,O(2)] built=1"
chk "ADAPT e3 ROUND 2 EXEC real=1"
chk "ADAPT e3 ROUND 2 PRED h1=1 h2=0"
chk "ADAPT e3 ROUND 2 ELIM h2"
chk "ADAPT e3 RESOLVED winner=h1 rounds=2"
# One-shot insufficiency on M1/M2
chk "ONESHOT e2 TARGET V*=1 t*=1 schema=1"
chk "ONESHOT e2 ONESHOT-RESOLVE-FAIL survivors=2"
chk "ONESHOT e3 TARGET V*=1 t*=1 schema=1"
chk "ONESHOT e3 ONESHOT-RESOLVE-FAIL survivors=2"
# One-shot regression on A
chk "ONESHOT e4 RESOLVED winner=h1 rounds=1"
chk "ADAPT e4 RESOLVED winner=h1 rounds=1"
# Summaries
chk "SUMMARY mode=BASE ok=6/6 resolved=0"
chk "SUMMARY mode=ONESHOT ok=8/8 resolved=1"
chk "SUMMARY mode=ADAPT ok=12/12 resolved=3"
if [ "$fail" = "0" ]; then echo VERIFY-OK; fi
exit $fail
