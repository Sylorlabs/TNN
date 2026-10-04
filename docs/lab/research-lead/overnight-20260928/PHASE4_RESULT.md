# Phase 4 Result: Concept Usefulness

**Date:** 2026-09-29 02:00 PDT
**Test:** H-USE (concepts improve downstream reasoning)

## Setup

- E1 concept: norpal/squeezer with 6 facts.
- Novel "zorp": 2 facts (sqz_emit->glimx, sqz_glow->glowx).
- Distractor "zorpal": 2 facts with different objects.
- Probe: (zorp, sqz_heat, ?) → velx.

## Results

**Full (with unification):**
- Unifications: norpal~squeezer, norpal~zorp, squeezer~zorp.
- zorpal NOT unified (correctly rejected).
- Probe: CORRECT (1/1). zorp → concept → norpal → velx.

**Ablated (no unification):**
- Probe: WITHHOLD (MISS). 0/1.
- Concepts beat literal memory.

**Nearest-match baseline (structural):**
- zorp overlaps with norpal (2 pairs), squeezer (2 pairs), zorpal (0 pairs).
- Picks norpal (tie with squeezer, both valid).
- norpal has (sqz_heat, velx) → answers velx CORRECT.
- **Baseline matches Full performance.**

## Verdict

**H-USE KILLED (for accuracy).** Concepts do not outperform structural nearest-match.

The Jaccard unifier is functionally equivalent to:
"Find taught surfaces with high (R,O) overlap, share their facts."

**What concepts add:**
- Efficiency: O(1) parent[] lookup vs O(n) similarity scan.
- Explicitness: Inspectable UNIFY nodes.
- BUT NOT: Accuracy advantage over simple similarity.

**Implication:** SEM-L3's "concepts" are a caching/optimization of nearest-neighbor
lookup, not a qualitatively different reasoning mechanism. This further supports
the L2+ (not L3) classification.

## Note on Distractor

The "zorpal" distractor (similar name, different structure) was correctly rejected
by BOTH the unifier and structural nearest-match. A NAME-based baseline would fail,
but that's a strawman. The fair baseline is structural, and it matches.
