#!/bin/sh
# run_all.sh -- L3-INR DEV battery: 3/3 byte-identical runs per arm.
# Usage: run_all.sh [seed]   (default seed 7)
# Sequences (fresh statedir per run):
#   seq_i:  T1(dev_s1) -> T2 -> T3 -> C5 -> T4(dev_s2) -> T3b(dev_s1p)
#   t5a_i:  T5a(dev_s3a)      t5b_i: T5b(dev_s3b)
#   c0_i/c1_i/c2_i: C0/C1/C2 on dev_s1
#   c3t_i:  C3 on dev_s1trap  c4_i: C4 on dev_s1
# After all runs: sha256 digests per arm-run; 3/3 byte-identical check.
set -e
export PATH="$HOME/safebin"
HERE=$(dirname "$0")
SEED="${1:-7}"
RUNS="$HERE/runs"
mkdir -p "$RUNS"
run_seq() {
  i="$1"
  d="$RUNS/seq_$i"
  "$HERE/run_arm.sh" "$d" T1 "$HERE/dev/dev_s1.world" "$SEED" || return 1
  "$HERE/run_arm.sh" "$d" T2 "$HERE/dev/dev_s1.world" "$SEED" || return 1
  "$HERE/run_arm.sh" "$d" T3 "$HERE/dev/dev_s1.world" "$SEED" || return 1
  "$HERE/run_arm.sh" "$d" C5 "$HERE/dev/dev_s1.world" "$SEED" || return 1
  "$HERE/run_arm.sh" "$d" T4 "$HERE/dev/dev_s2.world" "$SEED" || return 1
  "$HERE/run_arm.sh" "$d" T3b "$HERE/dev/dev_s1p.world" "$SEED" || return 1
}
run_one() {
  # run_one <name> <arm> <world>
  d="$RUNS/$1"
  "$HERE/run_arm.sh" "$d" "$2" "$HERE/dev/$3" "$SEED" || return 1
}
i=1
while [ $i -le 3 ]; do
  echo "=== run $i/3 ==="
  run_seq "$i" || { echo "SEQ $i FAILED"; exit 1; }
  run_one "t5a_$i" T5a dev_s3a.world || { echo "T5a $i FAILED"; exit 1; }
  run_one "t5b_$i" T5b dev_s3b.world || { echo "T5b $i FAILED"; exit 1; }
  run_one "c0_$i" C0 dev_s1.world || { echo "C0 $i FAILED"; exit 1; }
  run_one "c1_$i" C1 dev_s1.world || { echo "C1 $i FAILED"; exit 1; }
  run_one "c2_$i" C2 dev_s1.world || { echo "C2 $i FAILED"; exit 1; }
  run_one "c3t_$i" C3 dev_s1trap.world || { echo "C3t $i FAILED"; exit 1; }
  run_one "c4_$i" C4 dev_s1.world || { echo "C4 $i FAILED"; exit 1; }
  i=$((i+1))
done
echo "ALL RUNS COMPLETE"
# digests: per arm, hash summary+trace+proto across the 3 runs
"$HERE/digests.sh" "$RUNS"
