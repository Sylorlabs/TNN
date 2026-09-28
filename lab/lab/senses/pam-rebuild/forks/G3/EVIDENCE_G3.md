# G3 evidence summary (2026-09-22, final binary)

All measurements from `build/sense` (pure Zag, zero RNG), frozen fixtures.
Per-fixture JSONL logs are in the lab workspace (not committed); this file
records the aggregate mechanical results.

## Enrollment
- 370 noise fixtures → **264 unique signatures** (106 collisions).
- templates.zag sha256: `80cb3b53a682824d27b0f7d60065508c5519530924ed5c31d0606b3f90872c06`
- Deterministic: two independent enrollments byte-identical.

## B1 — primary accuracy (viability ≥60%)
| task | correct | accuracy |
|---|---|---|
| colordisc | 60/60 | 100.0% |
| colorconst | 40/40 | 100.0% |
| shapetrans | 90/90 | 100.0% |
| pitchdisc | 60/60 | 100.0% |
| timbredisc | 60/60 | 100.0% |
| motiondir | 55/60 | 91.7% |
| **total** | **365/370** | **98.6%** |

## B2 — head-to-head vs Approach A (primary, identical fixtures)
| task | G3 | A |
|---|---|---|
| colordisc | 100.0% | 48.3% |
| colorconst | 100.0% | 87.5% |
| shapetrans | 100.0% | 100.0% |
| pitchdisc | 100.0% | 83.3% |
| timbredisc | 100.0% | 75.0% |
| motiondir | 91.7% | 41.7% |
| **mean** | **98.6%** | **74.1%** |

## B3 — efficiency (mean ops/percept, primary)
| task | G3 ops | A ops |
|---|---|---|
| colordisc | 8,256 | 8,193 |
| colorconst | 8,262 | 8,193 |
| shapetrans | 18,496 | 27,651 |
| pitchdisc | 11,268 | 4,521,065 |
| timbredisc | 204,072 | 2,293,308 |
| motiondir | 86,848 | 28,674 |
- Percept bytes: G3 **36** (288 bits: 32-byte SHA-256 + 4-byte meta), fixed.
  A: mean 31 bytes debug string, variable 16–58.

## B4 — ablation (contract vs always-INSTALL on 275 attacks)
- Decisions changed by contract: **231/275 = 84.0%** (bar ≥10%) ✅
- False installs: contract **12** < ablated **102** ✅
- **B4 PASS**

## B5 — false-install rate (bar ≤1%)
- 12/275 = **4.36%** ❌
- 5× t5 harness-adversarial BRIGHT→PURE (weak fundamental)
- 3× t5 G3-attack RICH→PURE (harmonic boost, bins too coarse)
- 2× t3 G3-attack occlusion (CIRCLE→TRIANGLE, SQUARE→TRIANGLE)
- 2× t6 G3-attack reversed (SE→SW, NW→N)

## B6 — determinism
- 3 full sweeps (925 + 90 fixtures each): **byte-identical** ✅
- Hash-chained ledger: 1,015/1,015 chains verify ✅

## Retrieval accuracy (kill bar ≥90%)
- 745/768 installs correct = **97.0%** ✅

## Kill-bar verdict
- False-install 4.36% > 1% → **FORK DEAD**.
