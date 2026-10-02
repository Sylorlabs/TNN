#!/bin/bash
# run_rt.sh — H4 crew 4 (red team) verification runner: attack streams + M0 driver.
# Static checks (no-RNG), compile, two-run byte-identity, differential fidelity
# gate (rt_m0 on frozen sids 0-5 byte-identical to committed m0_run1.txt),
# then attack evidence. Exits nonzero on any failure.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
M0D="$D/../targets/m0"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness in attack sources (comments stripped)
if sed 's|//.*||' "$D/rt_streams.zag" "$D/test_rt_streams.zag" "$D/rt_m0.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/rt_streams.zag" "$D/test_rt_streams.zag" "$D/rt_m0.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. compile attack stream self-test
"$ZNC" "$D/test_rt_streams.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/test_rt_streams_bin" 2>"$D/evidence_rt_streams_compile.txt"
if [ $? -ne 0 ]; then note "FAIL rt_streams compile"; cat "$D/evidence_rt_streams_compile.txt"; exit 1; fi
note "rt_streams compile OK"

# 3. stream determinism: two runs byte-identical; delegation check clean
"$D/test_rt_streams_bin" > "$D/rt_streams_run1.txt" 2>&1
"$D/test_rt_streams_bin" > "$D/rt_streams_run2.txt" 2>&1
if ! cmp -s "$D/rt_streams_run1.txt" "$D/rt_streams_run2.txt"; then note "FAIL rt_streams determinism"; fail=1
else note "rt_streams determinism OK (280 episodes x2 byte-identical)"; fi
n=$(grep -c '^RT_STREAM,' "$D/rt_streams_run1.txt")
[ "$n" != "280" ] && { note "FAIL rt stream episode count: $n != 280"; fail=1; }
[ "$(grep '^RT_DELEGATE_BAD,' "$D/rt_streams_run1.txt")" != "RT_DELEGATE_BAD,0" ] && { note "FAIL frozen delegation"; fail=1; } || note "frozen delegation OK (sids 0-5 identical)"

# 4. compile M0 attack driver
"$ZNC" "$D/rt_m0.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/rt_m0_bin" 2>"$D/evidence_rt_m0_compile.txt"
if [ $? -ne 0 ]; then note "FAIL rt_m0 compile"; cat "$D/evidence_rt_m0_compile.txt"; exit 1; fi
note "rt_m0 compile OK"

# 5. driver determinism: two runs byte-identical
"$D/rt_m0_bin" > "$D/rt_m0_run1.txt" 2>&1; e1=$?
"$D/rt_m0_bin" > "$D/rt_m0_run2.txt" 2>&1; e2=$?
if ! cmp -s "$D/rt_m0_run1.txt" "$D/rt_m0_run2.txt"; then note "FAIL rt_m0 determinism"; fail=1
else note "rt_m0 determinism OK (byte-identical x2)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 6. DIFFERENTIAL FIDELITY GATE: sids 0-5 WC lines byte-identical to committed m0_run1.txt
grep '^WC_' "$D/rt_m0_run1.txt" | grep -E '^WC_(AUDIT|MEASURE),[0-5],' > "$D/.rt_frozen.tmp"
grep '^WC_' "$M0D/m0_run1.txt" | grep -E '^WC_(AUDIT|MEASURE),[0-5],' > "$D/.m0_frozen.tmp"
if ! cmp -s "$D/.rt_frozen.tmp" "$D/.m0_frozen.tmp"; then
  note "FAIL differential fidelity gate (sids 0-5 differ from committed m0_run1.txt)"
  diff "$D/.m0_frozen.tmp" "$D/.rt_frozen.tmp" | head -10
  fail=1
else
  note "differential fidelity gate PASS (sids 0-5 byte-identical to committed m0_run1.txt)"
fi
rm -f "$D/.rt_frozen.tmp" "$D/.m0_frozen.tmp"

# 7. attack evidence present: 14 attack sids x 13 measures
for sid in 10 11 12 13 20 21 22 23 30 31 32 33 34 35; do
  c=$(grep -c "^WC_MEASURE,$sid," "$D/rt_m0_run1.txt")
  [ "$c" != "13" ] && { note "FAIL sid $sid measures: $c != 13"; fail=1; }
done
note "attack measures present (14 sids x 13)"

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
