#!/bin/bash
# run_m1.sh — H4 crew 2 verification runner: M1 (SUPERSEDE primitive).
# Static checks (no-RNG), compile from vendored sources only, two-run
# byte-identity, KB-FID fidelity gate (canonical 269/271, TN_FAILURES=0,
# canonical section byte-identical to the committed canonical evidence),
# then curriculum evidence. Exits nonzero on any failure. Curriculum
# measurements are findings, not gates.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
CANON="$HOME/workspace/tnn-lab/training_paradigms/scaffold_release/gl_default"
fail=0
note() { echo "RUNNER: $1"; }

# 1. static: no randomness in any source (comments stripped)
if sed 's|//.*||' "$D/wc_streams.zag" "$D/wc_mech.zag" "$D/m1_harness.zag" "$D/gl_learner_m1.zag" "$D/gl_substrate_m1.zag" "$D/transfer_probe.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"; sed 's|//.*||' "$D"/*.zag | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'; fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: all @import targets are vendored in this directory
missing=0
for f in gl_learner_m1.zag transfer_probe.zag; do
  while read -r imp; do
    [ -f "$D/$imp" ] || { note "FAIL import not vendored: $f -> $imp"; missing=1; }
  done < <(grep -o '@import("[^"]*")' "$D/$f" | sed 's/@import("//;s/")//')
done
[ "$missing" -eq 0 ] && note "all imports vendored OK" || fail=1

# 3. compile M1 learner
"$ZNC" "$D/gl_learner_m1.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/m1_bin" 2>"$D/evidence_m1_compile.txt"
if [ $? -ne 0 ]; then note "FAIL m1 compile"; cat "$D/evidence_m1_compile.txt"; exit 1; fi
note "m1 compile OK"

# 4. M1 determinism: two runs, byte-identical
"$D/m1_bin" > "$D/m1_run1.txt" 2>&1; e1=$?
"$D/m1_bin" > "$D/m1_run2.txt" 2>&1; e2=$?
if ! cmp -s "$D/m1_run1.txt" "$D/m1_run2.txt"; then note "FAIL m1 determinism"; fail=1
else note "m1 determinism OK (byte-identical x2)"; fi
if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit ($e1,$e2)"; fail=1; fi

# 5. KB-FID fidelity gate
hf=$(grep '^TN_FAILURES,' "$D/m1_run1.txt" | cut -d, -f2)
[ "$hf" != "0" ] && { note "FAIL TN_FAILURES=$hf"; fail=1; } || note "TN_FAILURES=0"
h=$(grep '^TN_CHECK,glh_audit_total,' "$D/m1_run1.txt" | cut -d, -f3)
l=$(grep '^TN_CHECK,gll_audit_total,' "$D/m1_run1.txt" | cut -d, -f3)
[ "$h" != "269" ] && { note "FAIL honest total: $h != 269"; fail=1; } || note "honest audit total 269 OK"
[ "$l" != "271" ] && { note "FAIL lying total: $l != 271"; fail=1; } || note "lying audit total 271 OK"
[ "$(grep '^KB-FID,' "$D/m1_run1.txt")" != "KB-FID,PASS,269-271" ] && { note "FAIL KB-FID line"; fail=1; } || note "KB-FID PASS"
head -79 "$D/m1_run1.txt" > "$D/.canon_head.tmp"
if ! cmp -s "$D/.canon_head.tmp" "$CANON/evidence_run1.txt"; then note "FAIL canonical section differs from committed evidence"; fail=1
else note "canonical section byte-identical to committed evidence"; fi
rm -f "$D/.canon_head.tmp"

# 6. curriculum evidence present (6 streams x 19 measures)
for sid in 0 1 2 3 4 5; do
  c=$(grep -c "^WC_MEASURE,$sid," "$D/m1_run1.txt")
  [ "$c" != "19" ] && { note "FAIL sid $sid measures: $c != 19"; fail=1; }
done
note "curriculum measures present (6 streams x 19)"

# 7. transfer probe: compile, two runs byte-identical, cross-checks pass
"$ZNC" "$D/transfer_probe.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/transfer_bin" 2>"$D/evidence_transfer_compile.txt"
if [ $? -ne 0 ]; then note "FAIL transfer compile"; cat "$D/evidence_transfer_compile.txt"; exit 1; fi
"$D/transfer_bin" > "$D/transfer_run1.txt" 2>&1; t1=$?
"$D/transfer_bin" > "$D/transfer_run2.txt" 2>&1; t2=$?
if ! cmp -s "$D/transfer_run1.txt" "$D/transfer_run2.txt"; then note "FAIL transfer determinism"; fail=1
else note "transfer determinism OK (byte-identical x2)"; fi
if [ $t1 -ne 0 ] || [ $t2 -ne 0 ]; then note "FAIL transfer nonzero exit ($t1,$t2)"; fail=1; fi
[ "$(grep '^TRANSFER_XCHECK,' "$D/transfer_run1.txt" | tail -1)" != "TRANSFER_XCHECK,PASS" ] && { note "FAIL transfer cross-checks"; fail=1; } || note "transfer cross-checks PASS"

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
