#!/bin/bash
# run_d19.sh - build and run the D19 focus-plane detail trial.
# Pure Zag, zero RNG, no Py interpreter anywhere.
# Static checks + compile + baseline byte-identity gate + 3 byte-identical
# variant runs + D19 dab-budget gate + verifier kill bars KB2..KB5.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC_SRC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
ZNC_TMP="/tmp/znc_d19_run"
BIN="$D/bin"
EV="$D/evidence"
mkdir -p "$BIN" "$EV"
fail=0
note() { echo "RUNNER: $1"; }

note "prereg commit (frozen before any D19 code existed):"
git -C "$HOME/workspace/tnn-rsi" log --oneline -1 35f81a256 2>/dev/null || { note "FAIL prereg commit 35f81a256 not found"; fail=1; }

# --- static checks: no interpreter, no randomness in new sources ---
# 1. no python files in the run dir, ever
if ls "$D"/*.py >/dev/null 2>&1; then note "FAIL py file in run dir"; fail=1; else note "no-pyfile check OK"; fi
# 2. no python token in comment-stripped authored zag sources
#    (the vendored substrate's single mention is its own purity comment,
#    line 17, covered by the pinned e6379ddb hash above)
if sed 's|//.*||' "$D/s19_focus.zag" "$D/s19_verify.zag" "$D/r8c_baseline.zag" | grep -ni 'python' >/dev/null 2>&1; then
  note "FAIL py token in zag sources"; fail=1
else
  note "no-py-in-zag check OK"
fi
# 3. no python command invocation in the runner itself (comments stripped)
if sed 's|#.*||' "$D/run_d19.sh" | grep -niE '(^|[;&|[:space:]])python[0-9]*([[:space:]]|$|;)' >/dev/null 2>&1; then
  note "FAIL py invocation in runner"; fail=1
else
  note "no-py-in-runner check OK"
fi
# 4. no randomness/time calls in comment-stripped zag sources
#    (string literals like the r8c trace prose "no clock" are not calls)
if sed 's|//.*||' "$D/s19_focus.zag" "$D/s19_verify.zag" "$D/r8c_baseline.zag" | grep -niE '\brand[[:space:]]*\(|random[[:space:]]*\(|srand|\btime[[:space:]]*\(|\bclock[[:space:]]*\(' >/dev/null 2>&1; then
  note "FAIL randomness/time call grep found a hit"; fail=1
else
  note "no-randomness static check OK"
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
if [ $? -ne 0 ]; then note "FAIL baseline compile"; fail=1; else note "baseline compile OK"; fi
"$ZNC_TMP" "$D/s19_focus.zag" -o "$BIN/s19_focus" 2>"$EV/evidence_compile_variant.txt"
if [ $? -ne 0 ]; then note "FAIL variant compile"; fail=1; else note "variant compile OK"; fi
"$ZNC_TMP" "$D/s19_verify.zag" -o "$BIN/s19_verify" 2>"$EV/evidence_compile_verify.txt"
if [ $? -ne 0 ]; then note "FAIL verifier compile"; fail=1; else note "verifier compile OK"; fi
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

# --- variant renders x3 (KB1 determinism) ---
t0=$(date +%s%N)
for i in 1 2 3; do
  "$BIN/s19_focus" "$EV/var$i.bmp" "$EV/var_trace$i.md" >"$EV/evidence_var_run$i.txt" 2>&1
  if [ $? -ne 0 ]; then note "FAIL variant run $i rc"; fail=1; fi
done
t1=$(date +%s%N)
var_ms=$(( (t1 - t0) / 1000000 / 3 ))
h1=$(sha256sum "$EV/var1.bmp" | cut -d' ' -f1)
h2=$(sha256sum "$EV/var2.bmp" | cut -d' ' -f1)
h3=$(sha256sum "$EV/var3.bmp" | cut -d' ' -f1)
if [ "$h1" = "$h2" ] && [ "$h2" = "$h3" ]; then
  note "KB1 determinism PASS ($h1)"
else
  note "FAIL KB1 rerun hashes differ"; fail=1
fi
echo "RUNNER: wall_ms baseline=$base_ms variant_avg=$var_ms" | tee "$EV/evidence_walltime.txt"

# --- KB6: dab budget exactly 208, asserted by the binary and traced ---
if grep -q "^D19 dabs: 208$" "$EV/var_trace1.md"; then
  note "KB6 dab budget PASS (208)"
else
  note "FAIL KB6 dab budget"; grep -h "D19 dabs" "$EV/var_trace1.md" || true; fail=1
fi
# cost ratio bar: variant <= 1.25x baseline wall time
if [ "$var_ms" -le $(( base_ms * 125 / 100 )) ]; then
  note "KB6 cost PASS (variant ${var_ms}ms vs baseline ${base_ms}ms)"
else
  note "FAIL KB6 cost"; fail=1
fi

# --- verifier kill bars KB2..KB5 ---
"$BIN/s19_verify" "$EV/base.bmp" "$EV/var1.bmp" >"$EV/evidence_verify.txt" 2>&1
vrc=$?
cat "$EV/evidence_verify.txt" | sed 's/^/RUNNER: verify: /'
if [ $vrc -ne 0 ]; then note "FAIL verifier bars (rc=$vrc)"; fail=1; else note "verifier bars PASS"; fi

if [ $fail -ne 0 ]; then note "OVERALL: FAIL"; exit 1; fi
note "OVERALL: harness checks complete (verdict decided by frozen bars, see VERDICT_C_D19.md)"
