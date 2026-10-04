export PATH="$HOME/safebin"
D=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/scaling_cont
B=$D/sc_base_expanded.zag
# Assembly: expanded base minus ev_teach (297-309), ev_teach_in (310-314),
# t2_lu_first (419-426), t2_gather (442-472), promote_graph (533-543),
# ev_query (813-835), main (1357); then patch, then driver.
sed -n '1,296p' $B > $D/sc_full.zag
sed -n '315,418p' $B >> $D/sc_full.zag
sed -n '427,441p' $B >> $D/sc_full.zag
sed -n '473,532p' $B >> $D/sc_full.zag
sed -n '544,812p' $B >> $D/sc_full.zag
sed -n '836,1356p' $B >> $D/sc_full.zag
sed -n '1358,1591p' $B >> $D/sc_full.zag
cat $D/sc_patch.zag >> $D/sc_full.zag
cat $D/sc_driver.zag >> $D/sc_full.zag
wc -l $D/sc_full.zag
echo "=== fn counts (expect 1 each) ==="
for f in "^fn main" "^fn ev_query" "^fn promote_graph" "^fn ev_teach" "^fn ev_teach_in" "^fn t2_gather" "^fn t2_lu_first" "^fn rb_chain_plen" "^fn rebind_try_idx" "^fn rebind_try_lin" "^fn idx_mode_set" "^fn fidx_add" "^fn mtf_win"; do
  printf "%s: " "$f"; grep -c "$f" $D/sc_full.zag
done
echo "=== compile ==="
ZNC=~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
if [ ! -x "$ZNC" ]; then ZNC=$(which znc); fi
echo "znc=$ZNC"
cd $D && "$ZNC" sc_full.zag -o sc_bin > compile_err.txt 2>&1
echo "exit=$?"
head -20 compile_err.txt
ls -la sc_bin 2>/dev/null