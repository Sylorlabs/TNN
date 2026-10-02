# SCALE-UP preregistration — frozen 2026-09-21

Micah's order: more categories, long-horizon FULL runs, LLM-scale training amounts.
First real test of the standing expectation: **no degradation over long horizons.**

## Corpus (frozen spec in corpus/FACTSPEC.md)

- 10 Project Gutenberg texts (original bytes + frozen normalization).
- 24 integer-valued, mechanically verifiable categories (word-level 0–15, text-level 16–23).
- Fact id = c*M + i, N = 24*M facts total.
- Planted falsehoods: exactly 5% of ids, splitmix64(seed=20260921) deterministic rule.
- Learners train on SUPPLIED values, evaluated against TRUTH (championship convention).

## Scale points

| Point | M (per category) | N (facts) | Passes | Reps |
|---|---|---|---|---|
| S0 baseline | 10 | 240 | 1, 2, 3 | 5 |
| S1 | 100 | 2,400 | 1, 2, 3 | 5 |
| S2 | 1,000 | 24,000 | 1, 2 | 5 (3 if time-forced, documented) |
| S3 | 10,000 | 240,000 | 1 | 3 (documented) |
| S4 stretch | per feasibility | >240k | 1 | 1–3 (documented) |

S0 must reproduce championship-class behavior (≈0.9911 mastery regime) or the driver is invalid.

## Measures (per scale point)

- M-mastery: fraction of facts recalled == truth (full probe at S0/S1, stratified sample ≥2,400 facts at S2+).
- M-horizon: mastery by training decile — facts from the first 10% of pass 1 vs the last 10%.
  **This is the catastrophic-forgetting measure.**
- M-retention: mastery after pass 2 and pass 3 (S0/S1).
- M-cost: total ops and ops/fact.
- M-flaw: sampled §B.7-style battery (96 probes on a fact sample).
- M-false: falsehood absorption rate (recalled == supplied false value, on false ids).
- M-determinism: byte-identical outputs across reps (diff).

## Kill bars (frozen)

| Bar | Condition | Consequence |
|---|---|---|
| KB-SCALING | M-mastery drops >2pp below the S0 baseline at any scale point | SCALING-FAIL — stop, report ceiling |
| KB-FORGET | M-horizon: last-decile minus first-decile mastery >3pp (early facts forgotten) at any scale | FORGET-FAIL — stop, report |
| KB-COST | ops/fact grows superlinearly (S2 ops/fact > 1.5× S1 ops/fact, or S3 > 1.5× S2) | COST-FAIL — stop, report |
| KB-DETERMINISM | any rep differs byte-wise at any scale | DETERMINISM-FAIL — stop, fix or report |
| KB-FLAW | M-flaw pass rate < 7/8 slices at any scale | FLAW-FAIL — stop, report |

If a bar trips, the scale-up STOPS at that point and the verdict reports the ceiling.
Bars are mechanical; no discretion. Amendments need Micah's dated sign-off.

## Honesty rules

- Report the ACTUAL ceiling reached, not "LLM amounts". Billions of tokens are out of
  reach on this VM; the verdict will state the real number.
- Procedural Gutenberg-derived corpus: no LLM API calls burned. Documented tradeoff:
  we lose prose-mediated effects; we gain unlimited deterministic real-English facts.
- znc 2^25-bytes-per-slice limit: all storage chunked (AGENTS.md lesson).
- Pure Zag TNN-side, no RNG in decision paths, N as tabled or documented.
- /tmp is 512MB tmpfs: all battery workdirs under ~/workspace/scale/.
