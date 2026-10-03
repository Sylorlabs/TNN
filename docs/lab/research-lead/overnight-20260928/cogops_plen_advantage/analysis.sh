#!/bin/sh
# analysis.sh -- kill-bar analysis for COGOPS-PLEN-ADVANTAGE (shell text
# processing of binary-emitted lines only; all research logic is in adv.zag).
export PATH="$HOME/safebin"
D="$HOME/workspace/tnn-rsi-plenadv/docs/lab/research-lead/overnight-20260928/cogops_plen_advantage"
G="$HOME/workspace/tnn-rsi-plenadv/docs/lab/research-lead/overnight-20260928/cogops_plen_granularity/gran_run1.txt"
cd "$D"
R=adv_run1.txt

echo "=== AH1: GEN-trajectory byte-match vs gran_run1.txt (rg 0,2; k 0..7; P1/P3/PA) ==="
# extract GEN blocks keyed rg,pair,arm from each file into temp files, cmp
TMPD=/tmp/ah1_$$; mkdir -p "$TMPD"
awk '/^PAIR /{split($3,a,"="); rg=a[2]; pair=$2; arm=$5}
     /^GEN /{print $0 > ("'"$TMPD"'/gen_" rg "_" pair "_" arm ".txt")}' "$G"
awk '/^PAIR /{split($3,a,"="); rg=a[2]; pair=$2; arm=$5}
     /^GEN /{print $0 > ("'"$TMPD"'/adv_" rg "_" pair "_" arm ".txt")}' "$R"
pass=0; failn=0
for rg in 0 2; do
  for k in 0 1 2 3 4 5 6 7; do
    for arm in P1 P3 PA; do
      if cmp -s "$TMPD/gen_${rg}_${k}_${arm}.txt" "$TMPD/adv_${rg}_${k}_${arm}.txt"; then
        pass=$((pass+1))
      else
        failn=$((failn+1)); echo "DIFF rg=$rg pair=$k arm=$arm"
      fi
    done
  done
done
echo "AH1 byte-match: $pass/48 (need 48/48)"
rm -rf "$TMPD"

echo ""
echo "=== cost table (cost = trials if adopted else 369), rg=2 ==="
awk '/^REVISE-RESULT/{
  for(i=1;i<=NF;i++){
    split($i,a,"="); if(a[1]=="pair")p=a[2]; if(a[1]=="rg")g=a[2];
    if(a[1]=="plenmode")m=a[2]; if(a[1]=="trials")t=a[2]; if(a[1]=="adopted")ad=a[2];
  }
  c=(ad==1)?t:369; key=g","p; cost[key","m]=c; adp[key","m]=ad;
}
END{
  print "pair: P0cost PAcost P1cost P3cost | PA-P3 PA-P0 P0-P3 | adopted(P0,PA,P1,P3)";
  for(p=0;p<16;p++){
    k="2,"p;
    c0=cost[k",5"]; ca=cost[k",4"]; c1=cost[k",1"]; c3=cost[k",3"];
    printf "p=%2d: %3d %3d %3d %3d | %+4d %+4d %+4d | %d%d%d%d\n", p,c0,ca,c1,c3, ca-c3, ca-c0, c0-c3, adp[k",5"],adp[k",4"],adp[k",1"],adp[k",3"];
  }
}' "$R"

echo ""
echo "=== AH2/AH3/AH4 counts, rg=2 ==="
awk '/^REVISE-RESULT/{
  for(i=1;i<=NF;i++){
    split($i,a,"="); if(a[1]=="pair")p=a[2]; if(a[1]=="rg")g=a[2];
    if(a[1]=="plenmode")m=a[2]; if(a[1]=="trials")t=a[2]; if(a[1]=="adopted")ad=a[2];
  }
  cost[g","p","m]=(ad==1)?t:369;
}
END{
  # AH2: fresh pairs 8..15
  nw=0; sw=0;
  for(p=8;p<16;p++){ d=cost["2,"p",4"]-cost["2,"p",3"]; if(d<=0)nw++; if(d<0)sw++; }
  print "AH2 fresh: PA<=P3 in "nw"/8, PA<P3 in "sw"/8 (need 8/8 and >=2/8)";
  # AH3: all 16, sign test (ties dropped)
  n=0; k=0;
  for(p=0;p<16;p++){ d=cost["2,"p",4"]-cost["2,"p",3"]; if(d<0){n++;k++;} else if(d>0){n++;} }
  print "AH3 sign test: n="n" non-tied, k="k" favor PA";
  # AH4: PA vs P0
  eq=0; paw=0; p0w=0;
  for(p=0;p<16;p++){ d=cost["2,"p",4"]-cost["2,"p",5"]; if(d==0)eq++; else if(d<0)paw++; else p0w++; }
  print "AH4 PA-vs-P0: equal "eq"/16, PA<P0 "paw"/16, PA>P0 "p0w"/16";
}' "$R"

echo ""
echo "=== AH5: mean cost per arm, rg=2; monotone P0<=PA<=P1<=P3 count ==="
awk '/^REVISE-RESULT/{
  for(i=1;i<=NF;i++){
    split($i,a,"="); if(a[1]=="pair")p=a[2]; if(a[1]=="rg")g=a[2];
    if(a[1]=="plenmode")m=a[2]; if(a[1]=="trials")t=a[2]; if(a[1]=="adopted")ad=a[2];
  }
  if(g==2){ cost[p","m]=(ad==1)?t:369; }
}
END{
  for(m in mm){} # noop
  s0=0;sa=0;s1=0;s3=0; mono=0;
  for(p=0;p<16;p++){
    c0=cost[p",5"]; ca=cost[p",4"]; c1=cost[p",1"]; c3=cost[p",3"];
    s0+=c0; sa+=ca; s1+=c1; s3+=c3;
    if(c0<=ca && ca<=c1 && c1<=c3)mono++;
  }
  printf "mean cost: P0=%.1f PA=%.1f P1=%.1f P3=%.1f\n", s0/16, sa/16, s1/16, s3/16;
  print "monotone P0<=PA<=P1<=P3: "mono"/16";
}' "$R"

echo ""
echo "=== AH6: QUALITY (bestlen/inv/adj per arm), rg=2 ==="
grep -h "^QUALITY" "$R" | awk '$2=="rg=2" || $0 ~ /rg=2 /'
echo ""
echo "mean inv per arm (rg=2):"
grep -h "^QUALITY" "$R" | awk '{for(i=1;i<=NF;i++){split($i,a,"="); if(a[1]=="rg")g=a[2]; if(a[1]=="plenmode")m=a[2]; if(a[1]=="inv")v=a[2];} if(g==2){s[m]+=v; n[m]++}} END{for(m in s)printf "plenmode %s: mean inv %.1f\n", m, s[m]/n[m]}'
echo "mean bestlen per arm (rg=2):"
grep -h "^QUALITY" "$R" | awk '{for(i=1;i<=NF;i++){split($i,a,"="); if(a[1]=="rg")g=a[2]; if(a[1]=="plenmode")m=a[2]; if(a[1]=="bestlen")v=a[2];} if(g==2){s[m]+=v; n[m]++}} END{for(m in s)printf "plenmode %s: mean bestlen %.1f\n", m, s[m]/n[m]}'

echo ""
echo "=== early bestraw at g=5 (rg=2, per pair, P0/PA/P3) ==="
awk '/^PAIR /{split($3,a,"="); rg=a[2]; pair=$2; arm=$5}
     /^GEN /{split($2,b,"="); g=b[2]; if(rg==2 && g==5){split($4,c,"="); print "pair="pair" arm="arm" g5bestraw="c[2]}}' "$R"

echo ""
echo "=== SEEDCUR fresh pairs (rg=2) ==="
grep -h "^SEEDCUR" "$R" | awk '{for(i=1;i<=NF;i++){split($i,a,"="); if(a[1]=="pair")p=a[2]; if(a[1]=="rg")g=a[2]; if(a[1]=="cur")c=a[2];} if(g==2 && p>=8)print "pair="p" cur="c}'
