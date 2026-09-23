#!/bin/bash
# run_messy2.sh — STEP 5c-M2 battery runner (prereg §6 build order).
# Gates: no-RNG grep → vendored-file cmp → static checks → d1 probe →
# compile → CUR/CTL ×2 → cmp reruns → line counts → K1 → independent checker.
# Any gate failure aborts (set -e). Kill bars halt immediately.
set -e
cd "$(dirname "$0")"
ZNC="$HOME/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1"
PILOT="$HOME/workspace/tnn-lab/wave12/step5c-messy-pilot"

echo "=== [1/10] no-RNG grep (messy2.zag + vendored substrate)"
if grep -nEi '\brand\b|rand\(\)|srand|/dev/(u)?random|getrandom|_zag_rand' messy2.zag st_memory_core.zag mhist.zag substrate/cl/common.zag 2>/dev/null; then
  echo "K3 FAIL: RNG/static hit"; exit 10
fi
echo "no-RNG: clean"

echo "=== [2/10] vendored-file byte comparison vs step5c-messy-pilot"
for f in st_memory_core.zag mhist.zag; do
  cmp -s "$f" "$PILOT/$f" || { echo "VENDOR FAIL: $f differs"; exit 11; }
done
diff -r substrate "$PILOT/substrate" >/dev/null || { echo "VENDOR FAIL: substrate differs"; exit 11; }
echo "vendored files: byte-identical"

echo "=== [3/10] static integrity checks"
# CUR fns must not read assertion-volume fields
for fn in arm_cur_r2b arm_cur_n2 arm_cur_c2 arm_cur_a2; do
  # extract function body crudely: from "fn $fn" to next "^fn "
  body=$(awk "/^fn $fn\(/{p=1} p{print} /^\}/{if(p)exit}" messy2.zag)
  if echo "$body" | grep -q 'n_assert_a\|n_assert_b'; then
    echo "STATIC FAIL: $fn reads n_assert_*"; exit 12
  fi
done
echo "static: no CUR fn reads n_assert_*"
# arm_cur_c2 must reference prov_tier (the cross-check)
if ! grep -q 'prov_tier' messy2.zag; then echo "STATIC FAIL: no prov_tier cross-check"; exit 12; fi
echo "static: prov_tier cross-check present"

echo "=== [4/10] d1/d2 ledger-layout probe"
"$ZNC" d1probe.zag -o /tmp/d1probe_bin 2>/dev/null
/tmp/d1probe_bin > /tmp/d1probe.out 2>&1
grep -q '^PROBE_OK$' /tmp/d1probe.out || { echo "PROBE FAIL"; cat /tmp/d1probe.out; exit 13; }
echo "d1probe: PROBE_OK"

echo "=== [5/10] compile battery"
"$ZNC" messy2.zag -o /tmp/messy2_bin 2>/dev/null
echo "compile: ok"

echo "=== [6/10] run arms (CUR ×2, CTL ×2)"
/tmp/messy2_bin cur > /tmp/messy2_cur_a.log 2>&1
/tmp/messy2_bin cur > /tmp/messy2_cur_b.log 2>&1
/tmp/messy2_bin ctl > /tmp/messy2_ctl_a.log 2>&1
/tmp/messy2_bin ctl > /tmp/messy2_ctl_b.log 2>&1
echo "runs: complete"

echo "=== [7/10] K2 determinism (byte-identical reruns)"
cmp -s /tmp/messy2_cur_a.log /tmp/messy2_cur_b.log || { echo "K2 FAIL: CUR rerun divergence — HALT"; exit 20; }
cmp -s /tmp/messy2_ctl_a.log /tmp/messy2_ctl_b.log || { echo "K2 FAIL: CTL rerun divergence — HALT"; exit 20; }
echo "K2: reruns byte-identical"

echo "=== [8/10] line counts (1280 G + 1280 EP per transcript)"
for t in cur_a ctl_a; do
  g=$(grep -c '^G,' /tmp/messy2_${t}.log)
  ep=$(grep -c '^EP,' /tmp/messy2_${t}.log)
  grun=$(grep -c '^GRUN,' /tmp/messy2_${t}.log)
  [ "$g" = "1280" ] || { echo "COUNT FAIL: $t G=$g"; exit 14; }
  [ "$ep" = "1280" ] || { echo "COUNT FAIL: $t EP=$ep"; exit 14; }
  [ "$grun" = "8" ] || { echo "COUNT FAIL: $t GRUN=$grun"; exit 14; }
done
echo "counts: 1280 G, 1280 EP, 8 GRUN per transcript"

echo "=== [9/10] K1 audit cap (independent awk max ≤4096)"
maxb=$(awk -F, '/^EP,/{if($5+0>m)m=$5} END{print m+0}' /tmp/messy2_cur_a.log /tmp/messy2_ctl_a.log)
[ "$maxb" -le 4096 ] || { echo "K1 FAIL: max episode bytes=$maxb — DEAD, HALT"; exit 21; }
echo "K1: max episode bytes=$maxb ≤ 4096"

echo "=== [10/10] independent checker"
awk -f check_messy2.awk /tmp/messy2_cur_a.log > /tmp/messy2_check_cur.log 2>&1 || { echo "CHECKER FAIL (CUR)"; tail -20 /tmp/messy2_check_cur.log; exit 30; }
awk -f check_messy2.awk /tmp/messy2_ctl_a.log > /tmp/messy2_check_ctl.log 2>&1 || { echo "CHECKER FAIL (CTL schedule)"; tail -20 /tmp/messy2_check_ctl.log; exit 30; }
tail -3 /tmp/messy2_check_cur.log
echo "ALL GATES PASS"
