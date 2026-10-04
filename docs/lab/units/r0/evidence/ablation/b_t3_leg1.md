# B-T3 dose curve — leg 1 evidence (crew B-ABLDOSE)

Prereg: R0 §2 R0.1 battery 3 (dose curve). Manifest:
`docs/lab/units/r0/evidence/ablation/MANIFEST_BT2_BT3.md` (frozen pre-execution).
Binary `b_t3.zag`, pure Zag, seed 20260921 (environment inputs only).
Expected-value readback probe: `BT_PROBE,fails=0`. Golden mini-run passed
inside the binary. Fresh arena per dose; nested prefixes of the deterministic
unit schedule. Leg 1: re-derived parameters.

## Dose table (dual_active hard-grounding score, /1000)

| dose | dual | raw | chunk | promoted | live | ratio (/1000) | ledger |
|---|---|---|---|---|---|---|---|
[('0', 'baseline'), ('1', 'heap pre-fragmentation'), ('2', 'held 64KiB ASLR-equivalent offset'), ('3', 'entropy/clock canary'), ('4', 'free-list reversal + mid-run churn'), ('0r', 'repeat baseline')]

- Adjacent-dose monotonicity: strict_nondecreasing=1,
  max adjacent drop=0/1000.
- R-4 formal degradation tolerance: **PENDING-MICAH-AMENDMENT**
  (proposed ≤ 25/1000 adjacent drop).
- Descriptive verdict: **PASS**

## M8 adversarial-allocation battery (N=5 + repeated baseline)

| perturb | mode | rc |
|---|---|---|
| 0 | baseline | 0 |
| 1 | heap pre-fragmentation | 0 |
| 2 | held 64KiB ASLR-equivalent offset | 0 |
| 3 | entropy/clock canary | 0 |
| 4 | free-list reversal + mid-run churn | 0 |
| 0r | repeat baseline | 0 |

stdout/stderr byte-identical across all 6 runs: YES (sha256-verified by the evidence generator). Runner attestation: M8_IDENTICAL + _RC=0 in runner status.
Expected-readback probe + golden mini-run passed in every invocation.
