#!/usr/bin/env bash
# Red-team legs + frozen bars for v3c RT batteries.
set -e
export TMPDIR=~/workspace/tmp_commit
J=~/workspace/nec_v3b/job3
A=$J/analysis
W=$J/work
ATT=~/workspace/nec_v3b/job1/batteries
cd $W
declare -A INMAP
tags=()
add() { local tag=$1 battery=$2; tags+=("$tag"); INMAP[$tag]=$battery; }
for v in 26 27; do
  add rt${v}_rta_s1 rta_s1
  add rt${v}_rtb_s1 rtb_s1
  for c in base v1 v2 v3 v4 v5 v6; do add rt${v}_rtc_$c rtc_$c; done
  for s in s1 s10 s100; do add rt${v}_rtd_$s rtd_$s; done
  for e in learn fatigue solo_learn solo_fatigue; do add rt${v}_rte_$e rte_$e; done
  add rt${v}_rtf_collide rtf_collide
done
add rt28_rta_s1 rta_s1
add rt28_rtb_s1 rtb_s1
for c in base v1 v2 v3 v4 v5 v6; do add rt28_rtc_$c rtc_$c; done
add rt28_rtd_s1 rtd_s1
for e in learn fatigue solo_learn solo_fatigue; do add rt28_rte_$e rte_$e; done
add rt28_rtf_collide rtf_collide
for tag in "${tags[@]}"; do
  v=${tag:2:2}
  python3 $A/to_analyzer.py ${tag}_A.tsv legs_$tag v$v
  echo "########## $tag ##########"
  python3 $A/bars_full.py legs_$tag v$v ${tag}_A.tsv $ATT/${INMAP[$tag]}.tsv 2>&1 | grep -E "B1|B2:|B3:|B4=|B4b|B5=|B6|B7=|B9 |B13 |G curves" 
done
echo done
