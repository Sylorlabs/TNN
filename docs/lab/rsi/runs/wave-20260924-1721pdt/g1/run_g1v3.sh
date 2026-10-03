#!/bin/bash
# run_g1v3.sh - build and run the G1 v3 sunshafts trial (wave-20260924-1721pdt).
# Pure Zag, zero RNG, no Python anywhere.
# Order: static checks -> toolchain pin -> compile -> baseline byte-identity
# gate -> geometric validator gate -> v3 renders x3 (KB1) -> KB8 cost ->
# verifier kill bars KB2..KB7 (validator/verifier *_KEPT cross-check).
# Frozen evaluation order inside the variant (short-circuiting for cost):
# sky/r check -> sunward march + clarity gate -> fan marches only for gate
# passers -> delta predicate -> lift. The tripwire asserts the clarity-gate
# pass fraction lands near 10 percent (the measured-quantile design).
set -u
D="$(cd "$(dirname "$0")" && pwd)"
REPO="$HOME/workspace/tnn-rsi"
ZNC_SRC="$REPO/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
ZNC_RUN="$HOME/workspace/tmp_g1v3/znc_run"
BIN="$D/bin"
EV="$D/evidence"
mkdir -p "$BIN" "$EV" "$(dirname "$ZNC_RUN")"
fail=0
note() { echo "RUNNER: $1"; }

note "prereg commit (frozen before any G1 v3 code existed): acf7cedce"
git -C "$REPO" log --oneline -1 acf7cedce 2>/dev/null || { note "FAIL prereg commit acf7cedce not found"; fail=1; }
note "sign-correction addendum commit (before any v3 implementation): 1da140387"
git -C "$REPO" log --oneline -1 1da140387 2>/dev/null || { note "FAIL addendum commit 1da140387 not found"; fail=1; }
if git -C "$REPO" merge-base --is-ancestor acf7cedce 1da140387 2>/dev/null; then
  note "commit order OK (prereg strictly before addendum)"
else
  note "FAIL commit order: addendum is not a descendant of the prereg"; fail=1
fi

# --- static checks: no interpreter, no randomness in new sources ---
if ls "$D"/*.py >/dev/null 2>&1; then note "FAIL py file in g1 dir"; fail=1; else note "no-pyfile check OK"; fi
if sed 's|//.*||' "$D"/g1_sunshafts_v3.zag "$D"/g1_validate.zag "$D"/g1_verify_v3.zag "$D"/r8c_baseline.zag | grep -ni 'python' >/dev/null 2>&1; then
  note "FAIL py token in zag sources"; fail=1
else
  note "no-py-in-zag check OK"
fi
if sed 's|#.*||' "$D/run_g1v3.sh" | grep -niE '(^|[;&|[:space:]])python[0-9]*([[:space:]]|$|;)' >/dev/null 2>&1; then
  note "FAIL py invocation in runner"; fail=1
else
  note "no-py-in-runner check OK"
fi
if sed 's|//.*||' "$D"/g1_sunshafts_v3.zag "$D"/g1_validate.zag "$D"/g1_verify_v3.zag "$D"/r8c_baseline.zag | grep -niE '\\brand[[:space:]]*\\(|random[[:space:]]*\\(|srand|\\btime[[:space:]]*\\(|\\bclock[[:space:]]*\\(' >/dev/null 2>&1; then
  note "FAIL randomness/time call grep found a hit"; fail=1
else
  note "no-randomness static check OK"
fi

# --- toolchain pin (workspace-local copy, never /tmp) ---
cp "$ZNC_SRC" "$ZNC_RUN" && chmod +x "$ZNC_RUN"
if [ "$(sha256sum "$ZNC_RUN" | cut -d' ' -f1)" != "498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef" ]; then
  note "FAIL toolchain hash mismatch"; fail=1
else
  note "toolchain pinned OK (498abcb5)"
fi
if [ "$(sha256sum "$D/sub/R33_NATIVE_IO_V1.zag" | cut -d' ' -f1)" != "e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8" ]; then
  note "FAIL vendored IO substrate hash mismatch"; fail=1
else
  note "IO substrate pinned OK (e6379ddb)"
fi

# --- compile ---
"$ZNC_RUN" "$D/r8c_baseline.zag" -o "$BIN/r8c_baseline" --no-analyze 2>"$EV/evidence_compile_baseline.txt"
[ $? -ne 0 ] && { note "FAIL baseline compile"; fail=1; } || note "baseline compile OK"
"$ZNC_RUN" "$D/g1_sunshafts_v3.zag" -o "$BIN/g1_v3" --no-analyze 2>"$EV/evidence_compile_v3.txt"
[ $? -ne 0 ] && { note "FAIL v3 compile"; fail=1; } || note "v3 compile OK"
"$ZNC_RUN" "$D/g1_validate.zag" -o "$BIN/g1_validate" --no-analyze 2>"$EV/evidence_compile_validate.txt"
[ $? -ne 0 ] && { note "FAIL validator compile"; fail=1; } || note "validator compile OK"
"$ZNC_RUN" "$D/g1_verify_v3.zag" -o "$BIN/g1_verify_v3" --no-analyze 2>"$EV/evidence_compile_verify.txt"
[ $? -ne 0 ] && { note "FAIL verifier compile"; fail=1; } || note "verifier compile OK"
if [ $fail -ne 0 ]; then note "OVERALL: FAIL (build)"; exit 1; fi

# --- baseline byte-identity gate (frozen S14 hash) ---
t0=$(date +%s%N)
"$BIN/r8c_baseline" "$EV/base.bmp" "$EV/base_trace.md" >"$EV/evidence_base_run.txt" 2>&1
t1=$(date +%s%N)
base_ms=$(( (t1 - t0) / 1000000 ))
bh=$(sha256sum "$EV/base.bmp" | cut -d' ' -f1)
if [ "$bh" = "e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d" ]; then
  note "baseline byte-identity gate PASS ($bh)"
else
  note "FAIL baseline hash $bh"; fail=1
fi
if [ $fail -ne 0 ]; then note "OVERALL: FAIL (baseline gate)"; exit 1; fi

# --- geometric validator gate (must pass before the verifier runs) ---
"$BIN/g1_validate" >"$EV/evidence_validator.txt" 2>&1
vrc=$?
sed 's/^/RUNNER: validator: /' "$EV/evidence_validator.txt"
if [ $vrc -ne 0 ]; then note "FAIL validator rc=$vrc"; fail=1; fi
if ! grep -q "^VALIDATOR_OVERALL,PASS$" "$EV/evidence_validator.txt"; then
  note "FAIL validator overall not PASS"; fail=1
else
  note "geometric validator gate PASS"
fi
if [ $fail -ne 0 ]; then note "OVERALL: FAIL (validator gate)"; exit 1; fi

# --- variant renders: v3 x3 (KB1 determinism) ---
t0=$(date +%s%N)
for i in 1 2 3; do
  "$BIN/g1_v3" "$EV/var_v3_$i.bmp" "$EV/var_v3_trace_$i.md" >"$EV/evidence_v3_run$i.txt" 2>&1
  [ $? -ne 0 ] && { note "FAIL v3 run $i rc"; fail=1; }
done
t1=$(date +%s%N)
v3_ms=$(( (t1 - t0) / 1000000 / 3 ))
echo "RUNNER: wall_ms baseline=$base_ms v3_avg=$v3_ms" | tee "$EV/evidence_walltime.txt"

# --- required stdout line present ---
if grep -q "^G1v3 shafts: N=12 K=7 gated_px=[0-9][0-9]* clarity_pass=[0-9][0-9]* delta_pass=[0-9][0-9]* lifted_px=[0-9][0-9]*$" "$EV/evidence_v3_run1.txt"; then
  note "G1v3 stdout line OK"
  grep "^G1v3 shafts:" "$EV/evidence_v3_run1.txt" | sed 's/^/RUNNER: /'
else
  note "FAIL G1v3 stdout line missing"; fail=1
fi
grep "^G1.7:" "$EV/var_v3_trace_1.md" | sed 's/^/RUNNER: trace: /' || true

# --- tripwire: clarity-gate pass fraction near 10 percent (50..150 per mille) ---
gated=$(grep -o "gated_px=[0-9]*" "$EV/evidence_v3_run1.txt" | cut -d= -f2)
clarity=$(grep -o "clarity_pass=[0-9]*" "$EV/evidence_v3_run1.txt" | cut -d= -f2)
if [ -n "$gated" ] && [ -n "$clarity" ] && [ "$gated" -gt 0 ]; then
  pm=$(( clarity * 1000 / gated ))
  echo "RUNNER: tripwire clarity per_mille=$pm (gated=$gated clarity=$clarity)" | tee "$EV/evidence_tripwire.txt"
  if [ "$pm" -ge 50 ] && [ "$pm" -le 150 ]; then
    note "tripwire PASS (clarity pass fraction near 10 percent)"
  else
    note "FAIL tripwire: clarity per_mille=$pm outside [50,150]"; fail=1
  fi
else
  note "FAIL tripwire: could not parse predicate counts"; fail=1
fi

# --- KB1 determinism: 3 byte-identical reruns ---
h1=$(sha256sum "$EV/var_v3_1.bmp" | cut -d' ' -f1)
h2=$(sha256sum "$EV/var_v3_2.bmp" | cut -d' ' -f1)
h3=$(sha256sum "$EV/var_v3_3.bmp" | cut -d' ' -f1)
if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then
  note "KB1 determinism PASS ($h1)"
else
  note "FAIL KB1 rerun hashes differ: $h1 $h2 $h3"; fail=1
fi
echo "RUNNER: v3_sha256=$h1" | tee "$EV/evidence_v3_sha.txt"

# --- KB8 cost: v3 total wall <= 3.0x baseline total wall ---
if [ "$v3_ms" -le $(( base_ms * 3 )) ]; then
  note "KB8 cost PASS (v3 ${v3_ms}ms <= 3x baseline ${base_ms}ms)"
else
  note "FAIL KB8 cost (v3 ${v3_ms}ms > 3x baseline ${base_ms}ms)"; fail=1
fi

# --- verifier kill bars KB2..KB7 ---
"$BIN/g1_verify_v3" "$EV/base.bmp" "$EV/var_v3_1.bmp" >"$EV/evidence_verify_v3.txt" 2>&1
vrc=$?
note "verifier rc=$vrc"
sed 's/^/RUNNER: verify: /' "$EV/evidence_verify_v3.txt"
[ $vrc -ne 0 ] && { note "FAIL verifier reported bar failure"; fail=1; }

# --- validator/verifier *_KEPT cross-check (same frozen point sets) ---
for k in WEDGE_KEPT OFFWEDGE_KEPT TERRAIN_KEPT RADCUT_KEPT; do
  a=$(grep "^$k," "$EV/evidence_validator.txt" | cut -d, -f2)
  b=$(grep "^$k," "$EV/evidence_verify_v3.txt" | cut -d, -f2)
  if [ "$a" = "$b" ] && [ -n "$a" ]; then
    note "KEPT cross-check $k OK ($a)"
  else
    note "FAIL KEPT cross-check $k: validator=$a verifier=$b"; fail=1
  fi
done

if [ $fail -ne 0 ]; then note "OVERALL: FAIL"; exit 1; fi
note "OVERALL: harness checks complete (verdict decided by frozen bars, see VERDICT_G1_V3.md)"
