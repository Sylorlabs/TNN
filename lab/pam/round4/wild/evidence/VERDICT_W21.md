# VERDICT — W21 Deterministic Immune Repertoire (DIR)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** SURVIVE.

## Evidence

- **Implementation:** `pam/round4/wild/build/wildc.zag` (commit `36b5ca03507fc6f4f3ed0410a841e4fadb65c797`)
- **Runs:** `pam/round4/wild/evidence/w21_run1.txt`, `w21_run2.txt` (byte-identical)
- **Probes:** `w21_probe1.txt` (P-DIR5 rid=1, 8/8 anchors pass)

## Results

| Metric | Value |
|---|---|
| C correct-admit | 791/1,102 = 71.78% |
| Attack veto | 14/14 (LAU→r2, FRK→r3, FRG→r1) |
| W violations (K1) | 0 |
| K2 byte-identical | ✓ |

## Kill-bar adjudication

- **K1:** PASS.
- **K2:** PASS.
- **K3:** PASS.
- **K-DIR-1:** PASS. Every dec=1 has veto=0 ∧ c3=1 (scorer verified).
- **K-DIR-2:** PASS. Receptors are five compiled constants (masks: b6, b0|b2, b10, !b7, b11); extractor reads producer rows/bytes only.
- **K-DIR-3:** PASS. 14/14 > C3-only 0/14.
- **K-DIR-4:** PASS. 8/8 benign anchors not vetoed.
- **K-DIR-5:** PASS. P-DIR5 logged with receptor_id=1 (lowest of {1,2}).

## Verdict: SURVIVE

Five compiled receptors veto all attacks, nothing else. Maturation OFF (no code path). Honest traffic unaffected.
