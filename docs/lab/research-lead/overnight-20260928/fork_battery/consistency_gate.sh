#!/bin/sh
# consistency_gate.sh -- automated manifest/driver/result consistency check
# for the fork-battery loop. Pure shell + git. No Python anywhere.
#
# Usage: consistency_gate.sh [--pre-run] <driver.sh> <manifest.md> <scratch-E-dir>
#
# In --pre-run mode (run BEFORE the battery executes) only A1 and A2 are
# asserted; the E-dir argument may point at a scratch E directory that does
# not exist yet. A malformed driver (wrong count, unresolvable SHA) fails
# fast instead of burning the battery run. The full gate (A1-A4) still
# runs before the results commit.
#
# Assertions (all must hold; exit 0 only if every one passes):
#  A1: driver run() line count equals the manifest's declared total
#      (first line matching "^Total: N named entries").
#  A2: every run() SHA resolves via "git cat-file -t" to "commit".
#  A3: every run() name has <E>/<name>/RESULT.txt whose ref= matches the
#      pinned SHA from the driver line.
#  A4: the PASS/FAIL/UNTESTABLE tally over all RESULT.txt files sums to
#      the manifest's declared total.
#
# The results commit is blocked unless this gate exits 0.
# Pre-run mode: --pre-run asserts A1+A2 only, before the battery executes,
# so a malformed driver fails fast instead of burning the run. A3/A4 still
# run after results exist, before the results commit.
set -u

PRE_RUN=0
if [ "${1:-}" = "--pre-run" ]; then
  PRE_RUN=1
  shift
fi

DRIVER="$1"
MANIFEST="$2"
EDIR="${3:-/nonexistent-pre-run}"
FAIL=0

total=$(grep -m1 '^Total: [0-9][0-9]* named entries' "$MANIFEST" | sed 's/^Total: \([0-9][0-9]*\) named entries.*/\1/')
if [ -z "$total" ]; then
  echo "GATE-FAIL A1: no 'Total: N named entries' line in $MANIFEST"
  exit 1
fi

runlines=$(grep -c '^run [^ ][^ ]* [0-9a-f][0-9a-f]*$' "$DRIVER")
if [ "$runlines" != "$total" ]; then
  echo "GATE-FAIL A1: driver run() lines=$runlines != manifest total=$total"
  FAIL=1
else
  echo "GATE-PASS A1: driver run() lines=$runlines == manifest total=$total"
fi

# A2 per entry
grep '^run [^ ][^ ]* [0-9a-f][0-9a-f]*$' "$DRIVER" | while read -r _ name sha; do
  t=$(git cat-file -t "$sha" 2>/dev/null || echo MISSING)
  if [ "$t" != "commit" ]; then
    echo "GATE-FAIL A2: $name sha $sha does not resolve (got $t)"
    exit 1
  fi
done || FAIL=1
if [ "$FAIL" -eq 0 ]; then
  echo "GATE-PASS A2: all $runlines SHAs resolve to commit objects"
fi

if [ "$PRE_RUN" -eq 1 ]; then
  if [ "$FAIL" -eq 0 ]; then
    echo "CONSISTENCY-GATE PRE-RUN: ALL PASS (A1, A2)"
    exit 0
  else
    echo "CONSISTENCY-GATE PRE-RUN: FAIL"
    exit 1
  fi
fi

# A3 per entry
grep '^run [^ ][^ ]* [0-9a-f][0-9a-f]*$' "$DRIVER" | while read -r _ name sha; do
  rf="$EDIR/$name/RESULT.txt"
  if [ ! -f "$rf" ]; then
    echo "GATE-FAIL A3: $name missing $rf"
    exit 1
  fi
  ref=$(grep -m1 '^ref=' "$rf" | cut -d= -f2)
  if [ "$ref" != "$sha" ]; then
    echo "GATE-FAIL A3: $name RESULT.txt ref=$ref != driver sha=$sha"
    exit 1
  fi
done || FAIL=1
if [ "$FAIL" -eq 0 ]; then
  echo "GATE-PASS A3: all $runlines RESULT.txt refs match driver SHAs"
fi

# A4: tally
np=0; nf=0; nu=0
for rf in "$EDIR"/*/RESULT.txt; do
  v=$(grep -m1 '^verdict=' "$rf" | cut -d= -f2)
  case "$v" in
    PASS) np=$((np+1));;
    FAIL) nf=$((nf+1));;
    UNTESTABLE) nu=$((nu+1));;
    *) echo "GATE-FAIL A4: $rf has unknown verdict '$v'"; FAIL=1;;
  esac
done
sum=$((np+nf+nu))
if [ "$sum" != "$total" ]; then
  echo "GATE-FAIL A4: tally PASS=$np FAIL=$nf UNTESTABLE=$nu sum=$sum != total=$total"
  FAIL=1
else
  echo "GATE-PASS A4: tally PASS=$np FAIL=$nf UNTESTABLE=$nu sum=$sum == total=$total"
fi

if [ "$FAIL" -eq 0 ]; then
  echo "CONSISTENCY-GATE: ALL PASS"
  exit 0
else
  echo "CONSISTENCY-GATE: FAIL"
  exit 1
fi
