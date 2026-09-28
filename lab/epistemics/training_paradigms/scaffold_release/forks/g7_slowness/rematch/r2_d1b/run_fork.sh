#!/bin/bash
# run_fork.sh — G7 Q5 R2 runner (G1 pattern, written by the rematch crew).
# D1b early-evidence stream: A vs B vs FL2-honest vs FL2-lying in one binary.
# static checks (no-RNG grep; select/sim regions reference no `reward`
# token; no csum/ccnt) -> compile -> two runs sha256-identical ->
# every TN_CHECK actual==expected -> TN_FAILURES=0.
# Exits nonzero on any failure.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
SRC="${SRC:-d1b.zag}"
BIN="$D/r2_fork_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness anywhere (comments stripped)
if sed 's|//.*||' "$D/tn.zag" "$D/$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/tn.zag" "$D/$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: the select/simulation regions must not reference the scaffold
# signal token. Regions present: B-SELECT, FL2-SELECT, FL2-SIM.
if ! grep -q "B-SELECT-REGION-BEGIN" "$D/$SRC" || ! grep -q "FL2-SELECT-REGION-BEGIN" "$D/$SRC" || ! grep -q "FL2-SIM-REGION-BEGIN" "$D/$SRC"; then
  note "FAIL region markers missing"; fail=1
fi
for r in B-SELECT FL2-SELECT FL2-SIM; do
  REGION="$(sed -n "/$r-REGION-BEGIN/,/$r-REGION-END/p" "$D/$SRC" | sed 's|//.*||')"
  if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'reward'; then
    note "FAIL $r region references the scaffold signal token"; fail=1
  fi
done
[ $fail -eq 0 ] && note "region token checks OK (no signal reference in any select/simulation region)"

# 3. static: no accumulation of the scaffold signal anywhere
CODE="$(sed 's|//.*||' "$D/$SRC"; sed 's|//.*||' "$D/tn.zag")"
if echo "$CODE" | grep -qw 'csum'; then note "FAIL csum present:"; echo "$CODE" | grep -n -w 'csum'; fail=1; fi
if echo "$CODE" | grep -qw 'ccnt'; then note "FAIL ccnt present:"; echo "$CODE" | grep -n -w 'ccnt'; fail=1; fi
[ $fail -eq 0 ] && note "no-accumulation check OK (no csum/ccnt anywhere)"

# 4. compile
"$ZNC" "$D/$SRC" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile"; cat "$D/evidence_compile.txt"; exit 1; fi
note "compile OK"

# 5. determinism: two runs, byte-identical
"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 6. verify every TN_CHECK line (actual vs the binary's expected)
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
