#!/bin/bash
# m_b2.sh — detached: B-T2 full M8 matrix, both legs, serial.
cd ~/workspace/tnn-lab/units/r0/impl/ablation || exit 9
./run_matrix.sh b_t2 0 ~/workspace/scratch/bt2_bin evlogs >evlogs/m8_bt2_leg0.status 2>&1
echo "BT2_LEG0_RC=$?" >> evlogs/m8_bt2_leg0.status
./run_matrix.sh b_t2 1 ~/workspace/scratch/bt2_bin evlogs >evlogs/m8_bt2_leg1.status 2>&1
echo "BT2_LEG1_RC=$?" >> evlogs/m8_bt2_leg1.status
echo DONE > evlogs/m_b2.done
