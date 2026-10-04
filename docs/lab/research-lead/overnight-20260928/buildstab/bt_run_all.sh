#!/bin/bash
# bt_run_all.sh -- BUILD-STABILITY full matrix + probes driver (prereg section 4).
# Runs SERIALLY. Every binary execution goes through tnnwatch.sh reg.
# Writes one summary line per (arm, source, probe) to SUMMARY.txt.

set -u
D=/Users/Shared/micah/Documents/TNN/.worktrees/buildstab/docs/lab/research-lead/overnight-20260928/buildstab
ZNC=/Users/Shared/micah/Documents/TNN/.bin/znc
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
BT=/Users/Shared/micah/Documents/TNN/.bt
mkdir -p "$BT"
SUM="$D/SUMMARY.txt"
: > "$SUM"

S1="$D/bt_small.zag"
S2="$D/c8_shim.zag"
S3="$D/s3_tnn2.zag"

say(){ echo "$*" | tee -a "$SUM"; }

# ---------------------------------------------------------------- MATRIX ----
for ARM in A0 A1 A2 A3 A4 A5; do
  for S in S1 S2 S3; do
    case $S in S1) SRC=$S1;; S2) SRC=$S2;; S3) SRC=$S3;; esac
    TAG="m_${ARM}_${S}"
    say "### MATRIX arm=$ARM src=$S N=5"
    "$D/bt_matrix.sh" "$ARM" "$SRC" 5 "$TAG" >> "$BT/$TAG.out" 2>&1
    grep '^SUMMARY arm=' "$BT/$TAG.out" | tee -a "$SUM"
    grep -E '^ARM=' "$BT/$TAG.out" | sed 's/^/    /' | tee -a "$SUM"
  done
done

# ------------------------------------------------- P5 distinct -o paths -----
say "### P5 five distinct output paths (baseline flags, cache purged)"
P5="$BT/p5"; rm -rf "$P5"; mkdir -p "$P5"
( . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
  for i in 1 2 3 4 5; do
    rm -f "$P5/out$i" "$P5/out$i.bin"; rm -rf "$P5/.zag-cache"
    "$ZNC" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache \
       "$S3" -o "$P5/out$i" >/dev/null 2>&1
    cp "$P5/out$i" "$P5/out$i.bin"; rm -f "$P5/out$i"
    echo "P5 path=$P5/out$i.bin $(shasum -a 256 "$P5/out$i.bin" | cut -d' ' -f1)"
  done ) | tee -a "$SUM"

# ------------------------------------------------- P1 mtime touch ----------
say "### P1 rebuild after touching source mtime to distinct values"
P1="$BT/p1"; rm -rf "$P1"; mkdir -p "$P1"
cp "$S3" "$P1/s.zag"
( . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
  for i in 1 2 3 4 5; do
    rm -f "$P1/b"; rm -rf "$P1/.zag-cache"
    touch -t "200${i}010${i}0000" "$P1/s.zag" 2>/dev/null || touch "$P1/s.zag"
    "$ZNC" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache \
       "$P1/s.zag" -o "$P1/b" >/dev/null 2>&1
    echo "P1 mtime=$(date -r "$P1/s.zag" +%s) $(shasum -a 256 "$P1/b" | cut -d' ' -f1)"
  done ) | tee -a "$SUM"

# ------------------------------------------------- P2 zagd off/on ----------
say "### P2 --no-zagd present vs absent (N=5 each)"
( . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
  for MODE in with without; do
    if [ "$MODE" = with ]; then F="--no-zagd"; else F=""; fi
    for i in 1 2 3 4 5; do
      rm -f "$BT/p2_$MODE"; rm -rf "$BT/.zag-cache"
      "$ZNC" --target macos-arm64 $F --no-analyze --no-foreground-cache \
         "$S3" -o "$BT/p2_$MODE" > "$BT/p2_$MODE.compile.$i.txt" 2>&1
      echo "P2 $MODE b$i $(shasum -a 256 "$BT/p2_$MODE" | cut -d' ' -f1)"
    done
  done
  echo "P2 zagd-warning-without-flag: $(grep -c 'zagd unavailable' "$BT/p2_without.compile.1.txt")"
  echo "P2 zagd-warning-with-flag:    $(grep -c 'zagd unavailable' "$BT/p2_with.compile.1.txt")"
  echo "P2 zagd_processes_visible:    $(ps ax | grep -c '[z]agd')"
  echo "P2 sibling_zagd_next_to_znc:  $(ls /Users/Shared/micah/Documents/TNN/.bin/ | grep -c '^zagd$')"
  echo "P2 .zag-cache_dirs_created:    $(find "$D" "$BT" -maxdepth 3 -name .zag-cache 2>/dev/null | wc -l | tr -d ' ')"
) | tee -a "$SUM"

# ------------------------------------------------- P3 analyze on/off -------
say "### P3 --no-analyze present vs absent (N=5 each)"
( . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
  for MODE in with without; do
    if [ "$MODE" = with ]; then F="--no-analyze"; else F=""; fi
    for i in 1 2 3 4 5; do
      rm -f "$BT/p3_$MODE"; rm -rf "$BT/.zag-cache"
      "$ZNC" --target macos-arm64 --no-zagd $F --no-foreground-cache \
         "$S3" -o "$BT/p3_$MODE" > "$BT/p3_$MODE.compile.$i.txt" 2>&1
      echo "P3 $MODE b$i $(shasum -a 256 "$BT/p3_$MODE" | cut -d' ' -f1)"
    done
  done ) | tee -a "$SUM"

# ------------------------------------- P4 foreground-cache present/absent ---
say "### P4 --no-foreground-cache present vs absent (N=5 each)"
( . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
  for MODE in with without; do
    if [ "$MODE" = with ]; then F="--no-foreground-cache"; else F=""; fi
    for i in 1 2 3 4 5; do
      rm -f "$BT/p4_$MODE"; rm -rf "$BT/.zag-cache"
      "$ZNC" --target macos-arm64 --no-zagd --no-analyze $F \
         "$S3" -o "$BT/p4_$MODE" > "$BT/p4_$MODE.compile.$i.txt" 2>&1
      echo "P4 $MODE b$i $(shasum -a 256 "$BT/p4_$MODE" | cut -d' ' -f1)"
    done
  done ) | tee -a "$SUM"

# ------------------------------------------------- P6 clean-cache ----------
say "### P6 znc clean-cache between builds (N=5)"
( . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
  cd "$BT" || exit 1
  for i in 1 2 3 4 5; do
    rm -f "$BT/p6"
    "$ZNC" clean-cache "$BT" >/dev/null 2>&1
    "$ZNC" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache \
       "$S3" -o "$BT/p6" >/dev/null 2>&1
    echo "P6 b$i $(shasum -a 256 "$BT/p6" | cut -d' ' -f1)"
  done ) | tee -a "$SUM"

# ------------------------------------------------- P7 rebuild ORDER --------
say "### P7 rebuild order reversed / interleaved (does order matter?)"
P7="$BT/p7"; rm -rf "$P7"; mkdir -p "$P7"
( . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
  for i in 1 2 3 4 5; do
    for S in "$S3" "$S1" "$S2"; do
      B=$(basename "$S" .zag); rm -f "$P7/$B"; rm -rf "$P7/.zag-cache"
      "$ZNC" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache \
         "$S" -o "$P7/$B" >/dev/null 2>&1
      echo "P7 round=$i $B $(shasum -a 256 "$P7/$B" | cut -d' ' -f1)"
    done
  done ) | tee -a "$SUM"

# ------------------------------------- P8 zag.mod project root present ------
say "### P8 project root with zag.mod (does a project cache engage?)"
P8="$BT/p8"; rm -rf "$P8"; mkdir -p "$P8"
cp "$S1" "$P8/bt_small.zag"
( . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
  cd "$P8" || exit 1
  "$ZNC" init >/dev/null 2>&1
  echo "P8 zagmod_present=$([ -f zag.mod ] && echo yes || echo no)"
  for i in 1 2 3 4 5; do
    rm -f "$P8/b"; rm -rf "$P8/.zag-cache"
    "$ZNC" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache \
       "$P8/bt_small.zag" -o "$P8/b" >/dev/null 2>&1
    echo "P8 b$i $(shasum -a 256 "$P8/b" | cut -d' ' -f1) cache_dirs=$(find "$P8" -maxdepth 2 -name .zag-cache | wc -l | tr -d ' ')"
  done ) | tee -a "$SUM"

say "### DONE"