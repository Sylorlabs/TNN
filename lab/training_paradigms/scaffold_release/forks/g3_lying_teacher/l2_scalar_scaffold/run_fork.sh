#!/bin/bash
# run_fork.sh — G3/L2 runner: compile, determinism (two runs, sha256),
# static checks (no-RNG; B-select-region signal ban; no install path;
# scalar-reward present; no hint machinery), then verify every TN_CHECK.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
SRC="$D/l2_trial.zag"
BIN="$D/l2_trial_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness anywhere in system, world, or harness
if sed 's|//.*||' "$D/tn.zag" "$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/tn.zag" "$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: B's select region must not reference the scaffold signal
REGION="$(sed -n '/B-SELECT-REGION-BEGIN/,/B-SELECT-REGION-END/p' "$SRC" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL B-select region markers missing"; fail=1; fi
if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'reward'; then
  note "FAIL B-select-region references the scaffold signal token"; fail=1
else
  note "B-select-region token check OK"
fi

# 3. static: L2 is the SCALAR scaffold — the scalar reward must be present...
if ! grep -q 'tn_reward_contradiction' "$SRC"; then note "FAIL scalar reward missing"; fail=1
else note "scalar-reward present OK"; fi
# ...and there must be NO install-from-statement path (the lie cannot be installed).
# TN_OP_INSTALL/WITHHOLD may appear only inside tn_audit_count_op verification
# calls (which count zero installs in the ledger) — never in a tn_audit call
# that would ISSUE one.
ISSUERS="$(grep -n 'TN_OP_INSTALL' "$SRC" | grep -v 'tn_audit_count_op')"
if [ -n "$ISSUERS" ]; then note "FAIL install issued:"; echo "$ISSUERS"; fail=1
else note "no-install-path OK"; fi
ISSUERS2="$(grep -n 'TN_OP_WITHHOLD' "$SRC" | grep -v 'tn_audit_count_op')"
if [ -n "$ISSUERS2" ]; then note "FAIL withhold issued:"; echo "$ISSUERS2"; fail=1
else note "no-withhold-path OK"; fi
# ...and no hint machinery (that's L3's fork)
if grep -q 'tn_l3_hint' "$SRC"; then note "FAIL hint machinery in L2"; fail=1
else note "no-hint-machinery OK"; fi

# 4. static: PYTHON SWEEP — the decision path is Zag compiled by znc plus this
# bash runner; assert no python interpreter is ever invoked in it.
if sed -e 's|//.*||' -e 's|#.*||' "$D"/*.zag "$D"/*.sh | grep -E 'python3|/usr/bin/python|/usr/local/bin/python' >/dev/null 2>&1; then
  note "FAIL python interpreter referenced in decision path"; fail=1
else
  note "python-sweep OK (no Python in decision path)"
fi

# 5. compile (cwd = fork dir: @import resolves relative to cwd)
cd "$D"
"$ZNC" "$SRC" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile"; cat "$D/evidence_compile.txt"; exit 1; fi
note "compile OK"

# 6. determinism: two runs, byte-identical
"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 7. verify every TN_CHECK line
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^TN_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

# 8. TN_FAILURES must be 0
hf=$(grep '^TN_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL TN_FAILURES=$hf"; fail=1; else note "TN_FAILURES=0"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
