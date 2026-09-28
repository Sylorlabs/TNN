#!/bin/bash
# Senses phase-2 AUDIO qualification runner.
# Prereg: PREREG_SENSES_PHASE2_AUDIO.md (frozen pre-build) + AMENDMENT-01.
set -u
cd "$(dirname "$0")"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
LOGDIR="logs"
mkdir -p "$LOGDIR"

echo "=== static checks (K-SE5/K-SE6) ==="
# K-SE6: no RNG / wall-clock / threads / floats (strip full-line comments).
if grep -vE '^\s*//' se2a_ingress.zag se2a_memif.zag se2a_main.zag | grep -nE \
    "_zag_rand|gettimeofday|clock_gettime|thread_create|pthread_create|\bf32\b|\bf64\b|_zag_time"; then
  echo "STATIC_FAIL: banned construct found"; exit 1
fi
echo "static_no_banned_constructs: PASS"
# K-SE5: strength caller-declared only; no arithmetic on observation bytes
# feeds strength. The memif copy must match the phase-1 gate exactly.
if grep -n "strength\[slot\]=" se2a_memif.zag | grep -v "strength as u8" ; then
  echo "STATIC_FAIL: strength computed in memif"; exit 1
fi
if grep -vE '^\s*//' se2a_main.zag | grep -nE "strength.*(pay|rec\[|rA\[|rB\[|rb\[)"; then
  echo "STATIC_FAIL: strength derived from observation bytes"; exit 1
fi
echo "static_strength_declared: PASS"
for f in se2a_ingress.zag se2a_memif.zag se2a_main.zag; do
  grep -q '^@import(' "$f" || { echo "STATIC_FAIL: $f missing bare @import"; exit 1; }
done
echo "static_bare_imports: PASS"

echo "=== compile twice ==="
"$ZNC" build se2a_main.zag -o se2a_bin_a >"$LOGDIR/build_a.txt" 2>&1 || { echo "BUILD_A_FAIL"; cat "$LOGDIR/build_a.txt"; exit 1; }
"$ZNC" build se2a_main.zag -o se2a_bin_b >"$LOGDIR/build_b.txt" 2>&1 || { echo "BUILD_B_FAIL"; cat "$LOGDIR/build_b.txt"; exit 1; }
sha256sum se2a_bin_a se2a_bin_b | tee "$LOGDIR/build_hashes.txt"
ha=$(sha256sum se2a_bin_a | cut -d' ' -f1); hb=$(sha256sum se2a_bin_b | cut -d' ' -f1)
if [ "$ha" != "$hb" ]; then echo "BUILD_HASH_MISMATCH: FAIL"; exit 1; fi
echo "two-build identical hash: PASS"

echo "=== harness run A ==="
rm -rf se2a_store se2a_d??
./se2a_bin_a harness >"$LOGDIR/run_harness_a.txt" 2>&1; rc_a=$?
echo "rc_a=$rc_a"
echo "=== harness run B ==="
rm -rf se2a_store se2a_d??
./se2a_bin_b harness >"$LOGDIR/run_harness_b.txt" 2>&1; rc_b=$?
echo "rc_b=$rc_b"

echo "=== K-SE1 replay: diff of two full runs ==="
if [ $rc_a -ne 0 ] || [ $rc_b -ne 0 ]; then echo "K-SE1: FAIL (nonzero rc)"; exit 1; fi
if diff -u "$LOGDIR/run_harness_a.txt" "$LOGDIR/run_harness_b.txt" >"$LOGDIR/replay_diff.txt"; then
  echo "K-SE1 replay byte-identical: PASS"
else
  echo "K-SE1: FAIL (output divergence)"; cat "$LOGDIR/replay_diff.txt"; exit 1
fi

echo "=== mechanical CL_CHECK verification (run A) ==="
mismatch=0; total=0
while IFS=, read -r tag name actual expected; do
  if [ "$tag" = "CL_CHECK" ]; then
    total=$((total+1))
    if [ "$actual" != "$expected" ]; then
      echo "MISMATCH: $name actual=$actual expected=$expected"; mismatch=1
    fi
  fi
done < "$LOGDIR/run_harness_a.txt"
echo "total CL_CHECK lines: $total"
if [ $mismatch -ne 0 ]; then echo "MECHANICAL: FAIL"; exit 1; fi
echo "mechanical checks all actual==expected: PASS"

echo "=== K-SE7 fresh-process verify (binary B on run-B store) ==="
./se2a_bin_b verify >"$LOGDIR/run_verify.txt" 2>&1; rc_v=$?
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

echo "=== per-section tallies (run A) ==="
for sec in "-a" "-b" "-c" "-d" "-e"; do
  n=$(grep -c "^CL_CHECK,se2a${sec}" "$LOGDIR/run_harness_a.txt" || true)
  echo "section $sec: $n check lines (all actual==expected per mechanical gate)"
done

echo "=== ALL PHASE-2 AUDIO GATES PASSED ==="
