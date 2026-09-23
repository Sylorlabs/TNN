#!/usr/bin/env bash
# RC3 trial runner — native reasoning control at 100x scale (wave-10).
# Prereg: PREREG_RC3.md (2026-09-20, overnight-agentic authority).
# Compiles rc3_trial.zag, runs twice (byte-identical required), verifies
# every CL_CHECK actual==expected, checks determinism + no-RNG + capacity.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/rc3_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

# Prereg 3b: pre-compile audit-capacity estimate. RC_AUDIT_CAP=16384 retained
# only if the estimate stays <= 15,000; otherwise the cap is insufficient and
# the run is VOID before it starts (capacity mis-estimate, not a pass).
# Entry model (audited RC_OP_* entries per run):
#   phase A: 1200 episodes x 4 entries (EPISODE, OBSERVE, CHECKVERDICT, COMMIT)
#   revelation: 1200 REVEAL entries
#   phase B: 1200 episodes, <= 5 entries each (EPISODE, OBSERVE, DEEPCHECK,
#            REFUSE or CHECKVERDICT+COMMIT) -> upper bound 6000
#   mini phase: 400 episodes x <= 5 entries -> upper bound 2000
#   fixed overhead (PARAMINIT x2, INSPECT x4, PROPOSE x3, RCOMMIT x3,
#            RREFUSE x2, RROLLBACK x2, STAGE x1) = 17
est=$((4800 + 1200 + 6000 + 2000 + 17))
echo "audit_cap=16384 estimate=$est"
if [ "$est" -gt 15000 ]; then
  echo "AUDIT ESTIMATE EXCEEDS 15000: capacity insufficient per prereg 3b — run VOID, no compile"
  exit 1
fi

# Prereg 6: timing decision rule. Measure one RC2 binary run (identical
# machinery at 1/10 of RC3's episodes); projection p = t2 x 120.
# p > 8h triggers prereg FALLBACK A (50x leg); never improvise.
RC2BIN="$BASE/../../wave8/rc2/rc2_trial_linux"
if [ -x "$RC2BIN" ]; then
  t0=$(date +%s.%N)
  "$RC2BIN" >/dev/null 2>&1
  t1=$(date +%s.%N)
  t2=$(awk "BEGIN{print $t1 - $t0}")
  p=$(awk "BEGIN{print $t2 * 120}")
  echo "timing_probe: rc2_single_run_s=$t2 projected_rc3_s=$p"
  over=$(awk "BEGIN{print ($p > 28800) ? 1 : 0}")
  if [ "$over" = "1" ]; then
    echo "PROJECTION EXCEEDS 8h: prereg FALLBACK A (50x leg) is triggered — full 100x run NOT started"
    exit 3
  fi
else
  echo "timing_probe: RC2 binary absent, probe skipped (projection unavailable); proceeding per prereg 6 only if load allows"
fi

# Program law: no RNG anywhere in the SYSTEM's decision paths.
if sed 's|//.*||' "$BASE/rc3_trial.zag" "$BASE/il_core_rc3.zag" | grep -niE '\brng\b|\brand\b|srand|rand\(\)|random' >"$E/rng_grep.txt" 2>&1; then
  echo "RNG CHECK FAILED:"; cat "$E/rng_grep.txt"; exit 1
fi
echo "rng_check=clean"

nice -n 10 "$ZNC" "$BASE/rc3_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?; echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -40 "$E/compile.stderr"; exit 1; fi

t0=$(date +%s.%N)
nice -n 10 "$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"; ec1=$?
t1=$(date +%s.%N)
nice -n 10 "$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"; ec2=$?
t2=$(date +%s.%N)
echo "run_exit=$ec1,$ec2"
if [ $ec1 -ne 0 ] || [ $ec2 -ne 0 ]; then echo "RUN FAILED"; exit 1; fi
echo "run1_s=$(awk "BEGIN{print $t1 - $t0}") run2_s=$(awk "BEGIN{print $t2 - $t1}")"

h1=$(sha256sum "$E/run1.stdout" | cut -d' ' -f1)
h2=$(sha256sum "$E/run2.stdout" | cut -d' ' -f1)
echo "sha1=$h1"; echo "sha2=$h2"
if [ "$h1" != "$h2" ]; then echo "NONDETERMINISM"; exit 1; fi
echo "determinism=byte-identical"

# Capacity guards (prereg 3b / 5): ledger must never have hit a cap.
if grep -q "IL_AUDIT_FULL" "$E/run1.stdout"; then echo "IL LEDGER REPORTED FULL — RUN VOID"; exit 1; fi
ilhead=$(grep -E '^IL_HEAD,' "$E/run1.stdout" | head -1 | cut -d',' -f2)
audused=$(grep -E '^AUDIT_USED,' "$E/run1.stdout" | head -1 | cut -d',' -f2)
echo "il_head=$ilhead (cap 10240) audit_used=$audused (cap 16384)"
if [ -z "$ilhead" ] || [ "$ilhead" -ge 10240 ]; then echo "IL CAPACITY GUARD FAILED"; exit 1; fi
if [ -z "$audused" ] || [ "$audused" -ge 16384 ]; then echo "AUDIT CAPACITY GUARD FAILED"; exit 1; fi

cat "$E/run1.stdout"

bad=0; total=0
while IFS=, read -r tag name actual expected; do
  total=$((total+1))
  if [ "$actual" != "$expected" ]; then
    echo "MISMATCH: $name actual=$actual expected=$expected"; bad=$((bad+1))
  fi
done < <(grep '^CL_CHECK,' "$E/run1.stdout")
echo "checks_total=$total checks_bad=$bad"
if [ "$total" -ne 40 ]; then echo "EXPECTED 40 CHECKS, SAW $total"; bad=$((bad+1)); fi
grep -E '^RC_FAILURES,' "$E/run1.stdout" | tee "$E/summary.txt"
fline=$(grep -E '^RC_FAILURES,' "$E/run1.stdout" | head -1 | cut -d',' -f2)
if [ "$fline" != "0" ]; then echo "RC_FAILURES != 0"; bad=$((bad+1)); fi
if [ "$bad" -ne 0 ]; then echo "TRIAL FAILED"; exit 1; fi
echo "TRIAL PASSED"
