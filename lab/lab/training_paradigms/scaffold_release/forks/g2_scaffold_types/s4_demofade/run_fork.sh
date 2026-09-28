#!/bin/bash
# run_fork.sh — G2/S4 (demonstration-then-fade, no scalar signal).
# Compile, determinism (two runs, sha256), static checks (no-RNG grep,
# select-region scaffold-signal ban, fork-wide no-accumulation), then
# verify every TN_CHECK line -> require zero failures.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
SRC="$D/s4_trial.zag"
BIN="$D/s4_trial_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness anywhere in system, world, or harness
# (comments stripped first so prose about the rule doesn't trip the check)
if sed 's|//.*||' "$D/tn.zag" "$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/tn.zag" "$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: the select region must not reference the scaffold signal
# token (action selection is structurally independent of the signal;
# comments stripped so prose cannot pollute the token scan)
REGION="$(sed -n '/S4-SELECT-REGION-BEGIN/,/S4-SELECT-REGION-END/p' "$SRC" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL select region markers missing"; fail=1; fi
if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'demo'; then
  note "FAIL select-region references the demo token"; fail=1
else
  note "select-region token check OK (no demo-token reference in action selection)"
fi

# 3. static: nothing is accumulated anywhere in this fork — the scalar
# signal is contradiction evidence only (no greedy arm exists here)
CODE="$(sed 's|//.*||' "$D/tn.zag"; sed 's|//.*||' "$SRC")"
if echo "$CODE" | grep -qw 'csum'; then note "FAIL csum token present (accumulation)"; fail=1; fi
if echo "$CODE" | grep -qw 'ccnt'; then note "FAIL ccnt token present (accumulation)"; fail=1; fi
if echo "$CODE" | grep -ow 'mean' >/dev/null 2>&1; then note "FAIL mean token present (accumulation)"; fail=1; fi
if [ $fail -eq 0 ]; then note "no-accumulation static check OK"; fi

# 4. compile
"$ZNC" "$SRC" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile"; cat "$D/evidence_compile.txt"; exit 1; fi
note "compile OK"

# 5. determinism: two runs, byte-identical
"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 6. verify every TN_CHECK line
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^TN_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

# 7. TN_FAILURES must be 0
hf=$(grep '^TN_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL TN_FAILURES=$hf"; fail=1; else note "TN_FAILURES=0"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
