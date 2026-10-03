#!/bin/bash
# Wave-10 EXP-3 debate-norecord trial runner.
# Deterministic native Zag build + run + mechanical bar validation.
# Fails loudly on any deviation. See PREREG_DEBATE_NORECORD.md (frozen pre-build).
# DO NOT COMMIT (parent commits sequentially).
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
pass=0; fail=0
chk(){ if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

echo "== static: no RNG in debate-norecord driver =="
chk "no-rng" "! grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc' debate_nr.zag"
echo "== static: vendored cores byte-identical to wave8 =="
chk "st-core-identical" "cmp -s st_memory_core.zag ../../wave8/debate/st_memory_core.zag"
chk "il-core-identical" "cmp -s il_core.zag ../../wave8/debate/il_core.zag"
chk "bare-imports" "[ \"\$(grep -c '^@import' debate_nr.zag)\" = 2 ]"

echo "== compile =="
"$ZNC" debate_nr.zag --no-zagd --no-analyze --no-foreground-cache -o debate_nr_bin
chk "compile" "[ \$? -eq 0 ]"

echo "== load gate for heavy runs (1-min load < 2.5) =="
tries=0
while [ $tries -lt 10 ]; do
  load=$(awk '{print $1}' /proc/loadavg)
  if awk -v l="$load" 'BEGIN{exit !(l < 2.5)}'; then echo "load OK: $load"; break; fi
  echo "load high ($load), waiting 60s..."; sleep 60; tries=$((tries+1))
done
if [ $tries -ge 10 ]; then echo "ABORT: load still high after 10 min"; exit 3; fi

run_leg(){ # $1 = variant, $2 = scale word
  nice -n 10 ./debate_nr_bin "$1" "$2" > "run_${1}_${2}_a.txt" 2>/dev/null
  nice -n 10 ./debate_nr_bin "$1" "$2" > "run_${1}_${2}_b.txt" 2>/dev/null
}

for V in A B; do
  echo "== variant $V: small leg x2 (byte-identical reruns) =="
  run_leg "$V" small
  chk "$V-small-deterministic" "cmp -s run_${V}_small_a.txt run_${V}_small_b.txt"
  echo "== variant $V: scale leg x2 (10x throughput, byte-identical reruns) =="
  run_leg "$V" scale
  chk "$V-scale-deterministic" "cmp -s run_${V}_scale_a.txt run_${V}_scale_b.txt"
done

echo "== prereg bars: variant A small =="
O=run_A_small_a.txt
chk "A-small-cfg"        "grep -q '^DEBATE_CFG,A,small,1,sessions\$' $O"
chk "A-small-F1"         "grep -q 'CL_CHECK,agg_true_corrupt,0,0' $O"
chk "A-small-F2bar"      "grep -q 'CL_CHECK,agg_f2_bar,1,1' $O"
chk "A-small-F2-18"      "grep -q '^18,false_revised\$' $O"
chk "A-small-M1-margin0" "grep -q 'CL_CHECK,a_margin2,0,0' $O"
chk "A-small-M2-abst6"   "grep -q 'AGG_ABSTAIN,6,2\$' $O"
chk "A-small-M3-r3"      "grep -q 'CL_CHECK,a_r3_true,4,4' $O"
chk "A-small-no-falsif"  "! grep -q 'FALSIFIED_FA' $O"

echo "== prereg bars: variant A scale =="
O=run_A_scale_a.txt
chk "A-scale-cfg"          "grep -q '^DEBATE_CFG,A,scale,10,sessions\$' $O"
chk "A-F1-true-zero"       "grep -q 'CL_CHECK,agg_true_corrupt,0,0' $O"
chk "A-F1b-no-rev-fail"    "grep -q 'CL_CHECK,agg_false_rev_fail,0,0' $O"
chk "A-F2-bar"             "grep -q 'CL_CHECK,agg_f2_bar,1,1' $O"
chk "A-F2-180-revised"     "grep -q '^180,false_revised\$' $O"
chk "A-F2-keeps-truth"     "grep -q 'CL_CHECK,agg_false_true_kept,60,60' $O"
chk "A-M1-margin2-zero"    "grep -q 'CL_CHECK,a_margin2,0,0' $O"
chk "A-M2-r2-abstain-60"   "grep -q 'CL_CHECK,a_r2_abstain,60,60' $O"
chk "A-M2-r2-true-0"       "grep -q 'CL_CHECK,a_r2_true,0,0' $O"
chk "A-M3-margin3-40"      "grep -q 'CL_CHECK,a_margin3,40,40' $O"
chk "A-M3-r3-true-40"      "grep -q 'CL_CHECK,a_r3_true,40,40' $O"
chk "A-M3-r3-abstain-20"   "grep -q 'CL_CHECK,a_r3_abstain,20,20' $O"
chk "A-M3-admit-40"        "grep -q 'CL_CHECK,a_admit_net,40,40' $O"
chk "A-M3-split-0"         "grep -q 'CL_CHECK,a_split_net,0,0' $O"
chk "A-F7-replays-30"      "[ \"\$(grep -c 'CL_CHECK,sess_replay_[a-z]*,0,0' $O)\" = 30 ]"
chk "A-F7-asserts-48x10"   "[ \"\$(grep -c 'CL_CHECK,sess_assert_il_ok,48,48' $O)\" = 10 ]"
chk "A-F8-revise-180"      "[ \"\$(grep -c '^TR_REVISE' $O)\" = 180 ]"
chk "A-F8-no-true-rev"     "[ \"\$(grep -c '^TR_REVISE,[0-9]*,0,' $O)\" = 0 ]"
chk "A-F8-revise-rc-zero"  "[ \"\$(grep '^TR_REVISE' $O | grep -vc ',0,0,0,0,0,')\" = 0 ]"
chk "A-F8-verify-960"      "[ \"\$(grep -c '^TR_VERIFY' $O)\" = 960 ]"
chk "A-F8-verify-all-good" "[ \"\$(grep '^TR_VERIFY' $O | grep -vc ',1,1\$')\" = 0 ]"
chk "A-choice2-abst-60"    "[ \"\$(grep -c '^TR_CHOICE2,[0-9]*,[0-9]*,-1,' $O)\" = 60 ]"
chk "A-tbdiag-60-true"     "[ \"\$(grep -c '^TR_TBDIAG,[0-9]*,[0-9]*,0\$' $O)\" = 60 ]"
chk "A-choice3-true-40"    "[ \"\$(grep -c '^TR_CHOICE3,[0-9]*,[0-9]*,0,' $O)\" = 40 ]"
chk "A-choice3-abst-20"    "[ \"\$(grep -c '^TR_CHOICE3,[0-9]*,[0-9]*,-1,' $O)\" = 20 ]"
chk "A-no-falsified"       "! grep -q 'FALSIFIED_FA' $O"

echo "== prereg bars: variant B small =="
O=run_B_small_a.txt
chk "B-small-cfg"        "grep -q '^DEBATE_CFG,B,small,1,sessions\$' $O"
chk "B-small-F1"         "grep -q 'CL_CHECK,agg_true_corrupt,0,0' $O"
chk "B-small-F2-18"      "grep -q '^18,false_revised\$' $O"
chk "B-small-M4-cap"     "grep -q 'AGG_FALSE_PICKS,6,6\$' $O"
chk "B-small-M4-margin"  "grep -q 'CL_CHECK,b_margin2,-24,-24' $O"
chk "B-small-M6-over"    "grep -q 'CL_CHECK,b_overclaim,6,6' $O"
chk "B-small-no-falsif"  "! grep -q 'FALSIFIED_FB' $O"

echo "== prereg bars: variant B scale =="
O=run_B_scale_a.txt
chk "B-scale-cfg"          "grep -q '^DEBATE_CFG,B,scale,10,sessions\$' $O"
chk "B-F1-true-zero"       "grep -q 'CL_CHECK,agg_true_corrupt,0,0' $O"
chk "B-F1b-no-rev-fail"    "grep -q 'CL_CHECK,agg_false_rev_fail,0,0' $O"
chk "B-F2-bar"             "grep -q 'CL_CHECK,agg_f2_bar,1,1' $O"
chk "B-F2-180-revised"     "grep -q '^180,false_revised\$' $O"
chk "B-F2-keeps-truth"     "grep -q 'CL_CHECK,agg_false_true_kept,60,60' $O"
chk "B-M4-r2-false-60"     "grep -q 'CL_CHECK,b_r2_false,60,60' $O"
chk "B-M4-r2-true-0"       "grep -q 'CL_CHECK,b_r2_true,0,0' $O"
chk "B-M4-margin2-neg"     "grep -q 'CL_CHECK,b_margin2,-240,-240' $O"
chk "B-M5-ledger-blind"    "[ \"\$(grep -c 'CL_CHECK,sess_assert_il_ok,48,48' $O)\" = 10 ]"
chk "B-M6-margin3-neg"     "grep -q 'CL_CHECK,b_margin3,-280,-280' $O"
chk "B-M6-r3-false-60"     "grep -q 'CL_CHECK,b_r3_false,60,60' $O"
chk "B-M6-overclaim-60"    "grep -q 'CL_CHECK,b_overclaim,60,60' $O"
chk "B-corr-0-240"         "grep -q 'AGG_CORR,0,240,240\$' $O"
chk "B-fresh-contra-40"    "grep -q 'AGG_FRESH_CONTRA,40\$' $O"
chk "B-F7-replays-30"      "[ \"\$(grep -c 'CL_CHECK,sess_replay_[a-z]*,0,0' $O)\" = 30 ]"
chk "B-F8-revise-180"      "[ \"\$(grep -c '^TR_REVISE' $O)\" = 180 ]"
chk "B-F8-no-true-rev"     "[ \"\$(grep -c '^TR_REVISE,[0-9]*,0,' $O)\" = 0 ]"
chk "B-F8-revise-rc-zero"  "[ \"\$(grep '^TR_REVISE' $O | grep -vc ',0,0,0,0,0,')\" = 0 ]"
chk "B-choice2-false-60"   "[ \"\$(grep -c '^TR_CHOICE2,[0-9]*,[0-9]*,1,' $O)\" = 60 ]"
chk "B-choice3-false-60"   "[ \"\$(grep -c '^TR_CHOICE3,[0-9]*,[0-9]*,1,' $O)\" = 60 ]"
chk "B-qx-60-none"         "[ \"\$(grep -c '^TR_QX,[0-9]*,[0-9]*,9[0-9][0-9],0\$' $O)\" = 60 ]"
chk "B-no-falsified"       "! grep -q 'FALSIFIED_FB' $O"

echo "== RESULT: pass=$pass fail=$fail =="
[ "$fail" -eq 0 ]
