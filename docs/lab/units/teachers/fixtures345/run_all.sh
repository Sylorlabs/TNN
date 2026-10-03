#!/bin/bash
# run_all.sh — build + test + determinism gate for teacher fixtures (arms 3/4/5).
# Fails closed: any nonzero check aborts the run.
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
FLAGS="--no-zagd --no-analyze --no-foreground-cache"
FAIL=0

say(){ echo "T345_RUN,$1"; }

# ---- 1. static checks (no RNG, no wallclock, arm4/5 proposal-free) ----
say "static.no_rng_wallclock"
if grep -rn "urandom\|gettimeofday\|clock_gettime\|wallclock" --include="*.zag" . | grep -v "^./run_all" | grep -iv "no wallclock"; then
  echo "STATIC FAIL: rng/wallclock reference"; FAIL=1;
else say "static.no_rng_wallclock.ok"; fi

say "static.arm4_no_proposal_symbols"
if grep -n "sp_encode\|sp_decode\|sp_validate\|TEACHER_MSG" arm4.zag; then
  echo "STATIC FAIL: arm4 references proposal path"; FAIL=1;
else say "static.arm4_no_proposal_symbols.ok"; fi

say "static.arm5_no_proposal_symbols"
if grep -n "sp_encode\|sp_decode\|sp_validate\|TEACHER_MSG" arm5.zag; then
  echo "STATIC FAIL: arm5 references proposal path"; FAIL=1;
else say "static.arm5_no_proposal_symbols.ok"; fi

say "static.arm45_import_graph"
if grep -n '@import("sp345.zag")' arm4.zag arm5.zag; then
  echo "STATIC FAIL: arm4/5 import the proposal codec"; FAIL=1;
else say "static.arm45_import_graph.ok"; fi

# ---- 2. build ----
for a in arm3 arm4 arm5; do
  say "build.$a"
  if ! $ZNC "$a.zag" $FLAGS -o "${a}_bin" 2>&1 | grep -q "wrote native binary"; then
    echo "BUILD FAIL: $a"; FAIL=1;
  else say "build.$a.ok"; fi
done
[ $FAIL -ne 0 ] && { echo "T345_RESULT,FAIL,build_or_static"; exit 1; }

# ---- 3. self-tests ----
for a in arm3 arm4 arm5; do
  say "selftest.$a"
  OUT=$(./${a}_bin test 2>&1); EC=$?
  echo "$OUT" | grep "^T345_TEST," > /tmp/t345_self_$a.log
  BAD=$(awk -F, '$3!=$4{c++} END{print c+0}' /tmp/t345_self_$a.log)
  N=$(wc -l < /tmp/t345_self_$a.log)
  echo "T345_SELFTEST,$a,checks=$N,bad=$BAD,exit=$EC"
  if [ "$BAD" != "0" ] || [ "$EC" != "0" ]; then echo "SELFTEST FAIL: $a"; cat /tmp/t345_self_$a.log; FAIL=1; fi
done

# ---- 4. functional runs (expected exit codes) ----
run_expect(){ # name expected_exit args...
  local name=$1 want=$2; shift 2
  ./$@ > /tmp/t345_func_$name.log 2>&1; local ec=$?
  echo "T345_FUNC,$name,exit=$ec,want=$want"
  if [ "$ec" != "$want" ]; then echo "FUNC FAIL: $name"; cat /tmp/t345_func_$name.log; FAIL=1; fi
}
rm -f tape_*.tape
run_expect arm3_teach 0    ./arm3_bin dryrun dryrun_teach.txt tape_teach.tape
run_expect arm3_violation 4 ./arm3_bin dryrun dryrun_violation.txt tape_violation.tape
run_expect arm3_smuggle 11 ./arm3_bin dryrun dryrun_smuggle.txt tape_smuggle.tape
run_expect arm4_hints 0    ./arm4_bin hints gt_demo.txt tape_hints.tape
run_expect arm5_oracle 0   ./arm5_bin answer gt_demo.txt queries_demo.txt tape_oracle.tape
# arm5 brackets: K=16/32/64 legs
run_expect arm5_k16 0 ./arm5_bin answer gt_demo.txt queries_demo.txt tape_oracle_k16.tape 16
run_expect arm5_k64 0 ./arm5_bin answer gt_demo.txt queries_demo.txt tape_oracle_k64.tape 64

# spot assertions on oracle behavior
A16=$(grep -c "REFUSED (budget exhausted)" /tmp/t345_func_arm5_k16.log)
echo "T345_FUNC,arm5_k16_refused=$A16,want=20"
[ "$A16" != "20" ] && { echo "FUNC FAIL: arm5 k16 refusal count"; FAIL=1; }
A64=$(grep -c "REFUSED (budget exhausted)" /tmp/t345_func_arm5_k64.log)
echo "T345_FUNC,arm5_k64_refused=$A64,want=0"
[ "$A64" != "0" ] && { echo "FUNC FAIL: arm5 k64 refusal count"; FAIL=1; }

# ---- 5. byte-identical reruns N=5 (fresh dir each run: catches path/cwd dependence) ----
rerun5(){ # name tape binary args...
  local name=$1; shift
  local tape=$1; shift
  local H=""
  for r in 1 2 3 4 5; do
    D=/tmp/t345_rerun_${name}_$r
    rm -rf "$D"; mkdir -p "$D"
    cp gt_demo.txt queries_demo.txt dryrun_teach.txt dryrun_violation.txt dryrun_smuggle.txt "$D/" 2>/dev/null
    cp arm3_bin arm4_bin arm5_bin "$D/"
    ( cd "$D" && "$@" > stdout.log 2>&1 )
    local h=$(cat "$D/$tape" "$D/stdout.log" | sha256sum | cut -d' ' -f1)
    echo "T345_RERUN,$name,run=$r,hash=$h"
    if [ -z "$H" ]; then H=$h; elif [ "$H" != "$h" ]; then echo "RERUN FAIL: $name run $r differs"; FAIL=1; fi
  done
  echo "T345_RERUN,$name,identical5=$([ $FAIL -eq 0 ] && echo yes || echo CHECK)"
}
rerun5 arm3_teach    tape_teach.tape    ./arm3_bin dryrun dryrun_teach.txt tape_teach.tape
rerun5 arm3_violation tape_violation.tape ./arm3_bin dryrun dryrun_violation.txt tape_violation.tape
rerun5 arm3_smuggle  tape_smuggle.tape  ./arm3_bin dryrun dryrun_smuggle.txt tape_smuggle.tape
rerun5 arm4_hints    tape_hints.tape    ./arm4_bin hints gt_demo.txt tape_hints.tape
rerun5 arm5_oracle   tape_oracle.tape   ./arm5_bin answer gt_demo.txt queries_demo.txt tape_oracle.tape

if [ $FAIL -ne 0 ]; then echo "T345_RESULT,FAIL"; exit 1; fi
echo "T345_RESULT,PASS"
