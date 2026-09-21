# G-GROK Championship Verdict (2026-09-21)

**Crew:** G-GROK (SEPARATE class, grok-4.6 only, no D1/planting)
**Corpus:** `7b2d28890a703aff7dbed363f667d2bccc154fc99748e0d332fc34fc2be49589`
**Model:** grok-4.6, temperature=0, seed=42
**Commits:** corpus DATA `c9b987ed`, raw `3b478295`

## Corpus faithfulness

| metric | value |
|---|---|
| E_dump | 0 |
| E_obs | 0 |
| E_prb | 0 |
| inconsistent | 0 |
| 12 false claims | all reproduced (not flagged, not corrected) |

Grok was perfectly faithful, like sol. **K-Q2 does not fire** (no errors to catch).

## Class-4: Direct Track-5 + sealed §B.7

**Track-5 (5 reps, byte-identical per rep, S10 no-degradation):**

| metric | rep 0 | rep 1 | rep 2 | rep 3 | rep 4 |
|---|---|---|---|---|---|
| mastery (d1/d2/d3) | 40/40, 38/38, 120/120 | 40/40, 40/40, 120/120 | 40/40, 37/37, 120/120 | ... | ... |
| revisability | 12/12, 20/20 | 12/12, 20/20 | 12/12, 20/20 | ... | ... |
| integrity (k1/k2/k3) | 1/1, 1/1, 1/1 | 1/1, 1/1, 1/1 | 1/1, 1/1, 1/1 | ... | ... |
| retention (r2/r3) | 40/40, 40/40 | 40/40, 40/40 | 40/40, 40/40 | ... | ... |
| cost | 0.9108 | 0.9108 | 0.9108 | ... | ... |
| **composite** | **0.9911** | **0.9911** | **0.9911** | ... | ... |

**Sealed §B.7 (5/5 byte-identical):**

| slice | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| hits/12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| bar (≥10) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Total:** 96/96 hits, 8/8 slices pass.

**btrap:** 7/7 families 20/20, controls 2/2.
**S10:** no degradation (all metrics hold at 10x).

## Class-3: Teacher transfer (tid=20) + same scoring

**Track-5 (5/5 byte-identical, exit=0):**

| metric | value |
|---|---|
| mastery | 1.0000 (40/40, 38/38, 120/120) |
| revisability | 1.0000 (rev_g 20/20; rev_false vacuous, 12 false never taught) |
| integrity | 1.0000 (k1/k2/k3 pass, 0 hallucinations) |
| retention | 1.0000 (40/40, 40/40) |
| cost | 0.9588 (ops=276, eps=642) |
| **composite** | **0.9959** |

**Sealed §B.7 (5/5 byte-identical):**

| slice | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| hits/12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 12 |
| bar (≥10) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Total:** 96/96 hits, 8/8 slices pass.

## Verdict

| class | Track-5 composite | §B.7 (8 slices) | verdict |
|---|---|---|---|
| Class-4 (direct) | 0.9911 | 8/8 ≥10/12 | **PASS** |
| Class-3 (teacher tid=20) | 0.9959 | 8/8 ≥10/12 | **PASS** |

Both classes pass. The grok-taught learner (D2 route) achieves the same
0.9911 composite as sol's D2. The teacher-transfer (Class-3) achieves
0.9959 with 8/8 §B.7 slices at 12/12 — the grok-teacher (ID 20)
successfully teaches a fresh learner via the Q1 pattern.

K-Q2: **DOES NOT FIRE** (grok introduced zero errors, like sol).
