#!/usr/bin/env bash
# H-2 Phase-3: build every battery cell + control, run each twice, cmp-check.
# Run from ~/workspace/threeworlds/h2/build/. Evidence -> ../evidence/.
set -u
ZNC=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
HERE=$(cd "$(dirname "$0")" && pwd)
EV=$HERE/../evidence
mkdir -p "$EV"
PASS=0; FAIL=0; FAILED=""
build_run() {
  local dir=$1 bin=$2 ev=$3
  echo "=== $ev ($dir) ==="
  ( cd "$dir" && "$ZNC" gl_learner.zag --no-zagd --no-analyze --no-foreground-cache -o "$bin" ) >"$EV/build_$ev.log" 2>&1
  if [ ! -x "$dir/$bin" ]; then echo "BUILD FAILED: $ev"; FAIL=$((FAIL+1)); FAILED="$FAILED $ev(build)"; return; fi
  ( cd "$dir" && ./"$bin" >"$EV/${ev}_run1.txt" 2>"$EV/${ev}_run1.err"; echo $? >"$EV/${ev}_rc1" )
  ( cd "$dir" && ./"$bin" >"$EV/${ev}_run2.txt" 2>"$EV/${ev}_run2.err"; echo $? >"$EV/${ev}_rc2" )
  local rc1=$(cat "$EV/${ev}_rc1") rc2=$(cat "$EV/${ev}_rc2")
  if [ "$rc1" != "0" ] || [ "$rc2" != "0" ]; then echo "NONZERO RC: $ev ($rc1/$rc2)"; FAIL=$((FAIL+1)); FAILED="$FAILED $ev(rc)"; return; fi
  if [ -s "$EV/${ev}_run1.err" ] || [ -s "$EV/${ev}_run2.err" ]; then echo "STDERR NONEMPTY: $ev"; FAIL=$((FAIL+1)); FAILED="$FAILED $ev(stderr)"; return; fi
  if cmp -s "$EV/${ev}_run1.txt" "$EV/${ev}_run2.txt"; then
    echo "OK: $ev byte-identical"
    PASS=$((PASS+1))
  else
    echo "DIVERGENCE: $ev"; FAIL=$((FAIL+1)); FAILED="$FAILED $ev(cmp)"
  fi
}
for cell in w1 w2h w2l w3a w3b w3ae rta18 rta20 rtd rte; do
  build_run "$HERE/battery/$cell" "rtbin_$cell" "$cell"
done
build_run "$HERE/controls/ctl_h" "rtbin_ctl_h" "ctl_h"
build_run "$HERE/controls/fid" "rtbin_fid" "fid"
# unpatched lying-silent control (Phase-2 build/ctl) re-run for the record
build_run "$HERE/ctl" "rtbin" "esc_ctl_B"
echo "----"
echo "PASS=$PASS FAIL=$FAIL"
[ -n "$FAILED" ] && echo "FAILED:$FAILED"
exit $FAIL
