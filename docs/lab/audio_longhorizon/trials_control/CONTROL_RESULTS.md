# CONTROL_RESULTS — Phase B2b §2b (real references)

## Headline (r1; r2/r3 byte-identical — see rerun_identity)

| Axis     | Hits / 40 | Hit rate | Bar (≥70%) | RC0 p (wired>severed) | RC1 deranged |
|----------|-----------|----------|------------|----------------------|--------------|
| Pitch    | 28/40     | 70.0%    | PASS       | p=1.9e-12 PASS       | 0.0% PASS    |
| Envelope | 39/40     | 97.5%    | PASS       | p=6.1e-10 PASS       | 0.0% PASS    |
| Prosody  | 29/40     | 72.5%    | **VOID**   | (pending)            | 27.5% **VOID** |

**Prosody scorer VOID**: RC1 deranged hit rate 27.5% (11/40) exceeds the 25% bar.
Per prereg, this voids the SCORER (not the trial). The 72.5% hit rate cannot be
certified as valid evidence. The ±25% CV hit criterion is insufficiently
discriminating for the prosody40 CV range (0.094–0.487); deranged pairs fall
within tolerance by chance.

§2b verdict: Pitch and envelope PASS with valid scorers. Prosody cannot be
claimed (scorer void). The "each ≥70%" bar is NOT fully met.

Hit criteria (frozen scorer_ctrl.py, SHA 7a4c232a1b96aa1a9a2b52a5b843c35a3c604c7c3f246ea2898ab8421e726224):
- pitch: |f0_ren − f0_ref| / f0_ref ≤ 5%
- env: scorer 3-class == ref 3-class
- prosody: |cv_ren − cv_ref| / cv_ref ≤ 25% (robust CV)

Pitch misses (12): indices 0,1,4,5,6,9,16,27,30,33,36,38 (0-based within axis).
Env miss (1): index 23.

RC1: frozen derangements (pitch shift-20, env shift-1, pros shift-20) yield 0%
hits — scorer valid (≤25% bar).

## Per-target tables
(pending — from analysis.json)

## Drift vs H1
(pending — H1 bars from Phase A; drift >5pp = DRIFT-FAIL)
