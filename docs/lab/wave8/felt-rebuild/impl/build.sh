#!/bin/bash
# FELT-V3 build: static checks -> compile (no trial run).
# Usage: ./build.sh            (trial binary; requires CALIBRATION_RECORD.md)
#        ./build.sh --calib    (calibration-capable binary; needs only the
#                               placeholder calib_consts.zag; used to produce
#                               CALIBRATION_RECORD.md the first time)
set -u
D="$(cd "$(dirname "$0")" && pwd)"
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
W5=~/workspace/tnn-lab/wave5/strength-trial-run/trial
fail(){ echo "BUILD_FAIL,$1"; exit 1; }
cd "$D" || exit 1

echo "== static checks =="
# 1. I-7: substrate byte-identical to wave-5 source
cmp -s st_memory_core.zag "$W5/st_memory_core.zag" || fail "st_memory_core.zag differs from wave-5"
cmp -s substrate/cl/common.zag "$W5/substrate/cl/common.zag" || fail "common.zag differs from wave-5"
cmp -s substrate/R33_NATIVE_SHA256_V2.zag "$W5/substrate/R33_NATIVE_SHA256_V2.zag" || fail "sha256 differs"
cmp -s substrate/R33_NATIVE_IO_V1.zag "$W5/substrate/R33_NATIVE_IO_V1.zag" || fail "nativeio differs"
# 2. I-4: no RNG tokens (case-insensitive) in felt module, driver, substrate
grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc|shuffle|seed\(' \
  felt_v3.zag felt_trial_v3.zag calib_consts.zag st_memory_core.zag substrate/ >/dev/null 2>&1 \
  && fail "RNG token found"
# 3. bare @import (not commented)
grep -q '^@import' felt_v3.zag || fail "felt_v3.zag import not bare"
grep -q '^@import' felt_trial_v3.zag || fail "felt_trial_v3.zag import not bare"
# 4. I-5: no strength write outside the substrate's four lawful ops
if grep -nE 'st_str\[[^]]*\]\s*=' felt_v3.zag felt_trial_v3.zag | grep -v 'st_i32' >/dev/null 2>&1; then
  fail "direct st_str write outside substrate API"
fi
grep -niE 'st_write_strength|st_clear_strength|r_param' felt_v3.zag felt_trial_v3.zag \
  >/dev/null 2>&1 && fail "forbidden strength/R_PARAM token"
# 5. P1b: no learner/judgment path emits observations.
#    felt_emit_obs may appear only in driver emit_* fns + calibration + the
#    felt module definition itself.
python3 - "$D" <<'EOF' || fail "P1b observation-emitter scope"
import re,sys
D=sys.argv[1]
allowed_defs={"emit_contra","emit_corrob","emit_probe","emit_mark","run_calibration"}
for fn in ("felt_trial_v3.zag",):
    src=open(f"{D}/{fn}").read()
    cur=None
    for i,line in enumerate(src.splitlines(),1):
        m=re.match(r'\s*fn\s+([A-Za-z0-9_]+)\(',line)
        if m: cur=m.group(1)
        if "felt_emit_obs(" in line and cur not in allowed_defs:
            print(f"P1b violation: felt_emit_obs in {cur} ({fn}:{i})"); sys.exit(1)
print("P1b_OK")
EOF
# 6. lawful read sites: do_read only in the three §4 judgment sites
#    (invest, sacrifice, weaken) plus the frozen H1 ascending-I triage ordering
python3 - "$D" <<'EOF' || fail "read-site scope"
import re,sys
D=sys.argv[1]
allowed={"site1_f","gate2_f","revision_sweep","pick_victim_f"}
src=open(f"{D}/felt_trial_v3.zag").read()
cur=None; n=0
for i,line in enumerate(src.splitlines(),1):
    m=re.match(r'\s*fn\s+([A-Za-z0-9_]+)\(',line)
    if m: cur=m.group(1)
    if re.search(r'(?<![A-Za-z0-9_])do_read\(w,st,',line):
        n+=1
        if cur not in allowed:
            print(f"read-site violation: do_read in {cur} ({i})"); sys.exit(1)
if n!=4:
    print(f"do_read call sites = {n}, expected 4"); sys.exit(1)
print("READSITES_OK")
EOF
# 7. frozen curriculum formulas present verbatim
grep -q 'm%10)<3' felt_trial_v3.zag || fail "imp formula changed"
grep -q '(m+3)%10)<3' felt_trial_v3.zag || fail "wrong formula changed"
grep -q '(m%10==4||m%10==5||m%10==7)' felt_trial_v3.zag || fail "designation formula changed"
grep -q '(m+v)%5==0' felt_trial_v3.zag || fail "probe formula changed"
# 8. I-8: calibration record exists and trial constants match it
if [ "${1:-}" = "--calib" ]; then
  grep -q 'TEMPORARY PLACEHOLDER' calib_consts.zag || fail "placeholder marker missing"
  echo "STATIC_OK (calibration build; placeholder consts)"
else
  [ -f CALIBRATION_RECORD.md ] || fail "CALIBRATION_RECORD.md missing"
  for sym in CAL_ALPHA CAL_BETA CAL_GAMMA; do
    rec=$(grep -E "^${sym}=" CALIBRATION_RECORD.md | head -1 | cut -d= -f2)
    src=$(grep -E "const ${sym}:i32=" calib_consts.zag | head -1 | sed 's/.*=//;s/;.*//')
    [ -n "$rec" ] || fail "$sym missing in record"
    [ "$rec" = "$src" ] || fail "I-8: $sym trial($src) != record($rec)"
  done
  echo "STATIC_OK"
fi

echo "== compile =="
"$ZNC" felt_trial_v3.zag --no-zagd --no-analyze --no-foreground-cache -o felt_trial_v3_bin \
  || fail "compile"
echo "COMPILE_OK"
