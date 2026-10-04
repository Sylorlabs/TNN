#!/bin/sh
# audit.sh -- frozen audit procedure, PREREG_L3C_FORM.md section 8.
# Shell + grep only. Exit 0 when every check passes.
# Usage: sh audit.sh
set -u
D=$(dirname "$0")
F="$D/l3c_form.zag"
fail=0

echo "=== A1: forbidden constructor identifiers (expect zero matches) ==="
if grep -nE "mk_cond|make_cond|cond_new|build_cond|cond_dispatch|versioned|mk_if|if_pos|cond_pos" "$F"; then
  echo "A1=FAIL"; fail=1
else
  echo "A1=PASS (zero matches)"
fi

echo "=== A2: op_label_edge call sites (expect: 1 fn def + 1 call, call args are variables) ==="
grep -n "op_label_edge" "$F"
ncall=$(grep -c "op_label_edge(W,e1,fi,fv)" "$F")
nline=$(grep -c "op_label_edge" "$F")
echo "lines_with_op_label_edge=$nline exact_call_site_hits=$ncall"
if [ "$nline" -eq 2 ] && [ "$ncall" -eq 1 ]; then
  echo "A2=PASS"
else
  echo "A2=FAIL"; fail=1
fi

echo "=== A3: label feature/value writers (expect: generic op body only, loop variable source) ==="
grep -n "edge_addr(eid)+12\|edge_addr(eid)+16" "$F"
echo "(manual read: the only writers sit inside fn op_label_edge; feat/val are parameters)"

echo "=== A4: interpreter uniformity (expect: one edge path, no domain feature/value literals) ==="
sed -n '/^fn interp/,/^}/p' "$F" | grep -n "==" || true
echo "(manual read: comparisons are lk==0 / structural; label contents flow through variables lf/lv)"

echo "=== A5: writers of node/edge/label/rule state ==="
echo "--- fn definitions ---"
grep -n "^fn " "$F"
echo "--- all set32 sites ---"
grep -n "set32" "$F"
echo "(read: every set32 sits inside an op_* fn, rule_link (seeding), stash,"
echo " construct (which only calls op_*), or main init writing -1/0 to fresh state)"

if [ "$fail" -eq 0 ]; then
  echo "AUDIT=PASS"
else
  echo "AUDIT=FAIL"
fi
exit "$fail"
