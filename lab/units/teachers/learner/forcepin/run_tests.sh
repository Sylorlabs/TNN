#!/bin/bash
# run_tests.sh — B.6 force-pin full test gate.
# Builds + runs: module tests, wired scratch tests, static path audit.
# Determinism bar: N=5 byte-identical runs per binary + MALLOC_PERTURB_
# adversarial allocator runs. Fails closed: any nonzero check aborts.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
FLAGS="--no-zagd --no-analyze --no-foreground-cache"
WORK=~/workspace/tnn-lab/scratch_c3
mkdir -p "$WORK"
cd "$WORK"
FAIL=0

say(){ echo "C3_RUN,$1"; }

# ---- 0. static audit (claim c: no learner path sets/clears pins) ----
say "static.path_audit"
if ! "$HERE/static_audit.sh" > static_audit.log 2>&1; then
  echo "C3 FAIL: static path audit"; tail -5 static_audit.log; FAIL=1
else say "static.path_audit.ok"; fi

# ---- 1. module tests ----
say "build.test_forcepin"
if ! $ZNC "$HERE/tests/test_forcepin.zag" $FLAGS -o test_forcepin_bin 2>&1 | grep -q "wrote native binary"; then
  echo "C3 FAIL: build test_forcepin"; FAIL=1
else say "build.test_forcepin.ok"; fi

say "test.forcepin.run"
./test_forcepin_bin > forcepin_run1.log 2>&1
if ! grep -q "FORCEPIN PASS" forcepin_run1.log; then
  echo "C3 FAIL: test_forcepin"; tail -5 forcepin_run1.log; FAIL=1
else say "test.forcepin.pass.34checks"; fi

say "test.forcepin.det5"
for i in 2 3 4 5; do ./test_forcepin_bin > "forcepin_run$i.log" 2>&1; done
H1=$(sha256sum forcepin_run1.log | cut -d' ' -f1)
for i in 2 3 4 5; do
  Hi=$(sha256sum "forcepin_run$i.log" | cut -d' ' -f1)
  if [ "$Hi" != "$H1" ]; then echo "C3 FAIL: det run $i differs"; FAIL=1; fi
done
[ $FAIL -eq 0 ] && say "test.forcepin.det5.ok sha=$H1"

say "test.forcepin.perturb"
for p in 0 165 17; do
  MALLOC_PERTURB_=$p ./test_forcepin_bin > "forcepin_pert$p.log" 2>&1 || { echo "C3 FAIL: perturb $p"; FAIL=1; }
  Hp=$(sha256sum "forcepin_pert$p.log" | cut -d' ' -f1)
  if [ "$Hp" != "$H1" ]; then echo "C3 FAIL: perturb $p differs"; FAIL=1; fi
done
[ $FAIL -eq 0 ] && say "test.forcepin.perturb.ok"

# ---- 2. wired scratch tests (learner revise/reject/kill paths) ----
say "build.test_wired"
if ! $ZNC "$HERE/scratch/test_wired.zag" $FLAGS -o test_wired_bin 2>&1 | grep -q "wrote native binary"; then
  echo "C3 FAIL: build test_wired"; FAIL=1
else say "build.test_wired.ok"; fi

say "test.wired.run"
./test_wired_bin > wired_run1.log 2>&1
if ! grep -q "WIRED PASS" wired_run1.log; then
  echo "C3 FAIL: test_wired"; tail -8 wired_run1.log; FAIL=1
else say "test.wired.pass.17checks"; fi

say "test.wired.det5"
for i in 2 3 4 5; do ./test_wired_bin > "wired_run$i.log" 2>&1; done
W1=$(sha256sum wired_run1.log | cut -d' ' -f1)
for i in 2 3 4 5; do
  Wi=$(sha256sum "wired_run$i.log" | cut -d' ' -f1)
  if [ "$Wi" != "$W1" ]; then echo "C3 FAIL: wired det run $i differs"; FAIL=1; fi
done
[ $FAIL -eq 0 ] && say "test.wired.det5.ok sha=$W1"

say "test.wired.perturb"
for p in 0 165 17; do
  MALLOC_PERTURB_=$p ./test_wired_bin > "wired_pert$p.log" 2>&1 || { echo "C3 FAIL: wired perturb $p"; FAIL=1; }
  Wp=$(sha256sum "wired_pert$p.log" | cut -d' ' -f1)
  if [ "$Wp" != "$W1" ]; then echo "C3 FAIL: wired perturb $p differs"; FAIL=1; fi
done
[ $FAIL -eq 0 ] && say "test.wired.perturb.ok"

if [ $FAIL -ne 0 ]; then echo "C3_RESULT,FAIL"; exit 1; fi
echo "C3_RESULT,PASS det5_sha_module=$H1 det5_sha_wired=$W1"
