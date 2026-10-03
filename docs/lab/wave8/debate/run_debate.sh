#!/bin/bash
# Wave-8 debate trial runner.
# Deterministic native Zag build + run + mechanical bar validation.
# Fails loudly on any deviation. See PREREG_DEBATE.md.
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
pass=0; fail=0
chk(){ if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

echo "== static: no RNG in debate driver =="
chk "no-rng" "! grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc' debate.zag"
echo "== static: vendored cores byte-identical =="
chk "st-core-identical" "cmp -s st_memory_core.zag ../../wave7/felt-intensity/st_memory_core.zag"
chk "il-core-identical" "cmp -s il_core.zag ../../wave4/integrity-ledger/il_core.zag"
chk "bare-imports" "[ \"\$(grep -c '^@import' debate.zag)\" = 2 ]"

echo "== compile =="
"$ZNC" debate.zag --no-zagd --no-analyze --no-foreground-cache -o debate_bin
chk "compile" "[ \$? -eq 0 ]"

echo "== small leg x2 (byte-identical reruns) =="
./debate_bin small > run_small_a.txt 2>/dev/null
./debate_bin small > run_small_b.txt 2>/dev/null
chk "small-deterministic" "cmp -s run_small_a.txt run_small_b.txt"

echo "== scale leg x2 (10x throughput, byte-identical reruns) =="
./debate_bin scale > run_scale_a.txt 2>/dev/null
./debate_bin scale > run_scale_b.txt 2>/dev/null
chk "scale-deterministic" "cmp -s run_scale_a.txt run_scale_b.txt"

echo "== prereg bars on scale output =="
O=run_scale_a.txt
chk "F1-true-zero-corruption"   "grep -q 'CL_CHECK,agg_true_corrupt,0,0' $O"
chk "F1b-no-revision-failures"  "grep -q 'CL_CHECK,agg_false_rev_fail,0,0' $O"
chk "F2-false-revises-bar"      "grep -q 'CL_CHECK,agg_f2_bar,1,1' $O"
chk "F2-false-revised-180"      "grep -q '^180,false_revised\$' $O"
chk "F2-false-keeps-truth"      "grep -q 'CL_CHECK,agg_false_true_kept,60,60' $O"
chk "F3-r2-chooses-true"        "grep -q 'CL_CHECK,agg_f3_bar,1,1' $O"
chk "F4-r3-chooses-true"        "grep -q 'CL_CHECK,agg_f4_bar,1,1' $O"
chk "F5-volume-cheat-resisted"   "grep -q 'CL_CHECK,agg_f5_bar,1,1' $O"
chk "F6-all-replays-exact"      "[ \"\$(grep -c 'CL_CHECK,sess_replay_[a-z]*,0,0' $O)\" = 30 ]"
chk "F7-all-asserts-il-ok"      "[ \"\$(grep -c 'CL_CHECK,sess_assert_il_ok,48,48' $O)\" = 10 ]"
chk "F8-revise-count-180"       "[ \"\$(grep -c '^TR_REVISE' $O)\" = 180 ]"
chk "F8-no-true-revisions"      "[ \"\$(grep -c '^TR_REVISE,[0-9]*,0,' $O)\" = 0 ]"
chk "F8-all-revise-rc-zero"     "[ \"\$(grep '^TR_REVISE' $O | grep -vc ',0,0,0,0,0,')\" = 0 ]"
chk "F8-verify-lines-960"       "[ \"\$(grep -c '^TR_VERIFY' $O)\" = 960 ]"
chk "F8-choice3-all-true"        "[ \"\$(grep -c '^TR_CHOICE3,[0-9]*,[0-9]*,0,' $O)\" = 60 ]"

echo "== RESULT: pass=$pass fail=$fail =="
[ "$fail" -eq 0 ]
