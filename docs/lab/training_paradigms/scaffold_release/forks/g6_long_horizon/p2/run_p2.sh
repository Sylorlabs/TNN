#!/bin/bash
# run_p2.sh — G6/P2 runner: S5xR1 scaffold vs deliberate teaching, novel
# memory-agency triage, 100x. Compile, determinism (two runs, sha256),
# static checks (no-RNG grep, B-select-region signal ban, no-accumulation-
# token scan), then verify every TM_CHECK line.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
BIN="$D/p2_trial_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness anywhere in system, world, or harness
# (comments stripped first so prose about the rule doesn't trip the check)
if sed 's|//.*||' "$D/p2.zag" "$D/p2_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/p2.zag" "$D/p2_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: B's select region must not reference the scaffold signal
# (action selection is structurally independent of the signal; comments
# stripped so prose cannot pollute the token scan)
REGION="$(sed -n '/B-SELECT-REGION-BEGIN/,/B-SELECT-REGION-END/p' "$D/p2_trial.zag" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL B-select region markers missing"; fail=1; fi
if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'sig'; then
  note "FAIL B-select-region references the scaffold signal token"; fail=1
else
  note "B-select-region token check OK (no signal reference in action selection)"
fi

# 3. static: no accumulation anywhere — the signal is contradiction
# evidence only (csum/ccnt/mean/accum must not appear)
CODE="$(sed 's|//.*||' "$D/p2.zag"; sed 's|//.*||' "$D/p2_trial.zag")"
if echo "$CODE" | grep -nwE 'csum|ccnt|mean|accum' >/dev/null 2>&1; then
  note "FAIL accumulation token present:"; echo "$CODE" | grep -nwE 'csum|ccnt|mean|accum'; fail=1
else
  note "no-accumulation static check OK"
fi

# 4. compile
"$ZNC" "$D/p2_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile"; cat "$D/evidence_compile.txt"; exit 1; fi
note "compile OK"

# 5. determinism: two runs, byte-identical
"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 6. verify every TM_CHECK line
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^TM_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

# 7. TN_FAILURES must be 0
hf=$(grep '^TN_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL TN_FAILURES=$hf"; fail=1; else note "TN_FAILURES=0"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
