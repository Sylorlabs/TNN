# Phenomena SPEC — sealed set (Crew S, 2026-09-27)

Confounded attribute-table phenomena for the native hypothesis-testing line (frozen prereg `docs/lab/hyptest/PREREG.md` section 5).

Shape per phenomenon: taught facts establish two attributes A and B that each covary with an outcome O across the taught instances (A and B concordant in the taught set). The phenomenon instance dissociates A and B (O unstated), so A-based and B-based extrapolation disagree. The test observation varies one attribute while holding the other, deciding between the attributions. Boundary: the test observation is consistent with both hypotheses — correct behavior is withhold.

Phenomenon files (`sentences.tsv`) contain OBSERVATIONS ONLY — no hypothesis hints, no labels, no adjudications. `gold.tsv` is for the coordinator's scoring only (K4/K5/K10).

## Sentence contract (strict, Crew S2 repair 2026-09-27)

Every sentence is "<subject> <copula> <value>." — the copula is exactly "is" or "are", all lowercase, one trailing period, no numerals. ONE subject string per entity, byte-identical across all its sentences (leading "the" is allowed only if used on every sentence for that entity; the sealed set uses bare entity names). Teach: each entity appears in exactly 3 sentences in attribute order (sentence 1 = A value, sentence 2 = B value, sentence 3 = outcome value). Phenomenon: the phenomenon entity appears in exactly 2 sentences (A, B; outcome unstated). Test: the test entity appears in exactly 3 sentences (A, B, outcome). Possessives are paraphrased as copula + hyphenated category ("boeing is wide-winged." — never "boeing has wide wings."; "fries are many-caloried."; "jupiter is long-yeared."). `build_phenomena.py::check_contract` asserts rules 1–5 mechanically on every line of `sentences.tsv` (shape regex + per-entity subject uniformity + 3/2/3 sentence counts per phase) and fails loud on violation. The native intake only understands this strict copula form with one consistent subject string per entity; anything else is dropped and collapses the slot structure.

**SEALED UNTIL RUN.** Broker-held; Crew M must never see this set.

## Data sources

- USDA FoodData Central; McDonald's USA and Burger King published nutrition data
- Wikipedia aircraft articles (specifications); manufacturer data as cited therein
- NASA Planetary Fact Sheets; Wikipedia
- Wikipedia (moons of Jupiter / moons of Saturn; individual moon articles); NASA factsheets
- Wikipedia city articles, climate normals (WMO station data as cited therein); spot-verified via web search 2026-09-27

All category assignments below were checked against the real values; no numbers are invented. Sentences themselves are categorical (no numerals), so the intake never sees a figure to misparse.

## seal01 — food

- A = serving size; B = fat content; O = calories per serving
- Category thresholds: large serving: >= 150 g; small serving: <= 100 g; fatty: >= 10 g fat per 100 g; lean: <= 2 g fat per 100 g; many calories: >= 300 kcal per serving; few calories: <= 150 kcal per serving
- Source: USDA FoodData Central; McDonald's USA and Burger King published nutrition data

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| fries | teach | 154 g | 14.3 g/100g | 480 kcal | large / fatty / many |
| burger | teach | 290 g | 14.5 g/100g | 740 kcal | large / fatty / many |
| apple | teach | 100 g | 0.2 g/100g | 52 kcal | small / lean / few |
| peach | teach | 100 g | 0.3 g/100g | 39 kcal | small / lean / few |
| watermelon | phenomenon | 300 g | 0.15 g/100g | — (unstated) | large / lean / ? |
| strawberries | test | 300 g | 0.3 g/100g | 96 kcal | large / lean / few |

- Gold: test observable = 'calories', test value = 'few calories', winner = 'the hypothesis attributing O to attribute B wins'

## seal02 — planes

- A = wingspan; B = weight; O = cruise speed
- Category thresholds: wide wings: span >= 30 m; narrow wings: span <= 15 m; heavy: >= 10,000 kg MTOW; light: <= 3,000 kg; fast: >= 800 km/h; slow: <= 300 km/h
- Source: Wikipedia aircraft articles (specifications); manufacturer data as cited therein

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| boeing | teach | 64.4 m | 396,890 kg | 913 km/h | wide / heavy / fast |
| airbus | teach | 79.75 m | 575,000 kg | 903 km/h | wide / heavy / fast |
| cessna | teach | 11.0 m | 1,111 kg | 226 km/h | narrow / light / slow |
| piper | teach | 10.7 m | 1,157 kg | ~230 km/h | narrow / light / slow |
| solar | phenomenon | 71.9 m | 2,300 kg | — (unstated) | wide / light / ? |
| eta | test | 30.9 m | 850 kg | ~160 km/h | wide / light / slow |

- Gold: test observable = 'speed', test value = 'slow', winner = 'the hypothesis attributing O to attribute B wins'

## seal03 — planets

- A = distance from the sun; B = diameter; O = orbital period (year length)
- Category thresholds: distant: >= 5 AU; close: <= 2 AU; giant: diameter >= 50,000 km; tiny: diameter <= 10,000 km; long year: >= 5 years; short year: <= 2 years
- Source: NASA Planetary Fact Sheets; Wikipedia

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| jupiter | teach | 5.20 AU | 139,820 km | 11.86 y | distant / giant / long |
| saturn | teach | 9.58 AU | 116,460 km | 29.45 y | distant / giant / long |
| mercury | teach | 0.39 AU | 4,879 km | 88 d | close / tiny / short |
| mars | teach | 1.52 AU | 6,779 km | 687 d | close / tiny / short |
| pluto | phenomenon | 39.48 AU | 2,377 km | — (unstated) | distant / tiny / ? |
| eris | test | 67.9 AU | 2,326 km | 558 y | distant / tiny / long |

- Gold: test observable = 'year length', test value = 'long year', winner = 'the hypothesis attributing O to attribute A wins'

## seal04 — moons

- A = orbital distance; B = moon size; O = orbital period
- Category thresholds: inner: orbital radius < 500,000 km; outer: > 500,000 km; small: diameter < 500 km; big: diameter > 3,000 km (Jupiter) / > 1,000 km (Saturn); fast: period < 2 days; slow: period > 3 days
- Source: Wikipedia (moons of Jupiter / moons of Saturn; individual moon articles); NASA factsheets

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| pan | teach | 133,584 km | ~28 km | 0.575 d | inner / small / fast |
| daphnis | teach | 136,505 km | ~8 km | 0.594 d | inner / small / fast |
| rhea | teach | 527,108 km | 1,527 km | 4.518 d | outer / big / slow |
| iapetus | teach | 3,560,820 km | 1,471 km | 79.32 d | outer / big / slow |
| phoebe | phenomenon | 12,947,780 km | ~213 km | — (unstated) | outer / small / ? |
| ymir | test | 23,040,000 km | ~18 km | 1315.4 d | outer / small / slow |

- Gold: test observable = 'orbital speed', test value = 'slow', winner = 'the hypothesis attributing O to attribute A wins'

## sealB1 — climate

- A = latitude zone; B = altitude; O = mean annual temperature
- Category thresholds: tropical: |latitude| < 23.5 deg; northern: |latitude| >= 23.5 deg; lowland: elevation < 300 m; highland: elevation >= 1000 m; hot: annual mean >= 25 C; cold: annual mean <= 8 C
- Source: Wikipedia city articles, climate normals (WMO station data as cited therein); spot-verified via web search 2026-09-27

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| manila | teach | 14.60 N | 16 m | 28.1 C | tropical / lowland / hot |
| jakarta | teach | 6.20 S | 8 m | 28.0 C | tropical / lowland / hot |
| xining | teach | 36.62 N | ~2275 m | 6.0-6.1 C | northern / highland / cold |
| leh | teach | 34.16 N | 3505 m | 5.2 C | northern / highland / cold |
| stockholm | phenomenon | 59.33 N | 28 m | — (unstated) | northern / lowland / ? |
| mumbai | test | 19.08 N | 14 m | 27.7-27.9 C | tropical / lowland / hot |

- Gold: test observable = 'temperature', test value = 'hot', winner = 'WITHHOLD'

## sealB2 — food

- A = serving size; B = fat content; O = calories per serving
- Category thresholds: large serving: >= 150 g; small serving: <= 100 g; fatty: >= 10 g fat per 100 g; lean: <= 2 g fat per 100 g; many calories: >= 300 kcal per serving; few calories: <= 150 kcal per serving
- Source: USDA FoodData Central; McDonald's USA and Burger King published nutrition data

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| bigmac | teach | 217 g | 15.7 g/100g | 590 kcal | large / fatty / many |
| whopper | teach | 294 g | 13.6 g/100g | 660 kcal | large / fatty / many |
| banana | teach | 100 g | 0.3 g/100g | 89 kcal | small / lean / few |
| orange | teach | 100 g | 0.1 g/100g | 47 kcal | small / lean / few |
| celery | phenomenon | 300 g | 0.15 g/100g | — (unstated) | large / lean / ? |
| carrot | test | 60 g | 0.2 g/100g | ~25 kcal | small / lean / few |

- Gold: test observable = 'calories', test value = 'few calories', winner = 'WITHHOLD'

