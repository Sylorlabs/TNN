#!/bin/bash
# run_fork.sh — native trial runner for G5 DIALOGUE forks.
# Static checks (no-RNG grep; F-SELECT/BASE-ACT region token bans;
# F-ELIM answer-key ban) -> compile -> two runs (sha256 determinism) ->
# verify every DZ_CHECK line -> require DZ_FAILURES,0.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
BIN="$D/dz_trial_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness anywhere in system, world, or harness
# (comments stripped first so prose about the rule doesn't trip the check)
if sed 's|//.*||' "$D/dz.zag" "$D/dz_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/dz.zag" "$D/dz_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: F-SELECT-REGION must reference neither the demonstration
# signal (`demo`) nor the answer key (`correct`); the scaffold informs
# (elimination) but never selects. Comments stripped.
for REGION_NAME in F-SELECT-REGION BASE-ACT-REGION; do
  REGION="$(sed -n "/${REGION_NAME}-BEGIN/,/${REGION_NAME}-END/p" "$D/dz_trial.zag" | sed 's|//.*||')"
  if [ -z "$REGION" ]; then note "FAIL $REGION_NAME markers missing"; fail=1; continue; fi
  if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'demo'; then
    note "FAIL $REGION_NAME references the demonstration token"; fail=1
  fi
  if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'correct'; then
    note "FAIL $REGION_NAME references the answer-key token"; fail=1
  fi
done
note "F-SELECT/BASE-ACT region token checks done"

# 3. static: F-ELIM-REGION may read the demonstration (contradiction
# evidence) but must not reference the answer key.
EREGION="$(sed -n '/F-ELIM-REGION-BEGIN/,/F-ELIM-REGION-END/p' "$D/dz_trial.zag" | sed 's|//.*||')"
if [ -z "$EREGION" ]; then note "FAIL F-ELIM-REGION markers missing"; fail=1; fi
if echo "$EREGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'correct'; then
  note "FAIL F-ELIM-REGION references the answer-key token"; fail=1
else
  note "F-ELIM-REGION token check OK (demo allowed, answer key banned)"
fi

# 4. compile
"$ZNC" "$D/dz_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile"; cat "$D/evidence_compile.txt"; exit 1; fi
note "compile OK"

# 5. determinism: two runs, byte-identical
"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 6. verify every DZ_CHECK line
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^DZ_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

# 7. DZ_FAILURES must be 0
hf=$(grep '^DZ_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL DZ_FAILURES=$hf"; fail=1; else note "DZ_FAILURES=0"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
