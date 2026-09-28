# Low-F0 characterization — wiring layer estimator (f0low.zag)

## What was built
The frozen organ's YIN F0 (lags 36..551, Hann-windowed) cannot resolve below
~125 Hz on real material (PREREG_LH §4, measured). The wiring layer adds a
low-band estimator consulted ONLY when the organ reports unvoiced-but-loud or
F0 < 125 Hz:
- Mean-removed UNWINDOWED frames (P's finding: plain autocorr argmax fails
  80–112 Hz specifically under the Hann window).
- YIN cumulative-mean-normalized difference, lag range extended to sr/55,
  pre-roll from lag 1 (mirrors the organ's proven structure).
- Confidence gate (r[sel]/r0 ≥ 0.35), half-lag octave gate (ambiguous, never
  confident-wrong), hard floor: <55 Hz → below-floor/unvoiced.
- `scope` mode: strict range restriction (organ <125 Hz → forced unvoiced/0).

## Synthetic characterization (harmonic tones [1.0, 0.30, 0.10], 44.1 kHz, 2 s)
18 tones, 40–125 Hz, 85 frames each, `emit_desc probe`:

| f0 (Hz) | confident | median err | p90 err | % frames ≤5% |
|---|---|---|---|---|
| 40 | 0/85 (unvoiced) | — | — | — (below floor) |
| 45 | 0/85 (unvoiced) | — | — | — (below floor) |
| 50 | 0/85 (unvoiced) | — | — | — (below floor) |
| 55 | 85/85 | 1.98% | 4.08% | 100% |
| 60 | 85/85 | 2.24% | — | 100% |
| 65 | 85/85 | 1.55% | — | 100% |
| 70 | 85/85 | 1.34% | — | 100% |
| 75 | 85/85 | 1.51% | — | 100% |
| 80 | 85/85 | 1.17% | 2.29% | 100% |
| 85–120 | 85/85 | 0.8–1.2% | — | 100% |
| 125 | 85/85 | 0.23% | 0.23% | 100% |

Per-band (prereg): 55–80 Hz max err 4.62%; 80–100 Hz max 2.41%; 100–125 Hz
max 1.86%. All bands: 100% of voiced frames within 5%.

## Verdict vs prereg bars
- **FIXED (synthetic)**: floor 55 Hz ≤ 65 Hz ✓; ≤5% error on ≥90% voiced
  frames (100% observed 55–125 Hz) ✓; per-band results above ✓; P-R4
  regression check: pr4/env/bands/rms/zcr are the frozen organ's unguarded
  aggregates (untouched by the guard) — P-R4 anchor preserved by construction.
- **FIXED (real)**: OPEN — no real 55–125 Hz corpus with ground-truth F0
  labels exists in the lab. Not claimed.
- **SCOPING (real)**: OPEN — fewer than 50 real sub-125 Hz clips available.
  The `scope` mechanism is implemented; the ≥50-clip bar is not met.
- **No-silent-misread (mechanism)**: below 55 Hz the estimator reports
  unvoiced/0 (lag range physically excludes it) — never a confident wrong F0.
  On the 40 Hz synthetic tone: 85/85 unvoiced, 0 confident-wrong.

## Known limitation
Systematic sharp bias +1–4% (worse at low F0), from the 46 ms frame holding
<3 periods below ~65 Hz. Within the 5% bar at ≥55 Hz; documented, not hidden.
