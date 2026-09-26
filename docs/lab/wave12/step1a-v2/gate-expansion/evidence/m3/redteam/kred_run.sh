#!/bin/bash
# kred_run.sh — K-RED operator run for M3 gate-expansion.
# Builds the 12 faithful instrumented rewrites (kred_*.zag) with the pinned
# toolchain, verifies stdout variance (validity), runs the A/B trace pair per
# run_battery.sh protocol (M3_FLAG=7, setarch -R, A=clean heap small environ,
# B=predirtied heap + 5000-byte M3_PAD), and feeds both traces + the kred map
# + the frozen allowlist to the frozen checker. No commits; working tree only.
set -u
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
HERE=~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m3/redteam
CHECKER=~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m3/checker/m3_checker
ALLOW=~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m3/m3_allowlist.txt
cd "$HERE"
mkdir -p runs traces checker_out
LOG=KRED_BUILD.log
: > "$LOG"
log() { echo "$@" | tee -a "$LOG"; }
sha256f() { sha256sum "$1" | cut -d' ' -f1; }

log "=== K-RED build+run log $(date -u +%FT%TZ) ==="
log "frozen tracer  : $(sha256f ../tracer/m3_tracer.zag)"
log "frozen checker : $(sha256f "$CHECKER")"
log "frozen allowlst: $(sha256f "$ALLOW")"
log "toolchain      : $(sha256f "$ZNC")"
log ""

build_plain() { # $1=src $2=out
  log "BUILD $1 -> runs/$2"
  if ! $ZNC "$1" -o "runs/$2" 2>"runs/$2.build.log"; then
    log "BUILD-FAIL $1"; tail -5 "runs/$2.build.log" | tee -a "$LOG"; return 1
  fi
  log "  src_sha=$(sha256f "$1")"
  log "  bin_sha=$(sha256f "runs/$2")"
  return 0
}
build_dyn() { # $1=src $2=out $3=libbase $4=shimsrc
  log "SHIM $4 -> runs/lib$3.so"
  if ! cc -shared -fPIC -o "runs/lib$3.so" "$4" 2>"runs/$3.shim.log"; then
    log "SHIM-FAIL $4"; return 1
  fi
  cp "runs/lib$3.so" "runs/lib$3.so.1"
  log "BUILD $1 -> runs/$2 (dynamic, needed lib$3.so.1)"
  if ! (cd runs && $ZNC "../$1" --dynamic --needed "lib$3.so.1" -o "$2" 2>"$2.build.log"); then
    log "BUILD-FAIL $1"; tail -5 "runs/$2.build.log" | tee -a "$LOG"; return 1
  fi
  log "  src_sha=$(sha256f "$1")"
  log "  shim_sha=$(sha256f "runs/lib$3.so")"
  log "  bin_sha=$(sha256f "runs/$2")"
  return 0
}

# ---- builds (manifest order r1..r12) ----
build_plain kred_a1.zag kred_a1   || exit 1
build_dyn   kred_a2.zag kred_a2 a2wall_kred a2_shim.c || exit 1
build_plain kred_a3.zag kred_a3   || exit 1
build_plain kred_b1.zag kred_b1   || exit 1
build_dyn   kred_b2.zag kred_b2 b2wall_kred b2_shim.c || exit 1
build_plain kred_b3.zag kred_b3   || exit 1
build_plain kred_c1.zag kred_c1   || exit 1
build_plain kred_c2.zag kred_c2   || exit 1
build_plain kred_c3.zag kred_c3   || exit 1
build_plain kred_d1.zag kred_d1   || exit 1
build_plain kred_d2.zag kred_d2   || exit 1
build_plain kred_d3.zag kred_d3   || exit 1
log ""
log "map SHAs:"
for p in a1 a2 a3 b1 b2 b3 c1 c2 c3 d1 d2 d3; do
  log "  maps/kred_$p.map $(sha256f "maps/kred_$p.map")"
done
log ""

# ---- validity: stdout must vary run-to-run (proves the rewrite kept the plant's entropy) ----
PAD="$(python3 -c 'print("P"*5000)')"
valid_ok=0; valid_bad=0
for spec in "a1:8:plain" "a2:8:dyn" "a3:16:plain" "b1:8:plain" "b2:8:dyn" "b3:8:plain" \
            "c1:16:plain" "c2:16:plain" "c3:8:plain" "d1:1000000:plain" "d2:8:plain" "d3:8:plain"; do
  p="${spec%%:*}"; rest="${spec#*:}"; exp="${rest%%:*}"; kind="${rest##*:}"
  pre=""
  if [ "$kind" = "dyn" ]; then pre="LD_LIBRARY_PATH=$HERE/runs"; fi
  # shellcheck disable=SC2086
  env M3_FLAG=7 $pre setarch -R "runs/kred_$p" "traces/kred_${p}_v1.trace" clean >"traces/kred_${p}_v1.out" 2>/dev/null; r1=$?
  env M3_FLAG=7 $pre setarch -R "runs/kred_$p" "traces/kred_${p}_v2.trace" clean >"traces/kred_${p}_v2.out" 2>/dev/null; r2=$?
  s1=$(sha256sum "traces/kred_${p}_v1.out" | cut -d' ' -f1)
  s2=$(sha256sum "traces/kred_${p}_v2.out" | cut -d' ' -f1)
  len=$(wc -c <"traces/kred_${p}_v1.out")
  if [ $r1 -ne 0 ] || [ $r2 -ne 0 ]; then log "VALID-FAIL kred_$p rc=$r1/$r2"; valid_bad=$((valid_bad+1)); continue; fi
  if [ "$len" -ne "$exp" ]; then log "VALID-FAIL kred_$p len=$len want=$exp"; valid_bad=$((valid_bad+1)); continue; fi
  if [ "$s1" = "$s2" ]; then log "VALID-FAIL kred_$p NOVAR (stdout identical across runs)"; valid_bad=$((valid_bad+1)); continue; fi
  log "VALID kred_$p len=$len sha1=${s1:0:16} sha2=${s2:0:16}"
  valid_ok=$((valid_ok+1))
done
log "validity: $valid_ok ok, $valid_bad bad"
log ""

# ---- A/B trace pairs + frozen checker ----
for spec in "a1:plain" "a2:dyn" "a3:plain" "b1:plain" "b2:dyn" "b3:plain" \
            "c1:plain" "c2:plain" "c3:plain" "d1:plain" "d2:plain" "d3:plain"; do
  p="${spec%%:*}"; kind="${spec##*:}"
  pre=""
  if [ "$kind" = "dyn" ]; then pre="LD_LIBRARY_PATH=$HERE/runs"; fi
  # shellcheck disable=SC2086
  env M3_FLAG=7 $pre setarch -R "runs/kred_$p" "traces/kred_${p}_A.trace" clean >/dev/null 2>&1; rca=$?
  env M3_FLAG=7 M3_PAD="$PAD" $pre setarch -R "runs/kred_$p" "traces/kred_${p}_B.trace" dirty >/dev/null 2>&1; rcb=$?
  out="$("$CHECKER" "traces/kred_${p}_A.trace" "traces/kred_${p}_B.trace" "maps/kred_$p.map" "$ALLOW" 2>&1)"
  c_rc=$?
  echo "$out" > "checker_out/kred_$p.check"
  verdict="$(echo "$out" | grep '^VERDICT' | head -1)"
  if [ -z "$verdict" ]; then verdict="(no VERDICT line; checker rc=$c_rc)"; fi
  log "kred_$p rc=$rca/$rcb traceA=$(wc -c <"traces/kred_${p}_A.trace")B traceB=$(wc -c <"traces/kred_${p}_B.trace")B :: $verdict"
done
log ""
log "=== done ==="
