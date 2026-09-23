#!/bin/bash
# Curiosity-substrate trial runner. Compiles nothing (binary prebuilt);
# runs all four arms + a determinism repeat of the curiosity arm.
set -u
D="$(cd "$(dirname "$0")" && pwd)"
BIN="$D/curiosity_trial"
EVID="$D/evidence"; mkdir -p "$EVID"
fail=0
for m in 0 1 2 3; do
  "$BIN" "$m" > "$EVID/trace_mode$m.txt" 2>"$EVID/stderr_mode$m.txt"
  rc=$?
  echo "mode $m exit=$rc lines=$(wc -l < "$EVID/trace_mode$m.txt")"
  [ $rc -ne 0 ] && fail=1
done
# determinism repeat
"$BIN" 0 > "$EVID/trace_mode0_repeat.txt" 2>/dev/null
if cmp -s "$EVID/trace_mode0.txt" "$EVID/trace_mode0_repeat.txt"; then
  echo "determinism: IDENTICAL"
else
  echo "determinism: DIFFER"; fail=1
fi
grep -h "^MODE\|^PROBES\|^REGIME_FIRST_PROBE\|^NOISE_HALVES" "$EVID"/trace_mode*.txt | grep -v repeat
echo "fail=$fail"
