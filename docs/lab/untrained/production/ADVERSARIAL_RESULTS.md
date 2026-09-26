# Adversarial Battery Results (2026-09-26)

10 analytical zero-RNG fixtures, sealed before first run (commit f84733399b7f0e315614eb6298fe2ab411b15851).
Each run twice; all outputs byte-identical across runs.

## Scoring
PASS = correct abstention or honest qualified claim.
FAIL = forced incorrect structure or invented structure.

| Fixture | Analyzer Output (key lines) | Verdict |
|---|---|---|
| A1 faint irregular clicks | "ONSETS no clear repeating transient events." "RHYTHM no slow amplitude cycle detected." | PASS |
| A2 wobbling AM period | "RHYTHM amplitude repeats on a cycle of about 0.500 seconds." | FAIL — claims a stable 0.5s period; the period wobbles 0.43–0.61s. Should qualify or abstain. |
| A3 two competing rhythms | "RHYTHM amplitude repeats on a cycle of about 1.000 seconds." | FAIL — forces a single 1.0s period; the envelope has 2Hz and 3Hz components. Should report both or abstain. |
| A4 inharmonic partials | "PITCH predominantly tonal: ... near 186.000 Hz" | FAIL — hallucinates 186Hz pitch; partials are 211/359/547/733/941 Hz (inharmonic). No 186Hz component exists. |
| A5 slow pitch drift | "RHYTHM no slow amplitude cycle detected." "PITCH ... spanning 205.100 to 400.000 Hz." "PITCH glides upward across the clip." | PASS — correctly finds no stable rhythm; tracks the 180→420Hz glide. |
| I6 mid texture (0.226) | (no TEXTURE line — within SE margin of 0.200 gate, withheld) | PASS — correctly withholds at the gate. |
| I7 S-curved ridge | "EDGES orientation unclear: edge pixels are curved (quadrant axes run across the component axis; 549 of 649 voting pixels run cross-axis); no single straight orientation; withheld." | PASS — curved-ridge abstention works on novel parameters. |
| I8 isotropic rings | "EDGES run in mixed/diagonal directions, no single dominant orientation." | PASS — honest, not forced. |
| I9 near-blank | "TONE flat, low-contrast tonal range." "EDGES sparse: mostly smooth areas with few strong boundaries." (no NO_MATCH) | PASS — valid blank finding, not an abstention, not NO_MATCH. |
| V10 conflicting motion | "MOTION little consistent frame-to-frame motion; the scene is near-static or changes chaotically." | PASS — no forced heading. |

## Totals: 7 PASS, 3 FAIL

The 3 FAILs are all in the AUDIO rhythm/pitch estimators:
- A2: period-stability not checked (wobble not detected)
- A3: competing autocorr peaks not detected (forces winner)
- A4: pitch estimate not validated against spectrum (hallucination)

These are documented as SURVIVING LIMITATIONS in PRODUCTION_DECLARATION.md.
The image/video abstention machinery (the focus of this adoption) is 4/4 PASS.

## Determinism
All 10 fixtures run twice; outputs byte-identical (SHA-256 compared).
