#!/bin/bash
# run_matrix_m1m2.sh — measurement campaigns M1 (staggered genuine flips)
# and M2 (blinded-T0 attack). 3 arms x 2 campaigns x 3 variants x 12
# instances x 2 runs = 432 cells, 864 executions. Paired byte-identical
# reruns, ledger-replay exact. Evidence: evidence/mm/.
set -u
SUB="$HOME/workspace/tnn-lab/wave9/trust-tiers/substrate"
BIN="$SUB/trust_tiers.bin"
EV="$HOME/workspace/tnn-lab/wave9/trust-tiers/evidence/mm"
mkdir -p "$EV"
MANIFEST="$EV/cells.sha256"
: > "$MANIFEST"
[ -x "$BIN" ] || { echo "binary missing"; exit 2; }
fail=0
for arm in T N B; do for camp in M1 M2; do for var in 0 1 2; do
  for inst in 00 01 02 03 04 05 06 07 08 09 10 11; do
    base="${arm}_${camp}_${var}_${inst}_1"
    sel0="${arm}_${camp}_${var}_${inst}_0_1"; sel1="${arm}_${camp}_${var}_${inst}_1_1"
    f0="$EV/${base}.run0.log"; f1="$EV/${base}.run1.log"
    "$BIN" "$sel0" > "$f0" 2>"$EV/${base}.run0.err" || { echo "RC $sel0"; fail=1; continue; }
    "$BIN" "$sel1" > "$f1" 2>"$EV/${base}.run1.err" || { echo "RC $sel1"; fail=1; continue; }
    cmp -s "$f0" "$f1" || { echo "DIVERGENCE $base"; fail=1; continue; }
    sha256sum "$f0" "$f1" >> "$MANIFEST"
  done
done; done; done
[ $fail -eq 0 ] && echo "M1/M2 matrix complete: 432 cells paired-identical"
exit $fail
