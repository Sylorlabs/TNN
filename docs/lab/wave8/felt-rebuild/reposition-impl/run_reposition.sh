#!/bin/bash
# FELT-REPOSITION runner (PREREG_FELT_REPOSITION.md §16, APPROVED FOR RUN).
# Static gates -> compile both binaries -> 30 native runs (5 arms x 3
# variants x 2 runs) -> sha256 pair check per cell (STOP on mismatch,
# I-R-1) -> independent checker -> verdicts.
# Usage: ./run_reposition.sh [--static-only]
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
W5=~/workspace/tnn-lab/wave5/strength-trial-run/trial
IMPL="$D/../impl"
REC="$IMPL/CALIBRATION_RECORD.md"
RUNS="$D/runs"
fail(){ echo "RUN_FAIL,$1"; exit 1; }
note(){ echo "RUN_NOTE,$1"; }

echo "== static gates =="
# G0. Calibration record: exists, G-C1..G-C3 PASS (F-R-1), predates cells (I-R-8).
# "Predates" uses file BIRTH time: the record must have come into existence
# before the cells (a later mtime touch with unchanged content is not
# backdating; constants-equality below is the content check).
[ -f "$REC" ] || fail "CALIBRATION_RECORD.md absent (I-R-8/F-R-1)"
for g in G-C1 G-C2 G-C3; do
  grep -A3 -- "$g" "$REC" | grep -q "PASS" || fail "F-R-1: $g not PASS in record"
done
rec_birth=$(stat -c %W "$REC")
trial_birth=$(stat -c %W "$D/reposition_trial.zag")
check_birth=$(stat -c %W "$D/reposition_checker.zag")
[ "$rec_birth" -gt 0 ] && [ "$trial_birth" -gt 0 ] && [ "$rec_birth" -lt "$trial_birth" ] \
  || fail "I-R-8: record does not predate trial cells (birth $rec_birth vs $trial_birth)"
[ "$rec_birth" -lt "$check_birth" ] \
  || fail "I-R-8: record does not predate checker (birth $rec_birth vs $check_birth)"
note "calibration record OK (birth-predates cells, G-C1..G-C3 PASS)"
rec_sha=$(sha256sum "$REC" | cut -d' ' -f1)
note "calibration record sha256=$rec_sha (consumed, §10)"
# G1. Trial constants == record (I-R-8), consumed verbatim from V3.
for sym in CAL_ALPHA CAL_BETA CAL_GAMMA; do
  rec=$(grep -E "^${sym}=" "$REC" | head -1 | cut -d= -f2)
  src=$(grep -E "const ${sym}:i32=" "$D/calib_consts.zag" | head -1 | sed 's/.*=//;s/;.*//')
  [ -n "$rec" ] || fail "$sym missing in record"
  [ "$rec" = "$src" ] || fail "I-R-8: $sym trial($src) != record($rec)"
done
cmp -s "$D/calib_consts.zag" "$IMPL/calib_consts.zag" || fail "calib_consts.zag not verbatim V3"
note "constants == record (verbatim V3)"
# G2. Substrate + felt module byte-identical (I-R-7; same feeling, same substrate).
cmp -s "$D/st_memory_core.zag" "$W5/st_memory_core.zag" || fail "I-R-7 st_memory_core"
cmp -s "$D/substrate/cl/common.zag" "$W5/substrate/cl/common.zag" || fail "I-R-7 common.zag"
cmp -s "$D/substrate/R33_NATIVE_SHA256_V2.zag" "$W5/substrate/R33_NATIVE_SHA256_V2.zag" || fail "I-R-7 sha256"
cmp -s "$D/substrate/R33_NATIVE_IO_V1.zag" "$W5/substrate/R33_NATIVE_IO_V1.zag" || fail "I-R-7 nativeio"
cmp -s "$D/felt_v3.zag" "$IMPL/felt_v3.zag" || fail "felt_v3.zag not byte-identical to calibrated V3 module"
note "substrate + felt module byte-identical"
# G3. No RNG tokens (I-R-3) in trial, checker, felt module, consts, substrate.
grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc|shuffle|seed\(' \
  "$D/reposition_trial.zag" "$D/reposition_checker.zag" "$D/felt_v3.zag" \
  "$D/calib_consts.zag" "$D/st_memory_core.zag" "$D/substrate/" >/dev/null 2>&1 \
  && fail "I-R-3: RNG token found"
note "no RNG tokens"
# G4. Bare @import in both mains.
grep -q '^@import' "$D/reposition_trial.zag" || fail "trial import not bare"
grep -q '^@import' "$D/reposition_checker.zag" || fail "checker import not bare"
# G5. I-R-6: felt_* calls only in F's rehearsal selection (trial); checker
#     verification-only allowlist.
python3 - "$D" <<'EOF' || fail "I-R-6 felt_* scope"
import re,sys
D=sys.argv[1]
def callsites(fn, allowed):
    src=open(f"{D}/{fn}").read()
    cur="<top>"
    for i,line in enumerate(src.splitlines(),1):
        m=re.match(r'\s*fn\s+([A-Za-z0-9_]+)\(',line)
        if m: cur=m.group(1)
        if line.strip().startswith("//"): continue
        for mm in re.finditer(r'felt_[A-Za-z0-9_]+',line):
            tok=mm.group(0)
            if tok=="felt_v3": continue
            if cur not in allowed:
                print(f"I-R-6 violation: {tok} in {cur} ({fn}:{i})"); sys.exit(1)
callsites("reposition_trial.zag", {"rp_select_f"})
callsites("reposition_checker.zag", {"ck_scan","ck_a3b"})
print("IR6_OK")
EOF
# G6. Strength-side code reads no rehearsal state: rehearsal tokens only in
#     the rehearsal subsystem + driver sequencing.
python3 - "$D" <<'EOF' || fail "strength-side rehearsal quarantine"
import re,sys
D=sys.argv[1]
src=open(f"{D}/reposition_trial.zag").read()
allowed={"<top>","rp_emit_rehearsal","rp_rehearsal_window","rp_select_f",
         "rp_select_r","rp_select_q","rp_select_fifo","rp_select_c",
         "run_trial","main","rp_write_dump"}
cur="<top>"
for i,line in enumerate(src.splitlines(),1):
    m=re.match(r'\s*fn\s+([A-Za-z0-9_]+)\(',line)
    if m: cur=m.group(1)
    if line.strip().startswith("//"): continue
    for tok in ("REHEARSAL","INTENSITY_READ","rp_select","rp_rehearsal_window","rp_emit_rehearsal"):
        if tok in line and cur not in allowed:
            print(f"quarantine violation: {tok} in {cur} ({i})"); sys.exit(1)
print("QUARANTINE_OK")
EOF
# G7. No direct st_str writes / forbidden strength tokens outside substrate.
if grep -nE 'st_str\[[^]]*\]\s*=' "$D/reposition_trial.zag" "$D/reposition_checker.zag" \
   | grep -v 'st_i32' >/dev/null 2>&1; then
  fail "direct st_str write outside substrate API"
fi
grep -niE 'st_write_strength|st_clear_strength|r_param' \
  "$D/reposition_trial.zag" "$D/reposition_checker.zag" >/dev/null 2>&1 \
  && fail "forbidden strength/R_PARAM token"
note "static gates PASS"

[ "${1:-}" = "--static-only" ] && { echo "STATIC_ONLY_OK"; exit 0; }

echo "== compile =="
cd "$D" || exit 1
"$ZNC" reposition_trial.zag --no-zagd --no-analyze --no-foreground-cache \
  -o reposition_trial_bin || fail "trial compile"
"$ZNC" reposition_checker.zag --no-zagd --no-analyze --no-foreground-cache \
  -o reposition_checker_bin || fail "checker compile"
echo "COMPILE_OK"

echo "== 30 runs =="
mkdir -p "$RUNS"
cd "$RUNS" || exit 1
for arm in f r q fifo c; do
  for variant in 0 1 2; do
    for run in 0 1; do
      dump="L_${arm}_v${variant}_r${run}.bin"
      "$D/reposition_trial_bin" "$arm" "$variant" "$dump" > "stdout_${arm}_v${variant}_r${run}.log" 2>&1 \
        || fail "trial cell failed: $arm v$variant r$run"
      [ -f "$dump" ] || fail "missing dump: $dump"
      note "cell done: $arm v$variant r$run"
    done
    # I-R-1: paired runs must be byte-identical; STOP on mismatch.
    a="L_${arm}_v${variant}_r0.bin"; b="L_${arm}_v${variant}_r1.bin"
    ha=$(sha256sum "$a" | cut -d' ' -f1)
    hb=$(sha256sum "$b" | cut -d' ' -f1)
    [ "$ha" = "$hb" ] || fail "I-R-1: paired byte mismatch for $arm v$variant ($ha != $hb)"
    note "pair OK: $arm v$variant sha256=$ha"
  done
done
echo "PAIRS_OK (15/15 byte-identical)"

echo "== independent checker =="
"$D/reposition_checker_bin" "$RUNS" | tee "$RUNS/checker_output.log"
[ "${PIPESTATUS[0]}" -eq 0 ] || fail "checker reported INVALID"
echo "CHECKER_OK"
echo "RUN_DONE"
