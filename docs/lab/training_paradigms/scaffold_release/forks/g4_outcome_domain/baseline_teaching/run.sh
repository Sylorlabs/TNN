#!/bin/bash
# run.sh — G4 baseline_teaching runner.
# static checks -> compile -> two runs (sha256 determinism) ->
# verify every D3_CHECK line -> require D3_FAILURES,0.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
SRC="d3base.zag"
SHARED="../shared/d3.zag"
BIN="$D/d3base_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

if sed 's|//.*||' "$SRC" "$SHARED" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep hit:"; sed 's|//.*||' "$SRC" "$SHARED" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

REGION="$(sed -n '/SELECT-REGION-BEGIN/,/SELECT-REGION-END/p' "$SHARED" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL select region markers missing"; fail=1; fi
if echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | grep -qx 'signal'; then
  note "FAIL select region references the scaffold signal"; fail=1
else
  note "select-region token check OK (no signal reference in action selection)"
fi

if sed 's|//.*||' "$SRC" "$SHARED" | grep -niEw 'reward|csum|ccnt|mean|accum' >/dev/null 2>&1; then
  note "FAIL accumulation token found:"; sed 's|//.*||' "$SRC" "$SHARED" | grep -niEw 'reward|csum|ccnt|mean|accum'; fail=1
else
  note "no-accumulation static check OK"
fi

"$ZNC" "$SRC" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
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
done < <(grep '^D3_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

hf=$(grep '^D3_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL D3_FAILURES=$hf"; fail=1; else note "D3_FAILURES=0"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
