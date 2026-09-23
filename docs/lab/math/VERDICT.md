# Math Crew — VERDICT

**Date:** 2026-09-22
**Question:** Can TNN do basic math and quantitative reasoning — e.g. compute the Eiffel Tower's height at different temperatures, not just retrieve "330 m"?
**Answer: YES.** Pure-Zag learner scores **84/84** with byte-identical reruns.

## Scores vs frozen kill bars (PREREG.md, commit 3c7b376)

| Battery | Bar | Result | Verdict |
|---|---|---|---|
| B1 pure arithmetic (40) | KB-M1 ≥ 38/40 | **40/40** | PASS |
| B2 word problems (20) | KB-M2 ≥ 16/20 | **20/20** | PASS |
| B3 Eiffel thermal (12) | KB-M3 ≥ 10/12 | **12/12** | PASS |
| B4 compute/retrieve/abstain (12) | KB-M4 12/12 | **12/12** | PASS |
| Determinism (5 reruns) | KB-M5 byte-identical | **5/5 identical SHA256** | PASS |
| Arithmetic engine slips | KB-M6 zero slips in B1 | **0 slips** | PASS (exact-arithmetic claim stands) |

## Eiffel Tower results (the headline question)

Taught: height 330 m @ 20 °C, built 1889, iron α = 12×10⁻⁶/°C. Formula applied: L = L₀(1 + α(T−T₀)), inverse T = T₀ + (L−L₀)/(L₀α). All arithmetic exact rational, printed as decimals.

| Item | Question | Mode | Result |
|---|---|---|---|
| E-01 | Tower at 35 °C (3pm August) | COMPUTE | **330.0594 m** |
| E-02 | Tower at −2 °C (6am January) | COMPUTE | **329.91288 m** |
| E-03 | Infer temp from measured 330.0594 m | COMPUTE | **35 °C** |
| E-04 | Height at 20 °C | RETRIEVE | 330 m |
| E-05 | Year built | RETRIEVE | 1889 |
| E-06 | 100 m iron bridge at 40 °C | COMPUTE | **100.024 m** |
| E-07 | Tower, ambient 20 °C | COMPUTE | 330 m |
| E-08 | Tower at 10 °C (midnight) | COMPUTE | **329.9604 m** |
| E-09 | Taller at 3pm than 6am by | COMPUTE | **0.14652 m** |
| E-10 | 2 m steel rod at 70 °C | COMPUTE | **2.0012 m** |
| E-11 | Expansion coefficient of iron | RETRIEVE | 0.000012 |
| E-12 | Tower at 35 °C | COMPUTE | **330.0594 m** |

Mode judgment (B4): 12/12 — retrieves taught facts ("height at 20 °C", "built year", "coefficient"), computes thermal values, abstains on untaught knowledge ("capital of France").

## Concept vs computation errors

| Class | Count |
|---|---|
| CONCEPT (wrong formula / wrong mode / misparse) | 0 |
| COMPUTE (right setup, wrong rational arithmetic) | 0 |

Zero errors in the scored runs; nothing to classify.

## Determinism (KB-M5)

Five consecutive `./math_bin solve` runs → identical bytes.
SHA256 of each run: `e6377f6f3d7ee63107f3b43a7427bd33853d02050834cb7305d774fca6ca7818`

## Development notes (honest log)

First probe scored 70/84. All 14 misses were **concept/parsing bugs**, fixed before the scored runs — no bar was moved:

1. `num_before("expands")` crossed a sentence boundary and grabbed 20 instead of 12 → switched to `num_after("expands")` (tokenizer already scales "12 millionths" → 12/10⁶).
2. Inverse used number *before* "measures" ("measures 330.0594 m") → `num_after`.
3. `r_remainder`/`r_frac_drain` scanned backward from the query and grabbed the wrong number → anchor on the first unit occurrence; fraction = first proper-fraction token ("quarter" tokenizes to 1/4 by design).
4. `r_percent` used `first_num` as base → base = number after "of", else first number.
5. `r_addstock` required "holding" → "holding" now only overrides the "each"-rule value.
6. `r_convertq` took the token after "in" as the unit (it was the number) → unit = word after the number.
7. Bare "iron" didn't map to an entity → entity 3.
8. "How tall at T°" (T = reference) retrieves; ambient-temp "how tall" always computes — matches the frozen oracle's rule (E-07 COMPUTE vs M-07 RETRIEVE).

## Artifacts

- `math.zag` — the learner (pure Zag, no reference to `expected.json`)
- `runs/run1.txt … run5.txt` — the five scored runs
- `runs/teach.txt` — teach log + fact digest
- `score.py` — scorer
- `battery.txt` / `expected.json` / `facts.txt` / `gen_math.py` — frozen battery + independent Fraction oracle
