export PATH="$HOME/safebin"
cd ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/index_harden
B=../rebinding_hardening/hard_base.zag
# Assembly: base minus promote_graph (533-543), minus base ev_query
# (813-835), minus base main (1357); then the hardened index patch,
# then the corruption test driver.
sed -n '1,532p' $B > ih_full.zag
sed -n '544,812p' $B >> ih_full.zag
sed -n '836,1356p' $B >> ih_full.zag
sed -n '1358,1591p' $B >> ih_full.zag
cat ih_patch.zag >> ih_full.zag
cat ih_driver.zag >> ih_full.zag
wc -l ih_full.zag
echo "=== main count (expect 1) ==="
grep -c "^fn main" ih_full.zag
echo "=== ev_query count (expect 1) ==="
grep -c "^fn ev_query" ih_full.zag
echo "=== promote_graph count (expect 1) ==="
grep -c "^fn promote_graph" ih_full.zag
echo "=== rb_chain_plen count (expect 1) ==="
grep -c "^fn rb_chain_plen" ih_full.zag
echo "=== rebind_try_idx count (expect 1) ==="
grep -c "^fn rebind_try_idx" ih_full.zag
echo "=== idx_walk_bucket count (expect 1) ==="
grep -c "^fn idx_walk_bucket" ih_full.zag
