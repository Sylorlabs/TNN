export PATH="$HOME/safebin"
cd ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/scaling_index
B=../rebinding_hardening/hard_base.zag
# Assembly: base minus promote_graph (533-543), minus base ev_query
# (813-835), minus base main (1357); then the index patch, then the driver.
sed -n '1,532p' $B > si_full.zag
sed -n '544,812p' $B >> si_full.zag
sed -n '836,1356p' $B >> si_full.zag
sed -n '1358,1591p' $B >> si_full.zag
cat si_patch.zag >> si_full.zag
cat si_driver.zag >> si_full.zag
wc -l si_full.zag
echo "=== main count (expect 1) ==="
grep -c "^fn main" si_full.zag
echo "=== ev_query count (expect 1) ==="
grep -c "^fn ev_query" si_full.zag
echo "=== promote_graph count (expect 1) ==="
grep -c "^fn promote_graph" si_full.zag
echo "=== rb_chain_plen count (expect 1) ==="
grep -c "^fn rb_chain_plen" si_full.zag
