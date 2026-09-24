# VERIFY — T2-SENSESH2H (independent re-verification)

**Re-verifier:** replacement coordinator (Wave-2 crossref), 2026-09-23 PDT.
**Frozen authority:** commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, `docs/lab/crossref/PREREG_TIER2.md`, section T2-SENSESH2H (extracted programmatically).
**Tier-2 crew verdict under test:** REPRODUCED (with RV2 kill questions).

## RV1 — frozen figures re-derived
- Evidence: `docs/lab/senses/rebuild/harness/results/metrics.json` (blob `9c0c376567af40a9a152bc394ea75b495362dd3c`, API-fetched, SHA-verified).
- A: 0.7263888889 → 72.6% PASS. B: 0.5402777778 → 54.0% FAIL. Gap: 18.611111pp.
- A memory: 79/134 = 58.9552%, 560 withholds. B memory: 72/131 = 54.9618%, 440 withholds.
- A ops: 1,034,699,124. B ops: 428,070,933. Ratio: 2.4171.
- Determinism: A 60/60, B 60/60 byte-identical.
- Independent rebuild: `sense_b` MD5 exactly `e6c98d091bbb0f90f54936b46bf849d8` ✓. `sense_a` rebuilt (88,191 bytes main, matches build record).

## RV2 — fresh frozen-before-use variants
**RT-EASY** (370 fixtures, streams base 300):
- A: 79.7%. B: 56.4%.
- Kill Q: Does B cross 60% on easier fixtures? **NO.** B remains below 60%.

**RT-HARD** (370 fixtures, streams base 400):
- A: 58.6%. B: 45.1%.
- Kill Q: Does A drop below 60% on harder fixtures? **YES.**
- A's PASS is NOT robust to harder fixtures. Breakdown: A colordisc 33.3%, pitchdisc 33.3%, motiondir 30.0%.

**RT-ADV2** (185 adversarial fixtures, streams base 500):
- A wrong: 101/185 (54.6%), mean conf wrong=449 vs right=489. High-conf(>700) wrong: 9/101.
- B wrong: 113/185 (61.1%), mean conf wrong=790 vs right=799. High-conf(>700) wrong: 77/113 (68%).
- Kill Q: Does adversarial false-install failure replicate? **YES.** B is highly confident even when wrong; A's confidence is better calibrated.

## Verdict: REPRODUCED with qualifications
RV1 figures re-derive exactly. RV2: B cannot cross 60% even on easier fixtures (FAIL robust); A's 72.6% PASS is fragile — drops to 58.6% (below bar) on harder fixtures. The adversarial install-rule failure replicates.
