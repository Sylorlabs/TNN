#!/usr/bin/env bash
# NEC v3c JOB3 full scored matrix. A/B/C byte-identical, SHA-logged.
set -e
export TMPDIR=~/workspace/tmp_commit
J=~/workspace/nec_v3b/job3
B=$J/bin/nec_v3c_bin
W=$J/work
N=~/workspace/selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal
ATT=~/workspace/nec_v3b/job1/batteries
cd "$W"
SHA=$W/sha_runs_v3c.txt
: > $SHA
mkrun() { # scale variant in.tsv tag [tracefile_for_A]
  local scale=$1 variant=$2 in=$3 tag=$4 trace=${5:-} r
  if [ -n "$trace" ]; then
    $B "$scale" "$variant" "$in" "${tag}_A.tsv" "$trace"
    for r in B C; do $B "$scale" "$variant" "$in" "${tag}_${r}.tsv"; done
  else
    for r in A B C; do $B "$scale" "$variant" "$in" "${tag}_${r}.tsv"; done
  fi
  sha256sum "${tag}_A.tsv" "${tag}_B.tsv" "${tag}_C.tsv" | tee -a $SHA
  if cmp -s "${tag}_A.tsv" "${tag}_B.tsv" && cmp -s "${tag}_B.tsv" "${tag}_C.tsv"; then
    echo "OK $tag A/B/C byte-identical"
  else echo "FAIL $tag NON-DETERMINISTIC"; exit 1; fi
}
echo "=== matrix s1/s10/s100 x variants 26/27 (S, S8) ==="
for v in 26 27; do
  mkrun s1   $v $N/necc_input.tsv                                  v${v}_s1  v${v}_s1_trace.tsv
  mkrun s10  $v ~/workspace/nec_v2d/work/necc_input_s10.tsv        v${v}_s10
  mkrun s100 $v ~/workspace/nec_v2d/work/necc_input_s100.tsv       v${v}_s100
done
echo "=== matrix s1 x variant 28 (D, s1-only) ==="
mkrun s1 28 $N/necc_input.tsv v28_s1 v28_s1_trace.tsv
echo "=== traps x variants 26/27/28 ==="
for v in 26 27 28; do
  mkrun s1 $v $N/q2_traps/trap_t1.tsv v${v}_t1
  mkrun s1 $v $N/q2_traps/trap_t3.tsv v${v}_t3
done
echo "=== RT-A ==="
mkrun s1 26 $ATT/rta_s1.tsv rt26_rta_s1
mkrun s1 27 $ATT/rta_s1.tsv rt27_rta_s1
mkrun s1 28 $ATT/rta_s1.tsv rt28_rta_s1
echo "=== RT-B ==="
mkrun s1 26 $ATT/rtb_s1.tsv rt26_rtb_s1
mkrun s1 27 $ATT/rtb_s1.tsv rt27_rtb_s1
mkrun s1 28 $ATT/rtb_s1.tsv rt28_rtb_s1
echo "=== RT-C ==="
for c in base v1 v2 v3 v4 v5 v6; do
  mkrun s1 26 $ATT/rtc_$c.tsv rt26_rtc_$c
  mkrun s1 27 $ATT/rtc_$c.tsv rt27_rtc_$c
  mkrun s1 28 $ATT/rtc_$c.tsv rt28_rtc_$c
done
echo "=== RT-D ==="
for s in s1 s10 s100; do
  mkrun $s 26 $ATT/rtd_$s.tsv rt26_rtd_$s
  mkrun $s 27 $ATT/rtd_$s.tsv rt27_rtd_$s
done
mkrun s1 28 $ATT/rtd_s1.tsv rt28_rtd_s1
echo "=== RT-E ==="
for e in learn fatigue solo_learn solo_fatigue; do
  mkrun s1 26 $ATT/rte_$e.tsv rt26_rte_$e
  mkrun s1 27 $ATT/rte_$e.tsv rt27_rte_$e
  mkrun s1 28 $ATT/rte_$e.tsv rt28_rte_$e
done
echo "=== RT-F ==="
mkrun s1 26 $ATT/rtf_collide.tsv rt26_rtf_collide
mkrun s1 27 $ATT/rtf_collide.tsv rt27_rtf_collide
mkrun s1 28 $ATT/rtf_collide.tsv rt28_rtf_collide
echo "=== ALL V3C RUNS COMPLETE ==="
