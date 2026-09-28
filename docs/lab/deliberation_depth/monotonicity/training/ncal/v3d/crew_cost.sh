#!/usr/bin/env bash
# CREW B — COST (C1..C5). Static analysis first; RSS runs wait for speed's timing_done.flag.
set -e
export TMPDIR=~/workspace/tmp_commit
J=~/workspace/nec_v3b/job4; B=$J/bin/nec_h2h_bin; W=$J/work; S=$W/speed; C=$W/cost
N=~/workspace/selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal
V2D=~/workspace/nec_v2d/work
SRC=~/workspace/nec_v3b/job3/src
mkdir -p $C; cd $C
LOG=$C/COST_LOG.md
{
echo "# CREW B — COST log (2026-09-25)"
echo "binary: $(sha256sum $B | cut -d' ' -f1) ($(stat -c%s $B) bytes)"
echo "nec_v3c.zag: $(sha256sum $SRC/nec_v3c.zag | cut -d' ' -f1)"
echo "schema_kc.zag: $(sha256sum $SRC/schema_kc.zag | cut -d' ' -f1) ($(stat -c%s $SRC/schema_kc.zag) bytes)"
} | tee $LOG

echo "=== C1 per-item ledger (white-box source inspection) ===" | tee -a $LOG
grep -n "nio_alloc" $SRC/nec_v3c.zag | head -12 | tee -a $LOG
# slots 64 + confs 8 + pcp 8 + ptp 8 = 88 B/item — same arrays for variants 20/26
python3 - "$SRC/nec_v3c.zag" <<'EOF' | tee -a "$C/COST_LOG.md"
import re,sys
src=open(sys.argv[1]).read()
for name, per in [("slots",64),("confs",8),("pcp",8),("ptp",8)]:
    m=re.search(rf"let {name}:\[\]u8=nio_alloc\(\(max_items as i64\)\*(\d+)\);",src)
    print(name, "per-item bytes:", m.group(1) if m else "NOT-FOUND")
print("C1 total per-item ledger bytes = 64+8+8+8 = 88")
EOF
grep -n "max_items\s*:\|max_items=" $SRC/nec_v3c.zag | head -4 | tee -a $LOG
grep -n "htsize" $SRC/nec_v3c.zag | head -4 | tee -a $LOG

echo "=== C2 schema footprint (static) ===" | tee -a $LOG
grep -c "^    if(f1==" $SRC/schema_kc.zag | tee -a $LOG   # expect 312 L1 branches
sed -n '321,322p;570,571p' $SRC/schema_kc.zag | tee -a $LOG
python3 <<'EOF' | tee -a "$C/COST_LOG.md"
# data-table equivalent: L1=(f1,f5,dep,tot,rate)=5x8B; L2=(f1,f5,tot,rate)=4x8B; L3=(dep,tot,rate)=3x8B
l1, l2, l3 = 312, 246, 7
print(f"C2 data-equivalent: L1 {l1}*40={l1*40} + L2 {l2}*32={l2*32} + L3 {l3}*24={l3*24} = {l1*40+l2*32+l3*24} B")
print("m20 schema footprint: 0 B (d1prior is a compiled constant, no table)")
EOF

echo "=== C4 deliberation depth distribution (input property) ===" | tee -a $LOG
cut -f1,3 $N/necc_input.tsv | sort -u | cut -f2 | sort -n | uniq -c | tee -a $LOG
awk -F'\t' '{d[$3]++} END{for(k in d) printf "depth %s: %d rows\n", k, d[k]}' $N/necc_input.tsv | sort -n | tee -a $LOG

echo "waiting for speed timing_done.flag ..." | tee -a $LOG
for i in $(seq 1 360); do [ -f $S/timing_done.flag ] && break; sleep 10; done
[ -f $S/timing_done.flag ] || { echo "TIMEOUT waiting for speed crew"; exit 1; }

echo "=== C2 RSS delta (v26 - v20), /usr/bin/time -v, 3x each ===" | tee -a $LOG
rss_leg() { # variant scale infile tag
  local v=$1 s=$2 f=$3 tag=$4 r
  : > rss_${tag}.txt
  for r in 1 2 3; do
    /usr/bin/time -v $B $s $v $f rss_${tag}.tsv 2>&1 | grep "Maximum resident" | awk '{print $6}' >> rss_${tag}.txt
  done
  echo "$tag KB: $(cat rss_${tag}.txt | tr '\n' ' ')" | tee -a $LOG
  sha256sum rss_${tag}.tsv >> sha_cost.txt
}
rss_leg 20 s1   $N/necc_input.tsv            rss_s1_v20
rss_leg 26 s1   $N/necc_input.tsv            rss_s1_v26
rss_leg 20 s10  $V2D/necc_input_s10.tsv       rss_s10_v20
rss_leg 26 s10  $V2D/necc_input_s10.tsv       rss_s10_v26
rss_leg 20 s100 $V2D/necc_input_s100.tsv      rss_s100_v20
rss_leg 26 s100 $V2D/necc_input_s100.tsv      rss_s100_v26
# v20 RSS-run outputs must equal the scored outputs
cmp -s rss_s1_v20.tsv $S/s1_v20_A.tsv && echo "RSS-run v20 s1 == scored output OK" | tee -a $LOG

echo "=== C3 output bytes per item (from scored outputs) ===" | tee -a $LOG
for t in s1 s10 s100; do for v in 20 26; do
  bytes=$(stat -c%s $S/${t}_v${v}_A.tsv)
  echo "$t v$v: $bytes bytes" | tee -a $LOG
done; done
wc -l $S/s1_v20_A.tsv | tee -a $LOG

echo "=== C5 projection (1M items x 100 obs = 100M rows) ===" | tee -a $LOG
python3 - "$S" "$C" <<'EOF' | tee -a "$C/COST_LOG.md"
import sys, statistics
S, C = sys.argv[1], sys.argv[2]
def ns(tag):
    return [int(x) for x in open(f"{S}/{tag}_ns.txt").read().split()]
items = {"s1":1000, "s10":10000, "s100":100000}
rows  = {"s1":5240, "s10":52400, "s100":524000}
print("measured per-row wall (ns), mean of 3 runs:")
per_row = {}
for v in ("20","26"):
    for t in ("s1","s10","s100"):
        m = statistics.mean(ns(f"{t}_v{v}"))/rows[t]
        per_row[(v,t)] = m
        print(f"  v{v} {t}: {m:.1f} ns/row  (items={items[t]})")
    # projection uses s100 (largest, steadiest)
    pr = per_row[(v,"s100")]
    out_b = __import__("os").path.getsize(f"{S}/s100_v{v}_A.tsv")/rows["s100"]
    wall_s = 100_000_000 * pr / 1e9
    print(f"v{v} PROJECTION 1M items x 100 obs (100M rows):")
    print(f"  wall = 100M x {pr:.1f}ns = {wall_s:,.0f}s = {wall_s/3600:.2f}h")
    print(f"  ledger = 1M x 88B = {1_000_000*88/1e9:.3f} GB")
    print(f"  output = 100M x {out_b:.1f}B = {100_000_000*out_b/1e9:.2f} GB")
    print(f"  output bytes/row used: {out_b:.2f}")
print("assumptions: linear extrapolation from s100; arena allocator constant;")
print("single-threaded; no page-cache/GC effects; schema shared (not per-item).")
EOF
echo "COST DONE $(date -u +%FT%TZ)" | tee -a $LOG
