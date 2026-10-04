#!/bin/bash
# run_graded.sh — native trial runner for differentiation-robustness.
# Prereg: PREREG.md (G1-G12, X1-X6, D1-D6, P1).
# Compile, determinism (two runs, sha256), static checks (no-RNG grep;
# GCOMMIT-region token exclusion), then verify every check line plus
# judgment/UNKNOWN output shape, plus the wave-4 comparative baseline.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
fail=0
note() { echo "RUNNER: $1"; }

# 0. mechanism/extractor sources type-check
for f in gdiff.zag extract.zag; do
  "$ZNC" check "$D/$f" >/dev/null 2>&1
  if [ $? -ne 0 ]; then note "FAIL check $f"; fail=1; else note "check $f OK"; fi
done

# 1. static: no randomness anywhere in system, extractor, or harness
if sed 's|//.*||' "$D/gdiff.zag" "$D/gdiff_trial.zag" "$D/extract.zag" "$D/pipe_trial.zag" "$D/w4baseline.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
  note "FAIL no-randomness grep found a hit:"
  sed 's|//.*||' "$D/gdiff.zag" "$D/gdiff_trial.zag" "$D/extract.zag" "$D/pipe_trial.zag" "$D/w4baseline.zag" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]'
  fail=1
else
  note "no-randomness static check OK"
fi

# 2. static: the graded commit region must not reference evidence masks
# (doubt IS visible to commit — by design, DESIGN_GRADED.md section 5)
REGION="$(sed -n '/GCOMMIT-REGION-BEGIN/,/GCOMMIT-REGION-END/p' "$D/gdiff.zag" | sed 's|//.*||')"
if [ -z "$REGION" ]; then note "FAIL commit region markers missing"; fail=1; fi
if echo "$REGION" | grep -qE 'must1|must0|pm1|pm0'; then
  note "FAIL commit region references masks:"
  echo "$REGION" | grep -nE 'must1|must0|pm1|pm0'
  fail=1
else
  note "commit-region exclusion check OK (no mask reference)"
fi

# 3. compile all three binaries
"$ZNC" "$D/gdiff_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/gdiff_trial_linux" 2>"$D/evidence_gdiff_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile gdiff_trial"; cat "$D/evidence_gdiff_compile.txt"; exit 1; fi
note "compile gdiff_trial OK"
"$ZNC" "$D/pipe_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/pipe_trial_linux" 2>"$D/evidence_pipe_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile pipe_trial"; cat "$D/evidence_pipe_compile.txt"; exit 1; fi
note "compile pipe_trial OK"
"$ZNC" "$D/w4baseline.zag" --no-zagd --no-analyze --no-foreground-cache -o "$D/w4baseline_linux" 2>"$D/evidence_w4baseline_compile.txt"
if [ $? -ne 0 ]; then note "FAIL compile w4baseline"; cat "$D/evidence_w4baseline_compile.txt"; exit 1; fi
note "compile w4baseline OK"

# 4. determinism: two runs each, byte-identical
for b in gdiff_trial pipe_trial w4baseline; do
  "$D/${b}_linux" > "$D/evidence_${b}_run1.txt" 2>&1; e1=$?
  "$D/${b}_linux" > "$D/evidence_${b}_run2.txt" 2>&1; e2=$?
  s1=$(sha256sum "$D/evidence_${b}_run1.txt" | cut -d' ' -f1)
  s2=$(sha256sum "$D/evidence_${b}_run2.txt" | cut -d' ' -f1)
  if [ "$s1" != "$s2" ]; then note "FAIL determinism $b: $s1 != $s2"; fail=1
  else note "determinism $b OK (sha256 $s1)"; fi
  if [ $e1 -ne 0 ] || [ $e2 -ne 0 ]; then note "FAIL nonzero exit $b ($e1,$e2)"; fail=1; fi
done

# 5. verify every GDIFF_CHECK / PIPE_CHECK line
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^GDIFF_CHECK,' "$D/evidence_gdiff_trial_run1.txt")
note "gdiff checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1
bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then echo "MISMATCH $name: $actual != $expected"; bad=$((bad+1)); fi
done < <(grep '^PIPE_CHECK,' "$D/evidence_pipe_trial_run1.txt")
note "pipe checks: $total total, $bad mismatched"
[ $bad -ne 0 ] && fail=1

# 6. judgment shape.
# gdiff: 2 judgments (G1, G5) with 9 doubt citations + 4 refuted citations;
#        10 explicit UNKNOWNs (G2,G3,G4,G6,G7,4x G8,G10).
nj=$(grep -c '^GDIFF_JUDGMENT_BEGIN' "$D/evidence_gdiff_trial_run1.txt")
nd=$(grep -c '^GDIFF_JUDGMENT_DOUBT' "$D/evidence_gdiff_trial_run1.txt")
nr=$(grep -c '^GDIFF_JUDGMENT_REFUTED' "$D/evidence_gdiff_trial_run1.txt")
nu=$(grep -c '^GDIFF_UNKNOWN,survivors=' "$D/evidence_gdiff_trial_run1.txt")
note "gdiff judgments=$nj doubt_citations=$nd refuted_citations=$nr unknowns=$nu"
if [ "$nj" != "2" ] || [ "$nd" != "9" ] || [ "$nr" != "4" ] || [ "$nu" != "10" ]; then
  note "FAIL gdiff judgment/unknown shape (want 2/9/4/10)"; fail=1
fi
# every doubt citation must carry entry/bit/rel/kind; every refuted
# citation must carry entry/doubt/kinds
if grep '^GDIFF_JUDGMENT_DOUBT' "$D/evidence_gdiff_trial_run1.txt" | grep -vE 'by_entry=[1-9][0-9]*,bit=[0-9]+,rel=[123],kind=[0-3]$' >/dev/null 2>&1; then
  note "FAIL malformed doubt citation"; fail=1
else
  note "doubt citation shape OK"
fi
if grep '^GDIFF_JUDGMENT_REFUTED' "$D/evidence_gdiff_trial_run1.txt" | grep -vE 'by_entry=[1-9][0-9]*,doubt=[4-9][0-9]*,kinds=[0-9]+$' >/dev/null 2>&1; then
  note "FAIL malformed refuted citation"; fail=1
else
  note "refuted citation shape OK"
fi
# pipe: 1 judgment (D4), 5 explicit UNKNOWNs (D1,D2,D3,D5,D6)
nj=$(grep -c '^GDIFF_JUDGMENT_BEGIN' "$D/evidence_pipe_trial_run1.txt")
nu=$(grep -c '^GDIFF_UNKNOWN,survivors=' "$D/evidence_pipe_trial_run1.txt")
note "pipe judgments=$nj unknowns=$nu"
if [ "$nj" != "1" ] || [ "$nu" != "5" ]; then
  note "FAIL pipe judgment/unknown shape (want 1/5)"; fail=1
fi

# 7. wave-4 comparative baseline: the poisoned sequence must commit CAROL
wb=$(grep '^W4BASELINE_COMMITTED,' "$D/evidence_w4baseline_run1.txt" | cut -d, -f2)
note "w4baseline committed=$wb (expect 3=CAROL)"
if [ "$wb" != "3" ]; then note "FAIL w4baseline did not commit CAROL"; fail=1; fi

# 8. failure counters must be 0
for t in gdiff_trial pipe_trial; do
  case $t in
    gdiff_trial) tag=GDIFF_FAILURES;;
    pipe_trial) tag=PIPE_FAILURES;;
  esac
  hf=$(grep "^${tag}," "$D/evidence_${t}_run1.txt" | cut -d, -f2)
  if [ "$hf" != "0" ]; then note "FAIL ${tag}=$hf"; fail=1; else note "${tag}=0"; fi
done

if [ $fail -eq 0 ]; then note "ALL RUNNER CHECKS PASS"; else note "RUNNER FAILURES PRESENT"; fi
exit $fail
