#!/bin/bash
# nb.sh -- lane-local pure-Zag build+run+determinism harness for ns_invariant.
#
# Identical contract to tools/zbuild.sh (charter section 4: shell is
# orchestration only; every number is computed inside the Zag binary).
# Differences, both necessary:
#   1. prepends the lane directory to PATH so the produced binary is
#      resolvable without an absolute path (the restricted pure-Zag PATH does
#      not include the current directory);
#   2. forwards ARGS after "--" to the binary (tools/zbuild.sh takes none),
#      and uses those ARGS for the determinism repetitions.
#
# Usage: ./nb.sh FILE.zag [--rep N] [-- args...]
set -u
export PATH="$(pwd):$PATH"
SRC=""
MODE=""
ARGS=""
seen=0
for a in "$@"; do
  if [ "$a" = "--" ]; then seen=1; continue; fi
  if [ "$seen" = "1" ]; then ARGS="$ARGS $a"; continue; fi
  if [ -z "$SRC" ]; then SRC="$a";
  elif [ -z "$MODE" ]; then MODE="$a"; fi
done
if [ -z "$MODE" ] && [ -n "$ARGS" ]; then MODE="--rep 3"; fi
# shellcheck disable=SC2086
/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh "$SRC" $MODE >/dev/null 2>&1
RC=$?
BIN="${SRC%.zag}"
if [ "$RC" != "0" ]; then
  /Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh "$SRC" $MODE
  exit 1
fi
if [ "$MODE" = "--nobuild" ]; then
  # shellcheck disable=SC2086
  "$BIN" $ARGS
  exit $?
fi
N=1
case "$MODE" in --rep*) N="${MODE#--rep}"; N="${N:-3}";; esac
HASHES=""
ALLOK=1
for i in $(seq 1 "$N"); do
  # shellcheck disable=SC2086
  O=$("$BIN" $ARGS 2>&1); R=$?
  H=$(printf '%s\n' "$O" | shasum -a 256 | cut -d' ' -f1)
  HASHES="$HASHES $H"
  printf '%s\n' "$O" > ".nb_out_$i.txt"
  echo "[run $i] rc=$R sha=$H"
  if [ "$i" = "1" ] || [ "$N" = "1" ]; then
    printf '%s\n' "$O"
  fi
done
U=$(printf '%s\n' $HASHES | sort -u | wc -l | tr -d ' ')
if [ "$U" = "1" ]; then
  echo "[nb] DETERMINISM: PASS ($N/$N byte-identical $HASHES)"
else
  echo "[nb] DETERMINISM: FAIL ($U distinct outputs across $N runs)"
  ALLOK=0
fi
rm -f .nb_out_1.txt .nb_out_2.txt .nb_out_3.txt .nb_out_4.txt
[ "$ALLOK" = "1" ] || exit 1
exit 0
