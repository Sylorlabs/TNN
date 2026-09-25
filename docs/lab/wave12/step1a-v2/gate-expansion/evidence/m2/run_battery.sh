#!/bin/bash
# Run the full M2 battery: one driver invocation (18 schedule runs) per module.
# Usage: run_battery.sh <round>   (round = r1|r2|r3 for K-DET)
set -u
E2M=~/workspace/tnn-lab/wave12/step1a-v2/gate-expansion/evidence/m2
DRV=$E2M/build/driver/m2_driver
R=$1
OUT=$E2M/runs/$R
mkdir -p $OUT
MODULES="p01_getrandom p02_clock p03_urandom p04_uninit p05_envflag p06_aslr p07_rdtsc p08_hashorder p09_innocent_tables p10_machineid p11_argv p12_invoke_discard c01_clean c02_phrasing c03_seeded c04_fileio c05_instrcount c06_fixedmap"
for m in $MODULES; do
    mkdir -p $OUT/$m
    case $m in
        p10_machineid|p11_argv)
            $DRV $E2M/build/mod/$m $OUT/$m $m 1 $E2M/fixtures/state.bin $E2M/fixtures/input.bin > $OUT/$m.driver.log 2>&1 ;;
        c04_fileio)
            $DRV $E2M/build/mod/$m $OUT/$m $m 2 $E2M/fixtures/c04_data.bin > $OUT/$m.driver.log 2>&1 ;;
        *)
            $DRV $E2M/build/mod/$m $OUT/$m $m 0 > $OUT/$m.driver.log 2>&1 ;;
    esac
    echo "$m rc=$? $(grep M2-VERDICT $OUT/$m.driver.log)"
done
echo "ROUND $R DONE"
