export PATH="$HOME/safebin"
D=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/scaling_cont
B=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/rebinding_hardening/hard_base.zag
# Expand workspace: 1024 -> 8192 nodes, 4096 -> 16384 edges.
# Layout: header 64 + 8192*40 (nodes) + 16384*16 (edges) + 128*32 (log)
#   nodes end: 64+327680 = 327744 (eoff base)
#   edges end: 327744+262144 = 589888 (loff base)
#   total WSZ: 589888+4096 = 593984
sed \
 -e 's/return 110656;/return 593984;/' \
 -e 's/return 1024;/return 8192;/' \
 -e 's/return 4096;/return 16384;/' \
 -e 's/return 41024+e\*16;/return 327744+e*16;/' \
 -e 's/return 106560+l\*32;/return 589888+l*32;/' \
 -e 's/while(i<110656)/while(i<593984)/' \
 -e 's/1024 nodes, 4096 edges/8192 nodes, 16384 edges/' \
 -e 's/1024/8192/g' \
 -e '664s/8192/1024/g' \
 -e '1232s/8192/1024/g' \
 -e 's/4096/16384/g' \
 $B > $D/sc_base_expanded.zag
echo "=== verify key lines ==="
grep -n "fn WSZ\|fn NN\|fn NE\|fn eoff\|fn loff" $D/sc_base_expanded.zag
grep -n "1024" $D/sc_base_expanded.zag | head
echo "=== fn boundaries in expanded base ==="
grep -n "^fn ev_teach\|^fn ev_teach_in\|^fn promote_graph\|^fn ev_query\|^fn main\|^fn t2_lu_first\|^fn t2_gather\|^fn decay" $D/sc_base_expanded.zag
wc -l $D/sc_base_expanded.zag