#!/bin/bash
# run_gl.sh — canonical guided-learning (gl) default runner.
# Adapted from the G7 free-lunch FL2 run_fork.sh. Compile, determinism
# (two runs, sha256), static checks (no-RNG grep, select/simulation
# regions reference no accumulated-signal token, no-accumulation), then
# verify every TN_CHECK line and the headline audit totals (269/271).
# Exits nonzero on any failure.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
SRC="${SRC:-gl_learner.zag}"
BIN="$D/gl_default_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness anywhere in substrate, world, or harness
# (comments stripped first so prose about the rule doesn't trip the check)
if sed 's|//.*||' "$D/gl_substrate.zag" "$D/$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/gl_substrate.zag" "$D/$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: the GL select/simulation regions must not reference the
# accumulated-signal token (action selection is structurally independent
# of the contradiction signal)
REGION="$(sed -n '/-REGION-BEGIN/,/-REGION-END/p' "$D/$SRC" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL region markers missing"; fail=1; fi
if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'reward'; then
  note "FAIL select/simulation region references the scaffold signal token"; fail=1
else
  note "region token check OK (no signal reference in select/simulation regions)"
fi

# 3. static: no accumulation of the contradiction signal anywhere
# (csum/ccnt must be absent from the whole module, comments stripped)
CODE="$(sed 's|//.*||' "$D/$SRC"; sed 's|//.*||' "$D/gl_substrate.zag")"
if echo "$CODE" | grep -qw 'csum'; then
  note "FAIL csum accumulation token present:"; echo "$CODE" | grep -n -w 'csum'; fail=1
else
  note "no-accumulation check OK (no csum/ccnt anywhere)"
fi
if echo "$CODE" | grep -qw 'ccnt'; then
  note "FAIL ccnt accumulation token present:"; echo "$CODE" | grep -n -w 'ccnt'; fail=1
fi

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

# 8. headline audit totals: honest 269, lying 271
h=$(grep '^TN_CHECK,glh_audit_total,' "$OUT1" | cut -d, -f3)
l=$(grep '^TN_CHECK,gll_audit_total,' "$OUT1" | cut -d, -f3)
if [ "$h" != "269" ]; then note "FAIL honest total: $h != 269"; fail=1; else note "honest audit total 269 OK"; fi
if [ "$l" != "271" ]; then note "FAIL lying total: $l != 271"; fail=1; else note "lying audit total 271 OK"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
