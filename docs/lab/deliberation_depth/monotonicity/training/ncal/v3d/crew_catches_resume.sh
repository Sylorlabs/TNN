#!/usr/bin/env bash
# CREW C resume — missing legs + bars + T3 + asymmetry. Logs to file (true exit code).
set -e
export TMPDIR=~/workspace/tmp_commit
J=~/workspace/nec_v3b/job4; B=$J/bin/nec_h2h_bin; W=$J/work; S=$W/speed; K=$W/catches
N=~/workspace/selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal
ATT=~/workspace/nec_v3b/job1/batteries
A=$J/analysis
mkdir -p $K; cd $K
LOG=$K/CATCHES_LOG.md
exec >>$LOG 2>&1
echo "=== CREW C RESUME (2026-09-25) ==="

mkrun() { # scale variant infile tag [tracefile]
  local s=$1 v=$2 f=$3 tag=$4 trace=${5:-} r
  # idempotent: skip legs whose A/B/C already exist byte-identical
  if [ -f ${tag}_A.tsv ] && [ -f ${tag}_B.tsv ] && [ -f ${tag}_C.tsv ] && \
     cmp -s ${tag}_A.tsv ${tag}_B.tsv && cmp -s ${tag}_B.tsv ${tag}_C.tsv; then
    echo "SKIP $tag (already A/B/C identical)"
    return 0
  fi
  if [ -n "$trace" ]; then
    $B $s $v $f ${tag}_A.tsv "$trace"
    for r in B C; do $B $s $v $f ${tag}_${r}.tsv; done
  else
    for r in A B C; do $B $s $v $f ${tag}_${r}.tsv; done
  fi
  sha256sum ${tag}_A.tsv ${tag}_B.tsv ${tag}_C.tsv >> sha_catches.txt
  if cmp -s ${tag}_A.tsv ${tag}_B.tsv && cmp -s ${tag}_B.tsv ${tag}_C.tsv; then
    echo "OK $tag A/B/C identical"
  else echo "FAIL $tag NON-DETERMINISTIC"; exit 1; fi
}

echo "--- v20 remaining legs ---"
mkrun s100 20 $ATT/rtd_s100.tsv rt20_rtd_s100
for e in learn fatigue solo_learn solo_fatigue; do mkrun s1 20 $ATT/rte_$e.tsv rt20_rte_$e; done
mkrun s1 20 $ATT/rtf_collide.tsv rt20_rtf_collide
mkrun s1 20 $N/q2_traps/trap_t1.tsv v20_t1
mkrun s1 20 $N/q2_traps/trap_t3.tsv v20_t3
echo "--- v26 all legs ---"
for v in 26; do
  mkrun s1 $v $ATT/rta_s1.tsv       rt${v}_rta_s1
  mkrun s1 $v $ATT/rtb_s1.tsv       rt${v}_rtb_s1  26_rtb_trace.tsv
  for c in base v1 v2 v3 v4 v5 v6; do mkrun s1 $v $ATT/rtc_$c.tsv rt${v}_rtc_$c; done
  for s in s1 s10 s100; do mkrun $s $v $ATT/rtd_$s.tsv rt${v}_rtd_$s; done
  for e in learn fatigue solo_learn solo_fatigue; do mkrun s1 $v $ATT/rte_$e.tsv rt${v}_rte_$e; done
  mkrun s1 $v $ATT/rtf_collide.tsv  rt${v}_rtf_collide 26_rtf_trace.tsv
  mkrun s1 $v $N/q2_traps/trap_t1.tsv v${v}_t1
  mkrun s1 $v $N/q2_traps/trap_t3.tsv v${v}_t3 26_t3_trace.tsv
done
ls *_trace.tsv

echo "=== legs + frozen bars ==="
for spec in "20 s1 s10 s100" "26 s1 s10 s100"; do
  set -- $spec; v=$1; shift
  for s in "$@"; do
    case $s in
      s1)   inp=$N/necc_input.tsv;;
      s10)  inp=~/workspace/nec_v2d/work/necc_input_s10.tsv;;
      s100) inp=~/workspace/nec_v2d/work/necc_input_s100.tsv;;
    esac
    python3 $A/to_analyzer.py $S/${s}_v${v}_A.tsv legs_mx_v${v}_${s} v$v
    echo "##### matrix v$v $s #####"
    python3 $A/bars_full.py legs_mx_v${v}_${s} v$v $S/${s}_v${v}_A.tsv "$inp" 2>&1 | grep -E "^B[0-9]"
  done
done | tee bars_matrix.txt
for v in 20 26; do
  while read -r t20 t26 inp; do
    case $v in 20) tag=$t20;; 26) tag=$t26;; esac
    [ -z "$tag" ] && continue
    python3 $A/to_analyzer.py ${tag}_A.tsv legs_$tag v$v
    echo "##### $tag #####"
    python3 $A/bars_full.py legs_$tag v$v ${tag}_A.tsv "$inp" 2>&1 | grep -E "^B[0-9]|G curves"
  done < batteries.list
done | tee bars_rt.txt
echo "BARS DONE"

echo "=== T3 head-to-head ==="
cp $N/q2_traps/trap_t3_truth.tsv .
python3 $A/t3_h2h.py $K | tee t3_h2h.txt

echo "=== asymmetry (|err|<=0.100 catch rule) ==="
python3 $A/asymmetry.py $K | tee asymmetry.txt

echo "=== white-box trace excerpts ==="
echo "--- v26 RT-B wrong-first item (rtb-wf-00) ---"
grep -E "^(L0|L1) rtb-wf-00 " 26_rtb_trace.tsv | head -8
echo "--- v20 RT-B wrong-first item (output confs; rule exact per E1) ---"
grep -E "^rtb-wf-00\t" rt20_rtb_s1_A.tsv
echo "--- v26 RT-B correct-first control (rtb-cf-00) ---"
grep -E "^(L0|L1) rtb-cf-00 " 26_rtb_trace.tsv | head -8 || true
echo "--- v26 T3 trap classes (which backoff level) ---"
grep "^L0 T3C" 26_t3_trace.tsv | awk '{print $1, $2, "f1="$3, "f5="$4, "d="$5, "level="$6, "celln="$7, "rate="$8}' | head -12
echo "--- v26 RT-F long-id item (every obs = first obs?) ---"
awk -F'\t' '{print $1}' $ATT/rtf_collide.tsv | sort -u | head -3
LONGID=$(awk -F'\t' '{if (length($1)>63) {print $1; exit}}' $ATT/rtf_collide.tsv)
echo "long id: ${LONGID:0:40}... len=${#LONGID}"
grep -c "^L0 ${LONGID} " 26_rtf_trace.tsv || true
grep "^L0 ${LONGID} " 26_rtf_trace.tsv | head -6
echo "CATCHES DONE $(date -u +%FT%TZ)"
