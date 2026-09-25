#!/bin/bash
# K-DET: 3/3 byte-identical full-battery reruns for M4.
# Runs the subset checker over all 17 modules (12 plants + 5 clean),
# 3 times, saving certificates; compares run outputs byte-identically.
set -u
EVID=~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m4
BIN=$EVID/m4_subset
CFG=$EVID/config
MODULES="plants/P01_getrandom.zag plants/P02_clockgettime.zag plants/P03_urandom_path.zag plants/P04_uninit.zag plants/P05_envvar.zag plants/P06_aslr_leak.zag plants/P07_rdtsc.zag plants/P08_hashorder.zag plants/P09_innocent_tables.zag plants/P10_machineid.zag plants/P11_argv0.zag plants/P12_invoke_discard.zag clean/C01_canonical.zag clean/C02_state_phrasing.zag clean/C04_pinned_io.zag clean/C05_step_budget.zag clean/C06_fixed_order_map.zag"
for run in 1 2 3; do
  D=$EVID/certs/run$run
  mkdir -p "$D"
  for m in $MODULES; do
    base=$(basename "$m" .zag)
    "$BIN" "$EVID/$m" "$CFG" > "$D/$base.cert" 2>"$D/$base.err"
    echo "$? $base" >> "$D/exitcodes.txt"
  done
  (cd "$D" && sha256sum *.cert exitcodes.txt > SHA256SUMS)
done
echo "=== run digests ==="
sha256sum $EVID/certs/run1/SHA256SUMS $EVID/certs/run2/SHA256SUMS $EVID/certs/run3/SHA256SUMS
echo "=== pairwise cert-tree diff ==="
diff -r $EVID/certs/run1 $EVID/certs/run2 && echo "run1==run2 CERTS IDENTICAL"
diff -r $EVID/certs/run2 $EVID/certs/run3 && echo "run2==run3 CERTS IDENTICAL"
