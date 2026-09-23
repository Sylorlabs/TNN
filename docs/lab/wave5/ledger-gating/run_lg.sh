#!/usr/bin/env bash
# run_lg.sh — native trial runner for ledger-gating (wave-5).
# Static checks (byte-identity of wave-3/4 sources, no-RNG grep,
# commit-region token allowlist), compile, determinism (two runs,
# byte-identical, sha256), then verify every LG_CHECK line and the
# LG_GATE disagreement log counts.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
BIN="$D/lg_trial_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
COMPILE_LOG="$D/evidence_compile.txt"
W3="$HOME/workspace/tnn-lab/wave3/hypothesis-state-substrate/hss.zag"
W4="$HOME/workspace/tnn-lab/wave4/integrity-ledger/il_core.zag"
fail=0
note() { echo "RUNNER: $1"; }

# 0. Byte-identity: the real substrate and checker, unmodified (F7).
if cmp -s "$D/il_core.zag" "$W4"; then note "il_core.zag byte-identical to wave-4"; else note "FAIL il_core.zag differs from wave-4"; fail=1; fi
if cmp -s "$D/hss.zag" "$W3"; then note "hss.zag byte-identical to wave-3"; else note "FAIL hss.zag differs from wave-3"; fail=1; fi

# 1. static: no randomness anywhere in the new gate or the harness (F6).
# (comments stripped first so prose about the rule doesn't trip the check)
if sed 's|//.*||' "$D/lg.zag" "$D/lg_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/lg.zag" "$D/lg_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK (lg.zag, lg_trial.zag)"
fi

# 2. static: commit-region token allowlist on the (copied) hss.zag —
# the commit rule the gate wraps must not see scores (wave-3 check, re-run).
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

# 2b. static: the gate itself must not take or touch confirmation
# counters — decisions stay logic-only. (lg_attempt_commit's parameter
# list is scanned; 'conf' must not appear.)
if grep -n 'conf' "$D/lg.zag" | grep -v '//' | grep -qv 'confirmation counters'; then
  note "FAIL gate references conf/counters:"; grep -n 'conf' "$D/lg.zag" | grep -v '//'; fail=1
else
  note "gate counter-independence check OK"
fi

# 3. compile
"$ZNC" "$D/lg_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" >"$COMPILE_LOG" 2>&1
if [ $? -ne 0 ]; then note "FAIL compile"; tail -30 "$COMPILE_LOG"; exit 1; fi
note "compile OK"

# 4. determinism: two runs, byte-identical (F5).
"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 5. verify every LG_CHECK line: actual must equal expected.
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^LG_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

# 6. LG_FAILURES must be 0.
hf=$(grep '^LG_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL LG_FAILURES=$hf"; fail=1; else note "LG_FAILURES=0"; fi

# 7. LG_GATE disagreement log: preregistered shape —
# 73 gate events total, exactly 8 blocked (7 cheat probes incl. B3's two
# sub-cases + the C2 stale probe); zero honest blocks.
ngate=$(grep -c '^LG_GATE,' "$OUT1")
nblocked=$(grep -c '^LG_GATE,[0-9]*,[0-9]*,1$' "$OUT1")
note "gate events: $ngate total, $nblocked blocked"
if [ "$ngate" != "73" ]; then note "FAIL expected 73 LG_GATE lines, got $ngate"; fail=1; fi
if [ "$nblocked" != "8" ]; then note "FAIL expected 8 blocked gates, got $nblocked"; fail=1; fi
# every blocked gate must name a real il_check violation verdict
badverdict=0
while IFS=, read -r tag ep verdict blocked; do
  if [ "$blocked" = "1" ]; then
    case "$verdict" in
      101|102|103|104|105|106) ;;
      *) echo "BAD BLOCK VERDICT ep=$ep verdict=$verdict"; badverdict=$((badverdict+1));;
    esac
  fi
done < <(grep '^LG_GATE,' "$OUT1")
[ $badverdict -ne 0 ] && fail=1
# honest legs (ep 0-49, 100-109) must have zero blocks
honestblocked=$(grep '^LG_GATE,' "$OUT1" | awk -F, '$2<50 || ($2>=100 && $2<110)' | grep -c ',1$' || true)
if [ "$honestblocked" != "0" ]; then note "FAIL $honestblocked honest gate(s) blocked"; fail=1
else note "honest legs: 0 blocks (false-block rate 0/60)"; fi

# 8. LG_RESULT must be PASS.
if ! grep -q '^LG_RESULT,PASS$' "$OUT1"; then note "FAIL LG_RESULT not PASS"; fail=1; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
