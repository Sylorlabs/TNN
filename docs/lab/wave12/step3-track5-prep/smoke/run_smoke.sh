#!/bin/bash
# Track 5 STEP 3 smoke runner: build the native Zag prep binary, run each
# isolation mode twice, require byte-identical reruns, and check the
# machine-checkable bars. This is PREP ONLY — the comparison trial is BLOCKED.
# DO NOT COMMIT (parent commits sequentially).
set -u
cd "$(dirname "$0")/../src"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
pass=0; fail=0
chk(){ if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

echo "== static: no RNG anywhere in the T5 prep sources =="
chk "no-rng" "! grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc' t5.zag t5_core.zag t5_arms.zag t5_traps.zag"
echo "== static: bare @imports only =="
chk "bare-imports-core" "[ \"\$(grep -c '^@import' t5_core.zag)\" = 1 ]"
chk "bare-imports-arms" "[ \"\$(grep -c '^@import' t5_arms.zag)\" = 1 ]"
chk "bare-imports-traps" "[ \"\$(grep -c '^@import' t5_traps.zag)\" = 1 ]"
chk "bare-imports-driver" "[ \"\$(grep -c '^@import' t5.zag)\" = 3 ]"
echo "== static: vendored substrate present =="
chk "vendor-sha" "[ -f substrate/R33_NATIVE_SHA256_V2.zag ]"
chk "vendor-io" "[ -f substrate/R33_NATIVE_IO_V1.zag ]"
chk "vendor-cl" "[ -f substrate/cl/common.zag ]"

echo "== compile =="
"$ZNC" t5.zag --no-zagd --no-analyze --no-foreground-cache -o t5_bin
chk "compile" "[ \$? -eq 0 ]"
mkdir -p ../smoke/logs

for M in smoke_a smoke_b smoke_c traps_a traps_b traps_c; do
  echo "== $M x2 =="
  ./t5_bin "$M" > "../smoke/logs/${M}_a.txt" 2>&1; ec_a=$?
  ./t5_bin "$M" > "../smoke/logs/${M}_b.txt" 2>&1; ec_b=$?
  chk "$M-deterministic" "cmp -s ../smoke/logs/${M}_a.txt ../smoke/logs/${M}_b.txt"
  chk "$M-exit0-a" "[ $ec_a -eq 0 ]"
  chk "$M-exit0-b" "[ $ec_b -eq 0 ]"
done

echo "== arm A bars =="
O=../smoke/logs/smoke_a_a.txt
chk "a-clean-recall-48" "grep -q 'CL_CHECK,a_clean_recall,48,48' $O"
chk "a-false-held-12" "grep -q 'CL_CHECK,a_false_held,12,12' $O"
chk "a-false-unrevised-12" "grep -q 'CL_CHECK,a_false_unrevised,12,12' $O"
chk "a-no-revise-ops" "grep -q 'CL_CHECK,a_no_revise_ops,0,0' $O"
chk "a-gate-refuses" "grep -q 'CL_CHECK,a_gate_refuses_add,201,201' $O"
chk "a-unknown-honest" "grep -q 'CL_CHECK,a_unknown_honest,-1,-1' $O"
chk "a-domain-hash" "grep -q '^DOMAIN_HASH,[0-9a-f]\\{64\\}\$' $O"
chk "a-digest" "grep -q '^DIGEST,smoke_a,[0-9a-f]\\{64\\}\$' $O"
chk "a-blocked-banner" "grep -q '^TRIAL_BLOCKED' $O"

echo "== arm B bars =="
O=../smoke/logs/smoke_b_a.txt
chk "b-empty-cert" "grep -q 'CL_CHECK,b_empty_cert,0,0' $O"
chk "b-learned-48" "grep -q 'CL_CHECK,b_learned_n,48,48' $O"
chk "b-retention-48" "grep -q 'CL_CHECK,b_retention,48,48' $O"
chk "b-directive-killed" "grep -q 'CL_CHECK,b_directive_killed,0,0' $O"
chk "b-truth-kept" "grep -q 'CL_CHECK,b_truth_kept,' $O"

echo "== arm C bars =="
O=../smoke/logs/smoke_c_a.txt
chk "c-seed-48" "grep -q 'CL_CHECK,c_seed_n,48,48' $O"
chk "c-corrob-10" "grep -q 'CL_CHECK,c_corrob_10,10,10' $O"
chk "c-circular-rejected" "grep -q 'CL_CHECK,c_circular_rejected,202,202' $O"
chk "c-laundered-rejected" "grep -q 'CL_CHECK,c_laundered_rejected,202,202' $O"
chk "c-false-revised" "grep -q 'CL_CHECK,c_false_revised_dec,1,1' $O"
chk "c-unplant-ok" "grep -q 'CL_CHECK,c_unplant_ok,0,0' $O"
chk "c-unplant-refused" "grep -q 'CL_CHECK,c_unplant_refused,205,205' $O"
chk "c-k2-same" "grep -q 'CL_CHECK,c_k2_same_outcome,' $O"

echo "== trap battery bars (telemetry only, no verdict) =="
for A in a b c; do
  O=../smoke/logs/traps_${A}_a.txt
  chk "traps-$A-lines" "[ \"\$(grep -c \"^TRAP,$A,\" $O)\" -ge 5 ]"
  chk "traps-$A-controls" "grep -q 'CL_CHECK,.*_ctrl_.*,1,1' $O"
  chk "traps-$A-macro" "grep -q \"^TRAP_MACRO,$A,\" $O"
done
chk "traps-a-t7-20" "grep -q '^TRAP,a,7,20,20\$' ../smoke/logs/traps_a_a.txt"
chk "traps-c-t7p-20" "grep -q '^TRAP,c,7p,20,20\$' ../smoke/logs/traps_c_a.txt"

echo "== RESULT: pass=$pass fail=$fail =="
[ "$fail" -eq 0 ]
