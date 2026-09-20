#!/bin/bash
# Wave-12 STEP 2 runner: audit-ledger histogram instrumentation.
# Deterministic native Zag build + run + mechanical bar validation.
# Fails loudly on any deviation. See PREREG_STEP2.md (frozen pre-build).
# DO NOT COMMIT the binary (parent commits sources only).
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
pass=0; fail=0
chk(){ if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

echo "== static: no RNG anywhere in driver/counter =="
chk "no-rng" "! grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc' harness.zag hist.zag"
echo "== static: vendored substrate byte-identical to wave10/debate-norecord =="
chk "st-core-identical" "cmp -s st_memory_core.zag ../../wave10/debate-norecord/st_memory_core.zag"
chk "cl-identical" "cmp -s substrate/cl/common.zag ../../wave10/debate-norecord/substrate/cl/common.zag"
chk "bare-imports" "[ \"\$(grep -h '^@import' harness.zag hist.zag | wc -l)\" = 2 ]"

echo "== compile =="
"$ZNC" harness.zag --no-zagd --no-analyze --no-foreground-cache -o harness_bin
chk "compile" "[ \$? -eq 0 ]"

run_leg(){ # $1 = harness
  ./harness_bin "$1" > "run_${1}_a.txt" 2>/dev/null
  ./harness_bin "$1" > "run_${1}_b.txt" 2>/dev/null
}

for H in code english messy; do
  echo "== harness $H: 200 dry-run episodes x2 (byte-identical reruns) =="
  run_leg "$H"
  chk "$H-deterministic" "cmp -s run_${H}_a.txt run_${H}_b.txt"
done

echo "== prereg bars from transcript (independent of in-Zag checks) =="
for H in code english messy; do
  O=run_${H}_a.txt
  chk "$H-200eps"      "grep -q '^HISTAGG,$H,200,' $O"
  chk "$H-ep-lines"    "[ \"\$(grep -c \"^EP,$H,\" $O)\" = 200 ]"
  chk "$H-k1-zag"      "grep -q 'CL_CHECK,k1_max_bytes_le_4096,1,1' $O"
  chk "$H-no-other"    "grep -q 'CL_CHECK,k1_other_class_zero,0,0' $O"
  chk "$H-verify-ok"   "grep -q 'CL_CHECK,verify_fail,0,0' $O"
  chk "$H-kill-ok"     "grep -q 'CL_CHECK,kill_fail,0,0' $O"
  # independent K1: max per-episode bytes from the EP lines themselves
  maxb=$(awk -F, -v h="$H" '$1=="EP" && $2==h {if($5>m)m=$5} END{print m+0}' "$O")
  chk "$H-k1-indep-max-$maxb-le-4096" "[ \"$maxb\" -le 4096 ]"
  # independent entry<->byte consistency: bytes == entries*64 on every EP line
  bad=$(awk -F, -v h="$H" '$1=="EP" && $2==h {if($5!=$4*64)b++} END{print b+0}' "$O")
  chk "$H-bytes-eq-entries-x64" "[ \"$bad\" = 0 ]"
  # independent class-sum consistency: class counts sum to entries
  bad2=$(awk -F, -v h="$H" '$1=="EP" && $2==h {s=0;for(i=6;i<=14;i++)s+=$i;if(s!=$4)b++} END{print b+0}' "$O")
  chk "$H-class-sum-eq-entries" "[ \"$bad2\" = 0 ]"
done

echo "== RESULT: pass=$pass fail=$fail =="
[ "$fail" -eq 0 ]
