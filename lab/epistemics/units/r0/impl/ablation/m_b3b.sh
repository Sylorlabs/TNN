#!/bin/bash
# m_b3b.sh — detached: B-T3 leg 1 full M8 matrix (p0..p4 + repeat 0), serial.
# Resumable via run_matrix.sh skip logic.
cd ~/workspace/tnn-lab/units/r0/impl/ablation || exit 9
./run_matrix.sh b_t3 1 ~/workspace/scratch/bt3_bin evlogs BT3_DONE >evlogs/m8_bt3_leg1.status 2>&1
echo "BT3_LEG1_RC=$?" >> evlogs/m8_bt3_leg1.status
echo DONE > evlogs/m_b3b.done
