#!/bin/bash
# run_profiler.sh — G7 P0 instruments: per-arm per-op audit-count profilers.
# Builds prof_a.zag (Arm A only + pa_* per-op checks) and prof_b.zag
# (Arm B only + pb_* per-op checks). Each binary: 3 timed runs, median
# wall-clock reported; determinism (two runs sha256); every TN_CHECK
# verified; TN_FAILURES=0 required. Exits nonzero on any failure.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC="${ZNC:-$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1}"
fail=0
note() { echo "RUNNER: $1"; }

run_arm() {
  local arm="$1" src="$2"
  local bin="$D/prof_${arm}_linux"
  note "=== arm $arm ($src) ==="
  # static: no randomness (comments stripped)
  if sed 's|//.*||' "$D/tn.zag" "$D/$src" | grep -niE 'rng|rand\(|srand|/dev/urandom|[^a-z]seed[^a-z]' >/dev/null 2>&1; then
    note "FAIL no-randomness grep hit (arm $arm)"; fail=1; return
  fi
  "$ZNC" "$D/$src" --no-zagd --no-analyze --no-foreground-cache -o "$bin" 2>"$D/evidence_compile_${arm}.txt"
  if [ $? -ne 0 ]; then note "FAIL compile (arm $arm)"; cat "$D/evidence_compile_${arm}.txt"; fail=1; return; fi
  note "compile OK (arm $arm)"
  # 3 timed runs
  # 3 timed runs (wall-clock via date; diagnostic only)
  time_run() { local s e; s=$(date +%s.%N); "$bin" > "$1" 2>&1; e=$?; local t; t=$(date +%s.%N); echo "$t $s $e"; }
  read -r t1s t1b e1 <<< "$(time_run "$D/evidence_prof_${arm}_run1.txt")"
  read -r t2s t2b e2 <<< "$(time_run "$D/evidence_prof_${arm}_run2.txt")"
  read -r t3s t3b e3 <<< "$(time_run "$D/evidence_prof_${arm}_run3.txt")"
  t1=$(python3 -c "print(round($t1s-$t1b,3))"); t2=$(python3 -c "print(round($t2s-$t2b,3))"); t3=$(python3 -c "print(round($t3s-$t3b,3))")
  if [ "$e1" -ne 0 ] || [ "$e2" -ne 0 ] || [ "$e3" -ne 0 ]; then note "FAIL nonzero exit (arm $arm: $e1,$e2,$e3)"; fail=1; fi
  note "wall-clock arm $arm: run1=${t1}s run2=${t2}s run3=${t3}s"
  echo "$t1 $t2 $t3" > "$D/wallclock_${arm}.txt"
  s1=$(sha256sum "$D/evidence_prof_${arm}_run1.txt" | cut -d' ' -f1)
  s2=$(sha256sum "$D/evidence_prof_${arm}_run2.txt" | cut -d' ' -f1)
  if [ "$s1" != "$s2" ]; then note "FAIL determinism (arm $arm): $s1 != $s2"; fail=1
  else note "determinism OK arm $arm (sha256 $s1)"; fi
  bad=0; total=0
  while IFS=, read -r tag name actual expected; do
    total=$((total+1))
    if [ "$actual" != "$expected" ]; then echo "MISMATCH arm $arm $name: $actual != $expected"; bad=$((bad+1)); fi
  done < <(grep '^TN_CHECK,' "$D/evidence_prof_${arm}_run1.txt")
  note "arm $arm checks: $total total, $bad mismatched"
  [ $bad -ne 0 ] && fail=1
  hf=$(grep '^TN_FAILURES,' "$D/evidence_prof_${arm}_run1.txt" | cut -d, -f2)
  if [ "$hf" != "0" ]; then note "FAIL TN_FAILURES=$hf (arm $arm)"; fail=1; else note "TN_FAILURES=0 (arm $arm)"; fi
}

run_arm a prof_a.zag
run_arm b prof_b.zag

if [ $fail -eq 0 ]; then note "ALL PROFILER CHECKS PASS"; else note "PROFILER FAILURES PRESENT"; fi
exit $fail
