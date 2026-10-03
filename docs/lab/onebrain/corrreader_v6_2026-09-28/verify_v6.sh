#!/bin/bash
# verify_v6.sh — v6 operative-utterance understanding end-to-end verification.
# Protocol (mirrors the v5 VERIFICATION.md protocol):
#   v7: 8 modes x 3 reruns, byte-identical; score vs expected_bid.
#   v8: 5 modes x 3 reruns, byte-identical; score vs expected_bid.
#   v5 comparison: same modes/sets, byte-compare outputs (all modes except
#     nov4 must be byte-identical v5-vs-v6; nov4 judged by absolute bars).
#   kill scaffolds: a1b/a1d/a2b/a2c must match v4-control winners (bid 19).
set -u
HERE=~/workspace/onebrain_corrreader
BLD=$HERE/build
EV=$HERE/evidence
V5=~/workspace/onebrain_corrprotect/build/ob_v5
V4=~/workspace/onebrain_corrprotect/build/ob_v4ctl
mkdir -p $EV
pass=0; fail=0
note() { echo "$1" | tee -a $EV/verify.log; }
check() { # check <name> <cond: 0=pass>
  if [ "$2" = "0" ]; then note "PASS $1"; pass=$((pass+1));
  else note "FAIL $1"; fail=$((fail+1)); fi
}
score() { # score <outfile> <tsv> -> prints n_correct
  python3 - "$1" "$2" <<'EOF'
import sys
out, tsv = sys.argv[1], sys.argv[2]
exp = {}
with open(tsv) as f:
    head = f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) >= 3 and p[0]:
            exp[p[0]] = p[2]
got = {}
for line in open(out, errors="replace"):
    if line.startswith("VERDICT"):
        parts = line.split()
        i = [x.split("=",1)[1] for x in parts if x.startswith("id=")][0]
        w = [x.split("=",1)[1] for x in parts if x.startswith("winner=")][0]
        got[i] = w
n = c = 0
miss = []
for i, e in exp.items():
    n += 1
    if got.get(i) == e: c += 1
    else: miss.append((i, e, got.get(i)))
print(f"{c}/{n}")
for m in miss: print("  MISS", m)
EOF
}
: > $EV/verify.log
note "== v6 e2e verification $(date -u +%FT%TZ) =="
note "v6 binary: $(sha256sum $BLD/ob_v6u | cut -d' ' -f1)"
note "v6 source: $(sha256sum $BLD/onebrain_v6_utterance.zag | cut -d' ' -f1)"
note "utterance.zag: $(sha256sum $BLD/utterance.zag | cut -d' ' -f1)"
for spec in "v7 single onebrain nov4 nG nov4nG ablate min poison" "v8 single onebrain nov4 nG nov4nG"; do
  set -- $spec; tsv=$1; shift
  for mode in "$@"; do
    outs=""
    for r in 1 2 3; do
      o=$EV/v6_${tsv}_${mode}_r${r}.out; e=$EV/v6_${tsv}_${mode}_r${r}.err
      (cd $BLD && ./ob_v6u $mode $tsv.tsv > $o 2> $e)
      outs="$outs $o"
      [ -s "$e" ] && note "WARN stderr non-empty: $e"
    done
    s1=$(sha256sum $EV/v6_${tsv}_${mode}_r1.out | cut -d' ' -f1)
    s2=$(sha256sum $EV/v6_${tsv}_${mode}_r2.out | cut -d' ' -f1)
    s3=$(sha256sum $EV/v6_${tsv}_${mode}_r3.out | cut -d' ' -f1)
    if [ "$s1" = "$s2" ] && [ "$s2" = "$s3" ]; then check "$tsv/$mode 3x byte-identical" 0;
    else check "$tsv/$mode 3x byte-identical" 1; fi
    # v5 comparison output (single run; v5 determinism already established)
    vo=$EV/v5_${tsv}_${mode}.out
    (cd ~/workspace/onebrain_corrprotect/build && ./ob_v5 $mode $BLD/$tsv.tsv > $vo 2>/dev/null)
    if [ "$mode" = "nov4" ]; then
      sc=$(score $EV/v6_${tsv}_${mode}_r1.out $BLD/$tsv.tsv | head -1)
      note "SCORE v6 $tsv/$mode = $sc"
    else
      if cmp -s $EV/v6_${tsv}_${mode}_r1.out $vo; then check "$tsv/$mode v6==v5 byte-identical" 0;
      else check "$tsv/$mode v6==v5 byte-identical" 1; fi
      sc=$(score $EV/v6_${tsv}_${mode}_r1.out $BLD/$tsv.tsv | head -1)
      note "SCORE v6 $tsv/$mode = $sc"
    fi
  done
done
# kill scaffolds + genuine-correction controls through v6 nov4 vs v4 control
grep -P "^(a1b|a1d|a2b|a2c|a3|a4)\t" ~/workspace/onebrain_corrprotect/redteam/attack_items.tsv > $EV/kill.tsv
sed -i '1i id\tquery\texpected_bid\treadings\trationale' $EV/kill.tsv
(cd $BLD && ./ob_v6u nov4 $EV/kill.tsv > $EV/v6_kill.out 2>/dev/null)
(cd ~/workspace/onebrain_corrprotect/build && ./ob_v4ctl nov4 $EV/kill.tsv > $EV/v4_kill.out 2>/dev/null)
note "--- kill scaffold winners (v6 nov4 vs v4-control nov4) ---"
python3 - <<'EOF' | tee -a ~/workspace/onebrain_corrreader/evidence/verify.log
def winners(p):
    d={}
    for line in open(p, errors="replace"):
        if line.startswith("VERDICT"):
            ps=line.split()
            i=[x.split("=",1)[1] for x in ps if x.startswith("id=")][0]
            w=[x.split("=",1)[1] for x in ps if x.startswith("winner=")][0]
            d[i]=w
    return d
v6=winners("/home/hatch/workspace/onebrain_corrreader/evidence/v6_kill.out")
v4=winners("/home/hatch/workspace/onebrain_corrreader/evidence/v4_kill.out")
for i in ["a1b","a1d","a2b","a2c","a3","a4"]:
    flag = "OK " if v6.get(i)==v4.get(i) else "DIFF"
    print(f"{flag} {i}: v6={v6.get(i)} v4ctl={v4.get(i)}")
EOF
note "== totals: pass=$pass fail=$fail =="
