# V2 JUDGMENT — selene (B3 step 5: re-judge from pixels only)

**Judge:** frozen `judge` v1, same protocol, same representations.
**Trace:** `ui-judgment/traces/b3iter/selene_v2_a.txt` / `_b.txt`.
**v2 changes:** h1 52→68px, hero padding 120/90, card titles 18→20px,
card copy 15px, moon text 18→16px, section heads 26→28px, comp sections
64px, internal gaps 16/32 (CSS-only delta; HTML/TS byte-identical to v1,
tsc clean).

## Frozen mechanism verdict (verbatim)

- Rep a: judgment=GOOD, score=704,
  defects=TYPOGRAPHY_INCONSISTENT,HIERARCHY_FLAT
- Rep b: judgment=GOOD, score=704,
  defects=TYPOGRAPHY_INCONSISTENT,HIERARCHY_FLAT
- v1 → v2: 704 → 704 (tie). hero_ratio 575→740 (better, still <952 floor);
  type_modes stuck at 5 (envelope hi=4).

## Blind proxy rubric (preregistered; A=v1, B=v2)

| defect | measure | v1 | v2 | improved? |
|---|---|---|---|---|
| TYPOGRAPHY_INCONSISTENT | type_modes ↓ | 5 | 5 | no (tie) |
| HIERARCHY_FLAT | hero_ratio ↑ / size_ratio ↑ | 0.3718 / 4.182 | 0.4923 / 6.091 | YES |
| SPACING_IRREGULAR | gap_cv ↓ | 0.8352 | 1.0058 | no |

Majority improved: NO (1/3).

## B3 verdict: FAIL

(a) judge score v2>v1: NO (704=704). (b) proxy majority: NO (1/3).
Diagnosis: mixed. The hero did get more dominant (both instruments agree:
judge hero_ratio 575→740, proxy 0.37→0.49) but not enough to clear the
952‰ envelope floor — structural bar issue, as with dawn. The typography
collapse (5→4 modes) did not materialize in rendered band heights; the
defect persists identically. Acting moved the right direction on hierarchy
but could not reach the bar; spacing moved the wrong way on both
instruments (judge gap_cv 1048→1204, proxy 0.84→1.01).
