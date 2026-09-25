#!/usr/bin/env bash
set -e
export TMPDIR=~/workspace/tmp_commit
J=~/workspace/nec_v3b/job2
B=$J/bin/nec_v2d_bin
W=$J/work
N=~/workspace/selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal
cd "$W"
SHA=$W/sha_runs_v3b.txt
: > $SHA
mkrun() { # scale variant in.tsv tag -> A/B/C runs + sha + determinism check
  local scale=$1 variant=$2 in=$3 tag=$4 r
  for r in A B C; do $B "$scale" "$variant" "$in" "${tag}_${r}.tsv"; done
  sha256sum "${tag}_A.tsv" "${tag}_B.tsv" "${tag}_C.tsv" | tee -a $SHA
  if cmp -s "${tag}_A.tsv" "${tag}_B.tsv" && cmp -s "${tag}_B.tsv" "${tag}_C.tsv"; then
    echo "OK $tag A/B/C byte-identical"
  else echo "FAIL $tag NON-DETERMINISTIC"; exit 1; fi
}
echo "=== matrix s1/s10/s100 x variants 24/25 ==="
for v in 24 25; do
  mkrun s1   $v $N/necc_input.tsv m${v}_s1
  mkrun s10  $v ~/workspace/nec_v2d/work/necc_input_s10.tsv m${v}_s10
  mkrun s100 $v ~/workspace/nec_v2d/work/necc_input_s100.tsv m${v}_s100
done
echo "=== traps s1 x variants 24/25 ==="
for v in 24 25; do
  mkrun s1 $v $N/q2_traps/trap_t1.tsv m${v}_t1
  mkrun s1 $v $N/q2_traps/trap_t3.tsv m${v}_t3
done
echo "=== ALL V3B RUNS COMPLETE ==="
