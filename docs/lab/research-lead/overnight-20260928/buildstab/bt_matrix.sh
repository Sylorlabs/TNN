#!/bin/bash
# bt_matrix.sh -- BUILD-STABILITY determinism harness (prereg section 4).
#
# Shell is ORCHESTRATION ONLY (charter section 4). All scientific computation
# is inside the Zag binaries. This script only: calls znc, hashes files, calls
# the watchdog. No interpreter other than /bin/sh + coreutils is used.
#
# Usage: bt_matrix.sh <arm> <source.zag> <N> <outdir-tag>
#   arm:      A0 A1 A2 A3 A4 A5
#   source:   path to .zag
#   N:        number of builds (>=5)
#   tag:      label for the result directory
#
# Prints one TSV row per build:
#   build_idx  binary_bytes  binary_sha256  out_sha256  out_bytes  distinct_so_far
# and a final summary line.

set -u
ARM="${1:?arm}"
SRC="${2:?src}"
N="${3:?N}"
TAG="${4:?tag}"

ZNC=/Users/Shared/micah/Documents/TNN/.bin/znc
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
D=/Users/Shared/micah/Documents/TNN/.worktrees/buildstab/docs/lab/research-lead/overnight-20260928/buildstab
R=/Users/Shared/micah/Documents/TNN/.bt/$TAG
rm -rf "$R"; mkdir -p "$R"

BASE=$(basename "$SRC" .zag)

# ---- arm configuration -----------------------------------------------------
case "$ARM" in
  A0) FLAGS="--no-zagd --no-analyze --no-foreground-cache"
       CWD="$D"; OUTDIR="$R"; PURGE=1; FRESHENV=0 ;;
  A1) FLAGS="--no-zagd --no-analyze --no-foreground-cache"
       CWD="$D"; OUTDIR="$R"; PURGE=0; FRESHENV=0 ;;
  A2) FLAGS=""
       CWD="$D"; OUTDIR="$R"; PURGE=1; FRESHENV=0 ;;
  A3) FLAGS="--no-zagd --no-analyze --no-foreground-cache"
       CWD="/tmp"; OUTDIR="/tmp/bt_out_$TAG"; PURGE=1; FRESHENV=0 ;;
  A4) FLAGS="--no-zagd --no-analyze --no-foreground-cache"
       CWD="$D"; OUTDIR="$R"; PURGE=1; FRESHENV=0; HOSTPATH=1 ;;
  A5) FLAGS="--no-zagd --no-analyze --no-foreground-cache"
       CWD="$D"; OUTDIR="$R"; PURGE=1; FRESHENV=1 ;;
  *)  echo "unknown arm $ARM" >&2; exit 2 ;;
esac
mkdir -p "$OUTDIR"

# PURE-ZAG enforcement shim PATH (prereg "pure-zag shim PATH"). A4 replaces it
# with the inherited host PATH to test whether PATH can reach codegen.
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
[ "${HOSTPATH:-0}" = "1" ] && export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/Users/Shared/micah/Documents/TNN/.bin"

TSV="$R/builds.tsv"
printf 'build\tbytes\tbin_sha256\tout_sha256\tout_bytes\n' > "$TSV"

declare -a seen_shas=()
distinct=0

i=1
while [ "$i" -le "$N" ]; do
  BIN="$OUTDIR/${BASE}.a${ARM}.b${i}"
  rm -f "$BIN"                                   # CLEAN STATE: no stale binary
  [ "$PURGE" = "1" ] && rm -rf "$OUTDIR/.zag-cache" "$CWD/.zag-cache" 2>/dev/null

  if [ "$FRESHENV" = "1" ]; then
    # A5: fresh shell per build. env -i gives an empty environment; we supply
    # only what the compiler could conceivably read.
    ( cd "$CWD" && env -i PATH="$PATH" HOME="$HOME" TMPDIR="${TMPDIR:-/tmp}" \
        "$ZNC" --target macos-arm64 $FLAGS "$SRC" -o "$BIN" ) \
        > "$R/build$i.compile.txt" 2>&1
  else
    ( cd "$CWD" && "$ZNC" --target macos-arm64 $FLAGS "$SRC" -o "$BIN" ) \
        > "$R/build$i.compile.txt" 2>&1
  fi
  rc=$?
  if [ $rc -ne 0 ] || [ ! -f "$BIN" ]; then
    echo "ARM=$ARM BUILD=$i COMPILE-FAIL rc=$rc" | tee -a "$R/FAIL.txt"
    i=$((i+1)); continue
  fi

  bbytes=$(wc -c < "$BIN" | tr -d ' ')
  bsha=$(shasum -a 256 "$BIN" | cut -d' ' -f1)

  # 3/3 run determinism, behind the watchdog, non-empty asserted.
  osha=""; obytes=0; rcs=""
  for r in 1 2 3; do
    "$W" reg "bt_${TAG}_b${i}_r${r}" 300 "$BIN" > "$R/build${i}.run${r}.txt" 2>/dev/null
    osha="$osha $(shasum -a 256 "$R/build${i}.run${r}.txt" | cut -d' ' -f1)"
    obytes=$(wc -c < "$R/build${i}.run${r}.txt" | tr -d ' ')
  done
  odistinct=$(printf '%s\n' $osha | sort -u | wc -l | tr -d ' ')
  osha1=$(printf '%s\n' $osha | sort -u | tr -d ' ')

  printf '%s\t%s\t%s\t%s\t%s\truns_distinct=%s\n' \
    "$i" "$bbytes" "$bsha" "$osha1" "$obytes" "$odistinct" >> "$TSV"

  hit=0
  for s in "${seen_shas[@]:-}"; do [ "$s" = "$bsha" ] && hit=1; done
  if [ "$hit" = "0" ]; then distinct=$((distinct+1)); seen_shas+=("$bsha"); fi

  echo "ARM=$ARM build=$i bytes=$bbytes bin_sha=${bsha:0:16} out_sha=${osha1:0:16} out_bytes=$obytes run_distinct=$odistinct"
  i=$((i+1))
done

BIN_DISTINCT=$distinct
RUN_FAIL=$(grep -c 'runs_distinct=[^1]' "$TSV" 2>/dev/null || echo 0)
EMPTY=$(awk -F'\t' '$5==0' "$TSV" | wc -l | tr -d ' ')
echo "SUMMARY arm=$ARM src=$BASE N=$N BIN_DISTINCT=$BIN_DISTINCT RUN_NONDET_ROWS=$RUN_FAIL EMPTY_OUTPUTS=$EMPTY"
echo "SUMMARY_RESULT $TAG $ARM $BASE $N $BIN_DISTINCT $RUN_FAIL $EMPTY" >> "$R/summary.txt"
cat "$TSV"