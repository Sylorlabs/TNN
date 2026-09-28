#!/bin/bash
# run_mrc.sh — MESSY-REALITY 1x pilot runner.
# Static checks → compile → run CUR/CTL/INJ twice each → byte-compare reruns →
# separate awk checker → EP/audit validation → in-Zag CL_CHECK validation.
# Fails loudly on any deviation. See PREREG_MESSY_PILOT.md (frozen pre-build).
# DO NOT COMMIT (parent commits sequentially).
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
pass=0; fail=0
chk(){ if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

echo "== static: no RNG anywhere =="
chk "no-rng" "! grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc' mrc.zag mhist.zag st_memory_core.zag substrate/"

echo "== static: vendored substrate byte-identical to wave10 debate-norecord =="
chk "st-core-identical" "cmp -s st_memory_core.zag ../../wave10/debate-norecord/st_memory_core.zag"
chk "common-identical" "cmp -s substrate/cl/common.zag ../../wave10/debate-norecord/substrate/cl/common.zag"
chk "bare-imports" "[ \"\$(grep -c '^@import' mrc.zag)\" = 1 ] && [ \"\$(grep -c '^@import' mhist.zag)\" = 1 ]"

echo "== static: assertion volume never read by CUR contra code =="
# n_assert_a/n_assert_b are generated+hashed but must never be READ by arm code.
# The only allowed mentions are the struct fields, world_build writes, and the
# world_hash reads. Extract arm_cur_contra and demand zero mentions there.
awk '/fn arm_cur_contra/,/^}/' mrc.zag > /tmp/cur_contra_body.txt
chk "no-assertvol-in-cur-contra" "! grep -n 'n_assert' /tmp/cur_contra_body.txt"

echo "== compile =="
"$ZNC" mrc.zag --no-zagd --no-analyze --no-foreground-cache -o mrc_bin
chk "compile" "[ \$? -eq 0 ] && [ -x mrc_bin ]"

echo "== load gate for heavy runs (1-min load < 2.5) =="
tries=0
while [ $tries -lt 10 ]; do
  load=$(awk '{print $1}' /proc/loadavg)
  if awk -v l="$load" 'BEGIN{exit !(l < 2.5)}'; then echo "load OK: $load"; break; fi
  echo "load high ($load), waiting 60s..."; sleep 60; tries=$((tries+1))
done
if [ $tries -ge 10 ]; then echo "ABORT: load still high after 10 min"; exit 3; fi

for arm in cur ctl inj; do
  echo "== run arm=$arm (first) =="
  ./mrc_bin "$arm" > "transcript_${arm}_a.txt" 2>"run_${arm}_a.err"
  chk "run-$arm-a-exit" "[ \$? -eq 0 ]"
  echo "== run arm=$arm (rerun) =="
  ./mrc_bin "$arm" > "transcript_${arm}_b.txt" 2>"run_${arm}_b.err"
  chk "run-$arm-b-exit" "[ \$? -eq 0 ]"
  echo "== determinism: byte-identical reruns =="
  chk "rerun-identical-$arm" "cmp -s transcript_${arm}_a.txt transcript_${arm}_b.txt"

  echo "== EP/audit validation arm=$arm =="
  ep_n=$(grep -c '^EP,' "transcript_${arm}_a.txt")
  chk "ep-count-$arm" "[ \"$ep_n\" = 4560 ]"
  # every EP: bytes == entries*64  (EP,arm,ep,entries,bytes,...)
  chk "ep-bytes-eq-entries64-$arm" "awk -F, '/^EP,/{if (\$5 != \$4*64) {print; bad=1}} END{exit bad}' transcript_${arm}_a.txt"
  # K1: every episode <= 4096 B
  maxb=$(awk -F, '/^EP,/{if ($5>m) m=$5} END{print m+0}' "transcript_${arm}_a.txt")
  echo "  max EP bytes ($arm): $maxb"
  chk "k1-max-$arm" "[ \"$maxb\" -le 4096 ]"
  medb=$(awk -F, '/^EP,/{b[NR]=$4} END{n=asort(b); print b[int(n/2)]}' "transcript_${arm}_a.txt" 2>/dev/null || \
         awk -F, '/^EP,/{print $4}' "transcript_${arm}_a.txt" | sort -n | awk '{a[NR]=$1} END{print a[int(NR/2)]}')
  echo "  median EP bytes ($arm): $medb"

  echo "== G-line count arm=$arm =="
  g_n=$(grep -c '^G,' "transcript_${arm}_a.txt")
  chk "g-count-$arm" "[ \"$g_n\" = 4560 ]"

  echo "== in-Zag CL_CHECK validation arm=$arm =="
  chk "clchecks-$arm" "awk -F, '/^CL_CHECK,/{if (\$3 != \$4) {print; bad=1}} END{exit bad}' transcript_${arm}_a.txt"

  echo "== separate checker arm=$arm =="
  awk -f check_mrc.awk "transcript_${arm}_a.txt" > "check_${arm}.out" 2>"check_${arm}.err"
  chk "checker-exit-$arm" "[ \$? -eq 0 ]"
  tail -1 "check_${arm}.out" | grep -q CHECK_OK && echo "  checker: CHECK_OK" || echo "  checker output tail: $(tail -1 check_${arm}.out)"

  echo "== PREMSUM arm=$arm =="
  grep '^PREMSUM,' "transcript_${arm}_a.txt" || true
done

echo
echo "RESULT: pass=$pass fail=$fail"
[ "$fail" = 0 ]
