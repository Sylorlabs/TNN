#!/bin/bash
# B-303134 battery runner: every mode x3 runs, SHA-256 compare.
D=~/workspace/tnn-lab/senses/pam-rebuild/round2/b303134
R=$D/runs
declare -A MODES
MODES[drive30_bin]="honest rf_coarse rf_full rc_full xr_fresh xr_reuse n30 o30t o30n p30 j30 l30"
MODES[drive31_bin]="honest sl if readmit n31 o31t p31 j31 k31"
MODES[drive34_bin]="honest rcrf_coarse rcrf_full ge_closed ge_open if_window n34 o34t o34n p34 j34 m34 l34"
> $R/SHA256SUMS
for bin in drive30_bin drive31_bin drive34_bin; do
  drv=${bin%_bin}
  for m in ${MODES[$bin]}; do
    for r in 1 2 3; do
      $D/$bin $m > $R/${drv}_${m}_run${r}.out 2>&1 || echo "RUNFAIL $drv $m run$r"
    done
    s1=$(sha256sum $R/${drv}_${m}_run1.out | cut -d' ' -f1)
    s2=$(sha256sum $R/${drv}_${m}_run2.out | cut -d' ' -f1)
    s3=$(sha256sum $R/${drv}_${m}_run3.out | cut -d' ' -f1)
    if [ "$s1" = "$s2" ] && [ "$s2" = "$s3" ]; then st="IDENTICAL"; else st="DIVERGED"; fi
    echo "${drv}_${m} $s1 $st"
    echo "$s1  ${drv}_${m}_run1.out" >> $R/SHA256SUMS
  done
done
