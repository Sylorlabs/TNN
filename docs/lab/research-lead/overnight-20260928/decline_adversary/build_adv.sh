#!/bin/sh
# Build adversarial variant: splice gate with N threshold + driver
# Usage: ./build_adv.sh <N> <driver> <output>
# Example: ./build_adv.sh 3 adv_driver_reengage.zag adv_full_N3_reengage.zag
export PATH="$HOME/safebin"
N=$1
DRIVER=$2
OUTPUT=$3
DIR=~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/decline_adversary
cd $DIR
# Lines 1-812 (before ev_query)
head -812 adv_base.zag > $OUTPUT
# Gate with N
cat adv_gate_N$N.zag >> $OUTPUT
# Lines 836-1304 (after ev_query, before run_all test harness)
sed -n '836,1304p' adv_base.zag >> $OUTPUT
# Driver (has its own main)
cat $DRIVER >> $OUTPUT
echo "Built $OUTPUT with N=$N and driver $DRIVER"
wc -l $OUTPUT
