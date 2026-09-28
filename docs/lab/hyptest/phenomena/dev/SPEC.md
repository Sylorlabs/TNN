# Phenomena SPEC — dev set (Crew S, 2026-09-27)

Confounded attribute-table phenomena for the native hypothesis-testing line (frozen prereg `docs/lab/hyptest/PREREG.md` section 5).

Shape per phenomenon: taught facts establish two attributes A and B that each covary with an outcome O across the taught instances (A and B concordant in the taught set). The phenomenon instance dissociates A and B (O unstated), so A-based and B-based extrapolation disagree. The test observation varies one attribute while holding the other, deciding between the attributions. Boundary: the test observation is consistent with both hypotheses — correct behavior is withhold.

Phenomenon files (`sentences.tsv`) contain OBSERVATIONS ONLY — no hypothesis hints, no labels, no adjudications. `gold.tsv` is for the coordinator's scoring only (K4/K5/K10).

## Data sources

- Wikipedia city articles, climate normals (WMO station data as cited therein); spot-verified via web search 2026-09-27
- Wikipedia (moons of Jupiter / moons of Saturn; individual moon articles); NASA factsheets
- Wikipedia (list of lakes by volume; individual lake articles)

All category assignments below were checked against the real values; no numbers are invented. Sentences themselves are categorical (no numerals), so the intake never sees a figure to misparse.

## dev01 — climate

- A = latitude zone; B = altitude; O = mean annual temperature
- Category thresholds: tropical: |latitude| < 23.5 deg; northern: |latitude| >= 23.5 deg; lowland: elevation < 300 m; highland: elevation >= 1000 m; hot: annual mean >= 25 C; cold: annual mean <= 8 C
- Source: Wikipedia city articles, climate normals (WMO station data as cited therein); spot-verified via web search 2026-09-27

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| singapore | teach | 1.35 N | 15 m | 27.5 C | tropical / lowland / hot |
| lagos | teach | 6.45 N | 41 m | 27.0 C | tropical / lowland / hot |
| ulaanbaatar | teach | 47.92 N | 1350 m | -0.4 C | northern / highland / cold |
| erzurum | teach | 39.91 N | ~1900 m | ~5.5 C | northern / highland / cold |
| moscow | phenomenon | 55.76 N | 156 m | — (unstated) | northern / lowland / ? |
| harbin | test | 45.75 N | 150 m | ~3.5-5.6 C | northern / lowland / cold |

- Gold: test observable = 'temperature', test value = 'cold', winner = 'the hypothesis attributing O to attribute A wins'

## dev02 — moons

- A = orbital distance; B = moon size; O = orbital period
- Category thresholds: inner: orbital radius < 500,000 km; outer: > 500,000 km; small: diameter < 500 km; big: diameter > 3,000 km (Jupiter) / > 1,000 km (Saturn); fast: period < 2 days; slow: period > 3 days
- Source: Wikipedia (moons of Jupiter / moons of Saturn; individual moon articles); NASA factsheets

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| metis | teach | 128,000 km | ~60 km | 0.295 d | inner / small / fast |
| adrastea | teach | 129,000 km | ~16 km | 0.298 d | inner / small / fast |
| ganymede | teach | 1,070,400 km | 5,268 km | 7.155 d | outer / big / slow |
| callisto | teach | 1,882,700 km | 4,821 km | 16.689 d | outer / big / slow |
| himalia | phenomenon | 11,451,000 km | ~140 km | — (unstated) | outer / small / ? |
| elara | test | 11,741,000 km | ~86 km | 257.62 d | outer / small / slow |

- Gold: test observable = 'orbital speed', test value = 'slow', winner = 'the hypothesis attributing O to attribute A wins'

## dev03 — lakes

- A = surface area; B = maximum depth; O = water volume
- Category thresholds: large: area >= 5,000 km2; small: area <= 3,000 km2; deep: max depth >= 200 m; shallow: max depth <= 100 m; huge: volume >= 4,000 km3; tiny: volume <= 500 km3
- Source: Wikipedia (list of lakes by volume; individual lake articles)

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| superior | teach | 82,100 km2 | 406 m | 12,100 km3 | large / deep / huge |
| baikal | teach | 31,722 km2 | 1,642 m | 23,615 km3 | large / deep / huge |
| okeechobee | teach | 1,900 km2 | 3.7 m | ~5 km3 | small / shallow / tiny |
| simcoe | teach | 722 km2 | 41 m | 11.6 km3 | small / shallow / tiny |
| winnipeg | phenomenon | 24,514 km2 | 36 m | — (unstated) | large / shallow / ? |
| balkhash | test | 16,400 km2 | 26 m | ~100-112 km3 | large / shallow / tiny |

- Gold: test observable = 'water volume', test value = 'tiny', winner = 'the hypothesis attributing O to attribute B wins'

## devB1 — lakes

- A = surface area; B = maximum depth; O = water volume
- Category thresholds: large: area >= 5,000 km2; small: area <= 3,000 km2; deep: max depth >= 200 m; shallow: max depth <= 100 m; huge: volume >= 4,000 km3; tiny: volume <= 500 km3
- Source: Wikipedia (list of lakes by volume; individual lake articles)

| entity | phase | A (real) | B (real) | O (real) | categories |
|---|---|---|---|---|---|
| tanganyika | teach | 32,900 km2 | 1,470 m | 18,900 km3 | large / deep / huge |
| malawi | teach | 29,600 km2 | 706 m | 8,400 km3 | large / deep / huge |
| balaton | teach | 594 km2 | 11 m | 1.9 km3 | small / shallow / tiny |
| neusiedl | teach | 315 km2 | 1.8 m | ~0.5 km3 | small / shallow / tiny |
| maracaibo | phenomenon | 13,210 km2 | 60 m | — (unstated) | large / shallow / ? |
| michigan | test | 58,030 km2 | 281 m | 4,900 km3 | large / deep / huge |

- Gold: test observable = 'water volume', test value = 'huge', winner = 'WITHHOLD'

