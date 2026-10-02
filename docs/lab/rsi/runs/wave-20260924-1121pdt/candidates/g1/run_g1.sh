#!/bin/bash
# run_g1.sh - build and run the G1 sunshafts trial (wave-20260924-1121pdt).
# Pure Zag, zero RNG, no Py interpreter anywhere.
# Static checks + compile + baseline byte-identity gate + N in {6,12,24}
# renders + KB1 determinism (3 byte-identical N=12 reruns) + KB8 cost +
# verifier kill bars KB2..KB7 (with frozen point-set asserts).
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC_SRC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
ZNC_TMP="/tmp/znc_g1_run"
BIN="$D/bin"
EV="$D/evidence"
mkdir -p "$BIN" "$EV"
fail=0
note() { echo "RUNNER: $1"; }

note "prereg commit (frozen before any G1 code existed):"
git -C "$HOME/workspace/tnn-rsi" log --oneline -1 68c3bb868 2>/dev/null || { note "FAIL prereg commit 68c3bb868 not found"; fail=1; }

# --- static checks: no interpreter, no randomness in new sources ---
if ls "$D"/*.py >/dev/null 2>&1; then note "FAIL py file in g1 dir"; fail=1; else note "no-pyfile check OK"; fi
if sed 's|//.*||' "$D/g1_sunshafts.zag" "$D/g1_n6.zag" "$D/g1_n24.zag" "$D/g1_verify.zag" "$D/r8c_baseline.zag" | grep -ni 'python' >/dev/null 2>&1; then
  note "FAIL py token in zag sources"; fail=1
else
  note "no-py-in-zag check OK"
fi
if sed 's|#.*||' "$D/run_g1.sh" | grep -niE '(^|[;&|[:space:]])python[0-9]*([[:space:]]|$|;)' >/dev/null 2>&1; then
  note "FAIL py invocation in runner"; fail=1
else
  note "no-py-in-runner check OK"
fi
if sed 's|//.*||' "$D/g1_sunshafts.zag" "$D/g1_n6.zag" "$D/g1_n24.zag" "$D/g1_verify.zag" "$D/r8c_baseline.zag" | grep -niE '\brand[[:space:]]*\(|random[[:space:]]*\(|srand|\btime[[:space:]]*\(|\bclock[[:space:]]*\(' >/dev/null 2>&1; then
  note "FAIL randomness/time call grep found a hit"; fail=1
else
  note "no-randomness static check OK"
fi

# --- the three variant sources differ only in the frozen N constant ---
if [ "$(diff "$D/g1_sunshafts.zag" "$D/g1_n6.zag" | grep -c '^[<>]')" = "2" ] && [ "$(diff "$D/g1_sunshafts.zag" "$D/g1_n24.zag" | grep -c '^[<>]')" = "2" ]; then
  note "variant sources differ only in g1_n constant OK"
else
  note "FAIL variant sources differ by more than the N constant"; fail=1
fi

# --- toolchain pin ---
cp "$ZNC_SRC" "$ZNC_TMP" && chmod +x "$ZNC_TMP"
if [ "$(sha256sum "$ZNC_TMP" | cut -d' ' -f1)" != "498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef" ]; then
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
"$ZNC_TMP" "$D/r8c_baseline.zag" -o "$BIN/r8c_baseline" 2>"$EV/evidence_compile_baseline.txt"
[ $? -ne 0 ] && { note "FAIL baseline compile"; fail=1; } || note "baseline compile OK"
"$ZNC_TMP" "$D/g1_sunshafts.zag" -o "$BIN/g1_n12" 2>"$EV/evidence_compile_n12.txt"
[ $? -ne 0 ] && { note "FAIL n12 compile"; fail=1; } || note "n12 compile OK"
"$ZNC_TMP" "$D/g1_n6.zag" -o "$BIN/g1_n6" 2>"$EV/evidence_compile_n6.txt"
[ $? -ne 0 ] && { note "FAIL n6 compile"; fail=1; } || note "n6 compile OK"
"$ZNC_TMP" "$D/g1_n24.zag" -o "$BIN/g1_n24" 2>"$EV/evidence_compile_n24.txt"
[ $? -ne 0 ] && { note "FAIL n24 compile"; fail=1; } || note "n24 compile OK"
"$ZNC_TMP" "$D/g1_verify.zag" -o "$BIN/g1_verify" 2>"$EV/evidence_compile_verify.txt"
[ $? -ne 0 ] && { note "FAIL verifier compile"; fail=1; } || note "verifier compile OK"
if [ $fail -ne 0 ]; then note "OVERALL: FAIL (build)"; exit 1; fi

# --- baseline byte-identity gate (frozen hash e4f65557...) ---
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

# --- variant renders: N=6 x1, N=12 x3 (KB1), N=24 x1 ---
t0=$(date +%s%N)
"$BIN/g1_n6" "$EV/var_n6.bmp" "$EV/var_n6_trace.md" >"$EV/evidence_n6_run.txt" 2>&1
[ $? -ne 0 ] && { note "FAIL n6 run rc"; fail=1; }
t1=$(date +%s%N)
n6_ms=$(( (t1 - t0) / 1000000 ))
t0=$(date +%s%N)
for i in 1 2 3; do
  "$BIN/g1_n12" "$EV/var_n12_$i.bmp" "$EV/var_n12_trace_$i.md" >"$EV/evidence_n12_run$i.txt" 2>&1
  [ $? -ne 0 ] && { note "FAIL n12 run $i rc"; fail=1; }
done
t1=$(date +%s%N)
n12_ms=$(( (t1 - t0) / 1000000 / 3 ))
t0=$(date +%s%N)
"$BIN/g1_n24" "$EV/var_n24.bmp" "$EV/var_n24_trace.md" >"$EV/evidence_n24_run.txt" 2>&1
[ $? -ne 0 ] && { note "FAIL n24 run rc"; fail=1; }
t1=$(date +%s%N)
n24_ms=$(( (t1 - t0) / 1000000 ))
echo "RUNNER: wall_ms baseline=$base_ms n6=$n6_ms n12_avg=$n12_ms n24=$n24_ms" | tee "$EV/evidence_walltime.txt"

# --- required stdout line present ---
for tag in "n6:6" "n12:12" "n24:24"; do
  f="${tag%%:*}"; n="${tag##*:}"
  if grep -q "^G1 shafts: N=$n sky_px=[0-9][0-9]*$" "$EV/evidence_${f}_run.txt" 2>/dev/null || grep -q "^G1 shafts: N=$n sky_px=[0-9][0-9]*$" "$EV/evidence_${f}_run1.txt" 2>/dev/null; then
    note "G1 stdout line OK for N=$n"
  else
    note "FAIL G1 stdout line missing for N=$n"; fail=1
  fi
done

# --- KB1 determinism: 3 byte-identical N=12 reruns ---
h1=$(sha256sum "$EV/var_n12_1.bmp" | cut -d' ' -f1)
h2=$(sha256sum "$EV/var_n12_2.bmp" | cut -d' ' -f1)
h3=$(sha256sum "$EV/var_n12_3.bmp" | cut -d' ' -f1)
if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then
  note "KB1 determinism PASS ($h1)"
else
  note "FAIL KB1 rerun hashes differ: $h1 $h2 $h3"; fail=1
fi
echo "RUNNER: n12_sha256=$h1" | tee "$EV/evidence_n12_sha.txt"
echo "RUNNER: n6_sha256=$(sha256sum "$EV/var_n6.bmp" | cut -d' ' -f1)" | tee -a "$EV/evidence_n12_sha.txt"
echo "RUNNER: n24_sha256=$(sha256sum "$EV/var_n24.bmp" | cut -d' ' -f1)" | tee -a "$EV/evidence_n12_sha.txt"

# --- KB8 cost: N=12 total wall <= 3.0x baseline total wall ---
# (shaft pass is strictly inside the variant total, so this implies the bar)
if [ "$n12_ms" -le $(( base_ms * 3 )) ]; then
  note "KB8 cost PASS (n12 ${n12_ms}ms <= 3x baseline ${base_ms}ms)"
else
  note "FAIL KB8 cost (n12 ${n12_ms}ms > 3x baseline ${base_ms}ms)"; fail=1
fi

# --- verifier kill bars KB2..KB7 for N in {6,12,24} ---
for n in 6 12 24; do
  if [ "$n" = "12" ]; then vbmp="$EV/var_n12_1.bmp"; else vbmp="$EV/var_n${n}.bmp"; fi
  "$BIN/g1_verify" "$EV/base.bmp" "$vbmp" >"$EV/evidence_verify_n$n.txt" 2>&1
  vrc=$?
  note "verifier N=$n rc=$vrc"
  sed 's/^/RUNNER: verify: /' "$EV/evidence_verify_n$n.txt"
done

if [ $fail -ne 0 ]; then note "OVERALL: FAIL"; exit 1; fi
note "OVERALL: harness checks complete (verdict decided by frozen bars, see VERDICT_G1.md)"
