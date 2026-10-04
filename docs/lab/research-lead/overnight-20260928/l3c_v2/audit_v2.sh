#!/bin/sh
# audit_v2.sh -- anti-widening audit, PREREG_L3C_V2.md section 7.
# Shell + grep only. Exit 0 when every check passes.
# Usage: sh audit_v2.sh
set -u
D=$(dirname "$0")
F="$D/l3c_v2.zag"
fail=0

echo "=== A1: sig literals only inside fn main (expect total == in-main) ==="
for sg in 501 502 503 504 505 67 131 327; do
  tot=$(grep -cow "$sg" "$F")
  inm=$(sed -n '/^fn main/,$p' "$F" | grep -cow "$sg")
  echo "sig=$sg total=$tot in_main=$inm"
  if [ "$tot" -ne "$inm" ]; then echo "A1=FAIL sig=$sg"; fail=1; fi
done
if [ "$fail" -eq 0 ]; then echo "A1=PASS"; fi

echo "=== A2: op_label_edge call sites (expect 1 def + calls in build_chain with variable args) ==="
grep -n "op_label_edge" "$F"
ndef=$(grep -c "^fn op_label_edge" "$F")
ncall=$(grep -c "op_label_edge(W,e1,fi,op,fv)" "$F")
echo "defs=$ndef exact_variable_calls=$ncall"
if [ "$ndef" -eq 1 ] && [ "$ncall" -ge 1 ]; then
  echo "A2=PASS"
else
  echo "A2=FAIL"; fail=1
fi

echo "=== A3: interp uniformity (one edge path, recursive DISP targets) ==="
sed -n '/^fn interp/,/^}/p' "$F"
echo "(read: single select_edge path; recursion into edge targets; no domain literals)"

echo "=== A4: node/edge state writers (expect: op_* fns only) ==="
echo "--- set32 to node_addr ---"
grep -n "set32(W,node_addr" "$F" | grep -v "^.*fn op_" || true
grep -n "set32(W,node_addr" "$F"
echo "--- set32 to edge_addr ---"
grep -n "set32(W,edge_addr" "$F"
echo "(read: every node_addr/edge_addr set32 sits inside an op_* fn)"

echo "=== A5: no family-naming identifiers in protocol fns (expect zero matches before fn main) ==="
if sed -n '1,/^fn main/p' "$F" | grep -niE "fam_a|fam_b|fam_c|fam_d|fam_e|conj_fix|thresh_fix|nested_fix|ambig_fix|hist_fix|sig501|sig502|sig503|sig504|sig505"; then
  echo "A5=FAIL"; fail=1
else
  echo "A5=PASS (zero matches in protocol section; FAM_* emit labels live only in main's harness reporting)"
fi

echo "=== A6: no per-family branch on sig in protocol fns ==="
prot=$(sed -n '1,/^fn main/p' "$F" | grep -cow "501\|502\|503\|504\|505" || true)
echo "sig_literal_hits_before_main=$prot"
if [ "$prot" -eq 0 ]; then echo "A6=PASS"; else echo "A6=FAIL"; fail=1; fi

if [ "$fail" -eq 0 ]; then
  echo "AUDIT=PASS"
else
  echo "AUDIT=FAIL"
fi
exit "$fail"
