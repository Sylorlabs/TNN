# SENSES REBUILD — Harness results

Generated: 2026-09-22T00:07:56 (harness crew)
Approach A = raw values (`a_raw/sense`), Approach B = qualitative percepts (`b_percept/sense`).
Runner errors (missing keys / bad vocab / nonzero exit): 1

## 1. Primary-fixture accuracy per task

| task | A acc | B acc | Δ (B−A) | A n | B n |
|---|---|---|---|---|---|
| color discrimination | 48.3% | 40.0% | -8.3pp | 60 | 60 |
| color constancy | 87.5% | 62.5% | -25.0pp | 40 | 40 |
| shape transform | 100.0% | 40.0% | -60.0pp | 90 | 90 |
| pitch discrimination | 83.3% | 78.3% | -5.0pp | 60 | 60 |
| timbre discrimination | 75.0% | 75.0% | +0.0pp | 60 | 60 |
| motion direction | 41.7% | 28.3% | -13.3pp | 60 | 60 |
| **mean (equal weights)** | **72.6%** | **54.0%** | **-18.6pp** | | |

## 2. Instrumented ops (element-visit grain)

| task | A ops | B ops | ratio B/A |
|---|---|---|---|
| color discrimination | 1228950 | 1228950 | 1.00× |
| color constancy | 819300 | 1280100 | 1.56× |
| shape transform | 6193824 | 2219883 | 0.36× |
| pitch discrimination | 678159750 | 215296950 | 0.32× |
| timbre discrimination | 343996200 | 203744250 | 0.59× |
| motion direction | 4301100 | 4300800 | 1.00× |
| **total** | **1034699124** | **428070933** | **0.41×** |

## 3. Robustness: noise and adversarial accuracy

### noise fixtures (deterministic precomputed noise)

| task | A | B | A n | B n |
|---|---|---|---|---|
| color discrimination | 48.3% | 41.7% | 60 | 60 |
| color constancy | 80.0% | 62.5% | 40 | 40 |
| shape transform | 100.0% | 36.7% | 90 | 90 |
| pitch discrimination | 83.3% | 78.3% | 60 | 60 |
| timbre discrimination | 75.0% | 75.0% | 60 | 60 |
| motion direction | 43.3% | 28.3% | 60 | 60 |
| **mean** | **71.7%** | **53.8%** | | |

### adversarial fixtures

| task | A | B | A n | B n |
|---|---|---|---|---|
| color discrimination | 50.0% | 50.0% | 30 | 30 |
| color constancy | 65.0% | 40.0% | 20 | 20 |
| shape transform | 31.8% | 37.8% | 44 | 45 |
| pitch discrimination | 33.3% | 36.7% | 30 | 30 |
| timbre discrimination | 100.0% | 83.3% | 30 | 30 |
| motion direction | 30.0% | 26.7% | 30 | 30 |
| **mean** | **51.7%** | **45.7%** | | |

## 4. Memory integration (shared deliberate-memory rule)

Rule (identical code path for both): INSTALL iff no contradictory installed
belief with confidence ≥ incoming exists in the (approach, task) stream;
else WITHHOLD + audit. False install = installed judgment contradicts .truth.

|  | A | B |
|---|---|---|
| installs (all fixtures) | 364 | 485 |
| false installs (all fixtures) | 160 | 269 |
| withholds (all fixtures) | 560 | 440 |
| installs (adversarial) | 134 | 131 |
| false installs (adversarial) | 79 | 72 |
| adversarial fixtures | 184 | 185 |
| false-install rate, adversarial (per install) | 59.0% | 55.0% |
| false-install rate, adversarial (per fixture) | 42.9% | 38.9% |
| false-install rate, all fixtures (per install) | 44.0% | 55.5% |

## 5. Kill-bar evaluation (computed)

| bar | A | B |
|---|---|---|
| KB1 viability (mean ≥ 60%) | PASS | FAIL |
| KB2 head-to-head | winner=A (|Δ|=18.6pp, ops ratio=2.42×) | (see A column) |
| KB3 fragility (winner drop > 25pp) | not fragile (noise drop 1.0pp, adv drop 20.9pp) | not fragile (noise drop 0.3pp, adv drop 8.3pp) |
| KB4 memory integration (adv false-install ≤ 10%) | FAIL (59.0% > 10%) | FAIL (55.0% > 10%) |
| KB5 determinism (3× byte-identical) | PASS (60/60 samples byte-identical over 3 runs) | PASS (60/60 samples byte-identical over 3 runs) |

KB3 evaluated against the KB2 winner = approach A.

## 6. Notes

- Fixture inventory: 60/40/90/60/60/60 primary, same counts noise, 30/20/45/30/30/30 adversarial (925 fixtures + 925 .truth files).
- Noise is deterministic precomputed noise baked into fixture files (splitmix64, master seed 20260921); no RNG at scoring time.
- Determinism sample: first 10 primary fixtures per task, 3 runs each.
- Memory streams: one per (approach, task); all variants in sorted-path order; KB4 uses the adversarial-fixture subset.
- Ops counted by the sense binaries at element-visit grain per INTERFACE.md.
- Runner error (1): approach A's binary exited 1 with `error=task_failed` on
  `t3_shapetrans/adversarial/p042.img` (valid 96×96 fixture, truth=TRIANGLE);
  approach A's shape-adversarial n is therefore 44, not 45. Approach-side
  failure, not a harness defect.

