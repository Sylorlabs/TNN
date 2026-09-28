# VERDICT R2-13 — FS-F "Signature-Ceiling Falsifier"

**Fork:** R2-13 / FS-F
**Date:** 2026-09-23
**Verdict:** **DEAD**

## Prereg compliance

- Original prereg: `PREREG_R2-13.md` (committed `a809feef45f1301f8fdd67c42488d9c17aa579ed`)
- Amendment A1: `PREREG_R2-13_AMEND_A1.md` (committed `1995e605889ca0fe8b5e1bf60770361334c703aa`) —
  superseded, noncompliant (N=10,425; ablation unchanged).
- Amendment A2: `PREREG_R2-13_AMEND_A2.md` (committed `12c6543a2c8e552128d2563a3a8d853ee0d13318`) —
  **authoritative**. Freezes exact N=10,000 manifest
  (SHA `797e0e44facd1e215ee3b4a501d73eadad5cb2f110d9f16845b38b0d42f999f9`)
  and the same-contract attack-clauses-removed ablation. Committed alone
  before any valid battery.

## Method

Pure-Zag binary `fsf` (zero RNG, integer math, deterministic). Two-sided
relational-signature contract: INSTALL iff `dt + 150 < df` where `dt` is the
distance to the nearest true exemplar and `df` the distance to the nearest
false-bank entry (margin 150). Attack-aware features rebuilt against the
three design collision families (TMB-2 harmonic boost, SHP-1 occlusion bar,
MOT-1 reversed video). False bank: 12 entries (4 per design family, lowest
r2a indices).

Batteries run twice over the exact-10,000 manifest; ledgers byte-identical
(`cmp`); hash chains independently verified.

## Results

### Bar 1: ≤1% false installs on exactly 10,000 adversarial trials

| Run | False installs | Rate | Bar | Result |
|-----|---------------|------|-----|--------|
| A   | 3,709 / 10,000 | 37.09% | ≤1% | **FAIL** |
| B   | 3,709 / 10,000 | 37.09% | ≤1% | **FAIL** |

### Bar 2: novel-family holdout (6 families; ≤2% each, ≤1% pooled)

| Family | False installs | Rate | Bar | Result |
|--------|---------------|------|-----|--------|
| COL-1 (colordisc/1) | 810 / 810 | 100.00% | ≤2% | **FAIL** |
| COL-2 (colordisc/2) | 60 / 710 | 8.45% | ≤2% | **FAIL** |
| CCN-1 (colorconst/1) | 140 / 690 | 20.29% | ≤2% | **FAIL** |
| PTC-1 (pitchdisc/1) | 475 / 710 | 66.90% | ≤2% | **FAIL** |
| TMB-1 (timbredisc/1) | 87 / 438 | 19.86% | ≤2% | **FAIL** |
| SHP-3 (shapetrans/3) | 39 / 398 | 9.80% | ≤2% | **FAIL** |
| **Pooled** | **1,611 / 3,756** | **42.89%** | ≤1% | **FAIL** |

### Bar 3: same-contract ablation on design families (≥50% cut)

| Variant | Design-family false installs | Rate | Cut vs ablation |
|---------|------------------------------|------|-----------------|
| FULL | 8 / 1,663 | 0.48% | — |
| Ablation (noclause) | 8 / 1,663 | 0.48% | 0% (**FAIL**; bar requires ≥50%) |

The attack-specific clauses produced zero change on the design families:
the refined features did not do the work. Bar 3 fails.

## Determinism

- Run A vs Run B ledgers: `cmp` → **byte-identical**.
- Hash chains: 0 bad (run A), 0 bad (run B), 0 bad (ablation).
- Final chain (A=B): `783e7dcce354fc4ad4540a2c3e4c506ecd60c270374da0afa778c3804866a215`

## Verdict rationale

Dies on all three bars:
- **Bar 1:** 37.09% vs ≤1%.
- **Bar 2:** all six holdouts exceed 2% per-family; pooled 42.89% vs ≤1%.
- **Bar 3:** 0% cut vs ≥50% required — the attack-aware clauses were
  ineffective even on their design families.

Per Debate D §7, bar 3's failure means the holdout failure cannot be cleanly
attributed to "the property is the ceiling" — the engineering did not do the
work either. The fork is DEAD regardless: the signature contract with
attack-aware features does not approach the 1% bar.
