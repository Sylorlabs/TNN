#!/bin/sh
# run_k1.sh -- K1 no-regression: run all 16 FW worlds through both shims
# (fresh state per world), compare stdout byte-for-byte.
# Blind: outputs are compared, never inspected for tuning.
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
cd "$HERE"
mkdir -p runs/pre runs/post
WORLDS="fw1_world.txt fw2_world.txt fw3_world.txt fw4_world.txt fw5_world.txt fw6_controlA.txt fw6_controlB.txt fw6_controlB2.txt fw6_phaseA1.txt fw6_phaseB1.txt fw6_phaseB2.txt fw6b_phaseA1.txt fw7_world.txt fw8_world.txt fw9_dagA.txt fw9_dagB.txt"
FAIL=0
for w in $WORLDS; do
  rm -f runs/pre/state.bin runs/post/state.bin
  ./shim_frozen worlds/$w runs/pre/state.bin > runs/pre/$w.out 2>runs/pre/$w.err; ec1=$?
  ./shim_unify  worlds/$w runs/post/state.bin > runs/post/$w.out 2>runs/post/$w.err; ec2=$?
  if [ $ec1 -ne $ec2 ]; then echo "EXIT-DIFF $w: pre=$ec1 post=$ec2"; FAIL=1; fi
  if cmp -s runs/pre/$w.out runs/post/$w.out; then
    echo "IDENTICAL $w"
  else
    echo "DIFF $w"; FAIL=1
  fi
done
# 3/3 run determinism on the post arm (K4): rerun everything twice more
for rep in 2 3; do
  mkdir -p runs/post$rep
  for w in $WORLDS; do
    rm -f runs/post$rep/state.bin
    ./shim_unify worlds/$w runs/post$rep/state.bin > runs/post$rep/$w.out 2>/dev/null
    if ! cmp -s runs/post/$w.out runs/post$rep/$w.out; then
      echo "RUN-NONDETERMINISM $w rep$rep"; FAIL=1
    fi
  done
  echo "rep$rep determinism ok"
done
if [ $FAIL -eq 0 ]; then echo "K1 PASS: all 16 worlds byte-identical pre/post"; else echo "K1 FAIL"; exit 1; fi
