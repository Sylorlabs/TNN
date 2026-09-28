#!/usr/bin/env bash
# Wave-5 phase-transitions-remaining trial runner.
# Compiles trial01 / trial23 / trial34 natively, runs each twice,
# checks determinism (byte-identical), verifies every CL_CHECK line
# (actual==expected) and every PT*_STAT line against prereg hand-computed
# expectations.
# Usage: ./run_trials.sh [ZNC]
set -u
BASE="$(cd "$(dirname "$0")" && pwd)"
ZNC="${1:-${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}}"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
mkdir -p "$E"
overall_bad=0

run_one() {
  local name="$1" src="$2" stat_tag="$3" fail_tag="$4"
  local bin="$BASE/${name}_linux"
  echo "=== $name ==="
  # Program law: no RNG anywhere in the SYSTEM's decision paths.
  if sed 's|//.*||' "$src" | grep -niE '\brng\b|\brand\b|srand|rand\(\)|random' >"$E/${name}_rng_grep.txt" 2>&1; then
    echo "RNG CHECK FAILED in $src:"; cat "$E/${name}_rng_grep.txt"; overall_bad=1; return
  fi
  echo "rng_check=clean ($name)"
  "$ZNC" "$src" --no-zagd --no-analyze --no-foreground-cache -o "$bin" \
    >"$E/${name}_compile.stdout" 2>"$E/${name}_compile.stderr"
  ec=$?
  echo "compile_exit=$ec ($name)"
  if [ $ec -ne 0 ]; then echo "COMPILE FAILED ($name)"; tail -30 "$E/${name}_compile.stderr"; overall_bad=1; return; fi
  "$bin" >"$E/${name}_run1.stdout" 2>"$E/${name}_run1.stderr"; ec1=$?
  "$bin" >"$E/${name}_run2.stdout" 2>"$E/${name}_run2.stderr"; ec2=$?
  echo "run1_exit=$ec1 run2_exit=$ec2 ($name)"
  if [ $ec1 -ne 0 ]; then echo "RUN FAILED ($name)"; overall_bad=1; fi
  if ! cmp -s "$E/${name}_run1.stdout" "$E/${name}_run2.stdout"; then
    echo "DETERMINISM FAILED ($name)"; overall_bad=1; return
  fi
  echo "determinism=byte-identical ($name)"
  local bad=0 total=0
  while IFS=, read -r tag cname actual expected; do
    total=$((total+1))
    if [ "$actual" != "$expected" ]; then echo "MISMATCH ($name): $cname actual=$actual expected=$expected"; bad=$((bad+1)); fi
  done < <(grep '^CL_CHECK,' "$E/${name}_run1.stdout")
  echo "checks_total=$total checks_bad=$bad ($name)"
  while IFS=, read -r tag sname rest; do
    want="${EXP_STAT[$sname]:-}"; got="$rest"
    if [ -z "$want" ]; then echo "UNEXPECTED STAT ($name): $sname"; bad=$((bad+1)); continue; fi
    if [ "$got" != "$want" ]; then echo "STAT MISMATCH ($name): $sname got=$got want=$want"; bad=$((bad+1)); fi
  done < <(grep "^${stat_tag}," "$E/${name}_run1.stdout")
  echo "stat_check_done ($name)"
  grep -E "^${fail_tag}," "$E/${name}_run1.stdout" | tee -a "$E/summary.txt"
  if [ "$bad" -ne 0 ]; then echo "TRIAL FAILED ($name)"; overall_bad=1; else echo "TRIAL PASSED ($name)"; fi
}

# hand-computed expectations: tag -> rest-of-line after "TAG,name,"
# PT01_STAT: phase,grant_rc,stage,verify_count
declare -A EXP_STAT=(
  ["A"]="1,0,2,3"
  ["B"]="0,211,2,0"
  ["C"]="0,212,2,1"
  ["D"]="0,213,0,3"
  ["E"]="0,0,0,0"
  ["F"]="1,214,2,3"
)
run_one "trial01" "$BASE/trial01.zag" "PT01_STAT" "PT01_FAILURES"

# PT23_STAT: phase,commit_rc,judgments,promotes,arm
declare -A EXP_STAT=(
  ["A"]="3,0,8,4,3"
  ["B"]="2,222,2,1,3"
  ["C"]="2,222,0,0,3"
  ["D"]="3,0,8,4,3"
  ["E"]="3,0,8,4,3"
  ["F"]="3,0,8,4,3"
  ["G"]="3,0,8,4,3"
  ["H"]="2,223,8,4,3"
)
run_one "trial23" "$BASE/trial23.zag" "PT23_STAT" "PT23_FAILURES"

# PT34_STAT: phase,grant_rc,evid_spk1,evid_spk2,mask
declare -A EXP_STAT=(
  ["A"]="4,0,2,1,7"
  ["B"]="3,234,2,2,7"
  ["C"]="3,235,2,1,7"
  ["D"]="3,236,2,1,7"
  ["E"]="3,231,2,1,7"
  ["F"]="3,232,2,1,0"
  ["G"]="3,233,0,0,7"
  ["H"]="4,0,2,1,7"
)
run_one "trial34" "$BASE/trial34.zag" "PT34_STAT" "PT34_FAILURES"

if [ "$overall_bad" -ne 0 ]; then echo "WAVE-5 PHASE-TRANSITIONS-REMAINING: FAILED"; exit 1; fi
echo "WAVE-5 PHASE-TRANSITIONS-REMAINING: ALL TRIALS PASSED"
