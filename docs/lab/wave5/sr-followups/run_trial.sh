#!/bin/bash
# run_trial.sh — native trial runner for wave-5 sr-followups.
# Compile, determinism (two runs, sha256), static checks (no-RNG grep,
# sr_select-region signal-token ban on sr2.zag), then verify every
# SR_CHECK line.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
BIN="$D/sr2_trial_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness anywhere in system, world, or harness
# (comments stripped first so prose about the rule doesn't trip the check)
if sed 's|//.*||' "$D/sr2.zag" "$D/sr2_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/sr2.zag" "$D/sr2_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: sr_select region must not reference the scaffold signal
# (action selection is structurally independent of the signal; comments
# stripped so prose cannot pollute the token scan)
REGION="$(sed -n '/SELECT-REGION-BEGIN/,/SELECT-REGION-END/p' "$D/sr2.zag" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL select region markers missing"; fail=1; fi
if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'reward'; then
  note "FAIL select-region references the scaffold signal token"; fail=1
else
  note "select-region token check OK (no signal reference in action selection)"
fi

# 3. compile
"$ZNC" "$D/sr2_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile"; cat "$D/evidence_compile.txt"; exit 1; fi
note "compile OK"

# 4. determinism: two runs, byte-identical
"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 5. verify every SR_CHECK line
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^SR_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

# 6. SR_FAILURES must be 0
hf=$(grep '^SR_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL SR_FAILURES=$hf"; fail=1; else note "SR_FAILURES=0"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
