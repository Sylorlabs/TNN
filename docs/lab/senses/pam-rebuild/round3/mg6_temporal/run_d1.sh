#!/bin/bash
# run_d1.sh — run the D1 battery (r3_main) 3x, one invocation per stream.
set -e
cd "$(dirname "$0")/src"
STREAMS="leg1 leg2 leg3_C1 leg3_C2 leg3_C3 leg3_R1 leg3_R2 leg3_CC1 leg3_CC2 leg3_H1 leg3_T1 leg3_W1 leg4_clean leg4_withhold leg4_install leg4_decoy"
for run in 1 2 3; do
  out="../evidence/d1_run${run}.txt"
  : > "$out"
  for s in $STREAMS; do
    ./r3_main "$s" >> "$out"
  done
  echo "run$run: $(wc -l < "$out") lines"
done
sha256sum ../evidence/d1_run*.txt
