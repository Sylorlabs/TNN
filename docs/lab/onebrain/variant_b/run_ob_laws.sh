#!/bin/bash
# run_ob_laws.sh — batteries 3A..3F for the repaired-B one-brain Fable composition laws.
# Prereg: LAWS_PREREG.md (frozen). Builds each battery, runs each 3x,
# requires byte-identical reruns, runs 3E in pre AND post modes, and runs
# the static no-RNG + registry-authority checks.
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
WORK=~/workspace/onebrain_laws/work
mkdir -p "$WORK"
fail=0

build() { # name src extra-args
  echo "== build $1"
  "$ZNC" build "$2" -o "$WORK/$1.bin" $3 > "$WORK/$1.build.log" 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then echo "BUILD_FAIL $1"; tail -20 "$WORK/$1.build.log"; fail=1; fi
  return $rc
}

run3() { # name tag args
  echo "== run $1 ($2)"
  local log="$WORK/$1.$2"
  for i in 1 2 3; do
    "$WORK/$1.bin" $3 > "$log.run$i.log" 2>&1
    rc=$?
    if [ $rc -ne 0 ]; then echo "RUN_FAIL $1/$2 run$i rc=$rc"; tail -5 "$log.run$i.log"; fail=1; fi
  done
  cmp -s "$log.run1.log" "$log.run2.log" || { echo "NONDETERMINISTIC $1/$2 (run1 vs run2)"; fail=1; }
  cmp -s "$log.run2.log" "$log.run3.log" || { echo "NONDETERMINISTIC $1/$2 (run2 vs run3)"; fail=1; }
  nfail=$(grep -oE 'LAW(3A|3B|3C|3D|3E|3F)_FAILURES,[0-9]+' "$log.run1.log" | tail -1 | cut -d, -f2)
  if [ -n "$nfail" ] && [ "$nfail" != "0" ]; then
    echo "CHECKS_FAILED $1/$2 failures=$nfail"
    grep 'LAW_CHECK' "$log.run1.log" | while IFS= read -r l; do
      act=$(echo "$l" | cut -d, -f3); exp=$(echo "$l" | cut -d, -f4)
      [ "$act" != "$exp" ] && echo "  FAIL: $l"
    done
    fail=1
  fi
  batt=$(echo "$1" | sed 's/^ob_laws_//' | tr a-z A-Z)
  if ! grep -q "LAW${batt}_DONE" "$log.run1.log"; then
    echo "MISSING_DONE_MARKER $1/$2"; fail=1
  fi
}

build ob_laws_3a ob_test_laws_3a.zag ""
build ob_laws_3b ob_test_laws_3b.zag ""
build ob_laws_3c ob_test_laws_3c.zag ""
build ob_laws_3d ob_test_laws_3d.zag ""
build ob_laws_3e ob_test_laws_3e.zag ""
build ob_laws_3f ob_test_laws_3f.zag ""

run3 ob_laws_3a 3a ""
run3 ob_laws_3b 3b ""
run3 ob_laws_3c 3c ""
run3 ob_laws_3d 3d ""
run3 ob_laws_3f 3f ""
run3 ob_laws_3e 3e-pre pre
run3 ob_laws_3e 3e-post post

# 3E contrast: pre must show breaks executed, post must show all refused.
if ! grep -q '3E-pre_revoke_executed,1,1' "$WORK/ob_laws_3e.3e-pre.run1.log"; then echo "3E_PRE_MISSING pre_revoke_executed"; fail=1; fi
if ! grep -q '3E-pre_forcepin_executed,1,1' "$WORK/ob_laws_3e.3e-pre.run1.log"; then echo "3E_PRE_MISSING pre_forcepin_executed"; fail=1; fi
if ! grep -q '3E-pre_tampered_executed,1,1' "$WORK/ob_laws_3e.3e-pre.run1.log"; then echo "3E_PRE_MISSING pre_tampered_executed"; fail=1; fi

# static 3A-4: registry nonce/issued write sites only in laws_registry_open.
viol=$(grep -n 'laws_reg_issue\|reg_\[\|reg_nl\[' ob_laws.zag | grep -v 'laws_registry_open' | grep -v '^.*://' || true)
if [ -n "$viol" ]; then echo "3A-4 STATIC FAIL: registry write outside laws_registry_open:"; echo "$viol"; fail=1; else echo "3A-4 static registry-authority OK"; fi

# static no-RNG scan over laws sources + this runner.
rng=$(grep -nE 'LCG|mt19937|lcgrand|srand|rand\(|/dev/urandom|random\(' ob_laws.zag ob_test_laws_3a.zag ob_test_laws_3b.zag ob_test_laws_3c.zag ob_test_laws_3d.zag ob_test_laws_3e.zag ob_test_laws_3f.zag run_ob_laws.sh | grep -v 'rng=$(grep' || true)
if [ -n "$rng" ]; then echo "STATIC RNG FAIL:"; echo "$rng"; fail=1; else echo "static no-RNG OK"; fi

if [ $fail -eq 0 ]; then echo "LAWS_SUITE_ALL_GREEN"; else echo "LAWS_SUITE_FAILED"; fi
exit $fail
