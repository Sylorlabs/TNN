# VERDICT.md - DEVANG6

Wave: wave-20261002-1121pdt. Lane: DEVANG (queue item 4: DEVANG6 with recalibrated K_ABL).
Owner: Micah. Mandate: make TNN create cognitive structure its programmers did not supply.

## Verdict: BUILD-FAIL

Killing bar: K_SEAL. Learner 9/20 < 12/20 on sealed Family C-tripleprime.

## Governing frozen bars (from PREREG_DEVANG6.md, commit bda385c32)

- K_ABL (recalibrated): (learner K_SEG - ablation K_SEG) >= 4 on sealed
  Family B; (learner K1 - ablation K1) >= 2 on Family A dev.
- K_SEG: learner >= 10/12 on sealed Family B-tripleprime.
- K_SEAL: learner >= 12/20 on sealed Family C-tripleprime.
- K_DISC: >= 5/6 on Family E-prime with frozen devang4 premise <= 2/6.
- K_SAME, K_AUD, K10, K11, K_C0, K8: as preregistered.

## Measured results (3/3 byte-identical sealed runs, zero stderr)

- K_ABL leg 1: learner 12/12, ablation 5/12, gap = 7 >= 4. PASS.
- K_ABL leg 2: learner K1 10/10, ablation 8/10, gap = 2 >= 2. PASS.
- K_SEG: 12/12 >= 10/12. PASS.
- K_SEAL: 9/20 < 12/20. FAIL. (Controls: c0 5/20, c2 11/20, c1 7/20, c3 7/20.)
- K_DISC: learner 6/6, premise 2/6. PASS.
- K_SAME: PASS (binary byte-identical to frozen DEVANG5 binary).
- K_AUD / K10 / K11: PASS (comments-only diff carry-forward).
- K_C0: 35pp. PASS. K8: 15pp. PASS.

## Classification

MECHANISM RESULT, not bar-miscalibration. The K_SEAL bar measures the right
quantity (fresh-vocabulary accuracy), was frozen before C-tripleprime existed,
and the learner <= fixed-3 pattern holds across all three C-families
(12v14, 14v14, 9v11), indicating a genuine capability gap: FINREG/POSSEG
provides no advantage on all-novel vocabulary. The bar is NOT re-tuned.

The recalibrated K_ABL is VALIDATED: it passes (gap 7 >= 4) on a fresh draw
with real margin, and the red team confirms it is stricter against vacuous
front-ends than the old bar. DEVANG6's contribution is the validated bar and
fresh measurements, not a mechanism (none was proposed; the binary is
byte-identical to DEVANG5's).

## Commit-order self-check

Prereg commit bda385c32 (2026-10-02 19:18:50 UTC) strictly precedes:
c72b40a54 (19:19:37), f541f16e3 (19:21:32), 1e852dbb2 (19:26:44). PASS.

## Commit ids

- 76361ff85: Step 0 toolchain guard.
- bda385c32: prereg + recalibration (ALONE).
- c72b40a54: E-prime baseline (premise 2/6 holds).
- f541f16e3: implementation (devang6.zag, byte-identical binary).
- 1e852dbb2: sealed package.
- (this commit): sealed eval, red team, debate, verdict, report, build log.

## Queued next

1. Multi-draw K_SEAL calibration study (the 12/20 bar sits near the observed
   mean of 12, 14, 9; single draws are noisy).
2. Independent-adversary replication of K_SEG / K_SEAL / K_ABL.
3. Investigate the learner's C-family deficit (never beats fixed-3 on novel
   vocabulary); determine whether FINREG can be extended or the base learner
   improved, without adding researcher-authored semantic cases.
4. Pinned znc now has FOUR documented miscompile patterns; assess toolchain
   fitness for sealed evaluation (governance question).
