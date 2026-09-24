# VERDICT — W22 Two-Phase Commit (TPC)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** SURVIVE.

## Evidence

- **Implementation:** `pam/round4/wild/build/wildc.zag` (commit `36b5ca03507fc6f4f3ed0410a841e4fadb65c797`)
- **Runs:** `pam/round4/wild/evidence/w22_run1.txt`, `w22_run2.txt` (byte-identical)
- **Probes:** `w22_probe1.txt` (P-TPC2 DivergenceRec emitted)

## Results

| Metric | Value |
|---|---|
| C correct-admit | 791/1,102 = 71.78% |
| Attack commit | 0/14 (LAU slow=0, FRK fast=0, FRG slow=0) |
| W violations (K1) | 0 |
| Divergences on tape | 4 (LAU slow=0) |
| K2 byte-identical | ✓ |

## Kill-bar adjudication

- **K1:** PASS.
- **K2:** PASS.
- **K3:** PASS.
- **K-TPC-1:** PASS. No commit with slow=0 or hash mismatch (OUT carries fast,slow,hf,hs; scorer verified).
- **K-TPC-2:** PASS. P-TPC2 emits DivergenceRec (flip=1 → hf≠hs).
- **K-TPC-3:** PASS. 14/14 kept out > C3-only 0/14.
- **K-TPC-4:** PASS. Slow path uses binary-searched indexes only; no scan of prior intents (code review).

## Verdict: SURVIVE

Two-phase commit prevents unilateral belief. Fault injection caught. All attacks kept out.
