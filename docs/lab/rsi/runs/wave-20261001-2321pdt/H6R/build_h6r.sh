#!/bin/sh
# build_h6r.sh -- mechanical rebuild of the H6R experiment binary.
# Pure shell. No Python. Steps:
#   1. copy the frozen tnn2.zag (hash-verified, never modified) into the lane dir
#   2. apply the substrate prereg's hook insertions (exact seds from build_proto.sh)
#   3. append the PKG block, extracted MECHANICALLY from the amended frozen
#      prereg at commit a11dde4b9 (sed between PKG-BEGIN and PKG-END; includes
#      Amendment 1's one-line deletion, as verified)
#   4. byte-compare the rebuilt substrate portion against the committed
#      prototype's substrate portion (dev harness stripped, main normalized)
#   5. set main to h6r_main and append this lane's experiment checks
#   6. compile with the pinned znc
set -e
export PATH="$HOME/safebin"
cd "$HOME/workspace/tnn-rsi"
LANE=docs/lab/rsi/runs/wave-20261001-2321pdt/H6R
FROZEN=docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
sha256sum "$FROZEN" | grep -q "^a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd " || { echo "FROZEN HASH MISMATCH"; exit 1; }
echo "frozen hash OK"
cp "$FROZEN" "$LANE/h6r_proto.zag"
cd "$LANE"
# --- hook insertions (adoption diff, prereg section 4; exact copies) ---
sed -i '145s/bid(W,n)/lbid(W,n)/' h6r_proto.zag
sed -i '259s/bid(W,n)/lbid(W,n)/' h6r_proto.zag
sed -i 's|let b:i32=bid(W,cand);|let b:i32=lbid(W,cand); // SUBSTRATE-HOOK C3|' h6r_proto.zag
sed -i 's|let b2:i32=bid(W,c2);|let b2:i32=lbid(W,c2); // SUBSTRATE-HOOK C3|' h6r_proto.zag
sed -i 's|link_edge(W,n,7,n,0); ref_prot(W,n);|link_edge(W,n,7,n,0); ref_prot(W,n);\n      ls_bump(W,n,1); // SUBSTRATE-HOOK C1|' h6r_proto.zag
sed -i 's|^      log_ev(W,4,s,r,o,1,0,0); return 1;$|      log_ev(W,4,s,r,o,1,0,0); lb_run(W); return 1; // SUBSTRATE-HOOK A|' h6r_proto.zag
sed -i 's|if(nn>=0){link_edge(W,nn,4,n,0);}|if(nn>=0){link_edge(W,nn,4,n,0);}\n    lt_fire(W,n,nn); ls_bump(W,n,-1); // SUBSTRATE-HOOK B C2|' h6r_proto.zag
sed -i 's|log_ev(W,4,s,r,o,0,0,0); return 0;|log_ev(W,4,s,r,o,0,0,0); lb_run(W); return 0; // SUBSTRATE-HOOK A|' h6r_proto.zag
sed -i 's|ev_teach_in(W,s,r,o); log_ev(W,4,s,r,o,1,0,0); return 1;|ev_teach_in(W,s,r,o); log_ev(W,4,s,r,o,1,0,0); lb_run(W); return 1; // SUBSTRATE-HOOK A|' h6r_proto.zag
# --- mechanical package extraction from the amended frozen prereg ---
git -C "$HOME/workspace/tnn-rsi" show a11dde4b9:docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3-SUBSTRATE/SUBSTRATE_PREREG.md | sed -n '/\/\/ PKG-BEGIN/,/\/\/ PKG-END/p' > pkg_block.zag
wc -l pkg_block.zag
cat pkg_block.zag >> h6r_proto.zag
# --- cross-check: rebuilt substrate portion == committed prototype's ---
git -C "$HOME/workspace/tnn-rsi" show a11dde4b9:docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3-SUBSTRATE/substrate_proto.zag | sed -n '1,/dev verification checks (harness only/p' | sed '$d' | sed 's|fn main()i32 { return proto_main(); } // SUBSTRATE-HOOK: dev harness entry|fn main()i32 { return MAIN(); }|' > /tmp/h6r_ref_n.zag
sed 's/return run_all()/return MAIN()/' h6r_proto.zag > /tmp/h6r_mine_n.zag
cmp /tmp/h6r_ref_n.zag /tmp/h6r_mine_n.zag || { echo "SUBSTRATE MISMATCH VS COMMITTED PROTOTYPE"; exit 1; }
echo "substrate byte-identical to committed prototype (modulo dev harness)"
# --- lane harness entry + experiment checks ---
sed -i 's|fn main()i32 { return run_all(); }|fn main()i32 { return h6r_main(); } // H6R: experiment harness entry|' h6r_proto.zag
cat h6r_checks.zag >> h6r_proto.zag
wc -l h6r_proto.zag
"$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1" h6r_proto.zag -o h6r_proto 2>&1 | grep -vi "A0102\|zagd unavailable\|note:\|hint:\|-->" | head -5
ls -la h6r_proto
