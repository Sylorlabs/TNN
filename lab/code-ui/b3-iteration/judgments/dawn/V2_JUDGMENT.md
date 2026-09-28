# V2 JUDGMENT — dawn (B3 step 5: re-judge from pixels only)

**Judge:** frozen `judge` v1, same protocol, same representations.
**Trace:** `ui-judgment/traces/b3iter/dawn_v2_a.txt` / `_b.txt`.
**v2 changes:** hero h1 56→72px, hero padding 140/110, sections 96px,
quote 28→24px (CSS-only delta; HTML/TS byte-identical to v1, tsc clean).

## Frozen mechanism verdict (verbatim)

- Rep a: judgment=GOOD, score=830, defects=HIERARCHY_FLAT
- Rep b: judgment=GOOD, score=830, defects=HIERARCHY_FLAT
- v1 → v2: 830 → 830 (tie). Metrics: hero_ratio 430→406, type_modes 4→3,
  gap_cv 865→879, contrast 3307→3739.

## Blind proxy rubric (preregistered; A=v1, B=v2)

| defect | measure | v1 | v2 | improved? |
|---|---|---|---|---|
| HIERARCHY_FLAT | hero_ratio ↑ / size_ratio ↑ | 0.4396 / 3.714 | 0.3811 / 4.000 | YES (size_ratio) |
| SPACING_IRREGULAR | gap_cv ↓ | 0.8828 | 0.9026 | no |
| TYPOGRAPHY_INCONSISTENT | type_modes ↓ | 4 | 4 | no (tie) |

Majority improved: NO (1/3).

## B3 verdict: FAIL

(a) judge score v2>v1: NO (830=830). (b) proxy majority: NO (1/3).
Diagnosis: the enlarged hero fragmented into more bands under the judge's
band detector (hero_ratio 430→406) instead of consolidating — acting on the
defect did not move the judge's number. The envelope floor (952‰) is
unreachable for any multi-section page (all 5 refs are near-single-band
hero crops: apple2 m_bands=1), so HIERARCHY_FLAT is structural, not
actionable, for full pages. Failure sits in the judging bar, not in the
acting: the proxy confirms the hero did get relatively larger (size_ratio
3.71→4.00) while the judge's metric moved the other way.
