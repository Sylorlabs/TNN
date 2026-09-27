# De-synth battery verdict — 2026-09-27

Planner: `plan_main_desynth.zag` (two-timbre atom calibration, atom-selection
growth, atom-coverage closed loop). Renderer: atom-stack renderer, zero
oscillators/FM/synth primitives in the planner production path.

## What was built and tested (the 5 gaps)

| # | Gap (Micah 2026-09-26) | Status |
|---|---|---|
| 1 | Replace FM calibration with atom/f0-bias calibration | DONE — two-timbre calibration (f0 bias @90/220/1010 Hz, CV yield @220 Hz, voiced fraction). See CALIBRATION.md |
| 2 | Replace FM planning/growth with atom-selection semantics | DONE — 4 candidates: atom0-flat, atom1-flat, atom0-contour, atom1-contour; growth = shootout + install; correction = atom reselect / contour-mean rescale / coverage findings |
| 3 | Run the complete 20-reference closed-loop battery | DONE — deep mode twice (see §1); fresh mode twice (see §1) |
| 4 | Apply LP coefficients or remove them honestly | DONE — REMOVED, honestly: atom format v2 drops the LP block; rationale recorded (period-averaged harmonic waveform already carries source coloration; LPC would double-color) |
| 5 | Validate or replace extractor 0.3 / renderer 0.5 | DONE — both replaced by explicitly-chosen unity: extractor texture normalized to peak 0.15, renderer mixes at 1.0 (effective 0.15, same as before, now honest) |

## 1. Battery runs

| Run | Mode | Result line | WAVs | Determinism |
|---|---|---|---|---|
| battery_deep1 | deep (depth=20, 4 iters/target) | `SUMMARY match=0 loop=20 targets=20 actions_grown=2` + `PLAN_DONE` | 80 | — |
| battery_deep2 | deep, rerun | identical summary | 80 | **80/80 WAVs byte-identical** to deep1; logs differ only in outdir path |
| battery_fresh1 | fresh (depth=0, 4 iters/target) | `SUMMARY match=0 loop=20 targets=20 actions_grown=1` + `PLAN_DONE` | 80 | per-target err_pm identical to deep on all 20 targets |
| battery_fresh2 | fresh, rerun | identical summary | 80 | **80/80 WAVs byte-identical** to battery_fresh1 |

`match=0` counts open-loop `M`-kind targets; the manifest holds 20 `L`
(loop) targets, so `match=0 / loop=20 / targets=20` is the exact result — it is
NOT a quality pass and must not be called one.

Note: fresh mode (vocabulary+history reset per target) reproduces deep mode's
per-target err_pm on all 20 targets exactly — cross-target accumulation does
not change per-target outcomes here.

Per-target final-iteration native error (`err_pm` = f0 term + CV term + env
term, per mille):

| tgt | ref (short) | plan (f0/amode) | df0 (Hz, organ) | env_ok | err_pm |
|---|---|---|---|---|---|
| 1 | lowf0-016 | 150.1 / contour | −77.8 | 0 | 1518 |
| 2 | field-100019 | 150.5 / contour | +1.8 | 0 | 1012 |
| 3 | speech-022 | 145.9 / contour | +9.5 | 1 | 565 |
| 4 | speech-001 | 158.3 / contour | +11.8 | 0 | 1074 |
| 5 | mir1k-bug_5 | 191.4 / contour | +13.9 | 0 | 572 |
| 6 | ravdess-17 | 180.1 / contour | −1.7 | 1 | 509 |
| 7 | emov-Amused | 220.8 / contour | −41.9 | 0 | 1189 |
| 8 | emov-Disgusted | 234.7 / contour | −1.6 | 1 | 506 |
| 9 | emov-Sleepy | 254.2 / contour | −53.0 | 0 | 1208 |
| 10 | cremad-DIS | 242.8 / contour | +74.0 | 0 | 804 |
| 11 | ravdess-24 | 286.7 / contour | +20.1 | 0 | 570 |
| 12 | tau-airport | 376.5 / contour | −0.0 | 1 | **0** |
| 13 | ravdess-18 | 379.7 / contour | +1.3 | 0 | 1003 |
| 14 | usn-roos | 520.6 / contour | +23.5 | 1 | 45 |
| 15 | field-100036 | 754.1 / contour | +46.7 | 0 | 561 |
| 16 | field-100039 | 1010.8 / contour | −0.8 | 1 | 500 |
| 17 | lowf0-022 | 152.5 / contour | −90.5 | 0 | 1593 |
| 18 | lowf0-012 | 146.0 / contour | −37.4 | 0 | 1255 |
| 19 | lowf0-027 | 407.4 / contour | −8.8 | 0 | 521 |
| 20 | lowf0-020 | 890.2 / **flat** | +0.3 | 0 | 500 |

Growth converged: 19/20 targets selected atom0-contour; t20 (heard 890 Hz,
voiced_frac 18/1000) selected atom0-flat. Vocabulary grew 2 actions.

## 2. Waveform analysis (40 files: final render + ref per target)

Analyzer: `src/waveform_full.py` (peak/RMS/DC/clipping, 10 ms envelope stats,
autocorrelation f0 + HNR, spectrum + top peaks, first/last-third spectral
drift, 50/60 Hz band energy, ZCR, onset count). Full table:
`evidence/waveform_battery2.tsv`.

| Measure | Renders (20) | References (20) |
|---|---|---|
| Peak | 1634–1966 | — |
| RMS | 612–714 | — |
| DC (max abs) | 1.61 samples | — |
| Clipping (samples ≥ 32760) | **0 everywhere** | — |
| Envelope CV (10 ms) | 0.359–0.414 | 0.298–1.922 |
| HNR | −1.3 … 13.5 dB (2× analyzer −inf, see §5) | −4.2 … 12.4 dB, mean 2.8 dB |
| ZCR/sec | 114–1950 | 962–8796 |
| Spectral drift (dom, 1st→3rd third) | ≤ 33 Hz typical; 6 contour targets drift more (see §4) | — |

Render envelope CV sits in a narrow 0.359–0.414 band on ALL targets — it is the
atom's own trajectory, time-warped. There is no envelope actuator by design
(synthetic envelopes are banned), so envelope mismatch is reported as a
coverage finding: 14/20 targets carry the 500 pm env term. The 2-atom
vocabulary cannot cover the references' envelope variety (ref CV up to 1.922).

## 3. Clean bills

- **No clipping, no DC**: 0 clipped samples, max |DC| 1.61 samples across 20 renders.
- **No mains hum from the renderer**: flat 220 Hz render measures −66.9 dB @60 Hz,
  −55.4 dB @120 Hz. The −14…−21 dB 60 Hz-band readings on t1/t7/t17/t18 renders
  are the planned low pitch itself (dominant 45–75 Hz, contour dips to ~37 Hz),
  not interference.
- **Determinism**: deep battery byte-identical across two full runs (80/80).

## 4. Spectral drift (contour mode working as designed)

Six contour targets show large first→last-third dominant shifts (t5: 295→~660,
t8, t11, t15, t16, t19 up to 465 Hz). This is the measured 16-pt contour moving
— the design intent (render the reference's pitch movement), not a defect. But
see §5: the contour's *absolute level* is unreliable.

## 5. Known defects (measured, not hypothesized)

**D1 — The organ mis-hears low-f0 contour renders, and the closed loop chases
the mis-hearing.** Decisive measurements (t17, commanded contour mean 152.5 Hz):
independent high-resolution FFT shows the render's strongest peak at **88 Hz**
(harmonic series 88/178 — 88 cannot be a subharmonic of anything the organ
reported); the organ heard the same file at **221–243 Hz** (2.5–2.8× sharp).
The `f0-contour-mean-rescale` correction then multiplies the contour by
`f0h/f0dr` — a ratio built on the wrong number. Observed consequence (t1):
true render mean **132 Hz → 96 Hz** after one "correction", moving AWAY from
the 150 Hz target; the loop then held (R8 no-progress-hold contained further
damage). The growth-shootout "bias" (+37.5% on contour probes) is this same
hearing bias, misattributed to the timbre: the calibration measures the
organ's error, not the renderer's. **The native `err_pm` scoreboard itself is
therefore compromised for contour actions** — it is computed in the organ's
hearing space, where the sign of the f0 error can be wrong.
Recommended fix (follow-up work, not implemented here): calibrate hearing bias
separately from render bias; for contour actions use the analytically-known
rendered contour mean instead of re-hearing render f0; make the organ's f0
estimator robust on low-f0 harmonic stacks.

**D2 — Render achieves below commanded contour level.** t17: commanded mean
152.5 Hz, achieved dominant ~88 Hz (−42%). The 16-pt contour carries the
reference's dips; interpolation + f0base fallback on unvoiced frames drags the
effective mean down. The `hear()` level-anchor (added 2026-09-26) does not
fully correct it.

**D3 — t20: organ octave error on the reference.** `lowf0-ptdb-020` (true ~105
Hz, voiced_frac 18/1000) heard at 890.2 Hz. The planner faithfully rendered
890 Hz (df0 +0.3 Hz — the loop "succeeded" on a phantom). Hearing failure, not
planning failure.

**D4 — Analyzer edge cases (mine, not the render's).** t17/t18 report HNR
`-inf`/f0 0.0: the autocorr peak-picker's 60 Hz floor misses true periods
below it (render energy at ~37 Hz on contour dips) while periodicity strength
reads 0.84. Estimator range limit, documented here.

**D5 — Assembled-runtime trig.** Planner sources are clean, but the assembled
binary still links `cosr` from `organ_lib.zag` (Hann/DFT tables for the organ's
`analyze()`). Strict zero-trig assembled compliance needs a trig-free hearing
path. No exception approved.

**D6 — 90 Hz calibration point degenerate.** Organ hears nothing at 90 Hz for
either atom (f0 = 0); `bias90_ppm = 0` is a placeholder. Low-pitch calibration
is unanchored.

## 6. Banned-primitive audit

- `plan_main_desynth.zag`: no active `cosr`/`sinr`/`exp10`/`fmix32`/hash-jitter/
  synthetic-envelope definitions or calls (removed 2026-09-27; `exp10`, `mul32`,
  `fmix32` defs+calls deleted).
- `render_desynth.zag`, `desynth_render.zag` (corrected): no banned primitives;
  v2 atoms only; unity texture mix; transients honestly disabled.
- Residual: assembled binary links organ `cosr` (D5 above). Not claimed clean.

## 7. Verdict

**Built and tested; not quality-passing.** The five assigned gaps are closed
with evidence: atom calibration replaces FM calibration, atom selection
replaces FM growth, the 20-reference battery ran complete in both modes with
byte-identical determinism, LP is honestly removed, texture/mix levels are
explicitly chosen rather than smuggled. One target (t12) reached err_pm=0;
fourteen carry envelope mismatch the 2-atom vocabulary cannot cover; the
closed loop's f0 correction is unreliable on contour renders (D1 — the
organ's hearing error, measured decisively, with a concrete recommended fix).
No audio is delivered for listening and no quality-pass claim is made: the
renders are deterministic harmonic-stack reconstructions with the documented
defects above. The next work is D1 (hearing-bias separation), D5 (trig-free
hearing path), and vocabulary growth — in that order.
