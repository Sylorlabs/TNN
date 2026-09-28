#!/bin/sh
# run_thincert.sh — RUNTHINCERT-2026-09-20-v1
# Deterministic shell glue for the THINCERT thin certifier (PREREG_THIN_CERTIFIER.md §K3′).
# The Zag certifier cannot spawn processes, so this runner:
#   1. rebuilds thincert from exact source and requires byte-identity with the
#      pinned binary (abort 3 on mismatch — the certifier itself is untrusted),
#   2. builds the trial binary twice from the frozen builddir and requires
#      byte-identity (rebuild_ok),
#   3. runs the interim 8-condition replay matrix (§K3′ interim) and writes the
#      replay evidence file (deterministic key=value lines),
#   4. runs the v2 checker as an informational tripwire (verdict recorded only),
#   5. invokes thincert, which validates the evidence, enforces R1–R7, and
#      writes the attestation.
# No RNG anywhere. Deterministic given inputs.
# usage: run_thincert.sh <thincert.zag> <pinned-thincert-bin> <manifest> <builddir>
#                        <state> <alt-state> <input> <evidence> <attestation>
# exit: 0/1 from thincert; 2 usage/IO; 3 certifier-binary mismatch.
set -u
TCSRC="$1"; TCPIN="$2"; MANIFEST="$3"; BUILDDIR="$4"
STATE="$5"; ALTSTATE="$6"; INPUT="$7"; EVIDENCE="$8"; ATT="$9"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
V2CHECK="/tmp/v2check/rngscan_v2"
work="$(mktemp -d)"
if command -v timeout >/dev/null 2>&1; then TO="timeout 180"; else TO=""; fi

# 1. rebuild certifier, require byte-identity with pinned binary
$TO "$ZNC" build "$TCSRC" -o "$work/thincert_rebuilt" >/dev/null 2>"$work/zc.log" || {
  echo "thincert rebuild failed" >&2; rm -rf "$work"; exit 2; }
if ! cmp -s "$work/thincert_rebuilt" "$TCPIN"; then
  echo "thincert binary mismatch: rebuild differs from pinned binary" >&2
  rm -rf "$work"; exit 3
fi

# 2. build trial binary twice from frozen builddir
$TO "$ZNC" build "$BUILDDIR/variation.zag" -o "$work/trial1" >/dev/null 2>>"$work/zc.log" || {
  echo "trial build failed" >&2; rm -rf "$work"; exit 2; }
$TO "$ZNC" build "$BUILDDIR/variation.zag" -o "$work/trial2" >/dev/null 2>>"$work/zc.log" || {
  echo "trial rebuild failed" >&2; rm -rf "$work"; exit 2; }
rebuild_ok=0
if cmp -s "$work/trial1" "$work/trial2"; then rebuild_ok=1; fi
TRIAL="$work/trial1"

# 3. interim 8-condition replay matrix
$TO "$TRIAL" "$STATE" "$INPUT" >"$work/out1.bin" 2>"$work/e1"; r1=$?
$TO "$TRIAL" "$STATE" "$INPUT" >"$work/out2.bin" 2>"$work/e2"; r2=$?
MALLOC_PERTURB_=165 $TO "$TRIAL" "$STATE" "$INPUT" >"$work/out3.bin" 2>"$work/e3"; r3=$?
MALLOC_PERTURB_=255 $TO "$TRIAL" "$STATE" "$INPUT" >"$work/out4.bin" 2>"$work/e4"; r4=$?
# shellcheck disable=SC2086
BLOAT="$(for i in $(seq 1 100); do printf 'TCBLOAT%03d=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ' "$i"; done)"
env $BLOAT $TO "$TRIAL" "$STATE" "$INPUT" >"$work/out5.bin" 2>"$work/e5"; r5=$?
(cd /tmp && $TO "$TRIAL" "$STATE" "$INPUT" >"$work/out6.bin" 2>"$work/e6"); r6=$?
$TO "$TRIAL" "$STATE" "$INPUT" < /dev/null >"$work/out7.bin" 2>"$work/e7"; r7=$?
$TO "$TRIAL" "$ALTSTATE" "$INPUT" >"$work/out8.bin" 2>"$work/e8"; r8=$?
exit_ok=1
for r in "$r1" "$r2" "$r3" "$r4" "$r5" "$r6" "$r7" "$r8"; do
  if [ "$r" -ne 0 ]; then exit_ok=0; fi
done
byte_identical=0
if [ "$exit_ok" -eq 1 ] && cmp -s "$work/out1.bin" "$work/out2.bin" \
   && cmp -s "$work/out1.bin" "$work/out3.bin" \
   && cmp -s "$work/out1.bin" "$work/out4.bin" \
   && cmp -s "$work/out1.bin" "$work/out5.bin" \
   && cmp -s "$work/out1.bin" "$work/out6.bin" \
   && cmp -s "$work/out1.bin" "$work/out7.bin"; then byte_identical=1; fi
varies=0
if [ "$exit_ok" -eq 1 ] && ! cmp -s "$work/out1.bin" "$work/out8.bin"; then varies=1; fi

# 4. v2 tripwire (informational only)
tripwire_v2="ERROR"
if [ -x "$V2CHECK" ]; then
  # v2 expects a pre-existing evidence file; write the interim evidence for it
  {
    echo "replay_evidence=v1"
    echo "byte_identical=$byte_identical"
    echo "varies_with_state=$varies"
    echo "state_words=0"
    echo "exit_ok=$exit_ok"
    echo "rebuild_ok=$rebuild_ok"
    echo "runs=8"
  } >"$work/v2ev"
  "$V2CHECK" "$BUILDDIR/variation.zag" "$TRIAL" "$work/v2ev" "$work/v2att" >/dev/null 2>&1
  v2rc=$?
  if [ "$v2rc" -eq 0 ]; then tripwire_v2="PASS"; elif [ "$v2rc" -eq 1 ]; then tripwire_v2="FAIL"; fi
fi

# 5. evidence + certifier
{
  echo "byte_identical=$byte_identical"
  echo "varies_with_state=$varies"
  echo "exit_ok=$exit_ok"
  echo "rebuild_ok=$rebuild_ok"
  echo "runs=8"
  echo "tripwire_v2=$tripwire_v2"
} >"$EVIDENCE"
rm -f "$ATT"
"$work/thincert_rebuilt" "$MANIFEST" "$BUILDDIR" "$TRIAL" "$EVIDENCE" "$ATT"
rc=$?
rm -rf "$work"
exit "$rc"
