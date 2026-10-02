#!/bin/sh
# build_proto.sh -- deterministic rebuild of the TNN3-SUBSTRATE dev prototype.
# Pure shell. No Python. Steps:
#   1. copy the frozen tnn2.zag (never modified) into the lane dir
#   2. apply the prereg-specified hook insertions (marked SUBSTRATE-HOOK)
#   3. append the package section, extracted MECHANICALLY from the frozen
#      SUBSTRATE_PREREG.md (sed between PKG-BEGIN and PKG-END; no retyping)
#   4. append the dev verification checks
#   5. compile with the pinned znc
set -e
export PATH="$HOME/safebin"
LANE=docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3-SUBSTRATE
cd "$HOME/workspace/tnn-rsi"
FROZEN=docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
sha256sum "$FROZEN"
cp "$FROZEN" "$LANE/substrate_proto.zag"
cd "$LANE"
# --- hook insertions (adoption diff, prereg section 4) ---
sed -i '145s/bid(W,n)/lbid(W,n)/' substrate_proto.zag
sed -i '259s/bid(W,n)/lbid(W,n)/' substrate_proto.zag
sed -i 's|let b:i32=bid(W,cand);|let b:i32=lbid(W,cand); // SUBSTRATE-HOOK C3|' substrate_proto.zag
sed -i 's|let b2:i32=bid(W,c2);|let b2:i32=lbid(W,c2); // SUBSTRATE-HOOK C3|' substrate_proto.zag
# confirm branch: standing +1, then run pending builds before returning
sed -i 's|link_edge(W,n,7,n,0); ref_prot(W,n);|link_edge(W,n,7,n,0); ref_prot(W,n);\n      ls_bump(W,n,1); // SUBSTRATE-HOOK C1|' substrate_proto.zag
sed -i 's|^      log_ev(W,4,s,r,o,1,0,0); return 1;$|      log_ev(W,4,s,r,o,1,0,0); lb_run(W); return 1; // SUBSTRATE-HOOK A|' substrate_proto.zag
# contradict branch: generic trigger + standing -1, then run pending builds
sed -i 's|if(nn>=0){link_edge(W,nn,4,n,0);}|if(nn>=0){link_edge(W,nn,4,n,0);}\n    lt_fire(W,n,nn); ls_bump(W,n,-1); // SUBSTRATE-HOOK B C2|' substrate_proto.zag
sed -i 's|log_ev(W,4,s,r,o,0,0,0); return 0;|log_ev(W,4,s,r,o,0,0,0); lb_run(W); return 0; // SUBSTRATE-HOOK A|' substrate_proto.zag
# teach path: run pending builds before returning
sed -i 's|ev_teach_in(W,s,r,o); log_ev(W,4,s,r,o,1,0,0); return 1;|ev_teach_in(W,s,r,o); log_ev(W,4,s,r,o,1,0,0); lb_run(W); return 1; // SUBSTRATE-HOOK A|' substrate_proto.zag
# dev harness entry
sed -i 's|fn main()i32 { return run_all(); }|fn main()i32 { return proto_main(); } // SUBSTRATE-HOOK: dev harness entry|' substrate_proto.zag
# --- mechanical package extraction from the frozen prereg ---
sed -n '/\/\/ PKG-BEGIN/,/\/\/ PKG-END/p' SUBSTRATE_PREREG.md > pkg_extract.zag
wc -l pkg_extract.zag
# --- append package + dev checks ---
cat pkg_extract.zag dev_checks.zag >> substrate_proto.zag
wc -l substrate_proto.zag
grep -c "SUBSTRATE-HOOK" substrate_proto.zag
# --- compile ---
"$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1" substrate_proto.zag -o substrate_proto 2>&1 | grep -vi "A0102\|zagd unavailable\|note:\|hint:\|-->" | head -5
ls -la substrate_proto
