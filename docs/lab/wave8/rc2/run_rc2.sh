#!/usr/bin/env bash
# RC2 trial runner — native reasoning control at 10x scale (wave-8).
# Ported from wave7/reasoning-control/trial/run_rc.sh.
# Compiles rc2_trial.zag, runs twice (byte-identical required), verifies
# every CL_CHECK actual==expected, checks determinism + no-RNG.
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
BIN="$BASE/rc2_trial_linux"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"

# Prereg 3b: pre-compile audit-capacity estimate. RC_AUDIT_CAP=2048 retained
# only if the estimate stays <= 1,800; otherwise bump to 4096 (capacity only).
# Entry model (audited RC_OP_* entries per run):
#   phase A: 120 episodes x 4 entries (EPISODE, OBSERVE, CHECKVERDICT, COMMIT)
#   revelation: 120 REVEAL entries
#   phase B: 120 episodes, <= 5 entries each (EPISODE, OBSERVE, DEEPCHECK,
#            REFUSE or CHECKVERDICT+COMMIT) -> upper bound 600
#   mini phase: 40 episodes x <= 5 entries -> upper bound 200
#   fixed overhead (PARAMINIT x2, INSPECT x3, PROPOSE x3, RCOMMIT x2,
#            RREFUSE x2, RROLLBACK x2, STAGE x1) = 15
est=$((480 + 120 + 600 + 200 + 15))
echo "audit_cap=2048 estimate=$est"
if [ "$est" -gt 1800 ]; then
  echo "AUDIT ESTIMATE EXCEEDS 1800: bump RC_AUDIT_CAP to 4096 per prereg 3b (capacity only, no bar changes)"
  exit 1
fi

# Program law: no RNG anywhere in the SYSTEM's decision paths.
if sed 's|//.*||' "$BASE/rc2_trial.zag" "$BASE/il_core_rc2.zag" | grep -niE '\brng\b|\brand\b|srand|rand\(\)|random' >"$E/rng_grep.txt" 2>&1; then
  echo "RNG CHECK FAILED:"; cat "$E/rng_grep.txt"; exit 1
fi
echo "rng_check=clean"

"$ZNC" "$BASE/rc2_trial.zag" --no-zagd --no-analyze --no-foreground-cache -o "$BIN" \
  >"$E/compile.stdout" 2>"$E/compile.stderr"
ec=$?; echo "compile_exit=$ec"
if [ $ec -ne 0 ]; then echo "COMPILE FAILED"; tail -40 "$E/compile.stderr"; exit 1; fi

"$BIN" >"$E/run1.stdout" 2>"$E/run1.stderr"; ec1=$?
"$BIN" >"$E/run2.stdout" 2>"$E/run2.stderr"; ec2=$?
echo "run_exit=$ec1,$ec2"
if [ $ec1 -ne 0 ] || [ $ec2 -ne 0 ]; then echo "RUN FAILED"; exit 1; fi

h1=$(sha256sum "$E/run1.stdout" | cut -d' ' -f1)
h2=$(sha256sum "$E/run2.stdout" | cut -d' ' -f1)
echo "sha1=$h1"; echo "sha2=$h2"
if [ "$h1" != "$h2" ]; then echo "NONDETERMINISM"; exit 1; fi
echo "determinism=byte-identical"

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
