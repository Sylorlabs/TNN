#!/usr/bin/env bash
# CREW A — SPEED (S1/S2/S3). Runs EXCLUSIVE on the machine for wall-clock timing.
# Creates work/speed/timing_done.flag when all wall-clock sampling is complete.
set -e
export TMPDIR=~/workspace/tmp_commit
J=~/workspace/nec_v3b/job4; B=$J/bin/nec_h2h_bin; W=$J/work; S=$W/speed
N=~/workspace/selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal
V2D=~/workspace/nec_v2d/work
mkdir -p $S; cd $S
LOG=$S/SPEED_LOG.md
{
echo "# CREW A — SPEED log (2026-09-25)"
echo "binary: $(sha256sum $B | cut -d' ' -f1)"
echo "toolchain: $(sha256sum ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 | cut -d' ' -f1)"
echo "machine: $(nproc) cores; $(grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)"
free -g | head -2; echo "load: $(cat /proc/loadavg)"
} | tee $LOG

timed_leg() { # variant scale infile tag ; 3 timed A/B/C runs, SHA-logged, determinism-checked
  local v=$1 s=$2 f=$3 tag=$4 r t0 t1
  : > ${tag}_ns.txt
  for r in A B C; do
    t0=$(date +%s%N)
    $B $s $v $f ${tag}_${r}.tsv
    t1=$(date +%s%N)
    echo "$((t1-t0))" >> ${tag}_ns.txt
  done
  sha256sum ${tag}_A.tsv ${tag}_B.tsv ${tag}_C.tsv >> sha_speed.txt
  if cmp -s ${tag}_A.tsv ${tag}_B.tsv && cmp -s ${tag}_B.tsv ${tag}_C.tsv; then
    echo "OK $tag A/B/C identical :: $(cat ${tag}_ns.txt | tr '\n' ' ')" | tee -a $LOG
  else echo "FAIL $tag NON-DETERMINISTIC" | tee -a $LOG; exit 1; fi
}

echo "=== S1 matrix timing (sequential, quiet machine) ===" | tee -a $LOG
timed_leg 20 s1   $N/necc_input.tsv            s1_v20
timed_leg 26 s1   $N/necc_input.tsv            s1_v26
timed_leg 20 s10  $V2D/necc_input_s10.tsv      s10_v20
timed_leg 26 s10  $V2D/necc_input_s10.tsv      s10_v26
timed_leg 20 s100 $V2D/necc_input_s100.tsv     s100_v20
timed_leg 26 s100 $V2D/necc_input_s100.tsv     s100_v26

# cross-check: v20 outputs must reproduce the adopted gate SHAs
for t in s1 s10 s100; do
  if cmp -s ${t}_v20_A.tsv $W/gate20_${t}_A.tsv; then echo "GATE-XCHECK $t v20 == adopted m20 OK" | tee -a $LOG
  else echo "GATE-XCHECK $t v20 DIFFERS FROM ADOPTED" | tee -a $LOG; exit 1; fi
done

echo "=== S3 chunked tail (s1 -> 50 chunks x 20 items) ===" | tee -a $LOG
cut -f1 $N/necc_input.tsv | awk '!seen[$1]++' > items_ordered.txt
wc -l items_ordered.txt | tee -a $LOG
split -n l/50 -d items_ordered.txt chunk_ids_   # chunk_ids_00 .. chunk_ids_49
: > /dev/null
# empty-input overhead calibration (10x)
: > empty.tsv
: > overhead_ns.txt
$B s1 20 empty.tsv probe_empty.tsv || { echo "EMPTY INPUT FAILED"; exit 1; }
for i in $(seq 1 10); do
  t0=$(date +%s%N); $B s1 20 empty.tsv probe_empty.tsv; t1=$(date +%s%N)
  echo "$((t1-t0))" >> overhead_ns.txt
done
echo "overhead_ns: $(cat overhead_ns.txt | tr '\n' ' ')" | tee -a $LOG

for v in 20 26; do
  : > chunk_ns_v${v}.txt
  for c in chunk_ids_*; do
    grep -F -f $c $N/necc_input.tsv > chunk_in.tsv
    t0=$(date +%s%N)
    $B s1 $v chunk_in.tsv chunk_out.tsv
    t1=$(date +%s%N)
    echo "$((t1-t0))" >> chunk_ns_v${v}.txt
    cat chunk_out.tsv >> chunks_v${v}_all.tsv
  done
done
echo "chunk runs done" | tee -a $LOG

# S3 semantic check: every chunked (id,depth,conf) matches the full-run A output
python3 - "$S" <<'EOF'
import sys
S=sys.argv[1]
def load(p):
    d={}
    for ln in open(p):
        f=ln.rstrip('\n').split('\t')
        d[(f[0],f[2])]=(f[4],f[5])
    return d
ok=True
for v in ('20','26'):
    full=load(f"{S}/s1_v{v}_A.tsv")
    n=0
    for ln in open(f"{S}/chunks_v{v}_all.tsv"):
        f=ln.rstrip('\n').split('\t'); n+=1
        if full.get((f[0],f[2]))!=(f[4],f[5]):
            print(f"MISMATCH v{v} {f[0]} d{f[2]}"); ok=False; break
    print(f"v{v}: {n} chunked rows verified against full run")
print("CHUNK-SEMANTIC-CHECK", "PASS" if ok else "FAIL")
EOF

echo "=== S2 deliberation steps (v26 trace; v20 by source) ===" | tee -a $LOG
$B s1 26 $N/necc_input.tsv s2_v26_s1_A.tsv s2_v26_s1_trace.tsv
for r in B C; do $B s1 26 $N/necc_input.tsv s2_v26_s1_${r}.tsv; done
sha256sum s2_v26_s1_A.tsv s2_v26_s1_B.tsv s2_v26_s1_C.tsv >> sha_speed.txt
cmp -s s2_v26_s1_A.tsv s1_v26_A.tsv && echo "trace-run output == scored s1_v26_A OK" | tee -a $LOG
awk '$1=="L0"{lvl[$6]++} END{for(l in lvl) printf "L%d: %d\n", l, lvl[l]}' s2_v26_s1_trace.tsv | sort | tee -a $LOG
grep -n "d1prior" ~/workspace/nec_v3b/job3/src/nec_v3c.zag | head -8 | tee -a $LOG

touch $S/timing_done.flag
echo "TIMING DONE $(date -u +%FT%TZ)" | tee -a $LOG
