#!/bin/bash
# KPROD shakedown: replay (byte-compare vs run1) + kb_tv/kb_prior differential
# + determinism. Usage: run2.sh <outdir>
# Zero RNG. All inputs throwaway (never battery material).
set -u
R="$1"
KP=~/workspace/tnn-lab/knowledge/web_guides/live_ingest/kprod
BIN=$KP/bin/instrument_kprod
S=$KP/shake/inputs
G=$KP/shake/guides
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
BF1BLD=$KP/shake/bf1build/webg_bf1_fresh

pass=0; fail=0
step(){ # step <outbase> <expected-rc> -- cmd...
  local out="$1"; local exprc="$2"; shift 2
  "$@" >"$out.txt" 2>"$out.txt.err"; local rc=$?
  echo "$rc" >"$out.txt.rc"
  if [ "$rc" != "$exprc" ]; then fail=$((fail+1)); echo "RC-MISMATCH $out: got $rc want $exprc"
  else pass=$((pass+1)); fi
}

mkdir -p "$R/k" "$R/n" "$R/k7"
[ -x "$BF1BLD" ] || $ZNC "$KP/shake/bf1build/webg_bf1.zag" -o "$BF1BLD" 2>/dev/null
BF1=$BF1BLD

### ---- Part 1: replay of the run1 sequence ----
step "$R/teach-k" 0 $BIN teach "$G" "$R/k"
step "$R/teach-n" 0 $BIN teach "$G" "$R/n"
step "$R/teach-k7" 0 $BIN teach "$G" "$R/k7"
step "$R/kbcommit-A" 0 $BIN kbcommit "$S/claimsA.txt" "$R/k"
step "$R/kbcommit-B" 0 $BIN kbcommit "$S/claimsB.txt" "$R/k"
cp "$R/k/knowledge.txt" "$R/knowledge-after-AB.txt"
step "$R/kbcommit-pipe" 3 $BIN kbcommit "$S/claims_pipe.txt" "$R/k"
step "$R/kbcommit-short" 3 $BIN kbcommit "$S/claims_short.txt" "$R/k"
cp "$R/k/knowledge.txt" "$R/knowledge-after-reject.txt"
Q=$($BIN query "$R/k" "$S/need.txt" | grep '^QUERY|' | head -1 | cut -d'|' -f2-)
V(){ $BIN verdict "$1" "$S/need.txt" "$2" FACT "$Q"; }
step "$R/verdict-agree" 0 V "$R/k" "$S/pages_agree.txt"
step "$R/verdict-contra" 0 V "$R/k" "$S/pages_contra.txt"
step "$R/verdict-novel-N" 0 V "$R/n" "$S/pages_novel.txt"
step "$R/verdict-novel-K" 0 V "$R/k" "$S/pages_novel.txt"
cp "$R/k/pending.txt" "$R/pending-after-P1.txt"
step "$R/verdict-novel-K-dedup" 0 V "$R/k" "$S/pages_novel.txt"
cp "$R/k/pending.txt" "$R/pending-after-dedup.txt"
step "$R/verdict-novel2-K" 0 V "$R/k" "$S/pages_novel2.txt"
cp "$R/k/pending.txt" "$R/pending-after-P2.txt"
# N-arm frozen identity (kprod vs fresh bf1, same kprod-taught n dir)
step "$R/bf1-novel" 0 $BF1 verdict "$R/n" "$S/need.txt" "$S/pages_novel.txt" FACT "$Q"
step "$R/kprod-novel-N" 0 V "$R/n" "$S/pages_novel.txt"
step "$R/bf1-agree-N" 0 $BF1 verdict "$R/n" "$S/need.txt" "$S/pages_agree.txt" FACT "$Q"
step "$R/kprod-agree-N" 0 V "$R/n" "$S/pages_agree.txt"
step "$R/bf1-single-N" 0 $BF1 verdict "$R/n" "$S/need.txt" "$S/pages_single.txt" FACT "$Q"
step "$R/kprod-single-N" 0 V "$R/n" "$S/pages_single.txt"
# kbtest lifecycle
step "$R/kbtest-true" 0 $BIN kbtest "$R/k" 1 true
cp "$R/k/knowledge.txt" "$R/knowledge-after-promote.txt"
cp "$R/k/pending.txt" "$R/pending-after-promote.txt"
step "$R/verdict-prom-paraphrase" 0 V "$R/k" "$S/pages_prom.txt"
step "$R/kbtest-false" 0 $BIN kbtest "$R/k" 2 false
cp "$R/k/resolved.txt" "$R/resolved-after-false.txt"
cp "$R/k/pending.txt" "$R/pending-after-false.txt"
step "$R/verdict-reingest-resolved" 0 V "$R/k" "$S/pages_novel2.txt"
step "$R/kbtest-badpseq" 3 $BIN kbtest "$R/k" 99 true
step "$R/verdict-P3" 0 V "$R/k" "$S/pages_P3.txt"
step "$R/verdict-P4" 0 V "$R/k" "$S/pages_P4.txt"
cp "$R/k/pending.txt" "$R/pending-P3P4.txt"
step "$R/kbtest-badverdict" 3 $BIN kbtest "$R/k" 1 maybe
cp "$R/k/pending.txt" "$R/pending-after-badverdict.txt"
# kbcommit auto-resolve
step "$R/kbcommit-contra3" 0 $BIN kbcommit "$S/contra3.txt" "$R/k"
cp "$R/k/pending.txt" "$R/pending-after-autofalse.txt"
cp "$R/k/resolved.txt" "$R/resolved-after-autofalse.txt"
step "$R/kbcommit-agree4" 0 $BIN kbcommit "$S/agree4.txt" "$R/k"
cp "$R/k/pending.txt" "$R/pending-after-autopromote.txt"
cp "$R/k/knowledge.txt" "$R/knowledge-final.txt"
cp "$R/k/resolved.txt" "$R/resolved-final.txt"
# k7: resolved-false precedence (knowledge AGREE must win)
step "$R/k7-kbcommit-U" 0 $BIN kbcommit "$S/claimsU.txt" "$R/k7"
step "$R/k7-verdict-R" 0 V "$R/k7" "$S/pages_agree.txt"
step "$R/k7-kbtest-false" 0 $BIN kbtest "$R/k7" 1 false
step "$R/k7-kbcommit-C1" 0 $BIN kbcommit "$S/claimsC1.txt" "$R/k7"
step "$R/k7-verdict-Cstar" 0 V "$R/k7" "$S/pages_Cstar.txt"
cp "$R/k7/resolved.txt" "$R/k7-resolved.txt"
cp "$R/k7/knowledge.txt" "$R/k7-knowledge.txt"
cp "$R/k/installed.txt" "$R/installed-k.txt"

### ---- Part 2: kb_tv vs kb_prior differential (20 throwaway pairs) ----
DP=$R/diffpairs; mkdir -p "$DP"
DUMMY="Midnight badgers quietly solve complex differential equations."
# pairs: id|S|C|expected-class
cat > "$DP/pairs.txt" <<'EOF'
p01|The amber lighthouse flashes every 30 seconds at night.|Every 30 seconds the amber lighthouse flashes at night.|AGREE
p02|Copper wires conduct electricity through 8 circuits.|Through 8 circuits copper wires conduct electricity.|AGREE
p03|The old mill grinds 45 sacks of flour daily.|Daily the old mill grinds 45 sacks of flour.|AGREE
p04|Brass bells ring across the valley 12 times on sundays.|On sundays brass bells ring across the valley 12 times.|AGREE
p05|The river ferry carries 120 passengers across the wide channel.|Across the wide channel the river ferry carries 120 passengers.|AGREE
p06|The amber lighthouse flashes every 31 seconds at night.|The amber lighthouse flashes every 30 seconds at night.|CONTRADICT
p07|Copper wires conduct electricity through 19 circuits.|Copper wires conduct electricity through 18 circuits.|CONTRADICT
p08|The old mill grinds 46 sacks of flour daily.|The old mill grinds 45 sacks of flour daily.|CONTRADICT
p09|Brass bells ring across the valley 13 times on sundays.|Brass bells ring across the valley 12 times on sundays.|CONTRADICT
p10|The river ferry carries 121 passengers across the wide channel.|The river ferry carries 120 passengers across the wide channel.|CONTRADICT
p11|Penguins waddle across the frozen southern ice.|The amber lighthouse flashes every 30 seconds at night.|UNKNOWN
p12|Volcanoes erupt with molten lava and ash.|Copper wires conduct electricity through 8 circuits.|UNKNOWN
p13|The clockmaker repairs antique pocket watches downtown.|The old mill grinds 45 sacks of flour daily.|UNKNOWN
p14|Seagulls steal sandwiches from careless tourists.|Brass bells ring across the valley 12 times on sundays.|UNKNOWN
p15|Desert cacti store water in thick stems.|The river ferry carries 120 passengers across the wide channel.|UNKNOWN
p16|Silent owls hunt mice in dark forests.|In dark forests silent owls hunt mice.|AGREE
p17|The baker kneads dough before dawn.|Before dawn the baker kneads dough.|AGREE
p18|Wild horses gallop over green hills.|Over green hills wild horses gallop.|AGREE
p19|The rocket reached 9000 meters altitude.|The amber lighthouse flashes every 30 seconds at night.|UNKNOWN
p20|She owns 42 cats and 17 dogs.|Copper wires conduct electricity through 8 circuits.|UNKNOWN
EOF
echo "$DUMMY" > "$DP/dummy.txt"
printf 'throwaway differential need\n' > "$DP/need.txt"
while IFS='|' read -r pid s c exp; do
  [ -n "$pid" ] || continue
  PD=$DP/$pid; mkdir -p "$PD/sdA" "$PD/sdB"
  printf 'P|pd1|Throwaway\nH|throwa.example\nS|%s\nP|pd2|Throwaway\nH|throwb.example\nS|%s\n' "$s" "$s" > "$PD/pages.txt"
  printf '%s\n' "$c" > "$PD/claim.txt"
  $BIN teach "$G" "$PD/sdA" >/dev/null 2>&1
  $BIN kbcommit "$PD/claim.txt" "$PD/sdA" >/dev/null 2>&1
  QA=$($BIN query "$PD/sdA" "$DP/need.txt" | grep '^QUERY|' | head -1 | cut -d'|' -f2-)
  $BIN verdict "$PD/sdA" "$DP/need.txt" "$PD/pages.txt" FACT "$QA" > "$PD/pathA.txt" 2>&1
  $BIN teach "$G" "$PD/sdB" >/dev/null 2>&1
  $BIN kbcommit "$DP/dummy.txt" "$PD/sdB" >/dev/null 2>&1
  QB=$($BIN query "$PD/sdB" "$DP/need.txt" | grep '^QUERY|' | head -1 | cut -d'|' -f2-)
  $BIN verdict "$PD/sdB" "$DP/need.txt" "$PD/pages.txt" FACT "$QB" > "$PD/pathB_pend.txt" 2>&1
  $BIN kbcommit "$PD/claim.txt" "$PD/sdB" > "$PD/pathB_auto.txt" 2>&1
  # classify
  if grep -q 'KB|CORROBORATED|' "$PD/pathA.txt"; then ca=AGREE
  elif grep -q 'GATE|KB_CONTRADICTION|' "$PD/pathA.txt"; then ca=CONTRADICT
  else ca=UNKNOWN; fi
  if grep -q 'KB|AUTO_PROMOTED|' "$PD/pathB_auto.txt"; then cb=AGREE
  elif grep -q 'KB|AUTO_FALSE|' "$PD/pathB_auto.txt"; then cb=CONTRADICT
  else cb=UNKNOWN; fi
  if [ "$ca" = "$exp" ] && [ "$cb" = "$exp" ] && [ "$ca" = "$cb" ]; then
    pass=$((pass+1)); # echo "OK $pid $ca==$cb==$exp"
  else
    fail=$((fail+1)); echo "DIVERGENCE $pid: prior=$ca tv=$cb expected=$exp"
  fi
done < "$DP/pairs.txt"

echo "SHAKEDOWN-DONE pass=$pass fail=$fail" | tee "$R/SUMMARY.txt"
