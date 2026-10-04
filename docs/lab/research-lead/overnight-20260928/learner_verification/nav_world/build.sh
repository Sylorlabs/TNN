#!/bin/sh
# build.sh -- assemble, compile, and run the H-LVNAV-1 binary 3x.
# Pure Zag. Safebin PATH required. Follows the frozen PREREG kill bars.
export PATH="$HOME/safebin"
set -u
L=docs/lab/research-lead/overnight-20260928/learner_verification/nav_world
if [ "$(which python3 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python3 resolves in PATH"; exit 1
fi
if [ "$(which python 2>/dev/null)" != "" ]; then
  echo "GUARD-FAIL: python resolves in PATH"; exit 1
fi
echo "guard: python3/python absent, znc=$(which znc)"
cd "$HOME/workspace/tnn-rsi" || exit 1
cat "$L/lv_mech.zag" "$L/lv_main.zag" > "$L/lv_full.zag"
echo "--- kill-bar source audits (frozen prereg) ---"
echo "K3a harness-key tokens in mech (want 0): $(grep -c 'hv_expected\|ht_expected' "$L/lv_mech.zag")"
echo "K3b harness-key tokens in driver (want >0): $(grep -c 'hv_expected\|ht_expected' "$L/lv_main.zag")"
echo "K3c direct world-state writes in mech (want only world_* fns):"
grep -n 'set32(E' "$L/lv_mech.zag"
echo "K3d direct world-state writes in driver (want 0): $(grep -c 'set32(E' "$L/lv_main.zag")"
echo "K8 modes/bridges/handlers tokens (want 0): $(grep -ci 'mode\|bridge\|handler' "$L/lv_mech.zag" "$L/lv_main.zag")"
echo "--- compile ---"
znc "$L/lv_full.zag" -o "$L/lv_bin" > "$L/compile.txt" 2>&1
echo "compile exit=$?"
ls -la "$L/lv_bin"
echo "--- run 3x ---"
for r in 1 2 3; do
  "$L/lv_bin" > "$L/run$r.txt" 2>&1
  echo "run$r exit=$?"
done
sha256sum "$L/run1.txt" "$L/run2.txt" "$L/run3.txt" | tee "$L/sha256sums.txt"
cmp "$L/run1.txt" "$L/run2.txt" && cmp "$L/run2.txt" "$L/run3.txt" && echo "DETERMINISM-OK: 3/3 byte-identical"
echo "BUILD-DONE"
