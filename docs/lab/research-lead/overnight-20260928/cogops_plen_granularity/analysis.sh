#!/bin/sh
# analysis.sh -- kill-bar analysis for COGOPS-PLEN-GRANULARITY (shell text
# processing of binary-emitted lines only; all research logic is in gran.zag).
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/cogops_plen_granularity"
cd "$D"
R=gran_run1.txt

echo "=== GEN-trajectory divergence: P1 vs P3, PA vs P3 (per rg, pair) ==="
awk '
/^PAIR / {rg=$3; sub(/rg=/,"",rg); pair=$2; arm=$5}
/^GEN / {key=rg "," pair "," arm; gen[key]=gen[key] $0 "\n"}
END {
  for (r=0; r<3; r++) {
    for (p=0; p<8; p++) {
      k1=r "," p ",P1"; k3=r "," p ",P3"; ka=r "," p ",PA";
      d13=(gen[k1]==gen[k3]) ? "SAME" : "DIFF";
      da3=(gen[ka]==gen[k3]) ? "SAME" : "DIFF";
      print "rg=" r " pair=" p " P1vsP3=" d13 " PAvsP3=" da3
    }
  }
}' "$R"

echo ""
echo "=== FLIP table (flips/comps/plenend per rg, pair, arm) ==="
grep -h "^FLIP" "$R"

echo ""
echo "=== REVISE-RESULT table ==="
grep -h "^REVISE-RESULT" "$R"

echo ""
echo "=== SEEDCUR (cur per rg, pair) ==="
grep -h "^SEEDCUR" "$R" | sort -t= -k2,2n -k4,4n | uniq

echo ""
echo "=== PLEN-ADJ count ==="
grep -c "PLEN-ADJ" "$R"
