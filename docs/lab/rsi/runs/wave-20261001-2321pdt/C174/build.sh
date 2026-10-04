#!/bin/sh
# build.sh -- C174 battery build and run. Pure Zag + shell.
# Usage: sh build.sh seal   -- generate world_sealed.zag (run ONCE,
#            then commit the seal before any eval output exists)
#        sh build.sh eval   -- build all binaries, run 3x each,
#            sha256 every output
#        sh build.sh selftest -- build+run the white-box self test 3x
export PATH="$HOME/safebin"
L=docs/lab/rsi/runs/wave-20261001-2321pdt/C174
cd ~/workspace/tnn-rsi || exit 1
set -e

cmd="$1"

if [ "$cmd" = "seal" ]; then
  znc "$L/c174_gen.zag" -o "$L/gen_bin"
  "./$L/gen_bin" > "$L/world_sealed.zag"
  echo "sealed: $L/world_sealed.zag"
  sha256sum "$L/world_sealed.zag"
  exit 0
fi

if [ "$cmd" = "selftest" ]; then
  cat "$L/armflag_s.zag" "$L/c174_sub.zag" "$L/c174_selftest.zag" > /tmp/c174_st.zag
  znc /tmp/c174_st.zag -o "$L/selftest_bin"
  mkdir -p "$L/runs"
  i=1
  while [ $i -le 3 ]; do
    "./$L/selftest_bin" > "$L/runs/selftest_$i.txt"
    i=$((i+1))
  done
  sha256sum "$L/runs/selftest_"*.txt
  exit 0
fi

if [ "$cmd" = "eval" ]; then
  if [ ! -f "$L/world_sealed.zag" ]; then
    echo "world_sealed.zag missing; run sh build.sh seal first" >&2
    exit 1
  fi
  cat "$L/armflag_s.zag" "$L/c174_sub.zag" "$L/world_sealed.zag" "$L/c174_eval.zag" > /tmp/c174_es.zag
  cat "$L/armflag_f.zag" "$L/c174_sub.zag" "$L/world_sealed.zag" "$L/c174_eval.zag" > /tmp/c174_ef.zag
  cat "$L/armflag_a.zag" "$L/c174_sub.zag" "$L/world_sealed.zag" "$L/c174_eval.zag" > /tmp/c174_ea.zag
  cat "$L/armflag_s.zag" "$L/c174_sub.zag" "$L/c174_migrate.zag" > /tmp/c174_mg.zag
  znc /tmp/c174_es.zag -o "$L/eval_S_bin"
  znc /tmp/c174_ef.zag -o "$L/eval_F_bin"
  znc /tmp/c174_ea.zag -o "$L/eval_A_bin"
  znc /tmp/c174_mg.zag -o "$L/migrate_bin"
  mkdir -p "$L/runs"
  for arm in S F A; do
    i=1
    while [ $i -le 3 ]; do
      "./$L/eval_${arm}_bin" > "$L/runs/eval_${arm}_$i.txt"
      i=$((i+1))
    done
  done
  i=1
  while [ $i -le 3 ]; do
    "./$L/migrate_bin" > "$L/runs/migrate_$i.txt"
    i=$((i+1))
  done
  sha256sum "$L/runs"/eval_*.txt "$L/runs"/migrate_*.txt
  exit 0
fi

echo "usage: sh build.sh seal|eval|selftest" >&2
exit 2
