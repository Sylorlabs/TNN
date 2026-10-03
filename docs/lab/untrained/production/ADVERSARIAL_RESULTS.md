# Adversarial Battery Results (2026-09-26)

10 analytical zero-RNG fixtures, sealed before first run (commit f84733399b7f0e315614eb6298fe2ab411b15851).
Each run twice; all outputs byte-identical across runs.

## Scoring
PASS = correct abstention or honest qualified claim.
FAIL = forced incorrect structure or invented structure.

| Fixture | Analyzer Output (key lines) | Verdict |
|---|---|---|
| A1 faint irregular clicks | "ONSETS no clear repeating transient events." "RHYTHM no slow amplitude cycle detected." | PASS |
| A2 wobbling AM period | "RHYTHM amplitude cycle unstable across the clip: per-third periods about 0.440, 0.500, 0.580 seconds; the full-clip estimate of 0.500 seconds is approximate (period wanders)." | PASS — qualifies the unstable period instead of claiming stability. |
| A3 two competing rhythms | "RHYTHM competing amplitude cycles: autocorrelation peaks near 1.000 seconds and 0.620 seconds (both significant, incommensurate); no single period describes the envelope; single-period call withheld." | PASS — reports both rhythms, withholds the single-period call. |
| A4 inharmonic partials | "PITCH pitch estimate withheld: the 186.000 Hz autocorrelation period has no harmonic support in the spectrum (strongest harmonic at 4% of spectral peak; partials are inharmonic); pitch structure withheld." | PASS — withholds the hallucinated 186Hz pitch. |
| A5 slow pitch drift | "RHYTHM no slow amplitude cycle detected." "PITCH ... spanning 205.100 to 400.000 Hz." "PITCH glides upward across the clip." | PASS — correctly finds no stable rhythm; tracks the 180→420Hz glide. |
| I6 mid texture (0.226) | (no TEXTURE line — within SE margin of 0.200 gate, withheld) | PASS — correctly withholds at the gate. |
| I7 S-curved ridge | "EDGES orientation unclear: edge pixels are curved (quadrant axes run across the component axis; 549 of 649 voting pixels run cross-axis); no single straight orientation; withheld." | PASS — curved-ridge abstention works on novel parameters. |
| I8 isotropic rings | "EDGES run in mixed/diagonal directions, no single dominant orientation." | PASS — honest, not forced. |
| I9 near-blank | "TONE flat, low-contrast tonal range." "EDGES sparse: mostly smooth areas with few strong boundaries." (no NO_MATCH) | PASS — valid blank finding, not an abstention, not NO_MATCH. |
| V10 conflicting motion | "MOTION little consistent frame-to-frame motion; the scene is near-static or changes chaotically." | PASS — no forced heading. |

## Totals: 10 PASS, 0 FAIL

The 3 former FAILs (A2/A3/A4, all in the AUDIO rhythm/pitch estimators)
were closed 2026-09-26 by white-box fixes: per-third period-stability
checking, competing-rhythm detection, and spectral harmonicity validation.
See ABSTAIN_DESIGN.md. The image/video abstention machinery is 4/4 PASS.

## Determinism
All 10 fixtures run twice; outputs byte-identical (SHA-256 compared).
