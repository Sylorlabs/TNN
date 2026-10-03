#!/bin/sh
# Championship runs: 4 sources x 5 reps, byte-identical within source,
# Zag log vs Python oracle, clean mastery over 228 clean IDs.
# Run from ~/workspace/richcomp. Logs -> runs/champ_<src>_rep<N>.log
set -e
cd ~/workspace/richcomp
BIN=src/prose_learn2
for src in grok sol step muse-native; do
  for rep in 1 2 3 4 5; do
    ./$BIN $src > runs/champ_${src}_rep${rep}.log 2>&1
  done
  # KB2-DET: 5/5 byte-identical
  for rep in 2 3 4 5; do
    cmp -s runs/champ_${src}_rep1.log runs/champ_${src}_rep${rep}.log || {
      echo "NONDET $src rep$rep"; exit 1; }
  done
  echo "DET-OK $src 5/5"
  # oracle cross-check on the canonical rep
  python3 src/oracle2.py $src inputs > runs/champ_${src}_oracle.log 2>&1
  if cmp -s runs/champ_${src}_rep1.log runs/champ_${src}_oracle.log; then
    echo "ORACLE-0DIFF $src"
  else
    echo "ORACLE-DIFF $src"; exit 1
  fi
  # clean mastery from the SUMMARY line
  grep '^SUMMARY' runs/champ_${src}_rep1.log
done
echo "ALL CHAMPIONSHIP RUNS DONE"
