export PATH="$HOME/safebin"
cd ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/rebinding_hardening
# Assemble hard_full.zag:
# - hard_base.zag lines 1-812 (before ev_query)
# - hard_base.zag lines 836-1356 (after ev_query, before main)
# - hard_base.zag lines 1358-1591 (ACT code after main)
# - hard_patch.zag (rebinding mechanism with new ev_query)
# - hard_driver.zag (hardening worlds, with main)
sed -n '1,812p' hard_base.zag > hard_full.zag
sed -n '836,1356p' hard_base.zag >> hard_full.zag
sed -n '1358,1591p' hard_base.zag >> hard_full.zag
cat hard_patch.zag >> hard_full.zag
cat hard_driver.zag >> hard_full.zag
wc -l hard_full.zag
echo "=== verify single main ==="
grep -c "^fn main" hard_full.zag
echo "=== verify single ev_query ==="
grep -c "^fn ev_query" hard_full.zag
