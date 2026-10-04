#!/bin/bash
# run_trial.sh — native trial runner for RL-NECESSITY head-to-head.
# Compile, determinism (two runs, sha256), static checks (no-RNG grep,
# B-select-region signal ban, mean-token confinement to C's greedy region),
# then verify every TN_CHECK line.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
BIN="$D/tn_trial_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness anywhere in system, world, or harness
# (comments stripped first so prose about the rule doesn't trip the check)
if sed 's|//.*||' "$D/tn.zag" "$D/tn_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/tn.zag" "$D/tn_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: B's select region must not reference the scaffold signal
# (action selection is structurally independent of the signal; comments
# stripped so prose cannot pollute the token scan)
REGION="$(sed -n '/B-SELECT-REGION-BEGIN/,/B-SELECT-REGION-END/p' "$D/tn_trial.zag" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL B-select region markers missing"; fail=1; fi
if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'reward'; then
  note "FAIL B-select-region references the scaffold signal token"; fail=1
else
  note "B-select-region token check OK (no signal reference in action selection)"
fi

# 3. static: Arm B accumulates nothing — the RL-style value estimates
# (`csum`/`ccnt`) may appear only inside C's greedy region or Arm C's body.
# (The region is deleted from the raw file first: comment-stripping would
# erase the marker lines themselves.)
if ! grep -q 'C-GREEDY-REGION-BEGIN' "$D/tn_trial.zag"; then note "FAIL C-greedy region markers missing"; fail=1; fi
NOCREGION="$(sed '/C-GREEDY-REGION-BEGIN/,/C-GREEDY-REGION-END/d' "$D/tn_trial.zag")"
CODE="$(echo "$NOCREGION" | sed 's|//.*||'; sed 's|//.*||' "$D/tn.zag")"
if ! echo "$CODE" | grep -qw 'csum'; then note "FAIL C never accumulates (csum missing)"; fail=1; fi
OUTSIDE="$(echo "$CODE" | awk 'BEGIN{drop=0} /^fn arm_c\(\)/{drop=1} drop==0{print} drop==1 && /^\}/{drop=0}')"
if echo "$OUTSIDE" | grep -qw 'csum'; then
  note "FAIL csum accumulated outside C:"; echo "$OUTSIDE" | grep -n -w 'csum'; fail=1
else
  note "accumulation confinement OK (csum/ccnt only in C)"
fi
if echo "$OUTSIDE" | grep -qw 'ccnt'; then
  note "FAIL ccnt accumulated outside C:"; echo "$OUTSIDE" | grep -n -w 'ccnt'; fail=1
fi

# 4. compile
"$ZNC" "$D/tn_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
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
