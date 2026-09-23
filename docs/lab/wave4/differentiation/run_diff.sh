#!/bin/bash
# run_diff.sh — native trial runner for speaker differentiation.
# Prereg: PREREG.md (F1-F8). Compile, determinism (two runs, sha256),
# static checks (no-RNG grep; commit-region token exclusion), then verify
# every DIFF_CHECK line plus judgment/UNKNOWN output shape.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
BIN="$D/diff_trial_linux"
OUT1="$D/evidence_run1.txt"
OUT2="$D/evidence_run2.txt"
fail=0
note() { echo "RUNNER: $1"; }

# 0. mechanism source type-check
"$ZNC" check "$D/diff.zag" >/dev/null 2>&1
if [ $? -ne 0 ]; then note "FAIL diff.zag check"; fail=1; else note "diff.zag check OK"; fi

# 1. static: no randomness anywhere in system or harness (comments stripped)
if sed 's|//.*||' "$D/diff.zag" "$D/diff_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/diff.zag" "$D/diff_trial.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: commit region must not reference evidence masks or
# confirmation counters (the commit decision sees only active/eliminated)
REGION="$(sed -n '/COMMIT-REGION-BEGIN/,/COMMIT-REGION-END/p' "$D/diff.zag" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL commit region markers missing"; fail=1; fi
if echo "$REGION" | grep -qE 'must1|must0|pcons|pm1|pm0'; then
  note "FAIL commit region references masks/counters:"; echo "$REGION" | grep -nE 'must1|must0|pcons|pm1|pm0'; fail=1
else
  note "commit-region exclusion check OK (no mask/counter reference)"
fi

# 3. compile
"$ZNC" "$D/diff_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" 2>"$D/evidence_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile"; cat "$D/evidence_compile.txt"; exit 1; fi
note "compile OK"

# 4. determinism: two runs, byte-identical
"$BIN" > "$OUT1" 2>&1; e1=$?
"$BIN" > "$OUT2" 2>&1; e2=$?
s1=$(sha256sum "$OUT1" | cut -d' ' -f1); s2=$(sha256sum "$OUT2" | cut -d' ' -f1)
if [ "$s1" != "$s2" ]; then note "FAIL determinism: $s1 != $s2"; fail=1
else note "determinism OK (sha256 $s1)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 5. verify every DIFF_CHECK line
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^DIFF_CHECK,' "$OUT1")
note "checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

# 6. judgment shape: 3 judgments (E1, E5, E6), 6 refuted citations total,
#    3 explicit UNKNOWN outputs (E3, E4, E5b)
nj=$(grep -c '^DIFF_JUDGMENT_BEGIN' "$OUT1")
nr=$(grep -c '^DIFF_JUDGMENT_REFUTED' "$OUT1")
nu=$(grep -c '^DIFF_UNKNOWN,survivors=' "$OUT1")
note "judgments=$nj refuted_citations=$nr unknowns=$nu"
if [ "$nj" != "3" ] || [ "$nr" != "6" ] || [ "$nu" != "3" ]; then
  note "FAIL judgment/unknown shape (want 3/6/3)"; fail=1
fi
# every judgment must cite per-rival refutations with entry numbers
if grep '^DIFF_JUDGMENT_REFUTED' "$OUT1" | grep -vE 'by_entry=[1-9][0-9]*,obs_bit=[0-9]+,obs_val=[01]$' >/dev/null 2>&1; then
  note "FAIL malformed refutation citation"; fail=1
else
  note "refutation citation shape OK"
fi

# 7. DIFF_FAILURES must be 0
hf=$(grep '^DIFF_FAILURES,' "$OUT1" | cut -d, -f2)
if [ "$hf" != "0" ]; then note "FAIL DIFF_FAILURES=$hf"; fail=1; else note "DIFF_FAILURES=0"; fi

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
