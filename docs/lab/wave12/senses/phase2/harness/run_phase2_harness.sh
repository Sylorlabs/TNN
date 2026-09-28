#!/bin/bash
# Phase-2 cross-cutting harness runner: §G static scans, §F replay
# (double build + hash compare, double harness run + stdout diff),
# §H/§I via the se2 driver, then fresh-process §I verify.
# Prereg: PREREG_SENSES_PHASE2_HARNESS.md (frozen before build).
set -u
cd "$(dirname "$0")"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
P2="$(cd .. && pwd)"
LOGDIR="logs"
mkdir -p "$LOGDIR"

fail() { echo "RUNNER_FAIL: $1"; exit 1; }

# All phase-2 mechanism sources: this dir + audio/vision when landed.
# Substrate is vendored canonical (hashes in VENDORING.md); the scan covers
# track mechanism sources, as in phase 1.
SRCS=$(find "$P2" -name '*.zag' -not -path '*/substrate/*' | sort)
[ -n "$SRCS" ] || fail "no phase-2 sources found"
echo "scanning sources:"; echo "$SRCS"

echo "=== §G static: banned constructs (K-SE6) ==="
# strip full-line and trailing // comments, then scan
if echo "$SRCS" | xargs sed -E 's#//.*$##' | grep -nE \
    '_zag_rand|gettimeofday|clock_gettime|thread_create|pthread_create|_zag_time|\bf32\b|\bf64\b|[0-9]\.[0-9]'; then
  echo "CL_CHECK,se2g-no-banned,0,1" >"$LOGDIR/se2_static.txt"
  fail "K-SE6: banned construct found"
fi
echo "=== §G static: computed strength (K-SE5) ==="
# Admit-path rule: strength is caller-declared only.
# R1: every indexed strength-store write must be the caller-declared form `= <ident> as u8;`
if echo "$SRCS" | xargs grep -nE '\.strength\[' 2>/dev/null | grep -vE '=[[:space:]]*[A-Za-z_][A-Za-z0-9_]* as u8;'; then
  echo "CL_CHECK,se2g-no-banned,1,1" >"$LOGDIR/se2_static.txt"
  echo "CL_CHECK,se2g-no-computed-strength,0,1" >>"$LOGDIR/se2_static.txt"
  fail "K-SE5: strength store write is not caller-declared"
fi
# R2: non-indexed `.strength=` may only be buffer allocation
if echo "$SRCS" | xargs grep -nE '\.strength=' 2>/dev/null | grep -v 'nio_alloc('; then
  echo "CL_CHECK,se2g-no-banned,1,1" >"$LOGDIR/se2_static.txt"
  echo "CL_CHECK,se2g-no-computed-strength,0,1" >>"$LOGDIR/se2_static.txt"
  fail "K-SE5: non-allocation strength assignment"
fi
# R3: in files with an admit path (a `.strength[` write), the strength
# parameter must not participate in arithmetic (no temp-variable laundering)
ADMIT_SRCS=$(echo "$SRCS" | xargs grep -lE '\.strength\[' 2>/dev/null)
if [ -n "$ADMIT_SRCS" ] && echo "$ADMIT_SRCS" | xargs grep -nE '\bstrength[[:space:]]*[-+*/]|[-+*/][[:space:]]*strength\b' 2>/dev/null; then
  echo "CL_CHECK,se2g-no-banned,1,1" >"$LOGDIR/se2_static.txt"
  echo "CL_CHECK,se2g-no-computed-strength,0,1" >>"$LOGDIR/se2_static.txt"
  fail "K-SE5: arithmetic on strength in admit path"
fi
# bare @imports present in every track source
echo "$SRCS" | xargs grep -L '^@import(' | grep . && fail "missing bare @import"
{
  echo "CL_CHECK,se2g-no-banned,1,1"
  echo "CL_CHECK,se2g-no-computed-strength,1,1"
} >"$LOGDIR/se2_static.txt"
echo "static checks: PASS"

echo "=== §F compile twice ==="
"$ZNC" build se2_main.zag -o se2_bin_a >"$LOGDIR/se2_build_a.txt" 2>&1 || { cat "$LOGDIR/se2_build_a.txt"; fail "build A"; }
"$ZNC" build se2_main.zag -o se2_bin_b >"$LOGDIR/se2_build_b.txt" 2>&1 || { cat "$LOGDIR/se2_build_b.txt"; fail "build B"; }
HA=$(sha256sum se2_bin_a | cut -d' ' -f1)
HB=$(sha256sum se2_bin_b | cut -d' ' -f1)
echo "build_a=$HA" >"$LOGDIR/se2_build.txt"
echo "build_b=$HB" >>"$LOGDIR/se2_build.txt"
if [ "$HA" = "$HB" ]; then
  echo "CL_CHECK,se2f-build-hash,1,1" >>"$LOGDIR/se2_build.txt"
  echo "build hashes identical: PASS"
else
  echo "CL_CHECK,se2f-build-hash,0,1" >>"$LOGDIR/se2_build.txt"
  fail "K-SE1: build hash mismatch"
fi

echo "=== §H/§I harness run A (clean state) ==="
rm -rf se2_store
./se2_bin_a harness >"$LOGDIR/se2_run_a.txt" 2>&1; rc_a=$?
echo "rc_a=$rc_a"
echo "=== §H/§I harness run B (clean state) ==="
rm -rf se2_store
./se2_bin_b harness >"$LOGDIR/se2_run_b.txt" 2>&1; rc_b=$?
echo "rc_b=$rc_b"

echo "=== §F K-SE1 replay: diff of two full runs ==="
[ $rc_a -eq 0 ] || fail "harness run A rc=$rc_a"
[ $rc_b -eq 0 ] || fail "harness run B rc=$rc_b"
if diff -q "$LOGDIR/se2_run_a.txt" "$LOGDIR/se2_run_b.txt" >/dev/null; then
  echo "CL_CHECK,se2f-replay-runs,1,1" >"$LOGDIR/se2_replay.txt"
  echo "K-SE1 replay byte-identical: PASS"
else
  echo "CL_CHECK,se2f-replay-runs,0,1" >"$LOGDIR/se2_replay.txt"
  diff "$LOGDIR/se2_run_a.txt" "$LOGDIR/se2_run_b.txt" | head -20
  fail "K-SE1: output divergence"
fi

echo "=== §I fresh-process verify (cross-build: bin B reads bin B state) ==="
./se2_bin_b verify se2_store >"$LOGDIR/se2_verify.txt" 2>&1; rc_v=$?
echo "rc_v=$rc_v"
[ $rc_v -eq 0 ] || { cat "$LOGDIR/se2_verify.txt"; fail "verify rc=$rc_v"; }

echo "=== mechanical CL_CHECK audit (all phase-2 logs) ==="
mismatch=0
while IFS= read -r line; do
  case "$line" in
    CL_CHECK,se2*)
      name=$(echo "$line" | cut -d, -f2); act=$(echo "$line" | cut -d, -f3); exp=$(echo "$line" | cut -d, -f4)
      if [ "$act" != "$exp" ]; then echo "MISMATCH: $name actual=$act expected=$exp"; mismatch=1; fi
      ;;
  esac
done < <(cat "$LOGDIR"/se2_*.txt)
[ $mismatch -eq 0 ] || fail "mechanical check mismatch"
echo "mechanical checks all actual==expected: PASS"

echo "=== counting reporter (155-count aggregation) ==="
# A-E inputs are the independent verifier's reproductions in evidence/
# (vision byte-identical to the vision worker's committed logs; audio has
# no committed logs yet). F-I inputs are this run's own logs.
if ./count_phase2.sh evidence/audio_run_a.txt evidence/vision_run_a.txt \
    "$LOGDIR/se2_static.txt" "$LOGDIR/se2_build.txt" \
    "$LOGDIR/se2_replay.txt" "$LOGDIR/se2_run_a.txt" \
    "$LOGDIR/se2_verify.txt"; then
  echo "=== FULL PHASE-2 BAR: MEETS-PROPOSED-BAR (155/155) ==="
else
  echo "RUNNER_FAIL: 155-count aggregation did not meet the proposed bar"
  exit 1
fi

echo "=== ALL CROSS-CUTTING GATES PASSED ==="
