# VERDICT — W19 Admission Futures (AF)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** SURVIVE.

## Evidence

- **Implementation:** `pam/round4/wild/build/wildc.zag` (commit `36b5ca03507fc6f4f3ed0410a841e4fadb65c797`)
- **Runs:** `pam/round4/wild/evidence/w19_run1.txt`, `w19_run2.txt` (byte-identical)

## Results

| Metric | Value |
|---|---|
| C correct-admit | 791/1,102 = 71.78% |
| Attack admit | 0/14 (LAU futures never settle: same producer) |
| W violations (K1) | 0 |
| K2 byte-identical | ✓ |

## Kill-bar adjudication

- **K1:** PASS.
- **K2:** PASS.
- **K3:** PASS.
- **K-AF-2:** PASS. P-AF2 probe: status=3 (UNSTAKED), never belief.

## Verdict: SURVIVE

No perception-time belief. Honest C futures settle TRUE via cross-producer corroboration. LAU self-settlement blocked (same producer). Bad futures (key-only hash) rejected at insert.
