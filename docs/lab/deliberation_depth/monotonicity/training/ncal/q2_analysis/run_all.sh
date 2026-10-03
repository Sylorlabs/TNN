#!/bin/bash
# Q2 head-to-head: variants x batteries x reruns, SHA-logged
cd ~/workspace/q2_crew/work
: > SHA_LOG.tsv
run_one() { # variant battery rep
  local v=$1 b=$2 r=$3
  local out="results/${v}_${b}_${r}.tsv"
  ./q2_${v}_bin ${b}.tsv $out || { echo "FAIL $v $b $r rc=$?"; return 1; }
  local sha=$(sha256sum $out | cut -d' ' -f1)
  echo -e "${v}\t${b}\t${r}\t${sha}\t${out}" >> SHA_LOG.tsv
}
for v in m11 floor u1 u2 g eb ind; do
  for b in trap_t1 trap_t3 necc_input; do
    for r in A B C; do run_one $v $b $r; done
  done
done
# m9 counterfactual for T2 (nec.zag = v0)
for r in A B C; do
  ./nec_bin necc_input.tsv results/m9_necc_input_${r}.tsv || echo "FAIL m9 $r"
  sha=$(sha256sum results/m9_necc_input_${r}.tsv | cut -d' ' -f1)
  echo -e "m9\tnecc_input\t${r}\t${sha}\tresults/m9_necc_input_${r}.tsv" >> SHA_LOG.tsv
done
echo "=== determinism check (A/B/C must match per variant×battery) ==="
python3 - <<'PYEOF'
import collections
groups = collections.defaultdict(set)
for line in open("SHA_LOG.tsv"):
    v,b,r,sha,out = line.rstrip("\n").split("\t")
    groups[(v,b)].add(sha)
bad = {k:v for k,v in groups.items() if len(v)>1}
print("groups:", len(groups), "non-deterministic:", len(bad))
for k,v in bad.items(): print("  BAD", k, v)
PYEOF
wc -l SHA_LOG.tsv
