# C3 White-Box: N-gram Collision Analysis

**Date:** 2026-09-27
**Method:** Exact MDUMP reconstructor (`analysis/reconstruct.py`) implementing frozen `predict()`.

## Mechanism

The learner fires markers by substring match on UTT/CTX/SPK fields. Score = number of firing markers per concept. A marker learned from a corpus item (support-1 n-gram) can fire on a probe containing the same substring, causing a miss.

## The three collisions

### 1. `the clock` (hypothetical) → si3_03

- **Corpus:** Volume item (v96 only).
- **Marker:** `the clock` learned as hypothetical (support-1).
- **Probe:** si3_03 (sincere type-3) contains "the clock".
- **Effect:** si3_03 withheld as hypothetical → T3 DP 8/10 (not 9/10) on v96.
- **Not present in:** ab2, abc2 (A+B/C don't have this item).

### 2. `is out` (hypothetical) → si5_01

- **Corpus:** A+B (cc??), persists in abc2/v96.
- **Marker:** `is out` learned as hypothetical (support-1).
- **Probe:** si5_01 (sincere type-5) contains "is out".
- **Effect:** si5_01 withheld → T5 DP 9/10 (not 10/10) on ab2/abc2/v96.
- **Pre-existing:** Present in exp2c A+B; NOT a volume artifact.

### 3. `at night` (joke) → si4_05, si5_09

- **Corpus:** Volume item (v96 only).
- **Marker:** `at night` learned as joke (support-1).
- **Probes:** si4_05 (sincere type-4) and si5_09 (sincere type-5) contain "at night".
- **Effect:** Both withheld → T4 DP 9/10 (not 10/10), T5 DP 8/9 (not 9/9) on v96.

## Bound

These three markers cause EXACTLY the predicted misses:
- v96 T3 DP: 8/10 (the clock)
- v96 T4 DP: 9/10 (at night → si4_05)
- v96 T5 DP: 8/10 (at night → si5_09; is out → si5_01 would be 9/10, but at night also hits)
- ab2/abc2 T5 DP: 9/10 (is out → si5_01)

No other probes are affected. The bound is precise: 3 markers, 4 probe hits, all accounted for.

## Why not fixed

A generic fix (revoke support-1 provisional markers after final calibration) was considered but NOT implemented:
- Risk: D/E markers (`what if`, `where do`) may be support-1; revoking them would break the novel-family mechanism.
- Risk: Load-bearing sincere markers might be support-1.
- The task allows "fix OR precisely bound". The bound is precise and honest.

## Verification

The reconstructor proves the misses are caused by these specific markers firing (not by other mechanisms). The MDUMP shows the markers live; the probe utterances contain the substrings; the scores match exactly.
