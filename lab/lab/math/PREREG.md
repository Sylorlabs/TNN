# MATH CREW — Preregistration (frozen 2026-09-21)

**Order:** Micah 2026-09-21 — "can TNN do basic math... could it do math and figure
out how tall the Eiffel Tower is at specific times?"
**Status:** FROZEN. Any change to batteries, bars, facts, or metrics needs a dated
amendment signed by Micah.
**Commit rule:** this file is committed alone before any scored run.

## 1. Question

Can the TNN do quantitative reasoning — exact arithmetic, multi-step word
problems, and the real Eiffel Tower task (select the thermal-expansion formula,
plug in taught constants + stated temperatures, compute) — and does it know
WHEN to compute versus retrieve?

## 2. Architecture (pure Zag, zero RNG)

- `math.zag`, modes via argv:
  - `teach facts.txt`: installs facts (entity/attribute/value/unit/condition)
    into a deliberate store; emits store digest. Install acts are logged.
  - `solve battery.txt`: for each problem line: parse → classify mode
    (RETRIEVE / COMPUTE / ABSTAIN) → select formula if computing → exact
    rational arithmetic → emit `ID MODE ANSWER TRACE`.
- Rational engine: every quantity is (num, den) i64, always gcd-reduced,
  den > 0. No floats anywhere. Output: terminating decimals as decimals,
  non-terminating as exact reduced fractions.
- Formula registry (selection is by question semantics, never by item id):
  - THERMAL: L = L0·(1 + α·(T − T0)); inverse: T = T0 + (L − L0)/(L0·α)
  - PERCENT: P% of N = N·P/100; drop-by-P = N·(1 − P/100)
  - RATE: total = rate·time; time = total/rate; speed = dist/time
  - REMAINDER: start − Σ spent (fraction words: half/quarter/fifth)
  - UNITRATE: (a per b)·c; AREA: l·w; UNITCONV via taught/built-in ratios
- Retrieve-vs-compute rule: exact (entity, attribute, condition) fact match
  AND no computation trigger → RETRIEVE. (entity, attribute) fact match with a
  differing condition + applicable formula → COMPUTE. Arithmetic triggers
  (remain/left/profit/per/percent of) with no stored answer → COMPUTE.
  Nothing taught, nothing computable → ABSTAIN (never guess).
- `gen_math.py` (independent oracle): generates battery.txt + expected.json
  with Python Fractions. The Zag learner never sees expected.json (verified by
  grep). `score.py` diffs run logs vs expected.json.

## 3. Taught facts (facts.txt, frozen)

| fact | value |
|---|---|
| eiffel_tower height_m @ 20°C | 330 |
| eiffel_tower built_year | 1889 |
| iron alpha_per_C | 0.000012 |
| oak_street_bridge length_m @ 20°C | 100 |

## 4. Batteries (frozen counts; full text in battery.txt, answers in expected.json)

| Battery | n | Input | Correct = |
|---|---|---|---|
| B1 ARITH | 40 | `EXPR:` / `CONVERT:` lines: add/sub/mul/div (20), fractions (6), percent (5), order-of-ops (5), unit conversion (4) | exact rational match |
| B2 WORD | 20 | natural-language multi-step problems (shopping, travel, remainder, percent, rate, area, age, laps) incl. 6 paraphrase variants of 6 base problems | exact numeric match |
| B3 EIFFEL | 12 | E-01..E-12: forward height ×4, inverse ×1, retrieve ×3, wrong-formula distractor ×1, transfer ×2, ΔT=0 ×1 | exact match (terminating decimals) |
| B4 MODE | 12 | M-01..M-12: retrieve/compute/abstain discrimination | mode AND answer correct (M-11 accepts either mode) |

Key Eiffel numbers (oracle-verified): 35°C → 330.0594 m; −2°C → 329.91288 m;
inverse of 330.0594 → 35°C; bridge 100m @40°C → 100.024 m; rod 2m @70°C → 2.0012 m.

## 5. Kill bars (applied mechanically)

| Bar | Rule |
|---|---|
| KB-M1 arithmetic | B1 < 38/40 exact → FAIL |
| KB-M2 word problems | B2 < 16/20 → FAIL |
| KB-M3 eiffel | B3 < 10/12 exact → FAIL |
| KB-M4 mode judgment | B4 mode < 12/12 or any B4 answer wrong → FAIL (M-11 either mode) |
| KB-M5 determinism | any of 5 reps not byte-identical → FAIL |
| KB-M6 no-slip engine | any COMPUTE-class (arithmetic-slip) error in B1 → FAIL the exact-arithmetic claim |

## 6. Error classification (every miss, crew-inspected)

- CONCEPT: wrong formula selected, wrong mode, wrong slot filled, misparse.
- COMPUTE: rational arithmetic produced a wrong value for a right setup.
- A COMPUTE error anywhere is an engine bug; a CONCEPT error is a reasoning gap.

## 7. Metrics (all reported)

- Per battery: accuracy, per-item table with mode/answer/trace.
- Eiffel: forward/inverse numbers, formula-selection record.
- B2: base vs paraphrase-variant accuracy (paraphrase robustness gap).
- Error table: every miss with CONCEPT/COMPUTE label and cause.
