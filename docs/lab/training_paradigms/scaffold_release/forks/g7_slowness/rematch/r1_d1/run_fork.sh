#!/bin/bash
# run_fork.sh — G7 Q5 R1 rematch runner (G1 pattern, written by the rematch crew).
# Rebuilds the free-lunch crew's committed FL2 sources byte-identical, then:
# static checks (no-RNG grep, FL2 select/sim regions reference no signal
# token, no-accumulation) -> compile -> two runs sha256-identical ->
# verify every TN_CHECK line actual==expected -> TN_FAILURES=0.
# Exits nonzero on any failure.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
SRC="${SRC:-fl2.zag}"
BIN="$D/r1_fork_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 0. byte-identity of the rebuilt sources vs the committed FL2 fork sources
FL2SRC="$HOME/workspace/tnn-lab/training_paradigms/scaffold_release/forks/g7_slowness/freelunch/fl2_provisional_revoke"
cmp -s "$FL2SRC/fl2.zag" "$D/fl2.zag" || { note "FAIL fl2.zag not byte-identical vs committed FL2"; fail=1; }
cmp -s "$FL2SRC/tn.zag" "$D/tn.zag" || { note "FAIL tn.zag not byte-identical vs committed FL2"; fail=1; }
[ $fail -eq 0 ] && note "byte-identity vs committed FL2 sources OK"

# 1. static: no randomness anywhere in substrate, world, or harness
# (comments stripped first so prose about the rule doesn't trip the check)
if sed 's|//.*||' "$D/tn.zag" "$D/$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/tn.zag" "$D/$SRC" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: the FL2 select/simulation regions must not reference the
# scaffold signal token (action selection is structurally independent of
# the contradiction signal)
REGION="$(sed -n '/-REGION-BEGIN/,/-REGION-END/p' "$D/$SRC" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL region markers missing"; fail=1; fi
if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'reward'; then
  note "FAIL select/simulation region references the scaffold signal token"; fail=1
else
  note "region token check OK (no signal reference in select/simulation regions)"
fi

# 3. static: no accumulation of the scaffold signal anywhere
# (csum/ccnt must be absent from the whole fork source and the substrate
# copy, comments stripped)
CODE="$(sed 's|//.*||' "$D/$SRC"; sed 's|//.*||' "$D/tn.zag")"
if echo "$CODE" | grep -qw 'csum'; then
  note "FAIL csum accumulation token present in fork:"; echo "$CODE" | grep -n -w 'csum'; fail=1
else
  note "no-accumulation check OK (no csum/ccnt anywhere)"
fi
if echo "$CODE" | grep -qw 'ccnt'; then
  note "FAIL ccnt accumulation token present in fork:"; echo "$CODE" | grep -n -w 'ccnt'; fail=1
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
