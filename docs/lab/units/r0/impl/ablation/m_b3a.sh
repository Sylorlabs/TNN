#!/bin/bash
# m_b3a.sh — detached: B-T3 leg 0, perturbations 1..4 + repeat 0
# (p0 already captured as an evidence run). Resumable: skips perturbs whose
# .out already ends with BT3_DONE.
cd ~/workspace/tnn-lab/units/r0/impl/ablation || exit 9
BIN=~/workspace/scratch/bt3_bin
cp work/bt3_leg0_p0.txt evlogs/b_t3_leg0_p0.out
: > evlogs/b_t3_leg0_p0.err
for P in 1 2 3 4 0r; do
  OUT=evlogs/b_t3_leg0_p${P}.out
  if [ -f "$OUT" ] && [ "$(tail -1 "$OUT" 2>/dev/null)" = "BT3_DONE" ]; then
    echo "skip leg0 p$P (already complete)" >> evlogs/m_b3a.progress
    continue
  fi
  PA=$P; if [ "$P" = "0r" ]; then PA=0; fi
  "$BIN" 0 $PA >$OUT 2>evlogs/b_t3_leg0_p${P}.err
  echo "leg0 p$P rc=$?" >> evlogs/m_b3a.progress
done
# byte-identical check
BASE=evlogs/b_t3_leg0_p0.out
for P in 1 2 3 4 0r; do
  cmp -s "$BASE" evlogs/b_t3_leg0_p${P}.out || echo "DIFF stdout p$P" >> evlogs/m_b3a.progress
  cmp -s evlogs/b_t3_leg0_p0.err evlogs/b_t3_leg0_p${P}.err || echo "DIFF stderr p$P" >> evlogs/m_b3a.progress
done
echo DONE > evlogs/m_b3a.done
