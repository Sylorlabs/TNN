#!/bin/bash
# Wave-12 STEP 5b runner: English curriculum 1x pilot.
# Deterministic native Zag build + double run (byte-identical) + independent
# Zag checker + mechanical transcript validation. Fails loudly on deviation.
# See PREREG_ENGLISH_PILOT.md (frozen pre-build; amendments in
# PREREG_AMENDMENTS.md are build notes / bug fixes, no bar changes).
# DO NOT COMMIT binaries (pilot_bin, check_bin) — parent commits sources only.
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
pass=0; fail=0
chk(){ if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

echo "== static: no RNG anywhere in pilot/counter/checker =="
chk "no-rng" "! grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc' pilot.zag hist_pilot.zag check.zag"
echo "== static: vendored substrate byte-identical to step2 =="
chk "st-core-identical" "cmp -s st_memory_core.zag ../step2-ledger-instrument/st_memory_core.zag"
chk "cl-identical" "cmp -s substrate/cl/common.zag ../step2-ledger-instrument/substrate/cl/common.zag"
chk "sha-identical" "cmp -s substrate/R33_NATIVE_SHA256_V2.zag ../step2-ledger-instrument/substrate/R33_NATIVE_SHA256_V2.zag"
chk "io-identical" "cmp -s substrate/R33_NATIVE_IO_V1.zag ../step2-ledger-instrument/substrate/R33_NATIVE_IO_V1.zag"
chk "bare-imports" "[ \"\$(grep -h '^@import' pilot.zag check.zag | wc -l)\" = 2 ]"

echo "== compile =="
"$ZNC" pilot.zag --no-zagd --no-analyze --no-foreground-cache -o pilot_bin
chk "compile-pilot" "[ \$? -eq 0 ]"
"$ZNC" check.zag --no-zagd --no-analyze --no-foreground-cache -o check_bin
chk "compile-check" "[ \$? -eq 0 ]"

echo "== pilot: 3,880 episodes x2 (byte-identical reruns) =="
./pilot_bin > run_a.txt 2>/dev/null
chk "run-a-ok" "grep -q '^PILOT,step5b,end' run_a.txt"
./pilot_bin > run_b.txt 2>/dev/null
chk "run-b-ok" "grep -q '^PILOT,step5b,end' run_b.txt"
chk "deterministic" "cmp -s run_a.txt run_b.txt"

echo "== independent checker (native Zag, reads transcript only) =="
./check_bin run_a.txt > check_a.txt 2>/dev/null
chk "checker-go" "grep -q '^CHECK,GO' check_a.txt"
chk "checker-no-dead" "! grep -q '^CHECK,DEAD' check_a.txt"

echo "== prereg bars from transcript (mechanical, independent of checker) =="
O=run_a.txt
chk "ep-total-3880" "[ \"\$(grep -c '^EP,' $O)\" = 3880 ]"
for H in E1 E2 E3 E4 E5 E6 EV; do
  case $H in
    E1) N=800;; E2) N=600;; E3) N=400;; E4) N=500;; E5) N=800;; E6) N=300;; EV) N=480;;
  esac
  chk "$H-histagg" "grep -q '^HISTAGG,$H,$N,' $O"
  chk "$H-ep-lines" "[ \"\$(grep -c \"^EP,$H,\" $O)\" = $N ]"
  chk "$H-k1-zag" "grep -q 'CL_CHECK,k1_max_bytes_le_4096,1,1' $O"
  chk "$H-no-other" "grep -q 'CL_CHECK,k1_other_class_zero,0,0' $O"
  maxb=$(awk -F, -v h="$H" '$1=="EP" && $2==h {if($5>m)m=$5} END{print m+0}' "$O")
  chk "$H-k1-indep-max-$maxb-le-4096" "[ \"$maxb\" -le 4096 ]"
  bad=$(awk -F, -v h="$H" '$1=="EP" && $2==h {if($5!=$4*64)b++} END{print b+0}' "$O")
  chk "$H-bytes-eq-entries-x64" "[ \"$bad\" = 0 ]"
  bad2=$(awk -F, -v h="$H" '$1=="EP" && $2==h {s=0;for(i=6;i<=15;i++)s+=$i;if(s!=$4)b++} END{print b+0}' "$O")
  chk "$H-class-sum-eq-entries" "[ \"$bad2\" = 0 ]"
done
chk "kfail-zero" "grep -q '^KFAIL,0,0' $O"
chk "dcount-6-6" "grep -q '^DCOUNT,6,6' $O"
chk "cksum-64" "grep -q '^CKSUM,64' $O"

echo "== RESULT: pass=$pass fail=$fail =="
[ "$fail" -eq 0 ]
