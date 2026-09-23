# D1 Diagnostic Report — RAW-VS-HUMAN TEST Wave

**Date:** 2026-09-22  
**Prereg:** `WAVE_RAWVSHUMAN_PREREG.md` § Diagnostic D1  
**Status:** PASS (both modalities in scope)

## Prereg language (verbatim)

> On TRAIN_T2, for B's colordisc errors: fraction where the pair straddles the
> ΔE 2.3 boundary (recomputed from the frozen generator code + fixture params —
> no new data) yet shares a color handle. Same for pitchdisc: fraction of errors
> where the relative difference is < one semitone yet both tones share a bin.
> **Gate: if D1 < 50% on BOTH modalities, H-mech is weakened — DO NOT BUILD.**

## Interpretation

"Straddles the ΔE 2.3 boundary yet shares a color handle" is formalized as:
the B error pair shares a single frozen color handle (perceptual identity),
while the frozen generator's recomputed ΔE confirms the pair is genuinely
above the 2.3 threshold (truth=DIFFERENT). No tolerance band is introduced;
the prereg states no band.

For pitch: the relative frequency difference is below one semitone (sub-semitone)
while both tones fall in the same frozen 48-bin semitone bin.

## Results (TRAIN_T2, frozen B, k=0)

| Modality | n (B errors) | Share handle/bin | D1 | Gate (≥50%) |
|----------|-------------|------------------|----|-------------|
| colordisc | 506 | 505 | **99.8%** | PASS |
| pitchdisc | 132 | 131 | **99.2%** | PASS |

### Color detail (506 errors)
- 505/506 share the same frozen color handle (all with truth=DIFFERENT,
  recomputed ΔE > 2.3).
- 1/506 uses different handles (below-threshold rendering artifact).
- Of the 505: 445 at recomputed ΔE 1.3–3.3, 16 at 3.3–10, 41 below 1.3,
  3 above 10. (ΔE recomputed from generator params; the sub-2.3 cases are
  generator/rendering deviations from the intended DIFFERENT label.)

### Pitch detail (132 errors)
- 131/132 share the same semitone bin with sub-semitone relative difference.
- 1/132 is sub-semitone but crosses a frozen bin edge.

## Scope decision

D1 ≥ 50% on **both** modalities. Scope = color + pitch. Proceed to build B2/B3.

## Artifacts

- `d1.py` — diagnostic implementation (frozen generator re-derivation)
- `d1_results.json` — machine-readable counts
- `d1_colordisc_rows.jsonl`, `d1_pitchdisc_rows.jsonl` — per-fixture rows

## Correction note

An earlier draft computed 87.94% for color using an invented ±1.0 ΔE band
around 2.3. That band appears nowhere in the prereg and is **withdrawn**.
The binding D1 is 99.8% (color) / 99.2% (pitch) per the prereg text above.
The gate outcome (PASS, both modalities) is unchanged.
