#!/bin/bash
# run_trial.sh — native trial runner for hypothesis-state-substrate.
# Compile, determinism (two runs, sha256), static checks (no-RNG grep,
# commit-region token allowlist), then verify every HSS_CHECK line.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
BIN="$D/hss_trial_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 0. v1 source type-check (analysis evidence: the surveyed source is sound)
"$ZNC" check "$D/r34_hypothesis_state_v1.zag" >/dev/null 2>&1
if [ $? -ne 0 ]; then note "FAIL v1 check"; fail=1; else note "v1 check OK"; fi

# 1. static: no randomness anywhere in system, world, or harness
# (comments stripped first so prose about the rule doesn't trip the check)
if sed 's|//.*||' "$D/hss.zag" "$D/trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/hss.zag" "$D/trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: commit region token allowlist (commit must not see scores)
# comments stripped; the region's prose must not pollute the token scan
REGION="$(sed -n '/COMMIT-REGION-BEGIN/,/COMMIT-REGION-END/p' "$D/hss.zag" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL commit region markers missing"; fail=1; fi
ALLOW="fn hss_commit active capacity committed step abuf acount i32 n s r r2 r3 i \
  HSS_OK HSS_BAD HSS_OP_COMMIT HSS_OP_HOLD HSS_OP_UNCOMMIT hss_audit null \
  as if len let return u8 while"
BADTOK=""
for tok in $(echo "$REGION" | grep -oE '[A-Za-z_][A-Za-z0-9_]*' | sort -u); do
  ok=0
  for a in $ALLOW; do [ "$tok" = "$a" ] && ok=1 && break; done
  if [ $ok -eq 0 ]; then BADTOK="$BADTOK $tok"; fi
done
if [ -n "$BADTOK" ]; then note "FAIL commit-region foreign tokens:$BADTOK"; fail=1
else note "commit-region token check OK (no conf/claims/score reference)"; fi

# 3. compile
"$ZNC" "$D/trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile"; cat "$D/evidence_compile.txt"; exit 1; fi
note "compile OK"

# 4. determinism: two runs, byte-identical
"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 5. verify every HSS_CHECK line
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^HSS_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

# 6. HSS_FAILURES must be 0
hf=$(grep '^HSS_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL HSS_FAILURES=$hf"; fail=1; else note "HSS_FAILURES=0"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
