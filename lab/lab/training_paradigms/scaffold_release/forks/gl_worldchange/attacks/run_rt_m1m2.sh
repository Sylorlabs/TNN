#!/bin/bash
# run_rt_m1m2.sh — H4 crew 4 (red team) verification runner: M1/M2 attack drivers.
# Static checks (no-RNG), compile, two-run byte-identity, DIFFERENTIAL FIDELITY
# GATE (rt_m1/rt_m2 on frozen sids 0-5 byte-identical to the targets' committed
# m1_run1.txt / m2_run1.txt — the gate runs the targets' REAL m1_run/m2_run, so
# a mismatch voids the whole run), then attack evidence. Exits nonzero on any
# failure. Attack-sid results must not be read unless the gate passes.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
M1D="$D/../targets/m1"
M2D="$D/../targets/m2"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness in attack sources (comments stripped)
if sed 's|//.*||' "$D/rt_m1.zag" "$D/rt_m2.zag" "$D/rt_w4_streams.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/rt_m1.zag" "$D/rt_m2.zag" "$D/rt_w4_streams.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. compile both drivers (cwd must be attacks/: @import resolves relative to cwd)
cd "$D" || exit 1
"$ZNC" "$D/rt_m1.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/rt_m1_bin" 2>"$D/evidence_rt_m1_compile.txt"
if [ $? -ne 0 ]; then note "FAIL rt_m1 compile"; cat "$D/evidence_rt_m1_compile.txt"; exit 1; fi
note "rt_m1 compile OK"
"$ZNC" "$D/rt_m2.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/rt_m2_bin" 2>"$D/evidence_rt_m2_compile.txt"
if [ $? -ne 0 ]; then note "FAIL rt_m2 compile"; cat "$D/evidence_rt_m2_compile.txt"; exit 1; fi
note "rt_m2 compile OK"

# 3. determinism: two runs each, byte-identical
"$D/rt_m1_bin" > "$D/rt_m1_run1.txt" 2>&1; e1=$?
"$D/rt_m1_bin" > "$D/rt_m1_run2.txt" 2>&1; e2=$?
if ! cmp -s "$D/rt_m1_run1.txt" "$D/rt_m1_run2.txt"; then note "FAIL rt_m1 determinism"; fail=1
else note "rt_m1 determinism OK (byte-identical x2)"; fi
[ $e1 -ne 0 ] || [ $e2 -ne 0 ] && { note "FAIL rt_m1 nonzero exit ($e1,$e2)"; fail=1; }
"$D/rt_m2_bin" > "$D/rt_m2_run1.txt" 2>&1; e3=$?
"$D/rt_m2_bin" > "$D/rt_m2_run2.txt" 2>&1; e4=$?
if ! cmp -s "$D/rt_m2_run1.txt" "$D/rt_m2_run2.txt"; then note "FAIL rt_m2 determinism"; fail=1
else note "rt_m2 determinism OK (byte-identical x2)"; fi
[ $e3 -ne 0 ] || [ $e4 -ne 0 ] && { note "FAIL rt_m2 nonzero exit ($e3,$e4)"; fail=1; }

# 4. DIFFERENTIAL FIDELITY GATE: sids 0-5 WC lines byte-identical to committed evidence.
# (The driver's sids 0-5 go through the targets' REAL m1_run/m2_run.)
grep '^WC_' "$D/rt_m1_run1.txt" | grep -E '^WC_(AUDIT|HIST|HISTX|MEASURE),[0-5],' > "$D/.rt_m1_frozen.tmp"
grep '^WC_' "$M1D/m1_run1.txt" | grep -E '^WC_(AUDIT|HIST|HISTX|MEASURE),[0-5],' > "$D/.m1_frozen.tmp"
if ! cmp -s "$D/.rt_m1_frozen.tmp" "$D/.m1_frozen.tmp"; then
  note "FAIL M1 differential fidelity gate (sids 0-5 differ from committed m1_run1.txt)"
  diff "$D/.m1_frozen.tmp" "$D/.rt_m1_frozen.tmp" | head -10
  fail=1
else
  note "M1 differential fidelity gate PASS (sids 0-5 byte-identical to committed m1_run1.txt)"
fi
grep '^WC_' "$D/rt_m2_run1.txt" | grep -E '^WC_(AUDIT|HIST|HISTX|MEASURE),[0-5],' > "$D/.rt_m2_frozen.tmp"
grep '^WC_' "$M2D/m2_run1.txt" | grep -E '^WC_(AUDIT|HIST|HISTX|MEASURE),[0-5],' > "$D/.m2_frozen.tmp"
if ! cmp -s "$D/.rt_m2_frozen.tmp" "$D/.m2_frozen.tmp"; then
  note "FAIL M2 differential fidelity gate (sids 0-5 differ from committed m2_run1.txt)"
  diff "$D/.m2_frozen.tmp" "$D/.rt_m2_frozen.tmp" | head -10
  fail=1
else
  note "M2 differential fidelity gate PASS (sids 0-5 byte-identical to committed m2_run1.txt)"
fi
rm -f "$D/.rt_m1_frozen.tmp" "$D/.m1_frozen.tmp" "$D/.rt_m2_frozen.tmp" "$D/.m2_frozen.tmp"

# 5. attack evidence present: 18 attack sids x 19 measures + 4 q_asof probes each
for tgt in m1 m2; do
  for sid in 10 11 12 13 20 21 22 23 30 31 32 33 34 35 40 41 42 43; do
    c=$(grep -c "^WC_MEASURE,$sid," "$D/rt_${tgt}_run1.txt")
    [ "$c" != "19" ] && { note "FAIL $tgt sid $sid measures: $c != 19"; fail=1; }
    p=$(grep -c "^RT_PROBE,$sid,1," "$D/rt_${tgt}_run1.txt")
    [ "$p" != "4" ] && { note "FAIL $tgt sid $sid q_asof probes: $p != 4"; fail=1; }
  done
  f=$(grep -c "^RT_FORGE," "$D/rt_${tgt}_run1.txt")
  [ "$f" = "0" ] && { note "FAIL $tgt: no RT_FORGE lines"; fail=1; }
done
note "attack evidence present (18 sids x 19 measures + probes + forge, both targets)"

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
