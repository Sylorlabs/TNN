#!/usr/bin/env bash
# CREW C — CATCHES. Full red-team + trap + unseen-class side-by-side, white-box traces.
# Waits for speed's timing_done.flag, then runs (machine otherwise quiet).
set -e
export TMPDIR=~/workspace/tmp_commit
J=~/workspace/nec_v3b/job4; B=$J/bin/nec_h2h_bin; W=$J/work; S=$W/speed; K=$W/catches
N=~/workspace/selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal
ATT=~/workspace/nec_v3b/job1/batteries
A3=~/workspace/nec_v3b/job3/analysis; A=$J/analysis
mkdir -p $K $A; cd $K
cp $A3/to_analyzer.py $A3/bars_full.py $A/
LOG=$K/CATCHES_LOG.md
echo "# CREW C — CATCHES log (2026-09-25)" | tee $LOG
echo "binary: $(sha256sum $B | cut -d' ' -f1)" | tee -a $LOG

echo "waiting for speed timing_done.flag ..." | tee -a $LOG
for i in $(seq 1 360); do [ -f $S/timing_done.flag ] && break; sleep 10; done
[ -f $S/timing_done.flag ] || { echo "TIMEOUT waiting for speed crew"; exit 1; }

mkrun() { # scale variant infile tag [tracefile]
  local s=$1 v=$2 f=$3 tag=$4 trace=${5:-} r
  if [ -n "$trace" ]; then
    $B $s $v $f ${tag}_A.tsv "$trace"
    for r in B C; do $B $s $v $f ${tag}_${r}.tsv; done
  else
    for r in A B C; do $B $s $v $f ${tag}_${r}.tsv; done
  fi
  # NOTE: RT-D legs must pass the matching scale (s10/s100); the original
  # calls below were fixed in crew_catches_resume.sh after rc=107 taught us
  # max_items(s1)=1200 < 8800 rtd_s100 items.
  sha256sum ${tag}_A.tsv ${tag}_B.tsv ${tag}_C.tsv >> sha_catches.txt
  if cmp -s ${tag}_A.tsv ${tag}_B.tsv && cmp -s ${tag}_B.tsv ${tag}_C.tsv; then
    echo "OK $tag A/B/C identical" | tee -a $LOG
  else echo "FAIL $tag NON-DETERMINISTIC" | tee -a $LOG; exit 1; fi
}

echo "=== RT batteries x {20,26} ===" | tee -a $LOG
for v in 20 26; do
  mkrun $v $ATT/rta_s1.tsv       rt${v}_rta_s1
  mkrun $v $ATT/rtb_s1.tsv       rt${v}_rtb_s1  ${v}_rtb_trace.tsv
  for c in base v1 v2 v3 v4 v5 v6; do mkrun $v $ATT/rtc_$c.tsv rt${v}_rtc_$c; done
  for s in s1 s10 s100; do mkrun $v $ATT/rtd_$s.tsv rt${v}_rtd_$s; done
  for e in learn fatigue solo_learn solo_fatigue; do mkrun $v $ATT/rte_$e.tsv rt${v}_rte_$e; done
  mkrun $v $ATT/rtf_collide.tsv  rt${v}_rtf_collide ${v}_rtf_trace.tsv
  mkrun $v $N/q2_traps/trap_t1.tsv v${v}_t1
  mkrun $v $N/q2_traps/trap_t3.tsv v${v}_t3 ${v}_t3_trace.tsv
done
# v20 traces are unsupported by the driver (26-28 only); v20 white-box comes from source+outputs.
ls *_trace.tsv | tee -a $LOG

echo "=== legs + frozen bars ===" | tee -a $LOG
cd $K
# matrix legs reuse speed crew's scored A outputs
for spec in "20 s1 s10 s100" "26 s1 s10 s100"; do
  set -- $spec; v=$1; shift
  for s in "$@"; do
    case $s in
      s1)   inp=$N/necc_input.tsv;;
      s10)  inp=~/workspace/nec_v2d/work/necc_input_s10.tsv;;
      s100) inp=~/workspace/nec_v2d/work/necc_input_s100.tsv;;
    esac
    python3 $A/to_analyzer.py $S/${s}_v${v}_A.tsv legs_mx_v${v}_${s} v$v
    echo "##### matrix v$v $s #####" | tee -a $LOG
    python3 $A/bars_full.py legs_mx_v${v}_${s} v$v $S/${s}_v${v}_A.tsv "$inp" 2>&1 | tee -a bars_matrix.txt | grep -E "^B[0-9]" | tee -a $LOG
  done
done
declare -A INMAP
tags=()
add() { tags+=("$1"); INMAP[$1]=$2; }
for v in 20 26; do
  add rt${v}_rta_s1 rta_s1; add rt${v}_rtb_s1 rtb_s1
  for c in base v1 v2 v3 v4 v5 v6; do add rt${v}_rtc_$c rtc_$c; done
  for s in s1 s10 s100; do add rt${v}_rtd_$s rtd_$s; done
  for e in learn fatigue solo_learn solo_fatigue; do add rt${v}_rte_$e rte_$e; done
  add rt${v}_rtf_collide rtf_collide
  add v${v}_t1 __TRAP_T1__; add v${v}_t3 __TRAP_T3__
done
for tag in "${tags[@]}"; do
  v=${tag:2:2}; [ "${tag:0:1}" = "v" ] && v=${tag:1:2}
  case "$tag" in v*) bat=${INMAP[$tag]}; [ "$bat" = "__TRAP_T1__" ] && inp=$N/q2_traps/trap_t1.tsv || inp=$N/q2_traps/trap_t3.tsv;; *) inp=$ATT/${INMAP[$tag]}.tsv;; esac
  python3 $A/to_analyzer.py ${tag}_A.tsv legs_$tag v$v
  echo "##### $tag #####" | tee -a $LOG
  python3 $A/bars_full.py legs_$tag v$v ${tag}_A.tsv "$inp" 2>&1 | tee -a bars_rt.txt | grep -E "^B[0-9]|G curves" | tee -a $LOG
done
echo "BARS DONE" | tee -a $LOG
