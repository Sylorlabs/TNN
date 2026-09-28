#!/bin/bash
# Strength trial runner: GATE first, then S1 cells. Two runs per config,
# byte-identical diff. Static checks: no-RNG grep, single strength-write site.
set -u
TRIAL_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$TRIAL_DIR/trial"
OUT_DIR="$TRIAL_DIR/evidence"
mkdir -p "$OUT_DIR"
BIN="$TRIAL_DIR/trial_bin"
LOG="$OUT_DIR/runner.log"
: > "$LOG"

pass=0; fail=0
note() { echo "$@" | tee -a "$LOG"; }
check() { # check <name> <cmd...>
  local name="$1"; shift
  if "$@" >>"$LOG" 2>&1; then note "PASS $name"; pass=$((pass+1));
  else note "FAIL $name"; fail=$((fail+1)); fi
}

note "=== static checks ==="
# 1. no RNG tokens in learner/decision paths
if grep -rniE "rand|srand|random|getrandom|/dev/urandom|rdtsc|time\(|clock_gettime" \
    "$SRC_DIR"/strength_core.zag "$SRC_DIR"/strength_learner.zag \
    "$SRC_DIR"/strength_trial.zag "$SRC_DIR"/strength_checker.zag >>"$LOG" 2>&1; then
  note "FAIL no_rng_tokens (matches found)"; fail=$((fail+1))
else
  note "PASS no_rng_tokens"; pass=$((pass+1))
fi
# 2. single strength-write site: all st_write_strength( callers must be in the
#    allowed set; st_write_strength defined once.
awk '
/^fn st_write_strength\(/{def++}
/st_write_strength\(s,/{ 
  # find enclosing fn: track last ^fn line
  callers[cur_fn]++
}
' "$SRC_DIR"/strength_core.zag > /dev/null 2>&1
# simpler: list (function, line) for each call site via grep -n + awk fn tracking
grep -n "st_write_strength(" "$SRC_DIR"/strength_core.zag | tee -a "$LOG" > /tmp/sw_calls.txt
awk '
/^fn /{fn=$2; sub(/\(.*/,"",fn)}
/st_write_strength\(s,/{print fn}
' "$SRC_DIR"/strength_core.zag | sort | uniq -c | tee -a "$LOG" > /tmp/sw_fns.txt
# allowed: st_write_strength (def), st_add_into_slot, st_redeclare,
#          st_trainer_declare, st_restore, st_clear_strength, st_add_core
allowed="st_write_strength st_add_into_slot st_redeclare st_trainer_declare st_restore st_clear_strength st_add_core st_overwrite"
ok=1
while read -r count fn; do
  case " $allowed " in
    *" $fn "*) ;;
    *) note "BAD strength-write caller: $fn"; ok=0;;
  esac
done < /tmp/sw_fns.txt
if [ "$ok" = 1 ]; then note "PASS strength_write_sites"; pass=$((pass+1));
else note "FAIL strength_write_sites"; fail=$((fail+1)); fi

note "=== GATE (runs first; any failure stops the trial) ==="
gate_fail=0
for arm in A B C; do
  if [ "$arm" = "A" ]; then arm_num=0; elif [ "$arm" = "B" ]; then arm_num=1; else arm_num=2; fi
  for run in 1 2; do
    "$BIN" "$arm" GATE 0 S1 > "$OUT_DIR/gate_${arm}_r${run}.log" 2>&1
    ec=$?
    echo "gate $arm run$run exit=$ec" >>"$LOG"
    if [ $ec -ne 0 ]; then note "FAIL gate_${arm}_r${run} exit=$ec"; gate_fail=1; fi
  done
  if cmp -s "$OUT_DIR/gate_${arm}_r1.log" "$OUT_DIR/gate_${arm}_r2.log"; then
    note "PASS gate_${arm}_deterministic"
  else
    note "FAIL gate_${arm}_deterministic"; gate_fail=1
  fi
  # gate must report f=0 (ST_GATE <arm> 0)
  if grep -q "^ST_GATE $arm_num 0$" "$OUT_DIR/gate_${arm}_r1.log"; then
    note "PASS gate_${arm}_checks"
  else
    note "FAIL gate_${arm}_checks"; gate_fail=1
  fi
done
if [ "$gate_fail" = 1 ]; then
  note "GATE FAILED — trial stops per prereg"
  echo "GATE_FAILED" > "$OUT_DIR/VERDICT.txt"
  note "pass=$pass fail=$fail"
  exit 1
fi
pass=$((pass+6))

note "=== S1 cells ==="
for arm in A B C; do
  for cur in VUP WBS JI; do
    for var in 0 1 2; do
      for run in 1 2; do
        "$BIN" "$arm" "$cur" "$var" S1 > "$OUT_DIR/cell_${arm}_${cur}_${var}_r${run}.log" 2>&1
        ec=$?
        if [ $ec -ne 0 ]; then note "FAIL cell_${arm}_${cur}_${var}_r${run} exit=$ec"; fail=$((fail+1)); fi
      done
      if cmp -s "$OUT_DIR/cell_${arm}_${cur}_${var}_r1.log" "$OUT_DIR/cell_${arm}_${cur}_${var}_r2.log"; then
        : # deterministic
      else
        note "FAIL cell_${arm}_${cur}_${var}_deterministic"; fail=$((fail+1))
      fi
      if grep -q "^ST_INVALID 1$" "$OUT_DIR/cell_${arm}_${cur}_${var}_r1.log"; then
        note "FAIL cell_${arm}_${cur}_${var}_invalid"; fail=$((fail+1))
      fi
      if ! grep -q "^ST_DONE$" "$OUT_DIR/cell_${arm}_${cur}_${var}_r1.log"; then
        note "FAIL cell_${arm}_${cur}_${var}_nodone"; fail=$((fail+1))
      fi
    done
  done
done
note "=== done ==="
note "pass=$pass fail=$fail"
if [ "$fail" = 0 ]; then echo "S1_COMPLETE" > "$OUT_DIR/VERDICT.txt"; else echo "S1_FAILED" > "$OUT_DIR/VERDICT.txt"; fi
