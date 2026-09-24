# PREREG AMENDMENT 1 — 2D attention grid for image/video

**Date:** 2026-09-24 (before any formal G2 run; calibration only)
**Reason:** Mathematical degeneracy in the frozen 1D offset formula.

The frozen PREREG §2b specifies `off[k] = ((2*k+1)*N)/128` for N>=64.
For 2D fixtures this is degenerate:
- COL (128×64, N=8192): off = (2k+1)*64 → x = off%128 = 64 for ALL k.
  All 64 patches center on the half-boundary; left half gets zero patches,
  so the colordisc/colorconst half-distance feature is undefined (returns -1).
- Video (64×64, N=4096): off = (2k+1)*32 → x = 32 for ALL k. Same degeneracy.
- Shape (96×96, N=9216): off = (2k+1)*72 → x = 72*(odd) % 96 cycles 72,24 —
  only 2 distinct columns. Degenerate.

Audio (1D, N=16000) is NOT degenerate: offsets 125,375,…,15875, spaced 250.

**Amendment (frozen):** The 1D formula is kept for audio (tcode 3,4).
For image/video (tcode 0,1,2,5), the 64 offsets are the 8×8 uniformly-spaced
grid midpoints, which is the 2D meaning of the task's "uniformly spaced":
  for k in 0..63: gx = k%8, gy = k/8;
    x = ((2*gx+1)*w)/16, y = ((2*gy+1)*h)/16.
This depends only on raw (w,h) geometry — never judgment/confidence/margin —
and is stable under span-edit (geometry preserved). Neighborhoods unchanged
(5×5 patches). The hypothesis, install rule, kill bars, and determinism rules
are UNCHANGED.

**Consequence:** organ2.zag's image/video offset computation uses the grid;
calibration is re-run for colordisc/colorconst with the corrected map.
Timbredisc calibration (audio, unaffected) stands: B1=2,B2=77,B3=267,
train ACC=89.2% on N=690.
