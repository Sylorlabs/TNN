# PREREG P3 — ADAPTIVE-EPS: surprise-modulated exploration period

Status: PREREGISTERED + EXECUTED 2026-09-19 (3 seeds). See TRIAL_RESULTS.md.

## Hypothesis

R34's fixed 1/5 exploration wastes touches in stable regimes and
under-explores after regime switches. Modulating the exploration period by
surprise — shrink on negative reward, grow on positive — should raise training
positives and cut exploratory episodes with identical endpoints.

## Rule mechanics

- Exploration period `p`, init 5 (== R34's 1/5: explore when `rng % p == 0`).
- In `accept`, when `learn==1`: negative reward → `p = max(2, p−1)`;
  positive reward → `p = min(20, p+1)`.
- Everything else (additive ±100 scores, clamp, context recruitment) identical
  to R34. Integer math only.

## Predicted observable difference vs R34

- Higher trainA/trainB positives; fewer total exploratory episodes;
  evalA/evalB/returnA unchanged (16/16, 16/16, 15/16).

## Falsification criteria

- If exploratory count does not drop, or training positives do not improve,
  on a majority of seeds — reject.

## Outcome (executed)

**ACCEPTED.** 3/3 seeds: training positives strictly ≥ baseline
(A: 37/36/40 vs 35/35/36; B: 35/35/38 vs 33/30/34), exploratory episodes
strictly fewer (10/12/1 vs 16/19/13 — up to 92% fewer on seed 999),
endpoints identical (16/16, 16/16, 15/16). The period visibly adapts: long
stable runs push it toward 20 (seed 999: 0 explores in 40 trainA episodes,
40/40 positives), regime switches pull it back down.
**Promote P3 as the default exploration rule for Agent E's long-horizon runs.**
Caveat: in richer worlds exploration has information value beyond this
bandit's; re-examine if a future world rewards inquiry (see deferred
nonzero-UNKNOWN / curiosity wiring).

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

This document cites results that are **QUARANTINED**: R34's fixed 1/5 exploration (the hidden LCG stream that P3's init period reproduces).
The cited runs trained with `explore_enabled=1`, engaging a hidden seeded LCG
(`r34v3_rng` in `r34_learner_core.zag`) in the learner's action-choice path —
a violation of the no-randomness law (r34 RNG probe, workstream 2/8, commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE).
Treat the cited numbers as recorded-but-uncertified until clean reruns exist.
The original text above is left intact for the record.
