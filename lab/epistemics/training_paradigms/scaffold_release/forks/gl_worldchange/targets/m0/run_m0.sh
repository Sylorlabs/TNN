#!/bin/bash
# run_m0.sh — H4 crew 1 verification runner: streams + M0 baseline.
# Static checks (no-RNG), compile, two-run byte-identity, KB-FID fidelity
# gate (canonical 269/271, TN_FAILURES=0, canonical section byte-identical
# to the committed canonical evidence), then curriculum evidence.
# Exits nonzero on any failure. Curriculum measurements are findings, not gates.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
CANON="$HOME/workspace/tnn-lab/training_paradigms/scaffold_release/gl_default"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness in streams or M0 sources (comments stripped)
if sed 's|//.*||' "$D/wc_streams.zag" "$D/test_streams.zag" "$D/gl_learner_m0.zag" "$D/gl_substrate.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D/wc_streams.zag" "$D/gl_learner_m0.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: canonical select/simulation regions still present and intact
for m in GL-SELECT-REGION-BEGIN GL-SELECT-REGION-END GL-SIM-REGION-BEGIN GL-SIM-REGION-END; do
  if ! grep -q "$m" "$D/gl_learner_m0.zag"; then note "FAIL region marker missing: $m"; fail=1; fi
done
note "region markers present"

# 3. compile streams test
"$ZNC" "$D/test_streams.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/test_streams_bin" 2>"$D/evidence_streams_compile.txt"
if [ $? -ne 0 ]; then note "FAIL streams compile"; cat "$D/evidence_streams_compile.txt"; exit 1; fi
note "streams compile OK"

# 4. streams determinism: two runs, byte-identical
"$D/test_streams_bin" > "$D/streams_run1.txt" 2>&1
"$D/test_streams_bin" > "$D/streams_run2.txt" 2>&1
if ! cmp -s "$D/streams_run1.txt" "$D/streams_run2.txt"; then note "FAIL streams determinism"; fail=1
else note "streams determinism OK (120 episodes x2 byte-identical)"; fi
n=$(grep -c '^WC_STREAM' "$D/streams_run1.txt")
[ "$n" != "120" ] && { note "FAIL stream episode count: $n != 120"; fail=1; }

# 5. compile M0
"$ZNC" "$D/gl_learner_m0.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/m0_bin" 2>"$D/evidence_m0_compile.txt"
if [ $? -ne 0 ]; then note "FAIL m0 compile"; cat "$D/evidence_m0_compile.txt"; exit 1; fi
note "m0 compile OK"

# 6. M0 determinism: two runs, byte-identical
"$D/m0_bin" > "$D/m0_run1.txt" 2>&1; e1=$?
"$D/m0_bin" > "$D/m0_run2.txt" 2>&1; e2=$?
if ! cmp -s "$D/m0_run1.txt" "$D/m0_run2.txt"; then note "FAIL m0 determinism"; fail=1
else note "m0 determinism OK (byte-identical x2)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 7. KB-FID fidelity gate
hf=$(grep '^TN_FAILURES,' "$D/m0_run1.txt" | cut -d, -f2)
[ "$hf" != "0" ] && { note "FAIL TN_FAILURES=$hf"; fail=1; } || note "TN_FAILURES=0"
h=$(grep '^TN_CHECK,glh_audit_total,' "$D/m0_run1.txt" | cut -d, -f3)
l=$(grep '^TN_CHECK,gll_audit_total,' "$D/m0_run1.txt" | cut -d, -f3)
[ "$h" != "269" ] && { note "FAIL honest total: $h != 269"; fail=1; } || note "honest audit total 269 OK"
[ "$l" != "271" ] && { note "FAIL lying total: $l != 271"; fail=1; } || note "lying audit total 271 OK"
[ "$(grep '^KB-FID,' "$D/m0_run1.txt")" != "KB-FID,PASS,269-271" ] && { note "FAIL KB-FID line"; fail=1; } || note "KB-FID PASS"
head -79 "$D/m0_run1.txt" > "$D/.canon_head.tmp"
if ! cmp -s "$D/.canon_head.tmp" "$CANON/evidence_run1.txt"; then note "FAIL canonical section differs from committed evidence"; fail=1
else note "canonical section byte-identical to committed evidence"; fi
rm -f "$D/.canon_head.tmp"

# 8. curriculum evidence present
for sid in 0 1 2 3 4 5; do
  c=$(grep -c "^WC_MEASURE,$sid," "$D/m0_run1.txt")
  [ "$c" != "13" ] && { note "FAIL sid $sid measures: $c != 13"; fail=1; }
done
note "curriculum measures present (6 streams x 13)"

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
