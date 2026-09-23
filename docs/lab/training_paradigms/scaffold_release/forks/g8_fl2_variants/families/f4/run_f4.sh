#!/bin/bash
# run_f1.sh — G8 F4 (lie designs x zone-routing family + generated policies) runner.
# Compile, determinism (two runs, sha256), static checks (no-RNG grep,
# select/simulation regions reference no csig token, no-accumulation,
# no `reward` token), then verify every TN_CHECK line. Exits nonzero on failure.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
SRC="${SRC:-f4_route.zag}"
BIN="$D/f4_fork_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

if sed 's|//.*||' "$D/f4.zag" "$D/$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/f4.zag" "$D/$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

REGION="$(sed -n '/-REGION-BEGIN/,/-REGION-END/p' "$D/$SRC" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL region markers missing"; fail=1; fi
if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'csig'; then
  note "FAIL select/simulation region references the signal token"; fail=1
else
  note "region token check OK (no csig reference in select/simulation regions)"
fi

CODE="$(sed 's|//.*||' "$D/$SRC"; sed 's|//.*||' "$D/f4.zag")"
if echo "$CODE" | grep -qw 'csum'; then
  note "FAIL csum accumulation token present:"; echo "$CODE" | grep -n -w 'csum'; fail=1
else
  note "no-accumulation check OK (no csum/ccnt anywhere)"
fi
if echo "$CODE" | grep -qw 'ccnt'; then
  note "FAIL ccnt accumulation token present:"; echo "$CODE" | grep -n -w 'ccnt'; fail=1
fi
if echo "$CODE" | grep -qw 'reward'; then
  note "FAIL reward token present in learner sources:"; echo "$CODE" | grep -n -w 'reward'; fail=1
else
  note "no-reward-token check OK"
fi

"$ZNC" "$D/$SRC" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile"; cat "$D/evidence_compile.txt"; exit 1; fi
note "compile OK"

"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^TN_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

hf=$(grep '^TN_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL TN_FAILURES=$hf"; fail=1; else note "TN_FAILURES=0"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
