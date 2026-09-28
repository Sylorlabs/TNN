#!/bin/bash
# Wave-12 STEP 1b runner: state schema + replay protocol + evolution law.
# Deterministic native Zag build + full evidence suite + mechanical bar checks.
# Fails loudly on any deviation. See PREREG_STATE_SCHEMA.md (frozen pre-build)
# and AMENDMENT_2026-09-20_schema.md (dated schema amendments).
# DO NOT COMMIT binaries (parent commits explicit file lists).
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
pass=0; fail=0
chk(){ if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

echo "== static: no RNG / wall-clock / threads in step1b sources =="
chk "no-rng" "! grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc|clock_gettime|gettimeofday' --include='*.zag' s1b_state.zag s1b_trans.zag s1b_codec.zag s1b_run.zag state1b.zag"
chk "no-float-state" "! grep -nE 'f32|f64|as f' s1b_state.zag s1b_trans.zag s1b_codec.zag s1b_run.zag state1b.zag"
echo "== static: bare @imports =="
chk "bare-imports" "[ \"\$(grep -h -c '^@import' s1b_state.zag s1b_trans.zag s1b_codec.zag s1b_run.zag state1b.zag | tr '\\n' '+' | sed 's/+\$//')\" = '1+1+1+2+1' ]"
echo "== static: vendored substrate present =="
chk "substrate-sha" "[ -f substrate/R33_NATIVE_SHA256_V2.zag ]"
chk "substrate-io"  "[ -f substrate/R33_NATIVE_IO_V1.zag ]"
chk "substrate-cl"  "[ -f substrate/cl/common.zag ]"

echo "== compile: two build hashes =="
"$ZNC" state1b.zag --no-zagd --no-analyze --no-foreground-cache -o state1b_bin_a
chk "compile-a" "[ \$? -eq 0 ]"
"$ZNC" state1b.zag --no-zagd -o state1b_bin_b
chk "compile-b" "[ \$? -eq 0 ]"
HA=$(sha256sum state1b_bin_a | awk '{print $1}')
HB=$(sha256sum state1b_bin_b | awk '{print $1}')
echo "BUILD_HASH_A=$HA"
echo "BUILD_HASH_B=$HB"
echo "$HA  state1b_bin_a" > build_hashes.txt
echo "$HB  state1b_bin_b" >> build_hashes.txt

echo "== replay suite: 1000 trials x2 build hashes (17: 1000/1000; KB1/KB5) =="
./state1b_bin_a replay v1 > run_replay_a.txt 2>&1
chk "replay-a-exit" "[ \$? -eq 0 ]"
./state1b_bin_b replay v1 > run_replay_b.txt 2>&1
chk "replay-b-exit" "[ \$? -eq 0 ]"
chk "replay-a-1000" "grep -q 'CL_CHECK,replay_pass,1000,1000' run_replay_a.txt"
chk "replay-a-0fail" "grep -q 'CL_CHECK,replay_fail,0,0' run_replay_a.txt"
chk "replay-b-1000" "grep -q 'CL_CHECK,replay_pass,1000,1000' run_replay_b.txt"
chk "replay-b-0fail" "grep -q 'CL_CHECK,replay_fail,0,0' run_replay_b.txt"
chk "replay-fieldcount" "grep -q 'FIELD_COUNT,273' run_replay_a.txt"
./state1b_bin_a replay v1 > run_replay_a2.txt 2>&1
chk "replay-rerun-identical" "cmp -s run_replay_a.txt run_replay_a2.txt"
chk "replay-no-kb2" "! grep -q 'KB2_VIOLATION' run_replay_a.txt"
chk "replay-no-kb4" "! grep -q 'KB4_VIOLATION' run_replay_a.txt"
chk "replay-no-fail-lines" "! grep -q 'REPLAY_FAIL' run_replay_a.txt"

echo "== perm: input-arrival-order fuzzer, 3 orders x 200 (18 §6) =="
./state1b_bin_a perm > run_perm.txt 2>&1
chk "perm-exit" "[ \$? -eq 0 ]"
chk "perm-3x200" "[ \"\$(grep -c 'CL_CHECK,perm_pass,200,200' run_perm.txt)\" = 3 ]"
chk "perm-0fail" "! grep -q 'CL_CHECK,perm_fail,[^0]' run_perm.txt"

echo "== difftest: 5x460 pairs, planted rctr p=0.05 (16: discovery) =="
./state1b_bin_a difftest > run_difftest.txt 2>&1
chk "difftest-exit" "[ \$? -eq 0 ]"
chk "difftest-5x23" "[ \"\$(grep -c 'CL_CHECK,diff_div,23,23' run_difftest.txt)\" = 5 ]"
chk "difftest-firsts" "grep -q 'CL_CHECK,diff_first,7,7' run_difftest.txt && grep -q 'CL_CHECK,diff_first,10,10' run_difftest.txt && grep -q 'CL_CHECK,diff_first,13,13' run_difftest.txt && grep -q 'CL_CHECK,diff_first,16,16' run_difftest.txt && grep -q 'CL_CHECK,diff_first,19,19' run_difftest.txt"
chk "difftest-hunt-5" "[ \"\$(grep -c 'HUNT_FOUND,rctr' run_difftest.txt)\" = 5 ]"
chk "difftest-k1-alive" "grep -q 'K1_16,NOT_FIRED' run_difftest.txt"

echo "== diffneg: 460-pair negative control =="
./state1b_bin_a diffneg > run_diffneg.txt 2>&1
chk "diffneg-exit" "[ \$? -eq 0 ]"
chk "diffneg-zero" "grep -q 'CL_CHECK,diffneg_div,0,0' run_diffneg.txt"

echo "== diffk2: v2 schema closure + retroactive re-validation =="
./state1b_bin_a diffk2 > run_diffk2.txt 2>&1
chk "diffk2-exit" "[ \$? -eq 0 ]"
chk "diffk2-0alarms" "[ \"\$(grep -c 'CL_CHECK,k2_alarms,0,0' run_diffk2.txt)\" = 5 ]"
chk "diffk2-no-k2alarm" "! grep -q 'K2_ALARM' run_diffk2.txt"
chk "diffk2-k2-alive" "grep -q 'K2_16,NOT_FIRED' run_diffk2.txt"
chk "diffk2-v2-replay-1000" "grep -q 'CL_CHECK,replay_pass,1000,1000' run_diffk2.txt"
chk "diffk2-v2-fieldcount" "grep -q 'FIELD_COUNT,274' run_diffk2.txt"

echo "== conform: 20-episode run + taxonomy + KB probes =="
./state1b_bin_a conform > run_conform.txt 2>&1
chk "conform-exit" "[ \$? -eq 0 ]"
chk "conform-replay-20" "grep -q 'CL_CHECK,conform_replay_pass,20,20' run_conform.txt"
chk "conform-taxonA-20" "grep -q 'CL_CHECK,taxon_A_count,20,20' run_conform.txt"
chk "conform-taxonC-20" "grep -q 'CL_CHECK,taxon_C_count,20,20' run_conform.txt"
chk "conform-taxonA-block" "[ \"\$(grep -c 'TAXON,[0-9]*,class,1,block,136' run_conform.txt)\" = 20 ]"
chk "conform-taxonC-block" "[ \"\$(grep -c 'TAXON,[0-9]*,class,3,block,16' run_conform.txt)\" = 20 ]"
chk "conform-classD-refuse" "grep -q 'REFUSE,constitution_mismatch' run_conform.txt"
chk "conform-kb3" "grep -q 'CL_CHECK,kb3_tiebreak,1,1' run_conform.txt"
chk "conform-kb4" "grep -q 'CL_CHECK,kb4_exhaust_refuse,1,1' run_conform.txt"
chk "conform-varbudget" "grep -q 'CL_CHECK,varbudget_fallback,1,1' run_conform.txt"
chk "conform-dcodec" "grep -q 'CL_CHECK,d_codec_roundtrip,1,1' run_conform.txt"
chk "conform-inventory" "grep -q 'TAXON_INVENTORY,A,20,C,20,B,0_static,D,1_refuse_demo' run_conform.txt"

echo "== evidence hashes =="
sha256sum run_replay_a.txt run_replay_b.txt run_perm.txt run_difftest.txt run_diffneg.txt run_diffk2.txt run_conform.txt build_hashes.txt > sha256sums.txt
cat sha256sums.txt

echo "== RESULT: pass=$pass fail=$fail =="
[ "$fail" -eq 0 ]
