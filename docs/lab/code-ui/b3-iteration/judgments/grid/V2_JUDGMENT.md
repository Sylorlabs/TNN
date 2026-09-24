# V2 JUDGMENT — grid (B3 step 5: re-judge from pixels only)

**Judge:** frozen `judge` v1, same protocol, same representations.
**Trace:** `ui-judgment/traces/b3iter/grid_v2_a.txt` / `_b.txt`.
**v2 changes:** masthead 64→72, lead 40→44, section heads 28→24, card
heads 20→18, sections 56px, internal gaps 32px, meta-text voices split
(CSS-only delta; HTML/TS byte-identical to v1, tsc clean).

## Frozen mechanism verdict (verbatim)

- Rep a: judgment=GOOD, score=704,
  defects=TYPOGRAPHY_INCONSISTENT,HIERARCHY_FLAT
- Rep b: judgment=GOOD, score=704,
  defects=TYPOGRAPHY_INCONSISTENT,HIERARCHY_FLAT
- v1 → v2: 830 → 704 (REGRESSION, −126). The typography fix backfired:
  type_modes 4→5 crossed the envelope ceiling (hi=4), firing a NEW defect
  TYPOGRAPHY_INCONSISTENT. hero_ratio improved 335→410 but stayed far below
  the 952 floor, so HIERARCHY_FLAT persists.

## Blind proxy rubric (preregistered; A=v1, B=v2)

| defect | measure | v1 | v2 | improved? |
|---|---|---|---|---|
| HIERARCHY_FLAT | hero_ratio ↑ / size_ratio ↑ | 0.168 / 3.538 | 0.2146 / 4.250 | YES |
| SPACING_IRREGULAR | gap_cv ↓ | 0.7325 | 0.7673 | no |
| TYPOGRAPHY_INCONSISTENT | type_modes ↓ | 7 | 7 | no (tie) |

Majority improved: NO (1/3).

## B3 verdict: FAIL

(a) judge score v2>v1: NO (830→704, regression). (b) proxy majority:
NO (1/3).
Diagnosis: failure in ACTING on the judgment. The reshufling of type sizes
(created a 5th rendered band-height class) tripped the judge's
TYPOGRAPHY_INCONSISTENT while aiming to fix it — the crew's size ladder
(72/44/24/18/16/15/12) is typographically cleaner to a human eye but the
judge counts rendered band heights, not CSS sizes. Both instruments agree
hierarchy improved (hero_ratio up) and spacing did not. The v1 (830) remains
the better-scoring artifact by the frozen judgment.
