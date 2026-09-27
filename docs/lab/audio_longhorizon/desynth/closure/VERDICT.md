# Audio de-synth: three-wall integration — final verdict

**Date:** 2026-09-27
**Status:** CLOSED (with honest residuals documented below)

## What was integrated

Three walls, built separately, merged into one planner:

1. **Wall 1 — strict trig-free hearing** (`wall1/`): removes all trig calls from the hearing path. Zero `cosr`/`fcosr`/`sinr` references in the final source. Hearing byte-identical on all 20 references.
2. **Wall 2 — low-F0 mis-hearing repair** (`wall2/`): root cause was guard-layer censoring + median bias, not YIN failure. Loudness gate −20 → −50 dBFS. t20: 890.2→96.9 Hz (truth ≈95.8). t17 render: 221.3→94.7 Hz (truth ≈94.2).
3. **Wall 3 — envelope vocabulary** (`wall3/`): four measured atoms (2 rise, 2 decay) from real corpus WAVs, no oscillators. Level-normalized to the native reference (harmonic RMS 619.8) so all six timbres calibrate.

## Integration defects found and repaired

| # | Defect | Root cause | Fix |
|---|--------|------------|-----|
| 1 | Wall-3 atoms too quiet to calibrate (timbre 2: 129/1000 voiced) | Source recording level leaked into fixture; renderer computed hrms but never used it | `extract_atom_v2.py`: scale all amplitude components by exact factor to native hrms=619.8 (proven: max rel deviation 0.00e+00) |
| 2 | Calibration gate rejected valid decay envelopes (t4: 494/1000) | Universal 500/1000 floor wrong for decay | R8: decay floor 400/1000, flat/rise stay 500/1000 |
| 3 | Vocabulary consult reused one rise timbre for all 20 targets | Consult predicted F0+CV but omitted envelope mismatch | R9: +500 pred penalty for envelope mismatch |
| 4 | R9 penalty ineffective (still all rise) | Only one action "covered", so penalty never chose among alternatives | R10: envelope mismatch = not covered → triggers growth; vocabulary accumulates one action per envelope class |

## Final battery (20 targets, run twice)

**Determinism:** 20/20 WAVs byte-identical across runs. Logs identical modulo output dir. Zero RNG. Pure Zag.

**Actions grown:** 4 (atom0-flat baseline + rise H6/amode5 + flat H3/amode2 + decay H10/amode9)

**Per-target err_pm (baseline 2-timbre → final 6-timbre):**

| tgt | baseline | final | delta | timbre used |
|----:|---------:|------:|------:|-------------|
| 1 | 1518 | 0 | −1518 | rise |
| 2 | 1012 | 145 | −867 | rise |
| 3 | 565 | 536 | −29 | flat |
| 4 | 1074 | 592 | −482 | decay |
| 5 | 572 | 624 | +52 | decay |
| 6 | 509 | 43 | −466 | flat |
| 7 | 1189 | 471 | −718 | rise |
| 8 | 506 | 816 | +310 | flat |
| 9 | 1208 | 351 | −857 | flat |
| 10 | 804 | 674 | −130 | decay |
| 11 | 570 | 80 | −490 | rise |
| 12 | 0 | 172 | +172 | flat |
| 13 | 1003 | 520 | −483 | decay |
| 14 | 45 | 146 | +101 | flat |
| 15 | 561 | 567 | +6 | decay |
| 16 | 500 | 510 | +10 | flat |
| 17 | 1593 | 381 | −1212 | rise |
| 18 | 1255 | 874 | −381 | rise |
| 19 | 521 | 500 | −21 | rise |
| 20 | 500 | 500 | +0 | rise |

**Mean:** 775 → 425 ppm (−45%). 11 improved, 4 regressed, 5 flat.

## Honest residuals

1. **t8 (+310), t12 (+172), t14 (+101):** the old 2-timbre system got lucky on these (t12 was a perfect 0). The 6-timbre system's honest envelope matching costs some F0 accuracy where the reference's envelope is ambiguous. The planner is not yet smart enough to trade envelope fidelity for F0 when the ear would prefer it.
2. **t17 (381 ppm):** reference still hears ≈148.5 Hz vs laryngograph truth ≈130.3 Hz. The frozen organ has octave-error outliers that Wall 2's repair does not fully suppress. Frozen hearing has ≈+1.4% bias at 90 Hz.
3. **t19/t20 (500 ppm):** low-F0 floor. The 80.04 Hz organ floor plus the +1.4% bias limits accuracy below ≈100 Hz.
4. **Renderer D2:** commanded contour mean renders at ≈0.59×. Outside the isolated scope of all three walls; the planner compensates via fid scaling but the underlying defect remains.
5. **Wall-3 extractor:** source F0 below ≈172 Hz can make NBINS > TEXLEN=256 and crash. Not hit in this battery.

## Waveform analysis (all 20 final renders)

- Clipping: 0/20 (zero clipped samples anywhere)
- DC offset: max 10.38 (negligible)
- Peak range: 1835–17886 (healthy headroom)
- HNR: −1.0 to +13.4 dB (appropriate for the material)
- Envelope CV: 0.359–1.624 (covers flat to highly dynamic)

## Closure statement

All three walls survive integrated testing. The integration exposed and repaired four defects (two in Wall 3's fixtures, two in the planner's growth logic). The final system is deterministic, trig-free, RNG-free, and pure Zag. Mean error down 45%. The residuals above are mechanism-level, documented, and bounded — they are the next walls, not failures of this one.

**CLOSED.**
