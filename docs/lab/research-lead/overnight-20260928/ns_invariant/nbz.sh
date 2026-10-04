#!/bin/bash
# nbz.sh -- lane-local pure-Zag run harness for drivers that write their output
# with _zag_write_file (the mandated _zag_raw_syscall output path is dead on
# this host: it returns -78/ENOSYS for every syscall number, see p5.zag).
#
#   ./nbz.sh FILE.zag [--rep N] [-- args...]
#
# Builds with tools/zbuild.sh (pinned znc, --target macos-arm64), then runs the
# binary N times with ARGS, and hashes the FILE the binary wrote. Shell is
# orchestration only (charter section 4): every number in that file was
# computed inside the Zag binary.
set -u
export PATH="$(pwd):$PATH"
SRC=""; MODE=""; ARGS=""; seen=0
for a in "$@"; do
  if [ "$a" = "--" ]; then seen=1; continue; fi
  if [ "$seen" = "1" ]; then ARGS="$ARGS $a"; continue; fi
  if [ -z "$SRC" ]; then SRC="$a"; elif [ -z "$MODE" ]; then MODE="$a"; fi
done
[ -n "$SRC" ] || { echo "usage: ./nbz.sh FILE.zag [--rep N] [-- args...]" >&2; exit 2; }
N=1
case "$MODE" in --rep*) N="${MODE#--rep}"; N="${N:-3}";; esac
OUT="ns_drv_out.txt"
# Always build first; never reuse a stale binary after a compile failure.
# shellcheck disable=SC2086
/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh "$SRC"
RC=$?
if [ "$RC" != "0" ]; then echo "[nbz] COMPILE-FAIL rc=$RC"; exit 1; fi
BIN="${SRC%.zag}"
[ -x "$BIN" ] || { echo "[nbz] INFRA-FAIL: no executable $BIN"; exit 2; }
rm -f "$OUT"
HASHES=""
ALLOK=1
for i in $(seq 1 "$N"); do
  rm -f "$OUT"
  # shellcheck disable=SC2086
  "$BIN" $ARGS
  R=$?
  [ -f "$OUT" ] || { echo "[nbz] run $i produced no $OUT (rc=$R)"; exit 1; }
  H=$(shasum -a 256 "$OUT" | cut -d' ' -f1)
  HASHES="$HASHES $H"
  echo "[run $i] rc=$R sha=$H"
done
U=$(printf '%s\n' $HASHES | sort -u | wc -l | tr -d ' ')
if [ "$U" = "1" ]; then
  echo "[nbz] DETERMINISM: PASS ($N/$N byte-identical $HASHES)"
else
  echo "[nbz] DETERMINISM: FAIL ($U distinct outputs across $N runs)"
  ALLOK=0
fi
[ "$ALLOK" = "1" ] || exit 1
exit 0
