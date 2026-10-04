#!/bin/bash
# zbuild: canonical pure-Zag build+run+determinism harness.
#
# Shell is used ONLY for orchestration (charter section 4). All scientific
# computation happens inside the Zag binary.
#
# Usage:
#   zbuild.sh <source.zag>            build once, run once
#   zbuild.sh <source.zag> --rep 3    build+run 3x, assert byte-identical outputs
#   zbuild.sh <source.zag> --nobuild  run existing binary
#
# Exit 0 = success. Exit 1 = FAIL. Exit 2 = usage/infra.

set -u
SRC="${1:-}"
MODE="${2:-}"
[ -n "$SRC" ] || { echo "usage: zbuild.sh FILE.zag [--rep N|--nobuild]" >&2; exit 2; }
[ -f "$SRC" ] || { echo "zbuild: no such source: $SRC" >&2; exit 2; }

ZNC="${TNN_ROOT:-/Users/Shared/micah/Documents/TNN}/.bin/znc"
# Mandatory flags; see docs/ops/TOOLCHAIN.md section 1.1. Omitting --target
# silently emits Linux ELF which cannot execute here.
FLAGS="--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache"

BASE="${SRC%.zag}"
BIN="$BASE"

if [ "$MODE" != "--nobuild" ]; then
  OUT=$("$ZNC" $FLAGS "$SRC" 2>&1)
  RC=$?
  echo "$OUT" | sed 's/^/[znc] /'
  if [ $RC -ne 0 ]; then
    echo "[zbuild] COMPILE-FAIL rc=$RC"
    exit 1
  fi
  # Guard against the silent-ELF failure mode even if flags were lost.
  if command -v file >/dev/null 2>&1; then
    case "$(file -b "$BIN" 2>/dev/null)" in
      *ELF*) echo "[zbuild] INFRA-FAIL: produced ELF binary on darwin; --target lost"; exit 2 ;;
    esac
  fi
fi

[ -x "$BIN" ] || { chmod +x "$BIN" 2>/dev/null; }
[ -x "$BIN" ] || { echo "[zbuild] INFRA-FAIL: no executable $BIN"; exit 2; }

case "$MODE" in
  --rep*)
    N="${MODE#--rep}"; N="${N:-3}"
    TMPD=$(mktemp -d); trap 'rm -rf "$TMPD"' EXIT
    HASHES=""; ALLOK=1
    for i in $(seq 1 "$N"); do
      O=$("$BIN" 2>&1); R=$?
      printf '%s\n' "$O" > "$TMPD/o$i"
      H=$(shasum -a 256 "$TMPD/o$i" | cut -d' ' -f1)
      HASHES="$HASHES $H"
      echo "[run $i] rc=$R sha=$H"
      echo "----- run $i output -----"
      echo "$O"
      echo "------------------------"
    done
    U=$(printf '%s\n' $HASHES | sort -u | wc -l | tr -d ' ')
    if [ "$U" = "1" ]; then
      echo "[zbuild] DETERMINISM: PASS ($N/$N byte-identical, $HASHES )"
    else
      echo "[zbuild] DETERMINISM: FAIL ($U distinct outputs across $N runs)"
      ALLOK=0
    fi
    [ "$ALLOK" = "1" ] || exit 1
    ;;
  *)
    "$BIN"; RC=$?
    echo "[zbuild] run rc=$RC"
    exit $RC
    ;;
esac
exit 0
