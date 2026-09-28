# V2 JUDGMENT — gadget (B3 step 5: re-judge from pixels only)

**Judge:** frozen `judge` v1, same protocol, same representations.
**Trace:** `ui-judgment/traces/b3iter/gadget_v2_a.txt` / `_b.txt`.
**v2 changes:** h1 40→56px, hero padding 96/64, component sections 56px,
body padding unified 24px, control gaps unified 16px (CSS-only delta;
HTML/TS byte-identical to v1, tsc clean).

## Frozen mechanism verdict (verbatim)

- Rep a: judgment=GOOD, score=960, defects=none
- Rep b: judgment=GOOD, score=960, defects=none
- v1 → v2: 830 → 960 (+130). HIERARCHY_FLAT cleared: the defect-severity
  line for HIERARCHY_FLAT dropped below the 450 firing threshold; all other
  metrics stayed in-envelope.

## Blind proxy rubric (preregistered; A=v1, B=v2)

| defect | measure | v1 | v2 | improved? |
|---|---|---|---|---|
| HIERARCHY_FLAT | hero_ratio ↑ / size_ratio ↑ | 0.4282 / 2.667 | 0.6902 / 4.667 | YES |
| SPACING_IRREGULAR | gap_cv ↓ | 0.7909 | 0.8676 | no |
| ALIGNMENT_WEAK | align_modes ↓ | 2 | 1 | YES |

Majority improved: YES (2/3).

## B3 verdict: PASS

(a) judge score v2>v1: YES (830→960, defect cleared on both
representations). (b) proxy majority: YES (2/3).
Caveat: the proxy's gap_cv did not improve — the unified paddings did not
regularize inter-band gaps as measured. The win came from hierarchy +
alignment, not spacing.
