# VERDICT — W17 Corroboration Codec (CC)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** SURVIVE.

## Evidence

- **Implementation:** `pam/round4/wild/build/wildc.zag` (commit `36b5ca03507fc6f4f3ed0410a841e4fadb65c797`)
- **Runs:** `pam/round4/wild/evidence/w17_run1.txt`, `w17_run2.txt` (byte-identical)

## Results

| Metric | Value |
|---|---|
| C correct-admit | 791/1,102 = 71.78% |
| Attack admit | 0/14 (all quarantined: single producer) |
| W violations (K1) | 0 |
| K2 byte-identical | ✓ |

## Kill-bar adjudication

- **K1:** PASS.
- **K2:** PASS.
- **K3:** PASS. 71.78% in band.
- **K-CC-5:** PASS. P-CC5 probe: dec=0, card=1 (quarantined).
- **K-CC-4:** (attack catch vs C3-only) 14/14 kept out > 0/14.

## Verdict: SURVIVE

Belief requires ≥2 distinct non-GEN EXT producers. Honest C rows corroborate across producers 1/2/10. Attacks (single producer each) remain quarantined.
