#!/usr/bin/env bash
# CREW B resume — RSS via python resource module + C3 + C5. Appends to COST_LOG.md.
set -e
export TMPDIR=~/workspace/tmp_commit
J=~/workspace/nec_v3b/job4; B=$J/bin/nec_h2h_bin; W=$J/work; S=$W/speed; C=$W/cost
N=~/workspace/selfpam_run/tnn-lab/docs/lab/deliberation_depth/monotonicity/training/ncal
V2D=~/workspace/nec_v2d/work
cd $C
LOG=$C/COST_LOG.md
echo "=== C2 RSS (python resource.ru_maxrss, KB), 2x per leg ===" | tee -a $LOG
: > rss_results.txt
for spec in "s1 20 $N/necc_input.tsv rss_s1_v20" "s1 26 $N/necc_input.tsv rss_s1_v26" \
            "s10 20 $V2D/necc_input_s10.tsv rss_s10_v20" "s10 26 $V2D/necc_input_s10.tsv rss_s10_v26" \
            "s100 20 $V2D/necc_input_s100.tsv rss_s100_v20" "s100 26 $V2D/necc_input_s100.tsv rss_s100_v26"; do
  set -- $spec
  k1=$(python3 $J/analysis/rss_one.py $B $1 $2 $3 $4.tsv)
  k2=$(python3 $J/analysis/rss_one.py $B $1 $2 $3 $4.tsv)
  echo "$4 $k1 $k2" | tee -a $LOG >> rss_results.txt
done
# v20 RSS outputs must equal scored outputs (same bytes)
cmp -s rss_s1_v20.tsv $S/s1_v20_A.tsv && echo "RSS-run v20 s1 == scored output OK" | tee -a $LOG
cmp -s rss_s100_v26.tsv $S/s100_v26_A.tsv && echo "RSS-run v26 s100 == scored output OK" | tee -a $LOG
sha256sum rss_*.tsv >> sha_cost.txt

echo "=== C3 output bytes per item (from scored outputs) ===" | tee -a $LOG
for t in s1 s10 s100; do for v in 20 26; do
  bytes=$(stat -c%s $S/${t}_v${v}_A.tsv)
  echo "$t v$v: $bytes bytes" | tee -a $LOG
done; done

echo "=== C5 projection (1M items x 100 obs = 100M rows) ===" | tee -a $LOG
python3 - "$S" "$C" <<'EOF' | tee -a "$C/COST_LOG.md"
import sys, statistics, os
S, C = sys.argv[1], sys.argv[2]
def ns(tag):
    return [int(x) for x in open(f"{S}/{tag}_ns.txt").read().split()]
def med(tag):
    return statistics.median(ns(tag))
items = {"s1":1000, "s10":10000, "s100":100000}
rows  = {"s1":5240, "s10":52400, "s100":524000}
# interleave validation (5 alternating pairs, drift-cancelling)
pairs=[]
for ln in open(f"{S}/interleave_ns.txt"):
    p=ln.split()
    if p[0].startswith("pair"): pairs.append((p[1], int(p[2])))
v20i=[t for v,t in pairs if v=="20"]; v26i=[t for v,t in pairs if v=="26"]
print("INTERLEAVED s10 validation (5 alternating pairs, ns):")
print(f"  v20: {[f'{t/1e9:.2f}s' for t in v20i]} median {statistics.median(v20i)/1e9:.2f}s")
print(f"  v26: {[f'{t/1e9:.2f}s' for t in v26i]} median {statistics.median(v26i)/1e9:.2f}s")
print(f"  median ratio v26/v20 = {statistics.median(v26i)/statistics.median(v20i):.3f}")
print("measured per-row wall (ns), median of 3 (s100 v26 flagged: contention-polluted):")
per_row = {}
for v in ("20","26"):
    for t in ("s1","s10","s100"):
        m = med(f"{t}_v{v}")/rows[t]
        per_row[(v,t)] = m
        flag = "  <-- CONTENTION-POLLUTED (see runlog)" if (v,t)==("26","s100") else ""
        print(f"  v{v} {t}: {m:.1f} ns/row{flag}")
    # projection uses s10 (cleanest: s1 has startup-share, s100v26 polluted)
    pr = per_row[(v,"s10")]
    out_b = os.path.getsize(f"{S}/s10_v{v}_A.tsv")/rows["s10"]
    wall_s = 100_000_000 * pr / 1e9
    print(f"v{v} PROJECTION 1M items x 100 obs (100M rows), from s10 per-row:")
    print(f"  wall = 100M x {pr:.1f}ns = {wall_s:,.0f}s = {wall_s/3600:.2f}h")
    print(f"  ledger = 1M x 88B = {1_000_000*88/1e9:.3f} GB")
    print(f"  output = 100M x {out_b:.1f}B = {100_000_000*out_b/1e9:.2f} GB")
print("assumptions: linear extrapolation from s10 medians; arena allocator")
print("constant; single-threaded; no page-cache/GC effects; schema shared.")
print("RSS model: base_RSS(s1) + 88B/item + schema(static); schema not per-item.")
EOF
echo "COST DONE $(date -u +%FT%TZ)" | tee -a $LOG
