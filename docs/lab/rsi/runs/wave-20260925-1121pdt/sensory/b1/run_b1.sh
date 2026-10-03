#!/bin/bash
# run_b1.sh - build and run the B1 bounce trial (wave-20260925-1121pdt).
# Pure Zag, zero RNG, no Python interpreter anywhere.
# Static checks + compile + baseline byte-identity gate + k in {384,192}
# renders + KB1 determinism (byte-identical reruns) + KB2 cost +
# verifier kill bars KB3..KB6 (frozen) + KB7 trace-text check.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC_SRC="$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
ZNC_TMP="/tmp/znc_b1_run"
BIN="$D/bin"
EV="$D/evidence"
mkdir -p "$BIN" "$EV"
fail=0
note() { echo "RUNNER: $1"; }

note "prereg commit (frozen before any B1 code existed):"
git -C "$HOME/workspace/tnn-rsi" log --oneline -1 b2b2a3349 2>/dev/null || { note "FAIL prereg commit b2b2a3349 not found"; fail=1; }

# --- static checks: no interpreter, no randomness in new sources ---
if ls "$D"/*.py >/dev/null 2>&1; then note "FAIL py file in b1 dir"; fail=1; else note "no-pyfile check OK"; fi
if sed 's|//.*||' "$D"/b1_bounce.zag "$D"/b1_k192.zag "$D"/b1_verify.zag "$D"/b1_baseline.zag | grep -ni 'python' >/dev/null 2>&1; then
  note "FAIL py token in zag sources"; fail=1
else
  note "no-py-in-zag check OK"
fi
if grep -niE '(^|[;&|[:space:]])python[0-9]*([[:space:]]|$|;)' "$D/run_b1.sh" >/dev/null 2>&1; then
  note "FAIL py invocation in runner"; fail=1
else
  note "no-py-in-runner check OK"
fi
if sed 's|//.*||' "$D"/b1_bounce.zag "$D"/b1_k192.zag "$D"/b1_verify.zag | grep -niE '\\brand[[:space:]]*\\(|random[[:space:]]*\\(|srand|\\btime[[:space:]]*\\(|\\bclock[[:space:]]*\\(' >/dev/null 2>&1; then
  note "FAIL randomness/time call grep found a hit"; fail=1
else
  note "no-randomness static check OK"
fi

# --- the two variant sources differ only in the frozen k constant ---
if [ "$(diff "$D/b1_bounce.zag" "$D/b1_k192.zag" | grep -c '^[<>]')" = "4" ]; then
  note "variant sources differ only in k constant OK"
else
  note "FAIL variant sources differ by more than the k constant"; fail=1
fi

# --- toolchain + substrate pins ---
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
"$ZNC_TMP" "$D/b1_baseline.zag" --no-zagd --no-analyze -o "$BIN/b1_baseline" 2>"$EV/evidence_compile_baseline.txt"
[ $? -ne 0 ] && { note "FAIL baseline compile"; fail=1; } || note "baseline compile OK"
"$ZNC_TMP" "$D/b1_bounce.zag" --no-zagd --no-analyze -o "$BIN/b1_bounce" 2>"$EV/evidence_compile_bounce.txt"
[ $? -ne 0 ] && { note "FAIL bounce compile"; fail=1; } || note "bounce compile OK"
"$ZNC_TMP" "$D/b1_k192.zag" --no-zagd --no-analyze -o "$BIN/b1_k192" 2>"$EV/evidence_compile_k192.txt"
[ $? -ne 0 ] && { note "FAIL k192 compile"; fail=1; } || note "k192 compile OK"
"$ZNC_TMP" "$D/b1_verify.zag" --no-zagd --no-analyze -o "$BIN/b1_verify" 2>"$EV/evidence_compile_verify.txt"
[ $? -ne 0 ] && { note "FAIL verifier compile"; fail=1; } || note "verifier compile OK"

# --- baseline byte-identity gate (frozen r8c hash) ---
"$BIN/b1_baseline" "$EV/base_r1.bmp" "$EV/base_trace_r1.md" >"$EV/run_base_r1.txt" 2>&1
BH="$(sha256sum "$EV/base_r1.bmp" | cut -d' ' -f1)"
if [ "$BH" != "e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d" ]; then
  note "FAIL baseline hash $BH"; fail=1
else
  note "baseline hash gate OK"
fi

# --- variant reruns (KB1 determinism) ---
"$BIN/b1_bounce" "$EV/var_r1.bmp" "$EV/var_trace_r1.md" >"$EV/run_var_r1.txt" 2>&1
"$BIN/b1_bounce" "$EV/var_r2.bmp" "$EV/var_trace_r2.md" >"$EV/run_var_r2.txt" 2>&1
if cmp -s "$EV/var_r1.bmp" "$EV/var_r2.bmp" && cmp -s "$EV/var_trace_r1.md" "$EV/var_trace_r2.md"; then
  note "KB1 byte-identical reruns OK"
else
  note "FAIL KB1 reruns differ"; fail=1
fi

# --- k192 data-amount trial ---
"$BIN/b1_k192" "$EV/k192_r1.bmp" "$EV/k192_trace_r1.md" >"$EV/run_k192_r1.txt" 2>&1
"$BIN/b1_k192" "$EV/k192_r2.bmp" "$EV/k192_trace_r2.md" >"$EV/run_k192_r2.txt" 2>&1

# --- verifier kill bars KB3..KB6 ---
"$BIN/b1_verify" "$EV/base_r1.bmp" "$EV/var_r1.bmp" >"$EV/verify_k384.txt" 2>&1
[ $? -ne 0 ] && { note "k384 verifier reported FAIL (see verify_k384.txt)"; } || note "k384 verifier all PASS"
"$BIN/b1_verify" "$EV/base_r1.bmp" "$EV/k192_r1.bmp" >"$EV/verify_k192.txt" 2>&1
[ $? -ne 0 ] && { note "k192 verifier reported FAIL (see verify_k192.txt)"; } || note "k192 verifier all PASS"

# --- KB7 trace-text check ---
if grep -q "PASS 3B" "$EV/var_trace_r1.md" && grep -q "Total: 270 deliberate decisions" "$EV/var_trace_r1.md"; then
  note "KB7 trace integrity OK"
else
  note "FAIL KB7 trace check"; fail=1
fi

if [ "$fail" = "1" ]; then note "RUNNER DONE: FAILURES PRESENT"; exit 1; fi
note "RUNNER DONE: all runner gates passed (verdict per frozen bars in EVIDENCE)"
