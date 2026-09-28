#!/bin/bash
# Senses phase-1 qualification runner.
# Prereg: PREREG_SENSES_PHASE1.md (frozen before build).
set -u
cd "$(dirname "$0")"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
LOGDIR="logs"
mkdir -p "$LOGDIR"

echo "=== static checks ==="
# K-SE6: no RNG / wall-clock / threads / floats in phase-1 sources.
# (Strip full-line comments first so the check can't trip on prose.)
if grep -vE '^\s*//' se_ingress.zag se_memif.zag se_main.zag | grep -nE \
    "_zag_rand|gettimeofday|clock_gettime|thread_create|pthread_create|\bf32\b|\bf64\b|_zag_time"; then
  echo "STATIC_FAIL: banned construct found"; exit 1
fi
echo "static_no_banned_constructs: PASS"
# K-SE5: strength must be caller-declared; the admit path must not compute
# strength from observation bytes. Check: no arithmetic assigning to
# strength fields from payload bytes in se_memif.zag.
if grep -n "strength\[slot\]=" se_memif.zag | grep -v "strength as u8" ; then
  echo "STATIC_FAIL: strength computed in memif"; exit 1
fi
echo "static_strength_declared: PASS"
# bare @imports present
for f in se_ingress.zag se_memif.zag se_main.zag; do
  grep -q '^@import(' "$f" || { echo "STATIC_FAIL: $f missing bare @import"; exit 1; }
done
echo "static_bare_imports: PASS"

echo "=== compile twice ==="
"$ZNC" build se_main.zag -o se_bin_a >"$LOGDIR/build_a.txt" 2>&1 || { echo "BUILD_A_FAIL"; cat "$LOGDIR/build_a.txt"; exit 1; }
"$ZNC" build se_main.zag -o se_bin_b >"$LOGDIR/build_b.txt" 2>&1 || { echo "BUILD_B_FAIL"; cat "$LOGDIR/build_b.txt"; exit 1; }
sha256sum se_bin_a se_bin_b | tee "$LOGDIR/build_hashes.txt"

echo "=== harness run A ==="
rm -rf se_p1_store
./se_bin_a harness >"$LOGDIR/run_harness_a.txt" 2>&1; rc_a=$?
echo "rc_a=$rc_a"
echo "=== harness run B ==="
rm -rf se_p1_store
./se_bin_b harness >"$LOGDIR/run_harness_b.txt" 2>&1; rc_b=$?
echo "rc_b=$rc_b"

echo "=== K-SE1 replay: diff of two full runs ==="
if [ $rc_a -ne 0 ] || [ $rc_b -ne 0 ]; then echo "K-SE1: FAIL (nonzero rc)"; exit 1; fi
if diff -u "$LOGDIR/run_harness_a.txt" "$LOGDIR/run_harness_b.txt" >"$LOGDIR/replay_diff.txt"; then
  echo "K-SE1 replay byte-identical: PASS"
else
  echo "K-SE1: FAIL (output divergence)"; cat "$LOGDIR/replay_diff.txt"; exit 1
fi

echo "=== mechanical CL_CHECK verification (run A) ==="
bad=$(grep -c "^CL_CHECK,.*,.*," "$LOGDIR/run_harness_a.txt" | true)
mismatch=0
while IFS=, read -r tag name actual expected; do
  if [ "$tag" = "CL_CHECK" ] && [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"; mismatch=1
  fi
done < "$LOGDIR/run_harness_a.txt"
if [ $mismatch -ne 0 ]; then echo "MECHANICAL: FAIL"; exit 1; fi
echo "mechanical checks all actual==expected: PASS"

echo "=== K-SE7 fresh-process verify ==="
# harness A already saved state into se_p1_store; verify with binary B (cross-build)
./se_bin_b verify >"$LOGDIR/run_verify.txt" 2>&1; rc_v=$?
echo "rc_v=$rc_v"
if [ $rc_v -ne 0 ]; then echo "K-SE7: FAIL (nonzero rc)"; cat "$LOGDIR/run_verify.txt"; exit 1; fi
mismatch=0
while IFS=, read -r tag name actual expected; do
  if [ "$tag" = "CL_CHECK" ] && [ "$actual" != "$expected" ]; then
    echo "VERIFY MISMATCH: $name actual=$actual expected=$expected"; mismatch=1
  fi
done < "$LOGDIR/run_verify.txt"
if [ $mismatch -ne 0 ]; then echo "K-SE7: FAIL"; exit 1; fi
echo "K-SE7 save/reload byte-identical: PASS"

echo "=== ALL PHASE-1 GATES PASSED ==="
