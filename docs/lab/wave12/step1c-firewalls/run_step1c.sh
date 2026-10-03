#!/bin/bash
# run_step1c.sh — Step 1c firewall build + kill-bar batteries.
# Fails loudly on any mismatch. Prereg: PREREG_FIREWALLS.md (frozen).
set -u
cd "$(dirname "$0")"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
FAIL=0
note(){ echo "STEP1C: $*"; }
die(){ echo "STEP1C FAIL: $*"; FAIL=1; }

MODS="fw_ledger.zag fw_judge.zag fw_refuse.zag fw_vary.zag fw_verdict.zag fw_run.zag fwmain.zag"

note "== static greps (no RNG/wall-clock/floats in firewall modules) =="
if grep -n "rand\|random\|[^a-z]rng\|srand\|gettime\|clock_gettime\|rdtsc" $MODS | grep -v "^.*://" ; then
  die "RNG/wall-clock token found"; else note "no RNG/wall-clock tokens"; fi
if grep -n "float\|f32\|f64\|double" $MODS | grep -v "^.*://"; then
  die "float token found"; else note "no float tokens"; fi
if grep -n "^[[:space:]]*//[[:space:]]*@import" $MODS fwgate.zag; then
  die "commented @import directive found"; else note "all @imports bare"; fi
for f in substrate/R33_NATIVE_SHA256_V2.zag substrate/R33_NATIVE_IO_V1.zag substrate/cl/common.zag; do
  [ -f "$f" ] || die "missing substrate $f";
done
note "substrate present"

note "== build fw_bin (twice: byte-identical rebuild check) =="
$ZNC fwmain.zag -o /tmp/fw_bin_b1 2>/tmp/build1.err || die "build1 failed"
$ZNC fwmain.zag -o /tmp/fw_bin_b2 2>/tmp/build2.err || die "build2 failed"
if cmp -s /tmp/fw_bin_b1 /tmp/fw_bin_b2; then note "rebuild byte-identical";
else die "rebuild NOT byte-identical"; fi
sha256sum /tmp/fw_bin_b1 | awk '{print $1}' > /tmp/fw_bin.sha
note "fw_bin sha256: $(cat /tmp/fw_bin.sha)"

note "== build fwgate_bin =="
$ZNC fwgate.zag -o /tmp/fwgate_bin 2>/tmp/buildg.err || die "gate build failed"
sha256sum /tmp/fwgate_bin | awk '{print $1}' > /tmp/fwgate_bin.sha
note "fwgate_bin sha256: $(cat /tmp/fwgate_bin.sha)"
cp /tmp/fw_bin_b1 /tmp/fw_bin

note "== BUILD GATE: fwgate clean (nonzero fails the build before trials) =="
/tmp/fwgate_bin clean $MODS > run_gate_clean.txt 2>&1 || die "gate flagged clean build"
tail -1 run_gate_clean.txt

note "== gate adversarial trial: 20 probes =="
/tmp/fwgate_bin probes probes/*.zag > run_gate_probes.txt 2>&1 || die "gate missed a probe"
grep -c "GATE_FILE.*viol,[1-9]" run_gate_probes.txt | grep -q "^20$" || die "probe count != 20"
tail -1 run_gate_probes.txt

for m in verdictinv tamper meminv refuseinv ledginv wiring replay; do
  note "== battery: $m =="
  /tmp/fw_bin $m > run_$m.txt 2>&1 || die "battery $m crashed"
  tail -4 run_$m.txt
done

note "== mechanical bar checks =="
chk(){ grep -q "$2" run_$1.txt || die "bar check failed: $1 expects $2"; }
chk verdictinv "CL_CHECK,verdict_cells,200,200"
chk verdictinv "CL_CHECK,verdict_cellfail,0,0"
chk tamper    "CL_CHECK,tamper_detected,5,5"
chk meminv    "CL_CHECK,meminv_cells,200,200"
chk meminv    "CL_CHECK,meminv_div,0,0"
chk meminv    "WATCH_LIVE,1"
chk refuseinv "CL_CHECK,refuse_cells,8,8"
chk refuseinv "CL_CHECK,refuse_vacuous,0,0"
chk refuseinv "CL_CHECK,refuse_k3bad,0,0"
chk ledginv   "CL_CHECK,led_pairs,200,200"
chk ledginv   "CL_CHECK,led_pairfail,0,0"
chk wiring    "CL_CHECK,wiring_cells,100,100"
chk wiring    "CL_CHECK,wiring_fail,0,0"
chk replay    "CL_CHECK,replay_cells,200,200"
note "all bar checks passed"

note "== determinism: rerun verdictinv, byte-compare =="
/tmp/fw_bin verdictinv > /tmp/re_det.txt 2>&1
if cmp -s run_verdictinv.txt /tmp/re_det.txt; then note "rerun byte-identical";
else die "rerun NOT byte-identical"; fi

note "== evidence hashes =="
{
  echo "fw_bin: $(cat /tmp/fw_bin.sha)"
  echo "fwgate_bin: $(cat /tmp/fwgate_bin.sha)"
  sha256sum $MODS fwgate.zag PREREG_FIREWALLS.md probes/*.zag run_*.txt
} > sha256sums.txt
cat sha256sums.txt | head -8

if [ "$FAIL" = "0" ]; then note "STEP1C ALL GREEN"; else note "STEP1C FAILURES PRESENT"; fi
exit $FAIL
