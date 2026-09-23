#!/bin/bash
# Senses phase-2 vision battery runner.
# Prereg: PREREG_SENSES_PHASE2_VISION.md (frozen before build).
# Measures proposed-bar §A–§E (vision); declares nothing qualified.
set -u
cd "$(dirname "$0")"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
LOGDIR="logs"
mkdir -p "$LOGDIR"

echo "=== static checks ==="
# K-SE6: no RNG / wall-clock / threads / floats in phase-2 vision sources.
# (Strip full-line comments first so the check can't trip on prose.)
if grep -vE '^\s*//' se_ingress.zag se_memif.zag se2v_main.zag | grep -nE \
    "_zag_rand|gettimeofday|clock_gettime|thread_create|pthread_create|\bf32\b|\bf64\b|_zag_time"; then
  echo "STATIC_FAIL: banned construct found"; exit 1
fi
echo "static_no_banned_constructs: PASS"
# K-SE5: strength must be caller-declared; the admit path must not compute
# strength from observation bytes. Memif check (as phase 1):
if grep -n "strength\[slot\]=" se_memif.zag | grep -v "strength as u8" ; then
  echo "STATIC_FAIL: strength computed in memif"; exit 1
fi
# Harness check: every mi_observe strength argument must be a literal or an
# index-derived expression — never a payload/record byte. The harness passes
# only literals (50, 60, 70, 80) and index expressions (1+k, 11..34 via the
# st param, 20+f). Fail the scan if a strength arg mentions pay/rec/buf.
if grep -nE "mi_observe\([^)]*(pay|rec\[|buf\[|ba\[|bb\[)" se2v_main.zag; then
  echo "STATIC_FAIL: strength derived from observation bytes"; exit 1
fi
echo "static_strength_declared: PASS"
# bare @imports present
for f in se_ingress.zag se_memif.zag se2v_main.zag; do
  grep -q '^@import(' "$f" || { echo "STATIC_FAIL: $f missing bare @import"; exit 1; }
done
echo "static_bare_imports: PASS"

echo "=== compile twice ==="
"$ZNC" build se2v_main.zag -o se2v_bin_a >"$LOGDIR/build_a.txt" 2>&1 || { echo "BUILD_A_FAIL"; cat "$LOGDIR/build_a.txt"; exit 1; }
"$ZNC" build se2v_main.zag -o se2v_bin_b >"$LOGDIR/build_b.txt" 2>&1 || { echo "BUILD_B_FAIL"; cat "$LOGDIR/build_b.txt"; exit 1; }
sha256sum se2v_bin_a se2v_bin_b | tee "$LOGDIR/build_hashes.txt"
ha=$(sha256sum se2v_bin_a | cut -d' ' -f1)
hb=$(sha256sum se2v_bin_b | cut -d' ' -f1)
if [ "$ha" != "$hb" ]; then echo "BUILD_HASH_MISMATCH"; exit 1; fi
echo "build hashes identical: PASS"

echo "=== harness run A ==="
./se2v_bin_a harness >"$LOGDIR/run_harness_a.txt" 2>&1; rc_a=$?
echo "rc_a=$rc_a"
echo "=== harness run B ==="
./se2v_bin_b harness >"$LOGDIR/run_harness_b.txt" 2>&1; rc_b=$?
echo "rc_b=$rc_b"

echo "=== K-SE1 replay: diff of two full runs ==="
if [ $rc_a -ne 0 ] || [ $rc_b -ne 0 ]; then echo "K-SE1: FAIL (nonzero rc)"; exit 1; fi
if diff -u "$LOGDIR/run_harness_a.txt" "$LOGDIR/run_harness_b.txt" >"$LOGDIR/replay_diff.txt"; then
  echo "K-SE1 replay byte-identical: PASS"
else
  echo "K-SE1: FAIL (output divergence)"; cat "$LOGDIR/replay_diff.txt"; exit 1
fi

echo "=== mechanical CL_CHECK verification (run A) ==="
mismatch=0
while IFS=, read -r tag name actual expected; do
  if [ "$tag" = "CL_CHECK" ] && [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"; mismatch=1
  fi
done < "$LOGDIR/run_harness_a.txt"
if [ $mismatch -ne 0 ]; then echo "MECHANICAL: FAIL"; exit 1; fi
echo "mechanical checks all actual==expected: PASS"

echo "=== ALL SE2V GATES PASSED ==="
